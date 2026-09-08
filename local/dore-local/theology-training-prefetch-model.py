#!/usr/bin/env python3
"""Prefetch exactly the approved MLX-VLM theology training model into isolated cache.

Network is allowed only in this preparation gate. The runtime/training action remains offline.
No caller-supplied repo id, revision, shell command, destination, or token is accepted.
"""
from __future__ import annotations

import hashlib
import json
import os
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

    os.environ["HF_HOME"] = str(HF_HOME)
    os.environ.pop("HF_HUB_OFFLINE", None)
    os.environ.pop("TRANSFORMERS_OFFLINE", None)
    HF_HOME.mkdir(parents=True, exist_ok=True)

    from huggingface_hub import snapshot_download
    try:
        path = Path(snapshot_download(repo_id=MODEL_ID, revision=REVISION, cache_dir=str(HF_HOME / "hub"))).resolve()
        # Immediately prove the same revision is resolvable with no network.
        offline = Path(snapshot_download(repo_id=MODEL_ID, revision=REVISION, cache_dir=str(HF_HOME / "hub"), local_files_only=True)).resolve()
    except Exception as exc:
        print(json.dumps({"ok":False,"status":"failed","error":{"code":"model_prefetch_failed","message":str(exc)}}, ensure_ascii=False, indent=2))
        raise SystemExit(2)

    nfiles, nbytes, digest = tree_digest(offline)
    report = {
        "ok": True,
        "status": "completed",
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
    raise SystemExit(0 if report["offline_resolve_verified"] else 2)


if __name__ == "__main__":
    main()
