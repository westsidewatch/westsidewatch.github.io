#!/usr/bin/env python3
"""Minimal Reflex Router and first adapters."""
from __future__ import annotations

from html import unescape
import re
from typing import Iterable

from reflex_contracts import ReflexAdapter, ReflexEvent, ReflexSession, SourceDescriptor


class TextAdapter:
    name = "text"

    def score(self, source: SourceDescriptor) -> int:
        mime = source.mime.lower()
        name = source.name.lower()
        if mime in {"text/plain", "text/markdown", "text/html"}:
            return 100
        if name.endswith((".txt", ".md", ".markdown", ".html", ".htm")):
            return 90
        return 0

    def parse(self, source: SourceDescriptor, payload: bytes) -> Iterable[ReflexEvent]:
        text = payload.decode("utf-8", errors="replace")
        if source.mime.lower() == "text/html" or source.name.lower().endswith((".html", ".htm")):
            text = re.sub(r"<script\b[^>]*>.*?</script>", "", text, flags=re.I | re.S)
            text = re.sub(r"<style\b[^>]*>.*?</style>", "", text, flags=re.I | re.S)
            text = unescape(re.sub(r"<[^>]+>", "\n", text))
        yield ReflexEvent("document.start", meta={"mime": source.mime})
        offset = 0
        for raw in text.splitlines(keepends=True):
            line = raw.strip()
            start, end = offset, offset + len(raw)
            offset = end
            if not line:
                continue
            heading = re.match(r"^(#{1,6})\s+(.+)$", line)
            if heading:
                yield ReflexEvent("heading", heading.group(2).strip(), level=len(heading.group(1)), span=(start, end))
            else:
                yield ReflexEvent("paragraph", line, span=(start, end))
        yield ReflexEvent("document.end")


class DegradedAdapter:
    name = "degraded"

    def score(self, source: SourceDescriptor) -> int:
        return 1

    def parse(self, source: SourceDescriptor, payload: bytes) -> Iterable[ReflexEvent]:
        yield ReflexEvent("document.start", meta={"mime": source.mime})
        yield ReflexEvent(
            "unsupported",
            meta={"bytes": len(payload), "reason": "no_structural_adapter"},
        )
        yield ReflexEvent("document.end")


class ReflexRouter:
    def __init__(self, adapters: list[ReflexAdapter] | None = None) -> None:
        self.adapters = adapters or [TextAdapter(), DegradedAdapter()]

    def resolve(self, source: SourceDescriptor) -> ReflexAdapter:
        return max(self.adapters, key=lambda adapter: adapter.score(source))

    def open(self, source: SourceDescriptor, payload: bytes) -> ReflexSession:
        adapter = self.resolve(source)
        events = list(adapter.parse(source, payload))
        return ReflexSession(source=source, adapter=adapter.name, events=events)
