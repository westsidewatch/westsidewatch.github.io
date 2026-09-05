from __future__ import annotations

import json
from typing import Mapping, Any
from urllib import request

from .executor import CapabilityHandler
from .model import ArtifactRef, TaskState
from .runtime import LoadedCapability

DESIGN_BASE_URL = "http://127.0.0.1:4310"


def _payload(inputs: Mapping[str, ArtifactRef], schema: str) -> dict[str, Any]:
    return dict(inputs[schema].payload)


def _json_get(path: str, timeout: float = 2.5) -> dict[str, Any]:
    with request.urlopen(f"{DESIGN_BASE_URL}{path}", timeout=timeout) as response:
        body = json.loads(response.read().decode("utf-8"))
    if not isinstance(body, dict):
        raise TypeError("Doré Design response must be an object")
    return body


def _json_post(path: str, payload: Mapping[str, Any], timeout: float = 2.5) -> dict[str, Any]:
    raw = json.dumps(dict(payload), ensure_ascii=False).encode("utf-8")
    req = request.Request(
        f"{DESIGN_BASE_URL}{path}",
        data=raw,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with request.urlopen(req, timeout=timeout) as response:
        body = json.loads(response.read().decode("utf-8"))
    if not isinstance(body, dict):
        raise TypeError("Doré Design response must be an object")
    return body


def design_compose_handler(
    loaded: LoadedCapability,
    inputs: Mapping[str, ArtifactRef],
    state: TaskState,
) -> dict[str, Any]:
    asset = _payload(inputs, "asset_candidate")
    mutation = asset.get("workspace_mutation")

    # The /dore design production live gate intentionally does not mutate the
    # user's workspace. Real product work supplies a typed workspace_mutation.
    if mutation is None:
        health = _json_get("/api/verify")
        return {"design_patch": {
            "operation": "resident-design-ready",
            "asset_id": asset.get("asset_id"),
            "workspace": health.get("document_id", "westside-watch"),
            "revision": health.get("revision"),
            "applied": False,
            "verified": bool(health.get("ok")),
            "boundary": "resident Doré Design reached; no mutation requested",
        }}

    if not isinstance(mutation, Mapping):
        raise TypeError("workspace_mutation must be an object")

    before = _json_get("/api/verify")
    changed = _json_post("/api/workspace", mutation)
    after = _json_get("/api/verify")
    if not after.get("ok"):
        raise RuntimeError("Doré Design verification failed after mutation")

    before_revision = before.get("revision")
    after_revision = after.get("revision")
    if isinstance(before_revision, int) and isinstance(after_revision, int) and after_revision <= before_revision:
        raise RuntimeError("Doré Design mutation did not advance workspace revision")

    return {"design_patch": {
        "operation": mutation.get("op", "workspace-mutation"),
        "asset_id": asset.get("asset_id"),
        "workspace": after.get("document_id", "westside-watch"),
        "revision_before": before_revision,
        "revision_after": after_revision,
        "applied": True,
        "verified": True,
        "workspace_result": changed,
        "render_sha256": after.get("page_render_sha256", {}),
        "boundary": "real resident Doré Design workspace mutation",
    }}


def design_verify_handler(
    loaded: LoadedCapability,
    inputs: Mapping[str, ArtifactRef],
    state: TaskState,
) -> dict[str, Any]:
    patch = _payload(inputs, "design_patch")
    verification = _json_get("/api/verify")
    return {"verification_result": {
        "contract_valid": bool(patch.get("operation")),
        "resident_workspace": verification.get("document_id"),
        "revision": verification.get("revision"),
        "real_render_verified": bool(verification.get("ok")),
        "checks": verification.get("checks", {}),
        "page_render_sha256": verification.get("page_render_sha256", {}),
        "boundary": "resident Doré Design render and structure verification",
    }}


def resident_design_handlers() -> dict[str, CapabilityHandler]:
    return {
        "design.compose": design_compose_handler,
        "design.verify": design_verify_handler,
    }
