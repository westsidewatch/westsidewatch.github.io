#!/usr/bin/env python3
from __future__ import annotations
import importlib.util, json, os, subprocess, sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("eval64_base",HERE/"theology-training-eval64.py")
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
RECOVERY=m.CACHE_ROOT/"runs"/"n64-recovery"/"adapter"/"adapter.safetensors"
ORIGINAL=m.CACHE_ROOT/"runs"/"n64"/"adapter"/"adapter.safetensors"
CONFIG=m.CACHE_ROOT/"runs"/"n64"/"adapter"/"adapter_config.json"
SELECTED=RECOVERY if RECOVERY.is_file() else ORIGINAL
m.ADAPTER_FILE=SELECTED
m.ADAPTER_CONFIG=CONFIG
m.BUNDLE=m.CACHE_ROOT/"runs"/"n64-recovery"/"eval-candidate-bundle"
def candidate_run_mode(mode):
    env=os.environ.copy(); env["HF_HOME"]=str(m.HF_HOME); env["HF_HUB_CACHE"]=str(m.HF_HOME/"hub"); env["HF_HUB_OFFLINE"]="1"; env["TRANSFORMERS_OFFLINE"]="1"
    p=subprocess.run([str(m.PY),str(Path(__file__).resolve()),"--worker",mode],text=True,capture_output=True,timeout=1500,env=env)
    if p.returncode!=0: raise RuntimeError(f"{mode}_worker_failed:{p.returncode}:{p.stderr[-3000:]}")
    return json.loads(p.stdout)
m.run_mode=candidate_run_mode
if __name__=="__main__": m.main()
