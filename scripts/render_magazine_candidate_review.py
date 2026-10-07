#!/usr/bin/env python3
"""Render six ranked editorial proposals for one Olive speaker."""
import argparse,html,importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];DEFAULT=ROOT/"static/dore-design/magazine-proof/olive-speaker-candidates/index.html"
def mod(n,p):
 s=importlib.util.spec_from_file_location(n,ROOT/p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
mg=mod("mgc",Path("scripts/generate_magazine_candidates.py"));ms=mod("msc",Path("scripts/score_magazine_candidates.py"))
def rect(r):return "" if not r else f"left:{r[0]}%;top:{r[1]}%;width:{r[2]}%;height:{r[3]}%"
def render(slug="david-pawson"):
 sp=mg.speaker(slug);alias=(sp.get("aliases") or ["Speaker / Archive"])[0];doc=ms.rank(mg.generate(slug,"verified"));cards=[]
 for c in doc["candidates"]:
  g=c["geometry"];refs=c["precedents"];ops=" / ".join(c["geometryAuthority"]["operations"]) or "BASE";hard="PASS" if c["score"]["hardPass"] else "BLOCK"
  image=f'<div class="image" style="{rect(g.get("image"))}"><span>VERIFIED PORTRAIT ASSET</span></div>' if g.get("image") else ""
  cards.append(f'''<section class="proposal"><div class="label">#{c["rank"]} · {html.escape(c["family"])} <b>{c["score"]["reward"]}</b> · {hard}</div><article class="cover">{image}<div class="type" style="{rect(g["type"])}"><h2>{html.escape(sp["name"])}</h2><i>{html.escape(alias)}</i><p>OLIVE MOUNTAIN / SPEAKER</p></div></article><div class="evidence">{html.escape(" · ".join(refs["evidenceIds"][:3]))}<br>{html.escape(ops)}</div></section>''')
 return '''<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Doré Candidate Review</title><style>:root{--o:#46543f;--p:#f5f6f1;--i:#183020}*{box-sizing:border-box}body{margin:0;background:var(--p);color:var(--i);font-family:"Noto Serif TC",serif}header{padding:30px 5vw 20px;border-bottom:1px solid #aab2a7}header h1{font:400 clamp(38px,6vw,78px)/.9 "Cormorant Garamond",serif;margin:0}header p{font-size:11px;letter-spacing:.14em}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:34px;padding:38px 5vw 80px}.proposal{min-width:0}.label{font:11px/1.4 sans-serif;letter-spacing:.08em;margin-bottom:9px}.label b{float:right}.cover{aspect-ratio:3/4;background:var(--o);color:white;position:relative;overflow:hidden;box-shadow:0 12px 28px #17231a1f}.image{position:absolute;border:1px dashed #ffffff70;background:#ffffff0b;display:grid;place-items:center}.image span{font:9px/1.4 sans-serif;letter-spacing:.1em;opacity:.65}.type{position:absolute;border-top:1px solid #ffffff8a;display:flex;flex-direction:column;justify-content:flex-end}.type h2{font-size:clamp(36px,4vw,62px);font-weight:400;line-height:.95;margin:0}.type i{font:italic 21px/1.1 "Cormorant Garamond",serif;margin-top:10px}.type p{font:9px/1.4 sans-serif;letter-spacing:.14em}.evidence{font:9px/1.5 sans-serif;letter-spacing:.04em;margin-top:9px;opacity:.7}</style></head><body><header><h1>DORÉ / EDITORIAL REVIEW</h1><p>SIX PROPOSALS · EVIDENCE → GEOMETRY → SCORE → RANK</p></header><main class="grid">'''+''.join(cards)+'''</main></body></html>'''
def main():
 a=argparse.ArgumentParser();a.add_argument("--speaker",default="david-pawson");a.add_argument("--output",default=str(DEFAULT));x=a.parse_args();o=Path(x.output);o.parent.mkdir(parents=True,exist_ok=True);o.write_text(render(x.speaker),encoding="utf-8");print(o)
if __name__=="__main__":main()
