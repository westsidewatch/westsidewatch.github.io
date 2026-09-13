#!/usr/bin/env python3
"""Provider-neutral Video Resource -> ephemeral Video Reflex v0."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Iterable

@dataclass(frozen=True)
class VideoResource:
    canonical_id: str
    source_pointer: str
    title: str
    provider: str
    duration_ms: int | None = None

    def validate(self) -> None:
        if not self.canonical_id or not self.source_pointer:
            raise ValueError("canonical video identity and source pointer are required")

@dataclass(frozen=True)
class VideoReflexEvent:
    kind: str
    start_ms: int | None = None
    end_ms: int | None = None
    text: str = ""
    meta: dict[str, Any] = field(default_factory=dict)

@dataclass
class VideoReflexSession:
    source: VideoResource
    events: list[VideoReflexEvent]
    closed: bool = False

    def iter_events(self) -> Iterable[VideoReflexEvent]:
        if self.closed:
            raise RuntimeError("video reflex session is closed")
        return tuple(self.events)

    def close(self) -> None:
        self.events.clear()
        self.closed = True


def open_video_reflex(
    resource: VideoResource,
    transcript: list[dict[str, Any]] | None = None,
    scenes: list[dict[str, Any]] | None = None,
    annotations: list[dict[str, Any]] | None = None,
) -> VideoReflexSession:
    resource.validate()
    events = [VideoReflexEvent("video.start", 0, resource.duration_ms, meta={"provider": resource.provider})]
    for item in transcript or []:
        events.append(VideoReflexEvent("transcript.span", int(item["startMs"]), int(item.get("endMs", item["startMs"])), str(item.get("text", ""))))
    for item in scenes or []:
        events.append(VideoReflexEvent("scene", int(item["startMs"]), int(item.get("endMs", item["startMs"])), meta={"label": item.get("label", "")}))
    for item in annotations or []:
        start_ms = int(item.get("startMs", 0))
        end_raw = item.get("endMs")
        events.append(VideoReflexEvent(
            "source.moment",
            start_ms,
            None if end_raw is None else int(end_raw),
            str(item.get("label", "")),
            meta={
                "momentId": item.get("momentId"),
                "keywords": list(item.get("keywords") or []),
                "provenance": dict(item.get("provenance") or {}),
                "confidence": item.get("confidence"),
            },
        ))
    events.append(VideoReflexEvent("video.end", resource.duration_ms, resource.duration_ms))
    return VideoReflexSession(resource, events)


def project_video_timeline(session: VideoReflexSession) -> dict[str, Any]:
    timeline = []
    for event in session.iter_events():
        if event.kind in {"video.start", "video.end"}:
            continue
        timeline.append({
            "kind": event.kind,
            "startMs": event.start_ms,
            "endMs": event.end_ms,
            "text": event.text,
            "meta": event.meta,
        })
    timeline.sort(key=lambda item: (item["startMs"] is None, item["startMs"] or 0, item["kind"]))
    return {
        "schema": "dore.video-reflex.timeline.v0",
        "canonicalId": session.source.canonical_id,
        "sourcePointer": session.source.source_pointer,
        "events": timeline,
        "persistent": False,
    }


def project_video_moments(session: VideoReflexSession) -> dict[str, Any]:
    moments = []
    for index, event in enumerate(session.iter_events()):
        if event.kind == "transcript.span" and event.text.strip():
            moments.append({
                "id": f"moment-{index}",
                "canonicalId": session.source.canonical_id,
                "sourcePointer": session.source.source_pointer,
                "startMs": event.start_ms,
                "endMs": event.end_ms,
                "text": event.text,
                "keywords": [],
                "provenance": {"type": "transcript", "provider": session.source.provider},
            })
        elif event.kind == "source.moment" and event.text.strip():
            provenance = dict(event.meta.get("provenance") or {})
            provenance.setdefault("provider", session.source.provider)
            moments.append({
                "id": event.meta.get("momentId") or f"moment-{index}",
                "canonicalId": session.source.canonical_id,
                "sourcePointer": session.source.source_pointer,
                "startMs": event.start_ms,
                "endMs": event.end_ms,
                "text": event.text,
                "keywords": list(event.meta.get("keywords") or []),
                "provenance": provenance,
                "confidence": event.meta.get("confidence"),
            })
    return {"schema": "dore.video-reflex.moments.v0", "moments": moments, "persistent": False}
