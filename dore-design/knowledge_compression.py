#!/usr/bin/env python3
"""Compress the 44-source PASS corpus into three contrasting design judgments."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
FIRST=ROOT/'dore-design/knowledge-lab/research/design-reference-library-expansion-20260901.json';CATALOG=ROOT/'dore-design/knowledge-lab/resources/source-catalog.json';DELTA=ROOT/'dore-design/knowledge-lab/resources/dawn-incremental-editorial-sources-v1.json'
DIRECTIONS={
 'dawn-atlas':{'name':'Dawn Atlas / 黎明圖譜','page':'homepage-concept-index','signature':'edge-cropped-atlas-route-twelve-column-grid','adopted':['edge-cropped hero','archival axis','ruled collision grid'],'rejected':['generic centered SaaS hero','decorative gradient cards'],'families':['design-community','static-site-template-registry','new-westside-brand']},
 'living-current':{'name':'Living Current / 活水流域','page':'homepage-concept-dispatch','signature':'vertical-current-rail-fluid-field-modular-cards','adopted':['vertical title frame','two-ink field','modular editorial cards'],'rejected':['dashboard chrome','uniform card grid'],'families':['independent-design-publication','oss-cms-theme-registry','new-westside-brand']},
 'signal-nocturne':{'name':'Signal Nocturne / 夜間信號','page':'homepage-concept-folio','signature':'nocturne-signal-star-asymmetric-two-column','adopted':['central overprint','high-contrast nocturne','signal-object field'],'rejected':['stock photography hero','soft lifestyle minimalism'],'families':['interactive-editorial','literary-independent-publication','new-westside-brand']}}
def corpus():
 a=json.loads(FIRST.read_text());c=json.loads(CATALOG.read_text());b=json.loads(DELTA.read_text());groups=(a.get('knowledge_artifact') or {}).get('sources') or {};rows=sum((v for v in groups.values() if isinstance(v,list)),[])+c.get('sources',[])+b.get('sources',[]);seen={}
 for x in rows:
  if isinstance(x,dict):
   k=str(x.get('id') or x.get('url') or x.get('path') or '')
   if k:seen.setdefault(k,x)
 return list(seen.values())
def compress():
 rows=corpus();digest=hashlib.sha256(json.dumps(sorted(str(x.get('id') or x.get('url')) for x in rows)).encode()).hexdigest()
 out=[]
 for key,d in DIRECTIONS.items():
  refs=[{'id':str(x.get('id') or x.get('url') or x.get('path')),'provenance':x.get('url') or x.get('path') or x.get('upstream') or 'knowledge-lab','source_family':x.get('source_family') or x.get('kind') or 'research-corpus'} for x in rows if any(f in json.dumps(x,ensure_ascii=False).lower() for f in [z.lower() for z in d['families'] if z!='new-westside-brand'])][:6]
  refs.append({'id':'new-westside-visual-language','provenance':'dore-design/new-westside','source_family':'new-westside-brand'})
  out.append({'direction':key,**d,'story_id':'new-westside-homepage-concepts--'+key,'candidate_id':'new-westside-'+key+'-v1','corpus_sha256':digest,'corpus_source_count':len(rows),'reference_lineage':refs,'pattern_judgment':{'adopted':d['adopted'],'rejected':d['rejected'],'westside_reason':'Preserves watchfulness, living water, editorial gravity and a restrained print-derived system.'}})
 return {'schema':'dore.design-knowledge-compression.v1','source_goal':'design-reference-library-expansion-20260901','source_goal_status':'PASS','corpus_source_count':len(rows),'corpus_sha256':digest,'clusters':['print-system','independent-editorial','interactive-publication','new-westside-brand'],'directions':out}
if __name__=='__main__':print(json.dumps({'ok':True,'compression':compress()},ensure_ascii=False))
