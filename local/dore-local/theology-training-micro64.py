#!/usr/bin/env python3
"""Fixed real MLX-VLM theology micro64 recovery execution. No caller-controlled args."""
from __future__ import annotations
import json, os, subprocess, sys
from pathlib import Path
ROOT=Path.home()/"Library"/"Caches"/"Dore"/"theology-training"/"quarantine-v1"; HERE=Path(__file__).resolve().parent; POC=HERE/"theology-training-poc.py"
def main():
    if len(sys.argv)!=1: raise SystemExit("no caller arguments accepted")
    if not (ROOT/"train-64.jsonl").is_file(): print(json.dumps({"ok":False,"status":"failed","error":"quarantine64_not_staged"})); raise SystemExit(2)
    env=os.environ.copy(); env["DORE_THEOLOGY_MLX_LR"]="2e-6"
    cmd=[sys.executable,str(POC),"--quarantine",str(ROOT),"--size","64","--iters","24","--execute"]
    proc=subprocess.run(cmd,text=True,capture_output=True,timeout=7200,env=env)
    try: report=json.loads(proc.stdout)
    except Exception: print(json.dumps({"ok":False,"status":"failed","returncode":proc.returncode,"stderr_tail":proc.stderr[-3000:],"stdout_tail":proc.stdout[-3000:]})); raise SystemExit(2)
    ok=proc.returncode==0 and bool(report.get("ok")) and report.get("training_size")==64 and report.get("learning_rate")=="2e-6" and report.get("adapter_present") and report.get("adapter_bytes",0)>0
    print(json.dumps({"ok":ok,"status":"completed" if ok else "failed","protocol":"dore.theology-training-micro64/2","training_size":64,"quarantine":str(ROOT),"canonical_ingest":False,"paid_api_required":False,"arbitrary_shell_allowed":False,"training":report},ensure_ascii=False,indent=2)); raise SystemExit(0 if ok else 2)
if __name__=="__main__": main()
