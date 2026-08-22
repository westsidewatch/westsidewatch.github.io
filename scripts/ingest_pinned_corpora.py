#!/usr/bin/env python3
"""Run Doré ingestion against real pinned upstream corpus files.

This runner is designed for CI: upstream files are downloaded at immutable
commit SHAs, then passed into Doré's ingestion adapters. It starts with real
Genesis, Daniel, Ezra, Matthew and Mark integration fixtures and is the bridge
to full-corpus traversal.
"""
from __future__ import annotations
import json
from urllib.request import urlopen
from dore_core.readers.corpus_ingestion import ingest_morphgnt, ingest_oshb, assert_lossless

OSHB_SHA = "3d15126fb1ef74867fc1434be1942e837932691f"
MORPHGNT_SHA = "aaed91e57c8e4a8dc9a2383e129ca5e75fe6393d"

TARGETS = {
    "GEN": f"https://raw.githubusercontent.com/openscriptures/morphhb/{OSHB_SHA}/wlc/Gen.xml",
    "DAN": f"https://raw.githubusercontent.com/openscriptures/morphhb/{OSHB_SHA}/wlc/Dan.xml",
    "EZR": f"https://raw.githubusercontent.com/openscriptures/morphhb/{OSHB_SHA}/wlc/Ezra.xml",
    "MAT": f"https://raw.githubusercontent.com/morphgnt/sblgnt/{MORPHGNT_SHA}/61-Mt-morphgnt.txt",
    "MRK": f"https://raw.githubusercontent.com/morphgnt/sblgnt/{MORPHGNT_SHA}/62-Mk-morphgnt.txt",
}

def fetch_text(url: str) -> str:
    with urlopen(url, timeout=30) as response:
        return response.read().decode("utf-8")

def main() -> None:
    reports = {}
    for code in ("GEN", "DAN", "EZR"):
        tokens, report = ingest_oshb(fetch_text(TARGETS[code]), code)
        assert_lossless(report)
        reports[code] = report.to_dict()
        reports[code]["languages"] = sorted({t.language for t in tokens})
    for code in ("MAT", "MRK"):
        tokens, report = ingest_morphgnt(fetch_text(TARGETS[code]).splitlines())
        assert_lossless(report)
        reports[code] = report.to_dict()
        reports[code]["languages"] = sorted({t.language for t in tokens})
    print(json.dumps(reports, ensure_ascii=False, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
