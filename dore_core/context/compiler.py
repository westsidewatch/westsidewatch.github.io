"""Minimal, dependency-free Westside Context compiler and local retriever.

Canonical Markdown remains the source of truth. This module creates a derived,
read-only SQLite projection and never writes back to the architecture document.
"""
from __future__ import annotations

import hashlib
import re
import sqlite3
from dataclasses import dataclass
from pathlib import Path

SCHEMA_VERSION = 1
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
STRUCTURAL_BULLET_RE = re.compile(r"^-\s+(.+?)\s+[—–-]\s+(.+)$")
CJK_RE = re.compile(r"[\u3400-\u9fff]+")
CANONICAL_MARKER = "> Canonical master index for Living Water Westside Watch"


@dataclass(frozen=True)
class ContextNode:
    node_id: str
    title: str
    level: int
    parent_id: str | None
    content: str
    source_path: str
    source_sha256: str
    ordinal: int


@dataclass(frozen=True)
class ContextPacket:
    match: ContextNode
    ancestors: tuple[ContextNode, ...]


def _slug(value: str) -> str:
    value = re.sub(r"[^0-9A-Za-z\u3400-\u9fff]+", "-", value.strip().lower())
    return value.strip("-") or "section"


def compile_markdown(markdown: str, source_path: str = "") -> list[ContextNode]:
    """Compile Markdown plus canonical structural bullets into context nodes.

    The canonical master file expresses Journal columns as top-level bullets rather
    than Markdown headings. In canonical mode those bullets become derived child
    nodes so Doré can retrieve a column such as Emmaus without changing the source
    document. Indented bullets remain evidence inside their parent column; they do
    not become competing structural nodes.
    """
    source_sha = hashlib.sha256(markdown.encode("utf-8")).hexdigest()
    lines = markdown.splitlines()
    canonical_mode = CANONICAL_MARKER in markdown
    headings: list[tuple[int, int, str]] = []
    for line_no, line in enumerate(lines):
        match = HEADING_RE.match(line)
        if match:
            title = match.group(2)
            if canonical_mode and len(match.group(1)) == 1 and title == "MASTER SITE ARCHITECTURE":
                title = "Living Water Westside Watch"
            headings.append((line_no, len(match.group(1)), title))

    nodes: list[ContextNode] = []
    stack: list[tuple[int, str]] = []
    heading_nodes: list[tuple[int, int, ContextNode]] = []
    ordinal = 0
    for idx, (start, level, title) in enumerate(headings):
        end = headings[idx + 1][0] if idx + 1 < len(headings) else len(lines)
        while stack and stack[-1][0] >= level:
            stack.pop()
        parent_id = stack[-1][1] if stack else None
        ordinal += 1
        node_id = f"{_slug(title)}-{ordinal:04d}"
        content = "\n".join(lines[start:end]).strip()
        node = ContextNode(node_id, title, level, parent_id, content, source_path, source_sha, ordinal - 1)
        nodes.append(node)
        heading_nodes.append((start, end, node))
        stack.append((level, node_id))

    if canonical_mode:
        # Promote only unindented descriptive bullets (`- Name — description`).
        # Their indented children stay within the bullet's evidence block.
        promoted: list[ContextNode] = []
        for start, end, parent in heading_nodes:
            bullet_starts: list[tuple[int, re.Match[str]]] = []
            for line_no in range(start + 1, end):
                match = STRUCTURAL_BULLET_RE.match(lines[line_no])
                if match:
                    bullet_starts.append((line_no, match))
            for bidx, (line_no, match) in enumerate(bullet_starts):
                block_end = bullet_starts[bidx + 1][0] if bidx + 1 < len(bullet_starts) else end
                title = match.group(1).strip().strip("*`")
                ordinal += 1
                node_id = f"{_slug(title)}-{ordinal:04d}"
                content = "\n".join(lines[line_no:block_end]).strip()
                promoted.append(ContextNode(node_id, title, min(parent.level + 1, 6), parent.node_id, content, source_path, source_sha, ordinal - 1))
        nodes.extend(promoted)

    nodes.sort(key=lambda n: n.ordinal)
    return nodes


def initialize(db: sqlite3.Connection) -> None:
    db.executescript(
        """
        PRAGMA foreign_keys = ON;
        CREATE TABLE IF NOT EXISTS context_meta (key TEXT PRIMARY KEY,value TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS context_nodes (
            node_id TEXT PRIMARY KEY,title TEXT NOT NULL,level INTEGER NOT NULL,parent_id TEXT,
            content TEXT NOT NULL,source_path TEXT NOT NULL,source_sha256 TEXT NOT NULL,ordinal INTEGER NOT NULL
        );
        CREATE VIRTUAL TABLE IF NOT EXISTS context_fts USING fts5(node_id UNINDEXED,title,content,tokenize = 'unicode61');
        """
    )


def build_index(markdown: str, db: sqlite3.Connection, source_path: str = "") -> str:
    nodes = compile_markdown(markdown, source_path)
    source_sha = hashlib.sha256(markdown.encode("utf-8")).hexdigest()
    with db:
        initialize(db); db.execute("DELETE FROM context_fts"); db.execute("DELETE FROM context_nodes")
        db.executemany("INSERT INTO context_nodes(node_id,title,level,parent_id,content,source_path,source_sha256,ordinal) VALUES (?,?,?,?,?,?,?,?)",[(n.node_id,n.title,n.level,n.parent_id,n.content,n.source_path,n.source_sha256,n.ordinal) for n in nodes])
        db.executemany("INSERT INTO context_fts(node_id,title,content) VALUES (?,?,?)",[(n.node_id,n.title,n.content) for n in nodes])
        db.execute("INSERT OR REPLACE INTO context_meta(key,value) VALUES('schema_version',?)",(str(SCHEMA_VERSION),))
        db.execute("INSERT OR REPLACE INTO context_meta(key,value) VALUES('source_sha256',?)",(source_sha,))
        db.execute("INSERT OR REPLACE INTO context_meta(key,value) VALUES('source_path',?)",(source_path,))
    return source_sha


def _node(db: sqlite3.Connection, node_id: str) -> ContextNode:
    row=db.execute("SELECT node_id,title,level,parent_id,content,source_path,source_sha256,ordinal FROM context_nodes WHERE node_id = ?",(node_id,)).fetchone()
    if row is None: raise KeyError(f"unknown context node: {node_id}")
    return ContextNode(*row)


def ancestor_chain(db: sqlite3.Connection, node: ContextNode) -> tuple[ContextNode,...]:
    chain=[]; parent_id=node.parent_id
    while parent_id is not None:
        parent=_node(db,parent_id); chain.append(parent); parent_id=parent.parent_id
    chain.reverse(); return tuple(chain)


def _rows_to_nodes(rows:list[tuple])->list[ContextNode]: return [ContextNode(*row) for row in rows]


def _fallback_terms(query:str)->list[str]:
    terms=[]
    for token in re.split(r"\s+",query.strip()):
        if not token: continue
        terms.append(token)
        for run in CJK_RE.findall(token):
            if len(run)>=2:
                terms.extend(run[i:i+2] for i in range(len(run)-1));terms.extend(run[i:i+3] for i in range(len(run)-2))
                if len(run)>=4: terms.append(run[:4])
    return list(dict.fromkeys(terms))


def search(db:sqlite3.Connection,query:str,limit:int=8)->list[ContextNode]:
    if not query.strip() or limit<1:return []
    try:
        rows=db.execute("SELECT n.node_id,n.title,n.level,n.parent_id,n.content,n.source_path,n.source_sha256,n.ordinal FROM context_fts f JOIN context_nodes n ON n.node_id=f.node_id WHERE context_fts MATCH ? ORDER BY bm25(context_fts) LIMIT ?",(query,limit)).fetchall()
    except sqlite3.OperationalError: rows=[]
    if rows:return _rows_to_nodes(rows)
    terms=_fallback_terms(query)
    if not terms:return []
    candidates:dict[str,tuple[int,int,ContextNode]]={}
    for term in terms:
        like=f"%{term}%"
        rows=db.execute("SELECT node_id,title,level,parent_id,content,source_path,source_sha256,ordinal FROM context_nodes WHERE title LIKE ? OR content LIKE ?",(like,like)).fetchall()
        for row in rows:
            node=ContextNode(*row);title_match=int(term.casefold() in node.title.casefold());matched,title_score,_=candidates.get(node.node_id,(0,0,node));candidates[node.node_id]=(matched+1,title_score+title_match,node)
    ranked=sorted(candidates.values(),key=lambda item:(-item[0],-item[1],-item[2].level,item[2].ordinal))
    return [item[2] for item in ranked[:limit]]


def search_context(db:sqlite3.Connection,query:str,limit:int=8)->list[ContextPacket]:
    return [ContextPacket(match=node,ancestors=ancestor_chain(db,node)) for node in search(db,query,limit)]


def build_index_from_file(source:Path,database:Path)->str:
    markdown=source.read_text(encoding="utf-8")
    with sqlite3.connect(database) as db:return build_index(markdown,db,str(source))
