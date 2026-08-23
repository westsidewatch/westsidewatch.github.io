"""BW-1 entity identity and alias reflex.

This layer routes a mention to evidence-bearing WorldEntity candidates.  It does
not merge equal-looking names and it does not silently choose when context is
insufficient.  Search/product layers may present the ranked candidates, but
identity remains evidence-bound.
"""
from __future__ import annotations
from dataclasses import dataclass
import re
from typing import Iterable
from .model import WorldEntity

# Deliberately small script normalization shared conceptually with Doré Search.
# This is orthographic normalization, never identity evidence.
ZH_VARIANTS = str.maketrans({
    '亞':'亚','約':'约','馬':'马','羅':'罗','撒':'撒','瑪':'玛','該':'该','該':'该',
    '該':'该','穌':'稣','穌':'稣','穌':'稣','穌':'稣','穌':'稣','穌':'稣','穌':'稣',
})

def normalize_mention(value: str) -> str:
    value=(value or '').strip().casefold().translate(ZH_VARIANTS)
    return re.sub(r'[\s·.\-–—_]+','',value)

@dataclass(frozen=True)
class EntityCandidate:
    entity: WorldEntity
    score: float
    matched_alias: str
    reasons: tuple[str,...]

@dataclass(frozen=True)
class EntityResolution:
    mention: str
    candidates: tuple[EntityCandidate,...]
    resolved_entity_id: str | None
    ambiguous: bool


def _names(entity: WorldEntity):
    yield entity.preferred_label, 'preferred_label'
    for alias in entity.aliases:
        yield alias.value, f'alias:{alias.language}:{alias.kind}'


def resolve_entity(mention: str, entities: Iterable[WorldEntity], *, canonical_ref_id: str | None=None, entity_type: str | None=None) -> EntityResolution:
    """Resolve by name/alias and optional passage/type context.

    Equal names may yield multiple candidates.  A single entity is resolved only
    when the best candidate is unique after evidence-bearing context is applied.
    """
    needle=normalize_mention(mention)
    if not needle:
        return EntityResolution(mention,(),None,False)
    found=[]
    for entity in entities:
        if entity_type and entity.entity_type != entity_type:
            continue
        best=None
        for value,kind in _names(entity):
            if normalize_mention(value)==needle:
                score=1.0 if kind=='preferred_label' else .95
                reasons=[kind]
                if canonical_ref_id and any(a.locator==canonical_ref_id for a in entity.attestations):
                    score+=.25;reasons.append('canonical_attestation')
                candidate=EntityCandidate(entity,score,value,tuple(reasons))
                if best is None or candidate.score>best.score:best=candidate
        if best:found.append(best)
    found.sort(key=lambda c:(-c.score,c.entity.entity_id))
    if not found:return EntityResolution(mention,(),None,False)
    top=found[0].score
    tied=[c for c in found if c.score==top]
    resolved=tied[0].entity.entity_id if len(tied)==1 else None
    return EntityResolution(mention,tuple(found),resolved,len(tied)>1)
