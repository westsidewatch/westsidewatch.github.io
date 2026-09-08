"""LongMemory adapter below Doré Knowledge Authority.

The adapter is deliberately CLI-based and read-only by default so Doré can evaluate
LongMemory without transferring identity, authority, or product contracts to it.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

Runner = Callable[[list[str]], subprocess.CompletedProcess[str]]

_MANAGED_BIN = Path.home() / "Library" / "Application Support" / "Dore" / "local-ai" / "bin" / "longmemory"


@dataclass(frozen=True)
class LongMemoryConfig:
    db: Path
    project: str
    binary: str = "longmemory"


def resolve_binary(binary: str = "longmemory") -> str:
    """Resolve Doré-managed LongMemory without relying on an interactive-shell PATH."""
    if binary != "longmemory":
        return binary
    configured = str(os.environ.get("DORE_LONGMEMORY_BIN") or "").strip()
    if configured and Path(configured).is_file():
        return configured
    if _MANAGED_BIN.is_file():
        return str(_MANAGED_BIN)
    return shutil.which("longmemory") or "longmemory"


def available(binary: str = "longmemory") -> bool:
    resolved = resolve_binary(binary)
    return Path(resolved).is_file() if resolved != binary or "/" in resolved else shutil.which(resolved) is not None


def _run(argv: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(argv, text=True, capture_output=True, timeout=30, check=False)


def recall(query: str, config: LongMemoryConfig, *, mode: str = "strict", runner: Runner = _run) -> dict:
    if not query.strip():
        return {"ok": True, "results": [], "substrate": "longmemory", "authority": False}
    if mode not in {"strict", "historical", "associative", "world_grounded"}:
        raise ValueError("unsupported LongMemory recall mode")
    argv = [resolve_binary(config.binary), "recall", query, "--mode", mode, "--db", str(config.db), "--project", config.project, "--json"]
    result = runner(argv)
    if result.returncode != 0:
        return {"ok": False, "substrate": "longmemory", "authority": False, "error": result.stderr.strip() or "longmemory_failed"}
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"ok": False, "substrate": "longmemory", "authority": False, "error": "invalid_json"}
    return {"ok": True, "substrate": "longmemory", "authority": False, "mode": mode, "payload": payload}


def project_context(task: str, config: LongMemoryConfig, *, runner: Runner = _run) -> dict:
    argv = [resolve_binary(config.binary), "project", "context", task, "--db", str(config.db), "--project", config.project, "--json"]
    result = runner(argv)
    if result.returncode != 0:
        return {"ok": False, "substrate": "longmemory", "authority": False, "error": result.stderr.strip() or "longmemory_failed"}
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"ok": False, "substrate": "longmemory", "authority": False, "error": "invalid_json"}
    return {"ok": True, "substrate": "longmemory", "authority": False, "payload": payload}
