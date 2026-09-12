"""DORÉ Visual Editorial Director — Candidate 01 live editorial selector.

This is an editorial decision layer, not an image searcher. It receives sitewide
content candidates, estimates fuzzy 4W affinity and editorial brightness, then
assigns visual/reading/temporal capacity for the Living Editorial River.
"""
from __future__ import annotations

import math
import re
from dataclasses import dataclass, asdict
from typing import Iterable

SCHEMA = "dore.visual-editorial-director.v1"
WORLDS = ("WATCH", "WITNESS", "WALK", "WORSHIP")

# Seed vocabulary is deliberately porous: a candidate can score in several W's.
# This is affinity, not taxonomy.
AFFINITY = {
    "WATCH": {
        "守望": 1.0, "黎明": .92, "看見": .86, "門": .74, "米斯巴": .9,
        "新聞": .64, "此刻": .66, "城市": .52, "光": .58, "等待": .7,
        "watch": 1.0, "dawn": .92, "gate": .74, "mizpah": .9,
    },
    "WITNESS": {
        "見證": 1.0, "人物": .78, "生命": .8, "記憶": .82, "教會": .62,
        "歷史": .68, "受洗": .86, "宣教": .8, "伯特利": .64, "testimony": 1.0,
        "witness": 1.0, "memory": .82, "mission": .8, "history": .68,
    },
    "WALK": {
        "查經": 1.0, "經文": .86, "學習": .78, "地圖": .72, "行走": .86,
        "以馬忤斯": .94, "研究": .76, "筆記": .7, "one": .9, "folio": .72,
        "scripture": .86, "study": .8, "walk": 1.0, "emmaus": .94,
    },
    "WORSHIP": {
        "敬拜": 1.0, "禱告": .96, "讚美": .9, "盼望": .74, "細拉": .82,
        "瑪拉拿": 1.0, "安靜": .66, "主": .52, "worship": 1.0,
        "prayer": .96, "maranatha": 1.0, "selah": .82,
    },
}

@dataclass(frozen=True)
class Candidate:
    id: str
    title: str
    source: str
    deck: str
    image: str
    world: str
    tags: tuple[str, ...] = ()
    freshness: float = .5
    significance: float = .5
    visual_strength: float = .5
    depth: float = .5

@dataclass(frozen=True)
class Decision:
    candidate_id: str
    w: str
    affinity: float
    brightness: float
    editorial_score: float
    weight: int
    shape: str
    reason: str


def _text(c: Candidate) -> str:
    return " ".join((c.title, c.source, c.deck, *c.tags)).lower()


def affinity(c: Candidate, w: str) -> float:
    text = _text(c)
    hits = []
    for token, value in AFFINITY[w].items():
        if token.lower() in text:
            hits.append(value)
    if not hits:
        return .12
    # Multiple weak signals can overtake a single accidental keyword, but cap it.
    return min(1.0, max(hits) + .12 * sum(sorted(hits, reverse=True)[1:3]))


def brightness(c: Candidate) -> float:
    # "亮" is editorial, not popularity: significance and depth lead; visual
    # strength and freshness help decide what deserves homepage attention now.
    value = (
        .36 * c.significance
        + .26 * c.depth
        + .23 * c.visual_strength
        + .15 * c.freshness
    )
    return max(0.0, min(1.0, value))


def decide(c: Candidate, preferred_w: str | None = None) -> Decision:
    scores = {w: affinity(c, w) for w in WORLDS}
    w = preferred_w if preferred_w in WORLDS else max(scores, key=scores.get)
    a = scores[w]
    b = brightness(c)
    score = .58 * a + .42 * b
    if score >= .82:
        weight, shape = 3, "wide"
    elif score >= .66:
        weight, shape = 2, "wide"
    else:
        weight = 1
        # Portrait is an editorial breathing device, not a random alternate ratio.
        shape = "portrait" if c.visual_strength >= .72 and c.depth < .72 else "standard"
    reason = f"{w} affinity {a:.2f}; brightness {b:.2f}; capacity {weight}"
    return Decision(c.id, w, round(a, 3), round(b, 3), round(score, 3), weight, shape, reason)


def select(candidates: Iterable[Candidate], per_w: int = 4) -> dict[str, list[tuple[Candidate, Decision]]]:
    """Select a balanced river without turning 4W into four hard folders."""
    pool = list(candidates)
    ranked: dict[str, list[tuple[Candidate, Decision]]] = {w: [] for w in WORLDS}
    for w in WORLDS:
        options = [(c, decide(c, w)) for c in pool]
        options.sort(key=lambda pair: pair[1].editorial_score, reverse=True)
        ranked[w] = options

    used: set[str] = set()
    result: dict[str, list[tuple[Candidate, Decision]]] = {w: [] for w in WORLDS}
    for w in WORLDS:
        for c, d in ranked[w]:
            if c.id in used:
                continue
            # Avoid a merely bright but semantically irrelevant item stealing a river.
            if d.affinity < .28:
                continue
            result[w].append((c, d))
            used.add(c.id)
            if len(result[w]) == per_w:
                break
    return result


def contract() -> dict:
    return {
        "schema": SCHEMA,
        "role": "Visual Editorial Director",
        "selection": "sitewide-highlight",
        "classification": "4w-fuzzy-affinity",
        "brightness": "significance+depth+visual-strength+freshness",
        "weight_meaning": "visual+reading+temporal-capacity",
        "world_interface": "dore.world-surface/1",
        "principle": "editorial judgment, not popularity ranking",
    }
