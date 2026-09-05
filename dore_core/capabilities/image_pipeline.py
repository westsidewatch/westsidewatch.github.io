from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Mapping

from .image_artifacts import ImageArtifactRecord, persist_record, record_image
from .image_renderer import ComfyUIRenderer, RenderRequest
from .image_style import StyleRecipe, compile_editorial_recipe
from .image_workflow import WorkflowTemplate, compile_comfy_workflow


@dataclass(frozen=True)
class ResidentGenerationResult:
    artifact: ImageArtifactRecord
    recipe: dict[str, Any]
    workflow_id: str
    prompt_id: str
    critic_input: dict[str, Any]


def generate_resident_image(*, renderer: ComfyUIRenderer, template: WorkflowTemplate,
                            brief: Mapping[str, Any], subject: str, model: str, seed: int,
                            output_dir: Path, correction_direction: str = "") -> ResidentGenerationResult:
    """Execute Doré's local image path from brief to durable real bytes.

    This function does not install/start a renderer and does not mark visual quality accepted.
    It succeeds only after ComfyUI returns an image and those bytes are fetched locally.
    """
    recipe: StyleRecipe = compile_editorial_recipe(brief)
    workflow = compile_comfy_workflow(
        template,
        subject=subject,
        recipe=recipe,
        model=model,
        seed=seed,
        direction=correction_direction,
    )
    rendered = renderer.render(RenderRequest(workflow, seed=seed, model=model, workflow_id=template.id))
    first = rendered.images[0]
    output_dir.mkdir(parents=True, exist_ok=True)
    suffix = Path(first.get("filename", "image.png")).suffix or ".png"
    target = output_dir / f"{rendered.prompt_id}{suffix}"
    renderer.fetch_image(first, target)
    artifact = record_image(target, provenance=rendered.provenance, recipe=recipe.to_payload(), brief=dict(brief))
    persist_record(artifact, output_dir / f"{rendered.prompt_id}.json")
    critic_input = {
        "artifact_id": artifact.id,
        "image_path": artifact.uri,
        "sha256": artifact.sha256,
        "recipe": recipe.to_payload(),
        "brief": dict(brief),
        "real_visual_review": False,
        "acceptance_boundary": "requires actual vision observations before critique can accept",
    }
    return ResidentGenerationResult(artifact, recipe.to_payload(), template.id, rendered.prompt_id, critic_input)


def result_payload(result: ResidentGenerationResult) -> dict[str, Any]:
    return {
        "artifact": asdict(result.artifact),
        "recipe": result.recipe,
        "workflow_id": result.workflow_id,
        "prompt_id": result.prompt_id,
        "critic_input": result.critic_input,
    }
