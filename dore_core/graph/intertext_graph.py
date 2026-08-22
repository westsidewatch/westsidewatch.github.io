"""Doré intertext graph validator v0.1."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any

ALLOWED_RELATIONS = {
    "explicit_quote", "explicit_citation_formula", "strong_allusion",
    "probable_allusion", "lexical_echo", "thematic_parallel",
    "typological_reading", "traditional_connection",
}
ALLOWED_CLAIM_CLASSES = {
    "TEXT_EXPLICIT", "TEXTUAL_DATA", "SCHOLARLY_INFERENCE",
    "TRADITIONAL_INTERPRETATION", "EDITORIAL_NORMALIZATION",
}

@dataclass
class IntertextValidationReport:
    edges: int = 0
    errors: list[str] | None = None
    warnings: list[str] | None = None
    def __post_init__(self) -> None:
        self.errors = [] if self.errors is None else self.errors
        self.warnings = [] if self.warnings is None else self.warnings
    @property
    def passed(self) -> bool:
        return not self.errors


def validate_intertext_edges(graph: dict[str, Any]) -> IntertextValidationReport:
    report = IntertextValidationReport()
    edges = graph.get("intertext_edges", [])
    report.edges = len(edges)
    ids: set[str] = set()
    for edge in edges:
        eid = edge.get("id")
        if not eid:
            report.errors.append("intertext_missing_id")
            continue
        if eid in ids:
            report.errors.append(f"duplicate_intertext:{eid}")
        ids.add(eid)
        if not edge.get("source_ref") or not edge.get("target_ref"):
            report.errors.append(f"missing_intertext_endpoint:{eid}")
        if edge.get("relation") not in ALLOWED_RELATIONS:
            report.errors.append(f"invalid_intertext_relation:{eid}")
        if edge.get("claim_class") not in ALLOWED_CLAIM_CLASSES:
            report.errors.append(f"invalid_intertext_claim_class:{eid}")
        if not edge.get("provenance"):
            report.errors.append(f"missing_intertext_provenance:{eid}")
        if edge.get("relation") in {"strong_allusion", "probable_allusion", "lexical_echo", "thematic_parallel"} and edge.get("claim_class") == "TEXT_EXPLICIT":
            report.errors.append(f"inference_promoted_to_explicit:{eid}")
        if edge.get("relation") == "traditional_connection" and edge.get("claim_class") != "TRADITIONAL_INTERPRETATION":
            report.errors.append(f"traditional_connection_misclassified:{eid}")
    return report
