#!/usr/bin/env python3
import importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SPEAKERS=ROOT/"data/westside-core/entities/sermon-speakers.v1.json"
GEN=ROOT/"scripts/generate_magazine_candidates.py"
SCORE=ROOT/"scripts/score_magazine_candidates.py"
OUT=ROOT/"static/dore-design/runtime/olive-speaker-compositions.v1.json"
COVERS=ROOT/"static/dore-design/runtime/olive-covers"
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
  records.append({"speaker":slug,"displayName":s["name"],"family":winner["family"],"identitySynthesis":False,"assetBinding":"none","candidateId":winner["id"],"geometry":winner["geometry"],"reward":winner["score"]["reward"]})
 return {"schema":"dore.olive-speaker-compositions.v1","authority":"Doré Magazine Engine scoring","deterministic":True,"records":records}
def render_cover(r, number):
 from html import escape
 slug=r["speaker"]
 name=escape(r["displayName"])
 family=r["family"]
 colors=[("#f7fbf8","#1b513a","#d6e8dc"),("#e8f3eb","#174b35","#bfdac8"),("#fff","#225a41","#e1efe5"),("#deede3","#174b35","#c8e1d0")]
 bg,ink,accent=colors[(number-1)%4]
 motifs={
  "negative-space":'<path d="M 480 0 H 900 V 1200 H 340 Z" fill="ACCENT"/>',
  "portrait-inset":'<rect x="540" y="150" width="270" height="850" fill="ACCENT"/>',
  "typographic-no-portrait":'<circle cx="795" cy="290" r="310" fill="ACCENT"/>',
  "asymmetric-split":'<rect x="500" width="400" height="1200" fill="ACCENT"/>',
  "full-bleed":'<path d="M0 810 Q460 240 900 70 V1200 H0Z" fill="ACCENT"/>',
  "extreme-crop":'<circle cx="860" cy="650" r="620" fill="ACCENT"/>'
 }
 motif=motifs.get(family,motifs["typographic-no-portrait"]).replace("ACCENT",accent)
 return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 1200" role="img" aria-label="{name} editorial cover"><rect width="900" height="1200" fill="{bg}"/>{motif}<text x="60" y="85" font-family="Arial,sans-serif" font-size="20" letter-spacing="4" fill="{ink}">WESTSIDE WATCH / OLIVE MOUNTAIN</text><path d="M60 110 H840" stroke="{ink}" stroke-opacity=".4"/><text x="60" y="475" font-family="Arial,Noto Sans TC,sans-serif" font-size="100" fill="{ink}">{name}</text><text x="60" y="545" font-family="Arial,sans-serif" font-size="22" letter-spacing="6" fill="{ink}">SERMON / EDITORIAL</text><text x="60" y="1120" font-family="Georgia,serif" font-size="260" fill="{ink}" fill-opacity=".12">{number:02d}</text><path d="M60 1150 H840" stroke="{ink}" stroke-opacity=".4"/></svg>'
def main():
 OUT.parent.mkdir(parents=True,exist_ok=True)
 COVERS.mkdir(parents=True,exist_ok=True)
 payload=build()
 for number,r in enumerate(payload["records"],1):
  filename=r["speaker"]+".svg"
  (COVERS/filename).write_text(render_cover(r,number),encoding="utf-8")
  r["cover"]="/dore-design/runtime/olive-covers/"+filename
 OUT.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
if __name__=="__main__":main()
