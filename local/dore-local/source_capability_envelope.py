#!/usr/bin/env python3
"""Doré Source Capability Envelope v1.

Pure, request-scoped projection over `dore.source-probe.v0` evidence. The envelope
never becomes source/canonical authority, never rehosts media by inference, and
never introduces provider-specific branches.
"""
from __future__ import annotations

from typing import Any
from urllib.parse import urlparse

SCHEMA = "dore.source-capability-envelope.v1"
PROBE_SCHEMA = "dore.source-probe.v0"
BANNED_HOST_SUFFIXES = ("wikisource.org",)
SAFE_DECLARED_ACCESS = {"static-http", "browser-runtime", "mcp", "api", "iiif", "manifest", "embed", "local-file"}


def _host(url: str) -> str:
    return (urlparse(url).hostname or "").lower().rstrip(".")


def _allowed(url: str) -> bool:
    host = _host(url)
    return bool(host) and not any(host == suffix or host.endswith("." + suffix) for suffix in BANNED_HOST_SUFFIXES)


def _items(probe: dict[str, Any], key: str) -> list[dict[str, Any]]:
    value = (probe.get("capabilities") or {}).get(key) or []
    return [row for row in value if isinstance(row, dict)]


def _access_modes(probe: dict[str, Any], claims: dict[str, Any]) -> tuple[list[str], str | None, bool]:
    modes: set[str] = set()
    provenance = probe.get("provenance") or {}
    boundary = provenance.get("fetchBoundary") or {}
    status = boundary.get("httpStatus")

    if provenance.get("networkUsed") and not boundary:
        modes.add("static-http")
    if provenance.get("runtimeBrowserUsed") or status in (401, 403, 405, 406, 429) or "runtime-browser-probe" in (probe.get("needs") or []):
        modes.add("browser-runtime")
    if _items(probe, "embed"):
        modes.add("embed")
    if _items(probe, "manifest"):
        modes.add("manifest")

    declared = claims.get("declaredAccess") or []
    if isinstance(declared, str):
        declared = [declared]
    for mode in declared:
        if str(mode) in SAFE_DECLARED_ACCESS:
            modes.add(str(mode))

    order = ["mcp", "api", "iiif", "static-http", "browser-runtime", "manifest", "embed", "local-file"]
    ordered = [mode for mode in order if mode in modes]
    preferred = ordered[0] if ordered else None
    runtime_required = "browser-runtime" in modes and not any(m in modes for m in ("mcp", "api", "iiif", "static-http"))
    return ordered, preferred, runtime_required


def _media(probe: dict[str, Any]) -> list[str]:
    media: set[str] = set()
    if _items(probe, "poster"):
        media.add("image")
    if _items(probe, "caption"):
        media.update(("captions", "text"))
    if _items(probe, "manifest"):
        media.update(("manifest", "video"))
    if _items(probe, "embed"):
        media.add("embedded-media")
    for item in _items(probe, "media"):
        mime = str(item.get("mime") or "").lower()
        if mime.startswith("video/"):
            media.add("video")
        elif mime.startswith("audio/"):
            media.add("audio")
        elif mime.startswith("image/"):
            media.add("image")
        else:
            media.add("media")
    return sorted(media)


def _operations(probe: dict[str, Any], modes: list[str], media: list[str], claims: dict[str, Any]) -> list[str]:
    ops: set[str] = {"cite"}
    if media or any(m in modes for m in ("static-http", "browser-runtime", "mcp", "api", "iiif", "local-file")):
        ops.add("read")
    if "embed" in modes:
        ops.add("embed")
    if "manifest" in modes or "video" in media or "audio" in media:
        ops.update(("seek", "segment"))
    if "captions" in media:
        ops.add("caption")
    if any(m in modes for m in ("mcp", "api")):
        ops.add("search")
    if media:
        ops.add("extract")

    declared = claims.get("declaredOperations") or []
    if isinstance(declared, str):
        declared = [declared]
    for op in declared:
        value = str(op).strip()
        if value:
            ops.add(value)
    return sorted(ops)


def _surface_hints(media: list[str], operations: list[str]) -> list[str]:
    hints = {"search"}
    if any(k in media for k in ("video", "audio", "embedded-media", "manifest")):
        hints.add("cinema")
    if any(k in media for k in ("text", "image", "media")) or "read" in operations:
        hints.update(("dawn", "multiwrite"))
    if "image" in media:
        hints.add("design")
    if "text" in media or "caption" in operations:
        hints.add("one")
    return sorted(hints)


def project(probe: dict[str, Any], claims: dict[str, Any] | None = None) -> dict[str, Any]:
    claims = claims or {}
    if probe.get("schema") != PROBE_SCHEMA:
        return {"ok": False, "status": "failed", "schema": SCHEMA, "error": {"code": "invalid_probe_schema"}}

    pointer = str(probe.get("resolvedSourcePointer") or probe.get("sourcePointer") or "").strip()
    if not pointer or not _allowed(pointer):
        return {"ok": False, "status": "blocked", "schema": SCHEMA, "sourcePointer": pointer or None,
                "sourcePolicy": {"allowed": False, "reason": "source-policy-deny"}}

    modes, preferred, runtime_required = _access_modes(probe, claims)
    media = _media(probe)
    operations = _operations(probe, modes, media, claims)
    probe_rights = probe.get("rights") or {}
    declared_rights = claims.get("declaredRights") if isinstance(claims.get("declaredRights"), dict) else {}

    # Rights claims are recorded as evidence; rehost remains false unless an
    # explicit rights authority later admits such a grant outside this projector.
    rights = {
        "rehost": False,
        "decision": str(probe_rights.get("decision") or "not-inferred-by-envelope"),
        "claims": declared_rights,
        "requiresRightsAdmissionFor": ["rehost", "redistribute"],
    }

    boundary_mode = "browser-runtime" if runtime_required else (preferred or "unresolved")
    return {
        "ok": True,
        "status": "completed",
        "schema": SCHEMA,
        "sourcePointer": pointer,
        "authority": {
            "sourceIsAuthority": bool(probe.get("sourceAuthority", True)),
            "identityClaimOnly": True,
            "canonicalIdentityAuthority": False,
            "envelopeAuthority": False,
        },
        "access": {
            "modes": modes,
            "preferred": preferred,
            "staticFetchStatus": ((probe.get("provenance") or {}).get("fetchBoundary") or {}).get("httpStatus"),
        },
        "media": media,
        "operations": operations,
        "rights": rights,
        "runtimeBoundary": {"required": runtime_required, "mode": boundary_mode},
        "editorialBoundary": {
            "canonRequiredFor": ["publish", "material-transform", "rehost"],
            "sourceContentMayBeRewrittenSilently": False,
        },
        "surfaceHints": _surface_hints(media, operations),
        "provenance": {
            "probeSchema": PROBE_SCHEMA,
            "probeStatus": probe.get("status"),
            "providerHint": probe.get("providerHint"),
            "probeProvenance": probe.get("provenance") or {},
            "declaredCapabilityEvidence": bool(claims),
        },
        "persistence": "request-scoped-none",
    }


def execute(args: dict[str, Any]) -> dict[str, Any]:
    probe = args.get("probe")
    if not isinstance(probe, dict):
        return {"ok": False, "status": "failed", "error": {"code": "probe_required"}}
    claims = args.get("claims") if isinstance(args.get("claims"), dict) else {}
    return project(probe, claims)
