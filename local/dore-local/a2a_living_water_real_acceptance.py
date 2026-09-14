#!/usr/bin/env python3
from __future__ import annotations
import importlib,os,tempfile

def snapshot():
 return {'schema':'dore.design.publish-snapshot.v1','workspace_id':'living-water-real','revision':1,'page_id':'p','page':{'id':'p','canvas':{'w':1200,'h':800},'nodes':[{'id':'hero','type':'text','text':'LET THE CHURCH BLOOM','x':90,'y':180,'w':900,'h':150,'size':64,'text_align':'left'},{'id':'body','type':'text','text':'Living Water','x':90,'y':420,'w':700,'h':90,'size':28,'text_align':'left'}]},'tokens':{},'sha256':'living-water-real-base','created_at':0}

def main():
 with tempfile.TemporaryDirectory(prefix='dore-living-water-real-') as td:
  os.environ['DORE_LOCAL_HOME']=td;os.environ.pop('DORE_DESIGN_A2A_FIXTURE',None)
  import native_host,a2a_execution_plane
  importlib.reload(a2a_execution_plane);importlib.reload(native_host)
  args={'surface_id':'living-water-real','surface_family':'living-water','task_context':'Universal A2A real consumer acceptance','primary_axis':'composition','viewport_context':'desktop','content_context':'church-editorial','scope':'surface-family','constraints':['preserve authored text','no production promotion'],'candidates':['A','B'],'base_snapshot':snapshot()}
  raw={'capability':'design.intelligence','args':args,'caller_product':'living-water','request_id':'living-water-real-1f','conversation_id':'living-water-design-experiment','session_id':'living-water-real','transport':'acceptance'}
  result=native_host.route_payload(raw);execution=result.get('execution') or {};design=result.get('result') or {};task_id=execution.get('task_id');proof=a2a_execution_plane.status(task_id) if task_id else {};candidates=design.get('candidates') or [];rasters=[c.get('raster') or {} for c in candidates]
  checks={'canonical':result.get('capability_id')=='design.intelligence','universal':((result.get('core_route') or {}).get('execution_authority')=='a2a_execution_plane'),'pass':execution.get('execution_status')=='PASS' and proof.get('completion_evidence') is True,'real':design.get('provider')=='dore-local' and str(design.get('model') or '') not in {'','fixture','local-default'},'pixels':len(candidates)==2 and all(r.get('real_browser_render') and r.get('sha256') for r in rasters),'judges':len((design.get('critic') or {}).get('votes') or [])==2,'immutable':design.get('canonical_workspace_mutated') is False,'not_promoted':design.get('production_promoted') is False}
  assert all(checks.values()),{'checks':checks,'result':result};print({'ok':True,'code':'A2A_LIVING_WATER_REAL_PASS','checks':checks,'task_id':task_id})
if __name__=='__main__':main()
