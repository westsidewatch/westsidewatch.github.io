#!/usr/bin/env python3
"""Bounded A2A actions for Doré theology-alignment training readiness.

This module exposes only fixed local scripts. It does not accept shell commands, does not
perform canonical ingest, and does not install packages or download models.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

CAPABILITIES={"theology.training.readiness"}


def _repo()->Path:
    return Path(
        os.environ.get("DORE_REPO_ROOT")
        or os.environ.get("DORE_WORKTREE")
        or Path.home()/"westsidewatch.github.io"
    ).expanduser().resolve()


def execute(capability:str,args=None):
    if capability not in CAPABILITIES:
        return {"ok":False,"status":"failed","error":{"code":"unsupported_action","message":capability}}
    repo=_repo()
    script=repo/"local"/"dore-local"/"theology-training-readiness.py"
    if not script.is_file():
        return {"ok":False,"status":"failed","error":{"code":"readiness_script_missing","message":str(script)}}
    try:
        proc=subprocess.run(
            [sys.executable,str(script)],
            cwd=str(repo),
            text=True,
            capture_output=True,
            timeout=60,
            env=os.environ.copy(),
        )
    except Exception as exc:
        return {"ok":False,"status":"failed","error":{"code":"readiness_exception","message":str(exc)}}
    if proc.returncode!=0:
        return {
            "ok":False,
            "status":"failed",
            "returncode":proc.returncode,
            "stderr_tail":proc.stderr[-2000:],
        }
    try:
        report=json.loads(proc.stdout)
    except Exception as exc:
        return {
            "ok":False,
            "status":"failed",
            "error":{"code":"invalid_readiness_json","message":str(exc)},
            "stdout_tail":proc.stdout[-2000:],
        }
    return {
        "ok":bool(report.get("ok")),
        "status":"completed" if report.get("ok") else "failed",
        "capability":capability,
        "readiness":report,
    }
