#!/usr/bin/env python3
"""Score candidate Camera Spines without letting cheapness erase cinema.

This is a planning-layer tool, not a renderer. It combines narrative intent with
measured/predicted World Demand so script and camera design can compare multiple
spines before purchasing hidden world.

Input JSON:
{
  "candidates": [
    {
      "id": "detail-reveal-wide",
      "narrative_value": 0.95,
      "reveal_value": 0.90,
      "rhythm_value": 0.80,
      "world_demand_fraction": 0.18,
      "avoidable_fraction": 0.25,
      "wide_scene_required": true
    }
  ]
}

All values are normalized to [0,1]. `avoidable_fraction` expresses how much of
World Demand could plausibly be avoided without damaging the shot's narrative
intention. A required wide shot therefore may have high demand but low avoidable
cost.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def clamp01(v):
    return max(0.0, min(1.0, float(v)))


def score_candidate(c):
    narrative = clamp01(c.get("narrative_value", 0.0))
    reveal = clamp01(c.get("reveal_value", 0.0))
    rhythm = clamp01(c.get("rhythm_value", 0.0))
    demand = clamp01(c.get("world_demand_fraction", 0.0))
    avoidable = clamp01(c.get("avoidable_fraction", 1.0))
    required_wide = bool(c.get("wide_scene_required", False))

    # Only avoidable demand is penalized. This is the central protection against
    # turning the film into a sequence of cheap occlusion tricks.
    avoidable_world_cost = demand * avoidable

    # High narrative value and intentionally required spectacle further cap the
    # penalty; expensive world is acceptable when the story earns it.
    if required_wide:
        avoidable_world_cost *= 0.35
    if narrative >= 0.90:
        avoidable_world_cost *= 0.70

    # Narrative remains dominant, then reveal, then rhythm. World cost can choose
    # between similarly strong shots but should not overrule a necessary scene.
    score = (
        0.50 * narrative
        + 0.28 * reveal
        + 0.22 * rhythm
        - 0.35 * avoidable_world_cost
    )

    out = dict(c)
    out.update({
        "narrative_value": narrative,
        "reveal_value": reveal,
        "rhythm_value": rhythm,
        "world_demand_fraction": demand,
        "avoidable_fraction": avoidable,
        "avoidable_world_cost": avoidable_world_cost,
        "camera_world_score": score,
    })
    return out


def rank_candidates(payload):
    ranked = [score_candidate(c) for c in payload.get("candidates", [])]
    ranked.sort(key=lambda x: (-x["camera_world_score"], x.get("id", "")))
    for i, item in enumerate(ranked, 1):
        item["rank"] = i
    return ranked


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", type=Path, required=True)
    ap.add_argument("--output", type=Path)
    a = ap.parse_args()

    payload = json.loads(a.input.read_text(encoding="utf-8"))
    ranked = rank_candidates(payload)
    result = {
        "status": "CAMERA_WORLD_SCORE_READY",
        "formula": "Narrative + Reveal + Rhythm - Avoidable World Cost",
        "candidates": ranked,
    }
    text = json.dumps(result, indent=2) + "\n"
    if a.output:
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
