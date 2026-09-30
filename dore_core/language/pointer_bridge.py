"""Bridge legacy Dawn URL-surface pointers into canonical reading pointers.

This module migrates capability, not ownership: old discovery/surface records
remain external pointers.  It extracts provider identity from already-approved
Gutenberg URLs and feeds the canonical source-mapping/materialization path.
"""
from __future__ import annotations

from dataclasses import dataclass
import re
from urllib.parse import urlparse

from dore_core.capabilities.url_surface import UrlSurfaceResolver
from .source_mapping import SourceMapping, map_public_domain_source

_GUTENBERG_EBOOK = re.compile(r"^/ebooks/(\d+)(?:[/.]|$)", re.I)


@dataclass(frozen=True)
class ReadingPointerBridge:
    work_id: str
    provider: str
    provider_id: str
    source_url: str
    mapping: SourceMapping


def _work_id(work: dict) -> str:
    return str(work.get("workId") or work.get("id") or "").strip()


def provider_identity_from_surface(source_url: str) -> tuple[str, str] | None:
    """Recover a provider-specific identity from a legacy approved surface."""
    value = str(source_url or "").strip()
    route = UrlSurfaceResolver().resolve(value)
    if route.surface != "book":
        return None

    parsed = urlparse(value)
    host = parsed.netloc.casefold().split(":", 1)[0]
    if host == "www.gutenberg.org" or host.endswith(".gutenberg.org") or host == "gutenberg.org":
        match = _GUTENBERG_EBOOK.match(parsed.path)
        if match:
            return ("projectGutenberg", match.group(1))
    return None


def bridge_legacy_surface(work: dict, source_url: str) -> ReadingPointerBridge | None:
    """Attach legacy provider identity to a canonical work without mutating it."""
    identity = provider_identity_from_surface(source_url)
    work_id = _work_id(work)
    if not identity or not work_id:
        return None

    key, provider_id = identity
    authority_ids = dict(work.get("authorityIds") or {})
    existing = str(authority_ids.get(key) or "").strip()
    if existing and existing != provider_id:
        # Never overwrite a conflicting canonical authority identity.
        return None
    authority_ids[key] = provider_id

    candidate = dict(work)
    candidate["authorityIds"] = authority_ids
    mapping = map_public_domain_source(candidate)
    if mapping is None:
        return None

    return ReadingPointerBridge(
        work_id=work_id,
        provider=mapping.provider,
        provider_id=provider_id,
        source_url=source_url,
        mapping=mapping,
    )


def bridge_surface_records(
    works_by_id: dict[str, dict], records: list[dict]
) -> list[ReadingPointerBridge]:
    """Bridge old surface-index/discovery records when they name a canonical work."""
    bridged: list[ReadingPointerBridge] = []
    seen: set[tuple[str, str, str]] = set()
    for record in records:
        work_id = str(record.get("workId") or record.get("work_id") or "").strip()
        source_url = str(record.get("source_url") or record.get("sourceUrl") or record.get("url") or "").strip()
        work = works_by_id.get(work_id)
        if not work or not source_url:
            continue
        result = bridge_legacy_surface(work, source_url)
        if result is None:
            continue
        marker = (result.work_id, result.provider, result.provider_id)
        if marker in seen:
            continue
        seen.add(marker)
        bridged.append(result)
    return bridged
