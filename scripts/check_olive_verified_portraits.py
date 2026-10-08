#!/usr/bin/env python3
"""Fail-closed Olive portrait registry audit; no downloads or external requests."""
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
registry = json.loads((root / "static/dore-design/runtime/olive-verified-portraits.v1.json").read_text())
speakers = json.loads((root / "data/westside-core/entities/sermon-speakers.v1.json").read_text())
known = {r["id"].removeprefix("speaker:") for r in speakers["records"]}
assert registry["schema"] == "dore.olive-verified-portraits.v1"
seen = set()
for record in registry["records"]:
    slug = record["speaker"]
    assert slug in known and slug not in seen, f"Unknown or duplicate speaker: {slug}"
    seen.add(slug)
    assert all(record.get(key) is True for key in ("verified", "licenseVerified", "identityVerified")), slug
    assert all(isinstance(record.get(key), str) and record[key].strip() for key in ("source", "license", "identityEvidence", "url")), slug
    url = record["url"]
    assert url.startswith("/") and not url.startswith("//") and ".." not in url and "?" not in url, slug
    asset = root / "static" / url.lstrip("/")
    assert asset.is_file(), f"Missing local asset: {asset}"
    assert asset.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp", ".avif"}, slug
print(f"PASS: {len(seen)} verified portraits; {len(known)-len(seen)} speakers use typographic fallback")
