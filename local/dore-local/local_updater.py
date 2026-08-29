#!/usr/bin/env python3
from __future__ import annotations
import json, os, subprocess, time
from datetime import datetime, timezone
from pathlib import Path
ROOT=Path(os.environ.get('DORE_REPO_ROOT',Path.home()/'westsidewatch.github.io')).expanduser(); DORE=Path(os.environ.get('DORE_LOCAL_HOME',Path.home()/'.dore')).expanduser(); STATE=DORE/'data'/'updater-state.json'; LOG=DORE/'logs'/'updater-events.jsonl'; LABEL='io.westsidewatch.dore-local'; TASKS=ROOT/'local/dore-local/tasks'; TASK_STATE=DORE/'data'/'local-task-state.json'
def now():return datetime.now(timezone.utc).isoformat()
def run(args,timeout=90):
 p=subprocess.run(args,cwd=ROOT,text=True,capture_output=True,timeout=timeout); return p.returncode,p.stdout.strip(),p.stderr.strip()
def emit(event,**extra):
 LOG.parent.mkdir(parents=True,exist_ok=True)
 with LOG.open('a',encoding='utf-8') as f:f.write(json.dumps({'ts':now(),'event':event,**extra},ensure_ascii=False)+'\n')
def save_state(x):STATE.parent.mkdir(parents=True,exist_ok=True); STATE.write_text(json.dumps(x,ensure_ascii=False,indent=2))
def get_json(url):
 import urllib.request; return json.loads(urllib.request.urlopen(url,timeout=5).read())
def spawn(name,script):
 worker=ROOT/'local/dore-local'/script
 if not worker.exists() or run(['git','status','--porcelain'])[1]:return False
 env=os.environ.copy(); env['DORE_REPO_ROOT']=str(ROOT); env['DORE_LOCAL_HOME']=str(DORE); out=DORE/'logs'/(name+'.stdout.log'); err=DORE/'logs'/(name+'.stderr.log'); out.parent.mkdir(parents=True,exist_ok=True)
 try:
  with out.open('a') as fo,err.open('a') as fe:subprocess.Popen(['python3',str(worker)],cwd=worker.parent,env=env,stdout=fo,stderr=fe,start_new_session=True)
  return True
 except Exception:return False
def load_task_state():
 try:return json.loads(TASK_STATE.read_text())
 except Exception:return {'processed':[]}
def save_task_state(s):TASK_STATE.parent.mkdir(parents=True,exist_ok=True); TASK_STATE.write_text(json.dumps(s,ensure_ascii=False,indent=2))
def run_pending_acceptance():
 state=load_task_state(); done=set(state.get('processed') or [])
 if not TASKS.exists():return False
 for p in sorted(TASKS.glob('*.json')):
  try:t=json.loads(p.read_text(encoding='utf-8'))
  except Exception:continue
  tid=str(t.get('task_id') or p.name)
  if tid in done or t.get('kind')!='conversation_acceptance_v1':continue
  script=ROOT/'local/dore-local/conversation_acceptance.py'; emit('acceptance_start',task_id=tid)
  try:cp=subprocess.run(['python3',str(script)],cwd=ROOT,text=True,capture_output=True,timeout=1200)
  except Exception as e:emit('acceptance_error',task_id=tid,detail=repr(e));return True
  raw=(cp.stdout or cp.stderr or '').strip(); evidence=DORE/'data'/f'{tid}.json'
  try:obj=json.loads(raw)
  except Exception:obj={'schema':'dore.conversation-acceptance.v1','task_id':tid,'pass':False,'returncode':cp.returncode,'raw':raw[-20000:]}
  obj['task_id']=tid; obj['executed_at']=now(); evidence.write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')
  # Use the already-tested git-backed mailbox transport to publish the full result to ChatGPT.
  try:
   import sys; sys.path.insert(0,str(ROOT/'local/dore-local'))
   from coordination_mailbox import send_to_chatgpt,flush_outbox
   send_to_chatgpt('Doré conversation acceptance',json.dumps(obj,ensure_ascii=False),requires_reply=False,priority='high',related_goal='persistent-conversation-interface',evidence_refs=[str(evidence)],thread_id='dore-conversation-acceptance-001'); flush_outbox()
  except Exception as e:emit('acceptance_publish_error',task_id=tid,detail=repr(e))
  done.add(tid); state['processed']=sorted(done); state['last_result']=obj; save_task_state(state); emit('acceptance_done',task_id=tid,passed=bool(obj.get('pass')),rounds=obj.get('rounds_attempted'),checks=f"{obj.get('checks_passed')}/{obj.get('checks_total')}"); return True
 return False
def main():
 if not (ROOT/'.git').exists():return 0
 rc,dirty,err=run(['git','status','--porcelain']);
 if rc or dirty:return 0
 old=run(['git','rev-parse','HEAD'])[1]
 if run(['git','fetch','origin','main'])[0]:return 4
 remote=run(['git','rev-parse','origin/main'])[1]
 if old!=remote:
  if run(['git','merge','--ff-only','origin/main'])[0] and run(['git','rebase','origin/main'])[0]:return 6
 targets=['local/dore-local/dore_local.py','local/dore-local/legacy_memory.py','local/dore-local/self_memory.py','local/dore-local/learning_planner.py','local/dore-local/autonomous_learner.py','local/dore-local/learning_worker.py','local/dore-local/bridge_reminder.py','local/dore-local/coordination_mailbox.py','local/dore-local/coordination_worker.py','local/dore-local/conversation_acceptance.py','local/dore-local/test_conversation_interface_contract.py','local/dore-local/local_updater.py','local/dore-local/test_coordination_transport.py']
 if run(['python3','-m','py_compile',*targets])[0]:return 7
 test=run(['python3','local/dore-local/test_coordination_transport.py'],timeout=30)
 if test[0] or 'DORE_COORDINATION_TRANSPORT_CONTRACT_PASS' not in test[1]:emit('error',stage='coordination_contract',detail=test[2] or test[1]); return 10
 ui=run(['python3','local/dore-local/test_conversation_interface_contract.py'],timeout=30)
 if ui[0] or 'DORE_CONVERSATION_INTERFACE_CONTRACT_PASS' not in ui[1]:emit('error',stage='conversation_interface_contract',detail=ui[2] or ui[1]);return 11
 uid=str(os.getuid()); subprocess.run(['launchctl','kickstart','-k',f'gui/{uid}/{LABEL}'],capture_output=True,text=True); time.sleep(2)
 ok=True
 if old!=remote:
  try:
   checks=[get_json('http://127.0.0.1:8788'+p) for p in ['/health','/legacy-memory/status','/memory/self/status','/learning/status','/learning/plan','/learning/autonomous/status']]; ok=all(bool(x.get('ok')) for x in checks) and checks[4].get('time_is_gate') is False
  except Exception as e:emit('error',stage='health',detail=str(e));return 8
 # Acceptance runs synchronously before any autonomous worker can dirty the shared worktree.
 if run_pending_acceptance():
  head=run(['git','rev-parse','HEAD'])[1];save_state({'ok':ok,'updated':old!=remote,'head':head,'coordination_contract':'PASS','conversation_interface_contract':'PASS','acceptance_dispatched':True,'checked_at':now()});return 0
 coordination=spawn('coordination-worker','coordination_worker.py'); learning=spawn('learning-worker','learning_worker.py'); head=run(['git','rev-parse','HEAD'])[1]; save_state({'ok':ok,'updated':old!=remote,'head':head,'coordination_contract':'PASS','conversation_interface_contract':'PASS','learning_worker_spawned':learning,'coordination_worker_spawned':coordination,'checked_at':now()}); emit('tick',head=head,coordination_contract='PASS',coordination_worker_spawned=coordination); return 0 if ok else 9
if __name__=='__main__':raise SystemExit(main())
