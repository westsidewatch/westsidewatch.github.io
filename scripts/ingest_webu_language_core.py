#!/usr/bin/env python3
"""Ingest pinned World English Bible Updated (WEBU) through Doré Language Core."""
from __future__ import annotations
import json, subprocess, traceback
from collections import Counter
from pathlib import Path
from dore_core.language.base import TextWitness, validate_units
from dore_core.language.inventory import write_inventory
from dore_core.language.adapters.verse_list_json import VerseListJSONAdapter

SOURCE_REPO = "https://github.com/ringletech/webu-open-bible.git"
SNAPSHOT = "44ce9156b77649adf11c0bbcee89c1d80e2c1f1c"
CACHE = Path(".cache/webu-open-bible")
OUT = Path("reports/DORÉ-WEBU-INGESTION.json")
INVENTORY = Path("reports/inventories/WEBU.json")

def main() -> None:
    try:
        if not CACHE.exists():
            CACHE.parent.mkdir(parents=True, exist_ok=True)
            subprocess.run(["git","clone","--filter=blob:none",SOURCE_REPO,str(CACHE)], check=True)
        subprocess.run(["git","-C",str(CACHE),"fetch","--depth","1","origin",SNAPSHOT], check=True)
        subprocess.run(["git","-C",str(CACHE),"checkout","--detach",SNAPSHOT], check=True)
        source = json.loads((CACHE / "json/complete-bible.json").read_text(encoding="utf-8"))
        witness = TextWitness("witness.english.webu","en","World English Bible Updated","source.ringletech.webu_open_bible",SNAPSHOT,"CC0-1.0",{"source_repo":"ringletech/webu-open-bible"})
        units = tuple(VerseListJSONAdapter("en").ingest(source, witness))
        errors = validate_units(units, witness)
        refs = {u.canonical_ref_id for u in units if u.canonical_ref_id}
        books = Counter(u.canonical_ref_id.split(".")[2] for u in units if u.canonical_ref_id)
        source_books = {str(r.get("book")) for r in source if isinstance(r, dict) and r.get("book")}
        inventory = write_inventory(INVENTORY, witness, units)
        result = {"status":"PASS" if len(books)==66 and not errors and refs else "FAIL","study":"language_core.english_webu.full_witness_ingestion","witness_id":witness.witness_id,"snapshot":SNAPSHOT,"license":"CC0-1.0","source_books":len(source_books),"mapped_book_ids":len(books),"canonical_verses":len(refs),"units":len(units),"inventory":str(INVENTORY),"inventory_refs":inventory["canonical_ref_count"],"validation_errors":errors[:100],"coverage_policy":"PASS requires all 66 canonical books mapped"}
    except Exception as exc:
        result={"status":"INFRA_FAIL","study":"language_core.english_webu.full_witness_ingestion","snapshot":SNAPSHOT,"error_type":type(exc).__name__,"error":str(exc),"traceback":traceback.format_exc().splitlines()[-20:]}
    OUT.parent.mkdir(parents=True, exist_ok=True); OUT.write_text(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True),encoding="utf-8")
    print(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True))
    if result["status"] != "PASS": raise AssertionError(result)
if __name__ == "__main__": main()
