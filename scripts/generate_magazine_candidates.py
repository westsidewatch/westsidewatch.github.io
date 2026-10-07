#!/usr/bin/env python3
"""Generate deterministic structured magazine-layout candidates for Doré."""
import argparse, hashlib, importlib.util, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PROFILE=ROOT/"static/dore-design/magazine-profile.olive-speaker.v1.json"
SPEAKERS=ROOT/"data/westside-core/entities/sermon-speakers.v1.json"\nPRECEDENT_SCRIPT=ROOT/"scripts/retrieve_editorial_precedents.py"\nspec=importlib.util.spec_from_file_location("precedents",PRECEDENT_SCRIPT)\nprecedents=importlib.util.module_from_spec(spec);spec.loader.exec_module(precedents)\n\nGEOMETRY={
 "full-bleed":{"image":[0,0,100,100],"type":[7,66,52,26]},
 "asymmetric-split":{"image":[44,0,56,100],"type":[6,12,34,72]},
 "negative-space":{"image":[56,14,36,72],"type":[7,12,39,54]},
 "portrait-inset":{"image":[52,18,38,62],"type":[7,14,38,64]},
 "extreme-crop":{"image":[30,0,70,100],"type":[6,69,54,22]},
 "typographic-no-portrait":{"image":None,"type":[7,16,86,68]}
}

def load(p): return json.loads(p.read_text(encoding="utf-8"))

def speaker(slug):
 db=load(SPEAKERS)
 items=db.get("records") or db.get("items") or db.get("speakers") or db
 if isinstance(items,dict): items=list(items.values())
 for x in items:
  if x.get("id")==f"speaker:{slug}" or x.get("slug")==slug: return x
 raise ValueError(f"unknown speaker: {slug}")

def mutate(base,tokens):\n im=list(base["image"]) if base["image"] else None; ty=list(base["type"]); ops=[]\n if "asymmetrical hierarchy" in tokens: ty=[max(3,ty[0]-3),ty[1],min(90,ty[2]+5),ty[3]]; ops.append("asymmetrical hierarchy")\n if "deliberate negative space" in tokens: ty=[ty[0],ty[1],max(24,ty[2]-8),max(28,ty[3]-10)]; ops.append("deliberate negative space")\n if im and "precise crop" in tokens: im=[im[0]+3,im[1]+2,max(20,im[2]-6),max(30,im[3]-4)]; ops.append("precise crop")\n return {"image":im,"type":ty},ops\n\ndef generate(slug, portrait_state):
 p=load(PROFILE); s=speaker(slug)
 name=s.get("displayName") or s.get("name") or slug
 families=p["candidateFamilies"]
 out=[]
 for family in families:
  if family!="typographic-no-portrait" and portrait_state=="missing": continue
  g=GEOMETRY[family]
  seed=hashlib.sha256(f"{p['id']}:{slug}:{family}:v1".encode()).hexdigest()[:12]
  out.append({"id":f"{slug}-{family}-{seed}","family":family,"seed":seed,
   "geometry":{"unit":"percent","image":g["image"],"type":g["type"]},"geometryAuthority":{"mode":"precedent-mutation","operations":ops},
   "content":{"speaker":slug,"displayName":name},
   "assetPolicy":{"portrait":portrait_state,"identitySynthesis":False},"precedents":{"evidenceIds":[r["id"] for r in refs],"matchedTokens":tokens,"items":refs},
   "scoreState":"pending","renderState":"structured-candidate"})
 return {"schema":"dore.magazine-candidates.v1","profile":p["id"],"speaker":slug,
  "deterministic":True,"candidateCount":len(out),"candidates":out}

def main():
 a=argparse.ArgumentParser();a.add_argument("--speaker",required=True)
 a.add_argument("--portrait-state",choices=["verified","missing"],default="missing")
 a.add_argument("--output")
 x=a.parse_args()
 try: out=generate(x.speaker,x.portrait_state)
 except (ValueError,FileNotFoundError,json.JSONDecodeError) as e:
  print(f"BLOCKED: {e}"); return 2
 payload=json.dumps(out,ensure_ascii=False,indent=2)
 if x.output: Path(x.output).write_text(payload+"\n",encoding="utf-8")
 else: print(payload)
 return 0
if __name__=="__main__": raise SystemExit(main())
