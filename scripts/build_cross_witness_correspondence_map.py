#!/usr/bin/env python3
from __future__ import annotations
import json
from collections import defaultdict,Counter
from pathlib import Path
CAUSES=Path("reports/DORÉ-CROSS-WITNESS-DIFFERENCE-CAUSES.json"); OUT=Path("reports/DORÉ-CROSS-WITNESS-CORRESPONDENCE-MAP.json")

def main():
    data=json.loads(CAUSES.read_text(encoding="utf-8")); groups=defaultdict(list)
    for row in data.get("rows",[]):
        ref=row["ref"]; parts=ref.split("."); book=parts[2] if len(parts)>=5 and parts[:2]==["bible","ref"] else "SOURCE_SPECIFIC"; code=row["cause"]["code"]
        groups[(book,code)].append(row)
    clusters=[]; policies=Counter()
    for (book,code),rows in sorted(groups.items()):
        rows=sorted(rows,key=lambda r:r["ref"]); cause=rows[0]["cause"]; policies[cause["correspondence_policy"]]+=len(rows)
        clusters.append({"cluster_id":f"correspondence.{book}.{code}","book":book,"cause_code":code,"cause_family":cause["family"],"confidence":cause["confidence"],"explanation":cause["explanation"],"correspondence_policy":cause["correspondence_policy"],"phenomenon_count":len(rows),"refs":[r["ref"] for r in rows],"membership_patterns":[{"ref":r["ref"],"membership":r.get("membership",[]),"present":r.get("present",[]),"missing":r.get("missing",[])} for r in rows]})
    result={"schema":"dore.cross-witness-correspondence-map.v0.1","status":"PASS" if clusters else "FAIL","cluster_count":len(clusters),"phenomena":sum(c["phenomenon_count"] for c in clusters),"clusters":clusters,"policy_counts":dict(policies),"rule":"A correspondence cluster relates reference phenomena by cause and book. It does not assert verse-for-verse equivalence unless separately evidenced."}
    OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8");print(json.dumps({"status":result["status"],"clusters":len(clusters),"phenomena":result["phenomena"]},indent=2))
    if result["status"]!="PASS": raise SystemExit(1)
if __name__=="__main__":main()
