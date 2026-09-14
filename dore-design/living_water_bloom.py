#!/usr/bin/env python3
"""Policy adapter for the Living Water / 讓教會開花 design experiment.

This is not a transport. It only enriches design.intelligence requests with a
bounded experiment contract while preserving canonical church authority.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path

CONTRACT_PATH = Path(__file__).with_name("living_water_bloom_round1.v1.json")
EXPERIMENT_ID = "living-water-bloom"


def contract() -> dict:
    data = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    if data.get("experiment_id") != EXPERIMENT_ID:
        raise ValueError("living_water_bloom_contract_mismatch")
    return data


def applies(payload: dict) -> bool:
    return (
        str(payload.get("surface_family") or "") == "living-water"
        and str(payload.get("experiment_id") or "") == EXPERIMENT_ID
    )


def enrich(payload: dict) -> dict:
    if not applies(payload):
        return copy.deepcopy(payload)
    spec = contract()
    out = copy.deepcopy(payload)
    constraints = [str(x) for x in (out.get("constraints") or [])]
    required = [
        "preserve canonical Living Water identity, authored content, real relationships, ministry structure, and theological boundaries",
        "historical Living Water designs are evidence only and must never be treated as templates",
        "generate materially different compositions rather than palette or spacing variants",
        "do not invent ministries, people, doctrine, events, or church claims",
        "judge real browser pixels before design rationale",
        "record rejected directions into failure-domain memory and use them as negative precedent",
        "do not mutate canonical workspace",
        "do not promote any candidate to production",
    ]
    for item in required:
        if item not in constraints:
            constraints.append(item)
    out["constraints"] = constraints
    out["experiment_contract"] = spec
    out["divergence_domains"] = list(spec["exploration"]["directions"])
    out["known_failure_domains"] = list(spec["rejection_memory"]["failure_domains"])
    out["historical_design_authority"] = False
    out["production_promotion_allowed"] = False
    out["canonical_workspace_mutation_allowed"] = False
    return out
