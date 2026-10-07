#!/usr/bin/env python3
"""Generate deterministic magazine candidates from evidence plus human preference."""
import argparse,hashlib,importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];PROFILE=ROOT/"static/dore-design/magazine-profile.olive-speaker.v1.json";SPEAKERS=ROOT/"data/westside-core/entities/sermon-speakers.v1.json";PREFERENCES=ROOT/"static/dore-design/magazine-preferences.v1.json"
spec=importlib.util.spec_from_file_location("precedents",ROOT/"scripts/retrieve_editorial_precedents.py");precedents=importlib.util.module_from_spec(spec);spec.loader.exec_module(precedents)
GEOMETRY={"full-bleed":{"image":[0,0,100,100],"type":[7,66,52,26]},"asymmetric-split":{"image":[44,0,56,100],"type":[6,12,34,72]},"negative-space":{"image":[56,14,36,72],"type":[7,12,39,54]},"portrait-inset":{"image":[52,18,38,62],"type":[7,14,38,64]},"extreme-crop":{"image":[30,0,70,100],"type":[6,69,54,22]},"typographic-no-portrait":{"image":None,"type":[7,16,86,68]}}
def load(p):return json.loads(p.read_text(encoding="utf-8"))
def speaker(slug):
 for x in load(SPEAKERS)["records"]:
  if x["id"]==f"speaker:{slug}":return x
 raise ValueError(f"unknown speaker: {slug}")
def evidence_mutate(base,tokens):
 im=list(base["image"]) if base["image"] else None;ty=list(base["type"]);ops=[]
 if "asymmetrical hierarchy" in tokens:ty=[max(3,ty[0]-3),ty[1],min(90,ty[2]+5),ty[3]];ops.append("asymmetrical hierarchy")
 if "deliberate negative space" in tokens:ty=[ty[0],ty[1],max(24,ty[2]-8),max(28,ty[3]-10)];ops.append("deliberate negative space")
 if im and "precise crop" in tokens:im=[im[0]+3,im[1]+2,max(20,im[2]-6),max(30,im[3]-4)];ops.append("precise crop")
 return {"image":im,"type":ty},ops
def preference(slug,family):
 try:rows=load(PREFERENCES)["records"]
 except FileNotFoundError:return {}
 out={}
 for r in rows:
  if r.get("surface")=="OliveMountain" and r.get("selectedFamily")==family and r.get("speaker") in (slug,None):
   out.update(r.get("corrections",{}))
 return out
def pref_mutate(g,c):
 im=list(g["image"]) if g["image"] else None;ty=list(g["type"]);ops=[]
 def num(k,default=0):
  try:return float(c.get(k,default))
  except:return default
 ns=num("negative_space");ps=num("portrait_scale");ims=num("image_scale");ts=num("type_scale")
 if ns:ty[2]=max(18,min(92,ty[2]-ns*6));ty[3]=max(20,min(90,ty[3]-ns*5));ops.append(f"negative_space:{ns:g}")
 scale=ps or ims
 if im and scale:
  factor=max(.55,min(1.45,1+scale*.1));nw,nh=im[2]*factor,im[3]*factor;im=[im[0]+(im[2]-nw)/2,im[1]+(im[3]-nh)/2,nw,nh];ops.append(f"image_scale:{scale:g}")
 if ts:
  factor=max(.7,min(1.3,1+ts*.08));ty[2]=max(18,min(94,ty[2]*factor));ty[3]=max(20,min(94,ty[3]*factor));ops.append(f"type_scale:{ts:g}")
 if c.get("name_alignment") in ("left","center","right"):ops.append("name_alignment:"+c["name_alignment"])
 return {"image":[round(x,2) for x in im] if im else None,"type":[round(x,2) for x in ty]},ops
def generate(slug,portrait_state):
 p=load(PROFILE);s=speaker(slug);out=[]
 for family in p["candidateFamilies"]:
  if family!="typographic-no-portrait" and portrait_state=="missing":continue
  refs=precedents.retrieve(family);tokens=sorted({t for r in refs for t in r["matchedTokens"]});g,eops=evidence_mutate(GEOMETRY[family],tokens);corr=preference(slug,family);g,pops=pref_mutate(g,corr)
  seed=hashlib.sha256(f"{p['id']}:{slug}:{family}:{json.dumps(corr,sort_keys=True)}:v3".encode()).hexdigest()[:12]
  out.append({"id":f"{slug}-{family}-{seed}","family":family,"seed":seed,"geometry":{"unit":"percent",**g},"geometryAuthority":{"mode":"evidence+preference","operations":eops},"preferenceAuthority":{"corrections":corr,"operations":pops},"content":{"speaker":slug,"displayName":s["name"]},"assetPolicy":{"portrait":portrait_state,"identitySynthesis":False},"precedents":{"evidenceIds":[r["id"] for r in refs],"matchedTokens":tokens,"items":refs},"scoreState":"pending","renderState":"structured-candidate"})
 return {"schema":"dore.magazine-candidates.v3","profile":p["id"],"speaker":slug,"deterministic":True,"candidateCount":len(out),"candidates":out}
def main():
 a=argparse.ArgumentParser();a.add_argument("--speaker",required=True);a.add_argument("--portrait-state",choices=["verified","missing"],default="missing");a.add_argument("--output");x=a.parse_args()
 try:out=generate(x.speaker,x.portrait_state)
 except (ValueError,FileNotFoundError,json.JSONDecodeError) as e:print(f"BLOCKED: {e}");return 2
 payload=json.dumps(out,ensure_ascii=False,indent=2)
 if x.output:Path(x.output).write_text(payload+"\n",encoding="utf-8")
 else:print(payload)
 return 0
if __name__=="__main__":raise SystemExit(main())
