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
def spawn_learning_worker():
 worker=ROOT/'local/dore-local/learning_worker.py'
 if not worker.exists(): return False
 # Learning from a dirty working tree would allow ephemeral, unreviewed code to become evidence.
 rc,dirty,_=run(['git','status','--porcelain'])
 if rc!=0 or dirty:
  emit('learning_worker_skipped',reason='dirty_worktree'); return False
 out=DORE/'logs'/'learning-worker.stdout.log'; err=DORE/'logs'/'learning-worker.stderr.log'; out.parent.mkdir(parents=True,exist_ok=True)
 env=os.environ.copy(); env['DORE_REPO_ROOT']=str(ROOT); env['DORE_LOCAL_HOME']=str(DORE)
 try:
  with out.open('a') as fo, err.open('a') as fe: subprocess.Popen(['python3',str(worker)],cwd=ROOT,env=env,stdout=fo,stderr=fe,start_new_session=True)
  emit('learning_worker_spawned'); return True
 except Exception as e: emit('learning_worker_spawn_failed',detail=str(e)); return False
def main():
 if not (ROOT/'.git').exists(): emit('skip',reason='repo_missing'); return 0
 rc,out,err=run(['git','status','--porcelain'])
 if rc!=0: emit('error',stage='status',detail=err); return 2
 if out: emit('skip',reason='dirty_worktree'); return 0
 rc,old,err=run(['git','rev-parse','HEAD'])
 if rc!=0: emit('error',stage='head',detail=err); return 3
 rc,_,err=run(['git','fetch','origin','main'])
 if rc!=0: emit('error',stage='fetch',detail=err); return 4
 rc,new,err=run(['git','rev-parse','origin/main'])
 if rc!=0: emit('error',stage='origin_head',detail=err); return 5
 if old==new:
  spawned=spawn_learning_worker(); save_state({'ok':True,'updated':False,'head':old,'learning_worker_spawned':spawned,'checked_at':now()}); return 0
 rc,_,err=run(['git','merge','--ff-only','origin/main'])
 if rc!=0: emit('error',stage='fast_forward',detail=err,old=old,new=new); return 6
 targets=['local/dore-local/dore_local.py','local/dore-local/legacy_memory.py','local/dore-local/self_memory.py','local/dore-local/learning_planner.py','local/dore-local/autonomous_learner.py','local/dore-local/learning_worker.py','local/dore-local/local_updater.py']
 rc,_,err=run(['python3','-m','py_compile',*targets])
 if rc!=0: emit('error',stage='compile',detail=err,old=old,new=new); return 7
 uid=str(os.getuid()); subprocess.run(['launchctl','kickstart','-k',f'gui/{uid}/{LABEL}'],capture_output=True,text=True); time.sleep(2)
 try:
  health=get_json('http://127.0.0.1:8788/health'); legacy=get_json('http://127.0.0.1:8788/legacy-memory/status'); selfmem=get_json('http://127.0.0.1:8788/memory/self/status'); learning=get_json('http://127.0.0.1:8788/learning/status'); planner=get_json('http://127.0.0.1:8788/learning/plan'); autonomous=get_json('http://127.0.0.1:8788/learning/autonomous/status')
  ok=all(bool(x.get('ok')) for x in (health,legacy,selfmem,learning,planner,autonomous)) and len(selfmem.get('self_memory') or [])>=4 and (learning.get('learning') or {}).get('total',0)>=4 and planner.get('time_is_gate') is False
 except Exception as e: emit('error',stage='health',detail=str(e),old=old,new=new); return 8
 spawned=spawn_learning_worker(); state={'ok':ok,'updated':True,'from':old,'head':new,'health':health,'legacy_status':legacy,'self_status':selfmem,'learning_status':learning,'learning_plan':planner,'autonomous_learning_status':autonomous,'learning_worker_spawned':spawned,'checked_at':now()}; save_state(state)
 emit('updated',old=old,new=new,legacy_total=(legacy.get('legacy_memory') or {}).get('total'),self_total=len(selfmem.get('self_memory') or []),learning_total=(learning.get('learning') or {}).get('total'),autonomous_runs=len(autonomous.get('runs') or []),learning_worker_spawned=spawned)
 return 0 if ok else 9
if __name__=='__main__': raise SystemExit(main())
