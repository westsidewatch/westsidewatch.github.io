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
    """Truth table for presentation equipment actually attached to Dawn."""

    _mounts = {
        "bibliographic-page": CapabilityMount("bibliographic-page", "mounted", "lazy", "project-gutenberg", "static/dawn-library/dawn-web-surface.js", "data/dawn-capability-acceptance-corpus.json#gutenberg-josephus-antiquities"),
        "iiif-visual-surface": CapabilityMount("iiif-visual-surface", "integration-proven", "on-demand", "iiif", "static/js/dawn-visual-viewer.js", "data/dawn-capability-acceptance-corpus.json#princeton-storm-sea-galilee-iiif"),
        "pdfjs": CapabilityMount("pdfjs", "integration-proven", "on-demand", "pdf", "static/js/dawn-pdf-surface.js", "data/dawn-capability-acceptance-corpus.json#wikimedia-augustine-confessions-pdf"),
        "book-reader": CapabilityMount("book-reader", "integration-proven", "on-demand", "internet-archive-scan", "static/js/dawn-bookreader-surface.js", "data/dawn-capability-acceptance-corpus.json#internetarchive-josephus-1900-bookreader"),
        "zotero-translate": CapabilityMount("zotero-translate", "integration-proven", "on-demand", "bibliographic-reconciliation", "dore_core/capabilities/zotero_reconciliation.py", "reports/DAWN-ZOTERO-TRANSLATION.json"),
        "oembed-opengraph": CapabilityMount("oembed-opengraph", "reserved", "on-demand", "web-preview"),
        "readability": CapabilityMount("readability", "fixture-found", "fallback-only", "article-reader", None, "data/dawn-capability-acceptance-corpus.json#bibleproject-chinese-article-source"),
        "video-surface": CapabilityMount("video-surface", "integration-proven", "on-demand", "bible-film-video", "static/js/dawn-video-surface.js", "data/dawn-capability-acceptance-corpus.json#jesus-film-official-youtube"),
        "cover-resolve": CapabilityMount("cover-resolve", "integration-proven", "on-demand", "book-cover", "dore_core/capabilities/cover_resolver.py", "data/dawn-capability-acceptance-corpus.json#openlibrary-josephus-1900-cover"),
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
