"""Single local entrypoint composing Doré Context Economy primitives."""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from .code_retrieval import CodeHit, retrieve_code
from .economy import ContextBudget, ContextDecision, bounded_working_set
from .tool_economy import OutputDigest, VerifiedState, can_reuse_verified, compress_output

@dataclass(frozen=True)
class GateResult:
    admission: ContextDecision
    code: tuple[CodeHit, ...]

def ui_context(target: str, task: str, candidates: Iterable[Path], *, query: str | None = None,
               budget: ContextBudget = ContextBudget()) -> GateResult:
    paths = tuple(candidates)
    admission = bounded_working_set(target, task, paths, budget=budget)
    admitted = [Path(ref.path) for ref in admission.evidence]
    code = tuple(retrieve_code(query or f"{target} {task}", admitted))
    return GateResult(admission, code)

def ui_expand(target: str, task: str, candidates: Iterable[Path], *, reason: str,
              query: str | None = None, budget: ContextBudget = ContextBudget(max_files=16, max_bytes=96000)) -> GateResult:
    if not reason.strip():
        raise ValueError("context expansion requires an explicit reason")
    return ui_context(target, task, candidates, query=query, budget=budget)

def ui_verify(state: VerifiedState | None, inputs: Iterable[Path]) -> bool:
    return bool(state and can_reuse_verified(state, inputs))

def tool_context(text: str, *, max_bytes: int = 12000) -> OutputDigest:
    return compress_output(text, max_bytes=max_bytes)
