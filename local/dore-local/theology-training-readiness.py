#!/usr/bin/env python3
"""Read-only local readiness probe for Doré theology alignment training."""
from __future__ import annotations

import importlib.util
import json
import os
import platform
import shutil
import subprocess
import sys


def command_output(cmd: list[str]) -> str | None:
    try:
        return subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True, timeout=8).strip()
    except Exception:
        return None


def main() -> None:
    runtime_model = os.environ.get("DORE_LOCAL_MODEL", "gemma4:e4b")
    training_model = os.environ.get("DORE_THEOLOGY_MLX_MODEL")
    mlx_spec = importlib.util.find_spec("mlx_lm")
    mlx_version = None
    if mlx_spec is not None:
        mlx_version = command_output([sys.executable, "-c", "import importlib.metadata as m; print(m.version('mlx-lm'))"])

    ollama = shutil.which("ollama")
    ollama_models = command_output([ollama, "list"]) if ollama else None
    training_model_path = None
    training_model_local = False
    if training_model:
        candidate = os.path.expanduser(training_model)
        if os.path.exists(candidate):
            training_model_path = os.path.realpath(candidate)
            training_model_local = True

    report = {
        "ok": True,
        "protocol": "dore.theology-training-readiness/2",
        "machine": platform.machine(),
        "macos": platform.mac_ver()[0],
        "runtime_model": runtime_model,
        "runtime_model_source": "DORE_LOCAL_MODEL" if os.environ.get("DORE_LOCAL_MODEL") else "bootstrap-default",
        "runtime_model_visible_in_ollama_list": bool(ollama_models and runtime_model in ollama_models),
        "training_model": training_model,
        "training_model_source": "DORE_THEOLOGY_MLX_MODEL" if training_model else None,
        "training_model_local_path": training_model_path,
        "training_model_local": training_model_local,
        "training_model_configured": bool(training_model),
        "mlx_lm_installed": mlx_spec is not None,
        "mlx_lm_version": mlx_version,
        "ollama_installed": bool(ollama),
        "paid_api_required": False,
        "canonical_ingest": False,
        "network_action_performed": False,
    }
    report["training_ready"] = bool(
        report["machine"] == "arm64"
        and report["mlx_lm_installed"]
        and report["training_model_configured"]
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
