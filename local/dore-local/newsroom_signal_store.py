#!/usr/bin/env python3
"""Atomic signal/revision ledger separating observation, execution and publication."""
from __future__ import annotations
import hashlib,json
from datetime import datetime,timezone
from pathlib import Path
VERSION="dore.newsroom-signal-store.v1.0"
def now():return datetime.now(timezone.utc).isoformat()
def load(path):
 try:return json.loads(Path(path).read_text(encoding="utf-8"))
 except (OSError,ValueError):return {"schema":"dore.newsroom-signals.v1","signals":{},"operations":{}}
def save(data,path):
 target=Path(path);target.parent.mkdir(parents=True,exist_ok=True);temp=target.with_suffix(target.suffix+".tmp");temp.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");temp.replace(target)
def canonical_id(observation):
 identity=observation.get("external_id") or (observation.get("provenance") or [{}])[0].get("url")
 if not identity:raise ValueError("signal_identity_required")
 return "world-"+hashlib.sha256(str(identity).strip().lower().encode()).hexdigest()[:20]
def ingest(observation,*,store_path,update_kind="ACTIVE"):
 if update_kind not in {"ACTIVE","CORRECTION","RETRACTION"}:raise ValueError("unsupported_update_kind")
 signal_id=canonical_id(observation);content_hash=observation.get("content_hash")
 if not content_hash:raise ValueError("content_hash_required")
 data=load(store_path);prior=data["signals"].get(signal_id)
 if prior and prior.get("content_hash")==content_hash and prior.get("update_kind")==update_kind:return {"action":"DEDUPLICATED","signal":prior,"operation":None}
 revision=int((prior or {}).get("revision") or 0)+1;operation_id="newsroom-op-"+hashlib.sha256(f"{signal_id}:{revision}:{content_hash}".encode()).hexdigest()[:20]
 signal={**observation,"signal_id":signal_id,"revision":revision,"update_kind":update_kind,"status":"RETRACTED" if update_kind=="RETRACTION" else "ACTIVE","supersedes_revision":prior.get("revision") if prior else None,"ingested_at":now()}
 data["signals"][signal_id]=signal;data["operations"][operation_id]={"operation_id":operation_id,"signal_id":signal_id,"revision":revision,"state":"PREPARED","prepared_at":now(),"publication_state":"HUMAN_GATE_REQUIRED"};save(data,store_path)
 return {"action":"CREATED" if prior is None else update_kind,"signal":signal,"operation":data["operations"][operation_id]}
def commit(operation_id,*,store_path,result):
 data=load(store_path);operation=data["operations"][operation_id];operation.update(state="COMMITTED",committed_at=now(),result_code=result.get("code"),draft_id=(result.get("draft") or {}).get("draft_id"),published=False);save(data,store_path);return operation
def recoverable(store_path):return [x for x in load(store_path)["operations"].values() if x.get("state")=="PREPARED"]
