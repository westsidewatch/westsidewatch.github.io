#!/usr/bin/env python3
"""Two Days Phase 4: bind TODAY to canonical Doré capabilities.

The bridge does not invent capabilities or providers. It resolves only IDs that
exist in the canonical Doré capability registry and emits a small context pack.
TODAY remains state authority; Doré remains capability authority.
"""
from __future__ import annotations
import json,os
from pathlib import Path
from typing import Any
import two_days_today as today_mod

SCHEMA="two-days.capability-context.v0"
REGISTRY=Path(__file__).resolve().parents[2]/"dore-core/runtime/capability-registry.v1.json"

DEFAULT_PROFILES={
 "writing":["context.fuzzy-search","knowledge.recall","publishing.dimensional-writing"],
 "publishing":["context.fuzzy-search","knowledge.recall","publishing.book-intelligence","publishing.book-compile"],
 "bible-study":["context.fuzzy-search","knowledge.recall","bible.query-plan","bible.scripture-search","bible.original-language-search"],
 "design":["context.fuzzy-search","knowledge.recall","design.intelligence"],
}

def _registry()->dict[str,dict[str,Any]]:
 raw=json.loads(REGISTRY.read_text(encoding="utf-8"))
 return {c["id"]:c for c in raw.get("capabilities",[])}

def resolve(profile:str="writing",extra:list[str]|None=None,today:dict[str,Any]|None=None)->dict[str,Any]:
 state=today or today_mod.read()
 ids=list(DEFAULT_PROFILES.get(profile,[]))
 if not ids:raise ValueError("two_days_unknown_capability_profile")
 for cid in extra or []:
  if cid not in ids:ids.append(cid)
 reg=_registry();missing=[cid for cid in ids if cid not in reg]
 if missing:raise ValueError("two_days_unknown_capability:"+",".join(missing))
 caps=[]
 for cid in ids:
  c=reg[cid]
  caps.append({k:c[k] for k in ("id","type","service","status","execution","entrypoint","binding","provider","cost","network","load") if k in c})
 active=state.get("active_head")
 work=state.get("work_heads",{}).get(active,{}) if active else {}
 return {
  "schema_id":SCHEMA,
  "task":{"active_artifact":active,"accepted_head":work.get("accepted_head"),"working_head":work.get("working_head"),"resume_head":state.get("resume_head")},
  "capability_profile":profile,
  "capability_refs":caps,
  "source_refs":state.get("source_refs",[]),
  "authority":{"state":"TODAY","capability":"dore-core-registry","artifact_text":"artifact-ledger","may_rewrite_author_thesis":False},
 }

def verify(pack:dict[str,Any])->dict[str,Any]:
 reg=_registry()
 for c in pack.get("capability_refs",[]):
  cid=c.get("id")
  if cid not in reg:raise ValueError("two_days_capability_not_canonical")
  canonical=reg[cid]
  for k,v in c.items():
   if canonical.get(k)!=v:raise ValueError("two_days_capability_drift")
 return {"ok":True,"code":"TWO_DAYS_CAPABILITY_CONTEXT_VERIFIED","capabilities":[c["id"] for c in pack.get("capability_refs",[])]}
