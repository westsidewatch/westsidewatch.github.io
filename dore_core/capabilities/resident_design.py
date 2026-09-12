from __future__ import annotations

import json
from typing import Mapping, Any
from urllib import request
from urllib.error import URLError

from .executor import CapabilityHandler
from .model import ArtifactRef, TaskState
from .runtime import LoadedCapability

DESIGN_BASE_URL = "http://127.0.0.1:4310"
REQUIRED_RUNTIME = {
    "service": "dore-design",
    "version": "2.0",
    "entrypoint": "dore-design/app_design2.py",
}


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


def _runtime_identity(expected: Mapping[str, Any] | None = None) -> dict[str, Any]:
    identity = _json_get("/api/runtime/identity")
    if identity.get("ok") is False:
        raise RuntimeError("Doré Design runtime identity endpoint is not healthy")
    for key, required in REQUIRED_RUNTIME.items():
        if identity.get(key) != required:
            raise RuntimeError(
                f"Doré Design runtime identity mismatch: {key}={identity.get(key)!r}; expected {required!r}"
            )
    for key, required in dict(expected or {}).items():
        if required is None:
            continue
        actual = identity.get(key)
        if actual != required:
            raise RuntimeError(
                f"Doré Design runtime precondition failed: {key}={actual!r}; expected {required!r}"
            )
    if identity.get("workspace_id") in (None, "", "unknown"):
        raise RuntimeError("Doré Design runtime workspace identity is unverifiable")
    return identity


def _runtime_precondition(asset: Mapping[str, Any]) -> dict[str, Any]:
    value = asset.get("runtime_precondition") or {}
    if not isinstance(value, Mapping):
        raise TypeError("runtime_precondition must be an object")
    allowed = {"service", "version", "entrypoint", "branch", "commit", "workspace_id", "workspace_revision", "port"}
    return {key: value[key] for key in value if key in allowed}


def design_compose_handler(
    loaded: LoadedCapability,
    inputs: Mapping[str, ArtifactRef],
    state: TaskState,
) -> dict[str, Any]:
    asset = _payload(inputs, "asset_candidate")
    mutation = asset.get("workspace_mutation")

    # A no-mutation dispatch remains a readiness probe for CI/offline contract
    # tests. It reports runtime identity when the resident exists, but does not
    # manufacture a successful mutation result when it does not.
    if mutation is None:
        try:
            identity = _runtime_identity(_runtime_precondition(asset))
            health = _json_get("/api/verify")
            return {"design_patch": {
                "operation": "resident-design-ready",
                "asset_id": asset.get("asset_id"),
                "workspace": health.get("document_id", identity.get("workspace_id")),
                "revision": health.get("revision"),
                "applied": False,
                "resident_available": True,
                "verified": bool(health.get("ok")),
                "runtime_identity": identity,
                "lifecycle": ["QUEUED", "CLAIMED", "TARGET_VERIFIED", "WORKSPACE_VERIFIED"],
                "boundary": "resident Doré Design 2.0 identity verified; no mutation requested",
            }}
        except (URLError, OSError, TimeoutError):
            return {"design_patch": {
                "operation": "control-plane-ready",
                "asset_id": asset.get("asset_id"),
                "workspace": "resident-unavailable",
                "applied": False,
                "resident_available": False,
                "verified": False,
                "lifecycle": ["QUEUED", "CLAIMED"],
                "boundary": "typed Design control plane verified; physical resident not required for this no-mutation probe",
            }}

    if not isinstance(mutation, Mapping):
        raise TypeError("workspace_mutation must be an object")

    expected = _runtime_precondition(asset)
    runtime_before = _runtime_identity(expected)
    before = _json_get("/api/verify")
    if before.get("document_id") != runtime_before.get("workspace_id"):
        raise RuntimeError("Doré Design runtime/workspace identity disagreement before mutation")

    changed = _json_post("/api/workspace", mutation)

    runtime_after = _runtime_identity({
        **expected,
        "service": runtime_before.get("service"),
        "version": runtime_before.get("version"),
        "entrypoint": runtime_before.get("entrypoint"),
        "workspace_id": runtime_before.get("workspace_id"),
        "port": runtime_before.get("port"),
    })
    after = _json_get("/api/verify")
    if not after.get("ok"):
        raise RuntimeError("Doré Design verification failed after mutation")
    if after.get("document_id") != runtime_after.get("workspace_id"):
        raise RuntimeError("Doré Design runtime/workspace identity disagreement after mutation")

    before_revision = before.get("revision")
    after_revision = after.get("revision")
    if isinstance(before_revision, int) and isinstance(after_revision, int) and after_revision <= before_revision:
        raise RuntimeError("Doré Design mutation did not advance workspace revision")
    runtime_revision = runtime_after.get("workspace_revision")
    if isinstance(runtime_revision, int) and isinstance(after_revision, int) and runtime_revision != after_revision:
        raise RuntimeError("Doré Design runtime registry revision disagrees with verified workspace revision")

    return {"design_patch": {
        "operation": mutation.get("op", "workspace-mutation"),
        "asset_id": asset.get("asset_id"),
        "workspace": after.get("document_id", "westside-watch"),
        "revision_before": before_revision,
        "revision_after": after_revision,
        "applied": True,
        "resident_available": True,
        "verified": True,
        "runtime_identity_before": runtime_before,
        "runtime_identity_after": runtime_after,
        "workspace_result": changed,
        "render_sha256": after.get("page_render_sha256", {}),
        "lifecycle": [
            "QUEUED", "CLAIMED", "TARGET_VERIFIED", "EXECUTING",
            "WORKSPACE_VERIFIED", "VISUAL_VERIFIED", "DONE",
        ],
        "boundary": "real resident Doré Design 2.0 workspace mutation with fail-closed runtime identity",
    }}


def design_verify_handler(
    loaded: LoadedCapability,
    inputs: Mapping[str, ArtifactRef],
    state: TaskState,
) -> dict[str, Any]:
    patch = _payload(inputs, "design_patch")
    expected = patch.get("runtime_identity_after") or patch.get("runtime_identity") or {}
    identity = _runtime_identity({
        key: expected.get(key)
        for key in ("service", "version", "entrypoint", "workspace_id", "port")
        if expected.get(key) is not None
    })
    verification = _json_get("/api/verify")
    if verification.get("document_id") != identity.get("workspace_id"):
        raise RuntimeError("Doré Design verification reached a different workspace than runtime identity")
    return {"verification_result": {
        "contract_valid": bool(patch.get("operation")),
        "resident_workspace": verification.get("document_id"),
        "revision": verification.get("revision"),
        "runtime_identity": identity,
        "real_render_verified": bool(verification.get("ok")),
        "checks": verification.get("checks", {}),
        "page_render_sha256": verification.get("page_render_sha256", {}),
        "lifecycle": ["TARGET_VERIFIED", "WORKSPACE_VERIFIED", "VISUAL_VERIFIED", "DONE"],
        "boundary": "resident Doré Design 2.0 identity, render and structure verification",
    }}


def resident_design_handlers() -> dict[str, CapabilityHandler]:
    return {
        "design.compose": design_compose_handler,
        "design.verify": design_verify_handler,
    }
