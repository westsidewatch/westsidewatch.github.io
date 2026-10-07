#!/usr/bin/env python3
"""Doré Video Master v0.1 — local video quality diagnosis and web-master planning."""
from __future__ import annotations
import argparse,json,shutil,subprocess
from pathlib import Path

def exe(name):
    p=shutil.which(name)
    if not p: raise RuntimeError(f"{name} not found")
    return p

def probe(path):
    p=Path(path).expanduser().resolve()
    raw=subprocess.check_output([exe("ffprobe"),"-v","error","-select_streams","v:0","-show_entries","stream=width,height,avg_frame_rate,bit_rate,codec_name,pix_fmt","-show_entries","format=bit_rate,duration","-of","json",str(p)],text=True)
    d=json.loads(raw); s=(d.get("streams") or [{}])[0]; f=d.get("format") or {}
    w=int(s.get("width") or 0); h=int(s.get("height") or 0); br=int(s.get("bit_rate") or f.get("bit_rate") or 0)
    if h<720: tier="restore-upscale"
    elif h<1080: tier="upscale"
    elif br and br<3_500_000: tier="compression-repair"
    else: tier="web-master"
    target_h=1440 if h>=720 else 1080
    target_w=round(target_h*w/h/2)*2 if h else 0
    return {"schema":"dore.video-master.v0.1","source":str(p),"width":w,"height":h,"bit_rate":br,"codec":s.get("codec_name"),"pixel_format":s.get("pix_fmt"),"duration":f.get("duration"),"class":tier,"recommended":{"target_width":target_w,"target_height":target_h,"ai_upscale":tier in {"restore-upscale","upscale"},"denoise":tier in {"restore-upscale","compression-repair"},"web_renditions":[{"height":720},{"height":1080},{"height":1440}] if target_h>=1440 else [{"height":720},{"height":1080}]}}

def main():
    ap=argparse.ArgumentParser(); sub=ap.add_subparsers(dest="cmd",required=True); p=sub.add_parser("probe"); p.add_argument("file"); a=ap.parse_args()
    print(json.dumps(probe(a.file),ensure_ascii=False,indent=2))
if __name__=="__main__":
    try: main()
    except RuntimeError as e: raise SystemExit(str(e))
