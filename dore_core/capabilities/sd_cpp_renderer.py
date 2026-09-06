from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


def load_sd_cpp_config(path: str | Path) -> dict[str, Any] | None:
    p = Path(path).expanduser()
    if not p.is_file():
        return None
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None
    if data.get("renderer") != "stable-diffusion.cpp":
        return None
    return data


def health(path: str | Path) -> tuple[bool, dict[str, Any]]:
    cfg = load_sd_cpp_config(path)
    if not cfg:
        return False, {"config": False, "detail": "sd-cpp-config-missing"}
    binary = Path(str(cfg.get("binary", ""))).expanduser()
    model = Path(str(cfg.get("model", ""))).expanduser()
    ok = binary.is_file() and binary.stat().st_mode & 0o111 != 0 and model.is_file() and model.stat().st_size > 100_000_000
    return ok, {
        "config": True,
        "detail": "ready" if ok else "sd-cpp-assets-missing",
        "renderer": "stable-diffusion.cpp",
        "binary": str(binary),
        "model": str(model),
        "model_bytes": model.stat().st_size if model.is_file() else 0,
    }


def generate(path: str | Path, *, prompt: str, seed: int, output_dir: str | Path) -> dict[str, Any]:
    cfg = load_sd_cpp_config(path)
    if not cfg:
        raise RuntimeError("sd_cpp_config_missing")
    binary = Path(str(cfg["binary"])).expanduser()
    model = Path(str(cfg["model"])).expanduser()
    if not binary.is_file() or not model.is_file():
        raise RuntimeError("sd_cpp_renderer_not_ready")
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    key = hashlib.sha256(f"{seed}\n{prompt}".encode("utf-8")).hexdigest()[:20]
    out = out_dir / f"sdcpp-{key}.png"
    argv = [
        str(binary), "-m", str(model), "-p", prompt,
        "-s", str(int(seed)), "--steps", str(int(cfg.get("steps", 8))),
        "-W", str(int(cfg.get("width", 512))), "-H", str(int(cfg.get("height", 512))),
        "-o", str(out),
    ]
    negative = str(cfg.get("negative_prompt", "")).strip()
    if negative:
        argv.extend(["-n", negative])
    proc = subprocess.run(argv, text=True, capture_output=True, timeout=int(cfg.get("timeout_seconds", 1200)))
    if proc.returncode != 0 or not out.is_file() or out.stat().st_size < 1024:
        raise RuntimeError("sd_cpp_generation_failed:" + (proc.stderr or proc.stdout)[-1200:])
    raw = out.read_bytes()
    sha = hashlib.sha256(raw).hexdigest()
    return {
        "id": f"sha256:{sha}",
        "sha256": sha,
        "bytes": len(raw),
        "mime_type": "image/png",
        "uri": str(out),
        "renderer": "stable-diffusion.cpp",
        "model": model.name,
        "seed": int(seed),
    }
