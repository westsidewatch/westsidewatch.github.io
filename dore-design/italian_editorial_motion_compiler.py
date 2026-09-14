#!/usr/bin/env python3
"""Compile Italian Editorial Atlas emergence grammar into Doré motion intent.

Research language remains evidence; this compiler only projects it into the shared
motion vocabulary. It never turns publication names into templates or engines.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ATLAS = ROOT / "static" / "dore-design" / "italian-editorial-grammars.v1.json"
ARSENAL = ROOT / "dore-design" / "motion-arsenal.v0.json"

RULES = (
    (("wrapper", "uncover", "reveal"), "threshold-opening"),
    (("construction", "assemble"), "architectural-assembly"),
    (("interrupt", "rupture", "disturbance"), "editorial-cut"),
    (("cadence", "return", "continuity"), "page-turn-continuity"),
    (("atmosphere", "trace", "accumulation"), "measured-drift"),
    (("information becomes image", "type", "typograph"), "kinetic-typography"),
    (("evidence", "hierarchy", "persistence"), "ceremonial-reveal"),
)


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def compile_era(era: dict) -> dict:
    arsenal = _load(ARSENAL)
    allowed = {item["id"] for item in arsenal["semantics"]}
    emergence = " ".join(era.get("grammar", {}).get("emergence", []))
    prompt = str(era.get("prompt", {}).get("emergence", ""))
    source = f"{emergence} {prompt}".lower()
    scores: dict[str, int] = {}
    for terms, intent in RULES:
        score = sum(source.count(term) for term in terms)
        if score:
            scores[intent] = scores.get(intent, 0) + score
    intent = sorted(scores.items(), key=lambda pair: (-pair[1], pair[0]))[0][0] if scores else "stillness"
    if intent not in allowed:
        raise ValueError(f"unknown_motion_intent:{intent}")
    return {
        "schema": "dore.italian-editorial-motion-intent.v0",
        "eraId": era["id"],
        "intent": intent,
        "sourceModule": "emergence",
        "sourceLanguage": emergence,
        "engine": None,
        "enginePolicy": "router-selects-lowest-sufficient",
        "authority": False,
    }


def compile_all() -> list[dict]:
    atlas = _load(ATLAS)
    out = []
    for family in atlas.get("families", []):
        for era in family.get("eras", []):
            out.append(compile_era(era))
    return out


if __name__ == "__main__":
    print(json.dumps(compile_all(), ensure_ascii=False, indent=2))
