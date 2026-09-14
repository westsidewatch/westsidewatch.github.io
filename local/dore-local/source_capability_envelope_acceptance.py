#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("source_capability_envelope", HERE / "source_capability_envelope.py")
MOD = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MOD)


def base_probe(**overrides):
    probe = {
        "ok": True,
        "status": "completed",
        "schema": "dore.source-probe.v0",
        "sourcePointer": "https://example.org/watch/1",
        "resolvedSourcePointer": "https://example.org/watch/1",
        "sourceAuthority": True,
        "providerHint": "example.org",
        "capabilities": {"poster": [], "embed": [], "media": [], "manifest": [], "caption": [], "oembed": []},
        "needs": [],
        "provenance": {"networkUsed": True, "confidence": 0.9},
        "rights": {"rehost": False, "decision": "not-inferred-by-probe"},
    }
    probe.update(overrides)
    return probe


def test_static_media():
    probe = base_probe(capabilities={
        "poster": [{"url": "https://example.org/poster.jpg"}],
        "embed": [{"url": "https://example.org/embed/1"}],
        "media": [{"url": "https://cdn.example.org/1.mp4", "mime": "video/mp4"}],
        "manifest": [], "caption": [{"url": "https://example.org/1.vtt"}], "oembed": [],
    })
    env = MOD.project(probe)
    assert env["ok"] and env["schema"] == "dore.source-capability-envelope.v1"
    assert "static-http" in env["access"]["modes"]
    assert "embed" in env["access"]["modes"]
    assert {"video", "image", "captions", "text"}.issubset(set(env["media"]))
    assert {"read", "embed", "seek", "segment", "caption", "cite"}.issubset(set(env["operations"]))
    assert env["rights"]["rehost"] is False
    assert env["authority"]["identityClaimOnly"] is True
    assert env["authority"]["canonicalIdentityAuthority"] is False


def test_runtime_boundary_405():
    probe = base_probe(
        status="partial",
        capabilities={"poster": [], "embed": [], "media": [], "manifest": [], "caption": [], "oembed": []},
        needs=["runtime-browser-probe"],
        provenance={"networkUsed": True, "fetchBoundary": {"httpStatus": 405, "message": "Method Not Allowed"}, "confidence": 0.25},
    )
    env = MOD.project(probe)
    assert env["ok"]
    assert env["access"]["modes"] == ["browser-runtime"]
    assert env["access"]["staticFetchStatus"] == 405
    assert env["runtimeBoundary"] == {"required": True, "mode": "browser-runtime"}


def test_declared_mcp_is_capability_evidence_not_copy():
    env = MOD.project(base_probe(provenance={"networkUsed": False}), {
        "declaredAccess": ["mcp"],
        "declaredOperations": ["search", "read"],
        "declaredRights": {"citation": "allowed", "rehost": True},
    })
    assert "mcp" in env["access"]["modes"]
    assert env["access"]["preferred"] == "mcp"
    assert "search" in env["operations"]
    assert env["rights"]["claims"]["rehost"] is True
    assert env["rights"]["rehost"] is False
    assert env["persistence"] == "request-scoped-none"


def test_forbidden_source():
    probe = base_probe(sourcePointer="https://zh.wikisource.org/wiki/Test", resolvedSourcePointer="https://zh.wikisource.org/wiki/Test")
    env = MOD.project(probe)
    assert env["ok"] is False and env["status"] == "blocked"


def test_provider_neutral_source():
    text = (HERE / "source_capability_envelope.py").read_text(encoding="utf-8").casefold()
    assert "goodtv" not in text
    assert "youtube" not in text
    assert "reuters" not in text
    assert "cuttingroom" not in text


if __name__ == "__main__":
    test_static_media()
    test_runtime_boundary_405()
    test_declared_mcp_is_capability_evidence_not_copy()
    test_forbidden_source()
    test_provider_neutral_source()
    print("DORE_SOURCE_CAPABILITY_ENVELOPE_SCHEMA=PASS")
    print("DORE_SOURCE_CAPABILITY_405_RUNTIME_BOUNDARY=PASS")
    print("DORE_SOURCE_CAPABILITY_MCP_EVIDENCE=PASS")
    print("DORE_SOURCE_CAPABILITY_RIGHTS_NON_INFERENCE=PASS")
    print("DORE_SOURCE_CAPABILITY_WIKISOURCE_GATE=PASS")
    print("DORE_SOURCE_CAPABILITY_PROVIDER_NEUTRAL=PASS")
