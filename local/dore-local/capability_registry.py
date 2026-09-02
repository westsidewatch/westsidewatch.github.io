#!/usr/bin/env python3
"""Thin capability discovery for Doré.

This module never executes or replaces Doré Search/Conversation. It reads a
small registry and returns objective capability metadata so Agent Core can
load native capabilities only when needed.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "dore-design/knowledge-lab/capabilities/registry.json"


def load_registry(path: Path = REGISTRY) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema") != "dore.capability-registry.v1":
        raise ValueError("unsupported capability registry schema")
    return data


def discover(*, capability_type: str | None = None, service: str | None = None,
             include_planned: bool = False) -> list[dict[str, Any]]:
    items = load_registry().get("capabilities", [])
    found = []
    for item in items:
        if not include_planned and item.get("status") != "existing":
            continue
        if capability_type and item.get("type") != capability_type:
            continue
        if service and item.get("service") != service:
            continue
        found.append(item)
    return found


def get(capability_id: str, *, include_planned: bool = False) -> dict[str, Any] | None:
    for item in discover(include_planned=include_planned):
        if item.get("id") == capability_id:
            return item
    return None


if __name__ == "__main__":
    print(json.dumps(discover(include_planned=True), ensure_ascii=False, indent=2))
