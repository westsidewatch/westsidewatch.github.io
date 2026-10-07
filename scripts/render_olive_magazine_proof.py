#!/usr/bin/env python3
"""Render evidence-driven Olive speaker magazine proofs."""
import argparse,html,importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];SPEAKERS=ROOT/"data/westside-core/entities/sermon-speakers.v1.json";DEFAULT=ROOT/"static/dore-design/magazine-proof/olive-speakers/index.html"
def module(name,path):
 s=importlib.util.spec_from_file_location(name,ROOT/path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
mg=module("mg",Path("scripts/generate_magazine_candidates.py"));ms=module("ms",Path("scripts/score_magazine_candidates.py"))
def records():return json.loads(SPEAKERS.read_text(encoding="utf-8"))["records"]
def rect(r):
 return "" if not r else f"left:{r[0]}%;top:{r[1]}%;width:{r[2]}%;height:{r[3]}%"
def render():
 cards=[]
 for i,s in enumerate(records(),1):
  slug=s["id"].split(":",1)[1];c=ms.rank(mg.generate(slug,"missing"))["candidates"][0];g=c["geometry"];alias=(s.get("aliases") or ["Speaker / Archive"])[0]
  refs=c.get("precedents",{});lineage=" · ".join(refs.get("evidenceIds",[])[:2]) or "NO PRECEDENT";ops=" / ".join(c.get("geometryAuthority",{}).get("operations",[])) or "BASE GEOMETRY"
  image=f'<div class="image-field" style="{rect(g.get("image"))}">VERIFIED PORTRAIT FIELD</div>' if g.get("image") else ""
  cards.append(f'''<article class="cover" data-candidate="{html.escape(c["id"])}"><span class="folio">WESTSIDE WATCH · {i:02d}</span><span class="score">RANK {c["rank"]} · {c["score"]["reward"]}</span>{image}<div class="type" style="{rect(g["type"])}"><h2>{html.escape(s["name"])}</h2><div class="latin">{html.escape(alias)}</div><p>OLIVE MOUNTAIN / SPEAKER ARCHIVE</p></div><div class="lineage">{html.escape(lineage)}<br>{html.escape(ops)}</div></article>''')
 return '''<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Doré Evidence Geometry Proof</title><style>
:root{--olive:#46543f;--paper:#f5f6f1;--ink:#183020}*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font-family:"Noto Serif TC",serif}.head{padding:30px 5vw 18px;border-bottom:1px solid #aab2a7;display:flex;justify-content:space-between;align-items:end}.head b{font:400 clamp(34px,6vw,82px)/.85 "Cormorant Garamond",serif}.head small{letter-spacing:.15em}.grid{padding:38px 5vw 80px;display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:28px}.cover{aspect-ratio:3/4;background:var(--olive);color:#fff;position:relative;overflow:hidden;box-shadow:0 14px 34px #17231a20}.cover:before{content:"";position:absolute;inset:0;background:linear-gradient(128deg,transparent 0 57%,#fff 57% 57.15%,transparent 57.15%);opacity:.18}.folio,.score{position:absolute;top:5%;font:11px/1 "Cormorant Garamond",serif;letter-spacing:.15em;z-index:3}.folio{left:7%}.score{right:7%;opacity:.7}.type{position:absolute;border-top:1px solid #ffffff80;display:flex;flex-direction:column;justify-content:flex-end;z-index:2}.type h2{font-size:clamp(36px,4.5vw,64px);font-weight:400;line-height:.95;margin:0}.latin{font:italic 21px/1.1 "Cormorant Garamond",serif;margin-top:10px}.type p{font:9px/1.5 "Cormorant Garamond",serif;letter-spacing:.15em;margin:18px 0 0}.image-field{position:absolute;border:1px dashed #ffffff55;background:#ffffff0a;font:9px/1.4 sans-serif;letter-spacing:.12em;padding:10px}.lineage{position:absolute;left:7%;bottom:3.5%;max-width:86%;font:8px/1.45 sans-serif;letter-spacing:.07em;opacity:.58}@media(max-width:640px){.head{align-items:start;gap:20px;flex-direction:column}.grid{grid-template-columns:1fr}}</style></head><body><header class="head"><b>OLIVE MOUNTAIN</b><small>EVIDENCE-DRIVEN GEOMETRY · 12 SPEAKERS</small></header><main class="grid">'''+''.join(cards)+'''</main></body></html>'''
def main():
 p=argparse.ArgumentParser();p.add_argument("--output",default=str(DEFAULT));a=p.parse_args();out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(render(),encoding="utf-8");print(out)
if __name__=="__main__":main()
