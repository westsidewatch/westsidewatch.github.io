#!/usr/bin/env python3
"""Doré Theology Alignment micro-POC.

Purpose:
- train/evaluate a tiny LoRA adapter for abstract Christian theological alignment
- keep adversarial fixtures quarantined outside Doré Core/Knowledge/Memory
- never ingest training/eval records into canonical Doré stores
- stop training as soon as minimum sufficient learning is reached

This script is a local orchestration wrapper around mlx-lm. It does not download
models or data automatically and does not call paid/cloud APIs.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

DEFAULT_MODEL = os.environ.get("DORE_LOCAL_MODEL", "gemma4:e4b")
SIZES = (32, 64, 128, 256)


def die(message: str) -> None:
    print(json.dumps({"ok": False, "error": message}, ensure_ascii=False))
    raise SystemExit(2)


def require_quarantine(path: Path) -> None:
    resolved = path.expanduser().resolve()
    home = Path.home().resolve()
    forbidden = [
        (home / ".dore").resolve(),
        (home / "Library/Application Support/Dore").resolve(),
    ]
    for root in forbidden:
        try:
            resolved.relative_to(root)
            die("quarantine path must not be inside Doré runtime/core data")
        except ValueError:
            pass


def count_jsonl(path: Path) -> int:
    with path.open("r", encoding="utf-8") as fh:
        return sum(1 for line in fh if line.strip())


def verify_dataset(root: Path, size: int) -> dict:
    train = root / f"train-{size}.jsonl"
    valid = root / "valid.jsonl"
    test = root / "test.jsonl"
    for p in (train, valid, test):
        if not p.is_file():
            die(f"missing quarantined split: {p}")
    train_n = count_jsonl(train)
    if train_n != size:
        die(f"expected {size} training rows, found {train_n}")
    return {"train": str(train), "valid": str(valid), "test": str(test), "train_rows": train_n}


def mlx_available() -> bool:
    return shutil.which("mlx_lm.lora") is not None or shutil.which("mlx_lm") is not None


def build_command(model: str, train_file: str, valid_file: str, adapter_dir: Path, iters: int) -> list[str]:
    # mlx-lm CLI accepts a dataset directory rather than arbitrary split names.
    # Caller prepares an ephemeral stage directory containing train/valid/test.jsonl.
    return [
        sys.executable, "-m", "mlx_lm.lora",
        "--model", model,
        "--train",
        "--data", str(Path(train_file).parent),
        "--adapter-path", str(adapter_dir),
        "--iters", str(iters),
        "--batch-size", "1",
        "--num-layers", "4",
        "--mask-prompt",
    ]


def stage_split(dataset: dict, work: Path) -> Path:
    stage = work / "dataset"
    stage.mkdir(parents=True, exist_ok=True)
    mapping = {
        dataset["train"]: stage / "train.jsonl",
        dataset["valid"]: stage / "valid.jsonl",
        dataset["test"]: stage / "test.jsonl",
    }
    for src, dst in mapping.items():
        shutil.copyfile(src, dst)
    return stage


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--quarantine", required=True, help="external isolated dataset directory")
    ap.add_argument("--size", type=int, choices=SIZES, default=32)
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--work", default="/tmp/dore-theology-poc")
    ap.add_argument("--iters", type=int, default=80)
    ap.add_argument("--execute", action="store_true", help="actually invoke mlx-lm")
    args = ap.parse_args()

    quarantine = Path(args.quarantine)
    require_quarantine(quarantine)
    dataset = verify_dataset(quarantine, args.size)

    work = Path(args.work).expanduser().resolve() / f"n{args.size}"
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    stage = stage_split(dataset, work)
    adapter = work / "adapter"

    command = build_command(args.model, str(stage / "train.jsonl"), str(stage / "valid.jsonl"), adapter, args.iters)
    report = {
        "ok": True,
        "protocol": "dore.theology-training-poc/1",
        "model": args.model,
        "training_size": args.size,
        "quarantine": str(quarantine.resolve()),
        "canonical_ingest": False,
        "paid_api_required": False,
        "network_required_by_orchestrator": False,
        "adapter_fused_into_base": False,
        "adapter_path": str(adapter),
        "command": command,
        "executed": False,
    }

    if args.execute:
        if not mlx_available():
            die("mlx-lm is not installed/available on this Mac")
        proc = subprocess.run(command, cwd=str(work), text=True)
        report["executed"] = True
        report["returncode"] = proc.returncode
        report["ok"] = proc.returncode == 0

    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
