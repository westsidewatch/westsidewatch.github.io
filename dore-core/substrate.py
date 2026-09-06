"""Doré Core shared artifact substrate.

Stdlib-only canonical persistence for shared knowledge. Product surfaces are
adapters; indexes are rebuildable projections, never the source of truth.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import Any, Iterable
import hashlib, json, sqlite3, time, uuid

SCHEMA_ARTIFACT="dore.artifact.v1"
SCHEMA_REVISION="dore.artifact-revision.v1"
SCHEMA_PROVENANCE="dore.provenance-edge.v1"
SCHEMA_LINK="dore.artifact-link.v1"

def _now(): return time.time()
def _json(v): return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(",",":"))
def _sha(body,meta): return hashlib.sha256((body+"\n"+_json(meta)).encode()).hexdigest()

@dataclass(frozen=True)
class ProvenanceEdge:
    relation:str; source_id:str; target_id:str; activity:str=""; agent:str=""; evidence_ref:str=""; created_at:float=field(default_factory=_now); schema:str=SCHEMA_PROVENANCE

@dataclass(frozen=True)
class ArtifactLink:
    source_id:str; target_id:str; relation:str; weight:float=1.0; created_at:float=field(default_factory=_now); schema:str=SCHEMA_LINK

@dataclass
class Artifact:
    id:str; kind:str; body:str; metadata:dict[str,Any]=field(default_factory=dict); authority:str="USER"; protected:bool=True; revision:int=1; content_sha256:str=""; created_at:float=field(default_factory=_now); updated_at:float=field(default_factory=_now); schema:str=SCHEMA_ARTIFACT
    def to_dict(self): return asdict(self)

class SharedArtifactStore:
    """One SQLite truth with WAL, revision history, provenance and cheap retrieval."""
    def __init__(self,db_path:str|Path):
        self.db_path=Path(db_path); self.db_path.parent.mkdir(parents=True,exist_ok=True); self._fts5=False; self._ensure_schema()

    def connect(self):
        c=sqlite3.connect(self.db_path,timeout=5.0); c.row_factory=sqlite3.Row
        c.execute("PRAGMA foreign_keys=ON"); c.execute("PRAGMA busy_timeout=5000"); c.execute("PRAGMA journal_mode=WAL")
        return c

    def _ensure_schema(self):
        with self.connect() as c:
            c.executescript("""
            CREATE TABLE IF NOT EXISTS dore_artifacts(
              id TEXT PRIMARY KEY,kind TEXT NOT NULL,body TEXT NOT NULL,metadata_json TEXT NOT NULL DEFAULT '{}',
              authority TEXT NOT NULL DEFAULT 'USER',protected INTEGER NOT NULL DEFAULT 1,revision INTEGER NOT NULL,
              content_sha256 TEXT NOT NULL,created_at REAL NOT NULL,updated_at REAL NOT NULL,schema TEXT NOT NULL);
            CREATE INDEX IF NOT EXISTS idx_dore_artifacts_kind_updated ON dore_artifacts(kind,updated_at DESC);
            CREATE TABLE IF NOT EXISTS dore_artifact_revisions(
              artifact_id TEXT NOT NULL,revision INTEGER NOT NULL,body TEXT NOT NULL,metadata_json TEXT NOT NULL,
              content_sha256 TEXT NOT NULL,authority TEXT NOT NULL,protected INTEGER NOT NULL,created_at REAL NOT NULL,
              schema TEXT NOT NULL,PRIMARY KEY(artifact_id,revision),
              FOREIGN KEY(artifact_id) REFERENCES dore_artifacts(id) ON DELETE CASCADE);
            CREATE TABLE IF NOT EXISTS dore_provenance_edges(
              id INTEGER PRIMARY KEY AUTOINCREMENT,relation TEXT NOT NULL,source_id TEXT NOT NULL,target_id TEXT NOT NULL,
              activity TEXT NOT NULL DEFAULT '',agent TEXT NOT NULL DEFAULT '',evidence_ref TEXT NOT NULL DEFAULT '',created_at REAL NOT NULL,schema TEXT NOT NULL);
            CREATE INDEX IF NOT EXISTS idx_dore_prov_target ON dore_provenance_edges(target_id,relation);
            CREATE INDEX IF NOT EXISTS idx_dore_prov_source ON dore_provenance_edges(source_id,relation);
            CREATE TABLE IF NOT EXISTS dore_artifact_links(
              source_id TEXT NOT NULL,target_id TEXT NOT NULL,relation TEXT NOT NULL,weight REAL NOT NULL DEFAULT 1.0,
              created_at REAL NOT NULL,schema TEXT NOT NULL,PRIMARY KEY(source_id,target_id,relation));
            CREATE INDEX IF NOT EXISTS idx_dore_links_target ON dore_artifact_links(target_id,relation);
            """)
            try:
                # Ordinary FTS5 table is intentionally used instead of a contentless table:
                # updates/deletes stay portable across older macOS SQLite builds. It remains
                # a disposable projection and can always be rebuilt from dore_artifacts.
                c.execute("CREATE VIRTUAL TABLE IF NOT EXISTS dore_artifacts_fts USING fts5(artifact_id UNINDEXED,body,metadata)")
                self._fts5=True
            except sqlite3.OperationalError: self._fts5=False

    @property
    def fts5_available(self): return self._fts5

    def create_artifact(self,*,kind,body,metadata=None,authority="USER",protected=True,artifact_id=None,provenance:Iterable[ProvenanceEdge]=()):
        ts=_now(); aid=artifact_id or "art-"+uuid.uuid4().hex; meta=dict(metadata or {}); digest=_sha(body,meta)
        item=Artifact(aid,kind,body,meta,authority,protected,1,digest,ts,ts)
        with self.connect() as c:
            c.execute("INSERT INTO dore_artifacts VALUES(?,?,?,?,?,?,?,?,?,?,?)",(item.id,item.kind,item.body,_json(item.metadata),item.authority,1 if item.protected else 0,item.revision,item.content_sha256,item.created_at,item.updated_at,item.schema))
            self._insert_revision(c,item); self._index(c,item)
            for edge in provenance:self._insert_provenance(c,edge)
        return item

    def get_artifact(self,artifact_id):
        with self.connect() as c: row=c.execute("SELECT * FROM dore_artifacts WHERE id=?",(artifact_id,)).fetchone()
        if not row: raise KeyError(artifact_id)
        return self._decode(row)

    def update_artifact(self,artifact_id,*,body,metadata=None,expected_revision,authority=None,provenance:Iterable[ProvenanceEdge]=()):
        with self.connect() as c:
            row=c.execute("SELECT * FROM dore_artifacts WHERE id=?",(artifact_id,)).fetchone()
            if not row:raise KeyError(artifact_id)
            cur=self._decode(row)
            if cur.revision!=expected_revision:raise ValueError("stale_revision")
            meta=cur.metadata if metadata is None else dict(metadata); auth=authority or cur.authority; ts=_now(); digest=_sha(body,meta)
            nxt=Artifact(cur.id,cur.kind,body,meta,auth,cur.protected,cur.revision+1,digest,cur.created_at,ts)
            c.execute("UPDATE dore_artifacts SET body=?,metadata_json=?,authority=?,revision=?,content_sha256=?,updated_at=? WHERE id=?",(body,_json(meta),auth,nxt.revision,digest,ts,artifact_id))
            self._insert_revision(c,nxt); self._index(c,nxt)
            for edge in provenance:self._insert_provenance(c,edge)
            return nxt

    def add_link(self,link:ArtifactLink):
        with self.connect() as c:c.execute("INSERT INTO dore_artifact_links(source_id,target_id,relation,weight,created_at,schema) VALUES(?,?,?,?,?,?) ON CONFLICT(source_id,target_id,relation) DO UPDATE SET weight=excluded.weight",(link.source_id,link.target_id,link.relation,link.weight,link.created_at,link.schema))

    def add_provenance(self,edge:ProvenanceEdge):
        with self.connect() as c:self._insert_provenance(c,edge)

    def search(self,query,*,kind=None,limit=20):
        query=str(query).strip()
        if not query:return []
        with self.connect() as c:
            if self._fts5:
                try:
                    sql="SELECT a.*,bm25(dore_artifacts_fts) rank FROM dore_artifacts_fts f JOIN dore_artifacts a ON a.id=f.artifact_id WHERE dore_artifacts_fts MATCH ?"; args=[query]
                    if kind:sql+=" AND a.kind=?";args.append(kind)
                    sql+=" ORDER BY rank LIMIT ?";args.append(limit); rows=c.execute(sql,args).fetchall()
                    if rows:return [self._hit(r,"fts5",-float(r["rank"])) for r in rows]
                except sqlite3.OperationalError:pass
            like="%"+query.replace("%","\\%").replace("_","\\_")+"%"; sql="SELECT * FROM dore_artifacts WHERE (body LIKE ? ESCAPE '\\' OR metadata_json LIKE ? ESCAPE '\\')"; args=[like,like]
            if kind:sql+=" AND kind=?";args.append(kind)
            sql+=" ORDER BY updated_at DESC LIMIT ?";args.append(limit)
            return [self._hit(r,"deterministic-like",1.0) for r in c.execute(sql,args)]

    def history(self,artifact_id):
        with self.connect() as c:rows=c.execute("SELECT * FROM dore_artifact_revisions WHERE artifact_id=? ORDER BY revision",(artifact_id,)).fetchall()
        return [dict(r)|{"metadata":json.loads(r["metadata_json"])} for r in rows]

    def provenance_for(self,artifact_id):
        with self.connect() as c:rows=c.execute("SELECT * FROM dore_provenance_edges WHERE source_id=? OR target_id=? ORDER BY created_at",(artifact_id,artifact_id)).fetchall()
        return [dict(r) for r in rows]

    def links_for(self,artifact_id):
        with self.connect() as c:rows=c.execute("SELECT * FROM dore_artifact_links WHERE source_id=? OR target_id=? ORDER BY relation,target_id",(artifact_id,artifact_id)).fetchall()
        return [dict(r) for r in rows]

    def rebuild_search_projection(self):
        if not self._fts5:return 0
        with self.connect() as c:
            c.execute("DELETE FROM dore_artifacts_fts"); rows=c.execute("SELECT * FROM dore_artifacts").fetchall()
            for r in rows:self._index(c,self._decode(r),delete_first=False)
        return len(rows)

    def _insert_revision(self,c,item):
        c.execute("INSERT INTO dore_artifact_revisions VALUES(?,?,?,?,?,?,?,?,?)",(item.id,item.revision,item.body,_json(item.metadata),item.content_sha256,item.authority,1 if item.protected else 0,item.updated_at,SCHEMA_REVISION))

    def _index(self,c,item,delete_first=True):
        if not self._fts5:return
        if delete_first:c.execute("DELETE FROM dore_artifacts_fts WHERE artifact_id=?",(item.id,))
        c.execute("INSERT INTO dore_artifacts_fts(artifact_id,body,metadata) VALUES(?,?,?)",(item.id,item.body,_json(item.metadata)))

    @staticmethod
    def _insert_provenance(c,edge):c.execute("INSERT INTO dore_provenance_edges(relation,source_id,target_id,activity,agent,evidence_ref,created_at,schema) VALUES(?,?,?,?,?,?,?,?)",(edge.relation,edge.source_id,edge.target_id,edge.activity,edge.agent,edge.evidence_ref,edge.created_at,edge.schema))
    @staticmethod
    def _decode(r):return Artifact(r["id"],r["kind"],r["body"],json.loads(r["metadata_json"]),r["authority"],bool(r["protected"]),r["revision"],r["content_sha256"],r["created_at"],r["updated_at"],r["schema"])
    @staticmethod
    def _hit(r,engine,score):return {"artifact_id":r["id"],"kind":r["kind"],"revision":r["revision"],"authority":r["authority"],"protected":bool(r["protected"]),"score":round(score,6),"engine":engine}
