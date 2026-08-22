#!/usr/bin/env python3
from __future__ import annotations
import json,os
from collections import defaultdict,Counter
from pathlib import Path
from dore_core.language.base import TextWitness
from dore_core.language.adapters.verse_list_json import VerseListJSONAdapter
from dore_core.language.adapters.usx import USXAdapter
from dore_core.research.translation_wording import classify_wording
from scripts.ingest_kjv_language_core import nested_units
OUT=Path("reports/DORÉ-ENGLISH-WORDING-DIFFERENCES.json")

def group(units):
    g=defaultdict(list)
    for u in units:g[u.canonical_ref_id].append((u.order,u.surface))
    return {r:" ".join(x for _,x in sorted(v)) for r,v in g.items()}

def main():
    webu=json.loads(Path(".cache/webu-open-bible/json/complete-bible.json").read_text(encoding="utf-8")); ww=TextWitness("witness.english.webu","en","WEBU","ringletech/webu-open-bible","44ce9156b77649adf11c0bbcee89c1d80e2c1f1c","CC0-1.0"); webu_text=group(VerseListJSONAdapter("en").ingest(webu,ww))
    aw=TextWitness("bible.asv.1901","en","ASV 1901","openbibleinfo/American-Standard-Version-Bible","5c83ee265c75b3b1c056435eff622a875f1edc45","Public Domain"); asv_text=group(USXAdapter("en").ingest(Path(os.environ.get("DORE_ASV_USX_DIR",".cache/asv/usx")),aw))
    kjv_data=json.loads(Path(os.environ.get("DORE_KJV_JSON",".cache/kjv/KJV.json")).read_text(encoding="utf-8-sig")); kw=TextWitness("bible.kjv.1769","en","KJV 1769","TheologyCommons/Bible.TEI.KJV","014f6966aad1dc8888b088cd11ea8216a46fa738","Public Domain"); kjv_text=group(nested_units(kjv_data,kw))
    witnesses={"KJV":kjv_text,"ASV":asv_text,"WEBU":webu_text}; pairs=[("KJV","ASV"),("KJV","WEBU"),("ASV","WEBU")]; pair_reports={}; total=Counter(); examples=defaultdict(list); unknown=0
    for a,b in pairs:
        shared=sorted(set(witnesses[a])&set(witnesses[b])); counts=Counter(); differing=0
        for ref in shared:
            ta,tb=witnesses[a][ref],witnesses[b][ref]
            if ta==tb:continue
            differing+=1; code,confidence,why=classify_wording(ta,tb);counts[code]+=1;total[code]+=1
            if code=="substantial_rendering_difference":unknown+=1
            if len(examples[code])<25:examples[code].append({"ref":ref,"pair":[a,b],"cause":code,"confidence":confidence,"why":why,"a":ta[:240],"b":tb[:240]})
        pair_reports[f"{a}__{b}"]={"shared_refs":len(shared),"differing_refs":differing,"cause_counts":dict(sorted(counts.items()))}
    result={"schema":"dore.english-wording-differences.v0.1","status":"PASS" if all(v["shared_refs"]>=30000 for v in pair_reports.values()) else "FAIL","witnesses":{k:len(v) for k,v in witnesses.items()},"pairs":pair_reports,"cause_counts":dict(sorted(total.items())),"substantial_rendering_difference_count":unknown,"examples":dict(sorted(examples.items())),"model":"Reference/textual-base alignment happens first. Wording causes are then classified as formatting, modernization, syntax/word order, lexical choice, phrasing/expansion-compression, or substantial rendering requiring deeper lexical study.","boundary":"A wording classifier does not decide which translation is best or which reading is original."}
    OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8");print(json.dumps({"status":result["status"],"witnesses":result["witnesses"],"cause_counts":result["cause_counts"],"substantial":unknown},ensure_ascii=False,indent=2))
    if result["status"]!="PASS":raise SystemExit(1)
if __name__=="__main__":main()
