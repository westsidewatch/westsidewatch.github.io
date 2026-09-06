#!/usr/bin/env python3
"""Executable acceptance for the shared Doré Scripture workspace.
No product UI, model, network, or paid API is required.
"""
from __future__ import annotations
import json
import tempfile
from pathlib import Path
from scripture_workspace import ScriptureAnchor, LibrarySourceRef, ScriptureWorkspace


def run() -> dict:
    with tempfile.TemporaryDirectory(prefix="dore-scripture-workspace-") as td:
        ws = ScriptureWorkspace(Path(td))
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
        stale_blocked = False
        ws.update_note(note.id, text=loaded.text + " 更新。", expected_revision=1)
        try:
            ws.update_note(note.id, text="不應寫入", expected_revision=1)
        except ValueError as exc:
            stale_blocked = str(exc) == "stale_revision"
        revised = ws.get_note(note.id)
        checks = {
            "same_note_id": loaded.id == note.id == revised.id,
            "scripture_identity_preserved": loaded.anchors[0].canon_id == "40:6",
            "library_source_preserved": loaded.source_refs[0].source_id == "dawn:test:fatherhood",
            "fuzzy_personal_recall": bool(fuzzy) and fuzzy[0]["note_id"] == note.id,
            "fuzzy_scripture_recall": bool(scripture) and scripture[0]["note_id"] == note.id,
            "fuzzy_library_recall": bool(library) and library[0]["note_id"] == note.id,
            "revision_incremented": revised.revision == 2,
            "stale_revision_blocked": stale_blocked,
            "protected_by_default": revised.protected and revised.authorship == "USER",
        }
        return {"schema":"dore.scripture-workspace.acceptance.v1","ok":all(checks.values()),"checks":checks}


if __name__ == "__main__":
    result = run()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["ok"] else 1)
