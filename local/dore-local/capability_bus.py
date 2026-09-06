#!/usr/bin/env python3
"""Doré semantic capability bus.

Products address Doré capabilities by semantic name. Runtime/provider addresses stay
behind Core adapters so product surfaces do not grow point-to-point wiring.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Any
from urllib import request

HERE = Path(__file__).resolve().parent


def _load_sibling(name: str):
    path = HERE / f"{name}.py"
    spec = importlib.util.spec_from_file_location(f"dore_bus_{name}", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


REGISTRY = _load_sibling("capability_registry")

NATIVE_CAPABILITIES: dict[str, dict[str, Any]] = {
    "image.generate": {
        "id": "image.generate",
        "type": "production",
        "service": "visual",
        "status": "existing",
        "execution": "core-adapter",
        "provider": "dore-image-local",
        "load": "on-demand",
        "result": "image-artifact",
    },
}


def _post_json(url: str, payload: dict[str, Any], headers: dict[str, str] | None = None, timeout: int = 1500) -> dict[str, Any]:
    raw = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    merged = {"Content-Type": "application/json", "Accept": "application/json"}
    merged.update(headers or {})
    req = request.Request(url, data=raw, method="POST", headers=merged)
    with request.urlopen(req, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def discover(production, *, include_planned: bool = False) -> list[dict[str, Any]]:
    by_id: dict[str, dict[str, Any]] = {}
    for item in REGISTRY.discover(include_planned=include_planned):
        descriptor = dict(item)
        descriptor["owner"] = "dore-core"
        descriptor["callable"] = False
        by_id[str(descriptor["id"])] = descriptor
    for capability in sorted(production.CAPABILITIES):
        by_id[capability] = {
            "id": capability,
            "type": "production",
            "status": "existing",
            "execution": "production-action",
            "owner": "dore-core",
            "callable": True,
        }
    for capability, item in NATIVE_CAPABILITIES.items():
        descriptor = dict(item)
        descriptor["owner"] = "dore-core"
        descriptor["callable"] = True
        by_id[capability] = descriptor
    return [by_id[key] for key in sorted(by_id)]


def resolve(capability: str, production) -> dict[str, Any] | None:
    return next((item for item in discover(production, include_planned=True) if item.get("id") == capability), None)


def _image_generate(args: dict[str, Any], caller_product: str | None = None) -> dict[str, Any]:
    message = str(args.get("message") or args.get("prompt") or "").strip()
    if not message:
        return {"ok": False, "status": "failed", "error": {"code": "invalid_args", "message": "message or prompt is required"}}
    payload = dict(args)
    payload["message"] = message
    origin = caller_product or "dore-core"
    result = _post_json("http://127.0.0.1:8790/generate", payload, {"X-Dore-Origin": origin})
    if isinstance(result, dict):
        result = dict(result)
        result["core_route"] = {
            "capability": "image.generate",
            "caller_product": caller_product,
            "provider": "dore-image-local",
            "transport": "core-adapter",
        }
    return result


def call(capability: str, args: dict[str, Any], production, *, caller_product: str | None = None) -> dict[str, Any]:
    descriptor = resolve(capability, production)
    if descriptor is None:
        return {"ok": False, "status": "failed", "error": {"code": "capability_not_found", "message": capability}}
    if capability == "image.generate":
        try:
            return _image_generate(args, caller_product)
        except Exception as exc:
            return {"ok": False, "status": "failed", "capability": capability, "error": {"code": "provider_error", "message": str(exc)}}
    if capability in production.CAPABILITIES:
        result = production.execute(capability, args)
        if isinstance(result, dict):
            result = dict(result)
            result.setdefault("core_route", {"capability": capability, "caller_product": caller_product, "provider": "production-actions", "transport": "in-process"})
        return result
    return {"ok": False, "status": "failed", "capability": capability, "error": {"code": "capability_not_callable", "message": "registered for discovery but not yet connected to the Core execution path"}}
