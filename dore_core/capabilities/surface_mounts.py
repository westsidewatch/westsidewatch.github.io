from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Literal


MountState = Literal[
    "reserved",
    "fixture-found",
    "integration-proven",
    "mounted",
    "unavailable",
]


@dataclass(frozen=True)
class CapabilityMount:
    adapter: str
    state: MountState
    load: str
    scope: str
    implementation: str | None = None
    evidence: str | None = None

    def as_dict(self) -> dict:
        return asdict(self)


class SurfaceMountRegistry:
    """Truth table for presentation equipment actually attached to Dawn.

    A route name is never treated as proof of an installed capability.  Each
    adapter advances only through real evidence: reserved -> fixture-found ->
    integration-proven -> mounted.  Only mounted equipment is executable.
    """

    _mounts = {
        "bibliographic-page": CapabilityMount(
            adapter="bibliographic-page",
            state="mounted",
            load="lazy",
            scope="project-gutenberg",
            implementation="static/dawn-library/dawn-web-surface.js",
            evidence="data/dawn-capability-acceptance-corpus.json#gutenberg-josephus-antiquities",
        ),
        "iiif-visual-surface": CapabilityMount(
            adapter="iiif-visual-surface",
            state="fixture-found",
            load="on-demand",
            scope="iiif",
            evidence="data/dawn-capability-acceptance-corpus.json#loc-uta-evangeliary-iiif-source",
        ),
        "pdfjs": CapabilityMount(
            adapter="pdfjs",
            state="fixture-found",
            load="on-demand",
            scope="pdf",
            evidence="data/dawn-capability-acceptance-corpus.json#ccel-augustine-confessions-pdf",
        ),
        "book-reader": CapabilityMount(
            adapter="book-reader",
            state="reserved",
            load="on-demand",
            scope="scanned-book",
        ),
        "zotero-translate": CapabilityMount(
            adapter="zotero-translate",
            state="fixture-found",
            load="on-demand",
            scope="bibliographic-reconciliation",
            evidence="data/dawn-capability-acceptance-corpus.json#openlibrary-work-edition-identity",
        ),
        "oembed-opengraph": CapabilityMount(
            adapter="oembed-opengraph",
            state="reserved",
            load="on-demand",
            scope="web-preview",
        ),
        "readability": CapabilityMount(
            adapter="readability",
            state="fixture-found",
            load="fallback-only",
            scope="article-reader",
            evidence="data/dawn-capability-acceptance-corpus.json#bibleproject-chinese-article-source",
        ),
        "video-surface": CapabilityMount(
            adapter="video-surface",
            state="fixture-found",
            load="on-demand",
            scope="bible-film-video",
            evidence="data/dawn-capability-acceptance-corpus.json#jesus-film-full-feature",
        ),
        "cover-resolve": CapabilityMount(
            adapter="cover-resolve",
            state="fixture-found",
            load="on-demand",
            scope="book-cover",
            evidence="data/dawn-capability-acceptance-corpus.json#openlibrary-cover-augustine-fixture",
        ),
    }

    def get(self, adapter: str | None) -> CapabilityMount | None:
        if adapter is None:
            return None
        return self._mounts.get(adapter)

    def state(self, adapter: str | None) -> MountState:
        mount = self.get(adapter)
        return mount.state if mount else "unavailable"

    def executable(self, adapter: str | None) -> bool:
        return self.state(adapter) == "mounted"

    def inventory(self) -> list[dict]:
        return [self._mounts[key].as_dict() for key in sorted(self._mounts)]
