#!/usr/bin/env python3
"""Resident coordination daemon: continuously sync repo and drain Doré inbox.

This closes the gap where heartbeat stayed alive while coordination tasks waited
unconsumed. One process owns the loop; every cycle fetches/pulls, drains bounded
work, records status, and backs off only when idle/erroring.
"""
from __future__ import annotations
import json, os, subprocess, time, traceback
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(os.environ.get('DORE_REPO_ROOT',Path.home()/'westsidewatch.github.io')).expanduser()
HOME=Path(os.environ.get('DORE_LOCAL_HOME',Path.home()/'.dore')).expanduser()
STATE=HOME/'coordination'/'daemon-state.json'
INTERVAL=max(5,int(os.environ.get('DORE_COORDINATION_INTERVAL_SECONDS','15')))

def run(argv,timeout=120):
 return subprocess.run(argv,cwd=ROOT,text=True,capture_output=True,timeout=timeout)
def save(**kw):
 STATE.parent.mkdir(parents=True,exist_ok=True)
 old={}
 try: old=json.loads(STATE.read_text()) if STATE.exists() else {}
 except: pass
 old.update(kw);old['updated_at']=datetime.now(timezone.utc).isoformat()
 STATE.write_text(json.dumps(old,ensure_ascii=False,indent=2))
def sync():
 cp=run(['git','pull','--ff-only'],180)
 return {'ok':cp.returncode==0,'stdout':(cp.stdout or '')[-3000:],'stderr':(cp.stderr or '')[-3000:]}
def drain():
 cp=run(['python3',str(ROOT/'local/dore-local/coordination_worker.py')],3600)
 return {'ok':cp.returncode==0,'returncode':cp.returncode,'stdout':(cp.stdout or '')[-5000:],'stderr':(cp.stderr or '')[-5000:]}
def main():
 save(pid=os.getpid(),status='starting',interval_seconds=INTERVAL)
 while True:
  try:
   s=sync()
   if not s['ok']:
    save(status='sync_error',last_sync=s);time.sleep(INTERVAL);continue
   d=drain();save(status='healthy' if d['ok'] else 'worker_error',last_sync=s,last_drain=d)
  except Exception as e:
   save(status='daemon_error',error=type(e).__name__+': '+str(e),traceback=traceback.format_exc()[-4000:])
  time.sleep(INTERVAL)
if __name__=='__main__':main()
