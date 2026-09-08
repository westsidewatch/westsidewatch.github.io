#!/usr/bin/env python3
"""Prefetch exactly the approved MLX-VLM theology training model into isolated cache.

Network is allowed only in this preparation gate. The runtime/training action remains offline.
No caller-supplied repo id, revision, shell command, destination, or token is accepted.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
from pathlib import Path

CACHE_ROOT = Path.home() / "Library" / "Caches" / "Dore" / "theology-training"
VENV = CACHE_ROOT / "venv"
MODEL_ID = "mlx-community/gemma-4-e4b-it-4bit"
REVISION = "main"
HF_HOME = CACHE_ROOT / "hf"


def tree_digest(root: Path) -> tuple[int, int, str]:
    files = sorted(p for p in root.rglob("*") if p.is_file())
    h = hashlib.sha256()
    total = 0
    for p in files:
        rel = p.relative_to(root).as_posix().encode()
        size = p.stat().st_size
        total += size
        h.update(len(rel).to_bytes(4, "big")); h.update(rel)
        h.update(size.to_bytes(8, "big"))
    return len(files), total, h.hexdigest()


def main() -> None:
    py = VENV / "bin" / "python"
    if not py.is_file():
        print(json.dumps({"ok":False,"status":"failed","error":{"code":"training_venv_missing","message":str(py)}}))
        raise SystemExit(2)

    HF_HOME.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env["HF_HOME"] = str(HF_HOME)
    env.pop("HF_HUB_OFFLINE", None)
    env.pop("TRANSFORMERS_OFFLINE", None)

    code = r'''
import json
from huggingface_hub import snapshot_download
model = "mlx-community/gemma-4-e4b-it-4bit"
revision = "main"
cache_dir = __import__("os").path.expanduser("~/Library/Caches/Dore/theology-training/hf/hub")
path = snapshot_download(repo_id=model, revision=revision, cache_dir=cache_dir)
offline = snapshot_download(repo_id=model, revision=revision, cache_dir=cache_dir, local_files_only=True)
print(json.dumps({"path": path, "offline": offline}))
'''
    try:
        proc = subprocess.run([str(py), "-c", code], text=True, capture_output=True, timeout=3600, env=env)
    except Exception as exc:
        print(json.dumps({"ok":False,"status":"failed","error":{"code":"model_prefetch_exception","message":str(exc)}}, ensure_ascii=False, indent=2))
        raise SystemExit(2)
    if proc.returncode != 0:
        print(json.dumps({"ok":False,"status":"failed","returncode":proc.returncode,"stderr_tail":proc.stderr[-5000:],"stdout_tail":proc.stdout[-3000:]}, ensure_ascii=False, indent=2))
        raise SystemExit(2)

    try:
        payload = json.loads(proc.stdout)
        path = Path(payload["path"]).resolve()
        offline = Path(payload["offline"]).resolve()
    except Exception as exc:
        print(json.dumps({"ok":False,"status":"failed","error":{"code":"invalid_prefetch_result","message":str(exc)},"stdout_tail":proc.stdout[-3000:]}, ensure_ascii=False, indent=2))
        raise SystemExit(2)

    nfiles, nbytes, digest = tree_digest(offline)
    report = {
        "ok": path == offline and offline.is_dir(),
        "status": "completed" if path == offline and offline.is_dir() else "failed",
        "protocol": "dore.theology-training-prefetch-model/1",
        "model": MODEL_ID,
        "revision": REVISION,
        "snapshot_path": str(offline),
        "files": nfiles,
        "bytes": nbytes,
        "tree_digest": digest,
        "offline_resolve_verified": path == offline,
        "network_allowed_only_for_prefetch": True,
        "canonical_ingest": False,
        "paid_api_required": False,
        "adapter_fused_into_base": False,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(0 if report["ok"] else 2)


if __name__ == "__main__":
    main()
