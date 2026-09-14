#!/usr/bin/env python3
"""Doré Universal Source Dispatcher v1.

Single provider-neutral access-routing decision over a Source Capability Envelope.
Products consume this decision; they must not independently reinterpret access modes.
"""
from __future__ import annotations
from typing import Any

SCHEMA = "dore.source-dispatch.v1"
ENVELOPE_SCHEMA = "dore.source-capability-envelope.v1"
ROUTE_ORDER = ("local-file", "mcp", "api", "iiif", "static-http", "manifest", "embed", "browser-runtime")


def dispatch(envelope: dict[str, Any]) -> dict[str, Any]:
    if envelope.get("schema") != ENVELOPE_SCHEMA or envelope.get("ok") is not True:
        return {"ok": False, "status": "blocked", "schema": SCHEMA, "reason": "invalid-capability-envelope"}

    modes = [str(x) for x in ((envelope.get("access") or {}).get("modes") or [])]
    modes = [mode for mode in ROUTE_ORDER if mode in modes]
    runtime = envelope.get("runtimeBoundary") or {}
    runtime_required = runtime.get("required") is True

    if runtime_required:
        if "browser-runtime" not in modes:
            return {"ok": False, "status": "blocked", "schema": SCHEMA, "reason": "runtime-required-without-runtime-route"}
        route = "browser-runtime"
        status = "runtime-required"
    else:
        route = next((mode for mode in ROUTE_ORDER if mode in modes and mode != "browser-runtime"), None)
        if route is None and "browser-runtime" in modes:
            route = "browser-runtime"
            status = "runtime-required"
            runtime_required = True
        elif route is None:
            return {"ok": False, "status": "unresolved", "schema": SCHEMA, "reason": "no-access-route"}
        else:
            status = "ready"

    route_class = (
        "local" if route == "local-file" else
        "protocol" if route in {"mcp", "api", "iiif"} else
        "static" if route in {"static-http", "manifest"} else
        "embedded" if route == "embed" else
        "runtime"
    )
    return {
        "ok": True,
        "status": status,
        "schema": SCHEMA,
        "mode": route,
        "routeClass": route_class,
        "requiresRuntime": runtime_required,
        "materializationReady": route in {"local-file", "static-http"} and not runtime_required,
        "sourcePointer": envelope.get("sourcePointer"),
        "providerSpecificRouting": False,
        "authority": False,
        "persistence": "request-scoped-none",
    }


def execute(args: dict[str, Any]) -> dict[str, Any]:
    envelope = args.get("envelope")
    if not isinstance(envelope, dict):
        return {"ok": False, "status": "failed", "schema": SCHEMA, "reason": "envelope-required"}
    return dispatch(envelope)
