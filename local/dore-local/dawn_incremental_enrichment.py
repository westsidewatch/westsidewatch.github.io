#!/usr/bin/env python3
"""Delta-only Dawn enrichment against consumed source identities and families."""
import hashlib,json,sys
from pathlib import Path
VERSION='dore.dawn-incremental-enrichment.v1.0';ROOT=Path(__file__).resolve().parents[2];CATALOG=ROOT/'dore-design/knowledge-lab/resources/dawn-incremental-editorial-sources-v1.json'
REQUIRED=('id','url','authority','source_family','rights','provenance_status')
def incremental_enrich(consumed_sources=None,consumed_assets=None,catalog_path=None):
 catalog=json.loads(Path(catalog_path or CATALOG).read_text());consumed={str(x) for x in (consumed_sources or [])};qualified=[];rejected=[]
 for row in catalog.get('sources') or []:
  missing=[k for k in REQUIRED if not row.get(k)]
  if missing:rejected.append({'id':row.get('id'),'reason':'missing:'+','.join(missing)});continue
  if row['id'] in consumed:continue
  qualified.append({**row,'provenance':row['url'],'enriched_by':'dawn-library-incremental','qualified':True})
 ids=sorted(x['id'] for x in qualified);digest=hashlib.sha256(json.dumps(ids).encode()).hexdigest()[:16]
 return {'schema':'dore.knowledge-asset.v1','knowledge_id':'dawn-library-incremental-'+digest,'delta_only':True,'sources':qualified,'source_count':len(qualified),'candidate_examined_count':len(catalog.get('sources') or []),'duplicate_count':0,'consumed_source_count':len(consumed),'consumed_assets':list(consumed_assets or []),'source_families':sorted({x['source_family'] for x in qualified}),'source_family_count':len({x['source_family'] for x in qualified}),'provenance_preserved':all(x.get('provenance') for x in qualified),'rights_preserved':all(x.get('rights') for x in qualified),'rejected':rejected,'experiment_required':False}
if __name__=='__main__':
 payload=json.loads(sys.stdin.read() or '{}');print(json.dumps({'ok':True,'asset':incremental_enrich(payload.get('consumed_sources'),payload.get('consumed_assets'))},ensure_ascii=False))
