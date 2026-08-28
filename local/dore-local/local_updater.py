#!/usr/bin/env python3
from __future__ import annotations
import json, os, subprocess, time
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(os.environ.get('DORE_REPO_ROOT',Path.home()/'westsidewatch.github.io')).expanduser()
DORE=Path(os.environ.get('DORE_LOCAL_HOME',Path.home()/'.dore')).expanduser()
STATE=DORE/'data'/'updater-state.json'
LOG=DORE/'logs'/'updater-events.jsonl'
LABEL='io.westsidewatch.dore-local'

def now(): return datetime.now(timezone.utc).isoformat()
def run(args,timeout=90):
    p=subprocess.run(args,cwd=ROOT,text=True,capture_output=True,timeout=timeout)
    return p.returncode,p.stdout.strip(),p.stderr.strip()
def emit(event,**extra):
    LOG.parent.mkdir(parents=True,exist_ok=True)
    rec={'ts':now(),'event':event,**extra}
    with LOG.open('a',encoding='utf-8') as f:f.write(json.dumps(rec,ensure_ascii=False)+'\n')
def save_state(data):
    STATE.parent.mkdir(parents=True,exist_ok=True)
    STATE.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')

def main():
    if not (ROOT/'.git').exists():
        emit('skip',reason='repo_missing'); return 0
    rc,out,err=run(['git','status','--porcelain'])
    if rc!=0: emit('error',stage='status',detail=err); return 2
    # Never overwrite local work. Autonomous updater fails closed when repo is dirty.
    if out:
        emit('skip',reason='dirty_worktree'); return 0
    rc,old,err=run(['git','rev-parse','HEAD'])
    if rc!=0: emit('error',stage='head',detail=err); return 3
    rc,_,err=run(['git','fetch','origin','main'])
    if rc!=0: emit('error',stage='fetch',detail=err); return 4
    rc,new,err=run(['git','rev-parse','origin/main'])
    if rc!=0: emit('error',stage='origin_head',detail=err); return 5
    if old==new:
        save_state({'ok':True,'updated':False,'head':old,'checked_at':now()}); return 0
    rc,_,err=run(['git','merge','--ff-only','origin/main'])
    if rc!=0: emit('error',stage='fast_forward',detail=err,old=old,new=new); return 6
    # Static compile before restart; if compile fails, leave evidence and do not restart.
    targets=['local/dore-local/dore_local.py','local/dore-local/legacy_memory.py']
    rc,_,err=run(['python3','-m','py_compile',*targets])
    if rc!=0:
        emit('error',stage='compile',detail=err,old=old,new=new); return 7
    uid=str(os.getuid())
    subprocess.run(['launchctl','kickstart','-k',f'gui/{uid}/{LABEL}'],capture_output=True,text=True)
    time.sleep(2)
    try:
        import urllib.request
        health=json.loads(urllib.request.urlopen('http://127.0.0.1:8788/health',timeout=5).read())
        status=json.loads(urllib.request.urlopen('http://127.0.0.1:8788/legacy-memory/status',timeout=5).read())
        ok=bool(health.get('ok')) and bool(status.get('ok'))
    except Exception as e:
        emit('error',stage='health',detail=str(e),old=old,new=new); return 8
    save_state({'ok':ok,'updated':True,'from':old,'head':new,'health':health,'legacy_status':status,'checked_at':now()})
    emit('updated',old=old,new=new,legacy_total=(status.get('legacy_memory') or {}).get('total'))
    return 0 if ok else 9

if __name__=='__main__': raise SystemExit(main())
