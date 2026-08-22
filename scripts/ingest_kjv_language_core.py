#!/usr/bin/env python3
from __future__ import annotations
import json, os, re, traceback
from pathlib import Path
from typing import Any, Iterable
from dore_core.language.base import TextWitness, LanguageUnit, validate_units
from dore_core.language.inventory import write_inventory
from dore_core.language.adapters.verse_list_json import BOOK_ALIASES, TOKEN_RE
REPORT=Path("reports/DORÉ-KJV-INGESTION.json"); INVENTORY=Path("reports/inventories/KJV.json"); SNAPSHOT="014f6966aad1dc8888b088cd11ea8216a46fa738"; SOURCE="TheologyCommons/Bible.TEI.KJV"
CANON_66=("GEN","EXO","LEV","NUM","DEU","JOS","JDG","RUT","1SA","2SA","1KI","2KI","1CH","2CH","EZR","NEH","EST","JOB","PSA","PRO","ECC","SNG","ISA","JER","LAM","EZK","DAN","HOS","JOL","AMO","OBA","JON","MIC","NAM","HAB","ZEP","HAG","ZEC","MAL","MAT","MRK","LUK","JHN","ACT","ROM","1CO","2CO","GAL","EPH","PHP","COL","1TH","2TH","1TI","2TI","TIT","PHM","HEB","JAS","1PE","2PE","1JN","2JN","3JN","JUD","REV")
def canon_book(value):
    raw=str(value or "").strip(); upper=raw.upper()
    if re.fullmatch(r"(?:[1-3][A-Z]{2}|[A-Z]{3})",upper): return upper
    low=re.sub(r"\s+"," ",raw.lower()).strip(); direct=BOOK_ALIASES.get(low)
    if direct:return direct
    matches=[(len(name),code) for name,code in BOOK_ALIASES.items() if re.search(rf"(?<![a-z]){re.escape(name)}(?![a-z])",low)]
    return max(matches)[1] if matches else None
def emit_text_units(text,witness,ref):
    for order,surface in enumerate(TOKEN_RE.findall(text),1): yield LanguageUnit(witness.witness_id,ref,order,surface," ".join(surface.split()),witness.language,(),(f"textual_source:{witness.source_id}",f"snapshot:{witness.snapshot}"))
def row_units(rows,witness):
    for row in rows:
        if not isinstance(row,dict):continue
        book=canon_book(row.get("book") or row.get("bookName") or row.get("book_name") or row.get("b")); text=row.get("text") or row.get("verseText") or row.get("content")
        try: chapter=int(row.get("chapter") or row.get("chapterNumber") or row.get("c")); verse=int(row.get("verse") or row.get("verseNumber") or row.get("v"))
        except (TypeError,ValueError):continue
        if book and isinstance(text,str): yield from emit_text_units(text,witness,f"bible.ref.{book}.{chapter}.{verse}")
def tei_units(data,witness):
    try:testaments=data["TEI"]["text"]["group"]["text"]
    except (KeyError,TypeError):return
    books=[]
    for testament in testaments if isinstance(testaments,list) else []:
        group=testament.get("group") if isinstance(testament,dict) else None; nodes=group.get("text") if isinstance(group,dict) else None
        if isinstance(nodes,list):books.extend(n for n in nodes if isinstance(n,dict))
    canonical_order=len(books)==66
    for bi,node in enumerate(books):
        heading=((node.get("front") or {}).get("head") if isinstance(node.get("front"),dict) else None); book=CANON_66[bi] if canonical_order else canon_book(heading)
        chapters=(node.get("body") or {}).get("div") if isinstance(node.get("body"),dict) else None; chapters=[chapters] if isinstance(chapters,dict) else chapters
        if not book or not isinstance(chapters,list):continue
        for cn,ch in enumerate(chapters,1):
            verses=ch.get("p") if isinstance(ch,dict) else None; verses=[verses] if isinstance(verses,str) else verses
            if not isinstance(verses,list):continue
            for vn,text in enumerate(verses,1):
                if isinstance(text,str):yield from emit_text_units(text,witness,f"bible.ref.{book}.{cn}.{vn}")
def nested_units(data,witness):
    if isinstance(data,list):yield from row_units(data,witness);return
    if not isinstance(data,dict):return
    if "TEI" in data:yield from tei_units(data,witness);return
    for key in ("verses","data","rows"):
        if isinstance(data.get(key),list):yield from row_units(data[key],witness);return
def main():
    report={"witness":"KJV-1769","source":SOURCE,"snapshot":SNAPSHOT,"license":"Public Domain"}
    try:
        data=json.loads(Path(os.environ.get("DORE_KJV_JSON",".cache/kjv/KJV.json")).read_text(encoding="utf-8-sig")); witness=TextWitness("bible.kjv.1769","en","King James Version 1769",SOURCE,SNAPSHOT,"Public Domain"); units=list(nested_units(data,witness)); errors=validate_units(units,witness); refs={u.canonical_ref_id for u in units if u.canonical_ref_id}; books={r.split('.')[2] for r in refs}; inv=write_inventory(INVENTORY,witness,units); report.update(units=len(units),verses=len(refs),books=len(books),book_ids=sorted(books),inventory=str(INVENTORY),inventory_refs=inv["canonical_ref_count"],validation_errors=errors[:100]); report["status"]="PASS" if len(books)==66 and len(refs)>=30000 and not errors else "FAIL"
    except Exception as exc:report.update(status="INFRA_FAIL",error_type=type(exc).__name__,error=str(exc),traceback=traceback.format_exc())
    REPORT.parent.mkdir(exist_ok=True);REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");print(json.dumps(report,ensure_ascii=False,indent=2))
    if report["status"]!="PASS":raise SystemExit(1)
if __name__=="__main__":main()
