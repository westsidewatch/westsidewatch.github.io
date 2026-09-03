#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ADAPTER = ROOT / "local" / "dore-local" / "dawn_library_books.py"
REGISTRY = ROOT / "dore-design" / "knowledge-lab" / "capabilities" / "registry.json"
SEARCH = ROOT / "static" / "dore" / "dore-search.js"
CONVERSATION_WORKFLOW = ROOT / ".github" / "workflows" / "dore-conversation-alpha.yml"


def load_adapter():
    spec = importlib.util.spec_from_file_location("dawn_library_books", ADAPTER)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def main() -> int:
    assert ADAPTER.exists(), "adapter missing"
    assert SEARCH.exists(), "existing Doré Search missing"
    assert CONVERSATION_WORKFLOW.exists(), "existing Conversation workflow missing"

    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    books = next(x for x in registry["capabilities"] if x["id"] == "library.books")
    assert books["execution"] == "adapter"
    assert books["entrypoint"] == "local/dore-local/dawn_library_books.py"
    assert books["cost"] == "free-only"
    assert books["paid_fallback"] is False
    assert books["credentials"] == "none"

    adapter = load_adapter()
    fixture = {
        "key": "/works/OL82563W",
        "title": "The Pilgrim's Progress",
        "author_name": ["John Bunyan"],
        "author_key": ["OL122260A"],
        "first_publish_year": 1678,
        "edition_count": 400,
        "isbn": ["9780000000000"],
        "language": ["eng"],
        "cover_i": 123,
    }
    normalized = adapter.normalize_doc(fixture)
    assert normalized.work_id == "OL82563W"
    assert normalized.title == "The Pilgrim's Progress"
    assert normalized.provider == "open-library"
    assert normalized.provenance["credentials_required"] is False
    assert normalized.provenance["paid_fallback"] is False
    assert normalized.provider_url == "https://openlibrary.org/works/OL82563W"

    search_text = SEARCH.read_text(encoding="utf-8")
    for marker in ("function parseReference", "function interpret", "function search"):
        assert marker in search_text, f"native Doré Search marker missing: {marker}"

    print("DAWN_LIBRARY_BOOKS_ACCEPTANCE=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
