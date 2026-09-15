"""Compile generation instructions from grounded visual observations.

No publication stereotype vocabulary is introduced here. Italian lineage/canon may be
supplied as context, but concrete generation instructions come from observed image facts.
"""
from __future__ import annotations

from typing import Any, Iterable, Mapping

from editorial_visual_observation_capability import DIMENSIONS, promoteable_to_prompt


class ObservationCompileError(ValueError):
    pass


def compile_grounded_prompt(
    observation: Mapping[str, Any],
    *,
    selected_dimensions: Iterable[str] = DIMENSIONS,
    lineage_context: str = "",
) -> str:
    if not promoteable_to_prompt(observation):
        raise ObservationCompileError("only image-grounded observations may compile prompts")

    selected = [d for d in selected_dimensions if d in DIMENSIONS]
    if not selected:
        raise ObservationCompileError("at least one supported dimension is required")

    evidence = observation["evidence"]
    observer = observation["observer"]
    lines = [
        "Preserve the supplied subject identity unless the user explicitly requests replacement.",
        "Recompose from the observed design relationships of the selected historical magazine image.",
        "",
        "HISTORICAL IMAGE AUTHORITY",
        f"- evidence: {evidence['id']}",
        f"- source: {evidence['sourceUri']}",
        f"- observer: {observer['providerKind']} / {observer['providerId']}",
        "",
        "GROUNDING CONTRACT",
        "- The historical image controls concrete composition, crop, material, color and spatial relationships.",
        "- Do not introduce concrete, architecture, furniture, grids, colors, motifs or extra image regions unless supported by observed facts.",
        "- Do not complete missing information from a generic Italian/editorial/modernist style prior.",
    ]
    if lineage_context.strip():
        lines += [
            "",
            "ITALIAN DESIGN DNA — CONTEXT ONLY",
            f"- {lineage_context.strip()}",
            "- Use this only for editorial judgement; it cannot override or add concrete visual content.",
        ]

    lines += ["", "SELECTED EVIDENCE DIMENSIONS"]
    used = 0
    for name in selected:
        item = observation["dimensions"][name]
        if item["status"] == "insufficient":
            lines.append(f"- {name}: insufficient visual evidence; do not invent this dimension.")
            continue
        used += 1
        lines.append(f"- {name}:")
        for fact in item["facts"]:
            lines.append(f"  - {fact}")

    if used == 0:
        raise ObservationCompileError("selected dimensions contain no observed visual facts")

    lines += [
        "",
        "FINAL FIDELITY RULE",
        "The result should remain recognizably derived from this evidence image's design relationships even when subject/copy changes. Remove any element whose only justification is a generic style association.",
    ]
    return "\n".join(lines)
