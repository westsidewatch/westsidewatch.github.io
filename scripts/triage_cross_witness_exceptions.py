#!/usr/bin/env python3
"""Classify Doré cross-witness reference differences conservatively.

This script does not decide textual originality. It groups structural reference
patterns so later research can distinguish versification/canon-scope phenomena
from likely ingestion defects without silently normalizing any witness.
"""
from __future__ import annotations
import json
from collections import Counter, defaultdict
from pathlib import Path
from dore_core.language.inventory import read_inventory

INV_DIR = Path("reports/inventories")
OUT = Path("reports/DORÉ-CROSS-WITNESS-EXCEPTION-TRIAGE.json")
FILES = {
    "oshb": "OSHB.json",
    "morphgnt": "MORPHGNT-SBLGNT.json",
    "lxx": "LXX-RAHLFS1935.json",
    "vulgate": "VULGATE.json",
    "cuv": "CUV-TRADITIONAL.json",
    "webu": "WEBU.json",
    "asv": "ASV.json",
    "kjv": "KJV.json",
}
TRANSLATION_KEYS = {"lxx", "vulgate", "cuv", "webu", "asv", "kjv"}


def book_of(ref: str) -> str | None:
    parts = ref.split(".")
    return parts[2] if len(parts) >= 5 and parts[:2] == ["bible", "ref"] else None


def main() -> None:
    missing_files = [name for name in FILES.values() if not (INV_DIR / name).exists()]
    if missing_files:
        result = {"status": "FAIL", "missing_inventories": missing_files}
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        raise SystemExit(1)

    inv = {key: read_inventory(INV_DIR / name) for key, name in FILES.items()}
    refs = {key: set(value["canonical_refs"]) for key, value in inv.items()}
    books = {key: set(value["book_ids"]) for key, value in inv.items()}
    anchor = refs["oshb"] | refs["morphgnt"]
    anchor_books = books["oshb"] | books["morphgnt"]

    membership: dict[str, set[str]] = defaultdict(set)
    for key, values in refs.items():
        for ref in values:
            membership[ref].add(key)

    categories: dict[str, list[dict]] = defaultdict(list)
    all_refs = sorted(set().union(*refs.values()))
    for ref in all_refs:
        book = book_of(ref)
        if not book:
            categories["source_specific_reference"].append({"ref": ref, "witnesses": sorted(membership[ref])})
            continue
        members = membership[ref]
        translation_members = sorted(members & TRANSLATION_KEYS)
        in_anchor = ref in anchor

        if not in_anchor and len(translation_members) >= 2:
            categories["multi_witness_extra_reference_candidate"].append({
                "ref": ref,
                "translations": translation_members,
                "note": "structural candidate for versification/textual-history review; not a conclusion",
            })
        elif not in_anchor and len(translation_members) == 1:
            categories["single_witness_extra_reference"].append({
                "ref": ref,
                "witness": translation_members[0],
                "note": "priority ingestion-or-versification review",
            })

        if in_anchor:
            expected_translations = sorted(k for k in TRANSLATION_KEYS if book in books[k])
            missing = sorted(k for k in expected_translations if ref not in refs[k])
            if missing:
                present = sorted(k for k in expected_translations if ref in refs[k])
                if present:
                    categories["translation_reference_divergence"].append({
                        "ref": ref,
                        "present": present,
                        "missing": missing,
                        "note": "reference-level divergence only; classify before normalization",
                    })
                else:
                    categories["anchor_only_reference"].append({
                        "ref": ref,
                        "missing_from": missing,
                        "note": "all loaded translation witnesses in scope omit this anchor reference",
                    })

    summary = {name: len(items) for name, items in sorted(categories.items())}
    review_priority = (
        categories.get("single_witness_extra_reference", [])[:200]
        + categories.get("anchor_only_reference", [])[:200]
        + categories.get("multi_witness_extra_reference_candidate", [])[:200]
    )
    result = {
        "schema": "dore.cross-witness-exception-triage.v0.1",
        "status": "PASS",
        "principle": "classification is structural evidence, never automatic textual judgment",
        "anchor": {
            "policy": "OSHB OT + MorphGNT/SBLGNT NT",
            "books": len(anchor_books),
            "canonical_refs": len(anchor),
        },
        "category_counts": summary,
        "categories": {name: items for name, items in sorted(categories.items())},
        "review_priority": review_priority,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "category_counts": summary, "review_priority": len(review_priority)}, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
