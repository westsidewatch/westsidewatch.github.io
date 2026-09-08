#!/usr/bin/env python3
"""Run exactly the first 32-example Doré theology adapter training step.

This entrypoint is intentionally fixed: no arbitrary shell command, dataset path, size,
or model arguments are accepted from A2A callers. By default it consumes Doré's isolated,
reproducible cache quarantine built by theology-training-stage32.py. An owner process may
override that root with DORE_THEOLOGY_QUARANTINE; theology-training-poc.py re-validates it.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

DEFAULT_QUARANTINE = Path.home() / "Library" / "Caches" / "Dore" / "theology-training" / "quarantine-v1"


def repo_root() -> Path:
    return Path(
        os.environ.get("DORE_REPO_ROOT")
        or os.environ.get("DORE_WORKTREE")
        or Path.home() / "westsidewatch.github.io"
    ).expanduser().resolve()


def build_command(repo: Path, quarantine: Path) -> list[str]:
    poc = repo / "local" / "dore-local" / "theology-training-poc.py"
    return [
        sys.executable,
        str(poc),
        "--quarantine", str(quarantine),
        "--size", "32",
        "--execute",
    ]


def main() -> None:
    repo = repo_root()
    quarantine = Path(os.environ.get("DORE_THEOLOGY_QUARANTINE") or DEFAULT_QUARANTINE).expanduser().resolve()
    required = [quarantine / "train-32.jsonl", quarantine / "valid.jsonl", quarantine / "test.jsonl"]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        print(json.dumps({
            "ok": False,
            "status": "failed",
            "error": {
                "code": "quarantine_not_staged",
                "message": "Run theology.training.stage32 before micro32.",
                "missing": missing,
            },
        }, ensure_ascii=False, indent=2))
        raise SystemExit(2)

    poc = repo / "local" / "dore-local" / "theology-training-poc.py"
    if not poc.is_file():
        print(json.dumps({
            "ok": False,
            "status": "failed",
            "error": {"code": "poc_script_missing", "message": str(poc)},
        }, ensure_ascii=False, indent=2))
        raise SystemExit(2)

    command = build_command(repo, quarantine)
    try:
        proc = subprocess.run(
            command,
            cwd=str(repo),
            text=True,
            capture_output=True,
            timeout=7000,
            env=os.environ.copy(),
        )
    except Exception as exc:
        print(json.dumps({
            "ok": False,
            "status": "failed",
            "error": {"code": "micro32_exception", "message": str(exc)},
        }, ensure_ascii=False, indent=2))
        raise SystemExit(2)

    try:
        training = json.loads(proc.stdout)
    except Exception as exc:
        print(json.dumps({
            "ok": False,
            "status": "failed",
            "returncode": proc.returncode,
            "error": {"code": "invalid_training_json", "message": str(exc)},
            "stdout_tail": proc.stdout[-3000:],
            "stderr_tail": proc.stderr[-3000:],
        }, ensure_ascii=False, indent=2))
        raise SystemExit(2)

    ok = proc.returncode == 0 and bool(training.get("ok")) and training.get("training_size") == 32
    report = {
        "ok": ok,
        "status": "completed" if ok else "failed",
        "protocol": "dore.theology-training-micro32/2",
        "training_size": 32,
        "quarantine": str(quarantine),
        "canonical_ingest": False,
        "paid_api_required": False,
        "arbitrary_shell_allowed": False,
        "training": training,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(0 if ok else 2)


if __name__ == "__main__":
    main()
