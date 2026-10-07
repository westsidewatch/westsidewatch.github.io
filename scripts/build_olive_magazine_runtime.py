#!/usr/bin/env python3
import importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SPEAKERS=ROOT/"data/westside-core/entities/sermon-speakers.v1.json"
GEN=ROOT/"scripts/generate_magazine_candidates.py"
SCORE=ROOT/"scripts/score_magazine_candidates.py"
OUT=ROOT/"static/dore-design/runtime/olive-speaker-compositions.v1.json"
def module(path,name):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def build():
 gen=module(GEN,"magazine_gen");score=module(SCORE,"magazine_score")
 speakers=json.loads(SPEAKERS.read_text(encoding="utf-8"))["records"];records=[]
 for s in speakers:
  slug=s["id"].split(":",1)[1]
  # Layout scoring may evaluate all structural families without asserting a portrait exists.
  doc=gen.generate(slug,"verified")
  ranked=score.rank(doc)
  winner=next(x for x in ranked["candidates"] if x["id"]==ranked["winner"])
  records.append({"speaker":slug,"displayName":s["name"],"family":winner["family"],"candidateId":winner["id"],"geometry":winner["geometry"],"reward":winner["score"]["reward"],"identitySynthesis":False,"assetBinding":"none"})
 return {"schema":"dore.olive-speaker-compositions.v1","authority":"Doré Magazine Engine scoring","deterministic":True,"records":records}
def main():
 OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(build(),ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
if __name__=="__main__":main()
