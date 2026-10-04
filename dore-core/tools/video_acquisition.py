#!/usr/bin/env python3
"""Doré Video Acquisition Adapter v0.

Local-first adapter over mature open-source download engines.
Contract: probe URL | formats URL | download URL [--format FORMAT] [--output DIR]

Routing:
- normal webpage/media URL -> yt-dlp
- direct HLS/DASH/MSS manifest (.m3u8/.mpd/.ism) -> N_m3u8DL-RE
- yt-dlp failure on a manifest-like URL -> N_m3u8DL-RE

Scope: public or authorized media. DRM bypass is intentionally out of scope.
"""
from __future__ import annotations
import argparse, json, os, re, shutil, subprocess, sys
from pathlib import Path
from urllib.parse import urlparse

MANIFEST_EXTENSIONS=(".m3u8",".mpd",".ism","/manifest")

def run(cmd):
    p=subprocess.run(cmd,text=True,capture_output=True)
    if p.returncode:
        raise RuntimeError((p.stderr or p.stdout).strip())
    return p.stdout

def executable(*names):
    for name in names:
        exe=shutil.which(name)
        if exe: return exe
    return None

def yt_dlp():
    exe=executable("yt-dlp")
    if not exe: raise RuntimeError("yt-dlp not found")
    return exe

def nm3u8():
    exe=executable("N_m3u8DL-RE","N_m3u8DL-RE.exe")
    if not exe: raise RuntimeError("N_m3u8DL-RE not found")
    return exe

def is_manifest(url):
    path=urlparse(url).path.lower()
    return any(path.endswith(x) for x in (".m3u8",".mpd",".ism")) or "/manifest" in path

def yt_probe(url):
    data=json.loads(run([yt_dlp(),"-J","--no-playlist",url]))
    return {"engine":"yt-dlp","id":data.get("id"),"title":data.get("title"),
      "webpage_url":data.get("webpage_url") or url,"duration":data.get("duration"),
      "is_live":data.get("is_live"),"thumbnail":data.get("thumbnail"),
      "subtitles":sorted((data.get("subtitles") or {}).keys()),
      "automatic_captions":sorted((data.get("automatic_captions") or {}).keys()),
      "formats":[{"format_id":f.get("format_id"),"ext":f.get("ext"),"protocol":f.get("protocol"),
        "width":f.get("width"),"height":f.get("height"),"fps":f.get("fps"),
        "vcodec":f.get("vcodec"),"acodec":f.get("acodec")} for f in data.get("formats",[])]}

def manifest_probe(url):
    # N_m3u8DL-RE owns stream parsing; keep probe non-destructive.
    return {"engine":"N_m3u8DL-RE","id":None,"title":None,"webpage_url":url,
      "duration":None,"is_live":None,"thumbnail":None,"subtitles":[],
      "automatic_captions":[],"formats":[],
      "manifest":True,"manifest_type":Path(urlparse(url).path).suffix.lower().lstrip(".") or "manifest"}

def probe(url):
    if is_manifest(url):
        return manifest_probe(url)
    return yt_probe(url)

def download_manifest(url, output):
    Path(output).mkdir(parents=True,exist_ok=True)
    cmd=[nm3u8(),url,"--save-dir",str(Path(output).resolve()),"--auto-select"]
    subprocess.run(cmd,check=True)

def download_yt(url, fmt, output):
    Path(output).mkdir(parents=True,exist_ok=True)
    cmd=[yt_dlp(),"--no-playlist","--write-info-json","--write-thumbnail",
         "--write-subs","--write-auto-subs","--sub-langs","zh.*,en.*",
         "-P",output,"-o","%(title).180B [%(id)s].%(ext)s"]
    cmd += ["-f",fmt or "bv*+ba/b",url]
    subprocess.run(cmd,check=True)

def download(url, fmt, output):
    if is_manifest(url):
        return download_manifest(url,output)
    try:
        return download_yt(url,fmt,output)
    except subprocess.CalledProcessError:
        if is_manifest(url):
            return download_manifest(url,output)
        raise

def main():
    ap=argparse.ArgumentParser()
    sub=ap.add_subparsers(dest="command",required=True)
    for name in ("probe","formats"):
        p=sub.add_parser(name); p.add_argument("url")
    p=sub.add_parser("download"); p.add_argument("url"); p.add_argument("--format")
    p.add_argument("--output",default=os.environ.get("DORE_VIDEO_OUTPUT","downloads"))
    a=ap.parse_args()
    if a.command in ("probe","formats"):
        d=probe(a.url)
        print(json.dumps(d if a.command=="probe" else d["formats"],ensure_ascii=False,indent=2))
    else:
        download(a.url,a.format,a.output)

if __name__=="__main__":
    try: main()
    except (RuntimeError,subprocess.CalledProcessError) as e:
        print(json.dumps({"ok":False,"error":str(e)},ensure_ascii=False),file=sys.stderr); sys.exit(1)
