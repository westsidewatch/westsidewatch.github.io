#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import json
from dore_core.library_reading_layers import project_reading_layer

ROOT=Path(__file__).resolve().parents[1]
CANONICAL=ROOT/'static/dawn-library/canonical'
OUT=ROOT/'static/dawn-library/surfaces'

def works(payload):
 if isinstance(payload,list):return payload
 if not isinstance(payload,dict):raise ValueError('canonical shard must be object or array')
 for key in ('works','items','entries'):
  value=payload.get(key)
  if isinstance(value,list):return value
  if isinstance(value,dict):return [dict(v,workId=v.get('workId') or k) if isinstance(v,dict) else {'workId':k,'value':v} for k,v in value.items()]
 # Canonical shards may themselves be workId -> Work mappings.
 if payload and all(isinstance(v,dict) for v in payload.values()):
  return [dict(v,workId=v.get('workId') or k) for k,v in payload.items()]
 raise ValueError(f'canonical shard has no Work collection; keys={list(payload)[:8]}')

def compact(work,layer):
 r=layer.resolution
 return {'workId':work.get('workId') or work.get('id'),'title':work.get('title'),'authors':work.get('authors') or work.get('author'),'languages':work.get('languages') or work.get('language'),'layer':layer.layer,'mode':layer.mode,'translatable':layer.translatable,'capability':r.capability.value,'provider':r.provider,'href':r.href}

def priority(row):
 # Do not privilege the previously recovered Gutenberg 73: external readers stay layer 2.
 # First expose the works requiring the least transport work to enter Dawn Reader.
 rank={'local-full-text':0,'open-acquisition':1,'authenticated-acquisition':2,'external-reader':3,'metadata-only':4}
 return (rank.get(row['capability'],9),str(row.get('title') or ''),str(row.get('workId') or ''))

def main():
 root=json.loads((CANONICAL/'root.json').read_text())
 first=[];second=[]
 for shard in root['shards']:
  payload=json.loads((CANONICAL/shard['href']).read_text())
  shard_works=works(payload)
  if len(shard_works)!=shard['workCount']:raise SystemExit(f"shard count mismatch: {shard['href']} expected={shard['workCount']} actual={len(shard_works)}")
  for work in shard_works:
   layer=project_reading_layer(work); row=compact(work,layer)
   (first if layer.layer==1 else second).append(row)
 first.sort(key=priority);second.sort(key=priority)
 OUT.mkdir(parents=True,exist_ok=True)
 summary={'schema':'dawn.library.reading-layers.v1','canonicalWorkCount':root['workCount'],'firstReadableCount':len(first),'secondJumpCount':len(second),'firstLayer':'readable+translatable','secondLayer':'jump-reading','firstPriority':'local-full-text -> open-acquisition'}
 (OUT/'dawn-reading-layers.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
 (OUT/'dawn-readable-layer.json').write_text(json.dumps({'schema':'dawn.library.readable-layer.v1','count':len(first),'works':first},ensure_ascii=False,separators=(',',':')))
 (OUT/'dawn-jump-reading-layer.json').write_text(json.dumps({'schema':'dawn.library.jump-reading-layer.v1','count':len(second),'works':second},ensure_ascii=False,separators=(',',':')))
 print(json.dumps(summary,ensure_ascii=False));return 0
if __name__=='__main__':raise SystemExit(main())
