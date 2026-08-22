#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
from dore_core.research.difference_causes import classify
OUT=Path("reports/DORÉ-CROSS-WITNESS-RESEARCH-BENCHMARK.json")
CASES=[
("bible.ref.PSA.12.9","anchor_only_reference",[],"psalm_superscription_or_numbering"),
("bible.ref.JOL.4.1","anchor_only_reference",[],"chapter_partition_difference"),
("bible.ref.JHN.7.53","multi_witness_extra_reference_candidate",["asv","kjv"],"new_testament_textual_base_difference"),
("bible.ref.ACT.8.37","multi_witness_extra_reference_candidate",["kjv","asv"],"new_testament_textual_base_difference"),
("bible.ref.DAN.3.31","multi_witness_extra_reference_candidate",["lxx","vulgate"],"expanded_ancient_text_tradition"),
("lxx.ref.1ESDR.1.1","source_specific_reference",["lxx"],"source_specific_identity"),
]
def main():
    results=[]
    for ref,cat,members,expected in CASES:
        got=classify(ref,cat,members).code;results.append({"ref":ref,"category":cat,"expected":expected,"actual":got,"pass":got==expected})
    passed=sum(r["pass"] for r in results);result={"schema":"dore.cross-witness-research-benchmark.v0.1","status":"PASS" if passed==len(results) else "FAIL","passed":passed,"total":len(results),"results":results}
    OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8");print(json.dumps(result,ensure_ascii=False,indent=2))
    if result["status"]!="PASS":raise SystemExit(1)
if __name__=="__main__":main()
