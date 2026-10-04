#!/usr/bin/env python3
"""Doré Video Acquisition Adapter v0.

Local-first adapter over mature open-source download engines.
Contract:
  probe URL
  formats URL
  download URL [--format FORMAT] [--output DIR]

Scope: public or authorized media. DRM bypass is intentionally out of scope.
"""
from __future__ import annotations
import argparse, json, os, shutil, subprocess, sys
from pathlib import Path

def run(cmd):
    p=subprocess.run(cmd,text=True,capture_output=True)
    if p.returncode:
        raise RuntimeError((p.stderr or p.stdout).strip())
    return p.stdout

def yt_dlp():
    exe=shutil.which("yt-dlp")
    if not exe: raise RuntimeError("yt-dlp not found")
    return exe

def probe(url):
    data=json.loads(run([yt_dlp(),"-J","--no-playlist",url]))
    return {"engine":"yt-dlp","id":data.get("id"),"title":data.get("title"),
      "webpage_url":data.get("webpage_url") or url,"duration":data.get("duration"),
      "is_live":data.get("is_live"),"thumbnail":data.get("thumbnail"),
      "subtitles":sorted((data.get("subtitles") or {}).keys()),
      "automatic_captions":sorted((data.get("automatic_captions") or {}).keys()),
      "formats":[{"format_id":f.get("format_id"),"ext":f.get("ext"),"protocol":f.get("protocol"),
        "width":f.get("width"),"height":f.get("height"),"fps":f.get("fps"),
        "vcodec":f.get("vcodec"),"acodec":f.get("acodec")} for f in data.get("formats",[])]}

def download(url, fmt, output):
    Path(output).mkdir(parents=True,exist_ok=True)
    cmd=[yt_dlp(),"--no-playlist","--write-info-json","--write-thumbnail",
         "--write-subs","--write-auto-subs","--sub-langs","zh.*,en.*",
         "-P",output,"-o","%(title).180B [%(id)s].%(ext)s"]
    if fmt: cmd += ["-f",fmt]
    else: cmd += ["-f","bv*+ba/b"]
    cmd.append(url)
    subprocess.run(cmd,check=True)

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
    else: download(a.url,a.format,a.output)

if __name__=="__main__":
    try: main()
    except (RuntimeError,subprocess.CalledProcessError) as e:
        print(json.dumps({"ok":False,"error":str(e)},ensure_ascii=False),file=sys.stderr); sys.exit(1)
