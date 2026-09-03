#!/usr/bin/env python3
"""Replay the real iteration-445 failure and its repaired evidence checkpoint."""
import json,tempfile
from pathlib import Path
from multi_loop_agency import checkpoint,peer_poll_due,VERSION
goal={"goal_id":"design-reference-library-expansion-20260901","metadata":{"current_qualified_references":21,"current_source_families":0,"minimum_qualified_references":40,"minimum_source_families":6,"required_homepage_candidates":3}}
job={"state":"PEER_RESEARCH_QUEUED","peer_request_pending":True,"peer_blocking":False,"observed_replies":0}
def evidence(responsive):return {"result":{"browser_evidence":{"observation":{"summary":{"candidate_count":7,"westside_candidate_count":5,"stable_viewports":14,"total_viewports":14},"gates":{"BUILD_PASS":True,"RENDER_PASS":True,"VISUAL_STABLE":True,"DESIGN_DISTINCT":True,"WESTSIDE_FIT":True,"RESPONSIVE_PASS":responsive},"candidates":[{"id":"signal-nocturne","viewports":{"desktop":{"responsive_pass":responsive},"mobile":{"responsive_pass":responsive}}}]}}}}
with tempfile.TemporaryDirectory() as d:
 p=Path(d)/"agency.json";checkpoint(goal,evidence(False),job,state_path=p);repeated=checkpoint(goal,evidence(False),job,state_path=p);fixed=checkpoint(goal,evidence(True),job,state_path=p)
 checks={"repeated_activity_not_progress":repeated["assessment"]["kind"]=="REPEATED_ACTIVITY","responsive_gap_prioritized":repeated["decision"]["route"]=="LOCAL_RESPONSIVE_REPAIR","peer_nonblocking_and_asleep":repeated["decision"]["yield_peer"] and not peer_poll_due(repeated),"repair_creates_evidence_delta":fixed["assessment"]["evidence_delta"].get("responsive_failed")==-1 and fixed["assessment"]["progress"],"next_route_is_reference_expansion":fixed["decision"]["route"]=="LOCAL_REFERENCE_EXPANSION","parent_not_false_passed":fixed["snapshot"]["goal"]["qualified_references"]==21 and fixed["snapshot"]["goal"]["required_references"]==40}
 out={"ok":all(checks.values()),"code":"DORE_MULTI_LOOP_AGENCY_1_ACCEPTANCE_PASS" if all(checks.values()) else "DORE_MULTI_LOOP_AGENCY_1_ACCEPTANCE_FAIL","agency":VERSION,"baseline":"resident iteration 445","checks":checks,"before":repeated,"after":fixed};print(json.dumps(out,ensure_ascii=False));raise SystemExit(0 if out["ok"] else 1)
