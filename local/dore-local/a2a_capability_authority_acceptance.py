#!/usr/bin/env python3
"""Acceptance for 1C/1: canonical capability authority + execution bindings."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load(name: str):
    path = HERE / f"{name}.py"
    spec = importlib.util.spec_from_file_location(f"dore_test_{name}", path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


registry = load("capability_registry")
bindings = load("capability_bindings")
production = load("production_actions")
bus = load("capability_bus")
items = registry.discover(include_planned=True)
by_id = {item["id"]: item for item in items}
validation = bindings.validate_authority(items)

expected_bound = {
    "image.generate",
    "context.fuzzy-search",
    "bible.query-plan",
    "knowledge.recall",
    "reflex.project",
    "translation.project",
    "publishing.book-intelligence",
    *production.CAPABILITIES,
}

bus_items = bus.discover(production, include_planned=True)
bus_by_id = {item["id"]: item for item in bus_items}
canonical_ids = set(by_id)

checks = {
    "bindings_have_canonical_identity": validation["ok"],
    "all_current_bus_bindings_present": expected_bound <= bindings.callable_ids(),
    "production_actions_are_bindings_not_identity": set(production.CAPABILITIES) <= bindings.callable_ids(),
    "formerly_native_ids_are_canonical": all(cap in by_id for cap in {"image.generate", "context.fuzzy-search", "bible.query-plan", "knowledge.recall"}),
    "canonical_owner_is_core": registry.load_registry().get("owner") == "dore-core",
    "binding_descriptors_point_to_binding_layer": all(by_id[cap].get("binding") == "capability-bindings" for cap in expected_bound),
    "bus_identity_set_equals_canonical_registry": set(bus_by_id) == canonical_ids,
    "bus_callability_comes_only_from_bindings": all(bool(bus_by_id[cap].get("callable")) == (cap in bindings.callable_ids()) for cap in canonical_ids),
    "legacy_native_descriptor_authority_removed": not hasattr(bus, "NATIVE_CAPABILITIES"),
    "production_capability_list_cannot_create_identity": all(cap in canonical_ids for cap in production.CAPABILITIES),
}

ok = all(checks.values())
print(json.dumps({
    "ok": ok,
    "code": "DORE_A2A_CAPABILITY_AUTHORITY_PASS" if ok else "DORE_A2A_CAPABILITY_AUTHORITY_FAIL",
    "checks": checks,
    "canonical_count": len(by_id),
    "bus_identity_count": len(bus_by_id),
    "binding_count": len(bindings.callable_ids()),
    "bindings_without_canonical_identity": validation["bindings_without_canonical_identity"],
}, ensure_ascii=False, indent=2))
raise SystemExit(0 if ok else 1)
