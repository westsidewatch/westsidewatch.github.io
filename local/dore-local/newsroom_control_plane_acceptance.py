#!/usr/bin/env python3
import json
import tempfile
from pathlib import Path
from multi_loop_control_plane import load, register, route, wake
from newsroom_control_plane import VERSION, run_episode

with tempfile.TemporaryDirectory() as d:
    state = Path(d) / "state.json"; assets = Path(d) / "assets.jsonl"
    register("storybook", "Continue a checkpointable low-priority design task", kind="storybook", priority=50, state_path=state)
    wake("storybook", "work-started", state_path=state); route(state_path=state)
    signal = {"signal_id": "acceptance-world-001", "title": "Verified Toronto emergency affects neighbours", "summary": "A verified local emergency requires factual reporting and prayerful response", "occurred_at": "2026-09-03T12:00:00Z", "provenance": [{"publisher": "City of Toronto", "url": "https://www.toronto.ca/example"}], "topics": ["toronto", "emergency", "prayer"], "urgency": 5, "local_relevance": 5, "mission_relevance": 5, "verification_confidence": 5, "human_impact": 5, "unknowns": ["full impact"]}
    enrichment = {"knowledge_id": "dawn-newsroom-acceptance-1", "kind": "incremental-enrichment", "provenance_preserved": True, "sources": [{"id": "toronto-emergency-prayer", "url": "https://www.toronto.ca/example", "publisher": "City of Toronto", "title": "Toronto emergency prayer response"}], "source_count": 1}
    result = run_episode(signal, state_path=state, asset_path=assets, enrichment_asset=enrichment)
    final = load(state); events = result.get("events") or []
    checks = {"verified_signal_preempts": result.get("initial_route") == "newsroom-world-response", "lower_work_yields": "YIELD" in events, "dawn_incremental_enrichment_used": result.get("enriched") is True and not result.get("knowledge_gaps"), "shared_knowledge_reused": "dawn-newsroom-acceptance-1" in result.get("reused_assets", []), "prayer_and_report_drafted": bool((result.get("draft") or {}).get("prayer")) and bool((result.get("draft") or {}).get("report")), "no_autonomous_publish": result.get("published") is False and (result.get("draft") or {}).get("requires_human_editor") is True, "original_loop_resumed": result.get("resumed_loop") == "storybook" and final.get("active") == "storybook", "durable_record": "NEWSROOM_EPISODE_COMPLETE" in events}
    ok = all(checks.values())
    print(json.dumps({"ok": ok, "code": "DORE_NEWSROOM_CONTROL_PLANE_1_PASS" if ok else "DORE_NEWSROOM_CONTROL_PLANE_1_FAIL", "newsroom": VERSION, "checks": checks, "events": events, "draft_id": (result.get("draft") or {}).get("draft_id")}, ensure_ascii=False))
    raise SystemExit(0 if ok else 1)
