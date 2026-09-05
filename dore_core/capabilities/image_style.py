from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Mapping, Any


@dataclass(frozen=True)
class StyleRecipe:
    grammar: str
    dominant_ink: str
    accent_ink: str | None
    dominant_ratio: float
    empty_paper_ratio: float
    reproduction: str
    composition: tuple[str, ...]
    typography: tuple[str, ...]
    invariants: tuple[str, ...]

    def to_payload(self) -> dict[str, Any]:
        return asdict(self)


def compile_editorial_recipe(brief: Mapping[str, Any]) -> StyleRecipe:
    """Compile visual grammar, never copy a reference composition."""
    mode = str(brief.get("ink_mode", "chromatic+black"))
    accent = None if mode == "one-ink" else str(brief.get("accent_ink", "black"))
    empty = float(brief.get("empty_paper_ratio", 0.35))
    dominant = float(brief.get("dominant_ratio", 0.78))
    if not 0.25 <= empty <= 0.55:
        raise ValueError("empty paper must remain 25–55%")
    if not 0.70 <= dominant <= 0.85:
        raise ValueError("dominant plate must remain 70–85%")
    return StyleRecipe(
        grammar="dore.editorial-mono.v1",
        dominant_ink=str(brief.get("dominant_ink", "warm-red")),
        accent_ink=accent,
        dominant_ratio=dominant,
        empty_paper_ratio=empty,
        reproduction=str(brief.get("reproduction", "risograph-halftone")),
        composition=("asymmetric crop", "large subject mass", "deliberate negative paper", "off-axis tension"),
        typography=("oversized display type", "vertical-or-rotated counterpoint", "microcopy contrast"),
        invariants=("visible paper", "maximum two inks", "change at least four structural variables from any reference", "reference is grammar not template"),
    )
