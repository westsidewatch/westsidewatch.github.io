#!/usr/bin/env python3
from __future__ import annotations
import importlib,json,os,shutil,tempfile
from pathlib import Path

# Real-machine acceptance also persists inspectable Round-1 evidence.
def snapshot():
 return {'schema':'dore.design.publish-snapshot.v1','workspace_id':'living-water-real','revision':1,'page_id':'p','page':{'id':'p','canvas':{'w':1200,'h':800},'nodes':[{'id':'hero','type':'text','text':'LET THE CHURCH BLOOM','x':90,'y':180,'w':900,'h':150,'size':64,'text_align':'left'},{'id':'body','type':'text','text':'Living Water','x':90,'y':420,'w':700,'h':90,'size':28,'text_align':'left'}]},'tokens':{},'sha256':'living-water-real-base','created_at':0}

def _persist_evidence(design,task_id,checks):
 root=Path(os.environ.get('DORE_REPO_ROOT') or Path(__file__).resolve().parents[2])
 out=root/'.artifacts'/'living-water-bloom'/str(task_id);out.mkdir(parents=True,exist_ok=True)
 candidates=design.get('candidates') or []
 raster_files=[]
 for candidate in candidates:
  cid=str(candidate.get('candidate_id') or '?');raster=candidate.get('raster') or {};src=Path(str(raster.get('path') or ''))
  if src.is_file():
   dst=out/f'{cid}.png';shutil.copy2(src,dst);raster_files.append({'candidate_id':cid,'file':dst.name,'sha256':raster.get('sha256'),'width':raster.get('width'),'height':raster.get('height'),'byte_size':raster.get('byte_size')})
 critic=design.get('critic') or {}
 evidence={
  'schema':'dore.living-water-bloom.evidence.v1','task_id':task_id,'experiment_id':design.get('experiment_id'),'checks':checks,
  'provider':design.get('provider'),'model':design.get('model'),'variants':design.get('variants') or [],'raster_files':raster_files,
  'critic':critic,'winner':design.get('winner') or critic.get('winner'),'loser_failures':design.get('loser_failures') or critic.get('loser_failures') or [],
  'rejection_memory':design.get('rejection_memory') or [],'memory_admitted':design.get('memory_admitted'),'writeback':design.get('writeback'),
  'divergence_domains':design.get('divergence_domains') or [],'historical_design_authority':design.get('historical_design_authority'),
  'canonical_workspace_mutated':design.get('canonical_workspace_mutated'),'production_promoted':design.get('production_promoted')
 }
 (out/'evidence.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8')
 return out,evidence

def main():
 with tempfile.TemporaryDirectory(prefix='dore-living-water-real-') as td:
  os.environ['DORE_LOCAL_HOME']=td;os.environ.pop('DORE_DESIGN_A2A_FIXTURE',None)
  import native_host,a2a_execution_plane
  importlib.reload(a2a_execution_plane);importlib.reload(native_host)
  args={'surface_id':'living-water-real','surface_family':'living-water','experiment_id':'living-water-bloom','task_context':'Universal Core Living Water bloom real consumer acceptance','primary_axis':'identity-to-composition','viewport_context':'desktop','content_context':'real-church-canonical-content-and-relationships','scope':'surface-family','constraints':['preserve authored text','no production promotion'],'candidates':['A','B'],'base_snapshot':snapshot()}
  raw={'capability':'design.intelligence','args':args,'caller_product':'living-water','request_id':'living-water-bloom-real-1','conversation_id':'living-water-bloom-experiment','session_id':'living-water-bloom-real','transport':'acceptance'}
  result=native_host.route_payload(raw);execution=result.get('execution') or {};design=result.get('result') or {};task_id=execution.get('task_id');proof=a2a_execution_plane.status(task_id) if task_id else {};candidates=design.get('candidates') or [];rasters=[c.get('raster') or {} for c in candidates]
  checks={'canonical':result.get('capability_id')=='design.intelligence','universal':((result.get('core_route') or {}).get('execution_authority')=='a2a_execution_plane'),'pass':execution.get('execution_status')=='PASS' and proof.get('completion_evidence') is True,'real':design.get('provider')=='dore-local' and str(design.get('model') or '') not in {'','fixture','local-default'},'pixels':len(candidates)==2 and all(r.get('real_browser_render') and r.get('sha256') for r in rasters),'judges':len((design.get('critic') or {}).get('votes') or [])==2,'immutable':design.get('canonical_workspace_mutated') is False,'not_promoted':design.get('production_promoted') is False,'bloom_contract':design.get('experiment_contract_applied') is True and design.get('experiment_id')=='living-water-bloom','divergent':len(design.get('divergence_domains') or [])>=4,'old_design_not_authority':design.get('historical_design_authority') is False}
  assert all(checks.values()),{'checks':checks,'result':result}
  out,evidence=_persist_evidence(design,task_id,checks)
  assert len(evidence['raster_files'])==2,'persisted_raster_pair_required'
  assert len((evidence['critic'] or {}).get('votes') or [])==2,'persisted_blind_votes_required'
  print(json.dumps({'ok':True,'code':'LIVING_WATER_BLOOM_REAL_PASS','checks':checks,'task_id':task_id,'evidence_dir':str(out),'winner':evidence.get('winner'),'failure_domains':[x.get('domain') for x in evidence.get('loser_failures') or []],'memory_admitted':evidence.get('memory_admitted')},ensure_ascii=False))
if __name__=='__main__':main()
