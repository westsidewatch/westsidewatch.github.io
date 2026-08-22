#!/usr/bin/env python3
"""Audit Doré witness inventories against scoped canonical anchors."""
from __future__ import annotations
import json
from collections import Counter
from pathlib import Path
from dore_core.language.inventory import read_inventory
INV_DIR=Path("reports/inventories"); OUT=Path("reports/DORÉ-CROSS-WITNESS-ALIGNMENT-AUDIT.json")
EXPECTED={"OSHB.json","MORPHGNT-SBLGNT.json","LXX-RAHLFS1935.json","VULGATE.json","CUV-TRADITIONAL.json","WEBU.json","ASV.json","KJV.json"}
def book_of(ref): return ref.split(".")[2]
def main():
    missing=sorted(name for name in EXPECTED if not (INV_DIR/name).exists()); by_name={name:read_inventory(INV_DIR/name) for name in sorted(EXPECTED-set(missing))}
    oshb=set(by_name.get("OSHB.json",{}).get("canonical_refs",[])); nt=set(by_name.get("MORPHGNT-SBLGNT.json",{}).get("canonical_refs",[])); anchor=oshb|nt; anchor_books={book_of(r) for r in anchor}; exceptions=[]; observations=[]
    for name,inv in by_name.items():
        refs=set(inv["canonical_refs"]); books=set(inv["book_ids"]); overlap_books=books & anchor_books; expected_scope={r for r in anchor if book_of(r) in overlap_books}; missing_refs=sorted(expected_scope-refs); extra_refs=sorted(refs-expected_scope)
        observations.append({"file":name,"witness_id":inv["witness_id"],"books":len(books),"overlap_anchor_books":len(overlap_books),"canonical_refs":len(refs),"expected_anchor_refs_in_scope":len(expected_scope),"missing_from_witness":len(missing_refs),"extra_vs_anchor":len(extra_refs),"source_specific_refs":inv.get("source_specific_ref_count",0)})
        if missing_refs: exceptions.append({"type":"scoped_reference_gap","witness_id":inv["witness_id"],"count":len(missing_refs),"sample":missing_refs[:100],"classification":"unclassified: possible versification, omitted/combined verse, source scope, or ingestion defect","policy":"do not fill or renumber automatically"})
        if extra_refs: exceptions.append({"type":"scoped_reference_extra","witness_id":inv["witness_id"],"count":len(extra_refs),"sample":extra_refs[:100],"classification":"unclassified: possible alternate versification/addition or mapping defect","policy":"preserve witness identity; do not force onto anchor"})
        if inv.get("source_specific_ref_count",0): exceptions.append({"type":"source_specific_namespace","witness_id":inv["witness_id"],"count":inv["source_specific_ref_count"],"sample":inv.get("source_specific_ref_sample",[])[:100],"classification":"outside shared Protestant bible.ref alignment namespace","policy":"retain separately with provenance"})
    full66=[inv for inv in by_name.values() if set(inv.get("book_ids",[]))>=anchor_books]
    membership=Counter()
    for inv in full66:
        for ref in set(inv["canonical_refs"]):
            if ref in anchor: membership[ref]+=1
    status="PASS" if not missing and len(anchor_books)==66 and anchor else "FAIL"
    result={"schema":"dore.cross-witness-alignment-audit.v0.2","status":status,"milestone":"CORPUS_WIDE_ALIGNMENT_AUDITED" if status=="PASS" else "CORPUS_WIDE_ALIGNMENT_INCOMPLETE","anchor":{"policy":"OSHB OT + MorphGNT/SBLGNT NT define comparison loci, not theological textual authority","books":len(anchor_books),"refs":len(anchor),"oshb_refs":len(oshb),"morphgnt_refs":len(nt)},"expected_inventories":sorted(EXPECTED),"missing_inventories":missing,"witness_count":len(by_name),"observations":observations,"full_66_witness_count":len(full66),"anchor_membership_histogram_across_full_66_witnesses":dict(sorted(Counter(membership.values()).items())),"exception_count":len(exceptions),"exceptions":exceptions,"interpretation_policy":"A reference mismatch is an observation only. It is not a textual variant until source scope, versification, additions/omissions and adapter mapping have been investigated with provenance."}
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8"); print(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True))
    if status!="PASS": raise SystemExit(1)
if __name__=="__main__": main()
