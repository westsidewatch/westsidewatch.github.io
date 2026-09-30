#!/usr/bin/env python3
"""Build Dawn Library catalogue-v3 beside production.

One pass: current holdings -> Christian gate evidence -> normalize -> indexes ->
immutable shards. Never writes static/dawn-library/catalogue.
"""
from __future__ import annotations
import hashlib,json,re
from collections import defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'static/dawn-library/catalogue'
OUT=ROOT/'static/dawn-library/catalogue-v3'
SHARD=250
HAN=re.compile(r'[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]')
EXCLUDE=('buddh','hindu','islam','muslim','quran','koran','tao','daoism','new age','theosoph','occult','yoga')
CHRISTIAN=('christ','jesus','bible','biblical','church','theolog','gospel','sermon','devotion','spiritual','prayer','catholic','orthodox','protestant','reformed','puritan','patrist','augustine','luther','calvin')

def load(p): return json.loads(p.read_text(encoding='utf-8'))
def norm(v): return re.sub(r'\s+',' ',str(v or '')).strip()
def text(w):
    bits=[w.get('title'),w.get('creator'),w.get('date')]
    for k in ('subjects','languages'):
        v=w.get(k,[]); bits.extend(v if isinstance(v,list) else [v])
    return ' '.join(norm(x) for x in bits if x).casefold()
def gate(w):
    t=text(w); bad=[x for x in EXCLUDE if x in t]; good=[x for x in CHRISTIAN if x in t]
    if bad and not good:return 'exclude',bad
    if bad and good:return 'review',bad+good
    return 'admit',good
def authorities(w):
    out={}
    existing=w.get('authorityIds') or {}
    if isinstance(existing,dict):
        for k,v in existing.items(): out[k]=v if isinstance(v,list) else [v]
    for s in w.get('sources') or []:
        src=norm(s.get('source')).casefold() or 'source'; sid=norm(s.get('sourceId'))
        if sid: out.setdefault('source:'+src,[]).append(sid)
        for k,v in (s.get('identifiers') or {}).items():
            vals=v if isinstance(v,list) else [v]
            out.setdefault(str(k),[]).extend(norm(x) for x in vals if norm(x))
    return {k:list(dict.fromkeys(v)) for k,v in out.items() if v}
def lang(w):
    vals=w.get('languages') or w.get('language') or []
    if isinstance(vals,str):vals=[vals]
    s=' '.join(map(str,vals)).casefold()
    if any(x in s for x in ('chi','zho','zh','chinese','中文','漢','汉')) or HAN.search(text(w)):return 'zh'
    return norm(vals[0]).casefold() if vals else 'unknown'
def cover_locator(a):
    priority=('olid','isbn','oclc','lccn','cover','cover_i')
    flat={str(k).casefold():v for k,v in a.items()}
    for k in priority:
        vals=flat.get(k)
        if vals:return {'authority':k,'value':vals[0]}
    for k,vals in flat.items():
        if 'openlibrary' in k and vals:return {'authority':'olid','value':vals[0]}
    return None
def main():
    idx=load(SRC/'index.json'); works=[]; seen=set(); excluded=[]; review=[]
    indexes={k:defaultdict(list) for k in ('language','author','era','tradition','subject','type')}
    for page in idx['pages']:
        for raw in load(SRC/page).get('works',[]):
            iid=norm(raw.get('internalId') or raw.get('id'))
            if not iid or iid in seen:continue
            seen.add(iid); decision,evidence=gate(raw)
            if decision=='exclude':excluded.append({'id':iid,'evidence':evidence});continue
            if decision=='review':review.append({'id':iid,'evidence':evidence})
            a=authorities(raw); language=lang(raw); subjects=(raw.get('subjects') or [])[:24]
            rec={'id':iid,'title':norm(raw.get('title')),'creator':norm(raw.get('creator')),'date':raw.get('date'),'century':raw.get('century'),'language':language,'subjects':subjects,'authorityIds':a,'cover':cover_locator(a),'sources':raw.get('sources') or []}
            works.append(rec);indexes['language'][language].append(iid)
            if rec['creator']:indexes['author'][rec['creator']].append(iid)
            if rec['century']:indexes['era'][str(rec['century'])].append(iid)
            for s in subjects:indexes['subject'][norm(s)].append(iid)
    OUT.mkdir(parents=True,exist_ok=True)
    for old in OUT.glob('works-*.json'):old.unlink()
    shards=[]
    for n,start in enumerate(range(0,len(works),SHARD),1):
        name=f'works-{n:06d}.json';chunk=works[start:start+SHARD]
        (OUT/name).write_text(json.dumps({'schema':'dawn-catalogue-v3/shard','works':chunk},ensure_ascii=False,separators=(',',':')),encoding='utf-8');shards.append(name)
    for name,m in indexes.items():
        (OUT/f'index-{name}.json').write_text(json.dumps({'schema':'dawn-catalogue-v3/index','facet':name,'values':m},ensure_ascii=False,separators=(',',':')),encoding='utf-8')
    chinese=len(indexes['language'].get('zh',[]));covers=sum(bool(w['cover']) for w in works);authority=sum(bool(w['authorityIds']) for w in works)
    manifest={'schema':'dawn-library-catalogue/v3','sourceCount':idx.get('count'),'admittedCount':len(works),'excludedCount':len(excluded),'reviewCount':len(review),'chineseCount':chinese,'authorityBackedCount':authority,'coverAuthorityCount':covers,'shardSize':SHARD,'shards':shards,'indexes':[f'index-{x}.json' for x in indexes]}
    manifest['buildId']=hashlib.sha256(json.dumps(manifest,sort_keys=True).encode()).hexdigest()[:16]
    (OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
    (OUT/'audit.json').write_text(json.dumps({'excluded':excluded,'review':review},ensure_ascii=False,separators=(',',':')),encoding='utf-8')
    print(json.dumps(manifest,ensure_ascii=False))
    if idx.get('count') and len(seen)!=idx['count']:raise SystemExit(f"source count mismatch: {len(seen)} != {idx['count']}")
if __name__=='__main__':main()
