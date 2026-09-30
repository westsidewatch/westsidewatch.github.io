#!/usr/bin/env python3
"""Scan Dawn canonical root+shards and report how every Work can be read."""
from __future__ import annotations

from collections import Counter
from pathlib import Path
import json

from dore_core.reading_capability import resolve_reading_capability

ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT / "static" / "dawn-library" / "canonical"
OUTPUT = ROOT / "static" / "dawn-library" / "reading-capabilities.json"


def _works(payload):
    if isinstance(payload, list): return payload
    if isinstance(payload, dict):
        for key in ("works", "items", "entries"):
            if isinstance(payload.get(key), list): return payload[key]
    raise ValueError("canonical shard has no Work array")


def main() -> int:
    root = json.loads((CANONICAL / "root.json").read_text(encoding="utf-8"))
    counts: Counter[str] = Counter()
    providers: Counter[str] = Counter()
    total = 0
    for shard in root["shards"]:
        payload = json.loads((CANONICAL / shard["href"]).read_text(encoding="utf-8"))
        works = _works(payload)
        if len(works) != shard["workCount"]:
            raise SystemExit(f"shard count mismatch: {shard['href']}")
        for work in works:
            resolution = resolve_reading_capability(work)
            counts[resolution.capability.value] += 1
            if resolution.provider: providers[resolution.provider] += 1
            total += 1
    if total != root["workCount"]:
        raise SystemExit(f"canonical total mismatch: scanned={total} root={root['workCount']}")
    report = {
        "schema": "dawn.library.reading-capabilities.v1",
        "canonicalWorkCount": total,
        "capabilities": dict(sorted(counts.items())),
        "providers": dict(sorted(providers.items())),
        "readerReady": counts["local-full-text"] + counts["open-acquisition"] + counts["authenticated-acquisition"],
        "externalReader": counts["external-reader"],
        "metadataOnly": counts["metadata-only"],
        "policy": "identity-independent-reading-transport",
    }
    OUTPUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
