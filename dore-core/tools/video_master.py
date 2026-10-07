#!/usr/bin/env python3
"""Doré Video Master v0.2 — local diagnosis, restoration and web renditions."""
from __future__ import annotations
import argparse,json,shutil,subprocess,tempfile
from pathlib import Path

def exe(name,*alts):
    for n in (name,*alts):
        p=shutil.which(n)
        if p:return p
    raise RuntimeError(f"{name} not found")

def probe(path):
    p=Path(path).expanduser().resolve()
    raw=subprocess.check_output([exe("ffprobe"),"-v","error","-select_streams","v:0","-show_entries","stream=width,height,avg_frame_rate,bit_rate,codec_name,pix_fmt","-show_entries","format=bit_rate,duration","-of","json",str(p)],text=True)
    d=json.loads(raw);s=(d.get("streams") or [{}])[0];fmt=d.get("format") or {}
    w=int(s.get("width") or 0);h=int(s.get("height") or 0);br=int(s.get("bit_rate") or fmt.get("bit_rate") or 0)
    tier="restore-upscale" if h<720 else "upscale" if h<1080 else "compression-repair" if br and br<3500000 else "web-master"
    target_h=1440 if h>=720 else 1080;target_w=round(target_h*w/h/2)*2 if h else 0
    return {"schema":"dore.video-master.v0.2","source":str(p),"width":w,"height":h,"bit_rate":br,"codec":s.get("codec_name"),"pixel_format":s.get("pix_fmt"),"duration":fmt.get("duration"),"class":tier,"recommended":{"target_width":target_w,"target_height":target_h,"ai_upscale":tier in {"restore-upscale","upscale"},"denoise":tier in {"restore-upscale","compression-repair"},"web_renditions":[720,1080,1440] if target_h>=1440 else [720,1080]}}

def run(cmd): subprocess.run(cmd,check=True)

def restore(src,out):
    info=probe(src); src=Path(src).expanduser().resolve(); out=Path(out).expanduser().resolve(); out.mkdir(parents=True,exist_ok=True)
    ff=exe("ffmpeg"); master=out/(src.stem+"-master.mp4")
    if info["recommended"]["ai_upscale"]:
        ai=exe("realesrgan-ncnn-vulkan","realesrgan-ncnn-vulkan.exe")
        with tempfile.TemporaryDirectory(prefix="dore-video-") as td:
            td=Path(td); frames=td/"frames"; up=td/"up";frames.mkdir();up.mkdir()
            run([ff,"-y","-i",str(src),"-vsync","0",str(frames/"%08d.png")])
            run([ai,"-i",str(frames),"-o",str(up),"-n","realesr-general-x4v3","-s","2","-f","png"])
            vf=f"scale=-2:{info['recommended']['target_height']}:flags=lanczos"
            run([ff,"-y","-framerate","30","-i",str(up/"%08d.png"),"-i",str(src),"-map","0:v:0","-map","1:a?","-vf",vf,"-c:v","libx264","-crf","16","-preset","slow","-c:a","aac","-b:a","192k","-shortest",str(master)])
    else:
        vf="hqdn3d=1.0:1.0:3:3,scale=-2:%d:flags=lanczos"%info["recommended"]["target_height"] if info["recommended"]["denoise"] else "scale=-2:%d:flags=lanczos"%info["recommended"]["target_height"]
        run([ff,"-y","-i",str(src),"-vf",vf,"-c:v","libx264","-crf","16","-preset","slow","-c:a","aac","-b:a","192k",str(master)])
    rend=[]
    for h in info["recommended"]["web_renditions"]:
        if h>info["recommended"]["target_height"]:continue
        dst=out/f"{src.stem}-{h}p.mp4";run([ff,"-y","-i",str(master),"-vf",f"scale=-2:{h}:flags=lanczos","-c:v","libx264","-crf","20","-preset","slow","-movflags","+faststart","-c:a","aac","-b:a","160k",str(dst)]);rend.append(str(dst))
    return {"ok":True,"master":str(master),"renditions":rend,"diagnosis":info}

def main():
    ap=argparse.ArgumentParser();sub=ap.add_subparsers(dest="cmd",required=True)
    p=sub.add_parser("probe");p.add_argument("file")
    p=sub.add_parser("restore");p.add_argument("file");p.add_argument("--output",default=str(Path.home()/"Desktop"/"Dore-Video-Master"))
    a=ap.parse_args();print(json.dumps(probe(a.file) if a.cmd=="probe" else restore(a.file,a.output),ensure_ascii=False,indent=2))
if __name__=="__main__":
    try:main()
    except (RuntimeError,subprocess.CalledProcessError) as e:raise SystemExit(str(e))
