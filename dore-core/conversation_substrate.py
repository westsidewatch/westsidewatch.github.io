"""Doré conversation-memory adapter for the shared Core substrate.

Conversation tables remain domain state. Durable cross-product recall is projected
into SharedArtifactStore. Archive JSON is export/evidence only, never a truth store.
"""
from __future__ import annotations
from pathlib import Path
from typing import Iterable
import importlib.util, sqlite3

_CORE=Path(__file__).resolve().parent
_spec=importlib.util.spec_from_file_location("dore_substrate",_CORE/"substrate.py")
_mod=importlib.util.module_from_spec(_spec); assert _spec and _spec.loader; _spec.loader.exec_module(_mod)
SharedArtifactStore=_mod.SharedArtifactStore
ProvenanceEdge=_mod.ProvenanceEdge

class ConversationSubstrate:
    def __init__(self, db_path: str|Path):
        self.db_path=Path(db_path); self.store=SharedArtifactStore(self.db_path)

    @staticmethod
    def artifact_id(message_id:str)->str:return f"message:{message_id}"

    def project_message(self, *, message_id:str, conversation_id:str, project_id:str, role:str, content:str, created_at:str=""):
        aid=self.artifact_id(message_id)
        meta={"message_id":message_id,"conversation_id":conversation_id,"project_id":project_id,"role":role,"created_at":created_at,"projection":"conversation-message"}
        try:return self.store.get_artifact(aid)
        except KeyError:
            return self.store.create_artifact(kind="conversation-message",artifact_id=aid,body=content,metadata=meta,authority="USER" if role=="user" else "DORE",protected=True,provenance=[ProvenanceEdge(relation="projected-from",source_id=message_id,target_id=aid,activity="conversation-projection",agent="dore-core",evidence_ref=f"dore_messages:{message_id}")])

    def backfill(self)->dict:
        """Idempotently project existing dore_messages into shared retrieval."""
        with sqlite3.connect(self.db_path) as c:
            c.row_factory=sqlite3.Row
            rows=c.execute("SELECT id,conversation_id,project_id,role,content,created_at FROM dore_messages ORDER BY created_at").fetchall()
        created=0; existing=0
        for r in rows:
            aid=self.artifact_id(r["id"])
            try:self.store.get_artifact(aid);existing+=1;continue
            except KeyError:pass
            self.project_message(message_id=r["id"],conversation_id=r["conversation_id"],project_id=r["project_id"],role=r["role"],content=r["content"],created_at=r["created_at"]);created+=1
        return {"rows":len(rows),"created":created,"existing":existing}

    def recall(self, query:str, limit:int=18):
        return self.store.search(query,kind="conversation-message",limit=limit)
