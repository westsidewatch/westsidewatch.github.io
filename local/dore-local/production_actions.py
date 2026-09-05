#!/usr/bin/env python3
"""Bounded local production actions exposed to the DORÉ Native Messaging host."""
from __future__ import annotations
import json, os, subprocess
from pathlib import Path
from urllib import request

CAPABILITIES={"design.production.rollout"}

def _run(argv:list[str],cwd:Path|None=None,timeout:int=120,env:dict|None=None)->dict:
    child_env=os.environ.copy()
    if env: child_env.update(env)
    p=subprocess.run(argv,cwd=str(cwd) if cwd else None,text=True,capture_output=True,timeout=timeout,env=child_env)
    return {"argv":argv,"returncode":p.returncode,"stdout":p.stdout[-8000:],"stderr":p.stderr[-8000:]}

def _health()->dict:
    with request.urlopen("http://127.0.0.1:4310/api/health",timeout=5) as r:
        return json.loads(r.read().decode("utf-8"))

def design_production_rollout(args:dict|None=None)->dict:
    repo=Path(
        os.environ.get("DORE_WORKTREE")
        or os.environ.get("DORE_REPO_ROOT")
        or Path.home()/"westsidewatch.github.io"
    ).expanduser().resolve()
    if not (repo/".git").exists():
        return {"ok":False,"status":"failed","error":{"code":"worktree_missing","message":str(repo)}}
    fetch=_run(["git","fetch","origin","main"],repo)
    if fetch["returncode"]: return {"ok":False,"status":"failed","step":"fetch","result":fetch}
    ff=_run(["git","merge","--ff-only","origin/main"],repo)
    if ff["returncode"]: return {"ok":False,"status":"failed","step":"fast_forward","result":ff}
    install=_run(
        ["bash",str(repo/"dore-design"/"install-macos.sh")],
        repo,
        env={"DORE_SKIP_CONTROL_PLANE_REFRESH":"1"},
    )
    if install["returncode"]: return {"ok":False,"status":"failed","step":"install","result":install}
    health=_health()
    specimen={}
    try:
        with request.urlopen("http://127.0.0.1:4310/api/design2/specimen",timeout=5) as r:
            specimen=json.loads(r.read().decode("utf-8"))
    except Exception as exc:
        specimen={"ok":False,"error":str(exc)}
    ok=bool(health.get("ok") and health.get("resident_entrypoint")=="app_design2.py" and health.get("immutable_publication") is True and specimen.get("ok"))
    return {"ok":ok,"status":"completed" if ok else "failed","capability":"design.production.rollout","repo":str(repo),"head":_run(["git","rev-parse","HEAD"],repo)["stdout"].strip(),"health":health,"specimen":specimen,"install_tail":install["stdout"][-2000:]}

def execute(capability:str,args:dict|None=None)->dict:
    if capability=="design.production.rollout": return design_production_rollout(args)
    return {"ok":False,"status":"failed","error":{"code":"unsupported_production_action","message":capability}}
