"""Collection-wide reading capability resolver for Dawn Library.

The resolver deliberately separates bibliographic identity from reading transport.
A Work can exist canonically even when no machine-readable full text is available.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Iterable


class ReadingCapability(str, Enum):
    LOCAL_FULL_TEXT = "local-full-text"
    OPEN_ACQUISITION = "open-acquisition"
    AUTHENTICATED_ACQUISITION = "authenticated-acquisition"
    EXTERNAL_READER = "external-reader"
    METADATA_ONLY = "metadata-only"


@dataclass(frozen=True)
class ReadingResolution:
    capability: ReadingCapability
    provider: str | None = None
    href: str | None = None
    reason: str | None = None

    @property
    def dawn_reader_ready(self) -> bool:
        return self.capability in {
            ReadingCapability.LOCAL_FULL_TEXT,
            ReadingCapability.OPEN_ACQUISITION,
            ReadingCapability.AUTHENTICATED_ACQUISITION,
        }


def _strings(value: Any) -> Iterable[str]:
    if value is None:
        return ()
    if isinstance(value, str):
        return (value,)
    if isinstance(value, dict):
        return tuple(str(v) for v in value.values() if v is not None)
    if isinstance(value, (list, tuple, set)):
        out: list[str] = []
        for item in value:
            out.extend(_strings(item))
        return tuple(out)
    return (str(value),)


def _haystack(work: dict[str, Any]) -> str:
    keys = (
        "source", "sources", "provider", "providers", "authority", "authorities",
        "authorityIds", "identifiers", "links", "reading", "readingPointer",
        "readingPointers", "url", "urls", "href", "format", "formats",
    )
    return " ".join(s.lower() for key in keys for s in _strings(work.get(key)))


def resolve_reading_capability(work: dict[str, Any]) -> ReadingResolution:
    """Resolve the best known reading route without performing network I/O.

    Priority is intentional: owned/local text beats acquisition, which beats an
    external reader. Unknown bibliography remains a valid metadata-only Work.
    """
    text = _haystack(work)

    local = work.get("localFullText") or work.get("localPublication") or work.get("publicationPath")
    if local:
        return ReadingResolution(ReadingCapability.LOCAL_FULL_TEXT, "dawn", str(local), "owned local publication")

    # Explicit capability declarations always beat provider inference.
    declared = str(work.get("readingCapability") or work.get("acquisitionMode") or "").lower()
    if declared in {"local-full-text", "local_full_text"}:
        return ReadingResolution(ReadingCapability.LOCAL_FULL_TEXT, "dawn", reason="explicit capability")
    if declared in {"open-acquisition", "open_acquisition"}:
        return ReadingResolution(ReadingCapability.OPEN_ACQUISITION, reason="explicit capability")
    if declared in {"authenticated-acquisition", "authenticated_acquisition"}:
        return ReadingResolution(ReadingCapability.AUTHENTICATED_ACQUISITION, reason="explicit capability")
    if declared in {"external-reader", "external_reader"}:
        return ReadingResolution(ReadingCapability.EXTERNAL_READER, reason="explicit capability")

    # Current provider policies. These are transport policy, never identity authority.
    if "standardebooks.org" in text or "standard ebooks" in text or "standard_ebooks" in text:
        return ReadingResolution(ReadingCapability.AUTHENTICATED_ACQUISITION, "standard-ebooks", reason="official OPDS acquisition requires authentication")
    if "gutenberg.org" in text or "project gutenberg" in text or "gutenberg" in text:
        href = next((s for s in _strings(work.get("readingPointer")) if "gutenberg" in s.lower()), None)
        return ReadingResolution(ReadingCapability.EXTERNAL_READER, "gutenberg", href, "official external reading route")

    # Generic explicit machine-readable acquisition links can be consumed by adapters.
    for key in ("acquisitionUrl", "acquisitionURL", "epubUrl", "epubURL"):
        if work.get(key):
            return ReadingResolution(ReadingCapability.OPEN_ACQUISITION, href=str(work[key]), reason=f"{key} present")

    for key in ("readingPointer", "readerUrl", "readerURL"):
        if work.get(key):
            return ReadingResolution(ReadingCapability.EXTERNAL_READER, href=str(work[key]), reason=f"{key} present")

    return ReadingResolution(ReadingCapability.METADATA_ONLY, reason="no admitted reading transport")
