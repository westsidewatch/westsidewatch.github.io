from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class BibleReference:
    """Canonical, provider-neutral Bible location.

    `book` should use the product's canonical book identifier (for example
    `Matt` or another stable internal code).  This contract deliberately does
    not bind DORÉ to any parser or Bible data provider.
    """

    book: str
    chapter: int
    verse_start: Optional[int] = None
    verse_end: Optional[int] = None
    osis: Optional[str] = None

    def __post_init__(self) -> None:
        if not self.book or not str(self.book).strip():
            raise ValueError("book_required")
        if self.chapter < 1:
            raise ValueError("chapter_must_be_positive")
        if self.verse_start is not None and self.verse_start < 1:
            raise ValueError("verse_start_must_be_positive")
        if self.verse_end is not None and self.verse_end < 1:
            raise ValueError("verse_end_must_be_positive")
        if self.verse_end is not None and self.verse_start is None:
            raise ValueError("verse_end_requires_verse_start")
        if (
            self.verse_start is not None
            and self.verse_end is not None
            and self.verse_end < self.verse_start
        ):
            raise ValueError("verse_range_invalid")

    @property
    def key(self) -> str:
        base = f"{self.book}.{self.chapter}"
        if self.verse_start is None:
            return base
        if self.verse_end is None or self.verse_end == self.verse_start:
            return f"{base}.{self.verse_start}"
        return f"{base}.{self.verse_start}-{self.verse_end}"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "schema": "dore.bible-reference.v1",
            "book": self.book,
            "chapter": self.chapter,
            "verse_start": self.verse_start,
            "verse_end": self.verse_end,
            "osis": self.osis,
            "key": self.key,
        }

    @classmethod
    def from_dict(cls, payload: Dict[str, Any]) -> "BibleReference":
        if not isinstance(payload, dict):
            raise ValueError("bible_reference_must_be_object")
        return cls(
            book=str(payload.get("book") or "").strip(),
            chapter=int(payload.get("chapter") or 0),
            verse_start=(
                int(payload["verse_start"])
                if payload.get("verse_start") is not None
                else None
            ),
            verse_end=(
                int(payload["verse_end"])
                if payload.get("verse_end") is not None
                else None
            ),
            osis=(str(payload["osis"]).strip() if payload.get("osis") else None),
        )
