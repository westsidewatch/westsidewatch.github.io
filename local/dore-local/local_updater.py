#!/usr/bin/env python3
from __future__ import annotations
import json, os, subprocess, time
from datetime import datetime, timezone
from pathlib import Path
ROOT=Path(os.environ.get('DORE_REPO_ROOT',Path.home()/'westsidewatch.github.io')).expanduser(); DORE=Path(os.environ.get('DORE_LOCAL_HOME',Path.home()/'.dore')).expanduser()
STATE=DORE/'data'/'updater-state.json'; LOG=DORE/'logs'/'updater-events.jsonl'; LABEL='io.westsidewatch.dore-local'
def now(): return datetime.now(timezone.utc).isoformat()
def run(args,timeout=90):
 p=subprocess.run(args,cwd=ROOT,text=True,capture_output=True,timeout=timeout); return p.returncode,p.stdout.strip(),p.stderr.strip()
def emit(event,**extra):
 LOG.parent.mkdir(parents=True,exist_ok=True); rec={'ts':now(),'event':event,**extra}
 with LOG.open('a',encoding='utf-8') as f:f.write(json.dumps(rec,ensure_ascii=False)+'\n')
def save_state(data): STATE.parent.mkdir(parents=True,exist_ok=True); STATE.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
def get_json(url):
 import urllib.request
 return json.loads(urllib.request.urlopen(url,timeout=5).read())
def spawn_worker(name,script):
 worker=ROOT/'local/dore-local'/script
 if not worker.exists(): return False
 rc,dirty,_=run(['git','status','--porcelain'])
 if rc!=0 or dirty: emit(name+'_skipped',reason='dirty_worktree'); return False
 out=DORE/'logs'/(name+'.stdout.log'); err=DORE/'logs'/(name+'.stderr.log'); out.parent.mkdir(parents=True,exist_ok=True); env=os.environ.copy(); env['DORE_REPO_ROOT']=str(ROOT); env['DORE_LOCAL_HOME']=str(DORE)
 try:
  with out.open('a') as fo, err.open('a') as fe: subprocess.Popen(['python3',str(worker)],cwd=worker.parent,env=env,stdout=fo,stderr=fe,start_new_session=True)
  emit(name+'_spawned'); return True
 except Exception as e: emit(name+'_spawn_failed',detail=str(e)); return False
def spawn_workers(): return spawn_worker('learning-worker','learning_worker.py'),spawn_worker('coordination-worker','coordination_worker.py')
def main():
 if not (ROOT/'.git').exists(): emit('skip',reason='repo_missing'); return 0
 rc,out,err=run(['git','status','--porcelain']);
 if rc!=0: emit('error',stage='status',detail=err); return 2
 if out: emit('skip',reason='dirty_worktree'); return 0
 rc,old,err=run(['git','rev-parse','HEAD']);
 if rc!=0:return 3
 rc,_,err=run(['git','fetch','origin','main']);
 if rc!=0: emit('error',stage='fetch',detail=err); return 4
 rc,new,err=run(['git','rev-parse','origin/main']);
 if rc!=0:return 5
 if old!=new:
  rc,_,err=run(['git','merge','--ff-only','origin/main'])
  if rc!=0:
   # A Doré-originated coordination commit may race a remote ChatGPT commit. Rebase it instead of stalling.
   rc,_,err=run(['git','rebase','origin/main'])
   if rc!=0: emit('error',stage='sync',detail=err,old=old,new=new); return 6
 targets=['local/dore-local/dore_local.py','local/dore-local/legacy_memory.py','local/dore-local/self_memory.py','local/dore-local/learning_planner.py','local/dore-local/autonomous_learner.py','local/dore-local/learning_worker.py','local/dore-local/bridge_reminder.py','local/dore-local/coordination_mailbox.py','local/dore-local/coordination_worker.py','local/dore-local/local_updater.py']
 rc,_,err=run(['python3','-m','py_compile',*targets]);
 if rc!=0: emit('error',stage='compile',detail=err); return 7
 uid=str(os.getuid()); subprocess.run(['launchctl','kickstart','-k',f'gui/{uid}/{LABEL}'],capture_output=True,text=True); time.sleep(2)
 if old!=new:
  try:
   health=get_json('http://127.0.0.1:8788/health'); legacy=get_json('http://127.0.0.1:8788/legacy-memory/status'); selfmem=get_json('http://127.0.0.1:8788/memory/self/status'); learning=get_json('http://127.0.0.1:8788/learning/status'); planner=get_json('http://127.0.0.1:8788/learning/plan'); autonomous=get_json('http://127.0.0.1:8788/learning/autonomous/status'); ok=all(bool(x.get('ok')) for x in (health,legacy,selfmem,learning,planner,autonomous)) and planner.get('time_is_gate') is False
  except Exception as e: emit('error',stage='health',detail=str(e)); return 8
 else: ok=True
 learning_spawned,coordination_spawned=spawn_workers(); head=run(['git','rev-parse','HEAD'])[1]; save_state({'ok':ok,'updated':old!=new,'head':head,'learning_worker_spawned':learning_spawned,'coordination_worker_spawned':coordination_spawned,'checked_at':now()}); emit('tick',head=head,coordination_worker_spawned=coordination_spawned); return 0 if ok else 9
if __name__=='__main__': raise SystemExit(main())
