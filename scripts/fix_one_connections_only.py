#!/usr/bin/env python3
import json, re, urllib.request
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
ONE=ROOT/'static'/'one'
BIBLE_URL='https://raw.githubusercontent.com/m0ty/bible-io-json/main/Chinese/zho-cuv-trad-shen.json'
BOOKS=["創世記","出埃及記","利未記","民數記","申命記","約書亞記","士師記","路得記","撒母耳記上","撒母耳記下","列王紀上","列王紀下","歷代志上","歷代志下","以斯拉記","尼希米記","以斯帖記","約伯記","詩篇","箴言","傳道書","雅歌","以賽亞書","耶利米書","耶利米哀歌","以西結書","但以理書","何西阿書","約珥書","阿摩司書","俄巴底亞書","約拿書","彌迦書","那鴻書","哈巴谷書","西番雅書","哈該書","撒迦利亞書","瑪拉基書","馬太福音","馬可福音","路加福音","約翰福音","使徒行傳","羅馬書","哥林多前書","哥林多後書","加拉太書","以弗所書","腓立比書","歌羅西書","帖撒羅尼迦前書","帖撒羅尼迦後書","提摩太前書","提摩太後書","提多書","腓利門書","希伯來書","雅各書","彼得前書","彼得後書","約翰一書","約翰二書","約翰三書","猶大書","啟示錄"]
ALIASES={b:b for b in BOOKS}
ALIASES.update({"創":"創世記","出":"出埃及記","利":"利未記","民":"民數記","申":"申命記","書":"約書亞記","士":"士師記","得":"路得記","撒上":"撒母耳記上","撒下":"撒母耳記下","王上":"列王紀上","王下":"列王紀下","代上":"歷代志上","代下":"歷代志下","拉":"以斯拉記","尼":"尼希米記","斯":"以斯帖記","伯":"約伯記","詩":"詩篇","箴":"箴言","傳":"傳道書","歌":"雅歌","賽":"以賽亞書","耶":"耶利米書","哀":"耶利米哀歌","結":"以西結書","但":"但以理書","何":"何西阿書","珥":"約珥書","摩":"阿摩司書","俄":"俄巴底亞書","拿":"約拿書","彌":"彌迦書","鴻":"那鴻書","哈":"哈巴谷書","番":"西番雅書","該":"哈該書","亞":"撒迦利亞書","瑪":"瑪拉基書","太":"馬太福音","可":"馬可福音","路":"路加福音","約":"約翰福音","徒":"使徒行傳","羅":"羅馬書","林前":"哥林多前書","林後":"哥林多後書","加":"加拉太書","弗":"以弗所書","腓":"腓立比書","西":"歌羅西書","帖前":"帖撒羅尼迦前書","帖後":"帖撒羅尼迦後書","提前":"提摩太前書","提後":"提摩太後書","多":"提多書","門":"腓利門書","來":"希伯來書","雅":"雅各書","彼前":"彼得前書","彼後":"彼得後書","約一":"約翰一書","約二":"約翰二書","約三":"約翰三書","猶":"猶大書","啟":"啟示錄"})
TARGET=re.compile(r'^(?:genesis-(?:core|\d.*)|samuel-(?:core|chapters-.*)|samuel2-(?:core|chapters-.*)|psalms-(?:core|\d.*)|matthew-complete|mark-(?:core|\d.*)|luke-(?:core|\d.*)|john-(?:core|\d.*)|thessalonians-complete)\.js$')
STR=r'"(?:\\.|[^"\\])*"'
ENTRY=re.compile(r'\[(?P<ref>'+STR+r')\s*,\s*(?P<title>'+STR+r')(?P<third>\s*,\s*'+STR+r')?\s*\]')

def compact(s): return re.sub(r'\s+','',s).replace('﹐','，')
def verse(book,c,v):
    try:return compact(book['chapters'][str(c)][str(v)])
    except KeyError:return None
def chapter(book,c): return [(int(k),compact(v)) for k,v in book['chapters'].get(str(c),{}).items()]
def vrange(book,c1,v1,c2,v2,limit=18):
    out=[]
    for c in range(c1,c2+1):
        for v,t in chapter(book,c):
            if c==c1 and v<v1:continue
            if c==c2 and v>v2:continue
            out.append(t)
            if len(out)>=limit:return out,True
    return out,False

def resolve_loc(book,loc):
    loc=loc.strip().replace('：',':').replace('—','-').replace('–','-').replace('－','-').replace('至','-').replace('節','')
    m=re.fullmatch(r'(\d+):(\d+)-(\d+):(\d+)',loc)
    if m:
        a,b,c,d=map(int,m.groups());x,tr=vrange(book,a,b,c,d);return ''.join(x)+('……' if tr else '') if x else None
    m=re.fullmatch(r'(\d+):([\d、,\-]+)',loc)
    if m and ('、' in m.group(2) or ',' in m.group(2)):
        c=int(m.group(1));out=[]
        for token in re.split(r'[、,]',m.group(2)):
            if '-' in token:
                a,b=map(int,token.split('-',1));x,_=vrange(book,c,a,c,b,50);out+=x
            else:
                t=verse(book,c,int(token))
                if t is None:return None
                out.append(t)
        return ''.join(out) if out else None
    m=re.fullmatch(r'(\d+):(\d+)(?:-(\d+))?',loc)
    if m:
        c=int(m.group(1));a=int(m.group(2));b=int(m.group(3) or a);x,tr=vrange(book,c,a,c,b);return ''.join(x)+('……' if tr else '') if x else None
    loc=loc.replace('章','').replace('篇','')
    if len(book['chapters'])==1:
        m=re.fullmatch(r'(\d+)-(\d+)',loc)
        if m:
            a,b=map(int,m.groups());x,tr=vrange(book,1,a,1,b);return ''.join(x)+('……' if tr else '') if x else None
    m=re.fullmatch(r'(\d+)(?:-(\d+))?',loc)
    if m:
        c1=int(m.group(1));c2=int(m.group(2) or c1);out=[];tr=False
        for c in range(c1,c2+1):
            for _,t in chapter(book,c):
                out.append(t)
                if len(out)>=18:tr=True;break
            if tr:break
        return ''.join(out)+('……' if tr else '') if out else None
    return None

def parse_seg(seg,current=None):
    seg=seg.strip()
    for name in sorted(ALIASES,key=len,reverse=True):
        if seg.startswith(name):
            loc=seg[len(name):].strip()
            if loc and loc[0].isdigit():return ALIASES[name],loc
    if current and seg and seg[0].isdigit():return current,seg
    return None,None

def resolve(ref,bookmap):
    cur=None;out=[]
    for seg in re.split(r'[；;]',ref):
        b,loc=parse_seg(seg,cur)
        if not b:return None
        cur=b;t=resolve_loc(bookmap[b],loc)
        if not t:return None
        out.append(t)
    return '……'.join(out)

def array_end(src,start):
    depth=0;quote=None;esc=False
    for i in range(start,len(src)):
        ch=src[i]
        if quote:
            if esc:esc=False
            elif ch=='\\':esc=True
            elif ch==quote:quote=None
            continue
        if ch in ('"',"'",'`'):quote=ch;continue
        if ch=='[':depth+=1
        elif ch==']':
            depth-=1
            if depth==0:return i
    raise ValueError('unclosed connections array')

def main():
    with urllib.request.urlopen(BIBLE_URL,timeout=30) as r:bible=json.load(r)
    keys=list(bible['books'])
    if len(keys)!=66:raise SystemExit('Bible corpus does not contain 66 books')
    bookmap={name:bible['books'][k] for name,k in zip(BOOKS,keys)}
    fixed=scanned=blocks=changed_files=0;unresolved=[]
    for path in sorted(ONE.glob('*.js')):
        if not TARGET.match(path.name):continue
        src=path.read_text(encoding='utf-8');pos=0;pieces=[];changed=False
        while True:
            m=re.search(r'\bconnections\s*:\s*\[',src[pos:])
            if not m:break
            open_i=pos+m.end()-1;close_i=array_end(src,open_i);blocks+=1
            body=src[open_i+1:close_i]
            def repl(x):
                nonlocal fixed,scanned
                ref=json.loads(x.group('ref'));title=json.loads(x.group('title'));scanned+=1
                b,_=parse_seg(ref)
                if not b:
                    unresolved.append((path.name,ref,'not a Scripture reference'));return x.group(0)
                text=resolve(ref,bookmap)
                if not text:
                    unresolved.append((path.name,ref,'unresolved'));return x.group(0)
                old=json.loads(x.group('third').split(',',1)[1].strip()) if x.group('third') else None
                if old==text:return x.group(0)
                fixed+=1
                return '['+json.dumps(ref,ensure_ascii=False)+','+json.dumps(title,ensure_ascii=False)+','+json.dumps(text,ensure_ascii=False)+']'
            newbody=ENTRY.sub(repl,body)
            if newbody!=body:
                pieces.append((open_i+1,close_i,newbody));changed=True
            pos=close_i+1
        for a,b,newbody in reversed(pieces):src=src[:a]+newbody+src[b:]
        if changed:path.write_text(src,encoding='utf-8');changed_files+=1
    print(f'blocks={blocks} scanned={scanned} fixed={fixed} changed_files={changed_files}')
    if unresolved:
        for row in unresolved:print('UNRESOLVED',*row,sep='\t')
        raise SystemExit(f'Unresolved connection entries: {len(unresolved)}')
    if scanned==0:raise SystemExit('No connection entries found')

if __name__=='__main__':main()
