#!/usr/bin/env python3
"""Doré end-to-end cross-witness graduation gate.

Consumes the persisted alignment audit + structural triage reports and reduces
this phase to exactly one of:
  PASS
  RESEARCH_EXCEPTIONS_ONLY
  FAIL

The gate never declares textual originality and never normalizes witnesses.
"""
from __future__ import annotations
import json
from pathlib import Path

AUDIT = Path("reports/DORÉ-CROSS-WITNESS-ALIGNMENT-AUDIT.json")
TRIAGE = Path("reports/DORÉ-CROSS-WITNESS-EXCEPTION-TRIAGE.json")
OUT = Path("reports/DORÉ-CROSS-WITNESS-GRADUATION-GATE.json")

ENGINEERING_SUSPECT_CATEGORIES = {
    "single_witness_extra_reference",
    "anchor_only_reference",
}
RESEARCH_CATEGORIES = {
    "multi_witness_extra_reference_candidate",
    "translation_reference_divergence",
    "source_specific_reference",
}


def load(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(str(path))
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    try:
        audit = load(AUDIT)
        triage = load(TRIAGE)
        failures = []
        if audit.get("status") != "PASS":
            failures.append("alignment_audit_not_pass")
        if triage.get("status") != "PASS":
            failures.append("exception_triage_not_pass")
        if audit.get("missing_inventories"):
            failures.append("missing_witness_inventories")
        if audit.get("witness_count") != len(audit.get("expected_inventories", [])):
            failures.append("witness_inventory_count_mismatch")

        counts = triage.get("category_counts", {})
        engineering_suspects = sum(int(counts.get(name, 0)) for name in ENGINEERING_SUSPECT_CATEGORIES)
        research_exceptions = sum(int(counts.get(name, 0)) for name in RESEARCH_CATEGORIES)

        if failures:
            verdict = "FAIL"
            milestone = "CROSS_WITNESS_GRADUATION_FAILED"
        elif engineering_suspects:
            verdict = "FAIL"
            milestone = "CROSS_WITNESS_ENGINEERING_REVIEW_REQUIRED"
        elif research_exceptions:
            verdict = "RESEARCH_EXCEPTIONS_ONLY"
            milestone = "CROSS_WITNESS_ENGINEERING_GRADUATED"
        else:
            verdict = "PASS"
            milestone = "CROSS_WITNESS_ALIGNMENT_GRADUATED"

        result = {
            "schema": "dore.cross-witness-graduation-gate.v0.1",
            "verdict": verdict,
            "milestone": milestone,
            "engineering_failures": failures,
            "engineering_suspect_count": engineering_suspects,
            "research_exception_count": research_exceptions,
            "category_counts": counts,
            "rules": {
                "PASS": "all inventories/audits pass and no unresolved structural exceptions remain",
                "RESEARCH_EXCEPTIONS_ONLY": "engineering is clean; remaining differences are classified research phenomena only",
                "FAIL": "pipeline/inventory failure or unresolved engineering-suspect reference patterns remain",
            },
            "research_boundary": "No verdict in this file asserts textual originality, inspiration, authenticity, or automatic versification equivalence.",
        }
    except Exception as exc:
        result = {
            "schema": "dore.cross-witness-graduation-gate.v0.1",
            "verdict": "FAIL",
            "milestone": "CROSS_WITNESS_GRADUATION_FAILED",
            "engineering_failures": [f"{type(exc).__name__}: {exc}"],
        }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    if result["verdict"] == "FAIL":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
