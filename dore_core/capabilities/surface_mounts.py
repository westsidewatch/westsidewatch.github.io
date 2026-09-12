from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Literal


MountState = Literal["mounted", "dormant", "unavailable"]


@dataclass(frozen=True)
class CapabilityMount:
    adapter: str
    state: MountState
    load: str
    scope: str
    implementation: str | None = None

    def as_dict(self) -> dict:
        return asdict(self)


class SurfaceMountRegistry:
    """Truth table for presentation equipment actually attached to Dawn.

    Routing may name a useful adapter before that adapter is installed.  This
    registry prevents a route suggestion from being mistaken for an executable
    capability.  It contains no discovery, relevance, or admission policy.
    """

    _mounts = {
        "bibliographic-page": CapabilityMount(
            adapter="bibliographic-page",
            state="mounted",
            load="lazy",
            scope="project-gutenberg",
            implementation="static/dawn-library/dawn-web-surface.js",
        ),
        "iiif-visual-surface": CapabilityMount(
            adapter="iiif-visual-surface",
            state="dormant",
            load="on-demand",
            scope="iiif",
        ),
        "pdfjs": CapabilityMount(
            adapter="pdfjs",
            state="dormant",
            load="on-demand",
            scope="pdf",
        ),
        "book-reader": CapabilityMount(
            adapter="book-reader",
            state="dormant",
            load="on-demand",
            scope="epub-mobi",
        ),
        "zotero-translate": CapabilityMount(
            adapter="zotero-translate",
            state="dormant",
            load="on-demand",
            scope="bibliographic-reconciliation",
        ),
        "oembed-opengraph": CapabilityMount(
            adapter="oembed-opengraph",
            state="dormant",
            load="on-demand",
            scope="web-preview",
        ),
        "readability": CapabilityMount(
            adapter="readability",
            state="dormant",
            load="fallback-only",
            scope="article-reader",
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
