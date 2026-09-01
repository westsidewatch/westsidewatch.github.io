#!/usr/bin/env python3
"""Doré Resident Runtime v0.6 — durable A2A <-> Storybook loop controller.

Hard path: RESEARCH_REQUIRED -> RESEARCH_QUEUED -> RESEARCHING ->
[PEER_RESEARCH_QUEUED] -> KNOWLEDGE_RETURNED -> EXPERIMENTING ->
VERIFIED/REJECTED -> PROMOTED -> RESUME_PARENT. No identical retry without
new evidence; unknown technical knowledge is not a HUMAN_GATE.
"""
from __future__ import annotations
import fcntl, hashlib, json, os, shutil, subprocess, sys, time
from datetime import datetime, timezone
from pathlib import Path
VERSION='dore.resident-runtime.v0.6'
HOME=Path(os.environ.get('DORE_LOCAL_HOME',Path.home()/'.dore')).expanduser()
ROOT=Path(os.environ.get('DORE_REPO_ROOT',Path.home()/'westsidewatch.github.io')).expanduser()
LOCAL=ROOT/'local'/'dore-local';A2A=ROOT/'dore-design'/'knowledge-lab'/'a2a';RUNTIME=HOME/'runtime';LEARNING=HOME/'coordination'/'learning';RESEARCH=HOME/'coordination'/'research'
DRIVER=LOCAL/'autonomous_driver.py';RESEARCH_EXECUTOR=LOCAL/'research_executor.py';PEER_BRIDGE=LOCAL/'peer_research_bridge.py';SELF=LOCAL/'resident_runtime.py';PROJECT_STATE=A2A/'project-state.json'
STATE=RUNTIME/'state.json';EVENTS=RUNTIME/'events.jsonl';HEARTBEAT=RUNTIME/'heartbeat.json';LOCK=RUNTIME/'runtime.lock';TELEMETRY_REPO=RUNTIME/'telemetry-repo';TELEMETRY_BRANCH=os.environ.get('DORE_RUNTIME_TELEMETRY_BRANCH','dore-runtime-telemetry')
INTERVAL=max(10,int(os.environ.get('DORE_RUNTIME_INTERVAL_SECONDS','30')));TELEMETRY_INTERVAL=max(60,int(os.environ.get('DORE_RUNTIME_TELEMETRY_SECONDS','120')));SELF_UPDATE_INTERVAL=max(120,int(os.environ.get('DORE_RUNTIME_SELF_UPDATE_SECONDS','300')))
try:_rel=(json.loads(PROJECT_STATE.read_text(encoding='utf-8')).get('active_relationship') or {})
except Exception:_rel={}
PARENT_ID=os.environ.get('DORE_RUNTIME_PARENT_ID',str(_rel.get('current_parent_message_id') or 'new-westside-storybook-real-loop-2'));PARENT_GOAL=os.environ.get('DORE_RUNTIME_PARENT_GOAL',str(_rel.get('parent_product_goal') or 'New Westside visual construction'));PROJECT_LOOP=str(_rel.get('loop') or 'A2A <-> Storybook')
sys.path.insert(0,str(LOCAL))
def now():return datetime.now(timezone.utc).isoformat()
def run(argv,cwd=ROOT,timeout=120,input_text=None):return subprocess.run(argv,cwd=str(cwd),text=True,capture_output=True,timeout=timeout,input=input_text)
def read_json(p,default=None):
 try:return json.loads(Path(p).read_text(encoding='utf-8'))
 except Exception:return default
def atomic_json(p,v):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);t=p.with_suffix(p.suffix+'.tmp');t.write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8');t.replace(p)
def event(kind,**data):
 RUNTIME.mkdir(parents=True,exist_ok=True)
 with EVENTS.open('a',encoding='utf-8') as f:f.write(json.dumps({'at':now(),'event':kind,**data},ensure_ascii=False)+'\n')
def fp(v):return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,default=str).encode()).hexdigest()
def tail_events(n=40):
 if not EVENTS.exists():return []
 out=[]
 for line in EVENTS.read_text(encoding='utf-8',errors='replace').splitlines()[-n:]:
  try:out.append(json.loads(line))
  except Exception:out.append({'event':'UNPARSEABLE_EVENT','raw':line[-1000:]})
 return out
def latest_learning():
 p=LEARNING/f'{PARENT_ID}.json'
 if p.exists():
  d=read_json(p)
  if isinstance(d,dict):return p,d
 if LEARNING.exists():
  for p in sorted(LEARNING.glob('*.json'),key=lambda x:x.stat().st_mtime,reverse=True):
   d=read_json(p)
   if isinstance(d,dict) and d.get('state')=='RESEARCH_REQUIRED':return p,d
 return None,None
def transition(path,job,state,**extra):
 h=list(job.get('history') or []);h.append({'at':now(),'state':state});job={**job,'state':state,'updated_at':now(),'history':h,**extra};atomic_json(path,job);event(state,research_id=job.get('research_id'),parent_goal=PARENT_GOAL);return job
def ensure_job(lp,learning):
 RESEARCH.mkdir(parents=True,exist_ok=True);failure=(learning or {}).get('failure_fingerprint') or fp(learning or {'parent':PARENT_ID});rid=f'research-{PARENT_ID}-{fp(failure)[:16]}';p=RESEARCH/f'{rid}.json';old=read_json(p,{}) or {}
 if old:return p,old
 q=((learning or {}).get('knowledge_request') or {}).get('question') or (learning or {}).get('question') or 'Find a mature evidence-backed repair, verify it in isolation, promote it, then resume the parent goal.'
 job={'schema':'dore.research-job.v0.2','research_id':rid,'state':'RESEARCH_QUEUED','created_at':now(),'updated_at':now(),'iteration':1,'parent_message_id':PARENT_ID,'parent_goal':PARENT_GOAL,'project_loop':PROJECT_LOOP,'parent_goal_preserved':True,'failure_fingerprint':failure,'question':q,'preferred_sources':['local Knowledge Lab','verified skills/failure memory','official docs','maintained mature OSS','standards/specs'],'acceptance_test':'smallest falsifiable parent-specific experiment','promotion_target':'verified skill/failure-memory/shared-learning','human_gate':False,'history':[{'at':now(),'state':'RESEARCH_QUEUED'}]};atomic_json(p,job);event('RESEARCH_QUEUED',research_id=rid,parent_goal=PARENT_GOAL);return p,job
def exec_json(script,args=(),timeout=600,input_text=None):
 if not script.exists():return {'ok':False,'error':'component_missing:'+str(script)}
 cp=run([sys.executable,str(script),*map(str,args)],timeout=timeout,input_text=input_text);parsed=None
 try:parsed=json.loads((cp.stdout or '').strip().splitlines()[-1])
 except Exception:pass
 return {'ok':cp.returncode==0 and isinstance(parsed,dict) and bool(parsed.get('ok')),'returncode':cp.returncode,'stdout':(cp.stdout or '')[-12000:],'stderr':(cp.stderr or '')[-12000:],'result':parsed}
def drive(lp,learning,jp,job,reason):
 msg={'schema':'dore.runtime.v0.6','message_id':f'resident-{int(time.time())}','kind':'autonomous_driver','sender':'dore-resident-runtime','recipient':'dore','related_goal':PARENT_GOAL,'task':{'parent_source_message_id':PARENT_ID,'parent_goal':PARENT_GOAL,'project_loop':PROJECT_LOOP,'trigger':reason,'learning_evidence':str(lp) if lp else None,'failure_fingerprint':(learning or {}).get('failure_fingerprint'),'research_job':str(jp) if jp else None,'knowledge_artifact':(job or {}).get('knowledge_artifact')}}
 return exec_json(DRIVER,timeout=1200,input_text=json.dumps(msg,ensure_ascii=False))
def remember(result,verified=False,resolution=None):
 try:
  from failure_memory import remember_failure
  return remember_failure(PARENT_GOAL,((result.get('stderr') or '')+'\n'+(result.get('stdout') or ''))[-6000:],evidence=result.get('result'),resolution=resolution,verified=verified)
 except Exception as e:return {'error':repr(e)}
def shared(job,status,verification=None):
 try:
  from shared_learning import record
  a=(job or {}).get('knowledge_artifact') or {};return record(a,learned_by='dore',status=status,verification=verification,parent_goal=PARENT_GOAL) if a else None
 except Exception as e:return {'ok':False,'error':repr(e)}
def reject(jp,job,result):
 diag={'returncode':result.get('returncode'),'stdout':(result.get('stdout') or '')[-2500:],'stderr':(result.get('stderr') or '')[-2500:],'parsed':result.get('result')};job=transition(jp,{**job,'experiments':list(job.get('experiments') or [])+[{'at':now(),'status':'REJECTED','diagnostic':diag}],'failure_memory':remember(result)},'REJECTED');job={**job,'iteration':int(job.get('iteration') or 1)+1,'knowledge_artifact':None,'question':str(job.get('question') or '')+' New rejected-experiment evidence: '+json.dumps(diag,ensure_ascii=False)[-3000:]};return transition(jp,job,'RESEARCH_QUEUED')
def verify(jp,job,result):
 v={'at':now(),'signal':'parent-specific experiment passed','driver_result':result.get('result')};job=transition(jp,job,'VERIFIED',verification=v);s=shared(job,'VERIFIED',v);parsed=result.get('result') if isinstance(result.get('result'),dict) else {};promotion=parsed.get('promoted_skills') or parsed.get('promoted_skill') or 'verified evidence retained';job=transition(jp,{**job,'shared_learning':s,'failure_memory':remember(result,True,promotion)},'PROMOTED',promotion=promotion);return transition(jp,job,'RESUME_PARENT',resumed=True)
def a2a_task(state_name):
 try:
  from a2a_adapter import dore_to_a2a_task
  return dore_to_a2a_task(source_message_id=PARENT_ID,parent_goal=PARENT_GOAL,state=state_name,metadata={'projectLoop':PROJECT_LOOP,'runtime':VERSION})
 except Exception as e:return {'error':repr(e)}
def snapshot():
 st=read_json(STATE,{}) or {};hb=read_json(HEARTBEAT,{}) or {};jobs=[]
 if RESEARCH.exists():
  for p in sorted(RESEARCH.glob('*.json'),key=lambda x:x.stat().st_mtime,reverse=True)[:6]:
   j=read_json(p,{}) or {};jobs.append({'path':str(p),'research_id':j.get('research_id'),'state':j.get('state'),'iteration':j.get('iteration'),'evidence_count':((j.get('knowledge_artifact') or {}).get('evidence_count')),'peer_research':j.get('peer_research')})
 current=str(hb.get('state') or st.get('last_event') or 'RUNNING');return {'schema':'dore.runtime.telemetry.v0.5','published_at':now(),'runtime':VERSION,'project_loop':PROJECT_LOOP,'parent_goal':PARENT_GOAL,'parent_message_id':PARENT_ID,'heartbeat':hb,'state':st,'a2a_task':a2a_task(current),'research_jobs':jobs,'events':tail_events()}
def telemetry_repo():
 remote=run(['git','remote','get-url','origin'],timeout=30)
 if remote.returncode or not remote.stdout.strip():raise RuntimeError('origin_remote_unavailable')
 if not (TELEMETRY_REPO/'.git').exists():
  if TELEMETRY_REPO.exists():shutil.rmtree(TELEMETRY_REPO)
  cp=run(['git','clone','--filter=blob:none','--no-checkout',remote.stdout.strip(),str(TELEMETRY_REPO)],cwd=RUNTIME,timeout=180)
  if cp.returncode:raise RuntimeError('telemetry_clone_failed')
  run(['git','config','user.name','DORE-RUNTIME'],cwd=TELEMETRY_REPO);run(['git','config','user.email','westsidewatchca@gmail.com'],cwd=TELEMETRY_REPO)
 return TELEMETRY_REPO
def publish(force=False):
 st=read_json(STATE,{}) or {};last=float(st.get('last_telemetry_epoch') or 0)
 if not force and time.time()-last<TELEMETRY_INTERVAL:return
 repo=telemetry_repo();run(['git','fetch','origin',TELEMETRY_BRANCH],cwd=repo,timeout=90);exists=run(['git','show-ref','--verify',f'refs/remotes/origin/{TELEMETRY_BRANCH}'],cwd=repo,timeout=30).returncode==0;cp=run(['git','checkout','-B',TELEMETRY_BRANCH,f'origin/{TELEMETRY_BRANCH}'],cwd=repo,timeout=60) if exists else run(['git','checkout','--orphan',TELEMETRY_BRANCH],cwd=repo,timeout=60)
 if cp.returncode:raise RuntimeError('telemetry_checkout_failed')
 (repo/'runtime-latest.json').write_text(json.dumps(snapshot(),ensure_ascii=False,indent=2)+'\n',encoding='utf-8');run(['git','add','runtime-latest.json'],cwd=repo)
 if run(['git','diff','--cached','--quiet'],cwd=repo).returncode:
  if run(['git','commit','-m','chore(dore): publish resident runtime telemetry'],cwd=repo).returncode:raise RuntimeError('telemetry_commit_failed')
  if run(['git','push','origin',f'HEAD:{TELEMETRY_BRANCH}'],cwd=repo,timeout=120).returncode:raise RuntimeError('telemetry_push_failed')
 st['last_telemetry_epoch']=time.time();st['last_telemetry_at']=now();atomic_json(STATE,st)
def self_update():
 st=read_json(STATE,{}) or {};last=float(st.get('last_self_update_check_epoch') or 0)
 if time.time()-last<SELF_UPDATE_INTERVAL:return
 st['last_self_update_check_epoch']=time.time();st['last_self_update_check_at']=now();atomic_json(STATE,st)
 if run(['git','fetch','origin','main'],timeout=120).returncode:event('SELF_UPDATE_FETCH_FAILED');return
 rels=['local/dore-local/resident_runtime.py','local/dore-local/autonomous_driver.py','local/dore-local/research_executor.py','local/dore-local/peer_research_bridge.py','local/dore-local/autonomous_capability_loop.py','local/dore-local/failure_memory.py','local/dore-local/shared_learning.py','local/dore-local/a2a_adapter.py','local/dore-local/loop_contract_acceptance.py','dore-design/knowledge-lab/resources/source-catalog.json','dore-design/knowledge-lab/a2a/project-state.json','dore-design/knowledge-lab/a2a/loop-contract-v1.json','dore-design/knowledge-lab/a2a/agent-card.json','dore-design/knowledge-lab/skills/registry.json'];changed=[]
 for rel in rels:
  target=ROOT/rel;show=run(['git','show',f'origin/main:{rel}'],timeout=60)
  if show.returncode:continue
  if show.stdout!=(target.read_text(encoding='utf-8') if target.exists() else ''):
   target.parent.mkdir(parents=True,exist_ok=True);tmp=target.with_suffix(target.suffix+'.remote');tmp.write_text(show.stdout,encoding='utf-8');tmp.replace(target);changed.append(rel)
 if changed:
  event('SELF_UPDATED',files=changed);publish(True)
  if 'local/dore-local/resident_runtime.py' in changed:os.execv(sys.executable,[sys.executable,str(SELF)])
def tick():
 st=read_json(STATE,{}) or {};lp,learning=latest_learning();jp=job=None
 if learning and learning.get('state')=='RESEARCH_REQUIRED':
  jp,job=ensure_job(lp,learning)
  if job.get('state') in {'RESEARCH_QUEUED','RESEARCHING','RESEARCH_BLOCKED'}:
   event('RESEARCHING',research_id=job.get('research_id'));rr=exec_json(RESEARCH_EXECUTOR,[jp]);job=read_json(jp,job) or job;st={**st,'last_research_diagnostic':rr,'research_id':job.get('research_id'),'research_job':str(jp),'last_event':job.get('state'),'driver_passed':False};atomic_json(STATE,st);atomic_json(HEARTBEAT,{'runtime':VERSION,'at':now(),'state':job.get('state'),'parent_goal':PARENT_GOAL,'research_id':job.get('research_id'),'next_tick_seconds':INTERVAL});publish(True)
   if job.get('state') not in {'KNOWLEDGE_RETURNED','PEER_RESEARCH_QUEUED'}:return
  if job.get('state')=='PEER_RESEARCH_QUEUED':
   peer=exec_json(PEER_BRIDGE,[jp],timeout=60);job=read_json(jp,job) or job;st={**st,'last_peer_diagnostic':peer,'last_event':job.get('state')};atomic_json(STATE,st);atomic_json(HEARTBEAT,{'runtime':VERSION,'at':now(),'state':job.get('state'),'parent_goal':PARENT_GOAL,'research_id':job.get('research_id'),'next_tick_seconds':INTERVAL});publish(True)
   if job.get('state')!='KNOWLEDGE_RETURNED':return
  if job.get('state')=='KNOWLEDGE_RETURNED':job=transition(jp,job,'EXPERIMENTING');reason='KNOWLEDGE_RETURNED_EXPERIMENT'
  elif job.get('state')=='RESUME_PARENT':reason='RESUME_PARENT'
  else:return
 elif not st.get('driver_passed'):reason='NO_USER_INPUT_CONTINUE'
 else:atomic_json(HEARTBEAT,{'runtime':VERSION,'at':now(),'state':'IDLE_HEALTHY','parent_goal':PARENT_GOAL,'next_tick_seconds':INTERVAL});return
 event('CONTINUE',reason=reason,parent_goal=PARENT_GOAL);result=drive(lp,learning,jp,job,reason);new={**st,'runtime':VERSION,'project_loop':PROJECT_LOOP,'parent_goal':PARENT_GOAL,'parent_message_id':PARENT_ID,'last_attempt_at':now(),'last_driver_ok':bool(result.get('ok')),'last_result_fingerprint':fp(result),'driver_passed':bool(result.get('ok')),'last_driver_diagnostic':{'returncode':result.get('returncode'),'stdout':(result.get('stdout') or '')[-4000:],'stderr':(result.get('stderr') or '')[-4000:],'parsed_result':result.get('result')}}
 if jp and job:
  if result.get('ok'):job=verify(jp,job,result);new['last_event']='RESUME_PARENT';new['research_state']='RESUME_PARENT'
  else:job=reject(jp,job,result);new['last_event']='RESEARCH_QUEUED';new['research_state']='RESEARCH_QUEUED';new['driver_passed']=False
 else:new['last_event']=reason
 atomic_json(STATE,new);atomic_json(HEARTBEAT,{'runtime':VERSION,'at':now(),'state':'PASS' if result.get('ok') else ('RESEARCH_QUEUED' if jp else 'RUNNING_WITH_FAILURE_EVIDENCE'),'parent_goal':PARENT_GOAL,'last_event':new['last_event'],'driver_ok':bool(result.get('ok')),'next_tick_seconds':INTERVAL});event('DRIVER_RESULT',reason=reason,ok=bool(result.get('ok')),returncode=result.get('returncode'));publish(True)
def main():
 RUNTIME.mkdir(parents=True,exist_ok=True)
 with LOCK.open('w') as lock:
  try:fcntl.flock(lock.fileno(),fcntl.LOCK_EX|fcntl.LOCK_NB)
  except BlockingIOError:return 0
  event('RUNTIME_STARTED',pid=os.getpid(),runtime=VERSION,project_loop=PROJECT_LOOP)
  while True:
   try:self_update();tick();publish(False)
   except subprocess.TimeoutExpired as e:event('ACTION_TIMEOUT',command=str(e.cmd))
   except Exception as e:event('RUNTIME_ERROR',error=repr(e))
   time.sleep(INTERVAL)
if __name__=='__main__':raise SystemExit(main())
