#!/usr/bin/env python3
"""Live local smoke test for Doré Video Bridge using a public GOOD TV HLS."""
from __future__ import annotations
import argparse, json, time
from pathlib import Path
from urllib.request import Request, urlopen

BRIDGE="http://127.0.0.1:43127"
GOODTV_HLS="https://vod.streamingfast.net/hls-vod/video/T405001_0099.m3u8"

def request(path, payload=None):
    data=None if payload is None else json.dumps(payload).encode()
    req=Request(BRIDGE+path,data=data,headers={"Content-Type":"application/json"} if data else {})
    with urlopen(req,timeout=20) as r: return json.loads(r.read().decode())

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",default=str(Path.home()/"Desktop"/"dore-video-smoke"))
    ap.add_argument("--timeout",type=int,default=3600)
    ns=ap.parse_args()
    health=request("/health")
    assert health.get("ok"),health
    start=request("/download",{"url":GOODTV_HLS,"output":ns.output})
    task_id=start["task_id"]
    deadline=time.time()+ns.timeout
    last=None
    while time.time()<deadline:
        task=request("/task/"+task_id)
        p=task.get("progress") or {}
        state=(task.get("status"),p.get("segments"),p.get("total_segments"),p.get("percent"))
        if state!=last:
            print(json.dumps({"task_id":task_id,"status":state[0],"segments":state[1],"total_segments":state[2],"percent":state[3]},ensure_ascii=False))
            last=state
        if task.get("status") in {"merged","downloaded","completed","failed"}:
            if task.get("status")!="merged": raise RuntimeError(json.dumps(task,ensure_ascii=False))
            result=task.get("result") or {}
            media=Path(result.get("file",""))
            if not media.is_file() or media.stat().st_size==0: raise RuntimeError("merged MP4 missing or empty")
            if p.get("total_segments") and p.get("percent")!=100: raise RuntimeError("task merged before progress reached 100%")
            print(json.dumps({"ok":True,"status":"merged","file":str(media),"bytes":media.stat().st_size,"progress":p},ensure_ascii=False))
            return
        time.sleep(1.5)
    raise TimeoutError("Doré Video smoke test timed out")

if __name__=="__main__":
    main()
