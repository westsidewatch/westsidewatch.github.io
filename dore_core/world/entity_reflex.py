"""BW-1 entity identity, alias, scope and aggregation reflex.

Routes mentions/questions to evidence-bearing WorldEntity candidates. Equal-looking
names are never merged merely by spelling. ONE chapter context may rank candidates;
canon-wide questions deliberately ignore local scope. Identity remains evidence-bound.
"""
from __future__ import annotations
from dataclasses import dataclass
import re
from typing import Iterable
from .model import WorldEntity

ZH_VARIANTS = str.maketrans({'亞':'亚','約':'约','馬':'马','羅':'罗','瑪':'玛','該':'该','穌':'稣'})

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

@dataclass(frozen=True)
class EntityAggregation:
    mention: str
    entity_type: str | None
    candidates: tuple[EntityCandidate,...]
    minimum_distinct: int
    maximum_distinct: int
    disputed_groups: tuple[tuple[str,...], ...] = ()


def _names(entity: WorldEntity):
    yield entity.preferred_label, 'preferred_label'
    for alias in entity.aliases:
        yield alias.value, f'alias:{alias.language}:{alias.kind}'


def _ref_in_scope(locator: str, scope: str) -> bool:
    """Scope accepts canonical verse/chapter prefixes, e.g. bible.ref.MAT.1."""
    scope=scope.rstrip('.')
    return locator==scope or locator.startswith(scope+'.')


def resolve_entity(mention: str, entities: Iterable[WorldEntity], *, canonical_ref_id: str | None=None, canonical_scope: str | None=None, entity_type: str | None=None) -> EntityResolution:
    needle=normalize_mention(mention)
    if not needle:return EntityResolution(mention,(),None,False)
    found=[]
    for entity in entities:
        if entity_type and entity.entity_type != entity_type:continue
        best=None
        for value,kind in _names(entity):
            if normalize_mention(value)!=needle:continue
            score=1.0 if kind=='preferred_label' else .95; reasons=[kind]
            if canonical_ref_id and any(a.locator==canonical_ref_id for a in entity.attestations):
                score+=.25;reasons.append('canonical_attestation')
            elif canonical_scope and any(_ref_in_scope(a.locator,canonical_scope) for a in entity.attestations):
                score+=.15;reasons.append('canonical_scope')
            c=EntityCandidate(entity,score,value,tuple(reasons))
            if best is None or c.score>best.score:best=c
        if best:found.append(best)
    found.sort(key=lambda c:(-c.score,c.entity.entity_id))
    if not found:return EntityResolution(mention,(),None,False)
    top=found[0].score;tied=[c for c in found if c.score==top]
    return EntityResolution(mention,tuple(found),tied[0].entity.entity_id if len(tied)==1 else None,len(tied)>1)


def aggregate_entities(mention: str, entities: Iterable[WorldEntity], *, entity_type: str | None=None, disputed_identity_groups: Iterable[Iterable[str]]=()) -> EntityAggregation:
    """Canon-wide same-name aggregation for questions like 'how many Marys?'.

    It reports a range when scholarship/tradition may merge candidate identities.
    disputed_identity_groups contains entity-id sets that *may* represent one identity;
    the function never performs that merge as fact.
    """
    resolution=resolve_entity(mention,entities,entity_type=entity_type)
    candidates=resolution.candidates
    ids={c.entity.entity_id for c in candidates}
    groups=[]
    reduction=0
    for raw in disputed_identity_groups:
        group=tuple(sorted(set(raw)&ids))
        if len(group)>1:
            groups.append(group);reduction+=len(group)-1
    maximum=len(ids);minimum=max(0,maximum-reduction)
    return EntityAggregation(mention,entity_type,candidates,minimum,maximum,tuple(groups))
