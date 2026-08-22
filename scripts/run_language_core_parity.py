#!/usr/bin/env python3
"""Verify that universal Hebrew/Aramaic and Greek adapters preserve the validated legacy corpus evidence."""
from __future__ import annotations
import json
from pathlib import Path
from urllib.request import urlopen
from dore_core.language.base import TextWitness
from dore_core.language.adapters import OSHBAdapter, MorphGNTAdapter
from dore_core.readers.corpus_ingestion import ingest_oshb, ingest_morphgnt, assert_lossless
from dore_core.readers.original_language import OSHB_SNAPSHOT, MORPHGNT_SNAPSHOT

OUT = Path("reports/DORÉ-LANGUAGE-CORE-PARITY.json")
OT = {
"GEN":"Gen.xml","EXO":"Exod.xml","LEV":"Lev.xml","NUM":"Num.xml","DEU":"Deut.xml","JOS":"Josh.xml","JDG":"Judg.xml","RUT":"Ruth.xml","1SA":"1Sam.xml","2SA":"2Sam.xml","1KI":"1Kgs.xml","2KI":"2Kgs.xml","1CH":"1Chr.xml","2CH":"2Chr.xml","EZR":"Ezra.xml","NEH":"Neh.xml","EST":"Esth.xml","JOB":"Job.xml","PSA":"Ps.xml","PRO":"Prov.xml","ECC":"Eccl.xml","SNG":"Song.xml","ISA":"Isa.xml","JER":"Jer.xml","LAM":"Lam.xml","EZK":"Ezek.xml","DAN":"Dan.xml","HOS":"Hos.xml","JOL":"Joel.xml","AMO":"Amos.xml","OBA":"Obad.xml","JON":"Jonah.xml","MIC":"Mic.xml","NAM":"Nah.xml","HAB":"Hab.xml","ZEP":"Zeph.xml","HAG":"Hag.xml","ZEC":"Zech.xml","MAL":"Mal.xml"}
NT = {
"MAT":"61-Mt-morphgnt.txt","MRK":"62-Mk-morphgnt.txt","LUK":"63-Lk-morphgnt.txt","JHN":"64-Jn-morphgnt.txt","ACT":"65-Ac-morphgnt.txt","ROM":"66-Ro-morphgnt.txt","1CO":"67-1Co-morphgnt.txt","2CO":"68-2Co-morphgnt.txt","GAL":"69-Ga-morphgnt.txt","EPH":"70-Eph-morphgnt.txt","PHP":"71-Php-morphgnt.txt","COL":"72-Col-morphgnt.txt","1TH":"73-1Th-morphgnt.txt","2TH":"74-2Th-morphgnt.txt","1TI":"75-1Ti-morphgnt.txt","2TI":"76-2Ti-morphgnt.txt","TIT":"77-Tit-morphgnt.txt","PHM":"78-Phm-morphgnt.txt","HEB":"79-Heb-morphgnt.txt","JAS":"80-Jas-morphgnt.txt","1PE":"81-1Pe-morphgnt.txt","2PE":"82-2Pe-morphgnt.txt","1JN":"83-1Jn-morphgnt.txt","2JN":"84-2Jn-morphgnt.txt","3JN":"85-3Jn-morphgnt.txt","JUD":"86-Jud-morphgnt.txt","REV":"87-Re-morphgnt.txt"}

def fetch(url):
    with urlopen(url, timeout=60) as r: return r.read().decode("utf-8")

def token_signature(t):
    return (t.canonical_ref_id, t.order, t.surface, t.normalized, t.language, tuple((a.type, a.value) for a in t.analyses))

def unit_signature(u):
    return (u.canonical_ref_id, u.order, u.surface, u.normalized, u.language, tuple(u.analyses))

def main():
    mismatches=[]; legacy_total=0; core_total=0
    oshb_adapter=OSHBAdapter(); greek_adapter=MorphGNTAdapter()
    for code, filename in OT.items():
        raw=fetch(f"https://raw.githubusercontent.com/openscriptures/morphhb/{OSHB_SNAPSHOT}/wlc/{filename}")
        legacy, rep=ingest_oshb(raw, code); assert_lossless(rep)
        witness=TextWitness("witness.oshb.wlc", "he", "WLC/OSHB", "source.oshb", OSHB_SNAPSHOT)
        core=tuple(oshb_adapter.ingest((raw, code), witness))
        legacy_total+=len(legacy); core_total+=len(core)
        if [token_signature(x) for x in legacy] != [unit_signature(x) for x in core]: mismatches.append(code)
    for code, filename in NT.items():
        raw=fetch(f"https://raw.githubusercontent.com/morphgnt/sblgnt/{MORPHGNT_SNAPSHOT}/{filename}")
        legacy, rep=ingest_morphgnt(raw.splitlines()); assert_lossless(rep)
        witness=TextWitness("witness.sblgnt", "grc", "SBLGNT/MorphGNT", "source.sblgnt", MORPHGNT_SNAPSHOT)
        core=tuple(greek_adapter.ingest(raw, witness))
        legacy_total+=len(legacy); core_total+=len(core)
        if [token_signature(x) for x in legacy] != [unit_signature(x) for x in core]: mismatches.append(code)
    result={"status":"PASS" if not mismatches and legacy_total==core_total else "FAIL","books_checked":66,"legacy_units":legacy_total,"language_core_units":core_total,"mismatched_books":mismatches,"criterion":"surface+normalized+language+reference+order+analyses parity"}
    OUT.parent.mkdir(parents=True, exist_ok=True); OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"); print(json.dumps(result, ensure_ascii=False, indent=2))
    if result["status"]!="PASS": raise AssertionError(result)
if __name__=="__main__": main()
