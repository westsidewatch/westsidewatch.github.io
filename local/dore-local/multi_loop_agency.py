#!/usr/bin/env python3
"""Doré Multi-Loop Agency 1.0. Execution is activity; evidence delta is progress."""
from __future__ import annotations
import hashlib, json, os
from datetime import datetime, timedelta, timezone
from pathlib import Path
VERSION="dore.multi-loop-agency.v1.0"; HOME=Path(os.environ.get("DORE_LOCAL_HOME",Path.home()/".dore")).expanduser(); STORE=HOME/"agency"
def now():return datetime.now(timezone.utc).isoformat()
def _hash(v):return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def _int(v):
 try:return int(v or 0)
 except (TypeError,ValueError):return 0
def observation_from_result(result):
 parsed=result.get("result") if isinstance(result,dict) else None
 if not isinstance(parsed,dict):return {}
 evidence=parsed.get("browser_evidence") or {}; observation=evidence.get("observation") if isinstance(evidence,dict) else None
 if isinstance(observation,dict):return observation
 for state in reversed((parsed.get("driver") or {}).get("states") or []):
  if isinstance(state,dict) and isinstance(state.get("observation"),dict):return state["observation"]
 return {}
def snapshot(goal,result,job=None):
 meta=goal.get("metadata") or {}; obs=observation_from_result(result); gates=obs.get("gates") or {}; candidates=obs.get("candidates") or []; summary=obs.get("summary") or {}
 failed=sum(1 for c in candidates if any(not bool((v or {}).get("responsive_pass",True)) for v in (c.get("viewports") or {}).values()))
 if gates.get("RESPONSIVE_PASS") is False and not failed:failed=1
 goal_state={"qualified_references":max(_int(meta.get("current_qualified_references")),_int((job or {}).get("qualified_references"))),"source_families":max(_int(meta.get("current_source_families")),_int((job or {}).get("source_families"))),"required_references":_int(meta.get("minimum_qualified_references")),"required_source_families":_int(meta.get("minimum_source_families")),"required_candidates":_int(meta.get("required_homepage_candidates"))}
 evidence={"candidate_count":_int(summary.get("candidate_count")) or len(candidates),"responsive_failed":failed,"stable_viewports":_int(summary.get("stable_viewports")),"total_viewports":_int(summary.get("total_viewports")),"gates":{k:gates.get(k) for k in sorted(gates)}}
 peer={"pending":bool((job or {}).get("peer_request_pending")),"observed_replies":_int((job or {}).get("observed_replies"))}; signature=_hash({"goal":goal_state,"evidence":evidence,"peer_replies":peer["observed_replies"]})
 return {"schema":"dore.agency-snapshot.v1","goal_id":goal.get("goal_id"),"at":now(),"goal":goal_state,"evidence":evidence,"peer":peer,"signature":signature}
def evaluate(previous,current):
 if not previous:return {"progress":True,"kind":"BASELINE_CAPTURED","information_gain":True,"goal_delta":{},"evidence_delta":{},"repeated_activity":False}
 gd={k:current["goal"].get(k,0)-previous["goal"].get(k,0) for k in ("qualified_references","source_families")}; ed={k:current["evidence"].get(k,0)-previous["evidence"].get(k,0) for k in ("candidate_count","stable_viewports","responsive_failed")}
 progress=any(v>0 for v in gd.values()) or ed["candidate_count"]>0 or ed["stable_viewports"]>0 or ed["responsive_failed"]<0 or current["peer"]["observed_replies"]>previous.get("peer",{}).get("observed_replies",0)
 return {"progress":progress,"kind":"MATERIAL_PROGRESS" if progress else "REPEATED_ACTIVITY","information_gain":current["signature"]!=previous.get("signature"),"goal_delta":gd,"evidence_delta":ed,"repeated_activity":not progress}
def prioritize(current,assessment,stall_count=0):
 g=current["goal"]; e=current["evidence"]; p=current["peer"]
 if e["responsive_failed"]:return {"route":"LOCAL_RESPONSIVE_REPAIR","priority":100,"reason":"measured responsive failure is the highest-value actionable local gap","yield_peer":True}
 if g["qualified_references"]<g["required_references"] or g["source_families"]<g["required_source_families"]:return {"route":"LOCAL_REFERENCE_EXPANSION","priority":80,"reason":"reference/source-family acceptance remains unmet","yield_peer":bool(p["pending"] and p["observed_replies"]==0)}
 if p["pending"] and p["observed_replies"]==0:return {"route":"PEER_WAIT_SLEEP","priority":10,"reason":"peer pending has no evidence delta","yield_peer":True}
 return {"route":"RESUME_PARENT","priority":60,"reason":"no higher-value actionable gap","yield_peer":False}
def checkpoint(goal,result,job=None,*,state_path=None):
 path=Path(state_path) if state_path else STORE/f"{goal['goal_id']}.json"
 try:previous=json.loads(path.read_text())
 except Exception:previous={}
 current=snapshot(goal,result,job); assessment=evaluate(previous.get("snapshot"),current); stall=0 if assessment["progress"] else _int(previous.get("stall_count"))+1; decision=prioritize(current,assessment,stall)
 cooldown=(datetime.now(timezone.utc)+timedelta(minutes=min(60,5*(2**min(stall,3))))).isoformat() if decision["yield_peer"] else None
 record={"schema":"dore.multi-loop-agency-state.v1","agency":VERSION,"updated_at":now(),"snapshot":current,"assessment":assessment,"stall_count":stall,"decision":decision,"peer_cooldown_until":cooldown}
 path.parent.mkdir(parents=True,exist_ok=True); tmp=path.with_suffix(path.suffix+".tmp"); tmp.write_text(json.dumps(record,ensure_ascii=False,indent=2)); tmp.replace(path); return record
def peer_poll_due(record,at=None):
 value=(record or {}).get("peer_cooldown_until")
 if not value:return True
 try:return (at or datetime.now(timezone.utc))>=datetime.fromisoformat(value)
 except (TypeError,ValueError):return True
