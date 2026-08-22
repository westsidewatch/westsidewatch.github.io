#!/usr/bin/env python3
"""Doré Lesson 04: real pinned corpus experiment for Gen 15:6 -> Rom 4:3 / Gal 3:6."""
from __future__ import annotations
import json
from pathlib import Path
from urllib.request import urlopen
from dore_core.readers.corpus_ingestion import ingest_morphgnt, ingest_oshb, assert_lossless
from dore_core.graph.textual_bridge import bridge_edge
from dore_core.readers.original_language import OSHB_SNAPSHOT, MORPHGNT_SNAPSHOT

OUT = Path("reports/DORÉ-ABRAHAM-INTERTEXT-EXPERIMENT.json")

def fetch(url: str) -> str:
    with urlopen(url, timeout=60) as response:
        return response.read().decode("utf-8")

def witness_dict(w):
    return {"reference":w.reference,"language":w.language,"surface":w.surface,"normalized":w.normalized,"lemmas":w.lemmas,"morphology":w.morphology,"provenance":w.provenance}

def main() -> None:
    gen_xml = fetch(f"https://raw.githubusercontent.com/openscriptures/morphhb/{OSHB_SNAPSHOT}/wlc/Gen.xml")
    rom_txt = fetch(f"https://raw.githubusercontent.com/morphgnt/sblgnt/{MORPHGNT_SNAPSHOT}/66-Ro-morphgnt.txt")
    gal_txt = fetch(f"https://raw.githubusercontent.com/morphgnt/sblgnt/{MORPHGNT_SNAPSHOT}/69-Ga-morphgnt.txt")
    gen, gen_report = ingest_oshb(gen_xml, "GEN")
    rom, rom_report = ingest_morphgnt(rom_txt.splitlines())
    gal, gal_report = ingest_morphgnt(gal_txt.splitlines())
    for report in (gen_report, rom_report, gal_report): assert_lossless(report)
    edges = [
        {"id":"intertext.gen15_6.rom4_3","source_ref":"GEN.15.6","target_ref":"ROM.4.3","relation":"explicit_quote","claim_class":"TEXT_EXPLICIT"},
        {"id":"intertext.gen15_6.gal3_6","source_ref":"GEN.15.6","target_ref":"GAL.3.6","relation":"explicit_quote","claim_class":"TEXT_EXPLICIT"},
    ]
    bridges = [bridge_edge(e, gen, rom if e["target_ref"].startswith("ROM") else gal) for e in edges]
    result = {"status":"PASS","experiment":"lesson04.abraham.cross_language_intertext","snapshots":{"oshb":OSHB_SNAPSHOT,"morphgnt_sblgnt":MORPHGNT_SNAPSHOT},"bridges":[{"edge_id":b.edge_id,"relation":b.relation,"claim_class":b.claim_class,"source":witness_dict(b.source),"target":witness_dict(b.target)} for b in bridges]}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__": main()
