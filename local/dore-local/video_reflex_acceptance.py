#!/usr/bin/env python3
from video_reflex import VideoResource, open_video_reflex, project_video_moments

resource = VideoResource("teaching:test-001", "https://example.org/watch/001", "Test Teaching", "fixture", 120000)
session = open_video_reflex(resource, transcript=[
    {"startMs": 12000, "endMs": 16800, "text": "等候神"},
    {"startMs": 17000, "endMs": 23000, "text": "安靜在主面前"},
], scenes=[{"startMs": 0, "endMs": 30000, "label": "opening"}])
projection = project_video_moments(session)
assert projection["persistent"] is False
assert len(projection["moments"]) == 2
assert projection["moments"][0]["canonicalId"] == resource.canonical_id
assert projection["moments"][0]["sourcePointer"] == resource.source_pointer
assert projection["moments"][0]["startMs"] == 12000
assert projection["moments"][0]["text"] == "等候神"
session.close()
assert session.closed and session.events == []
try:
    open_video_reflex(VideoResource("", "", "bad", "fixture"))
except ValueError:
    pass
else:
    raise AssertionError("missing canonical identity must be rejected")
print("VIDEO_REFLEX_ACCEPTANCE_PASS")
