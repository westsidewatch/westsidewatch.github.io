#!/usr/bin/env python3
"""Build a review-only twelve-cover contact sheet from Doré geometry metadata.

No portrait synthesis, no publication overwrite, no simulated biographical motif.
"""
import html
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from olive_gold_geometry import assign, PAPER, GOLD, OLIVE

SPEAKERS = ROOT / "data/westside-core/entities/sermon-speakers.v1.json"
OUTPUT = ROOT / "static/dore-design/magazine-proof/olive-speakers/geometry-diversity.html"

def build():
    speakers = json.loads(SPEAKERS.read_text(encoding="utf-8"))["records"]
    slugs = [r["id"].split(":", 1)[1] for r in speakers]
    geometry = assign(slugs)
    tiles = []
    for number, (speaker, g) in enumerate(zip(speakers, geometry), 1):
        label = html.escape(speaker["name"])
        slug = html.escape(g["speaker"])
        identity = html.escape(g["identity"])
        # Vector art is deliberately abstract; portrait zone is a guide, not a fake portrait.
        tiles.append(f"""<figure><div class="art">
          <svg viewBox="0 0 100 133.333" aria-label="{identity} abstract geometry">
            <rect width="100" height="133.333" fill="{PAPER}"/>
            <g transform="scale(1 1.33333)"><path d="{g['goldPath']}" fill="{GOLD}"/></g>
            <path d="M7 119 H38" stroke="{OLIVE}" stroke-width=".5" opacity=".65"/>
          </svg>
          <span class="placeholder">PORTRAIT NOT RENDERED</span>
        </div><figcaption><strong>{number:02d} {label}</strong><small>{slug} / {identity}</small></figcaption></figure>""")
    page = f"""<!doctype html><html lang="zh-Hant"><meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Olive Mountain · Geometry Diversity Review</title>
    <style>
    :root{{--paper:{PAPER};--olive:{OLIVE};--gold:{GOLD}}}
    *{{box-sizing:border-box}}body{{margin:0;padding:clamp(18px,4vw,70px);background:var(--paper);color:var(--olive);font-family:system-ui,sans-serif}}
    h1{{font-size:clamp(24px,4vw,48px);font-weight:300;margin:0 0 12px}}p{{max-width:70ch;line-height:1.65}}
    main{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:clamp(12px,2vw,30px);margin-top:32px}}
    figure{{margin:0;min-width:0}}.art{{aspect-ratio:3/4;position:relative;border:1px solid #e5e5db;overflow:hidden}}
    svg{{display:block;width:100%;height:100%}}.placeholder{{position:absolute;bottom:12%;left:8%;font-size:clamp(7px,.75vw,11px);letter-spacing:.1em;opacity:.55}}
    figcaption{{display:grid;gap:4px;padding:10px 0 16px}}strong{{font-size:15px;font-weight:400}}small{{font-size:11px;opacity:.8;overflow-wrap:anywhere}}
    @media(max-width:700px){{main{{grid-template-columns:repeat(2,minmax(0,1fr))}}}}
    </style><h1>Olive Mountain / Geometry Review</h1>
    <p>Review-only geometry silhouettes. No speaker likeness or biography is asserted.
    This page does not replace published portraits. Evaluate silhouettes and spacing
    at thumbnail size before selecting artwork compositions.</p>
    <main>{''.join(tiles)}</main></html>"""
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(page, encoding="utf-8")
    return OUTPUT

if __name__ == "__main__":
    print(build())
