#!/usr/bin/env python3
"""AW-011 visual-regression guard.

A cheaper World Demand result is not admissible if it exposes substantially
more diagnostic fallback than the V7 persistent-LDI baseline.  This keeps the
optimization target ordered: source fidelity / visual stability first, world
cost second.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path


def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--candidate",type=Path,required=True)
    ap.add_argument("--baseline",type=Path,required=True)
    ap.add_argument("--report",type=Path,required=True)
    ap.add_argument("--residual-tolerance",type=float,default=0.00015)
    a=ap.parse_args()
    c=json.loads(a.candidate.read_text())
    b=json.loads(a.baseline.read_text())
    cr=float(c["max_residual_uncovered_fraction"])
    br=float(b["max_residual_uncovered_fraction"])
    relock=bool(c.get("exact_final_source_relock"))
    passed=relock and cr <= br + a.residual_tolerance
    out={
      "status":"VISUAL_REGRESSION_GUARD_PASS" if passed else "VISUAL_REGRESSION_GUARD_FAIL",
      "baseline":"V7 persistent multilayer LDI",
      "candidate_residual":cr,
      "baseline_residual":br,
      "allowed_residual":br+a.residual_tolerance,
      "exact_source_relock":relock,
      "rule":"World Demand optimization may not buy efficiency by regressing established visual coverage.",
      "human_visual_gate":"REQUIRED"
    }
    a.report.parent.mkdir(parents=True,exist_ok=True)
    a.report.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps(out,indent=2))
    return 0 if passed else 3

if __name__=="__main__": raise SystemExit(main())
