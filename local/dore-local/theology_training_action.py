#!/usr/bin/env python3
"""Bounded A2A actions for Doré theology-alignment training.

Only fixed repository scripts are callable. No arbitrary command or path is accepted.
Training artifacts live under the user cache or /tmp; nothing is canonically ingested.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

CAPABILITIES={"theology.training.readiness","theology.training.prepare","theology.training.stage32","theology.training.micro32"}
SCRIPTS={
    "theology.training.readiness":("theology-training-readiness.py",90),
    "theology.training.prepare":("theology-training-prepare.py",2100),
    "theology.training.stage32":("theology-training-stage32.py",60),
    "theology.training.micro32":("theology-training-micro32.py",7200),
}


def _repo()->Path:
    return Path(os.environ.get("DORE_REPO_ROOT") or os.environ.get("DORE_WORKTREE") or Path.home()/"westsidewatch.github.io").expanduser().resolve()


def execute(capability:str,args=None):
    if capability not in CAPABILITIES:
        return {"ok":False,"status":"failed","error":{"code":"unsupported_action","message":capability}}
    repo=_repo()
    name,timeout=SCRIPTS[capability]
    script=repo/"local"/"dore-local"/name
    if not script.is_file():
        return {"ok":False,"status":"failed","error":{"code":"training_script_missing","message":str(script)}}
    try:
        proc=subprocess.run([sys.executable,str(script)],cwd=str(repo),text=True,capture_output=True,timeout=timeout,env=os.environ.copy())
    except Exception as exc:
        return {"ok":False,"status":"failed","error":{"code":"training_action_exception","message":str(exc)}}
    if proc.returncode!=0:
        return {"ok":False,"status":"failed","returncode":proc.returncode,"stderr_tail":proc.stderr[-3000:],"stdout_tail":proc.stdout[-3000:]}
    try:
        report=json.loads(proc.stdout)
    except Exception as exc:
        return {"ok":False,"status":"failed","error":{"code":"invalid_training_json","message":str(exc)},"stdout_tail":proc.stdout[-3000:]}
    return {
        "ok":bool(report.get("ok")),
        "status":"completed" if report.get("ok") else "failed",
        "capability":capability,
        "report":report,
    }
