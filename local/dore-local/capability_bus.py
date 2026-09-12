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

from dore_core.bible.query_planner import plan_bible_query
from dore_core.retrieval.living import retrieve as living_retrieve
from dore_core.substrates.longmemory import LongMemoryConfig, available as longmemory_available, recall as longmemory_recall
from dore_core.substrates.qmd import (
    PRODUCTION_COLLECTION,
    QMDConfig,
    available as qmd_available,
    production_config,
    search as qmd_search,
)

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
BOOK_INTELLIGENCE = _load_sibling("book_intelligence_capability")

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
        "provider": "dore-search",
        "load": "deferred",
        "authority": False,
        "result": "dore-search-results",
        "identity": "dore",
        "execution_policy": "lowest-sufficient-capability",
    },
    "bible.query-plan": {
        "id": "bible.query-plan",
        "type": "context",
        "service": "bible-routing",
        "status": "existing",
        "execution": "in-process",
        "provider": "dore-core",
        "load": "always-light",
        "authority": False,
        "result": "bible-query-plan",
        "identity": "dore",
        "execution_policy": "lowest-sufficient-capability",
        "model_required": False,
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
    "publishing.book-intelligence": {
        "id": "publishing.book-intelligence",
        "type": "reasoning",
        "service": "publishing",
        "status": "existing",
        "execution": "core-adapter",
        "provider": "dore-core",
        "load": "on-demand",
        "result": "book-intelligence-report",
        "identity": "dore",
        "provider_neutral": True,
        "author_thesis_authority": True,
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


def _book_intelligence(args: dict[str, Any]) -> dict[str, Any]:
    """Invoke semantic publishing intelligence through the local Doré inference seam.

    The publishing adapter stays provider-neutral. Loading the local runtime happens
    inside the injected callback so an unavailable inference runtime is converted by
    the adapter into a safe degraded report instead of failing the bookmaking path.
    """
    def infer(messages: list[dict[str, str]]) -> str:
        runtime = _load_sibling("dore_local")
        return runtime.ollama(messages)

    return BOOK_INTELLIGENCE.execute(args, infer)


def _search_host(args: dict[str, Any], caller_product: str | None) -> str:
    explicit = str(args.get("host") or "").strip().lower()
    if explicit:
        return explicit
    product = str(caller_product or "").strip().lower()
    if product == "one" or product.startswith("one-"):
        return "one"
    if product == "multiwrite" or product.startswith("multiwrite-"):
        return "multiwrite"
    return "unknown"


def _bible_query_plan(args: dict[str, Any]) -> dict[str, Any]:
    query = str(args.get("query") or args.get("text") or "").strip()
    if not query:
        return {"ok": False, "status": "failed", "error": {"code": "invalid_args", "message": "query or text is required"}}
    plan = plan_bible_query(
        query,
        explicit_search=bool(args.get("explicit_search", False)),
        deep=bool(args.get("deep", False)),
    )
    return {
        "ok": True,
        "status": "completed",
        "capability": "bible.query-plan",
        "plan": plan.to_dict(),
        "dore_identity": True,
        "large_model_invoked": False,
    }


def _fuzzy_search(args: dict[str, Any], caller_product: str | None = None) -> dict[str, Any]:
    query = str(args.get("query") or args.get("text") or "").strip()
    if not query:
        return {"ok": False, "status": "failed", "error": {"code": "invalid_args", "message": "query or text is required"}}
    if not qmd_available():
        return {"ok": False, "status": "not_ready", "capability": "context.fuzzy-search", "authority": False, "error": {"code": "substrate_unavailable", "message": "local retrieval substrate is not installed on this runtime"}}

    bible_plan = plan_bible_query(
        query,
        explicit_search=bool(args.get("explicit_search", False)),
        deep=bool(args.get("deep", False)),
    )

    requested_collection = str(args.get("collection") or os.environ.get("DORE_QMD_COLLECTION") or "").strip()
    if not requested_collection or requested_collection == PRODUCTION_COLLECTION:
        qmd_config = production_config(collection=PRODUCTION_COLLECTION)
    else:
        qmd_config = QMDConfig(collection=requested_collection)

    db = Path(os.environ.get("DORE_LONGMEMORY_DB") or (Path.home() / ".dore" / "knowledge" / "longmemory.db"))
    project = str(args.get("project") or os.environ.get("DORE_LONGMEMORY_PROJECT") or "dore")
    memory_config = LongMemoryConfig(db=db, project=project)

    def search_documents(text: str, *, semantic: bool, deep: bool, limit: int) -> dict[str, Any]:
        return qmd_search(text, qmd_config, semantic=semantic, deep=deep, limit=limit)

    def recall_current(text: str, *, mode: str) -> dict[str, Any]:
        if not longmemory_available():
            return {"ok": False, "authority": False, "error": "memory_unavailable"}
        return longmemory_recall(text, memory_config, mode=mode)

    internal = living_retrieve(
        query,
        qmd_search=search_documents,
        memory_recall=recall_current,
        explicit_search=bool(args.get("explicit_search", False)),
        deep_requested=bool(args.get("deep", False)),
        limit=int(args.get("limit") or 8),
        host=_search_host(args, caller_product),
        mode=str(args.get("mode") or "prepare").strip().lower(),
        embedded=bool(args.get("embedded", False)),
    )
    plan = internal["plan"]
    return {
        "ok": internal.get("ok", False),
        "status": "completed" if internal.get("ok", False) else "failed",
        "capability": "context.fuzzy-search",
        "query": query,
        "results": internal.get("results", []),
        "retrieval": {
            "lexical": plan.lexical,
            "semantic": plan.semantic,
            "deep": plan.deep,
            "memory_recall": plan.recall_memory,
            "reason": plan.reason,
        },
        "bible_plan": bible_plan.to_dict(),
        "capability_runtime": {
            "identity": "dore",
            "execution_policy": "lowest-sufficient-capability",
            "execution_level": bible_plan.execution_level,
            "model_invoked": False,
            "escalation_available": bible_plan.reasoning_allowed or bible_plan.semantic_allowed,
        },
        "context_policy": internal.get("context_policy"),
        "search_scope": "production" if qmd_config.collection == PRODUCTION_COLLECTION else "requested-collection",
        "authority": False,
        "large_model_invoked": False,
        "core_route": {
            "capability": "context.fuzzy-search",
            "caller_product": caller_product,
            "provider": "dore-search",
            "transport": "core-adapter",
            "identity": "dore",
        },
    }


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
        if capability == "publishing.book-intelligence":
            result = _book_intelligence(args)
        elif capability == "bible.query-plan":
            result = _bible_query_plan(args)
        elif capability == "context.fuzzy-search":
            result = _fuzzy_search(args, caller_product)
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
