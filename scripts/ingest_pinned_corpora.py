#!/usr/bin/env python3
"""Run Doré ingestion against real pinned upstream corpus files."""
from __future__ import annotations
import json
from urllib.request import urlopen
from dore_core.readers.corpus_ingestion import ingest_morphgnt, ingest_oshb, assert_lossless

OSHB_SHA = "3d15126fb1ef74867fc1434be1942e837932691f"
MORPHGNT_SHA = "aaed91e57c8e4a8dc9a2383e129ca5e75fe6393d"

OT_TARGETS = {
    "GEN": "Gen.xml",
    "DAN": "Dan.xml",
    "EZR": "Ezra.xml",
}

NT_TARGETS = {
    "MAT": "61-Mt-morphgnt.txt", "MRK": "62-Mk-morphgnt.txt", "LUK": "63-Lk-morphgnt.txt",
    "JHN": "64-Jn-morphgnt.txt", "ACT": "65-Ac-morphgnt.txt", "ROM": "66-Ro-morphgnt.txt",
    "1CO": "67-1Co-morphgnt.txt", "2CO": "68-2Co-morphgnt.txt", "GAL": "69-Ga-morphgnt.txt",
    "EPH": "70-Eph-morphgnt.txt", "PHP": "71-Php-morphgnt.txt", "COL": "72-Col-morphgnt.txt",
    "1TH": "73-1Th-morphgnt.txt", "2TH": "74-2Th-morphgnt.txt", "1TI": "75-1Ti-morphgnt.txt",
    "2TI": "76-2Ti-morphgnt.txt", "TIT": "77-Tit-morphgnt.txt", "PHM": "78-Phm-morphgnt.txt",
    "HEB": "79-Heb-morphgnt.txt", "JAS": "80-Jas-morphgnt.txt", "1PE": "81-1Pe-morphgnt.txt",
    "2PE": "82-2Pe-morphgnt.txt", "1JN": "83-1Jn-morphgnt.txt", "2JN": "84-2Jn-morphgnt.txt",
    "3JN": "85-3Jn-morphgnt.txt", "JUD": "86-Jud-morphgnt.txt", "REV": "87-Re-morphgnt.txt",
}

def fetch_text(url: str) -> str:
    with urlopen(url, timeout=30) as response:
        return response.read().decode("utf-8")

def main() -> None:
    reports = {}
    total_tokens = 0
    for code, filename in OT_TARGETS.items():
        url = f"https://raw.githubusercontent.com/openscriptures/morphhb/{OSHB_SHA}/wlc/{filename}"
        tokens, report = ingest_oshb(fetch_text(url), code)
        assert_lossless(report)
        total_tokens += report.emitted_tokens
        reports[code] = {**report.to_dict(), "languages": sorted({t.language for t in tokens})}
    for code, filename in NT_TARGETS.items():
        url = f"https://raw.githubusercontent.com/morphgnt/sblgnt/{MORPHGNT_SHA}/{filename}"
        tokens, report = ingest_morphgnt(fetch_text(url).splitlines())
        assert_lossless(report)
        total_tokens += report.emitted_tokens
        reports[code] = {**report.to_dict(), "languages": sorted({t.language for t in tokens})}
    print(json.dumps({"books_read": len(reports), "tokens_read": total_tokens, "reports": reports}, ensure_ascii=False, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
