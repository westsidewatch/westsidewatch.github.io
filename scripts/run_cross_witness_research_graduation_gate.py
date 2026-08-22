#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ENG=Path("reports/DORÉ-CROSS-WITNESS-GRADUATION-GATE.json"); CAUSES=Path("reports/DORÉ-CROSS-WITNESS-DIFFERENCE-CAUSES.json"); MAP=Path("reports/DORÉ-CROSS-WITNESS-CORRESPONDENCE-MAP.json"); BENCH=Path("reports/DORÉ-CROSS-WITNESS-RESEARCH-BENCHMARK.json"); OUT=Path("reports/DORÉ-CROSS-WITNESS-RESEARCH-GRADUATION.json")
def load(p):return json.loads(p.read_text(encoding="utf-8"))
def main():
    failures=[]
    try:
        eng,causes,cmap,bench=map(load,(ENG,CAUSES,MAP,BENCH))
        if eng.get("verdict") not in {"PASS","RESEARCH_EXCEPTIONS_ONLY"}:failures.append("engineering_not_graduated")
        if causes.get("status")!="PASS":failures.append("cause_classification_failed")
        if causes.get("unclassified_generic_count")!=0:failures.append(f"generic_unclassified:{causes.get('unclassified_generic_count')}")
        if cmap.get("status")!="PASS":failures.append("correspondence_map_failed")
        if cmap.get("phenomena")!=causes.get("phenomena"):failures.append("correspondence_coverage_mismatch")
        if bench.get("status")!="PASS":failures.append("research_benchmark_failed")
        if int(bench.get("passed",0))!=int(bench.get("total",-1)):failures.append("benchmark_not_complete")
        # Capability families that may not occur in this particular 3,138-row shared-reference
        # dataset (especially source-specific canon identities) are proven by benchmark cases,
        # not by forcing the corpus to contain a member of every taxonomy class.
        verdict="PASS" if not failures else "FAIL"
        milestone="WHY_VERSIONS_DIFFER_RESEARCH_GRADUATED" if verdict=="PASS" else "WHY_VERSIONS_DIFFER_RESEARCH_INCOMPLETE"
        result={"schema":"dore.cross-witness-research-graduation.v0.2","verdict":verdict,"milestone":milestone,"failures":failures,"phenomena_explained":causes.get("phenomena",0),"generic_unclassified":causes.get("unclassified_generic_count"),"cause_counts":causes.get("cause_counts",{}),"family_counts":causes.get("family_counts",{}),"confidence_counts":causes.get("confidence_counts",{}),"correspondence_clusters":cmap.get("cluster_count",0),"benchmark":{k:bench.get(k) for k in ("status","passed","total")},"capability_statement":"Doré can distinguish reference differences caused by versification, canon/source scope, ancient textual traditions, New Testament textual-base differences, and witness-specific reference traditions, while preserving uncertainty and provenance.","boundary":"Graduation explains validated reference-level differences. Translation-wording differences remain a distinct downstream layer requiring aligned textual content; they are never inferred from numbering alone."}
    except Exception as exc:
        result={"schema":"dore.cross-witness-research-graduation.v0.2","verdict":"FAIL","milestone":"WHY_VERSIONS_DIFFER_RESEARCH_INCOMPLETE","failures":[f"{type(exc).__name__}: {exc}"]}
    OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8");print(json.dumps(result,ensure_ascii=False,indent=2))
    if result["verdict"]!="PASS":raise SystemExit(1)
if __name__=="__main__":main()
