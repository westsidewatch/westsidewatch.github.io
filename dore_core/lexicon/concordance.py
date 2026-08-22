"""Corpus-grounded lexical concordance tools for Doré."""
from __future__ import annotations
from dataclasses import dataclass
from collections import Counter
from typing import Iterable
from dore_core.readers.original_language import TokenRecord

@dataclass(frozen=True)
class ConcordanceOccurrence:
    canonical_ref_id: str
    surface: str
    normalized: str | None
    lemma: str | None
    morphology: str | None
    language: str
    provenance: str

@dataclass(frozen=True)
class ConcordanceReport:
    lemma: str
    occurrences: tuple[ConcordanceOccurrence, ...]
    surface_distribution: dict[str, int]
    morphology_distribution: dict[str, int]
    book_distribution: dict[str, int]


def _analysis(token: TokenRecord, kind: str) -> str | None:
    for item in token.analyses:
        if item.type == kind:
            return item.value
    return None


def _book(ref: str) -> str:
    parts = ref.split(".")
    return parts[2] if len(parts) >= 5 and parts[:2] == ["bible", "ref"] else "UNKNOWN"


def _lemma_components(raw_lemma: str | None) -> tuple[str, ...]:
    if not raw_lemma:
        return ()
    return tuple(part for part in raw_lemma.split("/") if part)


def build_concordance(tokens: Iterable[TokenRecord], lemma: str) -> ConcordanceReport:
    """Find a lexical id even when OSHB stores it in a composite lemma like c/539."""
    hits = []
    for token in tokens:
        token_lemma = _analysis(token, "lemma")
        if lemma not in _lemma_components(token_lemma):
            continue
        hits.append(ConcordanceOccurrence(
            canonical_ref_id=token.canonical_ref_id,
            surface=token.surface,
            normalized=token.normalized,
            lemma=token_lemma,
            morphology=_analysis(token, "morphology"),
            language=token.language,
            provenance=f"{token.textual_source_id}@{token.corpus_snapshot}",
        ))
    hits.sort(key=lambda x: x.canonical_ref_id)
    return ConcordanceReport(
        lemma=lemma,
        occurrences=tuple(hits),
        surface_distribution=dict(Counter(x.surface for x in hits)),
        morphology_distribution=dict(Counter(x.morphology or "UNKNOWN" for x in hits)),
        book_distribution=dict(Counter(_book(x.canonical_ref_id) for x in hits)),
    )
