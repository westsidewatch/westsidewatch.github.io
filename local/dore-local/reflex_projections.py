#!/usr/bin/env python3
"""Purpose-specific projections for Doré Reflex v0."""
from __future__ import annotations

from typing import Any

from reflex_contracts import ReflexEvent, ReflexSession


def _content_events(session: ReflexSession) -> list[ReflexEvent]:
    return [event for event in session.iter_events() if event.kind in {"heading", "paragraph"}]


def project_search(session: ReflexSession) -> dict[str, Any]:
    chunks = []
    for index, event in enumerate(_content_events(session)):
        chunks.append({
            "id": f"chunk-{index}",
            "kind": event.kind,
            "text": event.text,
            "level": event.level,
            "provenance": {
                "canonicalId": session.source.canonical_id,
                "sourcePointer": session.source.source_pointer,
                "span": event.span,
                "page": event.page,
                "bbox": event.bbox,
            },
        })
    return {"schema": "dore.reflex.search-projection.v0", "chunks": chunks}


def project_publishing(session: ReflexSession) -> dict[str, Any]:
    sections: list[dict[str, Any]] = []
    current = {"title": "", "level": 0, "blocks": []}
    sections.append(current)
    for event in _content_events(session):
        if event.kind == "heading":
            current = {"title": event.text, "level": event.level or 1, "blocks": []}
            sections.append(current)
        else:
            current["blocks"].append({"type": "paragraph", "text": event.text, "span": event.span})
    return {
        "schema": "dore.reflex.publishing-projection.v0",
        "source": {"canonicalId": session.source.canonical_id, "sourcePointer": session.source.source_pointer},
        "sections": sections,
    }


def project_design(session: ReflexSession) -> dict[str, Any]:
    events = _content_events(session)
    chars = sum(len(event.text) for event in events)
    headings = [event for event in events if event.kind == "heading"]
    paragraphs = [event for event in events if event.kind == "paragraph"]
    return {
        "schema": "dore.reflex.design-projection.v0",
        "hierarchy": [{"text": event.text, "level": event.level} for event in headings],
        "signals": {
            "textChars": chars,
            "paragraphCount": len(paragraphs),
            "headingCount": len(headings),
            "textDensity": "high" if chars > 2400 else "medium" if chars > 800 else "low",
        },
        "authority": {"layoutDecision": False, "brandDecision": False},
    }


def project(session: ReflexSession, intent: str) -> dict[str, Any]:
    if intent == "text.search":
        return project_search(session)
    if intent == "publishing.structure":
        return project_publishing(session)
    if intent == "design.structure":
        return project_design(session)
    raise ValueError(f"unsupported reflex projection: {intent}")
