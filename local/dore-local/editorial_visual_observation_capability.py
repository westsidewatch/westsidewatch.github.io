"""DORÉ Core — grounded editorial visual observation capability v0.

This module establishes the authority boundary missing from Italian Editorial Atlas.
It DOES NOT inspect images by itself and it contains no hand-written magazine fingerprints.
A vision provider must receive the real historical image and return observations grounded
in that image. Provider output is evidence, not learned DORÉ canon.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, Mapping

DIMENSIONS = (
    "layout", "image", "typography", "material",
    "density", "sequence", "irony", "emergence",
)

SCHEMA = "dore.editorial-visual-observation.v0"


class VisualObservationError(ValueError):
    pass


@dataclass(frozen=True)
class HistoricalImageEvidence:
    evidence_id: str
    image_uri: str
    source_uri: str
    publication: str
    era: str

    def validate(self) -> None:
        if not self.evidence_id.strip():
            raise VisualObservationError("evidence_id is required")
        if not self.image_uri.strip():
            raise VisualObservationError("real historical image_uri is required")
        if not self.source_uri.strip():
            raise VisualObservationError("historical source_uri is required")


def observation_request(evidence: HistoricalImageEvidence) -> Dict[str, Any]:
    evidence.validate()
    return {
        "schema": "dore.editorial-visual-observation-request.v0",
        "task": "observe-historical-editorial-image",
        "evidence": {
            "id": evidence.evidence_id,
            "imageUri": evidence.image_uri,
            "sourceUri": evidence.source_uri,
            "publication": evidence.publication,
            "era": evidence.era,
        },
        "authorityContract": {
            "mustInspectImage": True,
            "imageIsPrimaryAuthority": True,
            "publicationHistoryIsContextOnly": True,
            "noStyleStereotypeCompletion": True,
            "noUnsupportedConcreteInvention": True,
            "insufficientEvidenceMustRemainInsufficient": True,
        },
        "dimensions": list(DIMENSIONS),
        "requiredObservationKinds": [
            "visible-fact", "geometry-or-relation", "absence-or-uncertainty"
        ],
        "instruction": (
            "Inspect the supplied historical magazine image itself. For each dimension, "
            "record only visible design facts: proportions, regions, crop, scale, position, "
            "alignment, overlap, type-image relations, material/color evidence, density, "
            "reading order, and meaningful absences. Do not complete the image from a generic "
            "Italian/editorial/architectural style prior. If a dimension cannot be established "
            "from the image, mark it insufficient rather than inventing a rule."
        ),
    }


def _validate_provider_output(raw: Mapping[str, Any]) -> None:
    if raw.get("imageInspected") is not True:
        raise VisualObservationError("provider did not attest inspection of the historical image")
    dims = raw.get("dimensions")
    if not isinstance(dims, Mapping):
        raise VisualObservationError("provider dimensions missing")
    unknown = set(dims) - set(DIMENSIONS)
    if unknown:
        raise VisualObservationError(f"unknown dimensions: {sorted(unknown)}")
    for name in DIMENSIONS:
        item = dims.get(name)
        if not isinstance(item, Mapping):
            raise VisualObservationError(f"dimension {name} missing")
        status = item.get("status")
        if status not in {"observed", "insufficient"}:
            raise VisualObservationError(f"dimension {name}: invalid status")
        facts = item.get("facts", [])
        if not isinstance(facts, list) or not all(isinstance(x, str) and x.strip() for x in facts):
            raise VisualObservationError(f"dimension {name}: facts must be strings")
        if status == "observed" and not facts:
            raise VisualObservationError(f"dimension {name}: observed requires facts")
        if status == "insufficient" and facts:
            raise VisualObservationError(f"dimension {name}: insufficient must not fabricate facts")


def observe_historical_editorial_image(
    evidence: HistoricalImageEvidence,
    provider: Callable[[Mapping[str, Any]], Mapping[str, Any]],
    *,
    provider_id: str,
    provider_kind: str,
) -> Dict[str, Any]:
    """Run a real image-grounded provider behind a strict provenance boundary.

    provider_kind examples: ``dore-local-vision`` or ``grounded-chatgpt-vision``.
    Neither kind becomes canonical DORÉ learning merely by producing an observation.
    """
    if not provider_id.strip() or not provider_kind.strip():
        raise VisualObservationError("provider provenance is required")
    request = observation_request(evidence)
    raw = provider(request)
    if not isinstance(raw, Mapping):
        raise VisualObservationError("provider must return a mapping")
    _validate_provider_output(raw)
    return {
        "schema": SCHEMA,
        "authority": "historical-image-observation",
        "canonicalDoréLearning": False,
        "evidence": request["evidence"],
        "observer": {"providerId": provider_id, "providerKind": provider_kind},
        "dimensions": {name: dict(raw["dimensions"][name]) for name in DIMENSIONS},
        "provenance": {
            "imageInspected": True,
            "sourceUri": evidence.source_uri,
            "imageUri": evidence.image_uri,
            "derivation": "provider-grounded-observation",
        },
    }


def promoteable_to_prompt(observation: Mapping[str, Any]) -> bool:
    """Prompt compilation may consume grounded observations; canon promotion is separate."""
    return (
        observation.get("schema") == SCHEMA
        and observation.get("authority") == "historical-image-observation"
        and observation.get("provenance", {}).get("imageInspected") is True
    )
