#!/usr/bin/env python3
"""Doré semantic capability bus.

Products address Doré capabilities by semantic name. Runtime/provider addresses stay
behind Core adapters so product surfaces do not grow point-to-point wiring.
"""
from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
from typing import Any
from urllib import request

from dore_core.substrates.longmemory import LongMemoryConfig, available as longmemory_available, recall as longmemory_recall
from dore_core.substrates.qmd import QMDConfig, available as qmd_available, search as qmd_search

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
    "context.fuzzy-search": {
        "id": "context.fuzzy-search",
        "type": "context",
        "service": "retrieval",
        "status": "existing",
        "execution": "core-adapter",
        "provider": "qmd-local",
        "load": "deferred",
        "authority": False,
    },
    "knowledge.recall": {
        "id": "knowledge.recall",
        "type": "knowledge",
        "service": "memory",
        "status": "existing",
        "execution": "core-adapter",
        "provider": "longmemory-local",
        "load": "deferred",
        "authority": False,
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


def _fuzzy_search(args: dict[str, Any]) -> dict[str, Any]:
    query = str(args.get("query") or args.get("text") or "").strip()
    if not query:
        return {"ok": False, "status": "failed", "error": {"code": "invalid_args", "message": "query or text is required"}}
    if not qmd_available():
        return {"ok": False, "status": "not_ready", "capability": "context.fuzzy-search", "authority": False, "error": {"code": "substrate_unavailable", "message": "qmd is not installed on this runtime"}}
    semantic = bool(args.get("semantic", True))
    deep = bool(args.get("deep", False))
    collection = str(args.get("collection") or os.environ.get("DORE_QMD_COLLECTION") or "").strip() or None
    return qmd_search(query, QMDConfig(collection=collection), semantic=semantic, deep=deep, limit=int(args.get("limit") or 8))


def _knowledge_recall(args: dict[str, Any]) -> dict[str, Any]:
    query = str(args.get("query") or args.get("text") or "").strip()
    if not query:
        return {"ok": False, "status": "failed", "error": {"code": "invalid_args", "message": "query or text is required"}}
    if not longmemory_available():
        return {"ok": False, "status": "not_ready", "capability": "knowledge.recall", "authority": False, "error": {"code": "substrate_unavailable", "message": "longmemory is not installed on this runtime"}}
    db = Path(os.environ.get("DORE_LONGMEMORY_DB") or (Path.home() / ".dore" / "knowledge" / "longmemory.db"))
    project = str(args.get("project") or os.environ.get("DORE_LONGMEMORY_PROJECT") or "dore")
    mode = str(args.get("mode") or "strict")
    return longmemory_recall(query, LongMemoryConfig(db=db, project=project), mode=mode)


def call(capability: str, args: dict[str, Any], production, *, caller_product: str | None = None) -> dict[str, Any]:
    descriptor = resolve(capability, production)
    if descriptor is None:
        return {"ok": False, "status": "failed", "error": {"code": "capability_not_found", "message": capability}}
    try:
        if capability == "image.generate":
            return _image_generate(args, caller_product)
        if capability == "context.fuzzy-search":
            result = _fuzzy_search(args)
        elif capability == "knowledge.recall":
            result = _knowledge_recall(args)
        elif capability in production.CAPABILITIES:
            result = production.execute(capability, args)
        else:
            return {"ok": False, "status": "failed", "capability": capability, "error": {"code": "capability_not_callable", "message": "registered for discovery but not yet connected to the Core execution path"}}
    except Exception as exc:
        return {"ok": False, "status": "failed", "capability": capability, "error": {"code": "provider_error", "message": str(exc)}}
    if isinstance(result, dict):
        result = dict(result)
        result.setdefault("core_route", {"capability": capability, "caller_product": caller_product, "provider": descriptor.get("provider") or "production-actions", "transport": "core-adapter" if capability in NATIVE_CAPABILITIES else "in-process"})
    return result
