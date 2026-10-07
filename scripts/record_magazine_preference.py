#!/usr/bin/env python3
"""Record normalized human editorial preference evidence."""
import argparse,json
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];DEFAULT=ROOT/"static/dore-design/magazine-preferences.v1.json"
ALLOWED={"portrait_scale","negative_space","name_alignment","type_scale","image_scale","density"}
def record(doc,speaker,selected,rejected=None,corrections=None,note=None):
 corrections=corrections or {}
 bad=set(corrections)-ALLOWED
 if bad:raise ValueError("unsupported correction: "+",".join(sorted(bad)))
 row={"surface":"OliveMountain","speaker":speaker,"selectedFamily":selected,"rejectedFamilies":sorted(set(rejected or [])),
      "corrections":corrections,"note":note or None}
 # stable semantic duplicate protection; timestamps are metadata only.
 key={k:v for k,v in row.items() if k!="note"}
 for x in doc["records"]:
  if all(x.get(k)==v for k,v in key.items()):return doc
 row["recordedAt"]=datetime.now(timezone.utc).isoformat();doc["records"].append(row);return doc
def main():
 p=argparse.ArgumentParser();p.add_argument("--speaker",required=True);p.add_argument("--selected",required=True);p.add_argument("--rejected",nargs="*",default=[]);p.add_argument("--correction",action="append",default=[]);p.add_argument("--note");p.add_argument("--file",default=str(DEFAULT));a=p.parse_args()
 corrections={}
 for item in a.correction:
  k,sep,v=item.partition("=")
  if not sep:raise SystemExit("correction must be key=value")
  corrections[k]=float(v) if v.replace(".","",1).lstrip("-").isdigit() else v
 path=Path(a.file);doc=json.loads(path.read_text(encoding="utf-8"));record(doc,a.speaker,a.selected,a.rejected,corrections,a.note);path.write_text(json.dumps(doc,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
if __name__=="__main__":main()
