"""Bridge Doré original-language readers and intertext graph v0.2."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable, Optional
from dore_core.readers.original_language import TokenRecord

@dataclass(frozen=True)
class VerseWitness:
    reference: str
    language: str
    surface: tuple[str, ...]
    normalized: tuple[Optional[str], ...]
    lemmas: tuple[Optional[str], ...]
    morphology: tuple[Optional[str], ...]
    provenance: tuple[str, ...]

@dataclass(frozen=True)
class IntertextWitnessBridge:
    source: VerseWitness
    target: VerseWitness
    relation: str
    claim_class: str
    edge_id: str


def _analysis(token: TokenRecord, analysis_type: str) -> Optional[str]:
    for analysis in token.analyses:
        if analysis.type == analysis_type:
            return analysis.value
    return None


def _canonical_ref(reference: str) -> str:
    if reference.startswith("bible.ref."):
        return reference
    parts = reference.split(".")
    if len(parts) != 3:
        raise ValueError(f"invalid reference: {reference}")
    book, chapter, verse = parts
    return f"bible.ref.{book.upper()}.{int(chapter)}.{int(verse)}"


def build_verse_witness(tokens: Iterable[TokenRecord], reference: str) -> VerseWitness:
    canonical_ref = _canonical_ref(reference)
    selected = [t for t in tokens if t.canonical_ref_id == canonical_ref]
    if not selected:
        raise ValueError(f"no tokens for reference: {reference}")
    selected.sort(key=lambda t: t.order)
    languages = {t.language for t in selected}
    language = next(iter(languages)) if len(languages) == 1 else "mixed"
    provenance = []
    for token in selected:
        marker = f"{token.textual_source_id}@{token.corpus_snapshot}"
        if marker not in provenance:
            provenance.append(marker)
    return VerseWitness(
        reference=reference,
        language=language,
        surface=tuple(t.surface for t in selected),
        normalized=tuple(t.normalized for t in selected),
        lemmas=tuple(_analysis(t, "lemma") for t in selected),
        morphology=tuple(_analysis(t, "morphology") for t in selected),
        provenance=tuple(provenance),
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
