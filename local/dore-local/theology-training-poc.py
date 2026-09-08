#!/usr/bin/env python3
"""Doré Theology Alignment micro-POC through the isolated MLX-VLM toolchain.

Purpose:
- train/evaluate a tiny LoRA adapter for abstract Christian theological alignment
- keep adversarial fixtures quarantined outside Doré Core/Knowledge/Memory
- never ingest training/eval records into canonical Doré stores
- keep the adapter separate from the runtime/base model
- stop at the requested learning-curve size (32/64/128/256)

The orchestration is deliberately cache-only during execution. Model/tool downloads belong
to an explicit preparation step, never to the training action itself.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import time
from pathlib import Path

CACHE_ROOT = Path.home() / "Library" / "Caches" / "Dore" / "theology-training"
VENV = CACHE_ROOT / "venv"
PY = VENV / "bin" / "python"
DEFAULT_TRAINING_MODEL = os.environ.get("DORE_THEOLOGY_MLX_MODEL", "mlx-community/gemma-4-e4b-it-4bit")
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
    valid_n = count_jsonl(valid)
    test_n = count_jsonl(test)
    if train_n != size:
        die(f"expected {size} training rows, found {train_n}")
    if valid_n < 1 or test_n < 1:
        die("valid/test quarantine splits must be non-empty")
    return {
        "train": str(train),
        "valid": str(valid),
        "test": str(test),
        "train_rows": train_n,
        "valid_rows": valid_n,
        "test_rows": test_n,
    }


def mlx_vlm_available() -> bool:
    if not PY.is_file():
        return False
    probe = subprocess.run(
        [str(PY), "-c", "import mlx_vlm, datasets"],
        text=True,
        capture_output=True,
        timeout=30,
    )
    return probe.returncode == 0


def build_command(model: str, dataset_dir: Path, adapter_file: Path, iters: int) -> list[str]:
    return [
        str(PY), "-m", "mlx_vlm.lora",
        "--model-path", model,
        "--dataset", str(dataset_dir),
        "--split", "train",
        "--iters", str(iters),
        "--batch-size", "1",
        "--learning-rate", "2e-5",
        "--lora-rank", "8",
        "--lora-alpha", "16",
        "--max-seq-length", "2048",
        "--train-on-completions",
        "--steps-per-report", "10",
        "--steps-per-eval", "20",
        "--val-batches", "4",
        "--output-path", str(adapter_file),
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
    ap.add_argument("--model", default=DEFAULT_TRAINING_MODEL, help="MLX-VLM model path/id; independent of DORE_LOCAL_MODEL")
    ap.add_argument("--work", default=str(CACHE_ROOT / "runs"))
    ap.add_argument("--iters", type=int, default=80)
    ap.add_argument("--execute", action="store_true", help="actually invoke MLX-VLM LoRA training")
    args = ap.parse_args()

    quarantine = Path(args.quarantine)
    require_quarantine(quarantine)
    dataset = verify_dataset(quarantine, args.size)

    work = Path(args.work).expanduser().resolve() / f"n{args.size}"
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    stage = stage_split(dataset, work)
    adapter_dir = work / "adapter"
    adapter_dir.mkdir(parents=True, exist_ok=True)
    adapter_file = adapter_dir / "adapter.safetensors"

    command = build_command(args.model, stage, adapter_file, args.iters)
    report = {
        "ok": True,
        "protocol": "dore.theology-training-poc/3",
        "training_backend": "mlx-vlm",
        "training_model": args.model,
        "runtime_model": os.environ.get("DORE_LOCAL_MODEL", "gemma4:e4b"),
        "training_size": args.size,
        "dataset_rows": {
            "train": dataset["train_rows"],
            "valid": dataset["valid_rows"],
            "test": dataset["test_rows"],
        },
        "quarantine": str(quarantine.resolve()),
        "canonical_ingest": False,
        "paid_api_required": False,
        "network_action_performed": False,
        "adapter_fused_into_base": False,
        "adapter_path": str(adapter_file),
        "command": command,
        "executed": False,
    }

    if args.execute:
        if not mlx_vlm_available():
            die("isolated MLX-VLM training environment is not prepared")
        env = os.environ.copy()
        hf_home = CACHE_ROOT / "hf"
        env["HF_HOME"] = str(hf_home)
        env["HF_HUB_CACHE"] = str(hf_home / "hub")
        env["HF_HUB_OFFLINE"] = "1"
        env["TRANSFORMERS_OFFLINE"] = "1"
        started = time.monotonic()
        proc = subprocess.run(
            command,
            cwd=str(work),
            text=True,
            capture_output=True,
            timeout=6900,
            env=env,
        )
        report["executed"] = True
        report["returncode"] = proc.returncode
        report["seconds"] = round(time.monotonic() - started, 3)
        report["stdout_tail"] = proc.stdout[-5000:]
        report["stderr_tail"] = proc.stderr[-5000:]
        report["ok"] = proc.returncode == 0 and adapter_file.is_file()
        report["adapter_present"] = adapter_file.is_file()
        report["adapter_bytes"] = adapter_file.stat().st_size if adapter_file.is_file() else 0

    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
