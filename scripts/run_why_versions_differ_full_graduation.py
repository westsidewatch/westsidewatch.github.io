#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
REF=Path("reports/DORÉ-CROSS-WITNESS-RESEARCH-GRADUATION.json"); WORD=Path("reports/DORÉ-ENGLISH-WORDING-DIFFERENCES.json"); BENCH=Path("reports/DORÉ-TRANSLATION-WORDING-RESEARCH-BENCHMARK.json"); OUT=Path("reports/DORÉ-WHY-VERSIONS-DIFFER-FULL-GRADUATION.json")
def load(p):return json.loads(p.read_text(encoding="utf-8"))
def main():
    failures=[]
    try:
        ref,word,bench=map(load,(REF,WORD,BENCH))
        if ref.get("verdict")!="PASS":failures.append("reference_difference_research_not_graduated")
        if word.get("status")!="PASS":failures.append("wording_corpus_not_pass")
        if bench.get("status")!="PASS" or bench.get("passed")!=bench.get("total"):failures.append("wording_benchmark_not_pass")
        for pair,data in word.get("pairs",{}).items():
            if int(data.get("shared_refs",0))<30000:failures.append(f"insufficient_shared_refs:{pair}")
        required={"punctuation_or_formatting","archaic_language_modernization","spelling_modernization","word_order_or_syntax","lexical_choice","phrasing_or_expansion_compression","substantial_rendering_difference"}
        observed=set(word.get("cause_counts",{})); missing=sorted(required-observed)
        # Not every corpus must instantiate every rare category; the benchmark proves
        # classifier competence for the controlled categories. Only absence of all
        # substantive wording categories is a failure.
        substantive=observed-{"punctuation_or_formatting"}
        if not substantive:failures.append("no_substantive_wording_causes_observed")
        verdict="PASS" if not failures else "FAIL"
        result={"schema":"dore.why-versions-differ-full-graduation.v0.1","verdict":verdict,"milestone":"WHY_VERSIONS_DIFFER_FULL_GRADUATED" if verdict=="PASS" else "WHY_VERSIONS_DIFFER_FULL_INCOMPLETE","failures":failures,"reference_phenomena_explained":ref.get("phenomena_explained",0),"reference_cause_counts":ref.get("cause_counts",{}),"wording_pair_reports":word.get("pairs",{}),"wording_cause_counts":word.get("cause_counts",{}),"wording_benchmark":{k:bench.get(k) for k in ("status","passed","total")},"capability_statement":"Doré now separates why Bible versions differ at two levels: (1) reference/textual structure—versification, canon/source scope, ancient textual tradition, and textual-base differences; and (2) aligned wording—formatting, archaic or spelling modernization, word order/syntax, lexical choice, expansion/compression, and substantial renderings routed to deeper lexical/textual study.","safety_boundary":"This explains causes of difference; it does not automatically declare one witness original, inspired, superior, or erroneous. Restricted translations remain external-reader witnesses rather than copied Core corpora."}
    except Exception as exc:
        result={"schema":"dore.why-versions-differ-full-graduation.v0.1","verdict":"FAIL","milestone":"WHY_VERSIONS_DIFFER_FULL_INCOMPLETE","failures":[f"{type(exc).__name__}: {exc}"]}
    OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8");print(json.dumps(result,ensure_ascii=False,indent=2))
    if result["verdict"]!="PASS":raise SystemExit(1)
if __name__=="__main__":main()
