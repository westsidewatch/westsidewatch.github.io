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
 for key in ('works','items','entries'):
  if isinstance(payload.get(key),list):return payload[key]
 raise ValueError('canonical shard has no Work array')

def compact(work,layer):
 r=layer.resolution
 return {'workId':work.get('workId') or work.get('id'),'title':work.get('title'),'authors':work.get('authors') or work.get('author'),'languages':work.get('languages') or work.get('language'),'layer':layer.layer,'mode':layer.mode,'translatable':layer.translatable,'capability':r.capability.value,'provider':r.provider,'href':r.href}

def main():
 root=json.loads((CANONICAL/'root.json').read_text())
 first=[];second=[]
 for shard in root['shards']:
  payload=json.loads((CANONICAL/shard['href']).read_text())
  for work in works(payload):
   layer=project_reading_layer(work); row=compact(work,layer)
   (first if layer.layer==1 else second).append(row)
 OUT.mkdir(parents=True,exist_ok=True)
 summary={'schema':'dawn.library.reading-layers.v1','canonicalWorkCount':root['workCount'],'firstReadableCount':len(first),'secondJumpCount':len(second),'firstLayer':'readable+translatable','secondLayer':'jump-reading'}
 (OUT/'dawn-reading-layers.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
 (OUT/'dawn-readable-layer.json').write_text(json.dumps({'schema':'dawn.library.readable-layer.v1','count':len(first),'works':first},ensure_ascii=False,separators=(',',':')))
 (OUT/'dawn-jump-reading-layer.json').write_text(json.dumps({'schema':'dawn.library.jump-reading-layer.v1','count':len(second),'works':second},ensure_ascii=False,separators=(',',':')))
 print(json.dumps(summary,ensure_ascii=False));return 0
if __name__=='__main__':raise SystemExit(main())
