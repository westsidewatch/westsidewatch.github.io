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


_ASSOCIATION_CUES = (
    "想到", "聯想到", "联想到", "讓我想到", "让我想到", "這讓我想到", "这让我想到",
    "讓我想起", "让我想起", "想起", "這句", "这句", "好像", "似乎", "像是", "类似", "類似",
    "相關", "相关", "關於", "关于", "呼應", "呼应", "對應", "对应", "平行", "串珠",
    "可能和", "是不是和", "有沒有關係", "有没有关系", "預表", "预表", "應驗", "应验",
)

_CJK_SENTENCE_CUES = (
    "的", "了", "是", "和", "與", "与", "在", "中", "裡", "里", "嗎", "吗", "呢", "為什麼", "为什么",
)


def _looks_like_cjk_phrase(q: str) -> bool:
    cjk_count = sum(1 for ch in q if "\u3400" <= ch <= "\u9fff")
    if cjk_count < 5:
        return False
    return any(cue in q for cue in _CJK_SENTENCE_CUES) or cjk_count >= 9


def plan(text: str, *, explicit_search: bool = False, deep_requested: bool = False) -> RetrievalPlan:
    q = " ".join(text.split())
    if not q:
        return RetrievalPlan(False, False, False, False, "empty")
    if deep_requested:
        return RetrievalPlan(True, True, True, True, "explicit deep retrieval")

    association_like = any(cue in q for cue in _ASSOCIATION_CUES)
    if association_like:
        return RetrievalPlan(True, True, False, explicit_search, "association intent: hybrid without rerank")

    # Chinese prose often contains no spaces. Do not mistake a short natural-language
    # sentence for a compact identifier simply because split() returns one token.
    if _looks_like_cjk_phrase(q):
        return RetrievalPlan(True, True, False, explicit_search, "CJK natural-language phrase: hybrid without rerank")

    # Short identifiers, references, names, and compact terms stay deterministic/lexical.
    compact = len(q) <= 18 and len(q.split()) <= 3
    if compact:
        return RetrievalPlan(True, False, False, explicit_search, "compact query: BM25 first")

    # Longer natural-language fragments receive local hybrid retrieval without rerank.
    return RetrievalPlan(True, True, False, explicit_search, "natural-language query: hybrid without rerank")


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
        return {
            "ok": True,
            "plan": p,
            "qmd": None,
            "memory": None,
            "evidence": [],
            "authority": False,
            "large_model_invoked": False,
        }

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
        "large_model_invoked": False,
    }
