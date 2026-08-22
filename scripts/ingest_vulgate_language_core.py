#!/usr/bin/env python3
"""Ingest a pinned Latin Vulgate witness through Doré Language Core."""
from __future__ import annotations
import json, subprocess, traceback
from collections import Counter
from pathlib import Path
from dore_core.language.base import TextWitness, validate_units
from dore_core.language.inventory import write_inventory
from dore_core.language.adapters.vulgate_json import VulgateJSONAdapter
SOURCE_REPO="https://github.com/bible-api-io/bible-api-version-vulgate.git"; SNAPSHOT="06fddfc6e4c09c522271d77cd1ab3b5d924d84a5"; CACHE=Path(".cache/bible-api-version-vulgate"); OUT=Path("reports/DORÉ-VULGATE-INGESTION.json"); INVENTORY=Path("reports/inventories/VULGATE.json")
def write_result(result): OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True),encoding="utf-8"); print(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True))
def run():
    if not CACHE.exists(): CACHE.parent.mkdir(parents=True,exist_ok=True); subprocess.run(["git","clone","--filter=blob:none",SOURCE_REPO,str(CACHE)],check=True)
    subprocess.run(["git","-C",str(CACHE),"fetch","--depth","1","origin",SNAPSHOT],check=True); subprocess.run(["git","-C",str(CACHE),"checkout","--detach",SNAPSHOT],check=True)
    source=json.loads((CACHE/"vulgate.json").read_text(encoding="utf-8")); witness=TextWitness("witness.latin.vulgate.bible_api_io","la","Latin Vulgate / bible-api-io witness","source.bible_api_io.vulgate",SNAPSHOT,"MIT-0",{"source_repo":"bible-api-io/bible-api-version-vulgate"}); adapter=VulgateJSONAdapter(); source_books=source.get("booksData",{}) if isinstance(source,dict) else {}; recognized=adapter.recognized_book_names(source); unrecognized=adapter.unrecognized_book_names(source); units=tuple(adapter.ingest(source,witness)); errors=validate_units(units,witness); books=Counter(u.canonical_ref_id.split(".")[2] for u in units if u.canonical_ref_id); refs={u.canonical_ref_id for u in units if u.canonical_ref_id}; complete=bool(source_books) and not unrecognized and len(recognized)==len(source_books); inv=write_inventory(INVENTORY,witness,units); status="PASS" if units and refs and not errors and complete else "FAIL"
    return {"status":status,"study":"language_core.latin_vulgate.full_witness_ingestion","witness_id":witness.witness_id,"snapshot":SNAPSHOT,"license":"MIT-0","source_books":len(source_books),"recognized_source_books":len(recognized),"unrecognized_source_books":list(unrecognized),"units":len(units),"canonical_verses":len(refs),"mapped_book_ids":len(books),"book_distribution":dict(sorted(books.items())),"inventory":str(INVENTORY),"inventory_refs":inv["canonical_ref_count"],"validation_errors":errors[:100],"coverage_policy":"PASS requires every source booksData entry to be explicitly mapped; no silent book dropping","annotation_policy":"surface/token witness first; Latin lemma+morphology remain a separate enrichment layer"}
def main():
    try: result=run()
    except Exception as exc: result={"status":"INFRA_FAIL","study":"language_core.latin_vulgate.full_witness_ingestion","snapshot":SNAPSHOT,"error_type":type(exc).__name__,"error":str(exc),"traceback":traceback.format_exc().splitlines()[-20:]}
    write_result(result)
    if result["status"]!="PASS": raise AssertionError(result)
if __name__=="__main__": main()
