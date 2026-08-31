#!/usr/bin/env python3
from __future__ import annotations
import json,os,subprocess,shutil
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(os.environ.get('DORE_REPO_ROOT',Path.home()/'westsidewatch.github.io')).expanduser();HOME_DORE=Path(os.environ.get('DORE_LOCAL_HOME',Path.home()/'.dore')).expanduser();REMOTE='origin';BRANCH='main'
def run(*a,t=900):return subprocess.run(list(a),cwd=ROOT,text=True,capture_output=True,timeout=t)
def die(c,**e):print(json.dumps({'ok':False,'code':c,**e},ensure_ascii=False));raise SystemExit(2)
def rev(x):
 p=run('git','rev-parse',x,t=60);return p.stdout.strip() if p.returncode==0 else None
def quarantine(path,label):
 if not path.exists():return None
 qr=HOME_DORE/'rescue-untracked';qr.mkdir(parents=True,exist_ok=True);dst=qr/f'{label}-{datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")}'
 shutil.move(str(path),str(dst));return str(dst)
def main():
 if not (ROOT/'.git').is_dir():die('repo_not_found',root=str(ROOT))
 s=run('git','status','--porcelain',t=60); lines=[x.strip() for x in s.stdout.splitlines() if x.strip()];qs=[]
 known={'?? .framesmith/':(ROOT/'.framesmith','framesmith'),'?? .framesmith':(ROOT/'.framesmith','framesmith'),'?? dore-design/prep/':(ROOT/'dore-design/prep','dore-design-prep'),'?? dore-design/prep':(ROOT/'dore-design/prep','dore-design-prep')}
 unknown=[x for x in lines if x not in known]
 if unknown:die('dirty_worktree_requires_review',status='\n'.join(unknown),known_generated=[x for x in lines if x in known])
 for x in lines:
  if x in known:
   p=quarantine(*known[x])
   if p:qs.append(p)
 s=run('git','status','--porcelain',t=60)
 if s.stdout.strip():die('dirty_worktree_after_quarantine',status=s.stdout[-5000:],quarantined=qs)
 f=run('git','fetch','--prune',REMOTE,BRANCH,t=180)
 if f.returncode:die('fetch_failed',stderr=f.stderr[-3000:],quarantined=qs)
 topo=run('git','rev-list','--left-right','--count',f'HEAD...{REMOTE}/{BRANCH}',t=60)
 if topo.returncode:die('topology_failed',stderr=topo.stderr[-3000:],quarantined=qs)
 ahead,behind=map(int,topo.stdout.split());backup=None
 if ahead==0 and behind>0:
  m=run('git','merge','--ff-only',f'{REMOTE}/{BRANCH}',t=180)
  if m.returncode:die('fast_forward_failed',stderr=m.stderr[-3000:],quarantined=qs)
 elif ahead>0 and behind>0:
  backup=f'dore/rescue-{datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")}';b=run('git','branch',backup,'HEAD',t=60)
  if b.returncode:die('backup_failed',stderr=b.stderr[-3000:],quarantined=qs)
  r=run('git','rebase',f'{REMOTE}/{BRANCH}',t=900)
  if r.returncode:run('git','rebase','--abort',t=120);die('rebase_conflict_local_preserved',backup_branch=backup,stderr=r.stderr[-5000:],quarantined=qs)
 ins=run('bash',str(ROOT/'local/dore-local/install-coordination-daemon.sh'),t=180)
 if ins.returncode:die('daemon_install_failed',stdout=ins.stdout[-5000:],stderr=ins.stderr[-5000:],backup_branch=backup,quarantined=qs)
 print(json.dumps({'ok':True,'code':'DORE_COORDINATION_RESCUE_PASS','head':rev('HEAD'),'backup_branch':backup,'quarantined':qs,'installer_stdout':ins.stdout[-3000:]},ensure_ascii=False))
if __name__=='__main__':main()
