#!/usr/bin/env python3
"""Build a publication-safe review of Doré compositions with verified photo binding.

Review only. Never infer image rights, never synthesize a face, never overwrite
production Olive Mountain assets.
"""
import html
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from olive_gold_geometry import assign, GOLD, OLIVE, PAPER

SPEAKERS = ROOT / "data/westside-core/entities/sermon-speakers.v1.json"
REGISTRY = ROOT / "static/dore-design/runtime/olive-verified-portraits.v1.json"
OUTPUT = ROOT / "static/dore-design/magazine-proof/olive-speakers/verified-composition-review.html"

def verified_assets(registry):
    result = {}
    for record in registry.get("records", []):
        slug = record.get("speaker")
        if not slug or slug in result:
            raise ValueError("Missing or duplicated speaker in portrait registry")
        if not all(record.get(k) is True for k in ("verified", "licenseVerified", "identityVerified")):
            raise ValueError("Unverified portrait: " + slug)
        if not all(isinstance(record.get(k), str) and record[k].strip() for k in ("source", "license", "identityEvidence", "url")):
            raise ValueError("Missing provenance: " + slug)
        url = record["url"]
        if not url.startswith("/") or url.startswith("//") or ".." in url or "?" in url:
            raise ValueError("Unsafe portrait path: " + slug)
        path = ROOT / "static" / url.lstrip("/")
        if path.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp", ".avif"} or not path.is_file():
            raise ValueError("Portrait asset missing or invalid: " + slug)
        result[slug] = url
    return result

def render(speakers, portraits):
    slugs = [r["id"].split(":",1)[1] for r in speakers]
    geometries = assign(slugs)
    figures = []
    for n, (speaker, g) in enumerate(zip(speakers, geometries), 1):
        name = html.escape(speaker["name"])
        slug = g["speaker"]
        image = portraits.get(slug)
        photo = (f'<img class="portrait" src="{html.escape(image, quote=True)}" alt="{name} 已驗證肖像" loading="lazy">'
                 if image else '<div class="empty" aria-label="肖像尚未驗證">PORTRAIT NOT VERIFIED</div>')
        figures.append(f"""<figure><div class="cover">
          <svg class="geometry" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true"><path d="{g['goldPath']}" fill="{GOLD}"/></svg>
          {photo}<div class="name">{name}</div>
          <div class="index">{n:02d} / {html.escape(g['identity'])}</div></div>
          <figcaption>{html.escape(slug)} · {"verified image" if image else "typographic fallback"}</figcaption></figure>""")
    return f"""<!doctype html><html lang="zh-Hant"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
    <title>Doré Olive Mountain · Verified Composition Review</title>
    <style>*{{box-sizing:border-box}}body{{margin:0;padding:clamp(20px,4vw,64px);background:{PAPER};color:{OLIVE};font-family:system-ui,sans-serif}}
    h1{{font-size:clamp(24px,4vw,48px);font-weight:300}}p{{max-width:70ch;line-height:1.6}}
    main{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:24px}}figure{{margin:0;min-width:0}}
    .cover{{aspect-ratio:3/4;position:relative;overflow:hidden;background:{PAPER};border:1px solid #dcdccf}}
    .geometry{{position:absolute;inset:0;width:100%;height:100%}}.portrait{{position:absolute;inset:12% 0 0 22%;width:78%;height:88%;object-fit:contain;object-position:bottom right}}
    .empty{{position:absolute;top:48%;left:12%;font-size:clamp(8px,1vw,12px);letter-spacing:.12em;opacity:.55}}
    .name{{position:absolute;left:7%;top:7%;font-size:clamp(17px,2vw,30px);font-weight:300}}
    .index{{position:absolute;left:7%;bottom:6%;font-size:10px;letter-spacing:.08em}}
    figcaption{{font-size:11px;padding:9px 0;overflow-wrap:anywhere}}
    @media(max-width:700px){{main{{grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}}}}
    </style><h1>OLIVE MOUNTAIN / Verified Composition</h1>
    <p>Editorial proof only. Gold geometry is abstract; portraits appear only when local assets and provenance pass verification.
    This is not a published cover or a substitute for human art direction.</p><main>{''.join(figures)}</main></html>"""

def build():
    speakers = json.loads(SPEAKERS.read_text(encoding="utf-8"))["records"]
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    if registry.get("schema") != "dore.olive-verified-portraits.v1":
        raise ValueError("Unexpected registry schema")
    assets = verified_assets(registry)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(render(speakers, assets), encoding="utf-8")
    return {"speakers": len(speakers), "verifiedPortraits": len(assets), "fallbacks": len(speakers)-len(assets)}

if __name__ == "__main__":
    print(json.dumps(build(), ensure_ascii=False))
