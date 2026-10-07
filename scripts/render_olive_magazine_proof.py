#!/usr/bin/env python3
"""Render Olive speaker magazine proofs from canonical data and Doré candidates."""
import argparse, html, importlib.util, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SPEAKERS=ROOT/"data/westside-core/entities/sermon-speakers.v1.json"
DEFAULT=ROOT/"static/dore-design/magazine-proof/olive-speakers/index.html"

def module(name,path):
 s=importlib.util.spec_from_file_location(name,ROOT/path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
mg=module("mg",Path("scripts/generate_magazine_candidates.py"))
ms=module("ms",Path("scripts/score_magazine_candidates.py"))

def records():
 return json.loads(SPEAKERS.read_text(encoding="utf-8"))["records"]

def render():
 cards=[]
 for i,s in enumerate(records(),1):
  slug=s["id"].split(":",1)[1]; ranked=ms.rank(mg.generate(slug,"missing")); c=ranked["candidates"][0]
  alias=(s.get("aliases") or ["Speaker / Archive"])[0]
  cards.append(f'''<article class="cover" data-candidate="{html.escape(c["id"])}"><span class="folio">WESTSIDE WATCH · {i:02d}</span><span class="score">RANK {c["rank"]} · {c["score"]["reward"]}</span><div class="type"><h2>{html.escape(s["name"])}</h2><div class="latin">{html.escape(alias)}</div><p>OLIVE MOUNTAIN / SPEAKER ARCHIVE</p></div><div class="meta">{html.escape(slug.upper())}</div></article>''')
 return '''<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Doré Magazine Proof — Olive Speakers</title><style>
:root{--olive:#46543f;--paper:#f5f6f1;--ink:#183020}*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font-family:"Noto Serif TC",serif}.head{padding:30px 5vw 18px;border-bottom:1px solid #aab2a7;display:flex;justify-content:space-between;align-items:end}.head b{font:400 clamp(34px,6vw,82px)/.85 "Cormorant Garamond",serif}.head small{letter-spacing:.15em}.grid{padding:38px 5vw 80px;display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:28px}.cover{aspect-ratio:3/4;background:var(--olive);color:white;position:relative;overflow:hidden;box-shadow:0 14px 34px #17231a20}.cover:before{content:"";position:absolute;inset:0;background:linear-gradient(128deg,transparent 0 57%,#fff 57% 57.15%,transparent 57.15%);opacity:.24}.folio,.score{position:absolute;top:5%;font:11px/1 "Cormorant Garamond",serif;letter-spacing:.15em}.folio{left:7%}.score{right:7%;opacity:.7}.type{position:absolute;left:7%;top:16%;width:86%;height:68%;border-top:1px solid #ffffff80;display:flex;flex-direction:column;justify-content:flex-end}.type h2{font-size:clamp(42px,5vw,70px);font-weight:400;line-height:.95;margin:0}.latin{font:italic 22px/1.1 "Cormorant Garamond",serif;margin-top:12px}.type p{font:10px/1.5 "Cormorant Garamond",serif;letter-spacing:.17em;margin:24px 0 0}.meta{position:absolute;right:6%;bottom:5%;writing-mode:vertical-rl;font:10px/1 "Cormorant Garamond",serif;letter-spacing:.13em}@media(max-width:640px){.head{align-items:start;gap:20px;flex-direction:column}.grid{grid-template-columns:1fr}}</style></head><body><header class="head"><b>OLIVE MOUNTAIN</b><small>DORÉ GENERATED PROOF · 12 SPEAKERS · NO PORTRAIT</small></header><main class="grid">'''+''.join(cards)+'''</main></body></html>'''

def main():
 p=argparse.ArgumentParser();p.add_argument("--output",default=str(DEFAULT));a=p.parse_args()
 out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(render(),encoding="utf-8");print(out)
if __name__=="__main__":main()
