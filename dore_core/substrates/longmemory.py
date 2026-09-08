"""LongMemory adapter below Doré Knowledge Authority.

The adapter is deliberately CLI-based and read-only by default so Doré can evaluate
LongMemory without transferring identity, authority, or product contracts to it.
"""
from __future__ import annotations

import json
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

Runner = Callable[[list[str]], subprocess.CompletedProcess[str]]


@dataclass(frozen=True)
class LongMemoryConfig:
    db: Path
    project: str
    binary: str = "longmemory"


def available(binary: str = "longmemory") -> bool:
    return shutil.which(binary) is not None


def _run(argv: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(argv, text=True, capture_output=True, timeout=30, check=False)


def recall(query: str, config: LongMemoryConfig, *, mode: str = "strict", runner: Runner = _run) -> dict:
    if not query.strip():
        return {"ok": True, "results": [], "substrate": "longmemory", "authority": False}
    if mode not in {"strict", "historical", "associative", "world_grounded"}:
        raise ValueError("unsupported LongMemory recall mode")
    argv = [config.binary, "recall", query, "--mode", mode, "--db", str(config.db), "--project", config.project, "--json"]
    result = runner(argv)
    if result.returncode != 0:
        return {"ok": False, "substrate": "longmemory", "authority": False, "error": result.stderr.strip() or "longmemory_failed"}
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"ok": False, "substrate": "longmemory", "authority": False, "error": "invalid_json"}
    return {"ok": True, "substrate": "longmemory", "authority": False, "mode": mode, "payload": payload}


def project_context(task: str, config: LongMemoryConfig, *, runner: Runner = _run) -> dict:
    argv = [config.binary, "project", "context", task, "--db", str(config.db), "--project", config.project, "--json"]
    result = runner(argv)
    if result.returncode != 0:
        return {"ok": False, "substrate": "longmemory", "authority": False, "error": result.stderr.strip() or "longmemory_failed"}
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"ok": False, "substrate": "longmemory", "authority": False, "error": "invalid_json"}
    return {"ok": True, "substrate": "longmemory", "authority": False, "payload": payload}
