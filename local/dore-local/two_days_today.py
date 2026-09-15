#!/usr/bin/env python3
"""Two Days Phase 3: deterministic, rebuildable TODAY projection.

TODAY is a small projection, never source authority. It is rebuilt from the
artifact ledger and carries verifiable pointers to exact accepted/working text.
"""
from __future__ import annotations
import hashlib,json,os,sqlite3
from datetime import datetime,timezone
from pathlib import Path
from typing import Any
import two_days_artifact_ledger as ledger

SCHEMA="two-days.today.v0"

def _home()->Path:
 base=Path(os.environ.get("DORE_LOCAL_HOME") or "~/Library/Application Support/Dore").expanduser()
 return Path(os.environ.get("DORE_TWO_DAYS_HOME") or (base/"two-days")).expanduser()
def _path()->Path:return _home()/"state"/"today.json"
def _now()->str:return datetime.now(timezone.utc).isoformat()
def _sha(text:str)->str:return hashlib.sha256(text.encode("utf-8")).hexdigest()
def _ledger_db()->Path:return _home()/"state"/"artifact-ledger.db"

def _version_ref(db,artifact_id:str,version_id:str|None):
 if not version_id:return None
 row=db.execute("SELECT content_sha256 FROM versions WHERE artifact_id=? AND version_id=?",(artifact_id,version_id)).fetchone()
 if not row:raise ValueError("today_unknown_version")
 return {"version_id":version_id,"sha256":row[0]}

def build(active_artifact:str|None=None,resume:dict[str,Any]|None=None)->dict[str,Any]:
 dbp=_ledger_db()
 if not dbp.exists():
  return {"schema_id":SCHEMA,"active_head":None,"work_heads":{},"resume_head":resume,"source_refs":[],"generated_at":_now()}
 db=sqlite3.connect(dbp)
 try:
  rows=db.execute("SELECT artifact_id,accepted_head,working_head FROM heads ORDER BY artifact_id").fetchall()
  work={}
  for aid,accepted,working in rows:
   work[aid]={"accepted_head":_version_ref(db,aid,accepted),"working_head":_version_ref(db,aid,working)}
  if active_artifact is None and rows:active_artifact=rows[-1][0]
  if active_artifact is not None and active_artifact not in work:raise ValueError("today_unknown_active_artifact")
  source_refs=[]
  for eid,aid,etype,fv,tv,created in db.execute("SELECT event_id,artifact_id,event_type,from_version,to_version,created_at FROM events ORDER BY rowid"):
   source_refs.append({"event_id":eid,"artifact_id":aid,"event_type":etype,"from_version":fv,"to_version":tv,"created_at":created})
  return {"schema_id":SCHEMA,"active_head":active_artifact,"work_heads":work,"resume_head":resume,"source_refs":source_refs,"generated_at":_now()}
 finally:db.close()

def canonical(today:dict[str,Any])->str:
 stable={k:v for k,v in today.items() if k!="generated_at"}
 return json.dumps(stable,ensure_ascii=False,sort_keys=True,separators=(",",":"))

def commit(active_artifact:str|None=None,resume:dict[str,Any]|None=None)->dict[str,Any]:
 today=build(active_artifact,resume);body=json.dumps(today,ensure_ascii=False,sort_keys=True,indent=2)+"\n"
 p=_path();p.parent.mkdir(parents=True,exist_ok=True);tmp=p.with_suffix(".tmp")
 tmp.write_text(body,encoding="utf-8");os.replace(tmp,p)
 return {"path":str(p),"projection_sha256":_sha(canonical(today)),"today":today}

def read()->dict[str,Any]:return json.loads(_path().read_text(encoding="utf-8"))
def verify(today:dict[str,Any]|None=None)->dict[str,Any]:
 today=today or read();rebuilt=build(today.get("active_head"),today.get("resume_head"))
 if canonical(today)!=canonical(rebuilt):raise ValueError("today_projection_mismatch")
 for aid,heads in today.get("work_heads",{}).items():
  for key in ("accepted_head","working_head"):
   ref=heads.get(key)
   if ref and _sha(ledger.content(aid,ref["version_id"]))!=ref["sha256"]:raise ValueError("today_artifact_hash_mismatch")
 return {"ok":True,"code":"TWO_DAYS_TODAY_VERIFIED","projection_sha256":_sha(canonical(today))}
