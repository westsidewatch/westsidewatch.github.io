#!/usr/bin/env python3
"""Prepare a free local MLX-VLM training toolchain outside Doré canonical stores."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

CACHE_ROOT=Path.home()/"Library"/"Caches"/"Dore"/"theology-training"
VENV=CACHE_ROOT/"venv"
PY=VENV/"bin"/"python"
PIP=VENV/"bin"/"pip"


def run(argv:list[str],timeout:int)->dict:
    started=time.monotonic()
    p=subprocess.run(argv,text=True,capture_output=True,timeout=timeout)
    return {
        "returncode":p.returncode,
        "seconds":round(time.monotonic()-started,3),
        "stdout_tail":p.stdout[-3000:],
        "stderr_tail":p.stderr[-3000:],
    }


def version(package:str)->str|None:
    if not PY.is_file():
        return None
    p=subprocess.run([str(PY),"-c",f"import importlib.metadata as m; print(m.version('{package}'))"],text=True,capture_output=True)
    return p.stdout.strip() if p.returncode==0 else None


def main()->None:
    CACHE_ROOT.mkdir(parents=True,exist_ok=True)
    created=False
    steps=[]
    if not PY.is_file():
        created=True
        r=run([sys.executable,"-m","venv",str(VENV)],180)
        steps.append({"name":"venv","result":r})
        if r["returncode"]!=0:
            print(json.dumps({"ok":False,"status":"failed","stage":"venv","steps":steps},ensure_ascii=False,indent=2)); return
    # Install only into the disposable cache venv. No commercial API or cloud runtime is required.
    if not version("mlx-vlm") or not version("datasets"):
        r=run([str(PIP),"install","--disable-pip-version-check","mlx-vlm[train]"],1800)
        steps.append({"name":"install_mlx_vlm_train","result":r})
        if r["returncode"]!=0:
            print(json.dumps({"ok":False,"status":"failed","stage":"install","steps":steps},ensure_ascii=False,indent=2)); return
    probe=run([str(PY),"-c","import mlx, mlx_vlm, datasets; print('MLX_VLM_IMPORT_PASS')"],60)
    steps.append({"name":"import_probe","result":probe})
    ok=probe["returncode"]==0
    report={
        "ok":ok,
        "status":"completed" if ok else "failed",
        "protocol":"dore.theology-training-prepare/1",
        "cache_root":str(CACHE_ROOT),
        "venv_created":created,
        "mlx_vlm_version":version("mlx-vlm"),
        "mlx_version":version("mlx"),
        "datasets_version":version("datasets"),
        "canonical_ingest":False,
        "adapter_fused_into_base":False,
        "paid_api_required":False,
        "toolchain_open_source":True,
        "steps":steps,
    }
    print(json.dumps(report,ensure_ascii=False,indent=2))


if __name__=="__main__":
    main()
