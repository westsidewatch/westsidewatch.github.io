"""Project canonical Works onto Dawn Library's two reading layers."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any
from .reading_capability import ReadingCapability, ReadingResolution, resolve_reading_capability

@dataclass(frozen=True)
class LibraryReadingLayer:
    layer: int
    mode: str
    translatable: bool
    resolution: ReadingResolution


def project_reading_layer(work: dict[str, Any]) -> LibraryReadingLayer:
    r = resolve_reading_capability(work)
    # Layer 1 is materializable text owned/obtainable by Dawn. Authenticated
    # acquisition joins it only when a credential is actually available at runtime.
    if r.capability in {ReadingCapability.LOCAL_FULL_TEXT, ReadingCapability.OPEN_ACQUISITION}:
        return LibraryReadingLayer(1, "dawn-reader", True, r)
    return LibraryReadingLayer(2, "jump-reader", False, r)


def project_reading_layer_with_runtime(work: dict[str, Any], *, authenticated_acquisition_ready: bool=False) -> LibraryReadingLayer:
    r = resolve_reading_capability(work)
    if r.capability in {ReadingCapability.LOCAL_FULL_TEXT, ReadingCapability.OPEN_ACQUISITION} or (
        r.capability is ReadingCapability.AUTHENTICATED_ACQUISITION and authenticated_acquisition_ready
    ):
        return LibraryReadingLayer(1, "dawn-reader", True, r)
    return LibraryReadingLayer(2, "jump-reader", False, r)
