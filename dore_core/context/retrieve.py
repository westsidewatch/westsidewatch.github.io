"""Minimal Doré-facing adapter for retrieving Westside Context packets."""
from __future__ import annotations

import sqlite3
from typing import Any

from .compiler import search_context
from .packet import packet_dict


def retrieve_westside_context(
    query: str,
    db: sqlite3.Connection,
    limit: int = 4,
) -> list[dict[str, Any]]:
    """Return bounded, provenance-preserving Context Packets for a Doré task.

    The adapter is read-only: it retrieves the derived Context projection and
    serializes packets for downstream Doré faculties. It has no path to mutate
    the canonical architecture source.
    """
    if limit < 1:
        return []
    return [packet_dict(packet) for packet in search_context(db, query, limit)]
