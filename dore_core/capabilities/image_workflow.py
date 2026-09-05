from __future__ import annotations

import copy
from dataclasses import dataclass
from typing import Any, Mapping

from .image_style import StyleRecipe


@dataclass(frozen=True)
class WorkflowTemplate:
    id: str
    graph: dict[str, Any]
    positive_node: str = "6"
    negative_node: str = "7"
    sampler_node: str = "3"
    checkpoint_node: str = "4"


def recipe_prompt(subject: str, recipe: StyleRecipe, *, direction: str = "") -> str:
    parts = [
        subject.strip(),
        f"editorial print, {recipe.reproduction}",
        f"{recipe.dominant_ink} dominant ink",
        "visible warm paper",
        *recipe.composition,
        *recipe.typography,
    ]
    if recipe.accent_ink:
        parts.append(f"{recipe.accent_ink} accent ink")
    if direction.strip():
        parts.append(direction.strip())
    return ", ".join(p for p in parts if p)


def compile_comfy_workflow(template: WorkflowTemplate, *, subject: str, recipe: StyleRecipe,
                           model: str, seed: int, negative: str = "photorealistic gloss, generic stock poster",
                           direction: str = "") -> dict[str, Any]:
    """Bind Doré semantics to a provider graph without letting provider syntax leak upward."""
    graph = copy.deepcopy(template.graph)
    required = (template.positive_node, template.negative_node, template.sampler_node, template.checkpoint_node)
    missing = [node for node in required if node not in graph]
    if missing:
        raise ValueError(f"workflow template missing nodes: {missing}")
    graph[template.positive_node].setdefault("inputs", {})["text"] = recipe_prompt(subject, recipe, direction=direction)
    graph[template.negative_node].setdefault("inputs", {})["text"] = negative
    graph[template.sampler_node].setdefault("inputs", {})["seed"] = int(seed)
    graph[template.checkpoint_node].setdefault("inputs", {})["ckpt_name"] = model
    return graph


def template_from_payload(payload: Mapping[str, Any]) -> WorkflowTemplate:
    graph = payload.get("graph")
    if not isinstance(graph, dict):
        raise ValueError("workflow payload requires graph object")
    return WorkflowTemplate(
        id=str(payload.get("id", "dore.comfy.template")), graph=dict(graph),
        positive_node=str(payload.get("positive_node", "6")), negative_node=str(payload.get("negative_node", "7")),
        sampler_node=str(payload.get("sampler_node", "3")), checkpoint_node=str(payload.get("checkpoint_node", "4")),
    )
