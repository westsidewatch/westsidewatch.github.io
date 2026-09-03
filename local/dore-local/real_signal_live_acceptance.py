#!/usr/bin/env python3
"""Live, no-publish acceptance against an official free Atom feed."""
import json,os,tempfile
from pathlib import Path
from multi_loop_control_plane import load,register,route,wake
from newsroom_control_plane import ingest_and_run
from real_signal_connector import DEFAULT_FEED,fetch_atom
with tempfile.TemporaryDirectory() as d:
 root=Path(d);state=root/"state.json";assets=root/"assets.jsonl";signals=root/"signals.json"
 feed=fetch_atom(os.environ.get("DORE_REAL_SIGNAL_FEED",DEFAULT_FEED),limit=1,usage_file=str(root/"usage.json"))
 if not feed["observations"]:raise SystemExit("official_feed_returned_no_observations")
 observation=feed["observations"][0];observation.update(urgency=5,local_relevance=4,mission_relevance=5,verification_confidence=5,human_impact=5,topics=[])
 register("storybook","Checkpointable original work",kind="storybook",priority=50,state_path=state);wake("storybook","live-acceptance",state_path=state);route(state_path=state)
 first=ingest_and_run(observation,signal_store_path=signals,state_path=state,asset_path=assets);replay=ingest_and_run(observation,signal_store_path=signals,state_path=state,asset_path=assets)
 checks={"real_official_source":observation["provenance"][0]["publisher"]=="Government of Canada" and observation["provenance"][0]["url"].startswith("https://"),"free_no_key_connector":feed["free_api_budget"]["provider"]=="canada-news-atom","draft_created":first.get("code")=="NEWSROOM_DRAFT_READY","replay_deduplicated":replay.get("code")=="WORLD_SIGNAL_DEDUPLICATED","no_autonomous_publish":first.get("published") is False and first.get("draft",{}).get("requires_human_editor") is True,"original_loop_resumed":first.get("resumed_loop")=="storybook" and load(state).get("active")=="storybook"}
 ok=all(checks.values());print(json.dumps({"ok":ok,"code":"DORE_REAL_SIGNAL_LOOP_1_PASS" if ok else "DORE_REAL_SIGNAL_LOOP_1_FAIL","checks":checks,"source":observation["provenance"][0],"signal_id":first.get("signal_id"),"revision":first.get("revision"),"draft_id":first.get("draft",{}).get("draft_id")},ensure_ascii=False));raise SystemExit(0 if ok else 1)
