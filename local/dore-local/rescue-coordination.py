#!/usr/bin/env python3
"""One-shot non-destructive rescue for Doré Local coordination on macOS.

Designed for the exact failure where local main and origin/main diverged and the
resident coordination daemon was not yet installed. It preserves local commits
on a timestamped backup branch before rebasing. It refuses to touch a dirty
working tree because silent stashing/conflict resolution would risk user work.
"""
from __future__ import annotations
import json, os, subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(os.environ.get('DORE_REPO_ROOT',Path.home()/'westsidewatch.github.io')).expanduser()
REMOTE=os.environ.get('DORE_COORDINATION_REMOTE','origin')
BRANCH=os.environ.get('DORE_COORDINATION_BRANCH','main')
SKIP_INSTALL=os.environ.get('DORE_RESCUE_SKIP_INSTALL')=='1'

def run(*argv,timeout=900):
 return subprocess.run(list(argv),cwd=ROOT,text=True,capture_output=True,timeout=timeout)
def die(code,**evidence):
 print(json.dumps({'ok':False,'code':code,**evidence},ensure_ascii=False));raise SystemExit(2)
def rev(name):
 cp=run('git','rev-parse',name,timeout=60)
 return cp.stdout.strip() if cp.returncode==0 else None

def main():
 if not (ROOT/'.git').is_dir(): die('repo_not_found',root=str(ROOT))
 st=run('git','status','--porcelain',timeout=60)
 if st.returncode: die('git_status_failed',stderr=st.stderr[-2000:])
 if st.stdout.strip(): die('dirty_worktree_requires_dore_review',status=st.stdout[-5000:])
 f=run('git','fetch','--prune',REMOTE,BRANCH,timeout=180)
 if f.returncode: die('fetch_failed',stderr=f.stderr[-3000:])
 local,remote=rev('HEAD'),rev(f'{REMOTE}/{BRANCH}')
 if not local or not remote: die('rev_parse_failed',local=local,remote=remote)
 topology=run('git','rev-list','--left-right','--count',f'HEAD...{REMOTE}/{BRANCH}',timeout=60)
 if topology.returncode: die('topology_failed',stderr=topology.stderr[-2000:])
 ahead,behind=map(int,topology.stdout.split())
 backup=None
 if ahead==0 and behind>0:
  m=run('git','merge','--ff-only',f'{REMOTE}/{BRANCH}',timeout=180)
  if m.returncode: die('fast_forward_failed',stderr=m.stderr[-3000:])
 elif ahead>0 and behind>0:
  backup=f'dore/rescue-{datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")}'
  b=run('git','branch',backup,'HEAD',timeout=60)
  if b.returncode: die('backup_branch_failed',stderr=b.stderr[-3000:])
  r=run('git','rebase',f'{REMOTE}/{BRANCH}',timeout=900)
  if r.returncode:
   run('git','rebase','--abort',timeout=120)
   die('rebase_conflict_local_preserved',backup_branch=backup,stderr=r.stderr[-5000:])
 installer_stdout='SKIPPED_FOR_TEST'
 if not SKIP_INSTALL:
  installer=ROOT/'local/dore-local/install-coordination-daemon.sh'
  if not installer.is_file(): die('installer_missing_after_reconcile',head=rev('HEAD'))
  ins=run('bash',str(installer),timeout=180)
  if ins.returncode: die('daemon_install_failed',stdout=ins.stdout[-5000:],stderr=ins.stderr[-5000:],backup_branch=backup)
  installer_stdout=ins.stdout[-3000:]
 print(json.dumps({'ok':True,'code':'DORE_COORDINATION_RESCUE_PASS','head':rev('HEAD'),'remote':rev(f'{REMOTE}/{BRANCH}'),'ahead_before':ahead,'behind_before':behind,'backup_branch':backup,'installer_stdout':installer_stdout},ensure_ascii=False))

if __name__=='__main__': main()
