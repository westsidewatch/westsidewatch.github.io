from __future__ import annotations

from hashlib import sha256
from typing import Mapping

from .executor import CapabilityHandler
from .model import ArtifactRef, TaskState
from .runtime import LoadedCapability


def _payload(inputs: Mapping[str, ArtifactRef], schema: str) -> dict:
    return dict(inputs[schema].payload)


def visual_direct_handler(loaded: LoadedCapability, inputs: Mapping[str, ArtifactRef], state: TaskState) -> dict:
    seed = state.artifacts.get("request")
    need = dict(seed.payload).get("need", "visual asset") if seed else "visual asset"
    return {"visual_brief": {"need": need, "constraints": ["free-first", "shared-state"]}}


def visual_grammar_handler(loaded: LoadedCapability, inputs: Mapping[str, ArtifactRef], state: TaskState) -> dict:
    brief = _payload(inputs, "visual_brief")
    return {"style_recipe": {
        "family": "Dore Original",
        "intent": brief.get("need"),
        "rules": ["editorial hierarchy", "active negative space", "original composition"],
    }}


def image_generate_handler(loaded: LoadedCapability, inputs: Mapping[str, ArtifactRef], state: TaskState) -> dict:
    brief = _payload(inputs, "visual_brief")
    recipe = _payload(inputs, "style_recipe")
    signature = sha256(repr((brief, recipe)).encode("utf-8")).hexdigest()[:16]
    provider = loaded.providers[0] if loaded.providers else {"provider": "synthetic-local"}
    provider_id = provider.get("provider", "synthetic-local") if isinstance(provider, dict) else type(provider).__name__
    return {"asset_candidate": {
        "asset_id": f"synthetic:{signature}",
        "provider": provider_id,
        "kind": "test-double",
        "rendered": False,
        "claim_boundary": "synthetic evidence only; not a real generated image",
    }}


def image_critic_handler(loaded: LoadedCapability, inputs: Mapping[str, ArtifactRef], state: TaskState) -> dict:
    asset = _payload(inputs, "asset_candidate")
    return {"critique_result": {
        "accepted_for_pipeline_test": asset.get("kind") == "test-double",
        "real_visual_quality_verified": False,
        "boundary": "pipeline contract verified; visual quality remains unverified",
    }}


def design_compose_handler(loaded: LoadedCapability, inputs: Mapping[str, ArtifactRef], state: TaskState) -> dict:
    asset = _payload(inputs, "asset_candidate")
    return {"design_patch": {
        "operation": "insert-asset",
        "asset_id": asset.get("asset_id"),
        "workspace": "synthetic",
        "applied": False,
        "boundary": "structured patch contract only",
    }}


def design_verify_handler(loaded: LoadedCapability, inputs: Mapping[str, ArtifactRef], state: TaskState) -> dict:
    patch = _payload(inputs, "design_patch")
    return {"verification_result": {
        "contract_valid": patch.get("operation") == "insert-asset",
        "real_render_verified": False,
        "boundary": "end-to-end typed execution verified; real render pending",
    }}


def synthetic_visual_handlers() -> dict[str, CapabilityHandler]:
    return {
        "visual.direct": visual_direct_handler,
        "visual.grammar": visual_grammar_handler,
        "image.generate": image_generate_handler,
        "image.critic": image_critic_handler,
        "design.compose": design_compose_handler,
        "design.verify": design_verify_handler,
    }
