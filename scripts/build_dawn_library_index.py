#!/usr/bin/env python3
"""Build the Dawn Library processing index and derived Chinese projection.

The catalogue remains the presentation baseline, while language/classification
signals are enriched from the current work queue. Discovery-only Chinese works
are exposed as candidates, never silently promoted into holdings.
"""
from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOGUE = ROOT / "static/dawn-library/catalogue"
QUEUE = ROOT / "data/dawn-10k-work-queue.json"
DISCOVERY = ROOT / "data/dawn-10k-openlibrary-works.json"
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


def normalize_language(raw):
    values = [raw] if isinstance(raw, str) else raw if isinstance(raw, list) else []
    normalized = " ".join(str(x) for x in values).lower()
    if any(x in normalized for x in ("chinese", "zh", "zho", "chi", "中文", "漢", "汉")):
        return "zh"
    if normalized and normalized not in ("unknown", "und"):
        return normalized
    return "unknown"


def language_state(item):
    lang = normalize_language(item.get("language") or item.get("languages"))
    if lang != "unknown":
        return lang, "metadata"
    if HAN.search(text_of(item)):
        return "zh", "han-script"
    return "unknown", "unknown"


def first(item, *keys):
    for key in keys:
        value = item.get(key)
        if value not in (None, "", []):
            return value
    return None


def norm(text):
    if isinstance(text, list):
        text = " ".join(str(x) for x in text)
    text = unicodedata.normalize("NFKC", str(text or "")).casefold().strip()
    text = re.sub(r"[^\w\s-]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def signature(item):
    return f"{norm(first(item, 'title'))}::{norm(first(item, 'creator', 'author', 'creators', 'authors'))}"


def queue_maps():
    if not QUEUE.exists():
        return {}, {}, {"chi": 0, "eng": 0}
    data = load(QUEUE)
    by_id, by_sig = {}, {}
    for item in data.get("items", []):
        work_id = str(item.get("workId") or "").strip()
        if work_id:
            by_id[work_id] = item
        sig = signature(item)
        if sig != "::":
            by_sig.setdefault(sig, item)
    return by_id, by_sig, data.get("languageSignals") or {"chi": 0, "eng": 0}


def discovery_chinese():
    if not DISCOVERY.exists():
        return [], 0
    data = load(DISCOVERY)
    ids = []
    for item in data.get("items", []):
        if normalize_language(item.get("languages") or item.get("language")) == "zh" or item.get("matchedLanguage") == "chi":
            work_id = str(item.get("workId") or "").strip()
            if work_id:
                ids.append(work_id)
    metric = int((data.get("metrics") or {}).get("chineseMatchedWorksAdded", 0) or 0)
    return list(dict.fromkeys(ids)), metric


def main():
    root = payload(load(CATALOGUE / "index.json"))
    pages = root.get("pages", [])
    q_by_id, q_by_sig, queue_language_signals = queue_maps()
    candidate_ids, newly_discovered_chinese = discovery_chinese()
    rows, chinese, seen = [], [], set()
    enriched_language = enriched_classification = 0

    for page_name in pages:
        page = payload(load(CATALOGUE / page_name))
        for item in page_items(page):
            if not isinstance(item, dict):
                continue
            work_id = str(first(item, "id", "workId", "work_id", "key", "canonicalId") or "")
            if not work_id:
                work_id = f"anon:{len(rows)+1}"
            if work_id in seen:
                continue
            seen.add(work_id)
            queue_item = q_by_id.get(work_id) or q_by_sig.get(signature(item))
            lang, lang_evidence = language_state(item)
            if lang == "unknown" and queue_item:
                qlang = normalize_language(queue_item.get("languages") or queue_item.get("language"))
                if qlang != "unknown":
                    lang, lang_evidence = qlang, "work-queue"
                    enriched_language += 1
            cover = first(item, "cover", "coverId", "cover_id", "coverUrl", "cover_url")
            classification = first(item, "classification", "subjects", "subject", "categories")
            classification_evidence = "catalogue" if classification else "missing"
            if not classification and queue_item and queue_item.get("collectionScope"):
                classification = queue_item.get("collectionScope")
                classification_evidence = "collection-scope-gate"
                enriched_classification += 1
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
                "classificationStatus": "known" if classification else "missing",
                "classificationEvidence": classification_evidence,
                "catalogueStatus": "present",
            }
            rows.append(row)
            if row["chineseCollection"]:
                chinese.append(work_id)

    missing_cover = sum(r["coverStatus"] == "missing" for r in rows)
    missing_classification = sum(r["classificationStatus"] == "missing" for r in rows)
    out = {
        "schema": "dawn-library-build-index/v2",
        "source": "current-catalogue+current-work-queue",
        "count": len(rows),
        "expectedCatalogueCount": root.get("count"),
        "chineseCollectionCount": len(chinese),
        "queueLanguageSignals": queue_language_signals,
        "newlyDiscoveredChineseWorks": newly_discovered_chinese,
        "languageEnrichedFromQueueCount": enriched_language,
        "classificationEnrichedFromQueueCount": enriched_classification,
        "missingCoverCount": missing_cover,
        "missingClassificationCount": missing_classification,
        "items": rows,
    }
    zh = {
        "schema": "dawn-library-projection/v2",
        "id": "chinese-collection",
        "label": {"zh-Hant": "中文館藏", "en": "Chinese Collection"},
        "projectionOnly": True,
        "count": len(chinese),
        "workIds": chinese,
        "discoveryCandidateCount": len(candidate_ids),
        "newlyDiscoveredCandidateCount": newly_discovered_chinese,
        "discoveryCandidateWorkIds": candidate_ids,
        "candidatePolicy": "Discovery candidates remain pre-canonical until admission and promotion gates pass.",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    ZH_OUT.write_text(json.dumps(zh, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(json.dumps({
        "indexed": len(rows),
        "expected": root.get("count"),
        "chinese": len(chinese),
        "queueLanguageSignals": queue_language_signals,
        "newlyDiscoveredChinese": newly_discovered_chinese,
        "languageEnrichedFromQueue": enriched_language,
        "classificationEnrichedFromQueue": enriched_classification,
        "missingCover": missing_cover,
        "missingClassification": missing_classification,
    }, ensure_ascii=False))
    if root.get("count") is not None and len(rows) != root["count"]:
        raise SystemExit(f"catalogue count mismatch: indexed={len(rows)} expected={root['count']}")


if __name__ == "__main__":
    main()
