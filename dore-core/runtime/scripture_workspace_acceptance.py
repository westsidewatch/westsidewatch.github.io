#!/usr/bin/env python3
"""Executable acceptance: ScriptureWorkspace is a facade over the common substrate."""
from __future__ import annotations
import json, sys, tempfile
from pathlib import Path

CORE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CORE))
from scripture_workspace import ScriptureAnchor, LibrarySourceRef, ScriptureWorkspace


def run() -> dict:
    with tempfile.TemporaryDirectory(prefix="dore-scripture-workspace-") as td:
        root=Path(td)
        ws = ScriptureWorkspace(root)
        anchor = ScriptureAnchor(canon_id="40:6", book="馬太福音", chapter=6, labels=("主禱文", "父", "憂慮"))
        source = LibrarySourceRef(source_id="dawn:test:fatherhood", locator="chapter-1", title="父與兒子的語言", author="Test Source")
        note = ws.create_note(
            "第六章像父對兒子說話；先求神的國和義，與一天的憂慮一天當就夠了放在一起。",
            anchors=[anchor], source_refs=[source], entities=["父", "兒子"], topics=["主禱文", "憂慮"]
        )
        loaded = ws.get_note(note.id)
        fuzzy = ws.fuzzy("父 兒子 一天的憂慮")
        scripture = ws.fuzzy("40:6")
        library = ws.fuzzy("父與兒子的語言")
        source_art = ws.store.get_artifact(source.source_id)
        stale_blocked = False
        ws.update_note(note.id, text=loaded.text + " 更新。", expected_revision=1)
        try:
            ws.update_note(note.id, text="不應寫入", expected_revision=1)
        except ValueError as exc:
            stale_blocked = str(exc) == "stale_revision"
        revised = ws.get_note(note.id)
        history=ws.store.history(note.id)
        prov=ws.store.provenance_for(note.id)
        links=ws.store.links_for(note.id)
        checks = {
            "single_sqlite_truth": ws.store.db_path == root/"dore.sqlite3" and ws.store.db_path.exists(),
            "no_new_json_note_truth": not (root/"notes"/f"{note.id}.json").exists(),
            "same_note_id": loaded.id == note.id == revised.id,
            "scripture_identity_preserved": loaded.anchors[0].canon_id == "40:6",
            "library_source_is_artifact": source_art.kind == "library-source" and source_art.authority == "SOURCE",
            "library_source_preserved": loaded.source_refs[0].source_id == source.source_id,
            "fuzzy_personal_recall": bool(fuzzy) and fuzzy[0]["note_id"] == note.id,
            "fuzzy_scripture_recall": bool(scripture) and scripture[0]["note_id"] == note.id,
            "fuzzy_library_recall": bool(library) and library[0]["note_id"] == note.id,
            "revision_incremented": revised.revision == 2,
            "stale_revision_blocked": stale_blocked,
            "immutable_history": [x["revision"] for x in history] == [1,2],
            "provenance_shared": any(x["relation"]=="attached-source" for x in prov),
            "typed_link_shared": any(x["relation"]=="cites" for x in links),
            "protected_by_default": revised.protected and revised.authorship == "USER",
        }
        return {"schema":"dore.scripture-workspace.acceptance.v2","ok":all(checks.values()),"checks":checks,"fts5_available":ws.store.fts5_available}


if __name__ == "__main__":
    result = run()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["ok"] else 1)
