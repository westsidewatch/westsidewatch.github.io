#!/usr/bin/env python3
"""Acceptance: capability discovery must extend Doré without replacing Search."""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from capability_registry import discover, get  # noqa: E402

registry = json.loads((ROOT / "dore-design/knowledge-lab/capabilities/registry.json").read_text(encoding="utf-8"))
assert registry["schema"] == "dore.capability-registry.v1"

# Existing Doré Search remains the execution owner.
search_js = ROOT / "dore" / "dore-search.js"
assert search_js.exists(), "existing dore-search.js must remain present"
text = search_js.read_text(encoding="utf-8")
for marker in ("function parseReference", "function interpret", "function search"):
    assert marker in text, f"existing Doré Search contract missing: {marker}"

bible = discover(service="bible")
assert {x["id"] for x in bible} >= {"bible.scripture-search", "bible.original-language-search"}
assert all(x["execution"] == "native" for x in bible)
assert all(x["entrypoint"] == "/dore/dore-search.js" for x in bible)

# Planned library providers are discoverable only when explicitly requested.
assert get("library.books") is None
library = get("library.books", include_planned=True)
assert library and library["status"] == "planned"
assert library["cost"] == "free-only"

print("DORE_CAPABILITY_REGISTRY_ACCEPTANCE=PASS")
print("existing_search_owner=/dore/dore-search.js")
print("existing_bible_capabilities=2")
print("planned_library_capability=deferred")
