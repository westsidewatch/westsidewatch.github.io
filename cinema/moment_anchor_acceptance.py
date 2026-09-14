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
    inherited = {
        (entry["type"], entry["value"])
        for entry in [*work_coordinate.get("text", []), *work_coordinate.get("world", [])]
    }
    evidence_by_id = {entry.get("id"): entry for entry in moment["evidence"] if entry.get("id")}
    for anchor in moment["anchors"]:
        assert anchor.get("type") in {"scripture", "event", "person", "place", "period", "theme"}
        assert anchor.get("value")
        if (anchor["type"], anchor["value"]) not in inherited:
            evidence_ref = anchor.get("evidenceRef")
            assert evidence_ref in evidence_by_id, (
                f"{moment['momentId']}: granular anchor {anchor['type']}:{anchor['value']} "
                "must reference explicit source evidence"
            )
            source_evidence = evidence_by_id[evidence_ref]
            assert source_evidence.get("type") == "official-episode-metadata"
            assert source_evidence.get("sourcePointer") == moment["sourcePointer"]

    evidence_types = {entry.get("type") for entry in moment["evidence"]}
    assert evidence_types & {"source-title", "official-episode-metadata"}, (
        f"{moment['momentId']}: source evidence required"
    )
    assert any(entry.get("sourcePointer") == moment["sourcePointer"] for entry in moment["evidence"]), (
        f"{moment['momentId']}: evidence must preserve sourcePointer provenance"
    )

exact = [moment for moment in moments["items"] if moment["kind"] == "official-episode"]
assert exact, "at least one exact official episode Moment is required"
first = exact[0]
assert first["momentId"] == "cinema:moment:lumo-matthew:episode-01"
assert first["startMs"] == 0 and first["endMs"] == 574000
assert any(a["type"] == "scripture" and a["value"] == "Matt.1.1-2.23" for a in first["anchors"])
assert {a["type"] for a in first["anchors"]} >= {"scripture", "event", "person", "place", "period"}
assert first["sourcePointer"].endswith("/lumo-matthew-1-1-2-23.html")

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
    f"exact={len(exact)} "
    f"works={len({item['workId'] for item in moments['items']})}"
)
