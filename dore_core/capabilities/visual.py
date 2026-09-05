from __future__ import annotations

from typing import Any, Mapping
from uuid import uuid4

from .model import ArtifactRef, TaskState

VISUAL_SCHEMA_ORDER = (
    "visual_brief",
    "style_recipe",
    "asset_candidate",
    "critique_result",
    "design_patch",
    "verification_result",
)


def visual_artifact(
    state: TaskState,
    schema: str,
    payload: Mapping[str, Any],
    *,
    provenance: tuple[str, ...] = (),
    artifact_id: str | None = None,
) -> ArtifactRef:
    """Write one typed visual artifact into the shared Doré task state."""
    if schema not in VISUAL_SCHEMA_ORDER:
        raise ValueError(f"unsupported visual artifact schema: {schema}")
    artifact = ArtifactRef(
        id=artifact_id or f"{schema}:{uuid4().hex}",
        schema=schema,
        payload=dict(payload),
        provenance=provenance,
    )
    state.add_artifact(artifact)
    return artifact


def latest_visual_artifact(state: TaskState, schema: str) -> ArtifactRef | None:
    matches = [artifact for artifact in state.artifacts.values() if artifact.schema == schema]
    return matches[-1] if matches else None


def require_visual_inputs(state: TaskState, capability_inputs: tuple[str, ...]) -> dict[str, ArtifactRef]:
    resolved: dict[str, ArtifactRef] = {}
    missing: list[str] = []
    for schema in capability_inputs:
        artifact = latest_visual_artifact(state, schema)
        if artifact is None:
            missing.append(schema)
        else:
            resolved[schema] = artifact
    if missing:
        raise ValueError("missing typed task artifacts: " + ", ".join(missing))
    return resolved
