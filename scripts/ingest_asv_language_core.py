#!/usr/bin/env python3
from __future__ import annotations
import json, os, traceback
from collections import Counter
from pathlib import Path
from dore_core.language.base import TextWitness, validate_units
from dore_core.language.adapters.usx import USXAdapter

REPORT=Path("reports/DORÉ-ASV-INGESTION.json")
SNAPSHOT="5c83ee265c75b3b1c056435eff622a875f1edc45"
SOURCE="openbibleinfo/American-Standard-Version-Bible"

def main():
    report={"witness":"ASV-1901","source":SOURCE,"snapshot":SNAPSHOT,"license":"Public Domain"}
    try:
        src=Path(os.environ.get("DORE_ASV_USX_DIR", ".cache/asv/usx"))
        witness=TextWitness("bible.asv.1901","en","American Standard Version 1901",SOURCE,SNAPSHOT,"Public Domain")
        units=list(USXAdapter("en").ingest(src,witness))
        errors=validate_units(units,witness)
        refs={u.canonical_ref_id for u in units if u.canonical_ref_id}
        books={r.split(".")[2] for r in refs}
        report.update(units=len(units),verses=len(refs),books=len(books),book_ids=sorted(books),validation_errors=errors[:100])
        report["status"]="PASS" if len(books)==66 and len(refs)>=30000 and not errors else "FAIL"
    except Exception as exc:
        report.update(status="INFRA_FAIL",error_type=type(exc).__name__,error=str(exc),traceback=traceback.format_exc())
    REPORT.parent.mkdir(exist_ok=True)
    REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    if report["status"]!="PASS": raise SystemExit(1)
if __name__=="__main__": main()
