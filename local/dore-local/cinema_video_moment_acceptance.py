#!/usr/bin/env python3
import json
from pathlib import Path

root = Path(__file__).resolve().parents[2]
resource_payload = json.loads((root / "cinema/data/video-resource.v0.json").read_text(encoding="utf-8"))
moment_payload = json.loads((root / "cinema/data/video-moment.v0.json").read_text(encoding="utf-8"))

assert resource_payload["schema"] == "holy-light.video-resource.v0"
assert moment_payload["schema"] == "dore.bible-media-moment.v1"
resources = {item["canonicalId"]: item for item in resource_payload["items"]}
assert resources
assert moment_payload["items"]

seen = set()
for moment in moment_payload["items"]:
    moment_id = moment["momentId"]
    assert moment_id not in seen, f"duplicate momentId: {moment_id}"
    seen.add(moment_id)
    work_id = moment["workId"]
    assert work_id in resources, f"orphan moment: {moment_id}"
    resource = resources[work_id]
    exact_source = moment["sourcePointer"] != resource["sourcePointer"]
    if exact_source:
        assert moment.get("kind") == "official-episode", f"unexpected source drift: {moment_id}"
        assert any(
            e.get("type") == "official-episode-metadata" and e.get("sourcePointer") == moment["sourcePointer"]
            for e in moment.get("evidence", [])
        ), f"exact source lacks official episode evidence: {moment_id}"
    assert isinstance(moment["startMs"], int) and moment["startMs"] >= 0
    if moment.get("endMs") is not None:
        assert isinstance(moment["endMs"], int) and moment["endMs"] > moment["startMs"]
    assert moment["label"].strip()
    assert moment.get("kind") in {"source-title", "official-episode", "provider-chapter", "editorial", "transcript"}
    assert moment.get("anchors"), f"anchors required: {moment_id}"
    assert moment.get("evidence"), f"evidence required: {moment_id}"
    assert any(e.get("sourcePointer") == moment["sourcePointer"] for e in moment["evidence"]), f"source evidence missing: {moment_id}"
    assert 0 <= float(moment.get("confidence", 0)) <= 1

waiting = [m for m in moment_payload["items"] if any(a.get("value") == "waiting-on-god" for a in m.get("anchors", []))]
assert waiting, "real query 等候神 must resolve to at least one canonical VideoMoment"
assert waiting[0]["workId"] == "cinema:video:goodtv:waiting-on-god-no-minute-wasted"
assert waiting[0]["startMs"] == 0

exact = [m for m in moment_payload["items"] if m.get("kind") == "official-episode"]
assert exact, "at least one official-episode Moment required"
assert exact[0]["endMs"] == 574000

print(f"CINEMA_VIDEO_MOMENT_ACCEPTANCE_PASS resources={len(resources)} moments={len(moment_payload['items'])} exact={len(exact)}")
