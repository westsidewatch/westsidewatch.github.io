#!/usr/bin/env python3
import json
from pathlib import Path

root = Path(__file__).resolve().parents[2]
resource_payload = json.loads((root / "cinema/data/video-resource.v0.json").read_text(encoding="utf-8"))
moment_payload = json.loads((root / "cinema/data/video-moment.v0.json").read_text(encoding="utf-8"))

assert resource_payload["schema"] == "holy-light.video-resource.v0"
assert moment_payload["schema"] == "holy-light.video-moment.v0"
resources = {item["canonicalId"]: item for item in resource_payload["items"]}
assert resources
assert moment_payload["items"]

seen = set()
for moment in moment_payload["items"]:
    moment_id = moment["momentId"]
    assert moment_id not in seen, f"duplicate momentId: {moment_id}"
    seen.add(moment_id)
    canonical_id = moment["canonicalId"]
    assert canonical_id in resources, f"orphan moment: {moment_id}"
    resource = resources[canonical_id]
    assert moment["sourcePointer"] == resource["sourcePointer"], f"source drift: {moment_id}"
    assert isinstance(moment["startMs"], int) and moment["startMs"] >= 0
    if moment.get("endMs") is not None:
        assert isinstance(moment["endMs"], int) and moment["endMs"] >= moment["startMs"]
    assert moment["label"].strip()
    assert moment.get("provenance", {}).get("type") in {"source-title", "provider-chapter", "editorial", "transcript"}
    assert 0 <= float(moment.get("confidence", 0)) <= 1

waiting = [m for m in moment_payload["items"] if "等候神" in (m["label"] + " " + " ".join(m.get("keywords", [])))]
assert waiting, "real query 等候神 must resolve to at least one canonical VideoMoment"
assert waiting[0]["canonicalId"] == "cinema:video:goodtv:waiting-on-god-no-minute-wasted"
assert waiting[0]["startMs"] == 0

print(f"CINEMA_VIDEO_MOMENT_ACCEPTANCE_PASS resources={len(resources)} moments={len(moment_payload['items'])}")
