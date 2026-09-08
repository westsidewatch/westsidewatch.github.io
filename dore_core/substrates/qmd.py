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

_LOCAL_AI = Path.home() / "Library" / "Application Support" / "Dore" / "local-ai"
_MANAGED_BIN = _LOCAL_AI / "bin" / "qmd"
_PRODUCTION_ROOT = _LOCAL_AI / "data" / "qmd" / "production"
PRODUCTION_COLLECTION = "dore-production"


@dataclass(frozen=True)
class QMDConfig:
    collection: str | None = None
    binary: str = "qmd"
    state_root: Path | None = None


def production_config(*, binary: str = "qmd", collection: str = PRODUCTION_COLLECTION) -> QMDConfig:
    """Return the QMD state used by Doré's admitted production corpus."""
    return QMDConfig(collection=collection, binary=binary, state_root=_PRODUCTION_ROOT)


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


def _environment(config: QMDConfig) -> dict[str, str] | None:
    if config.state_root is None:
        return None
    root = Path(config.state_root).expanduser().resolve()
    home, cfg, cache = root / "home", root / "config", root / "cache"
    for path in (home, cfg, cache):
        path.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env.update({
        "HOME": str(home),
        "XDG_CONFIG_HOME": str(cfg),
        "XDG_CACHE_HOME": str(cache),
    })
    return env


def _run(argv: list[str], *, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(argv, text=True, capture_output=True, timeout=30, check=False, env=env)


def search(
    query: str,
    config: QMDConfig = QMDConfig(),
    *,
    semantic: bool = False,
    deep: bool = False,
    limit: int = 8,
    runner: Runner | None = None,
) -> dict:
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
    result = runner(argv) if runner is not None else _run(argv, env=_environment(config))
    if result.returncode != 0:
        return {"ok": False, "substrate": "qmd", "authority": False, "lane": lane, "error": result.stderr.strip() or "qmd_failed"}
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"ok": False, "substrate": "qmd", "authority": False, "lane": lane, "error": "invalid_json"}
    return {
        "ok": True,
        "substrate": "qmd",
        "authority": False,
        "lane": lane,
        "collection": config.collection,
        "managed_state": bool(config.state_root),
        "results": payload,
    }
