from __future__ import annotations

from dataclasses import asdict, dataclass
from urllib.parse import urlparse

from dore_core.capabilities.surface_mounts import SurfaceMountRegistry


@dataclass(frozen=True)
class SurfaceRoute:
    surface: str
    adapter: str | None
    confidence: float
    fallback: str | None = None


@dataclass(frozen=True)
class SurfacePayload:
    """Minimal provider-neutral payload consumed by Dawn presentation layers."""

    source_url: str
    surface: str
    adapter: str | None
    fallback: str | None
    confidence: float
    external: bool = True
    ownership: str = "external"

    def as_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class SurfacePlan:
    """Resolved route plus the truth about whether its equipment is mounted."""

    source_url: str
    surface: str
    adapter: str | None
    fallback: str | None
    confidence: float
    mount_state: str
    executable: bool
    external: bool = True
    ownership: str = "external"

    def as_dict(self) -> dict:
        return asdict(self)


class UrlSurfaceResolver:
    """Small deterministic pointer -> surface router.

    This resolver never decides relevance or admission. It only selects a
    presentation capability for an already-discovered external pointer.
    """

    def __init__(self, mounts: SurfaceMountRegistry | None = None) -> None:
        self.mounts = mounts or SurfaceMountRegistry()

    def resolve(self, url: str) -> SurfaceRoute:
        value = (url or "").strip()
        parsed = urlparse(value)
        host = parsed.netloc.casefold()
        path = parsed.path.casefold()
        lowered = value.casefold()

        if not (parsed.scheme in {"http", "https"} and host):
            return SurfaceRoute("unresolved", None, 0.0)

        if host in {"youtube.com", "www.youtube.com", "m.youtube.com", "youtu.be"}:
            return SurfaceRoute("video", "video-surface", 1.0)
        if "iiif" in lowered or path.endswith("/manifest") or path.endswith("/manifest.json"):
            return SurfaceRoute("visual", "iiif-visual-surface", 1.0)
        if path.endswith(".pdf"):
            return SurfaceRoute("document", "pdfjs", 1.0)
        if host.endswith("archive.org") and (path.startswith("/details/") or path.startswith("/embed/") or path.startswith("/stream/")):
            return SurfaceRoute("book", "book-reader", 1.0)
        if path.endswith((".epub", ".mobi")):
            return SurfaceRoute("book", "book-reader", 0.9)

        if host.endswith("gutenberg.org") and "/ebooks/" in path:
            return SurfaceRoute("book", "bibliographic-page", 1.0)
        if host.endswith(("openlibrary.org", "worldcat.org", "loc.gov", "hathitrust.org")):
            return SurfaceRoute("bibliographic", "zotero-translate", 0.85)

        return SurfaceRoute("web", "oembed-opengraph", 0.75, fallback="readability")

    def payload(self, url: str) -> SurfacePayload:
        value = (url or "").strip()
        route = self.resolve(value)
        return SurfacePayload(
            source_url=value,
            surface=route.surface,
            adapter=route.adapter,
            fallback=route.fallback,
            confidence=route.confidence,
        )

    def plan(self, url: str) -> SurfacePlan:
        value = (url or "").strip()
        route = self.resolve(value)
        return SurfacePlan(
            source_url=value,
            surface=route.surface,
            adapter=route.adapter,
            fallback=route.fallback,
            confidence=route.confidence,
            mount_state=self.mounts.state(route.adapter),
            executable=self.mounts.executable(route.adapter),
        )
