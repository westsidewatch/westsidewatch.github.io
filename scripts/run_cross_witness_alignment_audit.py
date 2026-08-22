#!/usr/bin/env python3
"""Audit every emitted Doré canonical inventory without inventing alignment."""
from __future__ import annotations
import json
from collections import Counter
from pathlib import Path
from dore_core.language.inventory import read_inventory
INV_DIR=Path("reports/inventories"); OUT=Path("reports/DORÉ-CROSS-WITNESS-ALIGNMENT-AUDIT.json")
EXPECTED={"OSHB.json","MORPHGNT-SBLGNT.json","LXX-RAHLFS1935.json","VULGATE.json","CUV-TRADITIONAL.json","WEBU.json","ASV.json","KJV.json"}
def main():
    missing=sorted(name for name in EXPECTED if not (INV_DIR/name).exists()); inventories=[]
    for name in sorted(EXPECTED-set(missing)):
        payload=read_inventory(INV_DIR/name); inventories.append(payload)
    ref_members=Counter()
    for inv in inventories:
        for ref in set(inv["canonical_refs"]): ref_members[ref]+=1
    union=set(ref_members); common={r for r,n in ref_members.items() if n==len(inventories)} if inventories else set(); exceptions=[]
    for inv in inventories:
        refs=set(inv["canonical_refs"]); absent=sorted(union-refs)
        if absent: exceptions.append({"type":"witness_reference_gap","witness_id":inv["witness_id"],"count":len(absent),"sample":absent[:100],"policy":"record only; do not infer missing text or renumber automatically"})
    status="PASS" if not missing and inventories and union else "FAIL"
    result={"schema":"dore.cross-witness-alignment-audit.v0.1","status":status,"milestone":"CORPUS_WIDE_ALIGNMENT_AUDITED" if status=="PASS" else "CORPUS_WIDE_ALIGNMENT_INCOMPLETE","expected_inventories":sorted(EXPECTED),"missing_inventories":missing,"witness_count":len(inventories),"witnesses":[{"witness_id":i["witness_id"],"language":i["language"],"books":i["book_count"],"canonical_refs":i["canonical_ref_count"]} for i in inventories],"union_canonical_refs":len(union),"refs_present_in_every_loaded_witness":len(common),"membership_histogram":dict(sorted(Counter(ref_members.values()).items())),"exception_count":len(exceptions),"exceptions":exceptions,"interpretation_policy":"inventory differences are observations, not automatically textual variants; canon scope, versification and ingestion errors require classification before conclusions"}
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8"); print(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True))
    if status!="PASS": raise SystemExit(1)
if __name__=="__main__": main()
