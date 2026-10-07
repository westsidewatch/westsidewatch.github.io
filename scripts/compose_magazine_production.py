#!/usr/bin/env python3
"""Deterministic production composer for Doré magazine candidates."""
import html, json

SURFACES={"web-hero":(1600,900),"speaker-card":(900,1200),"mobile":(750,1100),"preview-image":(1200,630)}

def winner(doc):
    wid=doc.get("winner")
    for c in doc.get("candidates",[]):
        if c.get("id")==wid and c.get("score",{}).get("hardPass"): return c
    raise ValueError("no hard-pass magazine winner")

def _box(r):
    return "" if r is None else f"left:{r[0]}%;top:{r[1]}%;width:{r[2]}%;height:{r[3]}%;"

def compose(doc,profile):
    c=winner(doc); g=c["geometry"]; name=html.escape(c["content"]["displayName"]); family=html.escape(c["family"])
    image="" if g.get("image") is None else f'<div class="dore-image" style="{_box(g["image"])}" aria-label="verified source portrait slot"></div>'
    css=".dore-cover{position:relative;overflow:hidden;background:#f5f4ec;color:#183b2b;font-family:serif}.dore-image{position:absolute;background:#dfe7df}.dore-type{position:absolute;display:flex;flex-direction:column;justify-content:flex-end}.dore-name{font-size:clamp(2rem,7vw,7rem);font-weight:400;line-height:.9}.dore-meta{font-size:clamp(.65rem,1.2vw,1rem);letter-spacing:.14em;text-transform:uppercase;margin-top:1rem}"
    body=f'<article class="dore-cover" data-family="{family}" data-candidate="{html.escape(c["id"])}">{image}<div class="dore-type" style="{_box(g["type"])}"><div class="dore-name">{name}</div><div class="dore-meta">Olive Mountain · Westside Watch</div></div></article>'
    return {"schema":"dore.magazine-composition.v1","candidate":c["id"],"family":c["family"],"profile":profile["id"],"css":css,"html":body,"identitySynthesis":False}

def render_variants(composition):
    out={}
    for surface,(w,h) in SURFACES.items():
        out[surface]={"width":w,"height":h,"html":f'<div style="width:{w}px;height:{h}px">{composition["html"]}</div>',"css":composition["css"]+f".dore-cover{{width:{w}px;height:{h}px}}"}
    return out

def preflight(composition,variants):
    checks={"identitySynthesisDisabled":composition.get("identitySynthesis") is False,"hasCandidate":bool(composition.get("candidate")),"hasHtml":bool(composition.get("html")),"hasCss":bool(composition.get("css")),"allSurfaces":set(variants)==set(SURFACES),"blackGoldAbsent":"#000" not in composition.get("css","") and "#CEBD74" not in composition.get("css","")}
    return {"schema":"dore.magazine-preflight.v1","checks":checks,"pass":all(checks.values())}

def produce(scored,profile):
    composition=compose(scored,profile); variants=render_variants(composition); flight=preflight(composition,variants)
    if not flight["pass"]: raise ValueError("magazine production preflight failed")
    return {"schema":"dore.magazine-production.v1","composition":composition,"variants":variants,"preflight":flight}
