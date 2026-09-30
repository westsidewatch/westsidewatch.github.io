#!/usr/bin/env python3
"""Resolve Dawn cover authority without downloading cover images.

Builds a thin persistent index: workId -> coverId/edition/isbn/source.
Designed for bounded batches so Open Library is never used as a bulk backend.
"""
from __future__ import annotations
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import quote
from urllib.error import HTTPError, URLError
import argparse, json, time

ROOT=Path(__file__).resolve().parents[1]
PREVIEW=ROOT/'static/dawn-library/cover-preview'
OUT=ROOT/'static/dawn-library/cover-authority'
UA='WestsideWatch-DawnLibrary/1.0 (cover authority resolver)'


def get_json(url, retries=3):
    for attempt in range(retries):
        try:
            with urlopen(Request(url,headers={'User-Agent':UA}),timeout=20) as r:
                return json.load(r)
        except (HTTPError,URLError,TimeoutError,json.JSONDecodeError):
            if attempt+1==retries:return None
            time.sleep(1.5*(attempt+1))


def positive_cover(values):
    if not isinstance(values,list):return None
    for value in values:
        try:
            value=int(value)
            if value>0:return value
        except (TypeError,ValueError):pass
    return None


def resolve(item, allow_editions=True):
    wid=str(item.get('workId') or '')
    c=item.get('cover') or {}
    if c.get('source') in ('open-library-cover-id','open-library-edition','canonical') and c.get('src'):
        return {'workId':wid,'coverUrl':c['src'],'source':c['source'],'status':'resolved'}
    ol=wid if wid.startswith('OL') and wid.endswith('W') else None
    lookup=c.get('workLookup') or (f'https://openlibrary.org/works/{quote(ol)}.json' if ol else None)
    if not lookup:return {'workId':wid,'status':'unresolved'}
    meta=get_json(lookup)
    cover_id=positive_cover((meta or {}).get('covers'))
    if cover_id:
        return {'workId':wid,'coverId':cover_id,'coverUrl':f'https://covers.openlibrary.org/b/id/{cover_id}-M.jpg?default=false','source':'open-library-work','status':'resolved'}
    if allow_editions and ol:
        editions=get_json(f'https://openlibrary.org/works/{quote(ol)}/editions.json?limit=20') or {}
        for ed in editions.get('entries') or []:
            cover_id=positive_cover(ed.get('covers'))
            if cover_id:
                key=ed.get('key','').rsplit('/',1)[-1] or None
                isbn=(ed.get('isbn_13') or ed.get('isbn_10') or [None])[0]
                return {'workId':wid,'coverId':cover_id,'editionId':key,'isbn':isbn,'coverUrl':f'https://covers.openlibrary.org/b/id/{cover_id}-M.jpg?default=false','source':'open-library-edition','status':'resolved'}
    return {'workId':wid,'status':'unresolved'}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--shard',type=int,default=1);ap.add_argument('--limit',type=int,default=100);ap.add_argument('--delay',type=float,default=.12);ap.add_argument('--no-editions',action='store_true');args=ap.parse_args()
    source=PREVIEW/f'covers-{args.shard:06d}.json'
    data=json.loads(source.read_text(encoding='utf-8'))
    rows=(data.get('items') or [])[:max(1,args.limit)]
    OUT.mkdir(parents=True,exist_ok=True)
    results=[]
    for n,row in enumerate(rows,1):
        results.append(resolve(row,not args.no_editions))
        if n<len(rows):time.sleep(args.delay)
    resolved=sum(x['status']=='resolved' for x in results)
    payload={'schema':'dawn.library.cover-authority.v1','sourceShard':args.shard,'sampleCount':len(results),'resolvedCount':resolved,'hitRate':round(resolved/len(results),4) if results else 0,'items':results}
    target=OUT/f'authority-{args.shard:06d}.json'
    target.write_text(json.dumps(payload,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8')
    print(json.dumps({'status':'PASS','target':str(target.relative_to(ROOT)),'sampleCount':len(results),'resolvedCount':resolved,'hitRate':payload['hitRate']},ensure_ascii=False))

if __name__=='__main__':main()
