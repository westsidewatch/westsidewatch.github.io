"""BW-2 geography reflex: keep biblical place identity distinct from modern reconstruction."""
from __future__ import annotations
from dataclasses import dataclass
from .geography import AncientPlace, ModernCandidate

@dataclass(frozen=True)
class GeographyAnswer:
    ancient_place_id: str
    canonical_refs: tuple[str,...]
    modern_candidates: tuple[ModernCandidate,...]
    scripture_explicit: tuple[str,...]
    reconstruction: tuple[str,...]
    resolved_modern_id: str | None


def explain_place(place: AncientPlace, *, min_resolution_confidence: float=.80) -> GeographyAnswer:
    """Return evidence-separated geography; never turn a coordinate candidate into Scripture fact."""
    explicit=tuple(f'{ref}:place_attested' for ref in place.canonical_refs)
    reconstruction=[]
    for c in place.candidates:
        coords=f'{c.lat},{c.lon}' if c.lat is not None and c.lon is not None else 'coordinates_unknown'
        reconstruction.append(f'{c.modern_id}|{coords}|confidence={c.confidence:.3f}')
    strong=[c for c in place.candidates if c.confidence>=min_resolution_confidence and c.modern_id]
    resolved=strong[0].modern_id if len(strong)==1 else None
    return GeographyAnswer(place.source_id,place.canonical_refs,place.candidates,explicit,tuple(reconstruction),resolved)


def distance_claim_allowed(*, source_is_scripture: bool, reconstructed: bool) -> str:
    """Label route/distance claims according to their evidence route."""
    if reconstructed:return 'SCHOLARLY_RECONSTRUCTION'
    return 'SCRIPTURE_EXPLICIT' if source_is_scripture else 'GEOSPATIAL_OBSERVATION'
