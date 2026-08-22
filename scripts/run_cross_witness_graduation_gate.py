#!/usr/bin/env python3
"""Doré end-to-end cross-witness graduation gate.

Reduces the cross-witness engineering phase to exactly one of:
  PASS
  RESEARCH_EXCEPTIONS_ONLY
  FAIL

Reference-level disagreement is textual/versification evidence, not an engineering
defect by itself. Engineering failure requires a failed pipeline, missing/invalid
inventory, scope invariant breach, or malformed canonical identity.
"""
from __future__ import annotations
import json
from pathlib import Path

AUDIT=Path("reports/DORÉ-CROSS-WITNESS-ALIGNMENT-AUDIT.json")
TRIAGE=Path("reports/DORÉ-CROSS-WITNESS-EXCEPTION-TRIAGE.json")
OUT=Path("reports/DORÉ-CROSS-WITNESS-GRADUATION-GATE.json")
RESEARCH_CATEGORIES={"single_witness_extra_reference","anchor_only_reference","multi_witness_extra_reference_candidate","translation_reference_divergence","source_specific_reference"}
EXPECTED_SCOPE={
 "witness.original.oshb":39,
 "witness.original.morphgnt_sblgnt":27,
 "witness.lxx.rahlfs1935.centerblc":37,
 "witness.latin.vulgate.bible_api_io":66,
 "witness.chinese.cuv.traditional.1919":66,
 "witness.english.webu":66,
 "bible.asv.1901":66,
 "bible.kjv.1769":66,
}
def load(path):
    if not path.exists(): raise FileNotFoundError(str(path))
    return json.loads(path.read_text(encoding="utf-8"))
def main():
    try:
        audit=load(AUDIT); triage=load(TRIAGE); failures=[]
        if audit.get("status")!="PASS": failures.append("alignment_audit_not_pass")
        if triage.get("status")!="PASS": failures.append("exception_triage_not_pass")
        if audit.get("missing_inventories"): failures.append("missing_witness_inventories")
        if audit.get("witness_count")!=len(audit.get("expected_inventories",[])): failures.append("witness_inventory_count_mismatch")
        observed_rows=audit.get("observations",[])
        if not isinstance(observed_rows,list): failures.append("invalid_audit_observations_shape"); observed_rows=[]
        seen={item.get("witness_id"):int(item.get("books",-1)) for item in observed_rows if isinstance(item,dict) and item.get("witness_id")}
        for wid,expected in EXPECTED_SCOPE.items():
            if wid not in seen: failures.append(f"missing_expected_witness:{wid}")
            elif seen[wid]!=expected: failures.append(f"scope_mismatch:{wid}:{seen[wid]}!={expected}")
        counts=triage.get("category_counts",{}); research=sum(int(counts.get(name,0)) for name in RESEARCH_CATEGORIES)
        if failures: verdict="FAIL"; milestone="CROSS_WITNESS_GRADUATION_FAILED"
        elif research: verdict="RESEARCH_EXCEPTIONS_ONLY"; milestone="CROSS_WITNESS_ENGINEERING_GRADUATED"
        else: verdict="PASS"; milestone="CROSS_WITNESS_ALIGNMENT_GRADUATED"
        result={"schema":"dore.cross-witness-graduation-gate.v0.3","verdict":verdict,"milestone":milestone,"engineering_failures":failures,"engineering_suspect_count":0 if not failures else len(failures),"research_exception_count":research,"category_counts":counts,"scope_invariants":{"expected":EXPECTED_SCOPE,"observed":seen},"rules":{"PASS":"all ingestion/inventory/alignment invariants pass and no structural reference exceptions remain","RESEARCH_EXCEPTIONS_ONLY":"engineering invariants pass; all remaining reference differences are preserved as research phenomena","FAIL":"pipeline, inventory, canonical-scope, identity, or audit-shape invariant failed"},"research_boundary":"Single-witness, anchor-only, multi-witness, translation-divergence and source-specific reference patterns are not automatically engineering defects or textual judgments."}
    except Exception as exc:
        result={"schema":"dore.cross-witness-graduation-gate.v0.3","verdict":"FAIL","milestone":"CROSS_WITNESS_GRADUATION_FAILED","engineering_failures":[f"{type(exc).__name__}: {exc}"]}
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8"); print(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True))
    if result["verdict"]=="FAIL": raise SystemExit(1)
if __name__=="__main__": main()
