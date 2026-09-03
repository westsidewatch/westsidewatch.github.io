#!/usr/bin/env python3
"""Doré Resident Runtime v0.10 — thin durable execution substrate.

Runtime owns liveness/wake/process/checkpoint/self-update/telemetry only. Doré Agent
Core owns reasoning. Self-update is two-phase: sync the control manifest first,
then immediately re-read it and sync the complete declared control surface in the
same cycle, preventing newly-added runtime components from waiting another cycle.
"""
from __future__ import annotations
import fcntl, json, os, shutil, subprocess, sys, time
from datetime import datetime, timezone
from pathlib import Path
VERSION='dore.resident-runtime.v0.10'
HOME=Path(os.environ.get('DORE_LOCAL_HOME',Path.home()/'.dore')).expanduser();ROOT=Path(os.environ.get('DORE_REPO_ROOT',Path.home()/'westsidewatch.github.io')).expanduser();LOCAL=ROOT/'local'/'dore-local';RUNTIME=HOME/'runtime';A2A=ROOT/'dore-design'/'knowledge-lab'/'a2a';SELF=LOCAL/'resident_runtime.py';AGENT=LOCAL/'dore_agent_core.py';SUPERVISOR=LOCAL/'a2a_supervisor.py';COORDINATION=LOCAL/'coordination_worker.py';STATE=RUNTIME/'state.json';EVENTS=RUNTIME/'events.jsonl';HEARTBEAT=RUNTIME/'heartbeat.json';SUPERVISION=RUNTIME/'a2a-supervision.json';LOCK=RUNTIME/'runtime.lock';TELEMETRY_REPO=RUNTIME/'telemetry-repo';TELEMETRY_BRANCH=os.environ.get('DORE_RUNTIME_TELEMETRY_BRANCH','dore-runtime-telemetry');MANIFEST=A2A/'runtime-control-manifest.json'
INTERVAL=max(10,int(os.environ.get('DORE_RUNTIME_INTERVAL_SECONDS','30')));TELEMETRY_INTERVAL=max(60,int(os.environ.get('DORE_RUNTIME_TELEMETRY_SECONDS','120')));SELF_UPDATE_INTERVAL=max(120,int(os.environ.get('DORE_RUNTIME_SELF_UPDATE_SECONDS','300')))
def now():return datetime.now(timezone.utc).isoformat()
def read_json(p,default=None):
 try:return json.loads(Path(p).read_text(encoding='utf-8'))
 except Exception:return default
def atomic_json(p,v):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);t=p.with_suffix(p.suffix+'.tmp');t.write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8');t.replace(p)
def run(argv,cwd=ROOT,timeout=120,input_text=None,env=None):return subprocess.run(argv,cwd=str(cwd),text=True,capture_output=True,timeout=timeout,input=input_text,env=env)
def event(kind,**data):
 RUNTIME.mkdir(parents=True,exist_ok=True)
 with EVENTS.open('a',encoding='utf-8') as f:f.write(json.dumps({'at':now(),'event':kind,**data},ensure_ascii=False)+'\n')
def tail_events(n=64):
 if not EVENTS.exists():return []
 out=[]
 for line in EVENTS.read_text(encoding='utf-8',errors='replace').splitlines()[-n:]:
  try:out.append(json.loads(line))
  except Exception:out.append({'event':'UNPARSEABLE_EVENT','raw':line[-1000:]})
 return out
def agent_step():
 if not AGENT.exists():return {'ok':False,'state':'AGENT_CORE_MISSING','error':str(AGENT),'continue':True}
 env=os.environ.copy();env['PATH']='/opt/homebrew/bin:/usr/local/bin:'+env.get('PATH','/usr/bin:/bin:/usr/sbin:/sbin');env['DORE_A2A_SUPERVISION_FILE']=str(SUPERVISION)
 cp=run([sys.executable,str(AGENT)],timeout=1800,env=env);parsed=None
 try:parsed=json.loads((cp.stdout or '').strip().splitlines()[-1])
 except Exception:pass
 return {'ok':cp.returncode==0 and isinstance(parsed,dict) and bool(parsed.get('ok')),'returncode':cp.returncode,'stdout':(cp.stdout or '')[-12000:],'stderr':(cp.stderr or '')[-12000:],'result':parsed}
def supervisor_step(agent_result):
 if not SUPERVISOR.exists():return {'ok':False,'a2a_state':'A2A_SUPERVISOR_MISSING','action_required':'REPAIR_CONTROL_PLANE','peer_required':False}
 cp=run([sys.executable,str(SUPERVISOR)],timeout=60,input_text=json.dumps(agent_result,ensure_ascii=False));parsed=None
 try:parsed=json.loads((cp.stdout or '').strip().splitlines()[-1])
 except Exception:pass
 if not isinstance(parsed,dict):return {'ok':False,'a2a_state':'A2A_SUPERVISOR_ERROR','action_required':'REPAIR_CONTROL_PLANE','peer_required':False,'stderr':(cp.stderr or '')[-2000:]}
 return parsed
def coordination_step():
 if not COORDINATION.exists():return {'ok':False,'state':'COORDINATION_WORKER_MISSING'}
 env=os.environ.copy();env['PATH']='/opt/homebrew/bin:/usr/local/bin:'+env.get('PATH','/usr/bin:/bin:/usr/sbin:/sbin')
 try:
  child=subprocess.Popen([sys.executable,str(COORDINATION)],cwd=str(ROOT),env=env,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,start_new_session=True);return {'ok':True,'state':'SPAWNED','pid':child.pid}
 except Exception as e:return {'ok':False,'state':'SPAWN_FAILED','error':type(e).__name__+': '+str(e)}
def telemetry_repo():
 remote=run(['git','remote','get-url','origin'],timeout=30)
 if remote.returncode or not remote.stdout.strip():raise RuntimeError('origin_remote_unavailable')
 if not (TELEMETRY_REPO/'.git').exists():
  if TELEMETRY_REPO.exists():shutil.rmtree(TELEMETRY_REPO)
  cp=run(['git','clone','--filter=blob:none','--no-checkout',remote.stdout.strip(),str(TELEMETRY_REPO)],cwd=RUNTIME,timeout=180)
  if cp.returncode:raise RuntimeError('telemetry_clone_failed')
  run(['git','config','user.name','DORE-RUNTIME'],cwd=TELEMETRY_REPO);run(['git','config','user.email','westsidewatchca@gmail.com'],cwd=TELEMETRY_REPO)
 return TELEMETRY_REPO
def snapshot():
 st=read_json(STATE,{}) or {};hb=read_json(HEARTBEAT,{}) or {};sup=read_json(SUPERVISION,{}) or {};result=st.get('last_agent_result') or {};agent=(result.get('result') or {}) if isinstance(result,dict) else {}
 try:
  sys.path.insert(0,str(LOCAL));from goal_queue import load;goals=load()
 except Exception:goals={}
 return {'schema':'dore.runtime.telemetry.v0.9','published_at':now(),'runtime':VERSION,'ownership':{'supervisor':'launchd','runtime':'wake/process/checkpoint/self-update/telemetry','a2a_supervisor':'asynchronous peer visibility/nonblocking health','agent_core':'reason/research/learn/experiment/verify/promote/next-action'},'a2a_supervision':sup,'agent_core':agent.get('agent_core'),'agent_state':agent.get('state'),'parent':agent.get('parent'),'goal_queue':goals,'heartbeat':hb,'state':st,'a2a_task':agent.get('a2a_task'),'research_job':agent.get('research_job'),'events':tail_events()}
def publish(force=False):
 st=read_json(STATE,{}) or {};last=float(st.get('last_telemetry_epoch') or 0)
 if not force and time.time()-last<TELEMETRY_INTERVAL:return
 repo=telemetry_repo();run(['git','fetch','origin',f'+refs/heads/{TELEMETRY_BRANCH}:refs/remotes/origin/{TELEMETRY_BRANCH}'],cwd=repo,timeout=90);exists=run(['git','show-ref','--verify',f'refs/remotes/origin/{TELEMETRY_BRANCH}'],cwd=repo,timeout=30).returncode==0;cp=run(['git','checkout','-B',TELEMETRY_BRANCH,f'origin/{TELEMETRY_BRANCH}'],cwd=repo,timeout=60) if exists else run(['git','checkout','--orphan',TELEMETRY_BRANCH],cwd=repo,timeout=60)
 if cp.returncode:raise RuntimeError('telemetry_checkout_failed')
 (repo/'runtime-latest.json').write_text(json.dumps(snapshot(),ensure_ascii=False,indent=2)+'\n',encoding='utf-8');run(['git','add','runtime-latest.json'],cwd=repo)
 if run(['git','diff','--cached','--quiet'],cwd=repo).returncode:
  if run(['git','commit','-m','chore(dore): publish resident runtime telemetry'],cwd=repo).returncode:raise RuntimeError('telemetry_commit_failed')
  if run(['git','push','origin',f'HEAD:{TELEMETRY_BRANCH}'],cwd=repo,timeout=120).returncode:raise RuntimeError('telemetry_push_failed')
 st=read_json(STATE,{}) or {};st['last_telemetry_epoch']=time.time();st['last_telemetry_at']=now();atomic_json(STATE,st)
def fallback_paths():return ['local/dore-local/resident_runtime.py','local/dore-local/a2a_supervisor.py','local/dore-local/dore_agent_core.py','local/dore-local/autonomous_driver.py','local/dore-local/research_executor.py','local/dore-local/peer_research_bridge.py','local/dore-local/autonomous_capability_loop.py','local/dore-local/failure_memory.py','local/dore-local/shared_learning.py','local/dore-local/a2a_adapter.py','local/dore-local/goal_queue.py','local/dore-local/knowledge_experiment.py','local/dore-local/coordination_goal_executor.py','local/dore-local/coordination_worker.py','local/dore-local/coordination_mailbox.py','local/dore-local/loop_contract_acceptance.py','dore-design/knowledge-lab/resources/source-catalog.json','dore-design/knowledge-lab/a2a/project-state.json','dore-design/knowledge-lab/a2a/loop-contract-v1.json','dore-design/knowledge-lab/a2a/agent-card.json','dore-design/knowledge-lab/a2a/runtime-control-manifest.json','dore-design/knowledge-lab/skills/registry.json']
def update_paths():
 manifest=read_json(MANIFEST,{}) or {};paths=[]
 for key in ('required_files','runtime_files','files'):
  v=manifest.get(key)
  if isinstance(v,list):paths.extend(str(x) for x in v if isinstance(x,str))
 return list(dict.fromkeys(paths or fallback_paths()))
def sync_remote_file(rel):
 target=ROOT/rel;show=run(['git','show',f'origin/main:{rel}'],timeout=60)
 if show.returncode:return False
 local=target.read_text(encoding='utf-8') if target.exists() else ''
 if show.stdout==local:return False
 target.parent.mkdir(parents=True,exist_ok=True);tmp=target.with_suffix(target.suffix+'.remote');tmp.write_text(show.stdout,encoding='utf-8');tmp.replace(target);return True
def self_update():
 st=read_json(STATE,{}) or {};last=float(st.get('last_self_update_check_epoch') or 0)
 if time.time()-last<SELF_UPDATE_INTERVAL:return
 st['last_self_update_check_epoch']=time.time();st['last_self_update_check_at']=now();atomic_json(STATE,st);fetch=run(['git','fetch','origin','+refs/heads/main:refs/remotes/origin/main'],timeout=120)
 if fetch.returncode:event('SELF_UPDATE_FETCH_FAILED',detail=(fetch.stderr or fetch.stdout)[-2000:]);return
 changed=[];manifest_rel='dore-design/knowledge-lab/a2a/runtime-control-manifest.json'
 # Phase 1: manifest first, so newly-declared files are visible immediately.
 if sync_remote_file(manifest_rel):changed.append(manifest_rel);event('CONTROL_MANIFEST_UPDATED',source='origin/main')
 # Phase 2: re-read the freshly synced manifest and apply the entire declared surface.
 for rel in update_paths():
  if rel==manifest_rel:continue
  if sync_remote_file(rel):changed.append(rel)
 if changed:
  event('SELF_UPDATED',files=changed,source='origin/main',two_phase_manifest_sync=True);publish(True)
  if 'local/dore-local/resident_runtime.py' in changed:os.execv(sys.executable,[sys.executable,str(SELF)])
def tick():
 event('WAKE',reason='NO_USER_INPUT_CONTINUE');coordination=coordination_step();event('COORDINATION_OBSERVATION',**coordination);result=agent_step();parsed=(result.get('result') or {}) if isinstance(result,dict) else {};state=str(parsed.get('state') or ('AGENT_ERROR' if not result.get('ok') else 'UNKNOWN'));supervision=supervisor_step(result);atomic_json(SUPERVISION,supervision);st=read_json(STATE,{}) or {};st.update({'runtime':VERSION,'last_tick_at':now(),'last_event':'A2A_SUPERVISION','last_coordination_result':coordination,'last_agent_state':state,'last_agent_result':result,'last_a2a_state':supervision.get('a2a_state'),'last_a2a_action':supervision.get('action_required')});atomic_json(STATE,st);atomic_json(HEARTBEAT,{'runtime':VERSION,'at':now(),'state':state,'coordination_state':coordination.get('state'),'a2a_state':supervision.get('a2a_state'),'a2a_action':supervision.get('action_required'),'peer_required':supervision.get('peer_required',False),'peer_blocking':supervision.get('peer_blocking',False),'agent_core':parsed.get('agent_core'),'continue':parsed.get('continue',True),'next_tick_seconds':INTERVAL});event('AGENT_OBSERVATION',state=state,ok=bool(result.get('ok')),returncode=result.get('returncode'));event('A2A_SUPERVISION',a2a_state=supervision.get('a2a_state'),action=supervision.get('action_required'),peer_required=supervision.get('peer_required'),peer_blocking=supervision.get('peer_blocking'),unchanged_cycles=supervision.get('unchanged_cycles'));publish(True)
def main():
 RUNTIME.mkdir(parents=True,exist_ok=True)
 with LOCK.open('w') as lock:
  try:fcntl.flock(lock.fileno(),fcntl.LOCK_EX|fcntl.LOCK_NB)
  except BlockingIOError:return 0
  event('RUNTIME_STARTED',pid=os.getpid(),runtime=VERSION,role='thin-execution-substrate')
  while True:
   try:self_update();tick();publish(False)
   except subprocess.TimeoutExpired as e:event('ACTION_TIMEOUT',command=str(e.cmd),timeout=e.timeout)
   except Exception as e:event('RUNTIME_ERROR',error=repr(e))
   time.sleep(INTERVAL)
if __name__=='__main__':raise SystemExit(main())
