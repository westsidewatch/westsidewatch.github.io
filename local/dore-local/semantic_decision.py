#!/usr/bin/env python3
"""Minimal semantic decision seam for Doré.

This module does not create another agent loop. It is invoked only when the
existing deterministic runtime cannot select the next action. It reuses an
injected local inference callable and returns one bounded decision for the
existing capability registry / A2A execution plane.
"""
from __future__ import annotations

from typing import Any, Callable

ALLOWED_ACTIONS = {
    "INVOKE",
    "RESEARCH",
    "ASK_HUMAN",
    "REQUIRE_APPROVAL",
    "WAIT",
    "FINISH",
}

DECISION_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "action": {"type": "string", "enum": sorted(ALLOWED_ACTIONS)},
        "capability_id": {"type": ["string", "null"]},
        "arguments": {"type": "object"},
        "reason": {"type": "string"},
        "evidence_refs": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["action", "capability_id", "arguments", "reason", "evidence_refs"],
    "additionalProperties": False,
}


def decide_next(
    *,
    goal: str,
    state: dict[str, Any],
    evidence: list[dict[str, Any]],
    capabilities: list[dict[str, Any]],
    infer: Callable[..., dict[str, Any]],
) -> dict[str, Any]:
    """Return one semantic next-action decision; never execute it here."""
    if not goal.strip():
        raise ValueError("goal_required")

    capability_ids = {
        str(item.get("id"))
        for item in capabilities
        if isinstance(item, dict) and item.get("id")
    }
    messages = [
        {
            "role": "system",
            "content": (
                "You are Doré's bounded semantic decision capability. "
                "The deterministic runtime has already declined to choose the next step. "
                "Choose exactly one next action toward the stated goal. "
                "Do not execute tools. Do not invent capability IDs. "
                "Prefer existing capabilities and evidence. Ask for human input or approval "
                "when authority, missing facts, or consequential action requires it."
            ),
        },
        {
            "role": "user",
            "content": {
                "goal": goal,
                "state": state,
                "evidence": evidence,
                "available_capabilities": capabilities,
            },
        },
    ]

    decision = infer(messages=messages, schema=DECISION_SCHEMA)
    if not isinstance(decision, dict):
        raise ValueError("decision_not_object")

    action = str(decision.get("action") or "")
    if action not in ALLOWED_ACTIONS:
        raise ValueError("decision_action_invalid")

    capability_id = decision.get("capability_id")
    if action == "INVOKE":
        if not capability_id or str(capability_id) not in capability_ids:
            raise ValueError("decision_capability_not_available")
    elif capability_id is not None:
        raise ValueError("decision_capability_only_valid_for_invoke")

    return {
        "schema": "dore.semantic-decision.v0",
        "action": action,
        "capability_id": str(capability_id) if capability_id is not None else None,
        "arguments": dict(decision.get("arguments") or {}),
        "reason": str(decision.get("reason") or ""),
        "evidence_refs": [str(x) for x in decision.get("evidence_refs") or []],
    }
