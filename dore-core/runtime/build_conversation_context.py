#!/usr/bin/env python3
"""Build a bounded internal Doré Conversation Alpha context packet.

This is an internal runtime helper. It does not expose a public API or UI.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
RUNTIME_STATE = ROOT / "dore-core/runtime/project-execution-state.json"
MASTER_REGISTER = ROOT / "dore-core/projects/DORÉ-MASTER-WORK-REGISTER.md"
CONSTITUTION = ROOT / "dore-core/constitution/CONSTITUTION.md"
ALPHA_CONTRACT = ROOT / "dore-core/runtime/conversation-alpha-contract.md"
MEETINGS_ROOT = ROOT / "dore-core/runtime/meetings"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_record(path: Path, role: str, required: bool = True) -> dict[str, Any]:
    if not path.exists():
        return {
            "role": role,
            "path": str(path.relative_to(ROOT)),
            "required": required,
            "status": "missing",
        }
    return {
        "role": role,
        "path": str(path.relative_to(ROOT)),
        "required": required,
        "status": "loaded",
        "sha256": digest(path),
        "bytes": path.stat().st_size,
    }


def load_prior_meeting(project_id: str) -> tuple[dict[str, Any] | None, dict[str, Any]]:
    latest = MEETINGS_ROOT / project_id / "latest.json"
    source = source_record(latest, "prior_meeting_record", required=False)
    if not latest.exists():
        return None, source
    try:
        record = json.loads(read_text(latest))
    except (OSError, json.JSONDecodeError) as exc:
        source["status"] = "invalid"
        source["error"] = type(exc).__name__
        return None, source
    if record.get("mode") != "INTERNAL_ALPHA_NOT_PUBLIC" or record.get("project_id") != project_id:
        source["status"] = "invalid"
        source["error"] = "meeting_record_scope_mismatch"
        return None, source
    if record.get("authority", {}).get("public_conversation_authorized") is not False:
        source["status"] = "invalid"
        source["error"] = "public_conversation_authority_violation"
        return None, source
    return record, source


def build_packet(project_id: str | None = None) -> dict[str, Any]:
    state = json.loads(read_text(RUNTIME_STATE))
    active = state.get("active_project") or {}
    active_id = active.get("id")
    requested = project_id or active_id
    if not requested:
        raise SystemExit("No active project and no --project-id supplied")
    if requested != active_id:
        raise SystemExit(
            f"Internal Alpha currently supports the persisted active project only: "
            f"requested={requested!r}, active={active_id!r}"
        )

    brief_rel = active.get("brief")
    brief_path = ROOT / brief_rel if brief_rel else None
    prior_meeting, prior_meeting_source = load_prior_meeting(requested)

    sources = [
        source_record(MASTER_REGISTER, "canonical_work_map"),
        source_record(RUNTIME_STATE, "persistent_runtime_state"),
        source_record(CONSTITUTION, "authority_and_identity"),
        source_record(ALPHA_CONTRACT, "conversation_alpha_contract"),
    ]
    if brief_path:
        sources.append(source_record(brief_path, "active_project_brief"))
    else:
        sources.append({"role": "active_project_brief", "required": True, "status": "missing", "path": None})
    sources.append(prior_meeting_source)

    missing_required = [s for s in sources if s.get("required") and s.get("status") != "loaded"]

    meeting_memory = None
    if prior_meeting:
        meeting_memory = {
            "project_id": prior_meeting.get("project_id"),
            "closed_at": prior_meeting.get("closed_at"),
            "project_state_at_close": prior_meeting.get("project_state_at_close"),
            "durable_contributions": prior_meeting.get("durable_contributions", []),
            "verified_learning": prior_meeting.get("verified_learning", []),
            "unresolved_blockers": prior_meeting.get("unresolved_blockers", []),
            "next_actions": prior_meeting.get("next_actions", []),
            "authority": prior_meeting.get("authority", {}),
        }

    packet = {
        "schema_version": 2,
        "mode": "INTERNAL_ALPHA_NOT_PUBLIC",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "project": {
            "id": active_id,
            "state": active.get("state"),
            "objective": active.get("objective"),
            "next_action": active.get("next_action"),
            "blocker": active.get("blocker"),
            "terminal_states": active.get("terminal_states", []),
            "checkpoint": active.get("checkpoint"),
        },
        "authority": {
            "doré_role": "advisory_and_evidentiary",
            "human_church_authority_final": True,
            "public_conversation_authorized": False,
            "rules": [
                "tool_access_is_not_authority",
                "suggestion_is_not_permission",
                "consequential_promotion_or_action_requires_appropriate_human_authority",
                "uncertainty_and_missing_evidence_must_remain_visible",
            ],
        },
        "contribution_contract": {
            "allowed_types": ["evidence", "judgment", "question", "suggestion", "risk", "decision_candidate"],
            "project_fact_claims_require_source_basis": True,
            "speculation_must_not_be_persisted_as_fact": True,
        },
        "meeting_memory": meeting_memory,
        "sources": sources,
        "missing_evidence": missing_required,
        "ready_for_internal_meeting": not missing_required,
    }
    return packet


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-id")
    parser.add_argument("--output")
    args = parser.parse_args()
    packet = build_packet(args.project_id)
    rendered = json.dumps(packet, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        out = Path(args.output)
        if not out.is_absolute():
            out = ROOT / out
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
