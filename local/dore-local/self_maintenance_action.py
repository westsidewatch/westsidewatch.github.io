#!/usr/bin/env python3
"""Bounded Doré self-maintenance action; no arbitrary shell surface."""
from __future__ import annotations
import json, os, subprocess
from pathlib import Path

CAPABILITIES={"system.self-maintain"}

def _run(argv:list[str],cwd:Path,timeout:int=900)->dict:
    try:
        p=subprocess.run(argv,cwd=str(cwd),text=True,capture_output=True,timeout=timeout)
        return {"returncode":p.returncode,"stdout":p.stdout[-6000:],"stderr":p.stderr[-6000:]}
    except subprocess.TimeoutExpired as exc:
        return {"returncode":124,"stdout":str(exc.stdout or "")[-6000:],"stderr":str(exc.stderr or "")[-6000:]}

def _repo()->Path:
    return Path(os.environ.get("DORE_WORKTREE") or Path.home()/"westsidewatch.github.io").expanduser().resolve()

def execute(capability:str,args=None):
    if capability!="system.self-maintain":
        return {"ok":False,"status":"failed","error":{"code":"unsupported_maintenance_action","message":capability}}
    repo=_repo()
    if not (repo/".git").is_dir():
        return {"ok":False,"status":"failed","capability":capability,"error":{"code":"worktree_missing","message":str(repo)}}
    dirty=_run(["git","status","--porcelain"],repo,30)
    if dirty["returncode"] or dirty["stdout"].strip():
        return {"ok":False,"status":"failed","capability":capability,"error":{"code":"dirty_worktree","message":"self-maintenance requires a clean worktree"}}
    script=repo/"local"/"dore-local"/"bootstrap-self-maintenance.command"
    if not script.is_file():
        return {"ok":False,"status":"failed","capability":capability,"error":{"code":"maintenance_script_missing","message":str(script)}}
    run=_run(["bash",str(script)],repo,1800)
    evidence={}
    for line in reversed(run["stdout"].splitlines()):
        try:
            candidate=json.loads(line)
            if isinstance(candidate,dict) and candidate.get("manual_bootstrap_complete") is True:
                evidence=candidate;break
        except Exception:
            pass
    ok=bool(run["returncode"]==0 and evidence.get("ok") is True and evidence.get("native_host_refreshed") is True)
    return {"ok":ok,"status":"completed" if ok else "failed","capability":capability,"repo":str(repo),"evidence":evidence,"stdout_tail":run["stdout"][-3000:],"stderr_tail":run["stderr"][-3000:]}
