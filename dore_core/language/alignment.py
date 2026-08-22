"""Cross-witness canonical alignment and corpus audit primitives for Doré."""
from __future__ import annotations
from dataclasses import dataclass, field
from collections import defaultdict
from typing import Iterable

from .base import LanguageUnit, TextWitness


@dataclass(frozen=True)
class AlignedWitnessUnit:
    witness_id: str
    language: str
    edition: str
    canonical_ref_id: str
    surface: str
    normalized: str | None
    provenance: tuple[str, ...]


@dataclass(frozen=True)
class AlignmentCluster:
    canonical_ref_id: str
    witnesses: tuple[AlignedWitnessUnit, ...]

    @property
    def witness_ids(self) -> tuple[str, ...]:
        return tuple(item.witness_id for item in self.witnesses)


@dataclass(frozen=True)
class AuditException:
    code: str
    canonical_ref_id: str | None
    witness_id: str | None
    detail: str


@dataclass
class CorpusAuditReport:
    expected_witnesses: tuple[str, ...]
    canonical_refs: int = 0
    aligned_units: int = 0
    complete_refs: int = 0
    incomplete_refs: int = 0
    exceptions: list[AuditException] = field(default_factory=list)

    @property
    def status(self) -> str:
        return "PASS" if not self.exceptions else "REVIEW"

    def to_dict(self) -> dict:
        return {
            "schema": "dore.cross-witness-audit.v0.1",
            "expected_witnesses": list(self.expected_witnesses),
            "canonical_refs": self.canonical_refs,
            "aligned_units": self.aligned_units,
            "complete_refs": self.complete_refs,
            "incomplete_refs": self.incomplete_refs,
            "exceptions": [e.__dict__ for e in self.exceptions],
            "status": self.status,
        }


def build_alignment_clusters(
    witness_units: dict[str, Iterable[LanguageUnit]],
    witnesses: dict[str, TextWitness],
) -> list[AlignmentCluster]:
    """Group distinct textual witnesses around stable canonical reference IDs.

    Witness identity is preserved. Text from one edition is never substituted for
    another. Units without canonical IDs are excluded from alignment and should
    be surfaced by ``audit_alignment``.
    """
    grouped: dict[str, list[AlignedWitnessUnit]] = defaultdict(list)
    for witness_id, units in witness_units.items():
        witness = witnesses[witness_id]
        for unit in units:
            if not unit.canonical_ref_id:
                continue
            grouped[unit.canonical_ref_id].append(
                AlignedWitnessUnit(
                    witness_id=witness_id,
                    language=unit.language,
                    edition=witness.edition,
                    canonical_ref_id=unit.canonical_ref_id,
                    surface=unit.surface,
                    normalized=unit.normalized,
                    provenance=unit.provenance,
                )
            )
    return [
        AlignmentCluster(ref, tuple(sorted(items, key=lambda x: x.witness_id)))
        for ref, items in sorted(grouped.items())
    ]


def audit_alignment(
    witness_units: dict[str, Iterable[LanguageUnit]],
    witnesses: dict[str, TextWitness],
    *,
    expected_witnesses: Iterable[str] | None = None,
) -> CorpusAuditReport:
    """Audit canonical alignment coverage without assuming verse-system parity.

    Missing units are queued for review rather than silently synthesized. This is
    important for LXX/Vulgate/Psalm numbering and other genuine textual-system
    differences.
    """
    materialized = {wid: list(units) for wid, units in witness_units.items()}
    expected = tuple(sorted(expected_witnesses or materialized.keys()))
    report = CorpusAuditReport(expected_witnesses=expected)

    canonical_by_witness: dict[str, set[str]] = {}
    for wid, units in materialized.items():
        refs: set[str] = set()
        for unit in units:
            report.aligned_units += 1
            if not unit.canonical_ref_id:
                report.exceptions.append(AuditException(
                    "UNALIGNED_UNIT", None, wid, f"order={unit.order}"
                ))
                continue
            if unit.canonical_ref_id in refs:
                report.exceptions.append(AuditException(
                    "DUPLICATE_CANONICAL_REF", unit.canonical_ref_id, wid,
                    "multiple units from same witness map to one canonical ref",
                ))
            refs.add(unit.canonical_ref_id)
        canonical_by_witness[wid] = refs

    all_refs = set().union(*canonical_by_witness.values()) if canonical_by_witness else set()
    report.canonical_refs = len(all_refs)
    for ref in sorted(all_refs):
        present = {wid for wid, refs in canonical_by_witness.items() if ref in refs}
        missing = [wid for wid in expected if wid not in present]
        if missing:
            report.incomplete_refs += 1
            for wid in missing:
                report.exceptions.append(AuditException(
                    "MISSING_WITNESS_AT_REF", ref, wid,
                    "absence requires classification; do not synthesize text",
                ))
        else:
            report.complete_refs += 1

    for wid in expected:
        if wid not in witnesses:
            report.exceptions.append(AuditException(
                "UNKNOWN_WITNESS", None, wid, "witness metadata missing"
            ))
        elif wid not in materialized:
            report.exceptions.append(AuditException(
                "WITNESS_NOT_INGESTED", None, wid, "no units supplied to audit"
            ))

    return report
