#!/usr/bin/env python3
"""Normalize public Doré calls into the canonical dore.a2a/1 dispatch envelope.

This is an ingress boundary only. It does not resolve capability identity and it does
not execute handlers. All normal transports must converge here before Core dispatch.
"""
from __future__ import annotations

from typing import Any

PROTOCOL = "dore.a2a/1"


def _text(value: Any, fallback: str) -> str:
    text = str(value or "").strip()
    return text or fallback


def normalize_public_call(payload: dict[str, Any]) -> dict[str, Any]:
    """Convert legacy/public ``capability + args`` into one typed Core envelope."""
    capability = _text(payload.get("capability") or payload.get("capability_id"), "")
    if not capability:
        raise ValueError("capability_required")
    args = payload.get("args") if "args" in payload else payload.get("payload", {})
    if args is None:
        args = {}
    if not isinstance(args, dict):
        raise ValueError("args_must_be_object")

    request_id = _text(payload.get("request_id"), "local-request")
    caller = _text(payload.get("caller_product") or payload.get("consumer_id"), "dore-local")
    conversation_id = _text(payload.get("conversation_id"), f"local:{caller}")
    session_id = _text(payload.get("session_id"), "local-unix")

    return {
        "protocol": PROTOCOL,
        "action": "dispatch",
        "request_id": request_id,
        "conversation_id": conversation_id,
        "session_id": session_id,
        "consumer_id": caller,
        "capability_id": capability,
        "payload": dict(args),
        "ingress": {
            "normalized": True,
            "source": str(payload.get("transport") or "public-dore-call"),
            "original_shape": "capability-args" if "capability" in payload else "typed",
        },
    }


def is_typed_envelope(payload: dict[str, Any]) -> bool:
    return bool(
        isinstance(payload, dict)
        and payload.get("protocol") == PROTOCOL
        and payload.get("capability_id")
        and isinstance(payload.get("payload", {}), dict)
    )
