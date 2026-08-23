"""Transferable reflex primitives connecting Doré's earned capabilities.

This layer routes evidence; it does not create facts. Every result retains the
boundary between exact evidence, candidates, and reconstruction.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable
from .search import BibleSearchIndex, SearchQuery
from .language.alignment import AlignmentCluster
from .world.model import WorldEntity, WorldClaim

@dataclass(frozen=True)
class ReflexResult:
    intent: str
    route: tuple[str,...]
    evidence: tuple[object,...]
    confidence: float
    boundary: str


def retrieve_text(index:BibleSearchIndex, text:str, *, limit:int=20)->ReflexResult:
    """RC2: true exact evidence suppresses containment; fuzzy is fallback only."""
    textual=index.search(SearchQuery(text,mode='text',limit=limit))
    strict=[h for h in textual if h.score==1.0]
    if strict:return ReflexResult('text-retrieval',('exact',),tuple(strict),1.0,'strict normalized textual evidence')
    if textual:return ReflexResult('text-retrieval',('exact','normalized-containment'),tuple(textual),0.9,'containment evidence; not fuzzy')
    fuzzy=index.search(SearchQuery(text,mode='fuzzy',limit=limit))
    confidence=fuzzy[0].score if fuzzy else 0.0
    return ReflexResult('text-retrieval',('exact','normalized-containment','bounded-fuzzy'),tuple(fuzzy),confidence,'fuzzy candidates are not facts')


def original_language_route(index:BibleSearchIndex, translated_phrase:str, original_units:Iterable, *, language:str)->ReflexResult:
    """RC3: translation -> passage -> same-ref original evidence.

    Stops at verse-level co-attestation unless an original unit itself carries
    explicit ``translation_alignment`` analysis evidence.
    """
    translated=index.search(SearchQuery(translated_phrase,mode='text',limit=20))
    refs={h.canonical_ref_id for h in translated}
    originals=[u for u in original_units if getattr(u,'canonical_ref_id','') in refs and getattr(u,'language','')==language]
    aligned=[u for u in originals if dict(getattr(u,'analyses',()) or ()).get('translation_alignment')]
    evidence=aligned or originals
    boundary='word-level alignment evidence' if aligned else 'verse-level co-attestation only; do not claim one-to-one word equivalence'
    return ReflexResult('translated-to-original',('translated-text','canonical-ref','original-language','lemma-morphology'),tuple(evidence),1.0 if aligned else (0.7 if evidence else 0.0),boundary)


def compare_witnesses(clusters:Iterable[AlignmentCluster], canonical_ref_id:str)->ReflexResult:
    cluster=next((c for c in clusters if c.canonical_ref_id==canonical_ref_id),None)
    evidence=tuple(cluster.witnesses) if cluster else ()
    return ReflexResult('cross-witness-comparison',('canonical-ref','aligned-witnesses','difference-characterization'),evidence,1.0 if len(evidence)>1 else 0.0,'differences are reported; missing witnesses are never synthesized and no winner is presumed')


def resolve_entity(mention:str, entities:Iterable[WorldEntity], *, context_refs:Iterable[str]=())->ReflexResult:
    key=mention.casefold().strip(); refs=set(context_refs); candidates=[]
    for e in entities:
        names={e.preferred_label.casefold(),*(a.value.casefold() for a in e.aliases)}
        if key in names:candidates.append(e)
    if refs:
        constrained=[e for e in candidates if any(a.locator in refs for a in e.attestations)]
        if constrained:candidates=constrained
    boundary='resolved by context attestation' if len(candidates)==1 else ('unresolved ambiguity; surface all candidates' if len(candidates)>1 else 'no attested entity candidate')
    return ReflexResult('entity-resolution',('mention','candidate-entities','context-attestation'),tuple(candidates),1.0 if len(candidates)==1 else (0.5 if candidates else 0.0),boundary)


def geography_claims(place_id:str, claims:Iterable[WorldClaim])->ReflexResult:
    matched=tuple(c for c in claims if c.subject_id==place_id)
    classes=tuple(sorted({a.evidence_class for c in matched for a in c.evidence}))
    boundary='evidence classes kept separate: '+(', '.join(classes) if classes else 'none')
    return ReflexResult('biblical-geography',('place-identity','scripture-attestation','geographic-evidence','epistemic-separation'),matched,1.0 if matched else 0.0,boundary)
