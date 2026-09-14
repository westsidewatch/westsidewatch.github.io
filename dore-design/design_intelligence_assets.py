#!/usr/bin/env python3
"""Normalize Image Local output into request-scoped trusted Design assets.

Only the loopback Image Local asset endpoint is accepted. Provider URLs and
paths never enter candidate patches. Bytes are re-fetched, bounded, hashed and
stored under the request's private Doré home before an opaque asset_ref is
exposed to generation.
"""
from __future__ import annotations

import hashlib
import mimetypes
import os
import re
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

MAX_ASSET_BYTES = 16 * 1024 * 1024
ALLOWED_MIME = {"image/png", "image/jpeg", "image/webp"}
EXT_BY_MIME = {"image/png": ".png", "image/jpeg": ".jpg", "image/webp": ".webp"}
ASSET_NAME = re.compile(r"^[A-Za-z0-9._-]{1,180}$")


def _home() -> Path:
    return Path(os.environ.get("DORE_LOCAL_HOME", Path.home() / ".dore")).expanduser()


def _asset_url(output: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    artifact = output.get("artifact") if isinstance(output.get("artifact"), dict) else {}
    url = str(artifact.get("asset_url") or output.get("asset_url") or "").strip()
    return url, artifact


def _validate_loopback_asset_url(url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme != "http" or parsed.hostname not in {"127.0.0.1", "localhost"} or parsed.port != 8790:
        raise ValueError("image_asset_not_from_dore_image_local")
    if parsed.path != "/asset" or parsed.username or parsed.password or parsed.fragment:
        raise ValueError("image_asset_endpoint_invalid")
    query = urllib.parse.parse_qs(parsed.query, strict_parsing=True)
    names = query.get("name") or []
    if len(names) != 1 or not ASSET_NAME.fullmatch(names[0]) or Path(names[0]).name != names[0]:
        raise ValueError("image_asset_name_invalid")
    return names[0]


def _magic_mime(raw: bytes) -> str:
    if raw.startswith(b"\x89PNG\r\n\x1a\n"):
        return "image/png"
    if raw.startswith(b"\xff\xd8\xff"):
        return "image/jpeg"
    if len(raw) >= 12 and raw[:4] == b"RIFF" and raw[8:12] == b"WEBP":
        return "image/webp"
    raise ValueError("image_asset_format_not_allowed")


def normalize_image_output(output: dict[str, Any], task_id: str, *, timeout: int = 20) -> dict[str, Any] | None:
    """Return one verified opaque visual asset, or None when no usable output exists."""
    if not isinstance(output, dict) or output.get("ok") is False:
        return None
    url, artifact = _asset_url(output)
    if not url:
        return None
    source_name = _validate_loopback_asset_url(url)
    req = urllib.request.Request(url, headers={"Accept": "image/png,image/jpeg,image/webp"})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        content_length = response.headers.get("Content-Length")
        if content_length and int(content_length) > MAX_ASSET_BYTES:
            raise ValueError("image_asset_too_large")
        raw = response.read(MAX_ASSET_BYTES + 1)
    if not raw or len(raw) > MAX_ASSET_BYTES:
        raise ValueError("image_asset_too_large")
    mime = _magic_mime(raw)
    if mime not in ALLOWED_MIME:
        raise ValueError("image_asset_mime_not_allowed")
    digest = hashlib.sha256(raw).hexdigest()
    declared_sha = str(artifact.get("sha256") or "").lower().strip()
    if declared_sha and declared_sha != digest:
        raise ValueError("image_asset_sha256_mismatch")
    declared_bytes = artifact.get("bytes")
    if declared_bytes is not None and int(declared_bytes) != len(raw):
        raise ValueError("image_asset_size_mismatch")
    declared_mime = str(artifact.get("mime_type") or "").lower().strip()
    if declared_mime and declared_mime != mime:
        raise ValueError("image_asset_declared_mime_mismatch")

    ref = "arsenal-image-" + digest[:16]
    out_dir = _home() / "design-intelligence-a2a" / "assets" / str(task_id)
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / (digest + EXT_BY_MIME[mime])
    path.write_bytes(raw)
    return {
        "asset_ref": ref,
        "sha256": digest,
        "bytes": len(raw),
        "mime_type": mime,
        "path": str(path),
        "source": "image.generate",
        "source_artifact_id": artifact.get("id"),
        "model": artifact.get("model") or output.get("model"),
        "renderer": artifact.get("renderer") or output.get("renderer"),
        "source_name": source_name,
        "trusted": True,
    }


def public_asset_descriptor(asset: dict[str, Any]) -> dict[str, Any]:
    """Safe descriptor that may be shown to the model; excludes path and URL."""
    return {k: asset.get(k) for k in ("asset_ref", "sha256", "bytes", "mime_type", "source", "model", "renderer") if asset.get(k) is not None}
