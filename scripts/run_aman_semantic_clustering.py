#!/usr/bin/env python3
"""Lesson 05B practicum: cluster אמן evidence by morphology, without semantic overclaim."""
from __future__ import annotations
import json
from pathlib import Path
from dore_core.lexicon.concordance import ConcordanceOccurrence
from dore_core.lexicon.semantic_clustering import cluster_by_morphology

SOURCE = Path("reports/DORÉ-AMAN-CONCORDANCE.json")
OUT = Path("reports/DORÉ-AMAN-MORPHOLOGY-CLUSTERS.json")

def main() -> None:
    raw = json.loads(SOURCE.read_text(encoding="utf-8"))
    occurrences = tuple(ConcordanceOccurrence(**item) for item in raw["occurrences"])
    report = cluster_by_morphology(occurrences, raw["lexical_id"])
    result = {
        "status": "PASS" if report.total_occurrences == raw["occurrence_count"] else "FAIL",
        "study": "lesson05b.aman.morphology_clustering",
        "lexical_id": report.lexical_id,
        "resolved_lexeme": raw.get("resolved_lexeme"),
        "source_report": str(SOURCE),
        "total_occurrences": report.total_occurrences,
        "interpretive_status": report.interpretive_status,
        "clusters": [
            {
                "morphology_family": c.key,
                "count": c.count,
                "references": c.references,
                "surfaces": c.surfaces,
                "raw_lemmas": c.raw_lemmas,
            }
            for c in report.clusters
        ],
        "guardrail": "No semantic sense labels are assigned by morphology alone.",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    if result["status"] != "PASS":
        raise AssertionError("morphology clustering lost concordance occurrences")

if __name__ == "__main__":
    main()
