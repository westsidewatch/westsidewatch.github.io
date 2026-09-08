"""BI-2 minimum-capability planner for Bible queries.

The planner is deterministic. It decides which existing Doré organs should be tried
before semantic/model escalation; it does not answer theology itself.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
import re

_REFERENCE = re.compile(r"(?:[1-3]?\s*[A-Za-z]{2,}|[\u4e00-\u9fff]{1,8})\s*\d{1,3}\s*[:：]\s*\d{1,3}(?:\s*[-–—]\s*\d{1,3})?")
_COUNT = re.compile(r"(?:幾|几|多少)(?:位|個|个)?.{0,12}(?:人|人物|馬利亞|马利亚)|(?:一共|總共|总共).{0,12}(?:幾|几|多少)")
_GEO = re.compile(r"(?:哪裡|哪里|何處|何处|地點|地点|距離|距离|多遠|多远|路線|路线|地圖|地图|位於|位于|城|山|河|海|曠野|旷野)")
_HISTORY = re.compile(r"(?:時代|时代|年代|時期|时期|帝國|帝国|王朝|先後|先后|之前|之後|之后|歷史|历史)")
_RELATION = re.compile(r"(?:關係|关系|同一人|同一個|同一个|誰是|谁是|是不是|為什麼|为什么|串珠|相關|相关|呼應|呼应)")

@dataclass(frozen=True)
class BibleQueryPlan:
    schema: str
    query: str
    intent: str
    lanes: tuple[str, ...]
    semantic_allowed: bool
    reasoning_allowed: bool
    large_model_required: bool
    reason: str

    def to_dict(self) -> dict:
        data=asdict(self); data['lanes']=list(self.lanes); return data


def plan_bible_query(query: str, *, explicit_search: bool=False, deep: bool=False) -> BibleQueryPlan:
    q=' '.join((query or '').strip().split())
    if not q:
        return BibleQueryPlan('dore.bible-query-plan.v1',q,'empty',(),False,False,False,'empty query')
    lanes=[]; intent='bible_context'
    if _REFERENCE.search(q):
        intent='reference'; lanes.extend(('reference','biblical_world'))
    elif _COUNT.search(q):
        intent='entity'; lanes.extend(('entity','biblical_world'))
    elif _GEO.search(q):
        intent='geography'; lanes.extend(('geography','biblical_world'))
    elif _HISTORY.search(q):
        intent='chronology'; lanes.extend(('chronology','biblical_world'))
    elif _RELATION.search(q):
        intent='relation'; lanes.extend(('entity','relation','biblical_world'))
    else:
        lanes.append('biblical_world')
    lanes.extend(('document','personal_context'))
    semantic=bool(explicit_search or deep)
    reasoning=bool(deep)
    if semantic: lanes.append('semantic')
    if reasoning: lanes.append('reasoning')
    return BibleQueryPlan(
        'dore.bible-query-plan.v1',q,intent,tuple(dict.fromkeys(lanes)),semantic,reasoning,
        False,
        'minimum-capability order: exact/reference/world before document/context and model escalation',
    )
