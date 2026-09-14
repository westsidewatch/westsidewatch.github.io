"""Doré Capability Arsenal v0.

A light meta-capability for discovering the smallest useful capability loadout
without stuffing the whole registry into model context. Beauty is a hard
admission boundary for Westside design work: technically valid but visually
unconvincing output is failure, never a temporary PASS.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REGISTRY = Path(__file__).with_name("capability-registry.v1.json")

BEAUTY_FIRST_SURFACES = {
    "living-water",
    "westside-watch",
    "dawn",
    "one",
    "multiwrite",
}

# This is intentionally semantic and small. It is not a hard-coded Living Water
# loadout: signals expose candidate affordances and discovery chooses from the
# canonical registry at runtime.
SIGNALS = {
    "visual": {"design", "visual", "image", "pixel", "raster", "typography", "layout"},
    "source": {"source", "media", "asset", "reference", "material"},
    "memory": {"memory", "recall", "rejection", "precedent", "history"},
    "context": {"context", "identity", "brand", "relationship", "authority"},
    "publishing": {"book", "publishing", "edition", "epub", "pdf", "cover"},
}


def _registry() -> list[dict[str, Any]]:
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    return [c for c in data.get("capabilities", []) if c.get("status") != "planned"]


def _terms(capability: dict[str, Any]) -> set[str]:
    raw = json.dumps(capability, ensure_ascii=False).lower()
    return {token.strip('.,:;[]{}()\"') for token in raw.replace('-', ' ').replace('_', ' ').split()}


def diagnose(request: dict[str, Any], observation: dict[str, Any] | None = None) -> dict[str, Any]:
    """Describe capability gaps without prescribing named weapons."""
    observation = observation or {}
    text = json.dumps({"request": request, "observation": observation}, ensure_ascii=False).lower()
    needs = []
    for family, words in SIGNALS.items():
        if any(word in text for word in words):
            needs.append(family)

    surface = str(request.get("surface_family") or request.get("consumer") or "")
    beauty_first = surface in BEAUTY_FIRST_SURFACES or bool(request.get("beauty_first"))
    if beauty_first and "visual" not in needs:
        needs.insert(0, "visual")

    failure_domains = list(observation.get("failure_domains") or [])
    if observation.get("beautiful") is False:
        failure_domains.append("aesthetic-admission-failed")
    if observation.get("visual_motivation") is False:
        failure_domains.append("unmotivated-visual-state")

    return {
        "schema": "dore.capability-gap.v0",
        "surface": surface,
        "beauty_first": beauty_first,
        "needed_families": list(dict.fromkeys(needs)),
        "failure_domains": list(dict.fromkeys(failure_domains)),
        "principle": "beauty-is-an-admission-boundary-not-a-late-optimization" if beauty_first else "smallest-sufficient-loadout",
    }


def discover(gap: dict[str, Any], limit: int = 8) -> list[dict[str, Any]]:
    """Retrieve candidate weapons from the canonical registry, deferred by default."""
    families = set(gap.get("needed_families") or [])
    scored: list[tuple[int, dict[str, Any]]] = []
    for capability in _registry():
        terms = _terms(capability)
        score = 0
        for family in families:
            score += len(terms & SIGNALS.get(family, set())) * 3
            if family in terms:
                score += 2
        if gap.get("beauty_first") and capability.get("id") == "design.intelligence":
            score += 8
        if score:
            scored.append((score, capability))
    scored.sort(key=lambda item: (-item[0], item[1].get("id", "")))
    return [
        {
            "id": capability["id"],
            "score": score,
            "service": capability.get("service"),
            "load": capability.get("load", "deferred"),
            "network": capability.get("network"),
        }
        for score, capability in scored[:limit]
    ]


def assemble(gap: dict[str, Any], candidates: list[dict[str, Any]], max_weapons: int = 4) -> dict[str, Any]:
    """Build a minimal set-level loadout; never claim aesthetic success before raster judgment."""
    chosen: list[dict[str, Any]] = []
    covered: set[str] = set()
    registry_by_id = {c["id"]: c for c in _registry()}

    for candidate in candidates:
        capability = registry_by_id.get(candidate["id"], {})
        terms = _terms(capability)
        families = {family for family in gap.get("needed_families", []) if terms & SIGNALS.get(family, set())}
        if not chosen or families - covered:
            chosen.append(candidate)
            covered |= families
        if len(chosen) >= max_weapons:
            break

    unresolved = [family for family in gap.get("needed_families", []) if family not in covered]
    return {
        "schema": "dore.capability-loadout.v0",
        "beauty_first": bool(gap.get("beauty_first")),
        "weapons": chosen,
        "covered_families": sorted(covered),
        "unresolved_families": unresolved,
        "requires_visual_admission": bool(gap.get("beauty_first")),
        "admission_rule": "real-raster-must-be-beautiful-and-visually-motivated" if gap.get("beauty_first") else "task-evidence-required",
    }


def plan(request: dict[str, Any], observation: dict[str, Any] | None = None) -> dict[str, Any]:
    gap = diagnose(request, observation)
    candidates = discover(gap)
    loadout = assemble(gap, candidates)
    return {
        "schema": "dore.capability-arsenal.v0",
        "gap": gap,
        "candidates": candidates,
        "loadout": loadout,
        "evolution_required": bool(loadout["unresolved_families"]),
    }
