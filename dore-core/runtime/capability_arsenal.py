"""Doré Capability Arsenal v0.

A light meta-capability for discovering the smallest useful capability loadout
without stuffing the whole registry into model context. Beauty is a hard
admission boundary for Westside design work.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REGISTRY = Path(__file__).with_name("capability-registry.v1.json")

BEAUTY_FIRST_SURFACES = {"living-water", "westside-watch", "dawn", "one", "multiwrite"}

SIGNALS = {
    "visual": {"design", "visual", "image", "pixel", "raster", "typography", "layout"},
    "source": {"source", "media", "asset", "reference", "material"},
    "memory": {"memory", "recall", "rejection", "precedent", "history"},
    "context": {"context", "identity", "brand", "relationship", "authority"},
    "publishing": {"book", "publishing", "edition", "epub", "pdf", "cover"},
}

# A beautiful visual task needs complementary roles, not one overloaded tool.
# The roles are generic Core affordances; no product-specific weapon IDs are
# prescribed here.
ROLE_RULES = {
    "visual-reasoning": lambda c, t: c.get("type") == "reasoning" and (c.get("service") == "design" or bool(t & SIGNALS["visual"])),
    "visual-materialization": lambda c, t: c.get("type") == "production" and (c.get("service") == "visual" or "image" in t),
    "identity-context": lambda c, t: c.get("type") == "context" or ("context" in t and "identity" in t),
    "experience-memory": lambda c, t: c.get("service") == "memory" or ("memory" in t and "recall" in t),
    "source-discovery": lambda c, t: c.get("type") == "discovery" or c.get("service") == "source-intelligence",
    "publishing-production": lambda c, t: c.get("service") == "publishing" and c.get("type") == "production",
}


def _registry() -> list[dict[str, Any]]:
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    return [c for c in data.get("capabilities", []) if c.get("status") != "planned" and c.get("id") != "core.capability-arsenal"]


def _terms(capability: dict[str, Any]) -> set[str]:
    raw = json.dumps(capability, ensure_ascii=False).lower()
    return {token.strip('.,:;[]{}()\"') for token in raw.replace('-', ' ').replace('_', ' ').split()}


def _roles_for(capability: dict[str, Any]) -> set[str]:
    terms = _terms(capability)
    return {role for role, predicate in ROLE_RULES.items() if predicate(capability, terms)}


def diagnose(request: dict[str, Any], observation: dict[str, Any] | None = None) -> dict[str, Any]:
    """Describe capability gaps without prescribing named weapons."""
    observation = observation or {}
    text = json.dumps({"request": request, "observation": observation}, ensure_ascii=False).lower()
    families = [family for family, words in SIGNALS.items() if any(word in text for word in words)]

    surface = str(request.get("surface_family") or request.get("consumer") or "")
    beauty_first = surface in BEAUTY_FIRST_SURFACES or bool(request.get("beauty_first"))
    roles: list[str] = []
    if beauty_first:
        families = list(dict.fromkeys(["visual", "context", "memory", *families]))
        roles.extend(["visual-reasoning", "visual-materialization", "identity-context", "experience-memory"])
    if "source" in families:
        roles.append("source-discovery")
    if "publishing" in families:
        roles.append("publishing-production")

    failure_domains = list(observation.get("failure_domains") or [])
    if observation.get("beautiful") is False:
        failure_domains.append("aesthetic-admission-failed")
    if observation.get("visual_motivation") is False:
        failure_domains.append("unmotivated-visual-state")

    return {
        "schema": "dore.capability-gap.v0",
        "surface": surface,
        "beauty_first": beauty_first,
        "needed_families": list(dict.fromkeys(families)),
        "needed_roles": list(dict.fromkeys(roles)),
        "failure_domains": list(dict.fromkeys(failure_domains)),
        "principle": "beauty-is-an-admission-boundary-not-a-late-optimization" if beauty_first else "smallest-sufficient-loadout",
    }


def discover(gap: dict[str, Any], limit: int = 12) -> list[dict[str, Any]]:
    """Retrieve candidate weapons and expose which roles each can actually fill."""
    families = set(gap.get("needed_families") or [])
    needed_roles = set(gap.get("needed_roles") or [])
    scored: list[tuple[int, dict[str, Any], set[str]]] = []
    for capability in _registry():
        terms = _terms(capability)
        roles = _roles_for(capability) & needed_roles
        score = len(roles) * 12
        for family in families:
            score += len(terms & SIGNALS.get(family, set())) * 2
        if score:
            scored.append((score, capability, roles))
    scored.sort(key=lambda item: (-item[0], item[1].get("id", "")))
    return [
        {
            "id": capability["id"],
            "score": score,
            "roles": sorted(roles),
            "service": capability.get("service"),
            "type": capability.get("type"),
            "load": capability.get("load", "deferred"),
            "network": capability.get("network"),
        }
        for score, capability, roles in scored[:limit]
    ]


def assemble(gap: dict[str, Any], candidates: list[dict[str, Any]], max_weapons: int = 6) -> dict[str, Any]:
    """Choose complementary weapons by role, not merely the highest-ranked tool."""
    chosen: list[dict[str, Any]] = []
    covered_roles: set[str] = set()
    needed_roles = list(gap.get("needed_roles") or [])

    for candidate in candidates:
        roles = set(candidate.get("roles") or [])
        if roles - covered_roles:
            chosen.append(candidate)
            covered_roles |= roles
        if len(chosen) >= max_weapons or all(role in covered_roles for role in needed_roles):
            break

    unresolved = [role for role in needed_roles if role not in covered_roles]
    return {
        "schema": "dore.capability-loadout.v0",
        "beauty_first": bool(gap.get("beauty_first")),
        "weapons": chosen,
        "covered_roles": sorted(covered_roles),
        "unresolved_roles": unresolved,
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
        "evolution_required": bool(loadout["unresolved_roles"]),
    }
