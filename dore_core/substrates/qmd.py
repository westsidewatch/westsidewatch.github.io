"""QMD adapter below Doré Search/Context.

Default mode is lexical/no-LLM. Hybrid mode can be selected explicitly and keeps
reranking off unless deep=True, preserving the minimum-capability rule.
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

_MANAGED_BIN = Path.home() / "Library" / "Application Support" / "Dore" / "local-ai" / "bin" / "qmd"


@dataclass(frozen=True)
class QMDConfig:
    collection: str | None = None
    binary: str = "qmd"


def resolve_binary(binary: str = "qmd") -> str:
    """Resolve Doré-managed QMD without relying on an interactive-shell PATH."""
    if binary != "qmd":
        return binary
    configured = str(os.environ.get("DORE_QMD_BIN") or "").strip()
    if configured and Path(configured).is_file():
        return configured
    if _MANAGED_BIN.is_file():
        return str(_MANAGED_BIN)
    return shutil.which("qmd") or "qmd"


def available(binary: str = "qmd") -> bool:
    resolved = resolve_binary(binary)
    return Path(resolved).is_file() if resolved != binary or "/" in resolved else shutil.which(resolved) is not None


def _run(argv: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(argv, text=True, capture_output=True, timeout=30, check=False)


def search(query: str, config: QMDConfig = QMDConfig(), *, semantic: bool = False, deep: bool = False, limit: int = 8, runner: Runner = _run) -> dict:
    if not query.strip():
        return {"ok": True, "results": [], "substrate": "qmd", "authority": False, "lane": "deterministic"}
    if limit < 1 or limit > 50:
        raise ValueError("limit must be between 1 and 50")
    if deep:
        command = "query"
        lane = "hybrid-rerank"
    elif semantic:
        command = "query"
        lane = "hybrid-no-rerank"
    else:
        command = "search"
        lane = "bm25"
    argv = [resolve_binary(config.binary), command, query, "--json", "-n", str(limit)]
    if config.collection:
        argv += ["-c", config.collection]
    if semantic and not deep:
        argv += ["--no-rerank"]
    result = runner(argv)
    if result.returncode != 0:
        return {"ok": False, "substrate": "qmd", "authority": False, "lane": lane, "error": result.stderr.strip() or "qmd_failed"}
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"ok": False, "substrate": "qmd", "authority": False, "lane": lane, "error": "invalid_json"}
    return {"ok": True, "substrate": "qmd", "authority": False, "lane": lane, "results": payload}
