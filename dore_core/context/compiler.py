"""Minimal, dependency-free Westside Context compiler and local retriever.

Design rule: canonical Markdown remains the source of truth. This module creates a
small derived SQLite projection; it never writes back to the canonical architecture.
"""
from __future__ import annotations

import hashlib
import re
import sqlite3
from dataclasses import dataclass
from pathlib import Path

SCHEMA_VERSION = 1
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")


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
    """A matched node plus its canonical ancestor chain."""

    match: ContextNode
    ancestors: tuple[ContextNode, ...]


def _slug(value: str) -> str:
    value = re.sub(r"[^0-9A-Za-z\u3400-\u9fff]+", "-", value.strip().lower())
    return value.strip("-") or "section"


def compile_markdown(markdown: str, source_path: str = "") -> list[ContextNode]:
    """Compile Markdown headings into a compact hierarchical context projection."""
    source_sha = hashlib.sha256(markdown.encode("utf-8")).hexdigest()
    lines = markdown.splitlines()
    headings: list[tuple[int, int, str]] = []
    for line_no, line in enumerate(lines):
        match = HEADING_RE.match(line)
        if match:
            headings.append((line_no, len(match.group(1)), match.group(2)))

    nodes: list[ContextNode] = []
    stack: list[tuple[int, str]] = []
    for ordinal, (start, level, title) in enumerate(headings):
        end = headings[ordinal + 1][0] if ordinal + 1 < len(headings) else len(lines)
        while stack and stack[-1][0] >= level:
            stack.pop()
        parent_id = stack[-1][1] if stack else None
        node_id = f"{_slug(title)}-{ordinal + 1:04d}"
        content = "\n".join(lines[start:end]).strip()
        nodes.append(ContextNode(node_id, title, level, parent_id, content, source_path, source_sha, ordinal))
        stack.append((level, node_id))
    return nodes


def initialize(db: sqlite3.Connection) -> None:
    """Create the smallest useful local context store using SQLite + FTS5."""
    db.executescript(
        """
        PRAGMA foreign_keys = ON;
        CREATE TABLE IF NOT EXISTS context_meta (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS context_nodes (
            node_id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            level INTEGER NOT NULL,
            parent_id TEXT,
            content TEXT NOT NULL,
            source_path TEXT NOT NULL,
            source_sha256 TEXT NOT NULL,
            ordinal INTEGER NOT NULL
        );
        CREATE VIRTUAL TABLE IF NOT EXISTS context_fts USING fts5(
            node_id UNINDEXED,
            title,
            content,
            tokenize = 'unicode61'
        );
        """
    )


def build_index(markdown: str, db: sqlite3.Connection, source_path: str = "") -> str:
    """Replace the derived projection atomically and return the source SHA-256."""
    nodes = compile_markdown(markdown, source_path)
    source_sha = hashlib.sha256(markdown.encode("utf-8")).hexdigest()
    with db:
        initialize(db)
        db.execute("DELETE FROM context_fts")
        db.execute("DELETE FROM context_nodes")
        db.executemany(
            """INSERT INTO context_nodes
               (node_id,title,level,parent_id,content,source_path,source_sha256,ordinal)
               VALUES (?,?,?,?,?,?,?,?)""",
            [(n.node_id, n.title, n.level, n.parent_id, n.content, n.source_path, n.source_sha256, n.ordinal) for n in nodes],
        )
        db.executemany(
            "INSERT INTO context_fts(node_id,title,content) VALUES (?,?,?)",
            [(n.node_id, n.title, n.content) for n in nodes],
        )
        db.execute("INSERT OR REPLACE INTO context_meta(key,value) VALUES('schema_version',?)", (str(SCHEMA_VERSION),))
        db.execute("INSERT OR REPLACE INTO context_meta(key,value) VALUES('source_sha256',?)", (source_sha,))
        db.execute("INSERT OR REPLACE INTO context_meta(key,value) VALUES('source_path',?)", (source_path,))
    return source_sha


def _node(db: sqlite3.Connection, node_id: str) -> ContextNode:
    row = db.execute(
        """SELECT node_id,title,level,parent_id,content,source_path,source_sha256,ordinal
           FROM context_nodes WHERE node_id = ?""",
        (node_id,),
    ).fetchone()
    if row is None:
        raise KeyError(f"unknown context node: {node_id}")
    return ContextNode(*row)


def ancestor_chain(db: sqlite3.Connection, node: ContextNode) -> tuple[ContextNode, ...]:
    """Return canonical ancestors from root toward the matched node's parent."""
    chain: list[ContextNode] = []
    parent_id = node.parent_id
    while parent_id is not None:
        parent = _node(db, parent_id)
        chain.append(parent)
        parent_id = parent.parent_id
    chain.reverse()
    return tuple(chain)


def _rows_to_nodes(rows: list[tuple]) -> list[ContextNode]:
    return [ContextNode(*row) for row in rows]


def search(db: sqlite3.Connection, query: str, limit: int = 8) -> list[ContextNode]:
    """Return relevant context nodes with FTS5 first and substring fallback.

    FTS5 is the primary ranked retriever. The tiny LIKE fallback matters for CJK
    substring queries because unicode61 does not provide a word-segmentation model
    for Chinese. It remains local, deterministic, and dependency-free.
    """
    if not query.strip() or limit < 1:
        return []
    try:
        rows = db.execute(
            """SELECT n.node_id,n.title,n.level,n.parent_id,n.content,n.source_path,n.source_sha256,n.ordinal
               FROM context_fts f JOIN context_nodes n ON n.node_id=f.node_id
               WHERE context_fts MATCH ? ORDER BY bm25(context_fts) LIMIT ?""",
            (query, limit),
        ).fetchall()
    except sqlite3.OperationalError:
        rows = []
    if rows:
        return _rows_to_nodes(rows)

    needle = query.strip()
    like = f"%{needle}%"
    rows = db.execute(
        """SELECT node_id,title,level,parent_id,content,source_path,source_sha256,ordinal
           FROM context_nodes
           WHERE title LIKE ? OR content LIKE ?
           ORDER BY ordinal LIMIT ?""",
        (like, like, limit),
    ).fetchall()
    return _rows_to_nodes(rows)


def search_context(db: sqlite3.Connection, query: str, limit: int = 8) -> list[ContextPacket]:
    """Search and attach each match's canonical ancestor chain.

    This is the minimal bridge from lexical retrieval to usable structural context:
    retrieval stays FTS5-first, while hierarchy is recovered from the same projection.
    """
    return [ContextPacket(match=node, ancestors=ancestor_chain(db, node)) for node in search(db, query, limit)]


def build_index_from_file(source: Path, database: Path) -> str:
    """Compile a canonical Markdown file into a local derived SQLite projection."""
    markdown = source.read_text(encoding="utf-8")
    with sqlite3.connect(database) as db:
        return build_index(markdown, db, str(source))
