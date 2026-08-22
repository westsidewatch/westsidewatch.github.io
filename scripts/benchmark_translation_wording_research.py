#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
from dore_core.research.translation_wording import classify_wording
OUT=Path("reports/DORÉ-TRANSLATION-WORDING-RESEARCH-BENCHMARK.json")
CASES=[
("Thou shalt not kill.","You shall not kill.","archaic_language_modernization"),
("He shewed them the way.","He showed them the way.","spelling_modernization"),
("Jesus Christ our Lord","our Lord Jesus Christ","word_order_or_syntax"),
("In the beginning God created the heaven and the earth","In the beginning God created the heavens and the earth","lexical_choice"),
("He went into the city and taught the people","He entered the city, teaching the people there","phrasing_or_expansion_compression"),
]
def main():
    rows=[]
    for a,b,expected in CASES:
        actual,confidence,why=classify_wording(a,b);rows.append({"expected":expected,"actual":actual,"confidence":confidence,"pass":actual==expected,"why":why})
    passed=sum(x["pass"] for x in rows); result={"schema":"dore.translation-wording-research-benchmark.v0.1","status":"PASS" if passed==len(rows) else "FAIL","passed":passed,"total":len(rows),"results":rows}
    OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8");print(json.dumps(result,ensure_ascii=False,indent=2))
    if result["status"]!="PASS":raise SystemExit(1)
if __name__=="__main__":main()
