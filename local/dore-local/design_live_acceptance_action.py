#!/usr/bin/env python3
"""Real-Mac model-backed acceptance for Doré Design Intelligence."""
from __future__ import annotations
import os,sqlite3,sys,tempfile
from pathlib import Path
CAPABILITIES={"design.intelligence.live.acceptance"};MAX_FIRST_PASS_ATTEMPTS=3
def _repo()->Path:return Path(os.environ.get("DORE_REPO_ROOT") or os.environ.get("DORE_WORKTREE") or Path.home()/"westsidewatch.github.io").expanduser().resolve()
def _snapshot()->dict:
 return {'schema':'dore.design.publish-snapshot.v1','workspace_id':'design-live-acceptance','revision':1,'page_id':'p','page':{'id':'p','canvas':{'w':1200,'h':800},'nodes':[{'id':'eyebrow','type':'text','text':'WESTSIDE WATCH','x':92,'y':92,'w':760,'h':64,'size':24,'text_align':'left'},{'id':'hero','type':'text','text':'WATCH FOR THE DAWN','x':92,'y':190,'w':920,'h':150,'size':64,'text_align':'left'},{'id':'body','type':'text','text':'A quiet field for Scripture, witness, and prayer.','x':92,'y':410,'w':780,'h':92,'size':27,'text_align':'left'},{'id':'rule','type':'rule','x':92,'y':560,'w':900,'h':1}]},'tokens':{},'sha256':'design-live-base','created_at':0}
def _payload(surface_id:str)->dict:
 return {'surface_id':surface_id,'surface_family':'living-water-live-acceptance','task_context':'real model closed-loop visual hierarchy acceptance','primary_axis':'composition','viewport_context':'desktop','content_context':'bilingual-capable-editorial','scope':'surface-family','constraints':['preserve authored text','preserve quiet Living Water identity','do not promote to production'],'candidates':['A','B'],'base_snapshot':_snapshot()}
def _count_memory(db_path:Path)->dict:
 if not db_path.exists():return {'comparisons':0,'rejections':0}
 with sqlite3.connect(db_path) as c:return {'comparisons':int(c.execute('SELECT COUNT(*) FROM dore_ui_taste_comparisons').fetchone()[0]),'rejections':int(c.execute('SELECT COUNT(*) FROM dore_ui_taste_rejections').fetchone()[0])}
def execute(capability:str,args=None):
 if capability not in CAPABILITIES:return {'ok':False,'status':'failed','error':{'code':'unsupported_action','message':capability}}
 repo=_repo();design=repo/'dore-design';local=repo/'local'/'dore-local'
 if not design.is_dir() or not local.is_dir():return {'ok':False,'status':'failed','stage':'repo','error':{'code':'repo_layout_missing','message':str(repo)}}
 old_fixture=os.environ.pop('DORE_DESIGN_A2A_FIXTURE',None);old_disagree=os.environ.pop('DORE_DESIGN_A2A_DISAGREE_FIXTURE',None);old_home=os.environ.get('DORE_LOCAL_HOME');old_db=os.environ.get('DORE_UI_TASTE_DB')
 try:
  with tempfile.TemporaryDirectory(prefix='dore-design-live-') as td:
   home=Path(td);taste_db=home/'design'/'ui-taste.sqlite3';os.environ['DORE_LOCAL_HOME']=str(home);os.environ['DORE_UI_TASTE_DB']=str(taste_db);os.environ['DORE_REPO_ROOT']=str(repo)
   if str(design) not in sys.path:sys.path.insert(0,str(design))
   if str(local) not in sys.path:sys.path.insert(0,str(local))
   import design_local_inference as local_inference
   import design_intelligence_a2a as bridge
   model=str(local_inference.MODEL);ollama_base=str(local_inference.OLLAMA);first=None;attempts=[]
   for idx in range(1,MAX_FIRST_PASS_ATTEMPTS+1):
    result=bridge.explore(_payload(f'live-first-{idx}'));attempts.append({'attempt':idx,'task_id':result.get('task_id'),'provider':result.get('provider'),'model':result.get('model'),'consensus':result.get('consensus'),'memory_admitted':result.get('memory_admitted'),'rejections':len(result.get('rejection_memory') or [])})
    if result.get('memory_admitted') and (result.get('rejection_memory') or []):first=result;break
   if first is None:return {'ok':False,'status':'failed','stage':'first-pass','model':model,'ollama_base':ollama_base,'attempts':attempts,'reason':'no_consensus_rejection_memory_after_bounded_attempts'}
   memory_after_first=_count_memory(taste_db);second=bridge.explore(_payload('live-second-memory-read'));route_before=second.get('route_before') or {};pack=route_before.get('preference_pack') or {};guardrails=pack.get('rejection_guardrails') or []
   first_domains={str(x.get('domain')) for x in (first.get('loser_failures') or [])};second_domains={str(x.get('failure_domain')) for x in guardrails};shared=sorted(first_domains & second_domains);candidates=second.get('candidates') or [];rasters=[c.get('raster') or {} for c in candidates]
   checks={'fixture_disabled':os.environ.get('DORE_DESIGN_A2A_FIXTURE')!='1','local_model_concrete':bool(model) and model not in {'fixture','local-default'},'gemma4_local_engine':model.startswith('gemma4:'),'localhost_ollama':ollama_base.startswith('http://127.0.0.1:') or ollama_base.startswith('http://localhost:'),'first_provider_local':first.get('provider')=='dore-local','first_real_model':str(first.get('model') or '') not in {'fixture','local-default',''},'first_real_browser_pixels':len(first.get('candidates') or [])==2 and all((c.get('raster') or {}).get('real_browser_render') for c in (first.get('candidates') or [])),'first_distinct_rasters':len({(c.get('raster') or {}).get('sha256') for c in (first.get('candidates') or [])})==2,'first_blind_two_judges':len((first.get('critic') or {}).get('votes') or [])==2,'first_memory_written':memory_after_first['comparisons']>=1 and memory_after_first['rejections']>=1,'second_reads_rejection_memory':bool(shared),'second_real_model':second.get('provider')=='dore-local' and str(second.get('model') or '') not in {'fixture','local-default',''},'second_real_browser_pixels':len(candidates)==2 and all(r.get('real_browser_render') for r in rasters),'second_distinct_rasters':len({r.get('sha256') for r in rasters})==2,'canonical_workspace_unchanged':first.get('canonical_workspace_mutated') is False and second.get('canonical_workspace_mutated') is False,'production_not_promoted':first.get('production_promoted') is False and second.get('production_promoted') is False}
   ok=all(checks.values())
   return {'ok':ok,'status':'completed' if ok else 'failed','capability':capability,'protocol':'dore.design-real-model-a2a-acceptance/1','model':model,'ollama_base':ollama_base,'checks':checks,'first_attempts':attempts,'first':{'task_id':first.get('task_id'),'winner':first.get('winner'),'failure_domains':sorted(first_domains),'memory_after':memory_after_first,'repair_loop':first.get('repair_loop'),'rejection_enforcement':first.get('rejection_enforcement')},'second':{'task_id':second.get('task_id'),'guardrail_domains':sorted(second_domains),'shared_domains':shared,'winner':second.get('winner'),'repair_loop':second.get('repair_loop'),'rejection_enforcement':second.get('rejection_enforcement')},'production_default_changed':False,'canonical_workspace_mutation':False,'fixture_mode':False}
 except Exception as exc:return {'ok':False,'status':'failed','stage':'execution','error':{'code':type(exc).__name__,'message':str(exc)}}
 finally:
  if old_fixture is not None:os.environ['DORE_DESIGN_A2A_FIXTURE']=old_fixture
  else:os.environ.pop('DORE_DESIGN_A2A_FIXTURE',None)
  if old_disagree is not None:os.environ['DORE_DESIGN_A2A_DISAGREE_FIXTURE']=old_disagree
  else:os.environ.pop('DORE_DESIGN_A2A_DISAGREE_FIXTURE',None)
  if old_home is not None:os.environ['DORE_LOCAL_HOME']=old_home
  else:os.environ.pop('DORE_LOCAL_HOME',None)
  if old_db is not None:os.environ['DORE_UI_TASTE_DB']=old_db
  else:os.environ.pop('DORE_UI_TASTE_DB',None)
