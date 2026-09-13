#!/usr/bin/env python3
from video_reflex import VideoResource, open_video_reflex, project_video_moments, project_video_timeline

resource = VideoResource("teaching:test-001", "https://example.org/watch/001", "Test Teaching", "fixture", 120000)
session = open_video_reflex(
    resource,
    transcript=[
        {"startMs": 12000, "endMs": 16800, "text": "等候神"},
        {"startMs": 17000, "endMs": 23000, "text": "安靜在主面前"},
    ],
    scenes=[{"startMs": 0, "endMs": 30000, "label": "opening"}],
    annotations=[{
        "momentId": "source-title",
        "startMs": 0,
        "endMs": None,
        "label": "Test Teaching",
        "keywords": ["teaching"],
        "provenance": {"type": "source-title"},
        "confidence": 1.0,
    }],
)
projection = project_video_moments(session)
timeline = project_video_timeline(session)
assert projection["persistent"] is False
assert timeline["persistent"] is False
assert timeline["canonicalId"] == resource.canonical_id
assert timeline["sourcePointer"] == resource.source_pointer
assert len(projection["moments"]) == 3
assert projection["moments"][0]["canonicalId"] == resource.canonical_id
assert projection["moments"][0]["sourcePointer"] == resource.source_pointer
assert projection["moments"][0]["startMs"] == 12000
assert projection["moments"][0]["text"] == "等候神"
source_moment = next(moment for moment in projection["moments"] if moment["id"] == "source-title")
assert source_moment["startMs"] == 0
assert source_moment["provenance"]["type"] == "source-title"
assert source_moment["provenance"]["provider"] == "fixture"
assert any(event["kind"] == "scene" for event in timeline["events"])
assert any(event["kind"] == "source.moment" for event in timeline["events"])
session.close()
assert session.closed and session.events == []
try:
    open_video_reflex(VideoResource("", "", "bad", "fixture"))
except ValueError:
    pass
else:
    raise AssertionError("missing canonical identity must be rejected")
print("VIDEO_REFLEX_ACCEPTANCE_PASS")
