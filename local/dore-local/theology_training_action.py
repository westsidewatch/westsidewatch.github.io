#!/usr/bin/env python3
"""Bounded A2A actions for Doré theology-alignment training."""
from __future__ import annotations
import json, os, subprocess, sys
from pathlib import Path
CAPABILITIES={"theology.training.readiness","theology.training.prepare","theology.training.stage32","theology.training.prefetch_model","theology.training.micro32","theology.training.eval32","theology.training.stage64","theology.training.micro64","theology.training.eval64","theology.training.recovery64","theology.shadow.acceptance64"}
SCRIPTS={
"theology.training.readiness":("theology-training-readiness.py",90),
"theology.training.prepare":("theology-training-prepare.py",2100),
"theology.training.stage32":("theology-training-stage32.py",60),
"theology.training.prefetch_model":("theology-training-prefetch-model.py",3700),
"theology.training.micro32":("theology-training-micro32.py",7200),
"theology.training.eval32":("theology-training-eval32.py",3300),
"theology.training.stage64":("theology-training-stage64.py",60),
"theology.training.micro64":("theology-training-micro64.py",7200),
"theology.training.eval64":("theology-training-eval64-candidate.py",3300),
"theology.training.recovery64":("theology-training-recovery64.py",3900),
"theology.shadow.acceptance64":("theology-shadow64-candidate.py",3900),
}
def _repo()->Path:
    return Path(os.environ.get("DORE_REPO_ROOT") or os.environ.get("DORE_WORKTREE") or Path.home()/"westsidewatch.github.io").expanduser().resolve()
def execute(capability:str,args=None):
    if capability not in CAPABILITIES: return {"ok":False,"status":"failed","error":{"code":"unsupported_action","message":capability}}
    repo=_repo(); name,timeout=SCRIPTS[capability]; script=repo/"local"/"dore-local"/name
    if not script.is_file(): return {"ok":False,"status":"failed","error":{"code":"training_script_missing","message":str(script)}}
    try: proc=subprocess.run([sys.executable,str(script)],cwd=str(repo),text=True,capture_output=True,timeout=timeout,env=os.environ.copy())
    except Exception as exc: return {"ok":False,"status":"failed","error":{"code":"training_action_exception","message":str(exc)}}
    if proc.returncode!=0: return {"ok":False,"status":"failed","returncode":proc.returncode,"stderr_tail":proc.stderr[-3000:],"stdout_tail":proc.stdout[-3000:]}
    try: report=json.loads(proc.stdout)
    except Exception as exc: return {"ok":False,"status":"failed","error":{"code":"invalid_training_json","message":str(exc)},"stdout_tail":proc.stdout[-3000:]}
    return {"ok":bool(report.get("ok")),"status":"completed" if report.get("ok") else "failed","capability":capability,"report":report}
