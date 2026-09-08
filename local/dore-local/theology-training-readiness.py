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
    model = os.environ.get("DORE_LOCAL_MODEL", "gemma4:e4b")
    mlx_spec = importlib.util.find_spec("mlx_lm")
    mlx_version = None
    if mlx_spec is not None:
        mlx_version = command_output([sys.executable, "-c", "import importlib.metadata as m; print(m.version('mlx-lm'))"])

    ollama = shutil.which("ollama")
    ollama_models = command_output([ollama, "list"]) if ollama else None

    report = {
        "ok": True,
        "protocol": "dore.theology-training-readiness/1",
        "machine": platform.machine(),
        "macos": platform.mac_ver()[0],
        "configured_model": model,
        "configured_model_source": "DORE_LOCAL_MODEL" if os.environ.get("DORE_LOCAL_MODEL") else "bootstrap-default",
        "mlx_lm_installed": mlx_spec is not None,
        "mlx_lm_version": mlx_version,
        "ollama_installed": bool(ollama),
        "configured_model_visible_in_ollama_list": bool(ollama_models and model in ollama_models),
        "paid_api_required": False,
        "canonical_ingest": False,
        "network_action_performed": False,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
