#!/usr/bin/env python3
"""Resident coordination daemon: safely sync repo and continuously drain Doré inbox."""
from __future__ import annotations
import json, os, subprocess, time, traceback
from datetime import datetime, timezone
from pathlib import Path
ROOT=Path(os.environ.get('DORE_REPO_ROOT',Path.home()/'westsidewatch.github.io')).expanduser();HOME=Path(os.environ.get('DORE_LOCAL_HOME',Path.home()/'.dore')).expanduser();STATE=HOME/'coordination'/'daemon-state.json';INTERVAL=max(5,int(os.environ.get('DORE_COORDINATION_INTERVAL_SECONDS','15')));REMOTE=os.environ.get('DORE_COORDINATION_REMOTE','origin');BRANCH=os.environ.get('DORE_COORDINATION_BRANCH','main')
def run(argv,timeout=120):return subprocess.run(argv,cwd=ROOT,text=True,capture_output=True,timeout=timeout)
def tail(cp,n=4000):return {'returncode':cp.returncode,'stdout':(cp.stdout or '')[-n:],'stderr':(cp.stderr or '')[-n:]}
def save(**kw):
 STATE.parent.mkdir(parents=True,exist_ok=True);old={}
 try:old=json.loads(STATE.read_text()) if STATE.exists() else {}
 except:pass
 old.update(kw);old['updated_at']=datetime.now(timezone.utc).isoformat();tmp=STATE.with_suffix('.tmp');tmp.write_text(json.dumps(old,ensure_ascii=False,indent=2));tmp.replace(STATE)
def git(*args,timeout=120):return run(['git',*args],timeout)
def rev(name):
 cp=git('rev-parse',name);return cp.stdout.strip() if cp.returncode==0 else None
def clean_tree():
 cp=git('status','--porcelain');return cp.returncode==0 and not cp.stdout.strip()
def counts():
 cp=git('rev-list','--left-right','--count',f'HEAD...{REMOTE}/{BRANCH}')
 if cp.returncode:return None
 a,b=cp.stdout.strip().split();return int(a),int(b)
def sync():
 fetch=git('fetch','--prune',REMOTE,BRANCH,timeout=180);e={'stage':'fetch','fetch':tail(fetch)}
 if fetch.returncode:e.update(ok=False,classification='fetch_failed');return e
 local,remote=rev('HEAD'),rev(f'{REMOTE}/{BRANCH}');e.update(local=local,remote=remote)
 if not local or not remote:e.update(ok=False,classification='rev_parse_failed');return e
 if local==remote:e.update(ok=True,classification='already_aligned');return e
 c=counts()
 if c is None:e.update(ok=False,classification='topology_unknown');return e
 ahead,behind=c;e.update(ahead=ahead,behind=behind,clean=clean_tree())
 if ahead==0 and behind>0:
  cp=git('merge','--ff-only',f'{REMOTE}/{BRANCH}',timeout=180);e['reconcile']=tail(cp);e.update(ok=cp.returncode==0,classification='fast_forward' if cp.returncode==0 else 'fast_forward_failed');return e
 if ahead>0 and behind==0:e.update(ok=True,classification='local_ahead');return e
 if ahead>0 and behind>0:
  if not e['clean']:e.update(ok=False,classification='diverged_dirty_requires_dore_reconcile');return e
  backup=f'dore/rescue-{datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")}';b=git('branch',backup,'HEAD')
  if b.returncode:e['backup']=tail(b);e.update(ok=False,classification='backup_branch_failed');return e
  e['backup_branch']=backup;rb=git('rebase',f'{REMOTE}/{BRANCH}',timeout=900);e['reconcile']=tail(rb)
  if rb.returncode:abort=git('rebase','--abort');e['abort']=tail(abort);e.update(ok=False,classification='rebase_conflict_preserved_backup');return e
  e.update(ok=True,classification='diverged_rebased_preserved_backup',local=rev('HEAD'));return e
 e.update(ok=False,classification='unhandled_topology');return e
def drain():
 cp=run(['python3',str(ROOT/'local/dore-local/coordination_worker.py')],3600);return {'ok':cp.returncode==0,**tail(cp,5000)}
def main():
 save(pid=os.getpid(),status='starting',interval_seconds=INTERVAL,remote=REMOTE,branch=BRANCH)
 while True:
  try:
   s=sync()
   if not s['ok']:save(status='sync_error',last_sync=s);time.sleep(INTERVAL);continue
   # Publish liveness immediately. A worker task can legitimately run for minutes/hours;
   # installers must not mistake that blocking drain for a dead daemon.
   save(status='healthy',phase='draining',last_sync=s)
   d=drain();save(status='healthy' if d['ok'] else 'worker_error',phase='sleeping',last_sync=s,last_drain=d)
  except Exception as e:save(status='daemon_error',error=type(e).__name__+': '+str(e),traceback=traceback.format_exc()[-4000:])
  time.sleep(INTERVAL)
if __name__=='__main__':main()
