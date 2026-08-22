"""Bridge Doré original-language readers and intertext graph v0.1."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable
from dore_core.readers.original_language import TokenRecord

@dataclass(frozen=True)
class VerseWitness:
    reference: str
    language: str
    surface: tuple[str, ...]
    normalized: tuple[str, ...]
    lemmas: tuple[str, ...]
    morphology: tuple[str, ...]
    provenance: tuple[str, ...]

@dataclass(frozen=True)
class IntertextWitnessBridge:
    source: VerseWitness
    target: VerseWitness
    relation: str
    claim_class: str
    edge_id: str


def build_verse_witness(tokens: Iterable[TokenRecord], reference: str) -> VerseWitness:
    selected = [t for t in tokens if t.reference == reference]
    if not selected:
        raise ValueError(f"no tokens for reference: {reference}")
    selected.sort(key=lambda t: t.order)
    languages = {t.language for t in selected}
    language = next(iter(languages)) if len(languages) == 1 else "mixed"
    return VerseWitness(
        reference=reference,
        language=language,
        surface=tuple(t.surface for t in selected),
        normalized=tuple(t.normalized for t in selected),
        lemmas=tuple(t.lemma for t in selected),
        morphology=tuple(t.morphology for t in selected),
        provenance=tuple(dict.fromkeys(t.provenance for t in selected)),
    )


def bridge_edge(edge: dict, source_tokens: Iterable[TokenRecord], target_tokens: Iterable[TokenRecord]) -> IntertextWitnessBridge:
    required = ("id", "source_ref", "target_ref", "relation", "claim_class")
    missing = [key for key in required if not edge.get(key)]
    if missing:
        raise ValueError(f"intertext edge missing fields: {','.join(missing)}")
    return IntertextWitnessBridge(
        source=build_verse_witness(source_tokens, edge["source_ref"]),
        target=build_verse_witness(target_tokens, edge["target_ref"]),
        relation=edge["relation"],
        claim_class=edge["claim_class"],
        edge_id=edge["id"],
    )
