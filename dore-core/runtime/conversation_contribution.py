#!/usr/bin/env python3
"""Doré Conversation Alpha grounded-contribution envelope.

Internal-only helper. It validates that a meeting contribution is typed,
evidence-grounded when required, uncertainty-explicit, authority-bounded, and
safe to persist only when the contribution class permits it.
"""
from __future__ import annotations

from typing import Any, Iterable

ALLOWED_TYPES = {
    "evidence",
    "judgment",
    "question",
    "suggestion",
    "risk",
    "decision_candidate",
}
ALLOWED_AUTHORITY = {"A0", "A1", "A2", "A3", "A4"}
PERSISTENCE_ELIGIBLE_TYPES = {"evidence", "risk", "decision_candidate"}


class ContributionError(ValueError):
    """Raised when an internal Alpha contribution violates the contract."""


def _source_ids(context_packet: dict[str, Any]) -> set[str]:
    ids: set[str] = set()
    for source in context_packet.get("sources", []):
        role = source.get("role")
        path = source.get("path")
        if role:
            ids.add(str(role))
        if path:
            ids.add(str(path))
    return ids


def build_contribution(
    *,
    context_packet: dict[str, Any],
    contribution_type: str,
    content: str,
    evidence_refs: Iterable[str] = (),
    uncertainty: str = "none",
    authority_level: str = "A1",
    persistence_requested: bool = False,
) -> dict[str, Any]:
    if context_packet.get("mode") != "INTERNAL_ALPHA_NOT_PUBLIC":
        raise ContributionError("Conversation Alpha contribution requires an internal context packet")
    if not context_packet.get("ready_for_internal_meeting"):
        raise ContributionError("Context packet is not ready for an internal meeting")
    if contribution_type not in ALLOWED_TYPES:
        raise ContributionError(f"Unsupported contribution type: {contribution_type}")
    if authority_level not in ALLOWED_AUTHORITY:
        raise ContributionError(f"Unsupported authority level: {authority_level}")
    if not isinstance(content, str) or not content.strip():
        raise ContributionError("Contribution content must be non-empty")
    if not isinstance(uncertainty, str) or not uncertainty.strip():
        raise ContributionError("Uncertainty must be explicit")

    refs = [str(ref) for ref in evidence_refs]
    available = _source_ids(context_packet)
    unknown = [ref for ref in refs if ref not in available]
    if unknown:
        raise ContributionError(f"Unknown evidence references: {unknown}")

    requires_basis = contribution_type in {"evidence", "judgment", "risk", "decision_candidate"}
    if requires_basis and not refs:
        raise ContributionError(f"{contribution_type} contribution requires at least one evidence reference")

    persistence_eligible = contribution_type in PERSISTENCE_ELIGIBLE_TYPES and uncertainty.lower() not in {
        "speculative",
        "unknown",
        "unverified",
    }
    persistence_allowed = persistence_requested and persistence_eligible

    return {
        "schema_version": 1,
        "mode": "INTERNAL_ALPHA_NOT_PUBLIC",
        "project_id": context_packet.get("project", {}).get("id"),
        "type": contribution_type,
        "content": content.strip(),
        "evidence_refs": refs,
        "uncertainty": uncertainty.strip(),
        "authority_level": authority_level,
        "authority": {
            "doré_role": "advisory_and_evidentiary",
            "human_church_authority_final": True,
            "public_conversation_authorized": False,
        },
        "persistence": {
            "requested": persistence_requested,
            "eligible": persistence_eligible,
            "allowed": persistence_allowed,
            "reason": (
                "eligible_under_alpha_contract"
                if persistence_allowed
                else "not_requested"
                if not persistence_requested
                else "type_or_uncertainty_not_persistence_eligible"
            ),
        },
    }
