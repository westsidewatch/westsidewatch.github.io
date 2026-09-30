#!/usr/bin/env python3
"""Resolve Dawn cover authority without downloading cover images.

Dawn Library is Christian/Biblical in religious scope. General secular works may
remain, but works whose primary subject is another religion are excluded before
cover resolution and never surface in the public cover stream.
"""
from __future__ import annotations
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import quote
from urllib.error import HTTPError, URLError
import argparse, json, re, time

ROOT=Path(__file__).resolve().parents[1]
PREVIEW=ROOT/'static/dawn-library/cover-preview'
OUT=ROOT/'static/dawn-library/cover-authority'
UA='WestsideWatch-DawnLibrary/1.0 (cover authority resolver)'

# Deliberately religion-specific, not ethnic/cultural. Do not exclude generic
# words such as Jewish/Israel/Arabic/Indian because they are not sufficient.
OTHER_RELIGION_PATTERNS=[
 r'\bbuddh(?:a|ism|ist|ist?s)\b', r'\bdharma\b', r'\bdalai lama\b', r'\brinpoche\b', r'\blama\b', r'\btibetan buddh', r'\bzen buddh',
 r'\bhindu(?:ism)?\b', r'\bvedas?\b', r'\bupanishad', r'\bbhagavad\s*gita\b', r'\bkrishna\b', r'\bvaishnav', r'\bshaiv',
 r'\bislam(?:ic)?\b', r'\bmuslim\b', r'\bqur[\'’]?an\b', r'\bkoran\b', r'\bmuhammad\b', r'\bsufi(?:sm)?\b',
 r'\bsikh(?:ism)?\b', r'\bguru granth\b', r'\bjain(?:ism)?\b', r'\bshinto\b', r'\btao(?:ism|ist)\b', r'\bdao(?:ism|ist)\b',
 r'\bconfucian(?:ism)?\b', r'\bzoroastr', r'\bbah[aá][’\']?i\b', r'\bscientology\b', r'\bneo[- ]?pagan', r'\bwicca\b'
]
OTHER_RELIGION_RE=re.compile('|'.join(OTHER_RELIGION_PATTERNS),re.I)


def get_json(url,retries=3):
    for attempt in range(retries):
        try:
            with urlopen(Request(url,headers={'User-Agent':UA}),timeout=20) as r:return json.load(r)
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


def text_blob(item,meta=None):
    bits=[item.get('title',''),*(item.get('authors') or [])]
    if meta:
        bits.extend(meta.get('subjects') or [])
        desc=meta.get('description')
        if isinstance(desc,dict):desc=desc.get('value','')
        if isinstance(desc,str):bits.append(desc[:2000])
    return ' '.join(str(x) for x in bits if x)


def other_religion(item,meta=None):
    return bool(OTHER_RELIGION_RE.search(text_blob(item,meta)))


def resolve(item,allow_editions=True):
    wid=str(item.get('workId') or '')
    if other_religion(item):return {'workId':wid,'status':'excluded','reason':'other-religion'}
    c=item.get('cover') or {}
    ol=wid if wid.startswith('OL') and wid.endswith('W') else None
    lookup=c.get('workLookup') or (f'https://openlibrary.org/works/{quote(ol)}.json' if ol else None)
    meta=get_json(lookup) if lookup else None
    if other_religion(item,meta):return {'workId':wid,'status':'excluded','reason':'other-religion'}
    if c.get('source') in ('open-library-cover-id','open-library-edition','canonical') and c.get('src'):
        return {'workId':wid,'coverUrl':c['src'],'source':c['source'],'status':'resolved'}
    cover_id=positive_cover((meta or {}).get('covers'))
    if cover_id:return {'workId':wid,'coverId':cover_id,'coverUrl':f'https://covers.openlibrary.org/b/id/{cover_id}-M.jpg?default=false','source':'open-library-work','status':'resolved'}
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
    ap=argparse.ArgumentParser();ap.add_argument('--shard',type=int,default=1);ap.add_argument('--limit',type=int,default=500);ap.add_argument('--delay',type=float,default=.12);ap.add_argument('--no-editions',action='store_true');args=ap.parse_args()
    source=PREVIEW/f'covers-{args.shard:06d}.json';data=json.loads(source.read_text(encoding='utf-8'));rows=(data.get('items') or [])[:max(1,args.limit)]
    OUT.mkdir(parents=True,exist_ok=True);results=[]
    for n,row in enumerate(rows,1):
        results.append(resolve(row,not args.no_editions))
        if n<len(rows):time.sleep(args.delay)
    resolved=sum(x['status']=='resolved' for x in results);excluded=sum(x['status']=='excluded' for x in results);eligible=len(results)-excluded
    payload={'schema':'dawn.library.cover-authority.v2','sourceShard':args.shard,'sampleCount':len(results),'eligibleCount':eligible,'excludedCount':excluded,'resolvedCount':resolved,'hitRate':round(resolved/eligible,4) if eligible else 0,'items':results}
    target=OUT/f'authority-{args.shard:06d}.json';target.write_text(json.dumps(payload,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8')
    print(json.dumps({'status':'PASS','target':str(target.relative_to(ROOT)),'sampleCount':len(results),'eligibleCount':eligible,'excludedCount':excluded,'resolvedCount':resolved,'hitRate':payload['hitRate']},ensure_ascii=False))

if __name__=='__main__':main()
