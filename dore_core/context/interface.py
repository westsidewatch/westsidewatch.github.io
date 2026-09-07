"""Small protocol boundary for Doré consumers of Westside Context."""
from __future__ import annotations

from typing import Any, Protocol


class WestsideContextRetriever(Protocol):
    """Read-only capability expected by Doré faculties/adapters."""

    def __call__(self, query: str, *, limit: int = 4) -> list[dict[str, Any]]:
        ...
