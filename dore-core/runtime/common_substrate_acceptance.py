#!/usr/bin/env python3
"""Executable acceptance for the Doré common substrate.

PASS proves: one SQLite truth, WAL, protected revision gate, immutable history,
provenance, typed links and rebuildable retrieval projection.
"""
from __future__ import annotations

from pathlib import Path
import importlib.util
import json
import sqlite3
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("dore_substrate", ROOT / "substrate.py")
assert SPEC and SPEC.loader
mod = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = mod
SPEC.loader.exec_module(mod)

SharedArtifactStore = mod.SharedArtifactStore
ProvenanceEdge = mod.ProvenanceEdge
ArtifactLink = mod.ArtifactLink


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="dore-substrate-") as td:
        db_path = Path(td) / "dore.sqlite3"
        store = SharedArtifactStore(db_path)

        source = store.create_artifact(
            kind="library-source",
            artifact_id="source-calvin-inst-1",
            body="Institutes source record",
            metadata={"title": "Institutes", "locator": "I.1"},
            authority="SOURCE",
            protected=True,
        )
        note = store.create_artifact(
            kind="study-note",
            artifact_id="note-matthew-6-33",
            body="先求他的國和他的義。",
            metadata={"canon_id": "40:6:33", "book": "Matthew", "topics": ["kingdom", "trust"]},
            authority="USER",
            protected=True,
            provenance=[
                ProvenanceEdge(
                    relation="attached-source",
                    source_id=source.id,
                    target_id="note-matthew-6-33",
                    activity="study-note-create",
                    agent="user",
                    evidence_ref="source-calvin-inst-1#I.1",
                )
            ],
        )
        store.add_link(ArtifactLink(note.id, source.id, "cites"))

        updated = store.update_artifact(
            note.id,
            body="先求他的國和他的義；不要為明天憂慮。",
            metadata=note.metadata,
            expected_revision=1,
            authority="USER",
        )

        stale_blocked = False
        try:
            store.update_artifact(note.id, body="stale overwrite", expected_revision=1)
        except ValueError as e:
            stale_blocked = str(e) == "stale_revision"

        history = store.history(note.id)
        provenance = store.provenance_for(note.id)
        links = store.links_for(note.id)
        hits = store.search("不要為明天憂慮", kind="study-note")
        rebuilt = store.rebuild_search_projection()
        hits_after_rebuild = store.search("不要為明天憂慮", kind="study-note")

        with sqlite3.connect(db_path) as c:
            journal = c.execute("PRAGMA journal_mode").fetchone()[0].lower()

        checks = {
            "single_sqlite_truth": db_path.exists(),
            "wal": journal == "wal",
            "protected_default": note.protected is True and note.authority == "USER",
            "revision_advanced": updated.revision == 2,
            "stale_revision_blocked": stale_blocked,
            "immutable_history": [x["revision"] for x in history] == [1, 2],
            "provenance_preserved": any(x["relation"] == "attached-source" for x in provenance),
            "typed_link_preserved": any(x["relation"] == "cites" for x in links),
            "retrieval_works": bool(hits) and hits[0]["artifact_id"] == note.id,
            "projection_rebuild_safe": (rebuilt >= 0) and bool(hits_after_rebuild),
        }
        ok = all(checks.values())
        print(json.dumps({
            "ok": ok,
            "schema": "dore.common-substrate-acceptance.v1",
            "checks": checks,
            "fts5_available": store.fts5_available,
            "search_engine": hits_after_rebuild[0]["engine"] if hits_after_rebuild else None,
        }, ensure_ascii=False, indent=2))
        return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
