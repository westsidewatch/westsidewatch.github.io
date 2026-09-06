"""Doré shared Scripture workspace backed by the canonical Core substrate.

ONE, Multiwrite, Search and 黎明書局 share artifact IDs and one SQLite truth.
The old JSON note directory is compatibility input only and can be migrated once;
it is no longer a second writable store.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import Any
import json, re, time, uuid

from substrate import SharedArtifactStore, ArtifactLink, ProvenanceEdge

SCHEMA_ANCHOR = "dore.scripture-anchor.v1"
SCHEMA_NOTE = "dore.study-note.v1"
SCHEMA_SOURCE = "dore.library-source-ref.v1"

@dataclass(frozen=True)
class ScriptureAnchor:
    canon_id: str
    book: str = ""
    chapter: int | None = None
    verse_start: int | None = None
    verse_end: int | None = None
    labels: tuple[str, ...] = ()
    schema: str = SCHEMA_ANCHOR

@dataclass(frozen=True)
class LibrarySourceRef:
    source_id: str
    locator: str = ""
    title: str = ""
    author: str = ""
    claim_class: str = "SOURCE"
    schema: str = SCHEMA_SOURCE

@dataclass
class StudyNote:
    id: str
    text: str
    anchors: list[ScriptureAnchor] = field(default_factory=list)
    source_refs: list[LibrarySourceRef] = field(default_factory=list)
    entities: list[str] = field(default_factory=list)
    topics: list[str] = field(default_factory=list)
    authorship: str = "USER"
    protected: bool = True
    revision: int = 1
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)
    schema: str = SCHEMA_NOTE

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

class ScriptureWorkspace:
    """Compatibility facade over SharedArtifactStore, not a separate datastore."""
    def __init__(self, root: str | Path):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self.store = SharedArtifactStore(self.root / "dore.sqlite3")
        self.legacy_notes_dir = self.root / "notes"
        self._migrate_legacy_json_once()

    def create_note(self, text: str, anchors=None, source_refs=None, entities=None, topics=None) -> StudyNote:
        anchors = list(anchors or [])
        source_refs = list(source_refs or [])
        entities = list(entities or [])
        topics = list(topics or [])
        note_id = "note-" + uuid.uuid4().hex
        metadata = self._metadata(anchors, source_refs, entities, topics)
        provenance = []
        for src in source_refs:
            self._ensure_source_artifact(src)
            provenance.append(ProvenanceEdge(
                relation="attached-source", source_id=src.source_id, target_id=note_id,
                activity="study-note-create", agent="user", evidence_ref=self._source_evidence(src),
            ))
        art = self.store.create_artifact(
            kind="study-note", artifact_id=note_id, body=text, metadata=metadata,
            authority="USER", protected=True, provenance=provenance,
        )
        for src in source_refs:
            self.store.add_link(ArtifactLink(note_id, src.source_id, "cites"))
        return self._from_artifact(art)

    def get_note(self, note_id: str) -> StudyNote:
        art = self.store.get_artifact(note_id)
        if art.kind != "study-note":
            raise KeyError(note_id)
        return self._from_artifact(art)

    def update_note(self, note_id: str, *, text: str, expected_revision: int) -> StudyNote:
        cur = self.store.get_artifact(note_id)
        if cur.kind != "study-note":
            raise KeyError(note_id)
        art = self.store.update_artifact(
            note_id, body=text, metadata=cur.metadata,
            expected_revision=expected_revision, authority="USER",
        )
        return self._from_artifact(art)

    def list_notes(self) -> list[StudyNote]:
        with self.store.connect() as c:
            rows = c.execute("SELECT * FROM dore_artifacts WHERE kind='study-note' ORDER BY updated_at DESC").fetchall()
        return [self._from_artifact(self.store._decode(r)) for r in rows]

    def fuzzy(self, query: str, limit: int = 20) -> list[dict[str, Any]]:
        """Deterministic L0 fuzzy projection over the canonical artifact truth."""
        q = self._tokens(query)
        if not q:
            return []
        hits=[]
        for n in self.list_notes():
            anchor_text=" ".join(a.canon_id+" "+a.book+" "+" ".join(a.labels) for a in n.anchors)
            entity_text=" ".join(n.entities+n.topics)
            source_text=" ".join(s.source_id+" "+s.title+" "+s.author+" "+s.locator for s in n.source_refs)
            body=self._tokens(n.text); anchors=self._tokens(anchor_text); entities=self._tokens(entity_text); sources=self._tokens(source_text)
            exact_anchor = any(a.canon_id.lower() in query.lower() for a in n.anchors)
            coverage=lambda bag: len(q & bag)/max(1,len(q))
            score=(4.0 if exact_anchor else 0.0)+2.0*coverage(body)+1.6*coverage(anchors)+1.3*coverage(entities)+0.8*coverage(sources)
            if score>0:
                hits.append({"note_id":n.id,"artifact_id":n.id,"score":round(score,4),"revision":n.revision,"anchors":[a.canon_id for a in n.anchors],"source_refs":[s.source_id for s in n.source_refs],"engine":"scripture-l0"})
        return sorted(hits,key=lambda x:(-x["score"],x["note_id"]))[:limit]

    def _ensure_source_artifact(self, src: LibrarySourceRef) -> None:
        try:
            self.store.get_artifact(src.source_id)
            return
        except KeyError:
            pass
        self.store.create_artifact(
            kind="library-source", artifact_id=src.source_id,
            body=(src.title or src.source_id),
            metadata={"locator":src.locator,"title":src.title,"author":src.author,"claim_class":src.claim_class,"schema":src.schema},
            authority="SOURCE", protected=True,
        )

    def _migrate_legacy_json_once(self) -> None:
        if not self.legacy_notes_dir.is_dir():
            return
        marker = self.root / ".scripture-json-migrated-v1"
        if marker.exists():
            return
        migrated=0
        for p in sorted(self.legacy_notes_dir.glob("note-*.json")):
            try:
                d=json.loads(p.read_text(encoding="utf-8"))
                note=self._decode_legacy(d)
                try:
                    self.store.get_artifact(note.id)
                    continue
                except KeyError:
                    pass
                meta=self._metadata(note.anchors,note.source_refs,note.entities,note.topics)
                for src in note.source_refs:
                    self._ensure_source_artifact(src)
                art=self.store.create_artifact(kind="study-note",artifact_id=note.id,body=note.text,metadata=meta,authority=note.authorship,protected=note.protected)
                for src in note.source_refs:
                    self.store.add_link(ArtifactLink(art.id,src.source_id,"cites"))
                migrated += 1
            except Exception:
                continue
        marker.write_text(json.dumps({"schema":"dore.scripture-json-migration.v1","migrated":migrated,"legacy":"read-only"}),encoding="utf-8")

    @staticmethod
    def _metadata(anchors, source_refs, entities, topics):
        return {
            "schema":SCHEMA_NOTE,
            "anchors":[asdict(x) for x in anchors],
            "source_refs":[asdict(x) for x in source_refs],
            "entities":list(entities),
            "topics":list(topics),
        }

    @staticmethod
    def _source_evidence(src: LibrarySourceRef) -> str:
        return src.source_id + ("#"+src.locator if src.locator else "")

    @staticmethod
    def _tokens(text: str) -> set[str]:
        text=text.lower().strip()
        words=set(re.findall(r"[a-z0-9:_-]+|[\u3400-\u9fff]",text))
        han="".join(re.findall(r"[\u3400-\u9fff]",text))
        words.update(han[i:i+n] for n in (2,3) for i in range(max(0,len(han)-n+1)))
        return {x for x in words if x}

    @staticmethod
    def _decode_legacy(d:dict[str,Any])->StudyNote:
        d=dict(d)
        d["anchors"]=[ScriptureAnchor(**x) for x in d.get("anchors",[])]
        d["source_refs"]=[LibrarySourceRef(**x) for x in d.get("source_refs",[])]
        return StudyNote(**d)

    @staticmethod
    def _from_artifact(art) -> StudyNote:
        m=art.metadata
        return StudyNote(
            id=art.id,text=art.body,
            anchors=[ScriptureAnchor(**x) for x in m.get("anchors",[])],
            source_refs=[LibrarySourceRef(**x) for x in m.get("source_refs",[])],
            entities=list(m.get("entities",[])),topics=list(m.get("topics",[])),
            authorship=art.authority,protected=art.protected,revision=art.revision,
            created_at=art.created_at,updated_at=art.updated_at,
        )
