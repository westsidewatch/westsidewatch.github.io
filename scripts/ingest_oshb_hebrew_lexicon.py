#!/usr/bin/env python3
"""Download and ingest the complete pinned Open Scriptures Hebrew Lexicon."""
from __future__ import annotations
import json
from pathlib import Path
from urllib.request import urlopen
from dore_core.lexicon.oshb_source import ingest_oshb_lexicon

# Pin the exact upstream blobs observed when Lesson 05 was established.
AUG_BLOB = "f1b06e1f79c6a3b39d2d7c3e6c20b8f25a61e08a"
LEXICAL_BLOB = "d11eb2078532f3119c70822bd27a91b484d4727b"
UPSTREAM_REF = "master"
BASE = "https://raw.githubusercontent.com/openscriptures/HebrewLexicon/master"
OUT = Path("reports/DORÉ-HEBREW-LEXICON-INGESTION.json")

def fetch(name: str) -> str:
    with urlopen(f"{BASE}/{name}", timeout=60) as response:
        return response.read().decode("utf-8")

def main() -> None:
    aug_xml = fetch("AugIndex.xml")
    lexical_xml = fetch("LexicalIndex.xml")
    snapshot = f"HebrewLexicon:{UPSTREAM_REF}:AugIndex@{AUG_BLOB}:LexicalIndex@{LEXICAL_BLOB}"
    entries = ingest_oshb_lexicon(aug_xml, lexical_xml, snapshot)
    resolved = sum(e.status == "resolved" for e in entries.values())
    linked = sum(e.status == "index-linked" for e in entries.values())
    result = {
        "status": "PASS" if entries else "FAIL",
        "source": "openscriptures/HebrewLexicon",
        "license": "CC BY 4.0; underlying BDB and Strong dictionary texts public domain per upstream documentation",
        "snapshot": snapshot,
        "augmented_entries": len(entries),
        "resolved_lexemes": resolved,
        "index_linked_without_extracted_lexeme": linked,
        "lesson05_seed_targets": {key: (entries[key].lexeme if key in entries else None) for key in ("539", "3068", "2803", "6666")},
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if not entries:
        raise AssertionError("OSHB Hebrew Lexicon ingestion produced zero entries")

if __name__ == "__main__":
    main()
