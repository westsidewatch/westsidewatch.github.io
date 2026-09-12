from __future__ import annotations

from dataclasses import dataclass
import re


_ITEM_ID = re.compile(r'^[A-Za-z0-9._-]+$')


@dataclass(frozen=True)
class ArchiveBookReaderTarget:
    provider: str
    item_id: str
    details_url: str
    embed_url: str
    external: bool = True


class ArchiveBookReaderAdapter:
    """Map a stable Internet Archive item id to its official embed surface."""

    def resolve(self, item_id: str | None) -> ArchiveBookReaderTarget | None:
        value = str(item_id or '').strip()
        if not value or not _ITEM_ID.fullmatch(value):
            return None
        return ArchiveBookReaderTarget(
            provider='Internet Archive',
            item_id=value,
            details_url=f'https://archive.org/details/{value}',
            embed_url=f'https://archive.org/embed/{value}',
        )
