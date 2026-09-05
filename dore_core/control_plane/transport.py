from __future__ import annotations

from dataclasses import asdict
from typing import Any, Mapping

from .model import ControlRequest
from .runtime import ControlPlane

PROTOCOL = "dore.a2a/1"


class TransportError(ValueError):
    pass


def _required_text(envelope: Mapping[str, Any], key: str) -> str:
    value = envelope.get(key)
    if not isinstance(value, str) or not value.strip():
        raise TransportError(f"missing or invalid {key}")
    return value


def _result_payload(result) -> dict[str, Any]:
    payload = asdict(result)
    payload["protocol"] = PROTOCOL
    return payload


def handle_envelope(plane: ControlPlane, envelope: Mapping[str, Any]) -> dict[str, Any]:
    """Translate one Companion/:4312 JSON envelope to the in-process control plane.

    The resident HTTP server owns sockets/auth/origin checks. This adapter owns
    only the stable A2A JSON contract and never contains Design implementation
    logic. Unknown/malformed messages fail closed.
    """
    if not isinstance(envelope, Mapping):
        raise TransportError("envelope must be an object")
    if envelope.get("protocol") != PROTOCOL:
        raise TransportError("unsupported protocol")

    action = envelope.get("action", "dispatch")
    if action == "discover":
        return {
            "protocol": PROTOCOL,
            "status": "succeeded",
            "consumers": [asdict(consumer) for consumer in plane.discover()],
        }

    if action == "status":
        request_id = _required_text(envelope, "request_id")
        conversation_id = _required_text(envelope, "conversation_id")
        session_id = _required_text(envelope, "session_id")
        result = plane.status(request_id)
        if result is None:
            return {
                "protocol": PROTOCOL,
                "request_id": request_id,
                "status": "not_found",
            }
        if result.conversation_id != conversation_id or result.session_id != session_id:
            return {
                "protocol": PROTOCOL,
                "request_id": request_id,
                "status": "failed",
                "error": "status request is not bound to this conversation/session",
            }
        return _result_payload(result)

    if action != "dispatch":
        raise TransportError("unsupported action")

    payload = envelope.get("payload", {})
    if not isinstance(payload, Mapping):
        raise TransportError("payload must be an object")

    request = ControlRequest(
        request_id=_required_text(envelope, "request_id"),
        conversation_id=_required_text(envelope, "conversation_id"),
        session_id=_required_text(envelope, "session_id"),
        consumer_id=_required_text(envelope, "consumer_id"),
        capability_id=_required_text(envelope, "capability_id"),
        payload=dict(payload),
    )
    return _result_payload(plane.dispatch(request))
