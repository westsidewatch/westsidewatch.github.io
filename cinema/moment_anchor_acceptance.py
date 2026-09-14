#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
moment_path = ROOT / "data" / "video-moment.v0.json"
coordinate_path = ROOT / "data" / "bible-media-coordinate.v0.json"
graph_path = ROOT / "resource-graph.js"
ui_path = ROOT / "cinema.js"
adapter_path = ROOT / "provider-adapters.js"

moments = json.loads(moment_path.read_text(encoding="utf-8"))
coordinates = json.loads(coordinate_path.read_text(encoding="utf-8"))
graph = graph_path.read_text(encoding="utf-8")
ui = ui_path.read_text(encoding="utf-8")
adapter = adapter_path.read_text(encoding="utf-8")

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
    inherited = {(entry["type"], entry["value"]) for entry in [*work_coordinate.get("text", []), *work_coordinate.get("world", [])]}
    evidence_by_id = {entry.get("id"): entry for entry in moment["evidence"] if entry.get("id")}
    for anchor in moment["anchors"]:
        assert anchor.get("type") in {"scripture", "event", "person", "place", "period", "theme"}
        assert anchor.get("value")
        if (anchor["type"], anchor["value"]) not in inherited:
            evidence_ref = anchor.get("evidenceRef")
            assert evidence_ref in evidence_by_id, f"{moment['momentId']}: granular anchor must reference explicit source evidence"
            source_evidence = evidence_by_id[evidence_ref]
            assert source_evidence.get("type") == "official-episode-metadata"
            assert source_evidence.get("sourcePointer") == moment["sourcePointer"]

    evidence_types = {entry.get("type") for entry in moment["evidence"]}
    assert evidence_types & {"source-title", "official-episode-metadata"}, f"{moment['momentId']}: source evidence required"
    assert any(entry.get("sourcePointer") == moment["sourcePointer"] for entry in moment["evidence"]), f"{moment['momentId']}: evidence must preserve sourcePointer provenance"

exact = [moment for moment in moments["items"] if moment["kind"] == "official-episode"]
exact_by_id = {moment["momentId"]: moment for moment in exact}
assert len(exact) >= 3, "incarnation, baptism, and cross/resurrection exact episodes are required"

expected = {
    "cinema:moment:lumo-matthew:episode-01": (574000, "Matt.1.1-2.23", {"escape-to-egypt", "return-to-nazareth"}),
    "cinema:moment:lumo-matthew:episode-02": (452000, "Matt.3.1-4.25", {"baptism-of-jesus"}),
    "cinema:moment:lumo-matthew:episode-24": (578000, "Matt.27.32-28.20", {"crucifixion", "resurrection"}),
}
for moment_id, (duration, scripture, events) in expected.items():
    moment = exact_by_id[moment_id]
    assert moment["startMs"] == 0 and moment["endMs"] == duration
    assert any(a["type"] == "scripture" and a["value"] == scripture for a in moment["anchors"])
    actual_events = {a["value"] for a in moment["anchors"] if a["type"] == "event"}
    assert events <= actual_events
    evidence = next(e for e in moment["evidence"] if e.get("type") == "official-episode-metadata")
    assert evidence["durationMs"] == duration
    assert evidence["scripture"] == scripture
    assert evidence["provider"] == "Jesus Film Project"

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
assert "resolveMoment(item,moment)" in adapter
assert "exactPointer!==item.sourcePointer" in adapter
assert "hasOfficialEvidence" in adapter
assert "exact:true" in adapter
assert "resolveMoment?.(item,moment)" in ui
assert "cinemaMomentPlayback=target.exact?'exact-source':'work-source'" in ui

print(
    "PASS moment-anchor-v1 "
    f"moments={len(moments['items'])} "
    f"exact={len(exact)} "
    f"works={len({item['workId'] for item in moments['items']})} runtime=exact-source"
)
