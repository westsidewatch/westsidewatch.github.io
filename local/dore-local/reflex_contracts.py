#!/usr/bin/env python3
"""Provider-neutral contracts for Doré Reflex v0.

Reflex is request-scoped: canonical source identity persists elsewhere; the reflex
session and its events must not become a second substrate.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, Protocol


@dataclass(frozen=True)
class SourceDescriptor:
    mime: str
    name: str = ""
    canonical_id: str = ""
    source_pointer: str = ""


@dataclass(frozen=True)
class ReflexEvent:
    kind: str
    text: str = ""
    level: int | None = None
    page: int | None = None
    span: tuple[int, int] | None = None
    bbox: tuple[float, float, float, float] | None = None
    meta: dict[str, Any] = field(default_factory=dict)


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

    def require_open(self) -> None:
        if self.closed:
            raise RuntimeError("reflex session is closed")

    def iter_events(self) -> Iterable[ReflexEvent]:
        self.require_open()
        return tuple(self.events)

    def close(self) -> None:
        self.events.clear()
        self.closed = True
