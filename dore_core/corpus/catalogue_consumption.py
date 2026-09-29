from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Mapping, Sequence
import json
import re

LANGUAGE_ALIASES = {
    "eng": "en", "en": "en", "english": "en",
    "lat": "la", "la": "la", "latin": "la",
    "fre": "fr", "fra": "fr", "fr": "fr", "french": "fr",
    "ger": "de", "deu": "de", "de": "de", "german": "de",
    "dut": "nl", "nld": "nl", "nl": "nl", "dutch": "nl",
    "ita": "it", "it": "it", "italian": "it",
    "spa": "es", "es": "es", "spanish": "es",
    "gre": "el", "ell": "el", "el": "el", "greek": "el",
    "heb": "he", "he": "he", "hebrew": "he",
}


def normalize_language(value: str | None) -> str | None:
    if not value:
        return None
    token = re.split(r"[;,/|]", value.casefold().strip(), maxsplit=1)[0].strip()
    return LANGUAGE_ALIASES.get(token, token if 1 < len(token) <= 8 else None)


def enrich_languages(catalogue: dict) -> dict:
    counts: Counter[str] = Counter()
    for work in catalogue.get("works", []):
        languages = []
        for value in work.get("languages", []):
            normalized = normalize_language(value)
            if normalized and normalized not in languages:
                languages.append(normalized)
        # EEBO-TCP catalogue is overwhelmingly English; never fabricate a per-work
        # language when the source metadata omitted it. Unknown remains explicit.
        work["languages"] = languages
        work["languageState"] = "known" if languages else "unknown"
        counts.update(languages or ["unknown"])
    catalogue.setdefault("facets", {})["languages"] = dict(counts.most_common())
    return catalogue


def _summary(work: Mapping) -> dict:
    return {
        "id": work.get("id"), "title": work.get("title"), "creator": work.get("creator"),
        "date": work.get("date"), "century": work.get("century"),
        "languages": work.get("languages", []), "languageState": work.get("languageState", "unknown"),
        "witnessCount": work.get("witnessCount", 1), "cover": work.get("cover"),
        "reading": work.get("reading"),
    }


def write_consumption_index(catalogue: dict, root: str | Path, page_size: int = 250) -> dict:
    root = Path(root); pages = root / "pages"; works = catalogue.get("works", [])
    pages.mkdir(parents=True, exist_ok=True)
    page_files = []
    for start in range(0, len(works), page_size):
        number = start // page_size + 1
        name = f"{number:04d}.json"
        payload = {"page": number, "pageSize": page_size, "works": [_summary(w) for w in works[start:start + page_size]]}
        (pages / name).write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
        page_files.append(f"pages/{name}")
    index = {
        "schema": "dawn-library-consumption-index/v1",
        "count": len(works), "pageSize": page_size, "pageCount": len(page_files),
        "pages": page_files, "facets": catalogue.get("facets", {}),
        "holdingsModel": catalogue.get("holdingsModel"),
        "reader": {"selection": "left-page-index", "content": "right-page-on-demand", "initialFullCatalogueLoad": False},
    }
    root.mkdir(parents=True, exist_ok=True)
    (root / "index.json").write_text(json.dumps(index, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    return index
