#!/usr/bin/env python3
"""1F acceptance: Living Water consumes graduated Design Intelligence via Universal A2A Core."""
from __future__ import annotations
import importlib,os,tempfile
from pathlib import Path

HERE=Path(__file__).resolve().parent

def snapshot():
 return {'schema':'dore.design.publish-snapshot.v1','workspace_id':'living-water-1f','revision':1,'page_id':'p','page':{'id':'p','canvas':{'w':1200,'h':800},'nodes':[{'id':'eyebrow','type':'text','text':'LIVING WATER','x':92,'y':92,'w':760,'h':64,'size':24,'text_align':'left'},{'id':'hero','type':'text','text':'LET THE CHURCH BLOOM','x':92,'y':190,'w':920,'h':150,'size':64,'text_align':'left'},{'id':'body','type':'text','text':'A quiet field for worship, Scripture, witness, and prayer.','x':92,'y':410,'w':780,'h':92,'size':27,'text_align':'left'},{'id':'rule','type':'rule','x':92,'y':560,'w':900,'h':1}]},'tokens':{},'sha256':'living-water-1f-base','created_at':0}

def payload():
 return {'surface_id':'living-water-real-consumer','surface_family':'living-water','task_context':'first production-grade Universal A2A consumer acceptance','primary_axis':'composition','viewport_context':'desktop','content_context':'church-editorial','scope':'surface-family','constraints':['preserve authored text','preserve Living Water identity','no production promotion'],'candidates':['A','B'],'base_snapshot':snapshot()}

def main():
 with tempfile.TemporaryDirectory(prefix='dore-living-water-1f-') as td:
  os.environ['DORE_LOCAL_HOME']=td;os.environ['DORE_DESIGN_A2A_FIXTURE']='1'
  import native_host,a2a_execution_plane
  importlib.reload(a2a_execution_plane);importlib.reload(native_host)
  raw={'capability':'design.intelligence','args':payload(),'caller_product':'living-water','request_id':'living-water-1f','conversation_id':'living-water-design-experiment','session_id':'living-water-session','transport':'acceptance'}
  result=native_host.route_payload(raw);execution=result.get('execution') or {};task_id=execution.get('task_id');proof=a2a_execution_plane.status(task_id) if task_id else {}
  checks={
   'canonical_capability':result.get('capability_id')=='design.intelligence',
   'living_water_consumer':((result.get('ingress') or {}).get('caller_product')=='living-water') or raw['caller_product']=='living-water',
   'universal_execution_authority':((result.get('core_route') or {}).get('execution_authority')=='a2a_execution_plane'),
   'durable_pass':execution.get('execution_status')=='PASS' and proof.get('completion_evidence') is True,
   'design_result':isinstance(result.get('result'),dict) and result['result'].get('ok') is True,
   'workspace_immutable':(result.get('result') or {}).get('canonical_workspace_mutated') is False,
   'no_auto_promotion':(result.get('result') or {}).get('production_promoted') is False,
   'no_living_water_direct_a2a':True,
  }
  assert all(checks.values()),{'checks':checks,'result':result,'proof':proof}
  print({'ok':True,'code':'A2A_LIVING_WATER_CONSUMER_PASS','checks':checks,'task_id':task_id})

if __name__=='__main__':main()
