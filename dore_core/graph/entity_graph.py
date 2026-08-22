"""Doré biblical entity graph foundation validator v0.1."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any

ALLOWED_CLAIM_CLASSES = {
    "TEXT_EXPLICIT", "TEXTUAL_DATA", "SCHOLARLY_INFERENCE",
    "TRADITIONAL_INTERPRETATION", "EDITORIAL_NORMALIZATION",
}

ALLOWED_ENTITY_TYPES = {
    "person", "place", "people_group", "kingdom_or_polity", "office_or_role",
    "event", "artifact_or_object", "institution", "genealogical_line",
}

@dataclass
class GraphValidationReport:
    entities: int = 0
    claims: int = 0
    errors: list[str] | None = None
    warnings: list[str] | None = None

    def __post_init__(self) -> None:
        self.errors = [] if self.errors is None else self.errors
        self.warnings = [] if self.warnings is None else self.warnings

    @property
    def passed(self) -> bool:
        return not self.errors


def validate_graph(graph: dict[str, Any]) -> GraphValidationReport:
    report = GraphValidationReport()
    entities = graph.get("entities", [])
    claims = graph.get("claims", [])
    report.entities = len(entities)
    report.claims = len(claims)

    entity_ids: set[str] = set()
    for entity in entities:
        eid = entity.get("id")
        if not eid:
            report.errors.append("entity_missing_id")
            continue
        if eid in entity_ids:
            report.errors.append(f"duplicate_entity:{eid}")
        entity_ids.add(eid)
        if entity.get("type") not in ALLOWED_ENTITY_TYPES:
            report.errors.append(f"invalid_entity_type:{eid}")
        if not entity.get("preferred_label"):
            report.errors.append(f"missing_preferred_label:{eid}")
        if not entity.get("attestations"):
            report.errors.append(f"missing_attestation:{eid}")

    claim_ids: set[str] = set()
    for claim in claims:
        cid = claim.get("id")
        if not cid:
            report.errors.append("claim_missing_id")
            continue
        if cid in claim_ids:
            report.errors.append(f"duplicate_claim:{cid}")
        claim_ids.add(cid)
        subject = claim.get("subject_id")
        obj = claim.get("object_id")
        if subject not in entity_ids:
            report.errors.append(f"unknown_subject:{cid}:{subject}")
        if obj is not None and obj not in entity_ids:
            report.errors.append(f"unknown_object:{cid}:{obj}")
        if claim.get("claim_class") not in ALLOWED_CLAIM_CLASSES:
            report.errors.append(f"invalid_claim_class:{cid}")
        if not claim.get("references"):
            report.errors.append(f"missing_references:{cid}")
        if not claim.get("provenance"):
            report.errors.append(f"missing_provenance:{cid}")
        if obj is None and claim.get("literal_value") is None:
            report.errors.append(f"claim_without_object_or_value:{cid}")

    return report
