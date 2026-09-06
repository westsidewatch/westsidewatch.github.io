"""Doré shared Scripture workspace: ONE + Multiwrite + Search + 黎明書局.
Stdlib-only canonical artifact skeleton. Product surfaces are adapters, not owners.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import Any
import json, re, time, uuid

SCHEMA_ANCHOR = "dore.scripture-anchor.v1"
SCHEMA_NOTE = "dore.study-note.v1"
SCHEMA_SOURCE = "dore.library-source-ref.v1"

@dataclass(frozen=True)
class ScriptureAnchor:
    canon_id: str                 # ONE Canon Index identity, e.g. 40:6
    book: str = ""
    chapter: int | None = None
    verse_start: int | None = None
    verse_end: int | None = None
    labels: tuple[str, ...] = ()
    schema: str = SCHEMA_ANCHOR

@dataclass(frozen=True)
class LibrarySourceRef:
    """Reference into 黎明書局; source stays independent from user interpretation."""
    source_id: str
    locator: str = ""             # page/chapter/section/fragment
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
    """Single local artifact store. ONE/Multiwrite/Search/黎明書局 share IDs."""
    def __init__(self, root: str | Path):
        self.root = Path(root)
        self.notes_dir = self.root / "notes"
        self.notes_dir.mkdir(parents=True, exist_ok=True)

    def create_note(self, text: str, anchors=None, source_refs=None, entities=None, topics=None) -> StudyNote:
        note = StudyNote(
            id="note-" + uuid.uuid4().hex,
            text=text,
            anchors=list(anchors or []), source_refs=list(source_refs or []),
            entities=list(entities or []), topics=list(topics or []),
        )
        self._save(note)
        return note

    def get_note(self, note_id: str) -> StudyNote:
        p = self.notes_dir / f"{note_id}.json"
        return self._decode(json.loads(p.read_text(encoding="utf-8")))

    def update_note(self, note_id: str, *, text: str, expected_revision: int) -> StudyNote:
        note = self.get_note(note_id)
        if note.revision != expected_revision:
            raise ValueError("stale_revision")
        note.text = text
        note.revision += 1
        note.updated_at = time.time()
        self._save(note)
        return note

    def list_notes(self) -> list[StudyNote]:
        return [self._decode(json.loads(p.read_text(encoding="utf-8"))) for p in sorted(self.notes_dir.glob("note-*.json"))]

    def fuzzy(self, query: str, limit: int = 20) -> list[dict[str, Any]]:
        """Cheap L0 fuzzy retrieval. No embedding/runtime dependency.
        Ranking: scripture identity > lexical coverage > entities/topics > library source metadata.
        """
        q = self._tokens(query)
        if not q: return []
        hits=[]
        for n in self.list_notes():
            anchor_text=" ".join(a.canon_id+" "+a.book+" "+" ".join(a.labels) for a in n.anchors)
            entity_text=" ".join(n.entities+n.topics)
            source_text=" ".join(s.source_id+" "+s.title+" "+s.author+" "+s.locator for s in n.source_refs)
            body=self._tokens(n.text); anchors=self._tokens(anchor_text); entities=self._tokens(entity_text); sources=self._tokens(source_text)
            exact_anchor = any(a.canon_id.lower() in query.lower() for a in n.anchors)
            coverage=lambda bag: len(q & bag)/max(1,len(q))
            score=(4.0 if exact_anchor else 0.0)+2.0*coverage(body)+1.6*coverage(anchors)+1.3*coverage(entities)+0.8*coverage(sources)
            if score>0: hits.append({"note_id":n.id,"score":round(score,4),"revision":n.revision,"anchors":[a.canon_id for a in n.anchors],"source_refs":[s.source_id for s in n.source_refs]})
        return sorted(hits,key=lambda x:(-x["score"],x["note_id"]))[:limit]

    @staticmethod
    def _tokens(text: str) -> set[str]:
        text=text.lower().strip()
        words=set(re.findall(r"[a-z0-9:_-]+|[\u3400-\u9fff]",text))
        han="".join(re.findall(r"[\u3400-\u9fff]",text))
        words.update(han[i:i+n] for n in (2,3) for i in range(max(0,len(han)-n+1)))
        return {x for x in words if x}

    def _save(self,note:StudyNote):
        p=self.notes_dir/f"{note.id}.json"; tmp=p.with_suffix(".tmp")
        tmp.write_text(json.dumps(note.to_dict(),ensure_ascii=False,indent=2),encoding="utf-8")
        tmp.replace(p)

    @staticmethod
    def _decode(d:dict[str,Any])->StudyNote:
        d=dict(d); d["anchors"]=[ScriptureAnchor(**x) for x in d.get("anchors",[])]; d["source_refs"]=[LibrarySourceRef(**x) for x in d.get("source_refs",[])]; return StudyNote(**d)
