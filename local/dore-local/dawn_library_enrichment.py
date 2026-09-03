#!/usr/bin/env python3
"""Create a provenance-preserving Dawn Library KnowledgeAsset from real repo sources."""
import hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def enrich(research_path=None,catalog_path=None):
 research=json.loads(Path(research_path or ROOT/'dore-design/knowledge-lab/research/design-reference-library-expansion-20260901.json').read_text());catalog=json.loads(Path(catalog_path or ROOT/'dore-design/knowledge-lab/resources/source-catalog.json').read_text());groups=(research.get('knowledge_artifact') or {}).get('sources') or {};raw=sum((v for v in groups.values() if isinstance(v,list)),[])+list(catalog.get('sources') or [])
 seen={};
 for item in raw:
  if not isinstance(item,dict):continue
  key=str(item.get('id') or item.get('url') or item.get('path') or '').strip()
  if key and key not in seen:seen[key]={**item,'id':key,'enriched_by':'dawn-library','provenance':item.get('url') or item.get('path') or item.get('upstream') or key,'rights':item.get('license') or item.get('rights') or 'review-required'}
 sources=list(seen.values());digest=hashlib.sha256(json.dumps([x['id'] for x in sources],sort_keys=True).encode()).hexdigest()[:16]
 return {'schema':'dore.knowledge-asset.v1','knowledge_id':'dawn-library-editorial-'+digest,'title':'Editorial design and publishing sources','sources':sources,'source_count':len(sources),'provenance_preserved':True,'rights_review_required':sum(x['rights']=='review-required' for x in sources),'capabilities':['reference-expansion','provenance-normalization','deduplication'],'experiment_required':False}
if __name__=='__main__':print(json.dumps({'ok':True,'asset':enrich(*(sys.argv[1:3]))},ensure_ascii=False))
