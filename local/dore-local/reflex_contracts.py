#!/usr/bin/env python3
"""Provider-neutral contracts for Doré Reflex v0.

Reflex is request-scoped: canonical source identity persists elsewhere; the reflex
session and its events must not become a second substrate.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, Protocol


REFLEX_EVENT_KINDS = frozenset({
    "document.start",
    "document.end",
    "heading",
    "paragraph",
    "table.start",
    "table.row",
    "table.end",
    "unsupported",
})

CONTENT_EVENT_KINDS = frozenset({"heading", "paragraph", "table.row"})


@dataclass(frozen=True)
class SourceDescriptor:
    mime: str
    name: str = ""
    canonical_id: str = ""
    source_pointer: str = ""


@dataclass(frozen=True)
class ReflexEvent:
    """One provider-neutral semantic event.

    Adapters may differ internally, but every event admitted to a ReflexSession must
    use this vocabulary. Structured values such as table cells live in ``meta`` so
    projections never need to know which parser produced them.
    """

    kind: str
    text: str = ""
    level: int | None = None
    page: int | None = None
    span: tuple[int, int] | None = None
    bbox: tuple[float, float, float, float] | None = None
    meta: dict[str, Any] = field(default_factory=dict)

    def validate(self) -> None:
        if self.kind not in REFLEX_EVENT_KINDS:
            raise ValueError(f"unsupported Reflex event kind: {self.kind}")
        if self.kind == "heading" and (self.level is None or self.level < 1):
            raise ValueError("heading events require a positive level")
        if self.kind == "table.row":
            cells = self.meta.get("cells")
            if not isinstance(cells, list) or not all(isinstance(cell, str) for cell in cells):
                raise ValueError("table.row events require meta.cells as list[str]")


class ReflexAdapter(Protocol):
    name: str

    def score(self, source: SourceDescriptor) -> int: ...

    def parse(self, source: SourceDescriptor, payload: bytes) -> Iterable[ReflexEvent]: ...


@dataclass
class ReflexSession:
    source: SourceDescriptor
    adapter: str
    events: list[ReflexEvent]
    closed: bool = False

    def __post_init__(self) -> None:
        for event in self.events:
            event.validate()

    def require_open(self) -> None:
        if self.closed:
            raise RuntimeError("reflex session is closed")

    def iter_events(self) -> Iterable[ReflexEvent]:
        self.require_open()
        return tuple(self.events)

    def close(self) -> None:
        self.events.clear()
        self.closed = True
