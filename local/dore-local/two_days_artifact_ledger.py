#!/usr/bin/env python3
"""Two Days Phase 2 deterministic artifact/event ledger.

AI may propose operations; only this mutation layer moves artifact heads.
Latest is not accepted: ACCEPTED_HEAD and WORKING_HEAD are independent.
"""
from __future__ import annotations
import hashlib,json,os,sqlite3
from datetime import datetime,timezone
from pathlib import Path
from typing import Any

SCHEMA="two-days.artifact-ledger.v0"
VALID={"TEXT_PROPOSED","TEXT_ACCEPTED","TEXT_REJECTED","TEXT_REPLACED","TEXT_REVERTED","TEXT_LOCKED"}

def _home()->Path:
 base=Path(os.environ.get("DORE_LOCAL_HOME") or "~/Library/Application Support/Dore").expanduser()
 return Path(os.environ.get("DORE_TWO_DAYS_HOME") or (base/"two-days")).expanduser()
def _db_path()->Path:return _home()/"state"/"artifact-ledger.db"
def _now()->str:return datetime.now(timezone.utc).isoformat()
def _hash(text:str)->str:return hashlib.sha256(text.encode("utf-8")).hexdigest()
def _connect():
 p=_db_path();p.parent.mkdir(parents=True,exist_ok=True);db=sqlite3.connect(p);db.execute("PRAGMA journal_mode=WAL");db.execute("PRAGMA synchronous=FULL")
 db.executescript("""
 CREATE TABLE IF NOT EXISTS versions(artifact_id TEXT NOT NULL,version_id TEXT NOT NULL,content TEXT NOT NULL,content_sha256 TEXT NOT NULL,created_at TEXT NOT NULL,PRIMARY KEY(artifact_id,version_id));
 CREATE TABLE IF NOT EXISTS events(event_id TEXT PRIMARY KEY,artifact_id TEXT NOT NULL,event_type TEXT NOT NULL,from_version TEXT,to_version TEXT,metadata_json TEXT NOT NULL,created_at TEXT NOT NULL,schema_id TEXT NOT NULL);
 CREATE TABLE IF NOT EXISTS heads(artifact_id TEXT PRIMARY KEY,accepted_head TEXT,working_head TEXT,updated_at TEXT NOT NULL);
 CREATE TABLE IF NOT EXISTS locks(artifact_id TEXT NOT NULL,lock_id TEXT NOT NULL,content_sha256 TEXT NOT NULL,metadata_json TEXT NOT NULL,PRIMARY KEY(artifact_id,lock_id));
 """);return db

def put_version(artifact_id:str,version_id:str,content:str)->dict[str,Any]:
 if not artifact_id or not version_id:raise ValueError("artifact_and_version_required")
 digest=_hash(content)
 with _connect() as db:
  row=db.execute("SELECT content_sha256 FROM versions WHERE artifact_id=? AND version_id=?",(artifact_id,version_id)).fetchone()
  if row:
   if row[0]!=digest:raise ValueError("version_identity_conflict")
  else:db.execute("INSERT INTO versions VALUES(?,?,?,?,?)",(artifact_id,version_id,content,digest,_now()))
 return {"artifact_id":artifact_id,"version_id":version_id,"sha256":digest}

def _exists(db,artifact_id,version_id):
 return version_id is None or db.execute("SELECT 1 FROM versions WHERE artifact_id=? AND version_id=?",(artifact_id,version_id)).fetchone() is not None

def apply(event_id:str,artifact_id:str,event_type:str,to_version:str|None=None,from_version:str|None=None,metadata:dict[str,Any]|None=None)->dict[str,Any]:
 if event_type not in VALID:raise ValueError("unsupported_artifact_event")
 metadata=metadata or {}
 with _connect() as db:
  prior=db.execute("SELECT artifact_id,event_type,from_version,to_version,metadata_json FROM events WHERE event_id=?",(event_id,)).fetchone()
  encoded=json.dumps(metadata,ensure_ascii=False,sort_keys=True,separators=(",",":"))
  if prior:
   if prior!=(artifact_id,event_type,from_version,to_version,encoded):raise ValueError("artifact_event_identity_conflict")
   return state(artifact_id,db)
  if not _exists(db,artifact_id,to_version) or not _exists(db,artifact_id,from_version):raise ValueError("unknown_artifact_version")
  row=db.execute("SELECT accepted_head,working_head FROM heads WHERE artifact_id=?",(artifact_id,)).fetchone();accepted,working=row if row else (None,None)
  if event_type in {"TEXT_PROPOSED","TEXT_REPLACED","TEXT_REVERTED"}:
   if not to_version:raise ValueError("to_version_required")
   working=to_version
  elif event_type=="TEXT_ACCEPTED":
   target=to_version or working
   if not target:raise ValueError("accepted_version_required")
   accepted=target;working=target
  elif event_type=="TEXT_REJECTED":
   if accepted is None:working=None
   else:working=accepted
  elif event_type=="TEXT_LOCKED":
   target=to_version or accepted or working
   if not target:raise ValueError("lock_version_required")
   content=db.execute("SELECT content FROM versions WHERE artifact_id=? AND version_id=?",(artifact_id,target)).fetchone()[0]
   lock_id=str(metadata.get("lock_id") or _hash(target+"\0"+content))
   db.execute("INSERT OR REPLACE INTO locks VALUES(?,?,?,?)",(artifact_id,lock_id,_hash(content),encoded))
  db.execute("INSERT INTO events VALUES(?,?,?,?,?,?,?)",(event_id,artifact_id,event_type,from_version,to_version,encoded,_now(),SCHEMA))
  db.execute("INSERT INTO heads VALUES(?,?,?,?) ON CONFLICT(artifact_id) DO UPDATE SET accepted_head=excluded.accepted_head,working_head=excluded.working_head,updated_at=excluded.updated_at",(artifact_id,accepted,working,_now()))
  return {"artifact_id":artifact_id,"accepted_head":accepted,"working_head":working}

def state(artifact_id:str,db=None)->dict[str,Any]:
 own=db is None;db=db or _connect()
 try:
  row=db.execute("SELECT accepted_head,working_head,updated_at FROM heads WHERE artifact_id=?",(artifact_id,)).fetchone()
  return {"artifact_id":artifact_id,"accepted_head":row[0] if row else None,"working_head":row[1] if row else None,"updated_at":row[2] if row else None}
 finally:
  if own:db.close()

def content(artifact_id:str,version_id:str)->str:
 with _connect() as db:
  row=db.execute("SELECT content,content_sha256 FROM versions WHERE artifact_id=? AND version_id=?",(artifact_id,version_id)).fetchone()
 if not row:raise KeyError(version_id)
 if _hash(row[0])!=row[1]:raise ValueError("artifact_hash_mismatch")
 return row[0]
