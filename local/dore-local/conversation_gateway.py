#!/usr/bin/env python3
"""Thin conversation-side gateway into the existing Doré A2A runtime.

This module owns no capability identity and no execution logic. It only
normalizes discover/describe/call requests and delegates them to the existing
A2A/native-host path.
"""
from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import native_host

GATEWAY_SCHEMA = "dore.conversation-gateway/1"


def _emit(payload: dict[str, Any]) -> dict[str, Any]:
    return {"schema": GATEWAY_SCHEMA, **payload}


def discover(query: str = "", consumer: str = "chatgpt-a2a") -> dict[str, Any]:
    needle = query.strip().lower()
    capabilities = native_host.discover_production(include_planned=False)
    if needle:
        capabilities = [
            item for item in capabilities
            if needle in json.dumps(item, ensure_ascii=False).lower()
        ]
    return _emit({"ok": True, "operation": "discover", "consumer": consumer, "capabilities": capabilities})


def describe(capability: str) -> dict[str, Any]:
    descriptor = native_host.resolve_production(capability)
    return _emit({
        "ok": descriptor is not None,
        "operation": "describe",
        "capability": capability,
        "descriptor": descriptor,
    })


def call(
    capability: str,
    args: dict[str, Any],
    *,
    consumer: str = "chatgpt-a2a",
    conversation_id: str | None = None,
    session_id: str | None = None,
    request_id: str = "conversation-gateway-request",
) -> dict[str, Any]:
    # native_host.route_payload is the existing normalization boundary. It
    # delegates execution into Doré's canonical A2A path; this gateway must
    # never import or invoke capability implementations directly.
    result = native_host.route_payload({
        "capability": capability,
        "args": args,
        "caller_product": consumer,
        "conversation_id": conversation_id,
        "session_id": session_id,
        "request_id": request_id,
        "transport": "conversation-gateway",
    })
    return _emit({
        "ok": bool(result.get("ok")) if isinstance(result, dict) else False,
        "operation": "call",
        "capability": capability,
        "result": result,
    })


def dispatch(request: dict[str, Any]) -> dict[str, Any]:
    operation = str(request.get("operation") or "").strip().lower()
    if operation == "discover":
        return discover(str(request.get("query") or ""), str(request.get("consumer") or "chatgpt-a2a"))
    if operation == "describe":
        capability = str(request.get("capability") or "")
        if not capability:
            return _emit({"ok": False, "operation": operation, "error": "capability_required"})
        return describe(capability)
    if operation == "call":
        capability = str(request.get("capability") or "")
        if not capability:
            return _emit({"ok": False, "operation": operation, "error": "capability_required"})
        args = request.get("args") or {}
        if not isinstance(args, dict):
            return _emit({"ok": False, "operation": operation, "error": "args_must_be_object"})
        return call(
            capability,
            args,
            consumer=str(request.get("consumer") or "chatgpt-a2a"),
            conversation_id=request.get("conversation_id"),
            session_id=request.get("session_id"),
            request_id=str(request.get("request_id") or "conversation-gateway-request"),
        )
    return _emit({"ok": False, "operation": operation or None, "error": "unsupported_operation"})


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("operation", choices=("discover", "describe", "call"))
    parser.add_argument("--query", default="")
    parser.add_argument("--capability", default="")
    parser.add_argument("--consumer", default="chatgpt-a2a")
    parser.add_argument("--args-json", default="{}")
    parser.add_argument("--conversation-id")
    parser.add_argument("--session-id")
    parser.add_argument("--request-id", default="conversation-gateway-cli")
    ns = parser.parse_args()
    try:
        args = json.loads(ns.args_json)
    except json.JSONDecodeError as exc:
        print(json.dumps(_emit({"ok": False, "error": "invalid_args_json", "detail": str(exc)}), ensure_ascii=False))
        return 2
    response = dispatch({
        "operation": ns.operation,
        "query": ns.query,
        "capability": ns.capability,
        "consumer": ns.consumer,
        "args": args,
        "conversation_id": ns.conversation_id,
        "session_id": ns.session_id,
        "request_id": ns.request_id,
    })
    print(json.dumps(response, ensure_ascii=False, separators=(",", ":")))
    return 0 if response.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
