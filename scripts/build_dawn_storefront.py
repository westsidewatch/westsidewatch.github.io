#!/usr/bin/env python3
import json,re,urllib.parse,urllib.request,xml.etree.ElementTree as ET
from datetime import datetime,timezone
from html import unescape
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'static/dawn-library/storefront.json'
REPORT=ROOT/'reports/DAWN-LIBRARY-STOREFRONT.json'
UA='Dore-Dawn-Library/1.0 (+https://westsidewatch.github.io)'
ATOM='http://www.w3.org/2005/Atom';NS={'atom':ATOM}
now=datetime.now(timezone.utc).isoformat()

def request(url,accept='*/*'):
    return urllib.request.Request(url,headers={'User-Agent':UA,'Accept':accept})
def fetch_xml(url,accept='application/atom+xml,application/xml;q=0.9,*/*;q=0.5'):
    with urllib.request.urlopen(request(url,accept),timeout=30) as r:return ET.fromstring(r.read())
def fetch_text(url):
    with urllib.request.urlopen(request(url,'text/html,application/xhtml+xml;q=0.9,*/*;q=0.5'),timeout=20) as r:return r.read(350000).decode('utf-8','replace')
def clean(s):return re.sub(r'\s+',' ',(s or '')).strip()
def http_image(url):return url if isinstance(url,str) and url.startswith(('https://','http://')) else ''
def page_cover(url):
    try:
        html=fetch_text(url)
        patterns=[r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)',r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image["\']']
        for p in patterns:
            m=re.search(p,html,re.I)
            if m:return http_image(unescape(m.group(1)))
    except Exception:pass
    return ''

def gutenberg_shelf(label,query,limit=36):
    root=fetch_xml('https://www.gutenberg.org/ebooks/search.opds/?'+urllib.parse.urlencode({'query':query}));items=[]
    for e in root.findall('atom:entry',NS):
        title=clean(e.findtext('atom:title',default='',namespaces=NS));a=e.find('atom:author/atom:name',NS);author=clean(a.text) if a is not None else ''
        eid=clean(e.findtext('atom:id',default='',namespaces=NS));gid='';m=re.search(r'(\d+)(?:/)?$',eid)
        if m:gid=m.group(1)
        links=e.findall('atom:link',NS)
        if not gid:
            for ln in links:
                mm=re.search(r'/ebooks/(\d+)',ln.attrib.get('href',''))
                if mm:gid=mm.group(1);break
        if not gid or not title:continue
        cover=''
        for ln in links:
            rel=ln.attrib.get('rel','');typ=ln.attrib.get('type','');href=http_image(ln.attrib.get('href',''))
            if href and ('image' in rel or typ.startswith('image/')):cover=href;break
        items.append({'id':f'gutenberg-{gid}','title':title,'author':author,'language':'en','source':{'provider':'Project Gutenberg','url':f'https://www.gutenberg.org/ebooks/{gid}','kind':'remote-public'},'cover':{'url':cover,'mode':'source'} if cover else {'mode':'one-fallback'},'rights':{'status':'public-domain-us','declaredBy':'Project Gutenberg'},'contentDownloaded':False})
        if len(items)>=limit:break
    return {'id':'gutenberg-'+re.sub(r'[^a-z0-9]+','-',query.lower()).strip('-'),'title':label,'kind':'source-shelf','source':'Project Gutenberg','items':items}

def standard_new_releases():
    root=fetch_xml('https://standardebooks.org/feeds/atom/new-releases');items=[]
    for e in root.findall('atom:entry',NS):
        title=clean(e.findtext('atom:title',default='',namespaces=NS));names=[clean(a.text) for a in e.findall('atom:author/atom:name',NS) if clean(a.text)];author=', '.join(names)
        href='';cover='';download=''
        for ln in e.findall('atom:link',NS):
            rel=ln.attrib.get('rel','');typ=ln.attrib.get('type','');u=ln.attrib.get('href','')
            if rel=='alternate' and not href:href=u
            if http_image(u) and ('image' in rel or typ.startswith('image/')) and not cover:cover=u
            if ('acquisition' in rel or typ=='application/epub+zip') and not download:download=u
        if not href:
            ident=clean(e.findtext('atom:id',default='',namespaces=NS));href=ident if ident.startswith('http') else ''
        if not title or not href:continue
        if not cover:cover=page_cover(href)
        slug=re.sub(r'[^a-z0-9]+','-',title.lower()).strip('-')[:64]
        items.append({'id':'standard-'+slug,'title':title,'author':author,'language':'en','source':{'provider':'Standard Ebooks','url':href,'downloadUrl':download or None,'kind':'remote-public-premium'},'cover':{'url':cover,'mode':'source'} if cover else {'mode':'one-fallback'},'rights':{'status':'public-domain-us','declaredBy':'Standard Ebooks'},'quality':'curated-edition','contentDownloaded':False})
    return {'id':'standard-ebooks-new','title':'精品書架 · Standard Ebooks','kind':'premium-shelf','source':'Standard Ebooks','items':items[:15]}

shelf_specs=[('聖經與基督教','bible christianity',40),('早期教會與教父','early church fathers',36),('猶太與第二聖殿世界','jewish history josephus',36),('古代世界與考古','ancient history archaeology',36),('哲學與思想','philosophy classics',36),('傳記與回憶','biography memoir',36)]
shelves=[];errors=[]
try:shelves.append(standard_new_releases())
except Exception as e:errors.append({'source':'Standard Ebooks','error':type(e).__name__+': '+str(e)[:160]})
for label,q,limit in shelf_specs:
    try:shelves.append(gutenberg_shelf(label,q,limit))
    except Exception as e:errors.append({'source':'Project Gutenberg','query':q,'error':type(e).__name__+': '+str(e)[:160]})
seen=set();total=0;cover_count=0
for shelf in shelves:
    dedup=[]
    for item in shelf['items']:
        if item['id'] in seen:continue
        seen.add(item['id']);dedup.append(item);cover_count+=1 if item.get('cover',{}).get('url') else 0
    shelf['items']=dedup;total+=len(dedup)
store={'schema':'dawn.library.storefront.v1','generatedAt':now,'title':'黎明書局','storagePolicy':'index-only','principle':'映射 ≠ 導入。閱讀 ≠ 收藏。收藏 ≠ 下載。','shelves':shelves,'metrics':{'shelves':len(shelves),'mappedBooks':total,'sourceCovers':cover_count},'errors':errors}
OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(store,ensure_ascii=False,indent=2)+'\n')
REPORT.parent.mkdir(parents=True,exist_ok=True);REPORT.write_text(json.dumps({'schema':'dawn.library.storefront.report.v2','generatedAt':now,'shelves':[{'id':s['id'],'title':s['title'],'books':len(s['items'])} for s in shelves],'mappedBooks':total,'sourceCovers':cover_count,'errors':errors,'contentDownloaded':False},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'mappedBooks':total,'sourceCovers':cover_count,'shelves':[(s['title'],len(s['items'])) for s in shelves],'errors':errors},ensure_ascii=False,indent=2))
