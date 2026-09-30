#!/usr/bin/env python3
"""Build lightweight, motion-ready cover-preview shards from Dawn canonical Works.

The generated surface is deliberately presentation-neutral: layout and motion are
consumers of stable canonical cover objects, not part of the data build.
"""
from __future__ import annotations
from pathlib import Path
from urllib.parse import quote
import hashlib, json

ROOT=Path(__file__).resolve().parents[1]
CANONICAL=ROOT/'static/dawn-library/canonical'
OUT=ROOT/'static/dawn-library/cover-preview'


def work_array(payload):
    if isinstance(payload,list): return payload
    if isinstance(payload,dict):
        for key in ('works','items','entries'):
            collection=payload.get(key)
            if isinstance(collection,list): return collection
            if isinstance(collection,dict):
                rows=[]
                for canonical_id, work in collection.items():
                    if not isinstance(work,dict): continue
                    if not (work.get('workId') or work.get('id')):
                        work=dict(work)
                        work['workId']=canonical_id
                    rows.append(work)
                return rows
        vals=[v for v in payload.values() if isinstance(v,dict)]
        if vals: return vals
    raise ValueError('canonical shard has no Work collection')


def strings(v):
    if v is None:return []
    if isinstance(v,str):return [v]
    if isinstance(v,list):return [str(x) for x in v if x]
    if isinstance(v,dict):return [str(x) for x in v.values() if x]
    return [str(v)]


def cover(work):
    for key in ('coverPreview','coverUrl','coverURL','cover','thumbnail','thumbnailUrl'):
        v=work.get(key)
        if isinstance(v,str) and v.startswith(('https://','http://','/')):return {'src':v,'source':'canonical'}
        if isinstance(v,dict):
            src=v.get('src') or v.get('url') or v.get('href')
            if isinstance(src,str):return {'src':src,'source':v.get('source') or 'canonical','width':v.get('width'),'height':v.get('height')}
    ids=work.get('authorityIds') or {}
    ol=((ids.get('openLibraryWork') or ids.get('openLibrary')) if isinstance(ids,dict) else None) or work.get('openLibraryId')
    if ol:return {'src':f'https://covers.openlibrary.org/b/olid/{quote(str(ol))}-M.jpg?default=false','source':'open-library'}
    return {'src':None,'source':'dawn-placeholder'}


def item(work):
    wid=str(work.get('workId') or work.get('id') or '').strip()
    if not wid:raise ValueError('Work missing canonical id')
    c=cover(work); w=c.get('width'); h=c.get('height')
    ratio=(round(float(w)/float(h),5) if w and h else None)
    authors=strings(work.get('authors') or work.get('author'))
    langs=strings(work.get('languages') or work.get('language'))
    return {'workId':wid,'motionKey':f'dawn-work:{wid}','title':work.get('title') or 'Untitled','authors':authors[:4],'languages':langs[:4],
            'cover':{'src':c.get('src'),'source':c.get('source'),'width':w,'height':h,'aspectRatio':ratio},
            'motion':{'layer':'cover','detachable':True,'layoutStable':bool(ratio),'preferredProperties':['transform','opacity']}}


def main():
    root=json.loads((CANONICAL/'root.json').read_text(encoding='utf-8'))
    OUT.mkdir(parents=True,exist_ok=True)
    manifest={'schema':'dawn.library.cover-preview-root.v1','workCount':0,'shardCount':0,'motionContract':'dawn.cover-motion.v1','shards':[]}
    source_counts={}
    for n,shard in enumerate(root['shards'],1):
        payload=json.loads((CANONICAL/shard['href']).read_text(encoding='utf-8'))
        rows=[item(w) for w in work_array(payload)]
        if len(rows)!=shard['workCount']:raise SystemExit(f"count mismatch {shard['href']}: {len(rows)} != {shard['workCount']}")
        for row in rows:
            source=row['cover']['source']; source_counts[source]=source_counts.get(source,0)+1
        name=f'covers-{n:06d}.json'; raw=json.dumps({'schema':'dawn.library.cover-preview-shard.v1','offset':shard['offset'],'count':len(rows),'items':rows},ensure_ascii=False,separators=(',',':'))+'\n'
        (OUT/name).write_text(raw,encoding='utf-8')
        manifest['shards'].append({'offset':shard['offset'],'count':len(rows),'href':name,'sha256':hashlib.sha256(raw.encode()).hexdigest()})
        manifest['workCount']+=len(rows)
    manifest['shardCount']=len(manifest['shards']); manifest['coverSources']=dict(sorted(source_counts.items()))
    if manifest['workCount']!=root['workCount']:raise SystemExit('cover-preview total mismatch')
    (OUT/'root.json').write_text(json.dumps(manifest,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8')
    print(json.dumps({'status':'PASS','workCount':manifest['workCount'],'shardCount':manifest['shardCount'],'coverSources':manifest['coverSources']},ensure_ascii=False))
    return 0
if __name__=='__main__':raise SystemExit(main())
