"""Doré universal language and textual intelligence core."""
from .base import TextWitness, LanguageUnit, AdapterCapabilities, LanguageAdapter, validate_units
from .registry import LanguageRegistry
from .alignment import (
    AlignedWitnessUnit,
    AlignmentCluster,
    AuditException,
    CorpusAuditReport,
    build_alignment_clusters,
    audit_alignment,
)

__all__ = [
    "TextWitness", "LanguageUnit", "AdapterCapabilities", "LanguageAdapter",
    "validate_units", "LanguageRegistry",
    "AlignedWitnessUnit", "AlignmentCluster", "AuditException", "CorpusAuditReport",
    "build_alignment_clusters", "audit_alignment",
]
