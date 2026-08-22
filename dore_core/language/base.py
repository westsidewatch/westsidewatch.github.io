"""Universal language and textual-witness contracts for Doré."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Iterable, Protocol

@dataclass(frozen=True)
class TextWitness:
    witness_id: str
    language: str
    edition: str
    source_id: str
    snapshot: str
    license_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class LanguageUnit:
    witness_id: str
    canonical_ref_id: str | None
    order: int
    surface: str
    normalized: str | None
    language: str
    analyses: tuple[tuple[str, str], ...] = ()
    provenance: tuple[str, ...] = ()

@dataclass(frozen=True)
class AdapterCapabilities:
    segmentation: bool = True
    normalization: bool = True
    lemma: bool = False
    morphology: bool = False
    syntax: bool = False
    transliteration: bool = False
    speech: bool = False
    canonical_alignment: bool = False

class LanguageAdapter(Protocol):
    adapter_id: str
    language: str
    capabilities: AdapterCapabilities

    def ingest(self, source: Any, witness: TextWitness) -> Iterable[LanguageUnit]: ...
    def normalize(self, text: str) -> str: ...


def validate_units(units: Iterable[LanguageUnit], witness: TextWitness) -> list[str]:
    errors: list[str] = []
    seen_orders: dict[str | None, set[int]] = {}
    for unit in units:
        if unit.witness_id != witness.witness_id:
            errors.append(f"witness_mismatch:{unit.witness_id}")
        if not unit.surface:
            errors.append(f"empty_surface:{unit.canonical_ref_id}:{unit.order}")
        if unit.language != witness.language:
            errors.append(f"language_mismatch:{unit.language}:{witness.language}")
        orders = seen_orders.setdefault(unit.canonical_ref_id, set())
        if unit.order in orders:
            errors.append(f"duplicate_order:{unit.canonical_ref_id}:{unit.order}")
        orders.add(unit.order)
        if not unit.provenance:
            errors.append(f"missing_provenance:{unit.canonical_ref_id}:{unit.order}")
    return errors
