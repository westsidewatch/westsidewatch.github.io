#!/usr/bin/env python3
"""Deterministic hard-gate + editorial scoring for Doré magazine candidates."""
import argparse, json\nROOT=Path(__file__).resolve().parents[1]\nPREFERENCES=ROOT/"static/dore-design/magazine-preferences.v1.json"
from pathlib import Path

def rect_ok(r):
 return r is None or (len(r)==4 and r[0]>=0 and r[1]>=0 and r[2]>0 and r[3]>0 and r[0]+r[2]<=100 and r[1]+r[3]<=100)

def overlap(a,b):
 if not a or not b:return 0.0
 x=max(0,min(a[0]+a[2],b[0]+b[2])-max(a[0],b[0]))
 y=max(0,min(a[1]+a[3],b[1]+b[3])-max(a[1],b[1]))
 return x*y

def preference_signal(c):\n try: rows=json.loads(PREFERENCES.read_text(encoding="utf-8")).get("records",[])\n except FileNotFoundError:return 50.0\n family=c["family"];speaker=c.get("content",{}).get("speaker");wins=losses=0\n for r in rows:\n  if r.get("surface")!="OliveMountain":continue\n  weight=2 if r.get("speaker")==speaker else 1\n  if r.get("selectedFamily")==family:wins+=weight\n  if family in r.get("rejectedFamilies",[]):losses+=weight\n return max(0.0,min(100.0,50.0+(wins-losses)*10.0))\n\ndef score(c):
 g=c["geometry"]; im=g.get("image"); ty=g["type"]; family=c["family"]
 hard={"bounds":rect_ok(im) and rect_ok(ty),"typeArea":ty[2]*ty[3]>=700,
       "portraitPolicy":not (c["assetPolicy"]["portrait"]=="missing" and im is not None)}
 hard_pass=all(hard.values())
 ov=overlap(im,ty)
 type_area=ty[2]*ty[3]
 whitespace=max(0,10000-(0 if im is None else im[2]*im[3])-type_area+ov)
 # Transparent, deterministic proxies; later preference learning may replace weights.
 editorial={
  "hierarchy":round(min(100,45+type_area/45),1),
  "negativeSpace":round(min(100,35+whitespace/90),1),
  "imageTypeRelation":100.0 if im is None else round(max(0,100-min(70,ov/45)),1),
  "distinctiveness":{"full-bleed":76,"asymmetric-split":91,"negative-space":94,"portrait-inset":84,"extreme-crop":88,"typographic-no-portrait":90}.get(family,70)
 }
 reward=round(sum(editorial.values())/len(editorial),1) if hard_pass else 0.0
 return {**c,"scoreState":"scored","score":{"hard":hard,"hardPass":hard_pass,"editorial":editorial,"reward":reward}}

def rank(doc):
 items=[score(x) for x in doc["candidates"]]
 items.sort(key=lambda x:(x["score"]["hardPass"],x["score"]["reward"]),reverse=True)
 for i,x in enumerate(items,1):x["rank"]=i
 return {**doc,"schema":"dore.magazine-candidates.scored.v1","candidates":items,
         "winner":items[0]["id"] if items and items[0]["score"]["hardPass"] else None}

def main():
 p=argparse.ArgumentParser();p.add_argument("input");p.add_argument("--output");a=p.parse_args()
 out=rank(json.loads(Path(a.input).read_text(encoding="utf-8")))
 payload=json.dumps(out,ensure_ascii=False,indent=2)
 if a.output:Path(a.output).write_text(payload+"\n",encoding="utf-8")
 else:print(payload)
if __name__=="__main__":main()
