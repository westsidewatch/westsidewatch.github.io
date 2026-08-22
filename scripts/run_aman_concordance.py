#!/usr/bin/env python3
"""Doré Lesson 05B: build a whole-OT corpus concordance for אמן / OSHB 539."""
from __future__ import annotations
import json
from pathlib import Path
from urllib.request import urlopen
from dore_core.readers.corpus_ingestion import ingest_oshb, assert_lossless
from dore_core.lexicon.concordance import build_concordance

OSHB_SHA = "3d15126fb1ef74867fc1434be1942e837932691f"
OUT = Path("reports/DORÉ-AMAN-CONCORDANCE.json")
OT_TARGETS = {
    "GEN":"Gen.xml","EXO":"Exod.xml","LEV":"Lev.xml","NUM":"Num.xml","DEU":"Deut.xml","JOS":"Josh.xml","JDG":"Judg.xml","RUT":"Ruth.xml","1SA":"1Sam.xml","2SA":"2Sam.xml","1KI":"1Kgs.xml","2KI":"2Kgs.xml","1CH":"1Chr.xml","2CH":"2Chr.xml","EZR":"Ezra.xml","NEH":"Neh.xml","EST":"Esth.xml","JOB":"Job.xml","PSA":"Ps.xml","PRO":"Prov.xml","ECC":"Eccl.xml","SNG":"Song.xml","ISA":"Isa.xml","JER":"Jer.xml","LAM":"Lam.xml","EZK":"Ezek.xml","DAN":"Dan.xml","HOS":"Hos.xml","JOL":"Joel.xml","AMO":"Amos.xml","OBA":"Obad.xml","JON":"Jonah.xml","MIC":"Mic.xml","NAM":"Nah.xml","HAB":"Hab.xml","ZEP":"Zeph.xml","HAG":"Hag.xml","ZEC":"Zech.xml","MAL":"Mal.xml",
}

def fetch(url: str) -> str:
    with urlopen(url, timeout=60) as r:
        return r.read().decode("utf-8")

def main() -> None:
    tokens = []
    for code, filename in OT_TARGETS.items():
        xml = fetch(f"https://raw.githubusercontent.com/openscriptures/morphhb/{OSHB_SHA}/wlc/{filename}")
        book_tokens, report = ingest_oshb(xml, code)
        assert_lossless(report)
        tokens.extend(book_tokens)
    # OSHB corpus stores the lexical identifier in lemma analysis; Lesson 05 lexicon resolves 539 -> אמן.
    report = build_concordance(tokens, "539")
    result = {
        "status": "PASS" if report.occurrences else "FAIL",
        "study": "lesson05b.aman.whole_ot_concordance",
        "lexical_id": "539",
        "resolved_lexeme": "אָמַן",
        "snapshot": OSHB_SHA,
        "occurrence_count": len(report.occurrences),
        "book_distribution": report.book_distribution,
        "morphology_distribution": report.morphology_distribution,
        "surface_distribution": report.surface_distribution,
        "occurrences": [o.__dict__ for o in report.occurrences],
        "interpretive_status": "CORPUS_DATA_ONLY",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    if not report.occurrences:
        raise AssertionError("no occurrences found for OSHB lexical id 539")

if __name__ == "__main__":
    main()
