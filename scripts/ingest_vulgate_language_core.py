#!/usr/bin/env python3
"""Ingest a pinned Latin Vulgate witness through Doré Language Core."""
from __future__ import annotations
import json, subprocess, traceback
from collections import Counter
from pathlib import Path
from typing import Any
from dore_core.language.base import TextWitness, validate_units
from dore_core.language.adapters.vulgate_json import VulgateJSONAdapter

SOURCE_REPO = "https://github.com/bible-api-io/bible-api-version-vulgate.git"
SNAPSHOT = "06fddfc6e4c09c522271d77cd1ab3b5d924d84a5"
CACHE = Path(".cache/bible-api-version-vulgate")
OUT = Path("reports/DORÉ-VULGATE-INGESTION.json")

def write_result(result: dict) -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))

def describe_source(value: Any, depth: int = 0) -> Any:
    """Return a compact, text-safe structural sample for CI diagnostics."""
    if depth >= 4:
        return {"type": type(value).__name__}
    if isinstance(value, dict):
        keys = list(value.keys())[:5]
        return {
            "type": "dict",
            "len": len(value),
            "keys": [str(k) for k in keys],
            "samples": {str(k): describe_source(value[k], depth + 1) for k in keys[:2]},
        }
    if isinstance(value, list):
        return {
            "type": "list",
            "len": len(value),
            "samples": [describe_source(v, depth + 1) for v in value[:2]],
        }
    if isinstance(value, str):
        return {"type": "str", "sample": value[:120]}
    return {"type": type(value).__name__, "sample": repr(value)[:120]}

def run() -> dict:
    if not CACHE.exists():
        CACHE.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["git","clone","--filter=blob:none",SOURCE_REPO,str(CACHE)], check=True)
    subprocess.run(["git","-C",str(CACHE),"fetch","--depth","1","origin",SNAPSHOT], check=True)
    subprocess.run(["git","-C",str(CACHE),"checkout","--detach",SNAPSHOT], check=True)
    source = json.loads((CACHE / "vulgate.json").read_text(encoding="utf-8"))
    witness = TextWitness(
        witness_id="witness.latin.vulgate.bible_api_io",
        language="la",
        edition="Latin Vulgate / bible-api-io witness",
        source_id="source.bible_api_io.vulgate",
        snapshot=SNAPSHOT,
        license_id="MIT-0",
        metadata={"source_repo":"bible-api-io/bible-api-version-vulgate"},
    )
    try:
        units = tuple(VulgateJSONAdapter().ingest(source, witness))
    except Exception as exc:
        raise ValueError(
            f"{exc}; source_shape={json.dumps(describe_source(source), ensure_ascii=False)}"
        ) from exc
    errors = validate_units(units, witness)
    books = Counter(u.canonical_ref_id.split(".")[2] for u in units if u.canonical_ref_id)
    refs = {u.canonical_ref_id for u in units if u.canonical_ref_id}
    return {
        "status":"PASS" if units and refs and not errors else "FAIL",
        "study":"language_core.latin_vulgate.full_witness_ingestion",
        "witness_id":witness.witness_id,
        "snapshot":SNAPSHOT,
        "license":"MIT-0",
        "units":len(units),
        "canonical_verses":len(refs),
        "books":len(books),
        "book_distribution":dict(sorted(books.items())),
        "validation_errors":errors[:100],
        "annotation_policy":"surface/token witness first; Latin lemma+morphology remain a separate enrichment layer",
    }

def main() -> None:
    try:
        result = run()
    except Exception as exc:
        result = {"status":"INFRA_FAIL","study":"language_core.latin_vulgate.full_witness_ingestion","snapshot":SNAPSHOT,"error_type":type(exc).__name__,"error":str(exc),"traceback":traceback.format_exc().splitlines()[-20:]}
    write_result(result)
    if result["status"] != "PASS": raise AssertionError(result)

if __name__ == "__main__": main()
