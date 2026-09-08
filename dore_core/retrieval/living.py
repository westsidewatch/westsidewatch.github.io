"""Doré Living Retrieval: fuzzy search begins before explicit search.

The orchestrator chooses the lightest retrieval lane and returns evidence only; it
never grants retrieved text authority or executes it. Provider payloads are normalized
into a stable Doré Search result contract before products see them.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from dore_core.retrieval.results import merge_results


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

_PASSIVE_SEPARATORS = (
    "裡的", "里的", "中的", "之中的", "之中", "當中的", "当中的", "裡面", "里面",
)


def _looks_like_cjk_phrase(q: str) -> bool:
    cjk_count = sum(1 for ch in q if "\u3400" <= ch <= "\u9fff")
    if cjk_count < 5:
        return False
    return any(cue in q for cue in _CJK_SENTENCE_CUES) or cjk_count >= 9


def _passive_lexical_query(text: str) -> str:
    """Reduce association prose to deterministic lexical terms without an AI model."""
    q = " ".join(text.split())
    reduced = q
    for cue in sorted(_ASSOCIATION_CUES, key=len, reverse=True):
        reduced = reduced.replace(cue, " ")
    for separator in _PASSIVE_SEPARATORS:
        reduced = reduced.replace(separator, " ")
    for punctuation in "，。！？；：、,.!?;:（）()「」『』《》<>\"'":
        reduced = reduced.replace(punctuation, " ")
    reduced = " ".join(reduced.split())
    return reduced if len(reduced) >= 2 else q


def plan(text: str, *, explicit_search: bool = False, deep_requested: bool = False) -> RetrievalPlan:
    q = " ".join(text.split())
    if not q:
        return RetrievalPlan(False, False, False, False, "empty")
    if deep_requested:
        return RetrievalPlan(True, True, True, True, "explicit deep retrieval")

    association_like = any(cue in q for cue in _ASSOCIATION_CUES)
    if association_like:
        if explicit_search:
            return RetrievalPlan(True, True, False, True, "explicit association search: hybrid without rerank")
        return RetrievalPlan(True, False, False, False, "passive association reflex: reduced BM25")

    if _looks_like_cjk_phrase(q):
        if explicit_search:
            return RetrievalPlan(True, True, False, True, "explicit CJK natural-language search: hybrid without rerank")
        return RetrievalPlan(True, False, False, False, "passive CJK natural-language reflex: BM25 first")

    compact = len(q) <= 18 and len(q.split()) <= 3
    if compact:
        return RetrievalPlan(True, False, False, explicit_search, "compact query: BM25 first")

    if explicit_search:
        return RetrievalPlan(True, True, False, True, "explicit natural-language search: hybrid without rerank")
    return RetrievalPlan(True, False, False, False, "passive natural-language reflex: BM25 first")


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
            "retrieval_query": "",
            "results": [],
            "qmd": None,
            "memory": None,
            "evidence": [],
            "authority": False,
            "large_model_invoked": False,
        }

    retrieval_query = text if p.semantic or p.deep or explicit_search else _passive_lexical_query(text)
    qmd = qmd_search(retrieval_query, semantic=p.semantic, deep=p.deep, limit=limit)
    evidence: list[dict[str, Any]] = []
    if qmd.get("ok"):
        evidence.append({"source": "qmd", "payload": qmd})

    memory = None
    if p.recall_memory and memory_recall is not None:
        memory = memory_recall(text, mode="strict")
        if memory.get("ok"):
            evidence.append({"source": "longmemory", "payload": memory})

    results = merge_results(qmd, memory, limit=limit)
    return {
        "ok": bool(results) or bool(evidence) or bool(qmd.get("ok")),
        "plan": p,
        "retrieval_query": retrieval_query,
        "results": results,
        "qmd": qmd,
        "memory": memory,
        "evidence": evidence,
        "authority": False,
        "large_model_invoked": False,
    }
