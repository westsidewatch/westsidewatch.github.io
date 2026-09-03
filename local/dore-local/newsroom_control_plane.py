#!/usr/bin/env python3
"""Event-driven Newsroom adapter; never publishes autonomously."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from multi_loop_control_plane import complete, event, load, register, route, save, share, wake
from newsroom_signal_store import commit as commit_signal_operation, ingest as ingest_signal

VERSION = "dore.newsroom-control-plane.v1.0"
NEWSROOM_LOOP = "newsroom-world-response"
DAWN_LOOP = "dawn-library-enrichment"


def now():
    return datetime.now(timezone.utc).isoformat()


def _words(value):
    return {x.strip(".,:;!?()[]{}\"'").lower() for x in str(value or "").split() if len(x.strip()) > 2}


def validate_signal(signal):
    required = ("signal_id", "title", "summary", "occurred_at", "provenance")
    missing = [name for name in required if not signal.get(name)]
    provenance = signal.get("provenance") or []
    if not isinstance(provenance, list) or not provenance:
        missing = sorted(set(missing + ["provenance"]))
    if any(not isinstance(x, dict) or not x.get("url") or not x.get("publisher") for x in provenance):
        missing = sorted(set(missing + ["provenance.publisher_url"]))
    return {"ok": not missing, "missing": missing}


def editorial_gravity(signal):
    """Bounded score; popularity is deliberately not an input."""
    urgency = max(0, min(5, int(signal.get("urgency") or 0)))
    local = max(0, min(5, int(signal.get("local_relevance") or 0)))
    mission = max(0, min(5, int(signal.get("mission_relevance") or 0)))
    confidence = max(0, min(5, int(signal.get("verification_confidence") or 0)))
    harm = max(0, min(5, int(signal.get("human_impact") or 0)))
    score = urgency * 5 + local * 4 + mission * 3 + confidence * 2 + harm * 4
    return {"score": min(80, score), "preempt": score >= 48 and confidence >= 3, "components": {"urgency": urgency, "local_relevance": local, "mission_relevance": mission, "verification_confidence": confidence, "human_impact": harm}}


def load_assets(asset_path):
    path = Path(asset_path)
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            asset = (json.loads(line).get("asset") or {})
            if asset.get("provenance_preserved"):
                rows.append(asset)
        except ValueError:
            continue
    return rows


def relevant_assets(signal, assets):
    wanted = _words(signal.get("title")) | _words(signal.get("summary")) | {str(x).lower() for x in signal.get("topics") or []}
    matched = []
    for asset in assets:
        overlap = sorted(wanted & _words(json.dumps(asset, ensure_ascii=False)))
        if overlap:
            matched.append({"asset": asset, "overlap": overlap})
    return matched


def knowledge_gaps(signal, matches):
    covered = set()
    for match in matches:
        covered.update(match["overlap"])
    return sorted({str(x).lower() for x in signal.get("topics") or []} - covered)


def _ensure_loops(state_path):
    state = load(state_path)
    if NEWSROOM_LOOP not in state["workflows"]:
        register(NEWSROOM_LOOP, "Sense, discern and draft a prayer/report response to a verified WorldSignal", kind="newsroom", priority=75, state_path=state_path, metadata={"publication_policy": "human-editor-required"})
    state = load(state_path)
    if DAWN_LOOP not in state["workflows"]:
        register(DAWN_LOOP, "Incrementally enrich reusable knowledge for active loops", kind="dawn-library", priority=65, state_path=state_path)


def _record_newsroom_metadata(state_path, **updates):
    state = load(state_path)
    row = state["workflows"][NEWSROOM_LOOP]
    row.setdefault("metadata", {}).update(updates)
    row["updated_at"] = now()
    save(state, state_path)


def draft_response(signal, matches):
    citations = [{"publisher": x["publisher"], "url": x["url"]} for x in signal.get("provenance") or []]
    for match in matches:
        for source in match["asset"].get("sources") or []:
            if source.get("url"):
                citations.append({"publisher": source.get("publisher") or source.get("title") or "Dawn Library", "url": source["url"]})
    unique = list({x["url"]: x for x in citations}.values())
    revision = int(signal.get("revision") or 1)
    draft_id = "newsroom-draft-" + hashlib.sha256(f'{signal["signal_id"]}:{revision}'.encode()).hexdigest()[:12]
    return {"schema": "dore.newsroom-draft.v1", "draft_id": draft_id, "signal_id": signal["signal_id"], "status": "EDITORIAL_REVIEW", "publishable": False, "prayer": {"title": "為此刻守望", "body": "在尚未掌握全部情況以前，我們先為受影響的人、回應者與需要作判斷的人禱告；求真實被看見，求傷害不被利用。"}, "report": {"title": signal["title"], "summary": signal["summary"], "known": "Only claims supported by the attached provenance are retained.", "unknown": list(signal.get("unknowns") or [])}, "citations": unique, "requires_human_editor": True, "created_at": now()}


def run_episode(signal, *, state_path, asset_path, enrichment_asset=None):
    valid = validate_signal(signal)
    if not valid["ok"]:
        return {"ok": False, "code": "WORLD_SIGNAL_REJECTED", "validation": valid}
    _ensure_loops(state_path)
    gravity = editorial_gravity(signal)
    if not gravity["preempt"]:
        _record_newsroom_metadata(state_path, last_signal=signal, last_gravity=gravity, disposition="RECORDED_NO_PREEMPT")
        return {"ok": True, "code": "WORLD_SIGNAL_RECORDED", "preempted": False, "gravity": gravity}
    wake(NEWSROOM_LOOP, "verified-world-signal:" + signal["signal_id"], gravity=gravity["score"], state_path=state_path)
    routed = route(state_path=state_path)
    matches = relevant_assets(signal, load_assets(asset_path))
    gaps = knowledge_gaps(signal, matches)
    _record_newsroom_metadata(state_path, last_signal=signal, last_gravity=gravity, reused_knowledge_ids=[x["asset"]["knowledge_id"] for x in matches], knowledge_gaps=gaps)
    enriched = False
    if gaps and enrichment_asset:
        wake(DAWN_LOOP, "newsroom-knowledge-gap:" + ",".join(gaps), gravity=gravity["score"] + 20, state_path=state_path)
        route(state_path=state_path)
        share(DAWN_LOOP, enrichment_asset, state_path=state_path, asset_path=asset_path)
        complete(DAWN_LOOP, state_path=state_path)
        matches = relevant_assets(signal, load_assets(asset_path))
        gaps = knowledge_gaps(signal, matches)
        enriched = True
        _record_newsroom_metadata(state_path, reused_knowledge_ids=[x["asset"]["knowledge_id"] for x in matches], knowledge_gaps=gaps)
    draft = draft_response(signal, matches)
    draft_asset = {"knowledge_id": draft["draft_id"], "kind": "newsroom-editorial-draft", "provenance_preserved": True, "signal_id": signal["signal_id"], "sources": draft["citations"], "draft": draft}
    share(NEWSROOM_LOOP, draft_asset, state_path=state_path, asset_path=asset_path)
    _record_newsroom_metadata(state_path, last_draft_id=draft["draft_id"], disposition="EDITORIAL_REVIEW")
    resumed = complete(NEWSROOM_LOOP, state_path=state_path)
    state = load(state_path)
    event(state, "NEWSROOM_EPISODE_COMPLETE", loop_id=NEWSROOM_LOOP, signal_id=signal["signal_id"], draft_id=draft["draft_id"], human_editor_required=True)
    save(state, state_path)
    return {"ok": True, "code": "NEWSROOM_DRAFT_READY", "preempted": True, "initial_route": routed["loop_id"] if routed else None, "gravity": gravity, "reused_assets": [x["asset"]["knowledge_id"] for x in matches], "knowledge_gaps": gaps, "enriched": enriched, "draft": draft, "resumed_loop": resumed["loop_id"] if resumed else None, "published": False, "events": [x["event"] for x in load(state_path)["events"]]}


def ingest_and_run(observation, *, signal_store_path, state_path, asset_path, update_kind="ACTIVE", enrichment_asset=None):
    """Idempotently ingest one observation and transactionally run it."""
    receipt = ingest_signal(observation, store_path=signal_store_path, update_kind=update_kind)
    if receipt["action"] == "DEDUPLICATED":
        return {"ok": True, "code": "WORLD_SIGNAL_DEDUPLICATED", "signal_id": receipt["signal"]["signal_id"], "revision": receipt["signal"]["revision"], "published": False}
    signal = receipt["signal"]
    if update_kind == "RETRACTION":
        result = {"ok": True, "code": "WORLD_SIGNAL_RETRACTED", "signal_id": signal["signal_id"], "revision": signal["revision"], "published": False, "requires_human_editor": True}
    else:
        signal.setdefault("topics", []);signal.setdefault("urgency", 3);signal.setdefault("local_relevance", 2);signal.setdefault("mission_relevance", 3);signal.setdefault("verification_confidence", 5);signal.setdefault("human_impact", 3);signal.setdefault("unknowns", ["independent corroboration and full impact"])
        result = run_episode(signal, state_path=state_path, asset_path=asset_path, enrichment_asset=enrichment_asset)
    commit_signal_operation(receipt["operation"]["operation_id"], store_path=signal_store_path, result=result)
    return {**result, "signal_id": signal["signal_id"], "revision": signal["revision"], "update_kind": update_kind, "operation_id": receipt["operation"]["operation_id"]}
