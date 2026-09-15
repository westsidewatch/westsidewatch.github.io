#!/usr/bin/env python3
"""Real image-grounded provider for DORÉ editorial visual observation.

The provider fetches the exact historical image bytes and sends those bytes to the
local multimodal model through Ollama. It never substitutes publication/lineage prose
for pixels. A text-only or image-incapable model fails closed so a grounded external
vision provider (e.g. ChatGPT vision) can be used explicitly by the caller.
"""
from __future__ import annotations

import base64
import json
import os
import urllib.request
from typing import Any, Mapping

from editorial_visual_observation_capability import DIMENSIONS, VisualObservationError

MODEL = os.environ.get("DORE_VISUAL_MODEL") or os.environ.get("DORE_LOCAL_MODEL") or os.environ.get("DORE_MODEL") or "gemma4:e4b"
OLLAMA = os.environ.get("OLLAMA_BASE_URL") or os.environ.get("OLLAMA_HOST") or "http://127.0.0.1:11434"
MAX_IMAGE_BYTES = int(os.environ.get("DORE_VISUAL_MAX_IMAGE_BYTES", str(12 * 1024 * 1024)))


def _fetch_image(uri: str) -> tuple[bytes, str]:
    req = urllib.request.Request(uri, headers={"User-Agent": "DoreDesign/1.0 historical-evidence-observer"})
    with urllib.request.urlopen(req, timeout=45) as response:
        content_type = str(response.headers.get("Content-Type") or "").split(";", 1)[0].strip().lower()
        data = response.read(MAX_IMAGE_BYTES + 1)
    if len(data) > MAX_IMAGE_BYTES:
        raise VisualObservationError("historical image exceeds grounded vision byte budget")
    if not data:
        raise VisualObservationError("historical image fetch returned no bytes")
    if content_type and not content_type.startswith("image/"):
        raise VisualObservationError(f"historical image URI returned {content_type}, not image bytes")
    return data, content_type or "application/octet-stream"


def _schema() -> dict[str, Any]:
    dimension = {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["observed", "insufficient"]},
            "facts": {"type": "array", "items": {"type": "string"}, "maxItems": 16},
        },
        "required": ["status", "facts"],
        "additionalProperties": False,
    }
    return {
        "type": "object",
        "properties": {
            "imageInspected": {"type": "boolean", "const": True},
            "dimensions": {
                "type": "object",
                "properties": {d: dimension for d in DIMENSIONS},
                "required": list(DIMENSIONS),
                "additionalProperties": False,
            },
        },
        "required": ["imageInspected", "dimensions"],
        "additionalProperties": False,
    }


def _messages(request: Mapping[str, Any], image_b64: str) -> list[dict[str, Any]]:
    contract = request.get("authorityContract") or {}
    evidence = request.get("evidence") or {}
    system = (
        "You are DORÉ grounded editorial vision. Inspect the attached historical magazine image itself. "
        "Pixels are primary authority. Publication and era names are identification context only. "
        "For each of the eight requested dimensions, report concrete visible facts: geometry, proportions, "
        "regions, crop, scale, anchor, alignment, overlap, text/image relation, color/material evidence, "
        "negative space, density and reading order. For irony/emergence, use only relationships visibly "
        "supported by the image; otherwise mark insufficient. Never add architecture, concrete, furniture, "
        "Swiss grids, red geometry, motifs or materials merely because they are associated with Italian design. "
        "If evidence is absent, status must be insufficient with an empty facts array. Return JSON only."
    )
    user = {
        "role": "user",
        "content": json.dumps({
            "evidenceId": evidence.get("id"),
            "publication": evidence.get("publication"),
            "era": evidence.get("era"),
            "dimensions": list(DIMENSIONS),
            "authorityContract": contract,
        }, ensure_ascii=False),
        "images": [image_b64],
    }
    return [{"role": "system", "content": system}, user]


def observe(request: Mapping[str, Any]) -> Mapping[str, Any]:
    evidence = request.get("evidence") if isinstance(request.get("evidence"), Mapping) else {}
    image_uri = str(evidence.get("imageUri") or "")
    if not image_uri:
        raise VisualObservationError("grounded provider requires imageUri")
    image_bytes, _ = _fetch_image(image_uri)
    image_b64 = base64.b64encode(image_bytes).decode("ascii")
    payload = {
        "model": MODEL,
        "messages": _messages(request, image_b64),
        "stream": False,
        "think": False,
        "format": _schema(),
    }
    req = urllib.request.Request(
        OLLAMA.rstrip("/") + "/api/chat",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=300) as response:
            result = json.loads(response.read().decode("utf-8"))
    except Exception as exc:
        raise VisualObservationError(f"local grounded vision unavailable: {type(exc).__name__}") from exc
    message = result.get("message") or {}
    content = message.get("content")
    if not isinstance(content, str) or not content.strip():
        raise VisualObservationError("local grounded vision returned no structured observation")
    try:
        value = json.loads(content)
    except json.JSONDecodeError as exc:
        raise VisualObservationError("local grounded vision returned invalid JSON") from exc
    if not isinstance(value, dict):
        raise VisualObservationError("local grounded vision output must be an object")
    value["imageInspected"] = True
    return value


def provenance() -> dict[str, str]:
    return {"providerId": f"ollama:{MODEL}", "providerKind": "dore-local-vision"}
