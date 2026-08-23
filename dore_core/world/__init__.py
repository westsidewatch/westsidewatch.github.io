"""Doré Biblical World foundation package."""
from .model import Alias, Attestation, WorldClaim, WorldEntity, WorldValidation, validate_claim, validate_entity
from .entity_reflex import EntityCandidate, EntityResolution, normalize_mention, resolve_entity

__all__ = [
    'Alias','Attestation','WorldClaim','WorldEntity','WorldValidation',
    'validate_claim','validate_entity',
    'EntityCandidate','EntityResolution','normalize_mention','resolve_entity',
]
