"""Deterministic minimum-sufficient planner for Bible queries.

This module is part of Doré itself. It chooses the lightest Doré capability lane that
can satisfy a Scripture request before any semantic/reasoning escalation. It never
generates a theological answer and never requires a model to classify the common
Bible lookup/reflex cases covered here.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import re

_REFERENCE = re.compile(
    r"(?:[1-3]?\s*[A-Za-z]{2,}|[\u4e00-\u9fff]{1,8})\s*\d{1,3}\s*[:：]\s*\d{1,3}(?:\s*[-–—]\s*\d{1,3})?"
)
_COUNT = re.compile(
    r"(?:幾|几|多少)(?:位|個|个)?.{0,12}(?:人|人物|馬利亞|马利亚)|(?:一共|總共|总共).{0,12}(?:幾|几|多少)"
)
_GEO = re.compile(
    r"(?:哪裡|哪里|何處|何处|地點|地点|距離|距离|多遠|多远|路線|路线|地圖|地图|位於|位于|城|山|河|海|曠野|旷野)"
)
_HISTORY = re.compile(
    r"(?:時代|时代|年代|時期|时期|帝國|帝国|王朝|先後|先后|之前|之後|之后|歷史|历史)"
)
_RELATION = re.compile(
    r"(?:關係|关系|同一人|同一個|同一个|誰是|谁是|是不是|串珠|相關|相关|呼應|呼应|平行)"
)
_INTERPRETIVE = re.compile(
    r"(?:為什麼|为什么|如何理解|怎麼理解|怎么理解|意義|意义|神學|神学|解釋|解释)"
)


@dataclass(frozen=True)
class BibleQueryPlan:
    schema: str
    query: str
    intent: str
    lanes: tuple[str, ...]
    execution_level: str
    semantic_allowed: bool
    reasoning_allowed: bool
    large_model_required: bool
    model_invoked: bool
    escalation_policy: str
    reason: str

    def to_dict(self) -> dict:
        data = asdict(self)
        data["lanes"] = list(self.lanes)
        return data


def plan_bible_query(
    query: str,
    *,
    explicit_search: bool = False,
    deep: bool = False,
) -> BibleQueryPlan:
    """Return a deterministic Doré execution plan for a Bible-oriented query.

    ``deep`` is an explicit escalation request. Ordinary lookup, entity, geography,
    chronology and relation questions remain in deterministic/retrieval lanes.
    Interpretive wording marks reasoning as appropriate, but does not itself invoke a
    model; the caller can still enforce authorization, privacy and availability gates.
    """
    q = " ".join((query or "").strip().split())
    if not q:
        return BibleQueryPlan(
            "dore.bible-query-plan.v1",
            q,
            "empty",
            (),
            "L0-deterministic",
            False,
            False,
            False,
            False,
            "lowest-sufficient-capability",
            "empty query",
        )

    lanes: list[str] = []
    intent = "bible_context"

    if _REFERENCE.search(q):
        intent = "reference"
        lanes.extend(("reference", "biblical_world"))
    elif _COUNT.search(q):
        intent = "entity"
        lanes.extend(("entity", "biblical_world"))
    elif _GEO.search(q):
        intent = "geography"
        lanes.extend(("geography", "biblical_world"))
    elif _HISTORY.search(q):
        intent = "chronology"
        lanes.extend(("chronology", "biblical_world"))
    elif _RELATION.search(q):
        intent = "relation"
        lanes.extend(("entity", "relation", "biblical_world"))
    else:
        lanes.append("biblical_world")

    lanes.extend(("document", "personal_context"))

    interpretive = bool(_INTERPRETIVE.search(q))
    semantic = bool(explicit_search or deep)
    reasoning = bool(deep or interpretive)

    if semantic:
        lanes.append("semantic")
    if reasoning:
        lanes.append("reasoning")

    if reasoning:
        execution_level = "L3-reasoning"
    elif semantic:
        execution_level = "L2-light-interpretation"
    elif intent in {"reference", "entity", "geography", "chronology", "relation"}:
        execution_level = "L1-retrieval"
    else:
        execution_level = "L1-retrieval"

    return BibleQueryPlan(
        "dore.bible-query-plan.v1",
        q,
        intent,
        tuple(dict.fromkeys(lanes)),
        execution_level,
        semantic,
        reasoning,
        False,
        False,
        "lowest-sufficient-capability",
        "Doré owns the capability; deterministic/structured retrieval runs before model escalation",
    )
