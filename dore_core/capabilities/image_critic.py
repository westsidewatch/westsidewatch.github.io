from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class CritiqueResult:
    accepted: bool
    scores: dict[str, float]
    violations: tuple[str, ...]
    corrections: tuple[str, ...]
    real_visual_review: bool


def critique_from_observations(recipe: Mapping[str, Any], observations: Mapping[str, Any], *, real_visual_review: bool) -> CritiqueResult:
    """Turn vision observations into a deterministic correction contract.

    The observations must come from an actual vision reader before real_visual_review=True.
    """
    scores = {k: float(observations.get(k, 0.0)) for k in ("composition", "style_fidelity", "typography", "product_fit")}
    violations: list[str] = []
    corrections: list[str] = []
    empty = observations.get("empty_paper_ratio")
    if isinstance(empty, (int, float)) and not .25 <= float(empty) <= .55:
        violations.append("negative-space-out-of-range")
        corrections.append("restore 25–55% visible paper")
    inks = observations.get("ink_count")
    if isinstance(inks, int) and inks > 2:
        violations.append("too-many-inks")
        corrections.append("reduce artwork to at most two inks")
    if scores["composition"] < .70:
        corrections.append("strengthen asymmetric subject mass and off-axis tension")
    if scores["typography"] < .70:
        corrections.append("rebuild display-type hierarchy and microcopy contrast")
    if scores["product_fit"] < .70:
        corrections.append("recompose for the target product surface rather than poster aesthetics alone")
    accepted = real_visual_review and not violations and all(value >= .70 for value in scores.values())
    return CritiqueResult(accepted, scores, tuple(violations), tuple(dict.fromkeys(corrections)), real_visual_review)


def correction_direction(result: CritiqueResult) -> str:
    return "; ".join(result.corrections)
