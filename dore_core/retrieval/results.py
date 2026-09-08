"""Normalize heterogeneous retrieval evidence into a stable Doré Search contract.

Products consume Doré Search results, never provider-specific payloads. Provenance is
preserved as source kind/locator/lane while substrate/provider names stay internal.
"""
from __future__ import annotations

import hashlib
from typing import Any, Iterable


def _as_items(payload: Any) -> list[dict[str, Any]]:
    if payload is None:
        return []
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    if isinstance(payload, dict):
        for key in ("results", "items", "matches", "memories", "records", "data"):
            value = payload.get(key)
            if isinstance(value, list):
                return [item for item in value if isinstance(item, dict)]
        return [payload] if payload else []
    return []


def _pick(item: dict[str, Any], *keys: str) -> Any:
    for key in keys:
        value = item.get(key)
        if value not in (None, "", []):
            return value
    return None


def _text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def _score(item: dict[str, Any], fallback: float) -> float:
    value = _pick(item, "score", "relevance", "similarity", "rank_score")
    try:
        return float(value)
    except (TypeError, ValueError):
        return fallback


def _identity(title: str, snippet: str, locator: str) -> str:
    basis = "|".join((locator.casefold(), title.casefold(), snippet[:240].casefold()))
    return hashlib.sha1(basis.encode("utf-8")).hexdigest()[:16]


def _normalize_item(item: dict[str, Any], *, source_kind: str, lane: str, fallback_score: float) -> dict[str, Any]:
    title = _text(_pick(item, "title", "name", "heading", "label"))
    snippet = _text(_pick(item, "snippet", "text", "content", "body", "summary", "excerpt", "memory"))
    locator = _text(_pick(item, "uri", "url", "path", "file", "source", "locator", "id"))
    if not title and locator:
        title = locator.rsplit("/", 1)[-1]
    if not snippet and title:
        snippet = title
    return {
        "id": _identity(title, snippet, locator),
        "title": title,
        "snippet": snippet,
        "locator": locator or None,
        "score": _score(item, fallback_score),
        "provenance": [{
            "kind": source_kind,
            "locator": locator or None,
            "lane": lane,
            "authority": False,
        }],
    }


def _dedupe_key(item: dict[str, Any]) -> str:
    locator = _text(item.get("locator")).casefold()
    if locator:
        return f"locator:{locator}"
    title = _text(item.get("title")).casefold()
    snippet = _text(item.get("snippet"))[:180].casefold()
    return f"content:{title}|{snippet}"


def merge_results(qmd: dict[str, Any] | None, memory: dict[str, Any] | None, *, limit: int = 8) -> list[dict[str, Any]]:
    """Return a provider-neutral ranked/deduplicated result list."""
    candidates: list[dict[str, Any]] = []

    if qmd and qmd.get("ok"):
        lane = _text(qmd.get("lane")) or "retrieval"
        for index, item in enumerate(_as_items(qmd.get("results"))):
            candidates.append(_normalize_item(
                item,
                source_kind="document",
                lane=lane,
                fallback_score=max(0.0, 1.0 - index * 0.01),
            ))

    if memory and memory.get("ok"):
        mode = _text(memory.get("mode")) or "strict"
        for index, item in enumerate(_as_items(memory.get("payload"))):
            candidates.append(_normalize_item(
                item,
                source_kind="memory",
                lane=f"recall:{mode}",
                fallback_score=max(0.0, 0.85 - index * 0.01),
            ))

    merged: dict[str, dict[str, Any]] = {}
    for item in candidates:
        key = _dedupe_key(item)
        previous = merged.get(key)
        if previous is None:
            merged[key] = item
            continue
        previous["score"] = max(float(previous.get("score") or 0.0), float(item.get("score") or 0.0))
        seen = {(p.get("kind"), p.get("locator"), p.get("lane")) for p in previous["provenance"]}
        for provenance in item["provenance"]:
            marker = (provenance.get("kind"), provenance.get("locator"), provenance.get("lane"))
            if marker not in seen:
                previous["provenance"].append(provenance)
                seen.add(marker)

    ranked = sorted(
        merged.values(),
        key=lambda item: (-float(item.get("score") or 0.0), _text(item.get("title")).casefold()),
    )
    return ranked[: max(1, limit)]
