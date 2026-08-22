#!/usr/bin/env python3
"""Ingest pinned Traditional Chinese Union Version through Doré Language Core."""
from __future__ import annotations
import json, subprocess, traceback
from collections import Counter
from pathlib import Path
from dore_core.language.base import TextWitness, validate_units
from dore_core.language.inventory import write_inventory
from dore_core.language.adapters.midvash_book_json import MidvashBookJSONAdapter, OSIS_TO_CANON
SOURCE_REPO="https://github.com/midvash/bible-data.git"; SNAPSHOT="d9fe1779447717bbfcb578e505b893125cad581c"; CACHE=Path(".cache/midvash-bible-data"); BOOK_DIR=CACHE/"versions/zh/cuv/books"; OUT=Path("reports/DORÉ-CUV-TRADITIONAL-INGESTION.json"); INVENTORY=Path("reports/inventories/CUV-TRADITIONAL.json")
def write_result(result): OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True),encoding="utf-8"); print(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True))
def run():
    if not CACHE.exists(): CACHE.parent.mkdir(parents=True,exist_ok=True); subprocess.run(["git","clone","--filter=blob:none",SOURCE_REPO,str(CACHE)],check=True)
    subprocess.run(["git","-C",str(CACHE),"fetch","--depth","1","origin",SNAPSHOT],check=True); subprocess.run(["git","-C",str(CACHE),"checkout","--detach",SNAPSHOT],check=True)
    witness=TextWitness("witness.chinese.cuv.traditional.1919","zh-Hant","Chinese Union Version (Traditional), 1919","source.midvash.bible_data.cuv",SNAPSHOT,"public-domain",{"source_repo":"midvash/bible-data","version":"cuv"}); adapter=MidvashBookJSONAdapter(language="zh-Hant"); units=[]; seen_osis=set(); source_files=sorted(BOOK_DIR.glob("*.json"))
    for path in source_files:
        source=json.loads(path.read_text(encoding="utf-8")); osis=str(source.get("book","")); seen_osis.add(osis); units.extend(adapter.ingest_book(source,witness))
    errors=validate_units(units,witness); refs={u.canonical_ref_id for u in units if u.canonical_ref_id}; books=Counter(u.canonical_ref_id.split(".")[2] for u in units if u.canonical_ref_id); unknown=sorted(x for x in seen_osis if x not in OSIS_TO_CANON); missing=sorted(set(OSIS_TO_CANON.values())-set(books)); inv=write_inventory(INVENTORY,witness,units); status="PASS" if len(seen_osis)==66 and len(books)==66 and not unknown and not missing and not errors else "FAIL"
    return {"status":status,"study":"language_core.chinese_cuv_traditional.full_witness_ingestion","witness_id":witness.witness_id,"snapshot":SNAPSHOT,"license":"public-domain","source_books":len(seen_osis),"mapped_book_ids":len(books),"canonical_verses":len(refs),"units":len(units),"inventory":str(INVENTORY),"inventory_refs":inv["canonical_ref_count"],"unknown_osis_books":unknown,"missing_canonical_books":missing,"validation_errors":errors[:100],"segmentation_policy":"Han character / alphanumeric run / punctuation; Chinese word segmentation is a later enrichment layer","coverage_policy":"PASS requires all 66 source books and all 66 canonical book ids with no silent dropping"}
def main():
    try: result=run()
    except Exception as exc: result={"status":"INFRA_FAIL","study":"language_core.chinese_cuv_traditional.full_witness_ingestion","snapshot":SNAPSHOT,"error_type":type(exc).__name__,"error":str(exc),"traceback":traceback.format_exc().splitlines()[-20:]}
    write_result(result)
    if result["status"]!="PASS": raise AssertionError(result)
if __name__=="__main__": main()
