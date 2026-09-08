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
BOOTSTRAP=CACHE_ROOT/"uv-bootstrap"
UV=BOOTSTRAP/"bin"/"uv"
UV_PY_DIR=CACHE_ROOT/"python"
MIN_PY=(3,11)
MIN_MLX_VLM=(0,5,0)


def run(argv:list[str],timeout:int,env:dict|None=None)->dict:
    started=time.monotonic()
    p=subprocess.run(argv,text=True,capture_output=True,timeout=timeout,env=env)
    return {"returncode":p.returncode,"seconds":round(time.monotonic()-started,3),"stdout_tail":p.stdout[-3000:],"stderr_tail":p.stderr[-3000:]}


def py_version(exe:Path)->tuple[int,int,int]|None:
    if not exe.is_file(): return None
    p=subprocess.run([str(exe),"-c","import sys; print('.'.join(map(str,sys.version_info[:3])))"],text=True,capture_output=True)
    if p.returncode: return None
    try: return tuple(int(x) for x in p.stdout.strip().split('.')[:3])
    except Exception: return None


def choose_existing_python()->Path|None:
    candidates=[]
    for raw in (
        "/opt/homebrew/bin/python3.13","/opt/homebrew/bin/python3.12","/opt/homebrew/bin/python3.11","/opt/homebrew/bin/python3",
        "/usr/local/bin/python3.13","/usr/local/bin/python3.12","/usr/local/bin/python3.11","/usr/local/bin/python3",
    ):
        candidates.append(Path(raw))
    for name in ("python3.13","python3.12","python3.11","python3"):
        found=shutil.which(name)
        if found: candidates.append(Path(found))
    seen=set()
    for exe in candidates:
        if str(exe) in seen: continue
        seen.add(str(exe))
        ver=py_version(exe)
        if ver and ver[:2]>=MIN_PY: return exe
    return None


def bootstrap_managed_python(steps:list[dict])->Path|None:
    """Use open-source uv + python-build-standalone in Doré's disposable cache only."""
    if not UV.is_file():
        if BOOTSTRAP.exists(): shutil.rmtree(BOOTSTRAP)
        r=run([sys.executable,"-m","venv",str(BOOTSTRAP)],180); steps.append({"name":"uv_bootstrap_venv","result":r})
        if r["returncode"]: return None
        bpip=BOOTSTRAP/"bin"/"pip"
        r=run([str(bpip),"install","--disable-pip-version-check","uv"],600); steps.append({"name":"install_uv","result":r})
        if r["returncode"]: return None
    env=os.environ.copy(); env["UV_PYTHON_INSTALL_DIR"]=str(UV_PY_DIR)
    r=run([str(UV),"python","install","3.12","--install-dir",str(UV_PY_DIR)],1200,env); steps.append({"name":"uv_python_install_312","result":r})
    if r["returncode"]: return None
    p=subprocess.run([str(UV),"python","find","3.12","--managed-python"],text=True,capture_output=True,env=env)
    if p.returncode: return None
    candidate=Path(p.stdout.strip())
    return candidate if py_version(candidate) and py_version(candidate)[:2]>=MIN_PY else None


def parse_version(raw:str|None)->tuple[int,...]:
    if not raw: return ()
    out=[]
    for part in raw.split('.'):
        digits=''.join(ch for ch in part if ch.isdigit())
        if not digits: break
        out.append(int(digits))
    return tuple(out)


def version(package:str)->str|None:
    if not PY.is_file(): return None
    p=subprocess.run([str(PY),"-c",f"import importlib.metadata as m; print(m.version('{package}'))"],text=True,capture_output=True)
    return p.stdout.strip() if p.returncode==0 else None


def main()->None:
    CACHE_ROOT.mkdir(parents=True,exist_ok=True)
    steps=[]
    base=choose_existing_python()
    managed=False
    if base is None:
        base=bootstrap_managed_python(steps); managed=True
    if base is None:
        print(json.dumps({"ok":False,"status":"failed","stage":"python","error":"modern_python_bootstrap_failed","canonical_ingest":False,"paid_api_required":False,"steps":steps},ensure_ascii=False,indent=2)); return
    base_ver=py_version(base)
    current_ver=py_version(PY)
    current_mlx=parse_version(version("mlx-vlm"))
    rebuild=not current_ver or current_ver[:2]<MIN_PY or current_mlx<MIN_MLX_VLM
    if rebuild and VENV.exists(): shutil.rmtree(VENV)
    if not PY.is_file():
        r=run([str(base),"-m","venv",str(VENV)],180); steps.append({"name":"training_venv","result":r})
        if r["returncode"]:
            print(json.dumps({"ok":False,"status":"failed","stage":"venv","base_python":str(base),"steps":steps},ensure_ascii=False,indent=2)); return
    if parse_version(version("mlx-vlm"))<MIN_MLX_VLM or not version("datasets"):
        r=run([str(PIP),"install","--disable-pip-version-check","mlx-vlm[train]>=0.5.0"],1800); steps.append({"name":"install_mlx_vlm_train","result":r})
        if r["returncode"]:
            print(json.dumps({"ok":False,"status":"failed","stage":"install","base_python":str(base),"steps":steps},ensure_ascii=False,indent=2)); return
    probe=run([str(PY),"-c","import mlx, mlx_vlm, datasets; print('MLX_VLM_IMPORT_PASS')"],90); steps.append({"name":"import_probe","result":probe})
    mlx_vlm_version=version("mlx-vlm")
    ok=probe["returncode"]==0 and parse_version(mlx_vlm_version)>=MIN_MLX_VLM
    report={
        "ok":ok,"status":"completed" if ok else "failed","protocol":"dore.theology-training-prepare/3",
        "base_python":str(base),"base_python_version":".".join(map(str,base_ver or ())),"managed_python":managed,"venv_python_version":".".join(map(str,py_version(PY) or ())),
        "cache_root":str(CACHE_ROOT),"venv_rebuilt":rebuild,"mlx_vlm_version":mlx_vlm_version,"mlx_version":version("mlx"),"datasets_version":version("datasets"),
        "canonical_ingest":False,"adapter_fused_into_base":False,"paid_api_required":False,"toolchain_open_source":True,"steps":steps,
    }
    print(json.dumps(report,ensure_ascii=False,indent=2))


if __name__=="__main__": main()
