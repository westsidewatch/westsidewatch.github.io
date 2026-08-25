#!/usr/bin/env python3
"""Doré Conversation Alpha meeting-close record builder.

Internal-only. Produces compact durable records from a ready context packet and
validated contribution envelopes. It does not publish conversation surfaces or
execute consequential decisions.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


class MeetingCloseError(ValueError):
    """Raised when a meeting-close record violates the Alpha contract."""


def build_meeting_record(
    *,
    context_packet: dict[str, Any],
    contributions: Iterable[dict[str, Any]],
    changed_constraints: Iterable[str] = (),
    verified_learning: Iterable[str] = (),
    unresolved_blockers: Iterable[str] = (),
    next_actions: Iterable[str] = (),
) -> dict[str, Any]:
    if context_packet.get("mode") != "INTERNAL_ALPHA_NOT_PUBLIC":
        raise MeetingCloseError("Meeting close requires an internal Alpha context packet")
    if not context_packet.get("ready_for_internal_meeting"):
        raise MeetingCloseError("Meeting context is not ready")
    if context_packet.get("authority", {}).get("public_conversation_authorized") is not False:
        raise MeetingCloseError("Public conversation must remain unauthorized")

    durable = []
    rejected = []
    for item in contributions:
        if item.get("mode") != "INTERNAL_ALPHA_NOT_PUBLIC":
            rejected.append({"type": item.get("type"), "reason": "non_internal_contribution"})
            continue
        if item.get("project_id") != context_packet.get("project", {}).get("id"):
            rejected.append({"type": item.get("type"), "reason": "project_mismatch"})
            continue
        if item.get("authority", {}).get("human_church_authority_final") is not True:
            rejected.append({"type": item.get("type"), "reason": "authority_boundary_missing"})
            continue
        if item.get("persistence", {}).get("allowed") is not True:
            rejected.append({"type": item.get("type"), "reason": "not_persistence_allowed"})
            continue
        durable.append(
            {
                "type": item.get("type"),
                "content": item.get("content"),
                "evidence_refs": item.get("evidence_refs", []),
                "uncertainty": item.get("uncertainty"),
                "authority_level": item.get("authority_level"),
            }
        )

    record = {
        "schema_version": 1,
        "mode": "INTERNAL_ALPHA_NOT_PUBLIC",
        "closed_at": datetime.now(timezone.utc).isoformat(),
        "project_id": context_packet.get("project", {}).get("id"),
        "project_state_at_close": context_packet.get("project", {}).get("state"),
        "authority": {
            "doré_role": "advisory_and_evidentiary",
            "human_church_authority_final": True,
            "public_conversation_authorized": False,
            "consequential_action_authorized_by_record": False,
        },
        "durable_contributions": durable,
        "rejected_transient_or_unsafe": rejected,
        "changed_constraints": [str(x).strip() for x in changed_constraints if str(x).strip()],
        "verified_learning": [str(x).strip() for x in verified_learning if str(x).strip()],
        "unresolved_blockers": [str(x).strip() for x in unresolved_blockers if str(x).strip()],
        "next_actions": [str(x).strip() for x in next_actions if str(x).strip()],
    }
    return record


def persist_meeting_record(record: dict[str, Any], output: Path) -> Path:
    if record.get("mode") != "INTERNAL_ALPHA_NOT_PUBLIC":
        raise MeetingCloseError("Refusing to persist a non-internal meeting record")
    if record.get("authority", {}).get("consequential_action_authorized_by_record") is not False:
        raise MeetingCloseError("Meeting record cannot authorize consequential action")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return output
