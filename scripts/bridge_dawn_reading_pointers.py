#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,re
from pathlib import Path

from dore_core.language.pointer_bridge import bridge_legacy_surface

ROOT=Path(__file__).resolve().parents[1]
DEFAULT_CANONICAL=ROOT/'static/dawn-library/canonical-index.json'
DEFAULT_DISCOVERY=ROOT/'static/dawn-library/biblical-world/discovery-candidates.json'
DEFAULT_OUT=ROOT/'static/dawn-library/reading-pointer-map.json'

def norm(v):return ' '.join(str(v or '').casefold().split())
def sig(title,author):return f'{norm(title)}::{norm(author)}'
def read(path):return json.loads(path.read_text(encoding='utf-8'))
def gutenberg_id(value):
 m=re.search(r'(?:ebooks/)?(\d+)',str(value or ''))
 return m.group(1) if m else ''
def resolve(ids,works,item):
 if len(ids)<=1:return ids
 source_id=gutenberg_id(item.get('sourceId') or item.get('sourceUrl'))
 if not source_id:return ids
 exact=[]
 for wid in ids:
  authority=works[wid].get('authorityIds') or {}
  candidates=(authority.get('projectGutenberg'),authority.get('gutenberg'),authority.get('gutenbergId'))
  if source_id in {gutenberg_id(v) for v in candidates if v}:exact.append(wid)
 return exact or ids

def main()->int:
 p=argparse.ArgumentParser();p.add_argument('--canonical',type=Path,default=DEFAULT_CANONICAL);p.add_argument('--discovery',type=Path,default=DEFAULT_DISCOVERY);p.add_argument('--out',type=Path,default=DEFAULT_OUT);a=p.parse_args()
 canonical=read(a.canonical);discovery=read(a.discovery);works=canonical.get('works') or {}
 by_sig={}
 for wid,w in works.items():
  authors=w.get('authors') or [];key=sig(w.get('title'),authors[0] if authors else '')
  if key!='::':by_sig.setdefault(key,[]).append(wid)
 rows=[];ambiguous=0;unmatched=0;ambiguities=[]
 for item in discovery.get('items',[]):
  if str(item.get('provider') or '').casefold()!='project gutenberg':continue
  ids=resolve(by_sig.get(sig(item.get('title'),item.get('author'))) or [],works,item)
  if len(ids)!=1:
   if len(ids)>1:
    ambiguous+=1;ambiguities.append({'sourceId':str(item.get('sourceId') or ''),'title':item.get('title'),'author':item.get('author'),'candidateWorkIds':ids})
   else:unmatched+=1
   continue
  wid=ids[0];result=bridge_legacy_surface(works[wid],item.get('sourceUrl'))
  if not result:continue
  rows.append({'workId':wid,'readingPointer':f'dawn://reading/{wid}','provider':result.provider,'providerId':result.provider_id,'sourceUrl':result.source_url,'witnessId':result.mapping.witness_id,'accessMode':result.mapping.policy.mode.value})
 rows.sort(key=lambda x:x['workId'])
 out={'schema':'dawn.library.reading-pointer-map.v1','identityAuthority':'Dawn','source':'biblical-world/discovery-candidates.json','count':len(rows),'ambiguous':ambiguous,'unmatched':unmatched,'ambiguities':ambiguities,'items':rows}
 a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(out,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8')
 print(json.dumps({'count':len(rows),'ambiguous':ambiguous,'unmatched':unmatched,'ambiguities':ambiguities,'output':str(a.out.relative_to(ROOT))},ensure_ascii=False));return 0
if __name__=='__main__':raise SystemExit(main())
