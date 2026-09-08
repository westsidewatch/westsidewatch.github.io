#!/usr/bin/env python3
"""Read-only readiness probe for Doré's isolated MLX-VLM theology adapter POC."""
from __future__ import annotations

import json
import os
import platform
import subprocess
from pathlib import Path

CACHE_ROOT=Path.home()/"Library"/"Caches"/"Dore"/"theology-training"
VENV=CACHE_ROOT/"venv"
PY=VENV/"bin"/"python"
DEFAULT_TRAINING_MODEL="mlx-community/gemma-4-e4b-it-4bit"


def command_output(cmd:list[str],timeout:int=12)->str|None:
    try:
        return subprocess.check_output(cmd,stderr=subprocess.STDOUT,text=True,timeout=timeout).strip()
    except Exception:
        return None


def package_version(python:Path,package:str)->str|None:
    if not python.is_file():
        return None
    return command_output([str(python),"-c",f"import importlib.metadata as m; print(m.version('{package}'))"])


def main()->None:
    runtime_model=os.environ.get("DORE_LOCAL_MODEL","gemma4:e4b")
    training_model=os.environ.get("DORE_THEOLOGY_MLX_MODEL",DEFAULT_TRAINING_MODEL)
    mlx_vlm_version=package_version(PY,"mlx-vlm")
    datasets_version=package_version(PY,"datasets")
    model_cache=CACHE_ROOT/"models"
    adapter_cache=CACHE_ROOT/"adapters"
    report={
        "ok":True,
        "protocol":"dore.theology-training-readiness/3",
        "machine":platform.machine(),
        "macos":platform.mac_ver()[0],
        "runtime_model":runtime_model,
        "training_model":training_model,
        "training_backend":"mlx-vlm",
        "venv":str(VENV),
        "venv_python_present":PY.is_file(),
        "mlx_vlm_installed":bool(mlx_vlm_version),
        "mlx_vlm_version":mlx_vlm_version,
        "datasets_version":datasets_version,
        "model_cache":str(model_cache),
        "adapter_cache":str(adapter_cache),
        "canonical_ingest":False,
        "paid_api_required":False,
        "network_action_performed":False,
    }
    report["training_ready"]=bool(
        report["machine"]=="arm64"
        and report["venv_python_present"]
        and report["mlx_vlm_installed"]
        and report["datasets_version"]
    )
    print(json.dumps(report,ensure_ascii=False,indent=2))


if __name__=="__main__":
    main()
