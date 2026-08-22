#!/usr/bin/env python3
"""Single final milestone gate: Scripture Reading Complete."""
from __future__ import annotations
import json
from pathlib import Path
CORPUS=Path("reports/DORÉ-CORPUS-READING-REPORT.json"); ALIGN=Path("reports/DORÉ-CROSS-WITNESS-GRADUATION-GATE.json"); DIFFER=Path("reports/DORÉ-WHY-VERSIONS-DIFFER-FULL-GRADUATION.json"); EXAM=Path("reports/DORÉ-SCRIPTURE-READING-FINAL-EXAM.json"); OUT=Path("reports/DORÉ-SCRIPTURE-READING-MILESTONE.json")
def load(p):return json.loads(p.read_text(encoding="utf-8"))
def main():
    failures=[]
    try:
        corpus,align,differ,exam=map(load,(CORPUS,ALIGN,DIFFER,EXAM))
        if corpus.get("status")!="PASS" or corpus.get("books_read")!=66 or corpus.get("silent_token_loss")!=0:failures.append("66_book_original_language_corpus_not_lossless")
        if align.get("milestone")!="CROSS_WITNESS_ENGINEERING_GRADUATED":failures.append("cross_witness_alignment_not_graduated")
        if differ.get("verdict")!="PASS" or differ.get("milestone")!="WHY_VERSIONS_DIFFER_FULL_GRADUATED":failures.append("version_difference_capability_not_passed")
        if exam.get("status")!="PASS" or exam.get("case_passed")!=exam.get("cases"):failures.append("canon_spanning_final_exam_not_passed")
        verdict="PASS" if not failures else "FAIL"
        result={"schema":"dore.scripture-reading-milestone.v1.0","verdict":verdict,"milestone":"SCRIPTURE_READING_COMPLETE" if verdict=="PASS" else "SCRIPTURE_READING_INCOMPLETE","failures":failures,"completion_definition":"Doré can independently locate and read any canonical passage using lossless original-language corpora, morphology/lemma evidence, context hierarchy, cross-witness alignment, version-difference reasoning, intertext confidence classes, provenance and uncertainty boundaries.","scope_boundary":"This closes Foundation Scripture Reading. It does not claim exhaustive exegesis, theology, church history, archaeology, geography or scholarship; those belong to later education/research layers.","evidence":{"books_read":corpus.get("books_read"),"tokens_read":corpus.get("tokens_read"),"silent_token_loss":corpus.get("silent_token_loss"),"alignment":align.get("milestone"),"version_difference":differ.get("milestone"),"final_exam_cases":exam.get("cases"),"final_exam_passed":exam.get("case_passed")}}
    except Exception as exc:result={"schema":"dore.scripture-reading-milestone.v1.0","verdict":"FAIL","milestone":"SCRIPTURE_READING_INCOMPLETE","failures":[f"{type(exc).__name__}: {exc}"]}
    OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8");print(json.dumps(result,ensure_ascii=False,indent=2))
    if result["verdict"]!="PASS":raise SystemExit(1)
if __name__=="__main__":main()
