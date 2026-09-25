"""Local, zero-API context economy gate for Codex/Doré engineering."""
from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class ContextBudget:
    max_files: int = 8
    max_bytes: int = 48_000


@dataclass(frozen=True)
class EvidenceRef:
    path: str
    sha256: str
    size: int


@dataclass(frozen=True)
class ContextDecision:
    target: str
    task: str
    evidence: tuple[EvidenceRef, ...]
    insufficient: bool
    reason: str


def fingerprint(path: Path) -> EvidenceRef:
    data = path.read_bytes()
    return EvidenceRef(str(path), hashlib.sha256(data).hexdigest(), len(data))


def bounded_working_set(
    target: str,
    task: str,
    candidates: Iterable[Path],
    *,
    budget: ContextBudget = ContextBudget(),
) -> ContextDecision:
    """Admit only a bounded working set; expansion must be explicit."""
    evidence: list[EvidenceRef] = []
    used = 0
    for path in candidates:
        if len(evidence) >= budget.max_files:
            break
        ref = fingerprint(path)
        if evidence and used + ref.size > budget.max_bytes:
            break
        evidence.append(ref)
        used += ref.size
    insufficient = not evidence
    return ContextDecision(
        target=target,
        task=task,
        evidence=tuple(evidence),
        insufficient=insufficient,
        reason="no evidence admitted" if insufficient else "bounded evidence admitted",
    )


def needs_invalidation(cached: EvidenceRef, path: Path) -> bool:
    """Verified state is reusable until the underlying file fingerprint changes."""
    return cached.sha256 != fingerprint(path).sha256
