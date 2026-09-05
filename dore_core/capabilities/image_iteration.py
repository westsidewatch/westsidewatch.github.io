from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Mapping

from .image_critic import CritiqueResult, correction_direction, critique_from_observations
from .image_pipeline import ResidentGenerationResult, generate_resident_image
from .image_renderer import ComfyUIRenderer
from .image_workflow import WorkflowTemplate


@dataclass(frozen=True)
class IterationStep:
    index: int
    generation: ResidentGenerationResult
    critique: CritiqueResult


@dataclass(frozen=True)
class IterationResult:
    accepted: bool
    steps: tuple[IterationStep, ...]
    stop_reason: str


VisionReader = Callable[[Path, Mapping[str, Any], Mapping[str, Any]], Mapping[str, Any]]


def iterate_image(*, renderer: ComfyUIRenderer, template: WorkflowTemplate, brief: Mapping[str, Any],
                  subject: str, model: str, seed: int, output_dir: Path,
                  vision_reader: VisionReader, max_iterations: int = 3) -> IterationResult:
    """Bounded generate→vision→critic→correct loop.

    The vision_reader boundary is explicit so Doré can later plug in its real vision faculty
    without coupling image generation to a particular model/provider.
    """
    if max_iterations < 1 or max_iterations > 8:
        raise ValueError("max_iterations must be between 1 and 8")
    steps: list[IterationStep] = []
    direction = ""
    for index in range(max_iterations):
        generation = generate_resident_image(
            renderer=renderer,
            template=template,
            brief=brief,
            subject=subject,
            model=model,
            seed=seed + index,
            output_dir=output_dir,
            correction_direction=direction,
        )
        image_path = Path(generation.artifact.uri)
        observations = dict(vision_reader(image_path, generation.recipe, brief))
        critique = critique_from_observations(generation.recipe, observations, real_visual_review=True)
        steps.append(IterationStep(index, generation, critique))
        if critique.accepted:
            return IterationResult(True, tuple(steps), "accepted")
        direction = correction_direction(critique)
        if not direction:
            return IterationResult(False, tuple(steps), "critic-returned-no-correction")
    return IterationResult(False, tuple(steps), "iteration-limit")
