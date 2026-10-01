#!/usr/bin/env python3
from __future__ import annotations
import html, json
from pathlib import Path
from calligraphy_open_index import load_index, lookup

TEXT="敬畏耶和華是智慧的開端"
OUT=Path(__file__).resolve().parents[1]/"static/calligraphy/tc001-open.svg"
REPORT=Path(__file__).resolve().parents[1]/"data/calligraphy/tc001-open.json"

def main():
    idx=load_index(); chosen={}; missing=[]
    for ch in TEXT:
        hits=lookup(idx,ch)
        if hits: chosen[ch]=hits[0]
        else: missing.append(ch)
    w,h=900,1500; x=610; y=120; step=112
    els=[f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {w} {h}">', '<rect width="100%" height="100%" fill="#f3efe5"/>']
    for i,ch in enumerate(TEXT):
        hit=chosen.get(ch); yy=y+i*step
        if hit:
            u=html.escape(hit["assetUrl"],quote=True)
            els.append(f'<image href="{u}" x="{x}" y="{yy}" width="150" height="150" preserveAspectRatio="xMidYMid meet"/>')
        else:
            els.append(f'<text x="{x+75}" y="{yy+100}" text-anchor="middle" font-size="92">{html.escape(ch)}</text>')
    els.append('</svg>')
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text('\n'.join(els)+'\n',encoding='utf-8')
    REPORT.parent.mkdir(parents=True,exist_ok=True); REPORT.write_text(json.dumps({"text":TEXT,"chosen":chosen,"missing":missing,"coverage":f"{len(chosen)}/{len(TEXT)}"},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({"output":str(OUT),"coverage":f"{len(chosen)}/{len(TEXT)}","missing":missing},ensure_ascii=False))
if __name__=='__main__': main()
