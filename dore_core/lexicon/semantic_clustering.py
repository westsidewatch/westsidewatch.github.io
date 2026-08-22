"""Evidence-first lexical semantic clustering for Doré.

This module groups concordance occurrences by corpus morphology before any
semantic label is assigned. Morphological clusters are evidence; semantic
interpretation belongs to a later, separately-provenanced layer.
"""
from __future__ import annotations
from dataclasses import dataclass
from collections import Counter, defaultdict
from typing import Iterable
from dore_core.lexicon.concordance import ConcordanceOccurrence

@dataclass(frozen=True)
class MorphologyCluster:
    key: str
    count: int
    references: tuple[str, ...]
    surfaces: dict[str, int]
    raw_lemmas: dict[str, int]

@dataclass(frozen=True)
class MorphologyClusterReport:
    lexical_id: str
    total_occurrences: int
    clusters: tuple[MorphologyCluster, ...]
    interpretive_status: str = "MORPHOLOGY_ONLY"


def morphology_family(code: str | None) -> str:
    """Return a conservative corpus morphology family without semantic glossing."""
    if not code:
        return "UNKNOWN"
    # OSHB morphology may carry conjunction/article/etc. prefixes before the
    # lexical component. Keep the full code in evidence, but group by the
    # final slash-delimited lexical morphology component.
    return code.split("/")[-1]


def cluster_by_morphology(
    occurrences: Iterable[ConcordanceOccurrence], lexical_id: str
) -> MorphologyClusterReport:
    buckets: dict[str, list[ConcordanceOccurrence]] = defaultdict(list)
    all_items = list(occurrences)
    for occurrence in all_items:
        buckets[morphology_family(occurrence.morphology)].append(occurrence)

    clusters = []
    for key, items in buckets.items():
        clusters.append(MorphologyCluster(
            key=key,
            count=len(items),
            references=tuple(sorted(x.canonical_ref_id for x in items)),
            surfaces=dict(Counter(x.surface for x in items)),
            raw_lemmas=dict(Counter((x.lemma or "UNKNOWN") for x in items)),
        ))
    clusters.sort(key=lambda x: (-x.count, x.key))
    return MorphologyClusterReport(
        lexical_id=lexical_id,
        total_occurrences=len(all_items),
        clusters=tuple(clusters),
    )
