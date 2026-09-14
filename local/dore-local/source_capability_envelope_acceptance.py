#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SPEC = importlib.util.spec_from_file_location("source_capability_envelope", HERE / "source_capability_envelope.py")
MOD = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MOD)
DAWN_SPEC = importlib.util.spec_from_file_location("dawn_source_capability_map", ROOT / "scripts/build_dawn_source_capability_map.py")
DAWN = importlib.util.module_from_spec(DAWN_SPEC)
assert DAWN_SPEC and DAWN_SPEC.loader
DAWN_SPEC.loader.exec_module(DAWN)


def base_probe(**overrides):
    probe = {
        "ok": True, "status": "completed", "schema": "dore.source-probe.v0",
        "sourcePointer": "https://example.org/watch/1", "resolvedSourcePointer": "https://example.org/watch/1",
        "sourceAuthority": True, "providerHint": "example.org",
        "capabilities": {"poster": [], "embed": [], "media": [], "manifest": [], "caption": [], "oembed": []},
        "needs": [], "provenance": {"networkUsed": True, "confidence": 0.9},
        "rights": {"rehost": False, "decision": "not-inferred-by-probe"},
    }
    probe.update(overrides)
    return probe


def assert_dispatch(env, mode, requires_runtime, status):
    dispatch = env["dispatch"]
    assert dispatch["schema"] == "dore.source-dispatch.v1"
    assert dispatch["ok"] is True
    assert dispatch["mode"] == mode
    assert dispatch["requiresRuntime"] is requires_runtime
    assert dispatch["status"] == status
    assert env["runtimeBoundary"]["required"] is requires_runtime


def test_static_media():
    probe = base_probe(capabilities={
        "poster": [{"url": "https://example.org/poster.jpg"}], "embed": [{"url": "https://example.org/embed/1"}],
        "media": [{"url": "https://cdn.example.org/1.mp4", "mime": "video/mp4"}], "manifest": [],
        "caption": [{"url": "https://example.org/1.vtt"}], "oembed": [],
    })
    env = MOD.project(probe)
    assert env["ok"] and env["schema"] == "dore.source-capability-envelope.v1"
    assert {"video", "image", "captions", "text"}.issubset(set(env["media"]))
    assert env["rights"]["rehost"] is False
    assert_dispatch(env, "static-http", False, "ready")


def test_runtime_boundary_405():
    probe = base_probe(status="partial", needs=["runtime-browser-probe"], provenance={"networkUsed": True, "fetchBoundary": {"httpStatus": 405}, "confidence": 0.25})
    env = MOD.project(probe)
    assert env["access"]["staticFetchStatus"] == 405
    assert_dispatch(env, "browser-runtime", True, "runtime-required")


def test_declared_mcp():
    env = MOD.project(base_probe(provenance={"networkUsed": False}), {"declaredAccess": ["mcp"], "declaredOperations": ["search", "read"], "declaredRights": {"rehost": True}})
    assert env["rights"]["rehost"] is False
    assert env["rights"]["claims"]["rehost"] is True
    assert_dispatch(env, "mcp", False, "ready")


def test_dawn_consumer_uses_dispatch():
    storefront = {"shelves": [{"items": [{"id": "source:1", "source": {"provider": "archive", "url": "https://example.org/book/1"}}]}]}
    identity = {"schema": "dore.source-identity-admission.v1", "claims": {"source:1": {"canonicalWorkId": "dawn:test", "status": "fallback-local", "sourcePointer": "https://example.org/book/1", "sourceAuthority": "archive"}}}
    result = DAWN.build(storefront, identity)
    row = result["claims"]["source:1"]
    assert row["status"] == "static-ready"
    assert row["dispatch"]["materializationReady"] is True
    assert row["dispatch"]["mode"] == "static-http"


def test_consumer_policy_is_not_reimplemented():
    dawn = (ROOT / "scripts/build_dawn_source_capability_map.py").read_text(encoding="utf-8")
    gate = (ROOT / "scripts/dawn_materialization_gate.py").read_text(encoding="utf-8")
    multiwrite = (ROOT / "static/multiwrite/source-capability-admission.mjs").read_text(encoding="utf-8")
    cinema = (ROOT / "local/dore-companion-extension/runtime_probe_background.js").read_text(encoding="utf-8")
    assert "projected.get('dispatch')" in dawn
    assert "access.get('preferred')" not in dawn
    assert "dispatch.get('materializationReady')" in gate
    assert "access.get('preferred')" not in gate
    assert "envelope.dispatch" in multiwrite
    assert "envelope.runtimeBoundary" not in multiwrite
    assert "needs.includes('runtime-browser-probe')" not in cinema
    assert "initialEnvelope.access" not in cinema


def test_forbidden_source():
    env = MOD.project(base_probe(sourcePointer="https://zh.wikisource.org/wiki/Test", resolvedSourcePointer="https://zh.wikisource.org/wiki/Test"))
    assert env["ok"] is False and env["status"] == "blocked"


def test_provider_neutral():
    text = ((HERE / "source_capability_envelope.py").read_text() + (HERE / "source_dispatcher.py").read_text()).casefold()
    for provider in ("goodtv", "youtube", "reuters", "cuttingroom"):
        assert provider not in text


if __name__ == "__main__":
    test_static_media(); test_runtime_boundary_405(); test_declared_mcp(); test_dawn_consumer_uses_dispatch(); test_consumer_policy_is_not_reimplemented(); test_forbidden_source(); test_provider_neutral()
    print("DORE_SOURCE_DISPATCHER_SCHEMA=PASS")
    print("DORE_SOURCE_DISPATCHER_STATIC=PASS")
    print("DORE_SOURCE_DISPATCHER_RUNTIME_405=PASS")
    print("DORE_SOURCE_DISPATCHER_MCP=PASS")
    print("DORE_SOURCE_DISPATCHER_DAWN=PASS")
    print("DORE_SOURCE_DISPATCHER_MULTIWRITE=PASS")
    print("DORE_SOURCE_DISPATCHER_CINEMA_NO_RAW_ACCESS_REINTERPRETATION=PASS")
    print("DORE_SOURCE_DISPATCHER_PROVIDER_NEUTRAL=PASS")
    print("DORE_SOURCE_CAPABILITY_WIKISOURCE_GATE=PASS")
