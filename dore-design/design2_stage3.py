"""Design 2.0 Stage 3: expansion -> maturity -> comparison -> convergence engine.

This is intentionally renderer-neutral. It turns the visual constitution into executable
workflow state without allowing technical checks to self-approve aesthetics.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Iterable, Mapping

DESIGN_WORLDS = (
    "swiss-international", "bauhaus-modernism", "editorial-newspaper", "book-print",
    "image-led-documentary", "japanese-editorial", "new-wave-postmodern", "brutalism",
    "neo-brutalism", "maximalism", "extreme-minimalism", "fashion-luxury",
    "museum-cultural", "collage-zine-punk", "y2k-early-web", "skeuomorphic",
    "spatial", "cinema", "illustration", "vernacular-community", "data-information",
    "sacred-architecture", "generative-experimental",
)

MATURITY_GATES = (
    "complete_experience", "real_material_strategy", "typography_system", "navigation",
    "section_rhythm", "content_components", "interaction", "meaningful_motion",
    "reduced_motion", "footer_end_state", "long_content_stress", "bilingual_stress",
    "desktop", "tablet", "mobile", "responsive_transformation", "contrast",
    "keyboard", "browser_evidence", "design_critique",
)

CONVERGENCE_SEQUENCE = (
    "museum_external_learning", "materially_different_experiments", "mature_templates",
    "browser_evidence", "critique", "durable_learning", "broad_comparison",
    "user_led_convergence", "design_system_foundations", "brick_system",
    "living_wall", "homepage_implementation",
)

@dataclass(frozen=True)
class ExperimentEvidence:
    experiment_id: str
    world: str
    gates: Mapping[str, bool]
    browser_evidence: tuple[str, ...] = ()
    critique: tuple[str, ...] = ()
    user_style_acceptance: bool = False

    @property
    def maturity_score(self) -> float:
        return sum(bool(self.gates.get(g)) for g in MATURITY_GATES) / len(MATURITY_GATES)

    @property
    def mature(self) -> bool:
        return all(bool(self.gates.get(g)) for g in MATURITY_GATES)

    def record(self) -> dict:
        data = asdict(self)
        data["maturity_score"] = self.maturity_score
        data["mature"] = self.mature
        data["style_acceptance"] = bool(self.user_style_acceptance)
        return data


def expansion_coverage(experiments: Iterable[ExperimentEvidence]) -> dict:
    items = tuple(experiments)
    covered = {e.world for e in items if e.world in DESIGN_WORLDS}
    mature = {e.world for e in items if e.world in DESIGN_WORLDS and e.mature}
    return {
        "world_count": len(DESIGN_WORLDS),
        "covered_worlds": sorted(covered),
        "coverage": len(covered) / len(DESIGN_WORLDS),
        "mature_worlds": sorted(mature),
        "maturity_depth": len(mature) / len(DESIGN_WORLDS),
    }


def convergence_gate(experiments: Iterable[ExperimentEvidence], *, minimum_worlds: int = 8,
                     minimum_mature_worlds: int = 3, user_authorized: bool = False) -> dict:
    items = tuple(experiments)
    coverage = expansion_coverage(items)
    accepted = [e.experiment_id for e in items if e.user_style_acceptance]
    reasons = []
    if len(coverage["covered_worlds"]) < minimum_worlds:
        reasons.append("insufficient-expansion-breadth")
    if len(coverage["mature_worlds"]) < minimum_mature_worlds:
        reasons.append("insufficient-maturity-depth")
    if not user_authorized:
        reasons.append("user-convergence-authorization-required")
    return {
        "ready": not reasons,
        "reasons": reasons,
        "coverage": coverage,
        "accepted_experiments": accepted,
        "sequence": CONVERGENCE_SEQUENCE,
    }
