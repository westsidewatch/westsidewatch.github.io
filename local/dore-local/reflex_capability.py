#!/usr/bin/env python3
"""Live request-scoped runtime capability for Doré Reflex v0."""
from __future__ import annotations

import base64
import binascii
from typing import Any, Callable

from reflex_contracts import ReflexSession, SourceDescriptor
from reflex_projections import project
from reflex_router import ReflexRouter

CAPABILITY_ID = "reflex.project"
RESULT_SCHEMA = "dore.reflex.runtime-result.v0"
SUPPORTED_INTENTS = {
    "text.search",
    "publishing.structure",
    "design.structure",
}


def _mapping(value: Any, field: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{field} must be an object")
    return value


def execute(
    args: dict[str, Any] | None,
    *,
    router: ReflexRouter | None = None,
    projector: Callable[[ReflexSession, str], dict[str, Any]] = project,
) -> dict[str, Any]:
    """Project one canonical source through a transient Reflex session.

    The public runtime boundary is JSON-safe: binary payload travels as base64.
    Reflex events/session state are never returned, and the session is always
    destroyed even when a downstream projector raises.
    """
    request = _mapping(args or {}, "args")
    intent = str(request.get("intent") or "")
    if intent not in SUPPORTED_INTENTS:
        return {
            "ok": False,
            "status": "failed",
            "capability": CAPABILITY_ID,
            "error": {"code": "unsupported_intent", "message": f"unsupported reflex projection: {intent}"},
        }

    source_data = _mapping(request.get("source"), "source")
    mime = str(source_data.get("mime") or "").strip()
    if not mime:
        return {
            "ok": False,
            "status": "failed",
            "capability": CAPABILITY_ID,
            "error": {"code": "invalid_args", "message": "source.mime is required"},
        }

    encoded = request.get("payloadBase64")
    if not isinstance(encoded, str):
        return {
            "ok": False,
            "status": "failed",
            "capability": CAPABILITY_ID,
            "error": {"code": "invalid_args", "message": "payloadBase64 must be a base64 string"},
        }
    try:
        payload = base64.b64decode(encoded, validate=True)
    except (binascii.Error, ValueError):
        return {
            "ok": False,
            "status": "failed",
            "capability": CAPABILITY_ID,
            "error": {"code": "invalid_args", "message": "payloadBase64 is invalid"},
        }

    source = SourceDescriptor(
        mime=mime,
        name=str(source_data.get("name") or ""),
        canonical_id=str(source_data.get("canonicalId") or ""),
        source_pointer=str(source_data.get("sourcePointer") or ""),
    )
    runtime_router = router or ReflexRouter()
    session = runtime_router.open(source, payload)
    try:
        output = projector(session, intent)
        return {
            "ok": True,
            "status": "completed",
            "capability": CAPABILITY_ID,
            "schema": RESULT_SCHEMA,
            "intent": intent,
            "adapter": session.adapter,
            "source": {
                "canonicalId": source.canonical_id,
                "sourcePointer": source.source_pointer,
            },
            "projection": output,
        }
    finally:
        session.close()
