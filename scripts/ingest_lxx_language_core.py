#!/usr/bin/env python3
"""Ingest the full CenterBLC Rahlfs 1935 LXX witness through Doré Language Core."""
from __future__ import annotations
import json
import os
import traceback
from collections import Counter
from pathlib import Path
from tf.fabric import Fabric
from dore_core.language.base import TextWitness, validate_units
from dore_core.language.adapters.lxx_textfabric import LXXTextFabricAdapter

SNAPSHOT = "4829f3746c84d75576702498e75a68856358f289"
OUT = Path("reports/DORÉ-LXX-INGESTION.json")
DEFAULT_DATA = Path(".cache/centerblc-lxx/tf/1935")
FEATURES = "otype book chapter verse word lex_utf8 morphology sp strongs translit_SBL subverse"

def write_result(result: dict) -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))

def load_api():
    data_dir = Path(os.environ.get("DORE_LXX_TF_DIR", str(DEFAULT_DATA))).resolve()
    if not data_dir.exists():
        raise FileNotFoundError(f"pinned LXX Text-Fabric directory not found: {data_dir}")
    fabric = Fabric(locations=str(data_dir), silent="deep")
    api = fabric.load(FEATURES, silent="deep")
    if api is None:
        raise RuntimeError(f"Text-Fabric failed to load pinned LXX features from {data_dir}")
    return api, data_dir

def run() -> dict:
    api, data_dir = load_api()
    witness = TextWitness(
        witness_id="witness.lxx.rahlfs1935.centerblc",
        language="grc",
        edition="Rahlfs LXX 1935 / CenterBLC Text-Fabric",
        source_id="source.centerblc.lxx",
        snapshot=SNAPSHOT,
        license_id="MIT-repository; derivative-source provenance retained",
        metadata={"doi":"10.5281/zenodo.5826308","source_repo":"CenterBLC/LXX"},
    )
    units = tuple(LXXTextFabricAdapter().ingest(api, witness))
    errors = validate_units(units, witness)
    books = Counter(u.canonical_ref_id.split(".")[2] for u in units if u.canonical_ref_id)
    lemma_units = sum(any(k == "lemma" and v for k, v in u.analyses) for u in units)
    morphology_units = sum(any(k == "morphology" and v for k, v in u.analyses) for u in units)
    translit_units = sum(any(k == "transliteration" and v for k, v in u.analyses) for u in units)
    return {
        "status":"PASS" if units and not errors else "FAIL",
        "study":"language_core.lxx.full_witness_ingestion",
        "witness_id":witness.witness_id,
        "snapshot":SNAPSHOT,
        "local_tf_directory":str(data_dir),
        "units":len(units),
        "books_or_witness_sections":len(books),
        "book_distribution":dict(sorted(books.items())),
        "lemma_coverage":{"units":lemma_units,"ratio":lemma_units / len(units) if units else 0},
        "morphology_coverage":{"units":morphology_units,"ratio":morphology_units / len(units) if units else 0},
        "transliteration_coverage":{"units":translit_units,"ratio":translit_units / len(units) if units else 0},
        "validation_errors":errors[:100],
        "source_policy":"remote repository pinned by git commit; loaded locally in CI; corpus not vendored into Doré",
    }

def main() -> None:
    try:
        result = run()
    except Exception as exc:
        result = {
            "status":"INFRA_FAIL",
            "study":"language_core.lxx.full_witness_ingestion",
            "snapshot":SNAPSHOT,
            "error_type":type(exc).__name__,
            "error":str(exc),
            "traceback":traceback.format_exc().splitlines()[-20:],
        }
    write_result(result)
    if result["status"] != "PASS":
        raise AssertionError(result)

if __name__ == "__main__":
    main()
