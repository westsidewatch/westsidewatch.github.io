#!/usr/bin/env python3
"""Promote only evidence-backed ThresholdStudy patterns into an experimental homepage.

The locked baseline remains byte-for-byte untouched.
Evidence source: NewWestsideEditorialHero.stories.jsx ThresholdStudy differs from
LockedBaseline only by hero minimum height (720 -> 660) and threshold/glow start
(42% -> 54%). No other visual behavior is promoted by this script.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOCKED = ROOT / "dore-design/new-westside/homepage-v2-living-fortress.html"
EXPERIMENT = ROOT / "dore-design/new-westside/homepage-v3-threshold-promoted.html"
EVIDENCE = ROOT / "dore-design/knowledge-lab/evidence/threshold-promotion-2026-09-01.json"
STORY = ROOT / "dore-design/knowledge-lab/storybook/src/stories/NewWestsideEditorialHero.stories.jsx"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

before_hash = sha256(LOCKED)
src = LOCKED.read_text(encoding="utf-8")
story_src = STORY.read_text(encoding="utf-8") if STORY.exists() else ""

checks = {
    "threshold_height_660_present": "alternate?'660px':'720px'" in story_src,
    "threshold_inset_54_present": "alternate ? '0 0 0 54%'" in story_src,
}
if not all(checks.values()):
    raise RuntimeError(f"ThresholdStudy evidence missing: {checks}")

changes = []
old = ".hero{min-height:720px;"
new = ".hero{min-height:660px;"
if old not in src:
    raise RuntimeError("locked hero min-height signature not found")
src = src.replace(old, new, 1)
changes.append({"pattern": "hero_min_height", "from": "720px", "to": "660px", "decision": "PROMOTE"})

old = ".hero-art{position:absolute;inset:0 0 0 42%;"
new = ".hero-art{position:absolute;inset:0 0 0 54%;"
if old not in src:
    raise RuntimeError("locked hero-art threshold signature not found")
src = src.replace(old, new, 1)
changes.append({"pattern": "hero_visual_threshold", "from": "42%", "to": "54%", "decision": "PROMOTE"})

# Mark only the experimental copy; never mutate the locked control.
src = src.replace('data-design="living-fortress-v2" data-revision="real-front-door-02"',
                  'data-design="living-fortress-v3-threshold" data-revision="threshold-promoted-01"', 1)
EXPERIMENT.write_text(src, encoding="utf-8")
after_hash = sha256(LOCKED)

if before_hash != after_hash:
    raise RuntimeError("locked baseline changed unexpectedly")

EVIDENCE.parent.mkdir(parents=True, exist_ok=True)
evidence = {
    "task": "threshold-study-promotion",
    "locked_baseline": str(LOCKED.relative_to(ROOT)),
    "locked_baseline_sha256_before": before_hash,
    "locked_baseline_sha256_after": after_hash,
    "locked_baseline_unchanged": before_hash == after_hash,
    "storybook_evidence_checks": checks,
    "experimental_homepage": str(EXPERIMENT.relative_to(ROOT)),
    "promoted": changes,
    "rejected_or_deferred": [
        "typography changes: not tested by ThresholdStudy",
        "navigation changes: not tested by ThresholdStudy",
        "content/IA changes: not tested by ThresholdStudy",
        "mobile breakpoint changes: not tested by ThresholdStudy",
        "gradient boundary changes: not explicitly tested by ThresholdStudy",
    ],
}
EVIDENCE.write_text(json.dumps(evidence, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(evidence, ensure_ascii=False))
