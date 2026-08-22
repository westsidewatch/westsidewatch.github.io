#!/usr/bin/env python3
from __future__ import annotations
import json
from collections import Counter,defaultdict
from pathlib import Path
from dore_core.research.difference_causes import classify

TRIAGE=Path("reports/DORÉ-CROSS-WITNESS-EXCEPTION-TRIAGE.json")
OUT=Path("reports/DORÉ-CROSS-WITNESS-DIFFERENCE-CAUSES.json")

def main():
    data=json.loads(TRIAGE.read_text(encoding="utf-8")); categories=data.get("categories",{})
    rows=[]; causes=Counter(); families=Counter(); confidence=Counter(); by_book=defaultdict(Counter)
    for category,items in categories.items():
        for item in items:
            ref=item.get("ref")
            if not ref: continue
            members=item.get("witnesses") or item.get("translations") or ([item.get("witness")] if item.get("witness") else [])
            cause=classify(ref,category,members,item.get("present",[]),item.get("missing",[])).to_dict()
            row={"ref":ref,"triage_category":category,"membership":sorted(x for x in members if x),"present":item.get("present",[]),"missing":item.get("missing",[]),"cause":cause}
            rows.append(row); causes[cause["code"]]+=1; families[cause["family"]]+=1; confidence[cause["confidence"]]+=1
            parts=ref.split("."); book=parts[2] if len(parts)>=5 and parts[:2]==["bible","ref"] else "SOURCE_SPECIFIC"; by_book[book][cause["code"]]+=1
    unclassified=[r for r in rows if r["cause"]["code"]=="structural_reference_difference"]
    result={"schema":"dore.cross-witness-difference-causes.v0.1","status":"PASS" if rows else "FAIL","phenomena":len(rows),"cause_counts":dict(sorted(causes.items())),"family_counts":dict(sorted(families.items())),"confidence_counts":dict(sorted(confidence.items())),"unclassified_generic_count":len(unclassified),"unclassified_generic_sample":unclassified[:100],"by_book":{b:dict(sorted(c.items())) for b,c in sorted(by_book.items())},"rows":rows,"interpretation_boundary":"A cause family explains why references diverge structurally; it does not adjudicate originality or doctrine."}
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8"); print(json.dumps({k:result[k] for k in ("status","phenomena","cause_counts","unclassified_generic_count")},ensure_ascii=False,indent=2))
    if result["status"]!="PASS": raise SystemExit(1)
if __name__=="__main__": main()
