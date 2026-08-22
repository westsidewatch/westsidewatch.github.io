#!/usr/bin/env python3
"""Ingest pinned Traditional Chinese Union Version through Doré Language Core."""
from __future__ import annotations
import json, subprocess, traceback
from collections import Counter
from pathlib import Path
from dore_core.language.base import TextWitness, validate_units
from dore_core.language.adapters.midvash_book_json import MidvashBookJSONAdapter, OSIS_TO_CANON

SOURCE_REPO = "https://github.com/midvash/bible-data.git"
SNAPSHOT = "d9fe1779447717bbfcb578e505b893125cad581c"
CACHE = Path(".cache/midvash-bible-data")
BOOK_DIR = CACHE / "versions/zh/cuv/books"
OUT = Path("reports/DORÉ-CUV-TRADITIONAL-INGESTION.json")


def write_result(result: dict) -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))


def run() -> dict:
    if not CACHE.exists():
        CACHE.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["git", "clone", "--filter=blob:none", SOURCE_REPO, str(CACHE)], check=True)
    subprocess.run(["git", "-C", str(CACHE), "fetch", "--depth", "1", "origin", SNAPSHOT], check=True)
    subprocess.run(["git", "-C", str(CACHE), "checkout", "--detach", SNAPSHOT], check=True)

    witness = TextWitness(
        witness_id="witness.chinese.cuv.traditional.1919",
        language="zh-Hant",
        edition="Chinese Union Version (Traditional), 1919",
        source_id="source.midvash.bible_data.cuv",
        snapshot=SNAPSHOT,
        license_id="public-domain",
        metadata={"source_repo": "midvash/bible-data", "version": "cuv"},
    )
    adapter = MidvashBookJSONAdapter(language="zh-Hant")
    units = []
    seen_osis = set()
    source_files = sorted(BOOK_DIR.glob("*.json"))
    for path in source_files:
        source = json.loads(path.read_text(encoding="utf-8"))
        osis = str(source.get("book", ""))
        seen_osis.add(osis)
        units.extend(adapter.ingest_book(source, witness))

    errors = validate_units(units, witness)
    refs = {u.canonical_ref_id for u in units if u.canonical_ref_id}
    books = Counter(u.canonical_ref_id.split(".")[2] for u in units if u.canonical_ref_id)
    unknown_osis = sorted(x for x in seen_osis if x not in OSIS_TO_CANON)
    expected_canonical = set(OSIS_TO_CANON.values())
    missing_canonical = sorted(expected_canonical - set(books))
    source_books = len(seen_osis)
    status = "PASS" if source_books == 66 and len(books) == 66 and not unknown_osis and not missing_canonical and not errors else "FAIL"
    return {
        "status": status,
        "study": "language_core.chinese_cuv_traditional.full_witness_ingestion",
        "witness_id": witness.witness_id,
        "snapshot": SNAPSHOT,
        "license": "public-domain",
        "source_books": source_books,
        "mapped_book_ids": len(books),
        "canonical_verses": len(refs),
        "units": len(units),
        "unknown_osis_books": unknown_osis,
        "missing_canonical_books": missing_canonical,
        "validation_errors": errors[:100],
        "segmentation_policy": "Han character / alphanumeric run / punctuation; Chinese word segmentation is a later enrichment layer",
        "coverage_policy": "PASS requires all 66 source books and all 66 canonical book ids with no silent dropping",
    }


def main() -> None:
    try:
        result = run()
    except Exception as exc:
        result = {
            "status": "INFRA_FAIL",
            "study": "language_core.chinese_cuv_traditional.full_witness_ingestion",
            "snapshot": SNAPSHOT,
            "error_type": type(exc).__name__,
            "error": str(exc),
            "traceback": traceback.format_exc().splitlines()[-20:],
        }
    write_result(result)
    if result["status"] != "PASS":
        raise AssertionError(result)


if __name__ == "__main__":
    main()
