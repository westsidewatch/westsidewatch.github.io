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
 if old==new: save_state({'ok':True,'updated':False,'head':old,'checked_at':now()}); return 0
 rc,_,err=run(['git','merge','--ff-only','origin/main'])
 if rc!=0: emit('error',stage='fast_forward',detail=err,old=old,new=new); return 6
 targets=['local/dore-local/dore_local.py','local/dore-local/legacy_memory.py','local/dore-local/self_memory.py','local/dore-local/local_updater.py']
 rc,_,err=run(['python3','-m','py_compile',*targets])
 if rc!=0: emit('error',stage='compile',detail=err,old=old,new=new); return 7
 uid=str(os.getuid()); subprocess.run(['launchctl','kickstart','-k',f'gui/{uid}/{LABEL}'],capture_output=True,text=True); time.sleep(2)
 try:
  health=get_json('http://127.0.0.1:8788/health'); legacy=get_json('http://127.0.0.1:8788/legacy-memory/status'); selfmem=get_json('http://127.0.0.1:8788/memory/self/status'); learning=get_json('http://127.0.0.1:8788/learning/status')
  ok=all(bool(x.get('ok')) for x in (health,legacy,selfmem,learning)) and len(selfmem.get('self_memory') or [])>=4 and (learning.get('learning') or {}).get('total',0)>=4
 except Exception as e: emit('error',stage='health',detail=str(e),old=old,new=new); return 8
 state={'ok':ok,'updated':True,'from':old,'head':new,'health':health,'legacy_status':legacy,'self_status':selfmem,'learning_status':learning,'checked_at':now()}; save_state(state)
 emit('updated',old=old,new=new,legacy_total=(legacy.get('legacy_memory') or {}).get('total'),self_total=len(selfmem.get('self_memory') or []),learning_total=(learning.get('learning') or {}).get('total'))
 return 0 if ok else 9
if __name__=='__main__': raise SystemExit(main())
