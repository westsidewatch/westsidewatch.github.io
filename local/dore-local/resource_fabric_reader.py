#!/usr/bin/env python3
"""Bounded Python reader for the site-wide Resource Fabric projections.

This reader is deliberately non-authoritative: it routes to compiled shards and returns
canonical projections. It never invents Work IDs, rights, or source authority.
"""
from __future__ import annotations

import json
import os
import re
from functools import lru_cache
from pathlib import Path

TOKEN_RE = re.compile(r"[\w\u3400-\u9fff]+", re.UNICODE)


def _root() -> Path:
    env = os.environ.get("DORE_REPO_ROOT")
    if env:
        return Path(env).expanduser().resolve()
    return Path(__file__).resolve().parents[2]


def _fabric() -> Path:
    return _root() / "static" / "dawn-library" / "resource-fabric"


def _fnv1a(text: str) -> int:
    h = 0x811C9DC5
    for b in str(text).encode("utf-8"):
        h ^= b
        h = (h * 0x01000193) & 0xFFFFFFFF
    return h


def _decode(row: list) -> dict:
    values = list(row) + [None] * max(0, 10 - len(row))
    work_id, title, author, cover_pointer, reading_pointer, authority_backed, authors, languages, authority_ids, edition = values[:10]
    authors = authors if isinstance(authors, list) and authors else ([author] if author else [])
    return {
        "workId": work_id,
        "title": title or "Untitled",
        "authors": authors,
        "languages": languages if isinstance(languages, list) else [],
        "authorityIds": authority_ids if isinstance(authority_ids, dict) else {},
        "edition": edition if isinstance(edition, dict) else {},
        "coverPointer": cover_pointer,
        "readingPointer": reading_pointer,
        "authorityBacked": bool(authority_backed),
        "identityAuthority": "Dawn",
        "resourceFabricProjection": True,
    }


@lru_cache(maxsize=1)
def manifest() -> dict:
    data = json.loads((_fabric() / "manifest.json").read_text(encoding="utf-8"))
    if data.get("schema") != "dore.resource-fabric.surface-manifest.v0":
        raise RuntimeError("resource_fabric_manifest_schema_mismatch")
    if data.get("canonicalMonolithRequired") is not False:
        raise RuntimeError("resource_fabric_monolith_boundary_violated")
    if data.get("identityAuthority") != "Dawn":
        raise RuntimeError("resource_fabric_identity_authority_mismatch")
    return data


@lru_cache(maxsize=128)
def _work_shard(index: int) -> dict:
    return json.loads((_fabric() / f"work-{index:02x}.json").read_text(encoding="utf-8"))


@lru_cache(maxsize=128)
def _search_bucket(index: int) -> dict:
    return json.loads((_fabric() / f"search-{index:02x}.json").read_text(encoding="utf-8"))


def work(work_id: str) -> dict | None:
    if not work_id:
        return None
    meta = manifest()
    index = _fnv1a(work_id) % int(meta["workShardCount"])
    for row in _work_shard(index).get("rows") or []:
        if row and row[0] == work_id:
            return _decode(row)
    return None


def search(query: str, limit: int = 12) -> list[dict]:
    q = str(query or "").strip().casefold()
    if not q:
        return []
    match = TOKEN_RE.search(q)
    if not match:
        return []
    token = match.group(0)
    prefix = token[: min(4, len(token))]
    meta = manifest()
    index = _fnv1a(prefix) % int(meta["searchBucketCount"])
    ids: list[str] = []
    for row in _search_bucket(index).get("rows") or []:
        if len(row) < 4 or row[0] != prefix:
            continue
        if q in f"{row[2]} {row[3]}".casefold():
            ids.append(row[1])
            if len(ids) >= max(1, min(int(limit), 50)):
                break
    return [resolved for wid in ids if (resolved := work(wid)) is not None]


def context(*, work_id: str | None = None, query: str | None = None, limit: int = 6) -> dict | None:
    if work_id:
        resolved = work(work_id)
        if resolved:
            return {"schema": "dore.resource-fabric.context.v0", "mode": "work", "work": resolved}
    if query:
        results = search(query, limit=limit)
        return {"schema": "dore.resource-fabric.context.v0", "mode": "search", "query": query, "works": results}
    return None
