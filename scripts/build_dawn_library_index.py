#!/usr/bin/env python3
"""Build a lightweight processing index for the current Dawn Library.

This is deliberately independent of the Reader and presentation layer. It scans
existing catalogue pages, records only routing/build facts, and projects Chinese
resources from the same global scan instead of maintaining a separate corpus.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOGUE = ROOT / "static/dawn-library/catalogue"
OUT = ROOT / "data/dawn-library-build-index.json"
ZH_OUT = ROOT / "data/dawn-library-chinese-projection.json"
HAN = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def payload(obj):
    if isinstance(obj, dict) and isinstance(obj.get("content"), str):
        try:
            return json.loads(obj["content"])
        except json.JSONDecodeError:
            pass
    return obj


def page_items(page):
    """Accept current consumption shards plus legacy catalogue shapes."""
    if isinstance(page, list):
        return page
    if not isinstance(page, dict):
        return []
    for key in ("works", "items", "resources", "entries"):
        value = page.get(key)
        if isinstance(value, list):
            return value
    return []


def text_of(item):
    bits = []
    for key in ("title", "subtitle", "creator", "author", "publisher", "description"):
        value = item.get(key)
        if isinstance(value, str):
            bits.append(value)
        elif isinstance(value, list):
            bits.extend(str(x) for x in value)
    for key in ("creators", "authors"):
        value = item.get(key)
        if isinstance(value, list):
            bits.extend(str(x) for x in value)
    return " ".join(bits)


def language_state(item):
    raw = item.get("language") or item.get("languages")
    values = []
    if isinstance(raw, str):
        values = [raw]
    elif isinstance(raw, list):
        values = [str(x) for x in raw]
    normalized = " ".join(values).lower()
    if any(x in normalized for x in ("chinese", "zh", "zho", "chi", "中文", "漢", "汉")):
        return "zh", "metadata"
    if HAN.search(text_of(item)):
        return "zh", "han-script"
    if normalized and normalized not in ("unknown", "und"):
        return normalized, "metadata"
    return "unknown", "unknown"


def first(item, *keys):
    for key in keys:
        value = item.get(key)
        if value not in (None, "", []):
            return value
    return None


def main():
    root = payload(load(CATALOGUE / "index.json"))
    pages = root.get("pages", [])
    rows = []
    chinese = []
    seen = set()

    for page_name in pages:
        page = payload(load(CATALOGUE / page_name))
        items = page_items(page)
        for item in items:
            if not isinstance(item, dict):
                continue
            work_id = str(first(item, "id", "workId", "work_id", "key", "canonicalId") or "")
            if not work_id:
                work_id = f"anon:{len(rows)+1}"
            if work_id in seen:
                continue
            seen.add(work_id)
            lang, lang_evidence = language_state(item)
            cover = first(item, "cover", "coverId", "cover_id", "coverUrl", "cover_url")
            row = {
                "id": work_id,
                "page": page_name,
                "title": first(item, "title") or "",
                "author": first(item, "creator", "author", "creators", "authors"),
                "period": first(item, "period", "century", "date", "year"),
                "language": lang,
                "languageEvidence": lang_evidence,
                "chineseCollection": lang == "zh",
                "coverStatus": "known" if cover else "missing",
                "classificationStatus": "known" if first(item, "classification", "subjects", "subject", "categories") else "missing",
                "catalogueStatus": "present",
            }
            rows.append(row)
            if row["chineseCollection"]:
                chinese.append(work_id)

    missing_cover = sum(r["coverStatus"] == "missing" for r in rows)
    missing_classification = sum(r["classificationStatus"] == "missing" for r in rows)
    out = {
        "schema": "dawn-library-build-index/v1",
        "source": "current-catalogue",
        "count": len(rows),
        "expectedCatalogueCount": root.get("count"),
        "chineseCollectionCount": len(chinese),
        "missingCoverCount": missing_cover,
        "missingClassificationCount": missing_classification,
        "items": rows,
    }
    zh = {
        "schema": "dawn-library-projection/v1",
        "id": "chinese-collection",
        "label": {"zh-Hant": "中文館藏", "en": "Chinese Collection"},
        "projectionOnly": True,
        "count": len(chinese),
        "workIds": chinese,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    ZH_OUT.write_text(json.dumps(zh, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(json.dumps({
        "indexed": len(rows),
        "expected": root.get("count"),
        "chinese": len(chinese),
        "missingCover": missing_cover,
        "missingClassification": missing_classification,
    }, ensure_ascii=False))
    if root.get("count") is not None and len(rows) != root["count"]:
        raise SystemExit(f"catalogue count mismatch: indexed={len(rows)} expected={root['count']}")


if __name__ == "__main__":
    main()
