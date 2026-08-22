"""Evidence-first contracts for Doré's Biblical World education."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Literal

EvidenceClass = Literal[
    'SCRIPTURE_EXPLICIT','SCRIPTURE_INFERRED','PRIMARY_EXTRA_BIBLICAL',
    'ARCHAEOLOGICAL','GEOSPATIAL_OBSERVATION','SCHOLARLY_RECONSTRUCTION',
    'TRADITIONAL_IDENTIFICATION','EDITORIAL_NORMALIZATION'
]
EntityType = Literal['person','place','people_group','kingdom_or_polity','office_or_role','event','artifact_or_object','institution','genealogical_line','period']

@dataclass(frozen=True)
class Attestation:
    source_id: str
    locator: str
    evidence_class: EvidenceClass
    confidence: float = 1.0
    note: str | None = None

@dataclass(frozen=True)
class Alias:
    value: str
    language: str
    source_id: str
    kind: str = 'name'
    confidence: float = 1.0

@dataclass(frozen=True)
class WorldEntity:
    entity_id: str
    entity_type: EntityType
    preferred_label: str
    aliases: tuple[Alias,...] = ()
    attestations: tuple[Attestation,...] = ()
    temporal_scope: str | None = None

@dataclass(frozen=True)
class WorldClaim:
    claim_id: str
    subject_id: str
    predicate: str
    object_id: str | None = None
    literal_value: str | float | int | None = None
    evidence: tuple[Attestation,...] = ()
    temporal_scope: str | None = None
    confidence: float = 1.0
    disputed: bool = False

@dataclass
class WorldValidation:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    @property
    def passed(self)->bool:return not self.errors


def validate_entity(entity: WorldEntity)->WorldValidation:
    r=WorldValidation()
    if not entity.entity_id:r.errors.append('missing_entity_id')
    if not entity.preferred_label:r.errors.append('missing_preferred_label')
    if not entity.attestations:r.errors.append(f'missing_attestation:{entity.entity_id}')
    for a in entity.aliases:
        if not a.value or not a.language or not a.source_id:r.errors.append(f'invalid_alias:{entity.entity_id}')
        if not 0 <= a.confidence <= 1:r.errors.append(f'invalid_alias_confidence:{entity.entity_id}:{a.value}')
    return r


def validate_claim(claim: WorldClaim, known_entities: set[str])->WorldValidation:
    r=WorldValidation()
    if claim.subject_id not in known_entities:r.errors.append(f'unknown_subject:{claim.claim_id}')
    if claim.object_id is not None and claim.object_id not in known_entities:r.errors.append(f'unknown_object:{claim.claim_id}')
    if claim.object_id is None and claim.literal_value is None:r.errors.append(f'missing_claim_value:{claim.claim_id}')
    if not claim.evidence:r.errors.append(f'missing_evidence:{claim.claim_id}')
    if not 0 <= claim.confidence <= 1:r.errors.append(f'invalid_confidence:{claim.claim_id}')
    # Precision discipline: disputed or reconstructed claims may be high-confidence, but never provenance-free.
    if any(a.evidence_class in {'SCHOLARLY_RECONSTRUCTION','TRADITIONAL_IDENTIFICATION'} for a in claim.evidence) and claim.confidence == 1.0:
        r.warnings.append(f'review_absolute_confidence_on_reconstruction:{claim.claim_id}')
    return r
