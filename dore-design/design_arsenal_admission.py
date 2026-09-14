#!/usr/bin/env python3
"""Doré Design Arsenal admission v0.

Exploration may discover tools, methods, grammars or architectures. Nothing is
allowed to remain as chat-only inspiration. Every finding is routed into one of
four explicit absorption modes: assimilate, learn, mount, defer.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

LEDGER = Path(__file__).with_name("design_arsenal_assimilation.v0.json")
ALLOWED_MODES = {"assimilate", "learn", "mount", "defer"}
CANONICAL_VISUAL_AUTHORITY = {"westside-canon", "surface-identity", "authored-content"}


def ledger() -> dict[str, Any]:
    data = json.loads(LEDGER.read_text(encoding="utf-8"))
    if data.get("schema") != "dore.design-arsenal-assimilation.v0":
        raise ValueError("design_arsenal_schema_mismatch")
    return data


def validate(data: dict[str, Any] | None = None) -> dict[str, Any]:
    data = data or ledger()
    findings = data.get("findings") or []
    ids: set[str] = set()
    targets: set[str] = set()
    errors: list[str] = []
    modes: dict[str, int] = {mode: 0 for mode in ALLOWED_MODES}

    for item in findings:
        item_id = str(item.get("id") or "")
        mode = str(item.get("mode") or "")
        target = str(item.get("target") or "")
        if not item_id:
            errors.append("finding_missing_id")
        elif item_id in ids:
            errors.append(f"duplicate_id:{item_id}")
        ids.add(item_id)
        if mode not in ALLOWED_MODES:
            errors.append(f"invalid_mode:{item_id}:{mode}")
        else:
            modes[mode] += 1
        if mode != "defer" and not target:
            errors.append(f"missing_target:{item_id}")
        if mode == "defer" and not item.get("reconsider_when"):
            errors.append(f"defer_without_trigger:{item_id}")
        if not item.get("why"):
            errors.append(f"missing_why:{item_id}")
        if target:
            targets.add(target)

    if not findings:
        errors.append("empty_ledger")
    if any(str(item.get("mode")) == "chat-only" for item in findings):
        errors.append("chat_only_result_forbidden")

    return {
        "schema": "dore.design-arsenal-admission-report.v0",
        "ok": not errors,
        "findings": len(findings),
        "modes": modes,
        "targets": sorted(targets),
        "errors": errors,
        "first_real_consumer": data.get("first_real_consumer"),
        "promotion_rule": data.get("promotion_rule"),
    }


def plan_for(target: str, data: dict[str, Any] | None = None) -> dict[str, Any]:
    data = data or ledger()
    selected = [item for item in data.get("findings", []) if item.get("target") == target]
    return {
        "schema": "dore.design-arsenal-target-plan.v0",
        "target": target,
        "findings": selected,
        "absorption_order": ["assimilate", "learn", "mount", "defer"],
        "authority": sorted(CANONICAL_VISUAL_AUTHORITY),
        "rule": "deterministic facts are solved; aesthetic and contextual judgment remains Doré/Westside authority",
    }


if __name__ == "__main__":
    report = validate()
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(0 if report["ok"] else 1)
