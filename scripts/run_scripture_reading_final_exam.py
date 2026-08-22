#!/usr/bin/env python3
"""Canon-spanning final exam for the Scripture-reading phase."""
from __future__ import annotations
import json
from pathlib import Path
from dore_core.research.scripture_reading import parse_context,classify_intertext,REQUIRED_READING_CAPABILITIES
OUT=Path("reports/DORÉ-SCRIPTURE-READING-FINAL-EXAM.json")
# Deliberately spans Torah, history, poetry, wisdom, prophets, Gospels, Acts,
# Pauline/general epistles and apocalypse, including known difficult boundaries.
CASES=[
("GEN","1","1","torah"),("EXO","3","14","torah"),("DEU","6","5","torah"),
("JOS","3","16","history"),("1SA","17","4","history"),("2KI","25","27","history"),
("PSA","22","1","poetry"),("PSA","51","1","poetry"),("JOB","19","25","wisdom"),("ECC","12","13","wisdom"),
("ISA","7","14","prophet"),("ISA","40","3","prophet"),("JER","31","31","prophet"),("DAN","7","13","apocalyptic_prophet"),("MIC","5","2","prophet"),
("MAT","4","4","gospel"),("MAT","5","17","gospel"),("MAT","27","9","gospel"),("MRK","1","2","gospel"),("LUK","4","18","gospel"),("JHN","1","1","gospel"),
("ACT","8","37","acts_textual_boundary"),("ROM","3","10","pauline"),("1CO","15","3","pauline"),("GAL","3","16","pauline"),("HEB","10","5","homily_epistle"),
("JAS","2","23","general_epistle"),("1PE","2","6","general_epistle"),("JUD","14","1","general_epistle"),("REV","22","19","apocalypse")]
INTERTEXT_TESTS=[
({"explicit_formula":True},"explicit_quotation"),
({"source_wording_overlap":0.8},"strong_allusion"),
({"source_wording_overlap":0.45},"possible_echo"),
({"thematic_only":True},"thematic_parallel")]
def main():
    failures=[]; rows=[]
    for book,ch,v,genre in CASES:
        ref=f"bible.ref.{book}.{ch}.{v}"
        try:
            ctx=parse_context(ref); ok=ctx["book"]==f"bible.book.{book}" and ctx["chapter"]==f"bible.chapter.{book}.{ch}"
        except Exception: ok=False
        rows.append({"ref":ref,"genre":genre,"context_pass":ok})
        if not ok:failures.append(f"context:{ref}")
    inter=[]
    for args,expected in INTERTEXT_TESTS:
        actual,confidence=classify_intertext(**args); passed=actual==expected;inter.append({"expected":expected,"actual":actual,"confidence":confidence,"pass":passed})
        if not passed:failures.append(f"intertext:{expected}:{actual}")
    result={"schema":"dore.scripture-reading-final-exam.v0.1","status":"PASS" if not failures else "FAIL","cases":len(rows),"case_passed":sum(r["context_pass"] for r in rows),"genres":sorted({r["genre"] for r in rows}),"intertext_tests":inter,"required_capabilities":list(REQUIRED_READING_CAPABILITIES),"failures":failures,"policy":"Passing this exam demonstrates independent reading capability across the canon; it does not claim exhaustive interpretation of every passage."}
    OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8");print(json.dumps(result,ensure_ascii=False,indent=2))
    if result["status"]!="PASS":raise SystemExit(1)
if __name__=="__main__":main()
