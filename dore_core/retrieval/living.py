"""Doré Living Retrieval: fuzzy search begins before explicit search.

The orchestrator is intentionally small. It chooses the lightest retrieval lane and
returns evidence only; it never grants retrieved text authority or executes it.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable


@dataclass(frozen=True)
class RetrievalPlan:
    lexical: bool
    semantic: bool
    deep: bool
    recall_memory: bool
    reason: str


_NOTE_CUES = (
    "想到", "讓我想到", "这让我想到", "這讓我想到", "這句", "这句",
    "好像", "似乎", "可能和", "是不是和", "讓我想起", "让我想起",
)


def plan(text: str, *, explicit_search: bool = False, deep_requested: bool = False) -> RetrievalPlan:
    q = " ".join(text.split())
    if not q:
        return RetrievalPlan(False, False, False, False, "empty")
    if deep_requested:
        return RetrievalPlan(True, True, True, True, "explicit deep retrieval")
    # Note-like association language is a fuzzy-search signal even when Chinese text
    # is short in character count. Detect intent before applying the compact-query gate.
    note_like = any(cue in q for cue in _NOTE_CUES)
    if note_like:
        return RetrievalPlan(True, True, False, explicit_search, "note-like association: hybrid without rerank")
    # Short identifiers, references, and compact terms stay deterministic/lexical.
    compact = len(q) <= 18 and len(q.split()) <= 3
    if compact:
        return RetrievalPlan(True, False, False, explicit_search, "compact query: BM25 first")
    # Longer natural-language note fragments receive local hybrid retrieval without rerank.
    return RetrievalPlan(True, True, False, explicit_search, "note-like query: hybrid without rerank")


def retrieve(
    text: str,
    *,
    qmd_search: Callable[..., dict[str, Any]],
    memory_recall: Callable[..., dict[str, Any]] | None = None,
    explicit_search: bool = False,
    deep_requested: bool = False,
    limit: int = 6,
) -> dict[str, Any]:
    p = plan(text, explicit_search=explicit_search, deep_requested=deep_requested)
    if not p.lexical:
        return {"ok": True, "plan": p, "evidence": [], "authority": False}
    qmd = qmd_search(text, semantic=p.semantic, deep=p.deep, limit=limit)
    evidence: list[dict[str, Any]] = []
    if qmd.get("ok"):
        evidence.append({"source": "qmd", "payload": qmd})
    memory = None
    if p.recall_memory and memory_recall is not None:
        memory = memory_recall(text, mode="strict")
        if memory.get("ok"):
            evidence.append({"source": "longmemory", "payload": memory})
    return {
        "ok": bool(evidence) or bool(qmd.get("ok")),
        "plan": p,
        "qmd": qmd,
        "memory": memory,
        "evidence": evidence,
        "authority": False,
    }
