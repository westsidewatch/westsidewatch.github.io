#!/usr/bin/env python3
"""Execution bindings for canonical Doré capabilities.

Identity lives only in dore-core/runtime/capability-registry.v1.json. This module
contains no semantic capability descriptors; it only binds canonical IDs to local
execution handlers/classes.
"""
from __future__ import annotations

from typing import Any

BINDINGS: dict[str, dict[str, Any]] = {
    "image.generate": {"kind": "native", "handler": "image.generate"},
    "context.fuzzy-search": {"kind": "native", "handler": "context.fuzzy-search"},
    "bible.query-plan": {"kind": "native", "handler": "bible.query-plan"},
    "knowledge.recall": {"kind": "native", "handler": "knowledge.recall"},
    "reflex.project": {"kind": "native", "handler": "reflex.project"},
    "translation.project": {"kind": "native", "handler": "translation.project"},
    "publishing.book-intelligence": {"kind": "native", "handler": "publishing.book-intelligence"},
    "publishing.dimensional-writing": {"kind": "native", "handler": "publishing.dimensional-writing"},
    "design.intelligence": {"kind": "native", "handler": "design.intelligence"},
    "design.production.rollout": {"kind": "production-action", "handler": "production_actions.execute"},
    "search.local.repair": {"kind": "production-action", "handler": "production_actions.execute"},
    "image.local.repair": {"kind": "production-action", "handler": "production_actions.execute"},
    "wake.runtime.install": {"kind": "production-action", "handler": "production_actions.execute"},
    "core.substrate.acceptance": {"kind": "production-action", "handler": "production_actions.execute"},
    "knowledge.substrates.install": {"kind": "production-action", "handler": "production_actions.execute"},
    "search.production.index": {"kind": "production-action", "handler": "production_actions.execute"},
}


def get(capability_id: str) -> dict[str, Any] | None:
    binding = BINDINGS.get(str(capability_id))
    return dict(binding) if binding else None


def callable_ids() -> set[str]:
    return set(BINDINGS)


def validate_authority(registry_items: list[dict[str, Any]]) -> dict[str, Any]:
    canonical = {str(item.get("id")) for item in registry_items if item.get("id")}
    bound = callable_ids()
    missing = sorted(bound - canonical)
    return {
        "ok": not missing,
        "canonical_count": len(canonical),
        "binding_count": len(bound),
        "bindings_without_canonical_identity": missing,
    }
