from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import parse_qs, urlparse


@dataclass(frozen=True)
class VideoTarget:
    provider: str
    video_id: str
    embed_url: str
    source_url: str


class VideoSurfaceAdapter:
    """Resolve approved public video pointers into safe embed targets.

    This layer only handles presentation. Content admission remains a separate
    Dawn policy decision.
    """

    def resolve(self, url: str) -> VideoTarget | None:
        value = (url or "").strip()
        parsed = urlparse(value)
        host = parsed.netloc.casefold().split(":", 1)[0]
        video_id = ""

        if host in {"www.youtube.com", "youtube.com", "m.youtube.com"} and parsed.path == "/watch":
            video_id = (parse_qs(parsed.query).get("v") or [""])[0]
        elif host == "youtu.be":
            video_id = parsed.path.strip("/").split("/", 1)[0]

        if not self._valid_video_id(video_id):
            return None

        return VideoTarget(
            provider="youtube",
            video_id=video_id,
            embed_url=f"https://www.youtube-nocookie.com/embed/{video_id}",
            source_url=value,
        )

    @staticmethod
    def _valid_video_id(value: str) -> bool:
        return len(value) == 11 and all(ch.isalnum() or ch in "-_" for ch in value)
