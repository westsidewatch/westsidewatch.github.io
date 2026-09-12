from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import quote


@dataclass(frozen=True)
class CoverCandidate:
    provider: str
    identifier_type: str
    identifier: str
    url: str
    external: bool = True


class CoverResolver:
    """Resolve a cover from stable edition identifiers without owning the image.

    Edition identifiers are preferred over title search so a cover can never be
    silently borrowed from a different translation/reprint.
    """

    BASE = "https://covers.openlibrary.org/b"
    PRIORITY = ("cover_id", "olid", "isbn", "oclc", "lccn")

    def resolve(self, identifiers: dict | None, size: str = "M") -> CoverCandidate | None:
        values = identifiers or {}
        normalized_size = size.upper()
        if normalized_size not in {"S", "M", "L"}:
            raise ValueError("cover size must be S, M or L")

        for key in self.PRIORITY:
            raw = values.get(key)
            if isinstance(raw, (list, tuple)):
                raw = next((item for item in raw if str(item).strip()), None)
            value = str(raw or "").strip()
            if not value:
                continue

            if key == "cover_id":
                path_type = "id"
            else:
                path_type = key
            encoded = quote(value, safe="")
            return CoverCandidate(
                provider="Open Library Covers",
                identifier_type=key,
                identifier=value,
                url=f"{self.BASE}/{path_type}/{encoded}-{normalized_size}.jpg?default=false",
            )
        return None
