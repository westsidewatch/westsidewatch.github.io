#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
moment_path = ROOT / "data" / "video-moment.v0.json"
coordinate_path = ROOT / "data" / "bible-media-coordinate.v0.json"
graph_path = ROOT / "resource-graph.js"
ui_path = ROOT / "cinema.js"

moments = json.loads(moment_path.read_text(encoding="utf-8"))
coordinates = json.loads(coordinate_path.read_text(encoding="utf-8"))
graph = graph_path.read_text(encoding="utf-8")
ui = ui_path.read_text(encoding="utf-8")

assert moments["schema"] == "dore.bible-media-moment.v1"
assert isinstance(moments.get("items"), list) and moments["items"], "Moment corpus must not be empty"
coordinate_by_work = {item["canonicalId"]: item for item in coordinates["items"]}
seen = set()

for moment in moments["items"]:
    required = {"momentId", "workId", "kind", "sourcePointer", "startMs", "endMs", "label", "anchors", "evidence"}
    missing = required - set(moment)
    assert not missing, f"{moment.get('momentId')}: missing {sorted(missing)}"
    assert moment["momentId"] not in seen, f"duplicate momentId: {moment['momentId']}"
    seen.add(moment["momentId"])
    assert moment["workId"] in coordinate_by_work, f"unknown workId: {moment['workId']}"
    assert isinstance(moment["startMs"], int) and moment["startMs"] >= 0
    assert moment["endMs"] is None or (isinstance(moment["endMs"], int) and moment["endMs"] > moment["startMs"])
    assert moment["anchors"], f"{moment['momentId']}: anchors required"
    assert moment["evidence"], f"{moment['momentId']}: evidence required"

    work_coordinate = coordinate_by_work[moment["workId"]]["coordinates"]
    permitted = {
        (entry["type"], entry["value"])
        for entry in [*work_coordinate.get("text", []), *work_coordinate.get("world", [])]
    }
    for anchor in moment["anchors"]:
        assert anchor.get("type") in {"scripture", "event", "person", "place", "period", "theme"}
        assert anchor.get("value")
        assert (anchor["type"], anchor["value"]) in permitted, (
            f"{moment['momentId']}: anchor {anchor['type']}:{anchor['value']} "
            "must be grounded by the current work coordinate"
        )

    evidence_types = {entry.get("type") for entry in moment["evidence"]}
    assert "source-title" in evidence_types, f"{moment['momentId']}: source-title evidence required"
    assert any(entry.get("sourcePointer") == moment["sourcePointer"] for entry in moment["evidence"]), (
        f"{moment['momentId']}: evidence must preserve sourcePointer provenance"
    )

assert "queryMoments" in graph
assert "momentsForAnchor" in graph
assert "deepLink" in graph
assert "moment(momentId)" in graph
assert "MOMENT_SCHEMA='dore.bible-media-moment.v1'" in graph
assert "searchParams.set('moment',momentId)" in graph
assert "restoreMomentFromUrl" in ui
assert "openMoment(moment" in ui
assert "moment.anchors" in ui
assert "moment.workId" in ui

print(
    "PASS moment-anchor-v1 "
    f"moments={len(moments['items'])} "
    f"works={len({item['workId'] for item in moments['items']})}"
)
