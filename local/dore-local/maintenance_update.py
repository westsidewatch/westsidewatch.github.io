#!/usr/bin/env python3
"""Guarded self-update for the local DORÉ resident.

This is deliberately not a general shell bridge. It updates only this repository,
only its main branch, only from origin/main, and only by fast-forward.
"""
from __future__ import annotations
import json, os, subprocess, urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(os.environ.get('DORE_REPO_ROOT') or Path(__file__).resolve().parents[2]).expanduser().resolve()
EXPECTED_REPO='westsidewatch.github.io'
EXPECTED_BRANCH='main'
HEALTH=os.environ.get('DORE_DESIGN_HEALTH','http://127.0.0.1:4310/api/health')

def run(argv,timeout=180):
 cp=subprocess.run(argv,cwd=ROOT,text=True,capture_output=True,timeout=timeout)
 if cp.returncode:
  raise RuntimeError(f"command_failed:{' '.join(argv)}:{(cp.stderr or cp.stdout)[-2000:]}")
 return (cp.stdout or '').strip()

def health():
 try:
  with urllib.request.urlopen(HEALTH,timeout=8) as r:
   body=r.read(4096).decode('utf-8','replace')
   return {'ok':200 <= r.status < 300,'status':r.status,'body':body[:1000]}
 except Exception as e:return {'ok':False,'error':type(e).__name__+': '+str(e)}

def restart_design():
 # Prefer launchd resident services. Never construct a shell command.
 uid=str(os.getuid()); labels=[]
 try:
  out=run(['launchctl','list'],30)
  labels=[line.split()[-1] for line in out.splitlines() if 'dore' in line.lower() and ('design' in line.lower() or 'resident' in line.lower())]
 except Exception:pass
 results=[]
 for label in labels:
  cp=subprocess.run(['launchctl','kickstart','-k',f'gui/{uid}/{label}'],text=True,capture_output=True,timeout=30)
  results.append({'label':label,'returncode':cp.returncode,'stderr':(cp.stderr or '')[-1000:]})
 return results

def main():
 before=run(['git','rev-parse','HEAD'])
 branch=run(['git','branch','--show-current'])
 if branch!=EXPECTED_BRANCH:raise RuntimeError('maintenance_wrong_branch:'+branch)
 top=Path(run(['git','rev-parse','--show-toplevel'])).resolve()
 if top!=ROOT or ROOT.name!=EXPECTED_REPO:raise RuntimeError('maintenance_wrong_repository:'+str(top))
 dirty=run(['git','status','--porcelain'])
 if dirty:raise RuntimeError('maintenance_dirty_worktree')
 remote=run(['git','remote','get-url','origin'])
 if 'westsidewatch/westsidewatch.github.io' not in remote:raise RuntimeError('maintenance_wrong_origin:'+remote)
 run(['git','fetch','--prune','origin','main'],180)
 # Refuse divergence or local-only commits. HEAD must be an ancestor of origin/main.
 anc=subprocess.run(['git','merge-base','--is-ancestor','HEAD','origin/main'],cwd=ROOT).returncode
 if anc!=0:raise RuntimeError('maintenance_non_fast_forward_refused')
 target=run(['git','rev-parse','origin/main'])
 run(['git','merge','--ff-only','origin/main'],180)
 after=run(['git','rev-parse','HEAD'])
 if after!=target:raise RuntimeError('maintenance_target_mismatch')
 # Lightweight deterministic verification that does not install dependencies.
 checks=[]
 for script in ('coordination_worker.py','autonomous_driver.py'):
  p=ROOT/'local/dore-local'/script
  cp=subprocess.run(['python3','-m','py_compile',str(p)],cwd=ROOT,text=True,capture_output=True,timeout=30)
  checks.append({'script':script,'ok':cp.returncode==0,'stderr':(cp.stderr or '')[-1000:]})
 if not all(x['ok'] for x in checks):raise RuntimeError('maintenance_verification_failed:'+json.dumps(checks))
 restarts=restart_design()
 post=health()
 result={'ok':post.get('ok',False),'operation':'maintenance.update','repository':'westsidewatch/westsidewatch.github.io','branch':'main','before_sha':before,'target_sha':target,'after_sha':after,'updated':before!=after,'verification':checks,'restart':restarts,'health':post,'completed_at':datetime.now(timezone.utc).isoformat()}
 print(json.dumps(result,ensure_ascii=False))
 return 0 if result['ok'] else 2
if __name__=='__main__':raise SystemExit(main())
