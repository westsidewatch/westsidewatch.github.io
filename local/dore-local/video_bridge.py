#!/usr/bin/env python3
"""Loopback-only HTTP bridge for Doré Video Acquisition."""
from __future__ import annotations
import argparse, json, subprocess, sys, threading, uuid, time, re
from urllib.parse import urljoin
from urllib.request import Request, urlopen
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
ADAPTER=ROOT/"dore-core"/"tools"/"video_acquisition.py"
ORIGINS={"https://westsidewatch.github.io","http://localhost","http://127.0.0.1"}
TASKS={}
TASK_LOCK=threading.Lock()

def hls_total(url):
    if ".m3u8" not in url.lower(): return None
    def read(u):
        req=Request(u,headers={"User-Agent":"Mozilla/5.0 Dore/0.3"})
        with urlopen(req,timeout=15) as r: return r.read(4_000_000).decode("utf-8",errors="replace")
    try:
        text=read(url); lines=[x.strip() for x in text.splitlines() if x.strip()]
        if "#EXT-X-STREAM-INF" not in text:
            return sum(1 for x in lines if not x.startswith("#"))
        variants=[]
        for i,line in enumerate(lines[:-1]):
            if line.startswith("#EXT-X-STREAM-INF"):
                m=re.search(r"BANDWIDTH=(\\d+)",line); bw=int(m.group(1)) if m else 0
                if not lines[i+1].startswith("#"): variants.append((bw,urljoin(url,lines[i+1])))
        totals=[]
        if variants:
            _,video_url=max(variants,key=lambda x:x[0])
            totals.append(hls_total(video_url) or 0)
        for line in lines:
            if line.startswith("#EXT-X-MEDIA") and "TYPE=AUDIO" in line:
                m=re.search(r'URI="([^"]+)"',line)
                if m: totals.append(hls_total(urljoin(url,m.group(1))) or 0)
        return max(totals) if totals else None
    except Exception:
        return None

def segment_progress(root,total=None):
    root=Path(root).expanduser()
    if not root.exists(): return {"segments":0}
    parts=[p for p in root.rglob("*.ts") if not p.name.startswith("._")]
    done=len(parts)
    if total and done > total:
        track_counts={}
        for p in parts:
            track_counts[p.parent]=track_counts.get(p.parent,0)+1
        done=max(track_counts.values(),default=0)
    progress={"segments":done}
    if total:
        progress.update({"total_segments":total,"percent":min(100,round(done*100/total))})
    return progress

def watch_progress(task_id,root,stop,total=None):
    while not stop.wait(1):
        progress=segment_progress(root,total)
        with TASK_LOCK:
            if task_id not in TASKS: return
            TASKS[task_id]["progress"]=progress
            if total and progress.get("percent")==100 and TASKS[task_id].get("status")=="downloading":
                TASKS[task_id]["status"]="merging"

def run_download_task(task_id,cmd,output,total=None):
    with TASK_LOCK: TASKS[task_id]["status"]="downloading"
    stop=threading.Event()
    watcher=threading.Thread(target=watch_progress,args=(task_id,output,stop,total),daemon=True); watcher.start()
    try:
        p=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True,timeout=3600)
        raw=((p.stdout if p.returncode==0 else p.stderr) or p.stdout or p.stderr).strip()
        try: result=json.loads(raw)
        except Exception: result={"raw":raw}
        status="failed"
        if p.returncode==0:
            status="merged" if result.get("merged") else ("downloaded" if result.get("downloaded") else "completed")
        with TASK_LOCK: TASKS[task_id].update({"status":status,"ok":p.returncode==0,"result":result})
    except Exception as e:
        with TASK_LOCK: TASKS[task_id].update({"status":"failed","ok":False,"error":type(e).__name__,"detail":str(e)})
    finally:
        stop.set()
        with TASK_LOCK: TASKS[task_id]["progress"]=segment_progress(output,total)

class H(BaseHTTPRequestHandler):
    def _cors(self):
        o=self.headers.get("Origin","")
        if o in ORIGINS: self.send_header("Access-Control-Allow-Origin",o)
        self.send_header("Vary","Origin")
    def _send(self,code,payload):
        data=json.dumps(payload,ensure_ascii=False).encode()
        self.send_response(code); self.send_header("Content-Type","application/json; charset=utf-8")
        self._cors(); self.send_header("Content-Length",str(len(data))); self.end_headers(); self.wfile.write(data)
    def do_OPTIONS(self):
        self.send_response(204); self._cors(); self.send_header("Access-Control-Allow-Methods","GET,POST,OPTIONS"); self.send_header("Access-Control-Allow-Headers","Content-Type"); self.end_headers()
    def do_GET(self):
        if self.path=="/health": return self._send(200,{"ok":True,"service":"dore-video-bridge","loopback":True})
        if self.path.startswith("/task/"):
            task_id=self.path.split("/",2)[2]
            with TASK_LOCK: task=TASKS.get(task_id)
            return self._send(200,task) if task else self._send(404,{"ok":False,"error":"task_not_found"})
        self._send(404,{"ok":False,"error":"not_found"})
    def do_POST(self):
        op=self.path.strip("/")
        if op not in {"probe","formats","download"}: return self._send(404,{"ok":False,"error":"not_found"})
        try:
            n=int(self.headers.get("Content-Length","0")); body=json.loads(self.rfile.read(n) or b"{}"); url=str(body.get("url","")).strip()
            if not url.startswith(("http://","https://")): return self._send(400,{"ok":False,"error":"public_http_url_required"})
            cmd=[sys.executable,str(ADAPTER),op,url]
            if op=="download":
                if body.get("format"): cmd += ["--format",str(body["format"])]
                if body.get("output"): cmd += ["--output",str(body["output"])]
            if op=="download":
                task_id=uuid.uuid4().hex
                output=str(Path(body.get("output") or Path.home()/"Desktop").expanduser())
                total=hls_total(url)
                progress={"segments":0}; progress.update({"total_segments":total,"percent":0} if total else {})
                with TASK_LOCK: TASKS[task_id]={"task_id":task_id,"status":"queued","ok":True,"output":output,"progress":progress}
                threading.Thread(target=run_download_task,args=(task_id,cmd,output,total),daemon=True).start()
                return self._send(202,{"ok":True,"operation":"download","task_id":task_id,"status":"queued"})
            p=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True,timeout=3600)
            raw=((p.stdout if p.returncode==0 else p.stderr) or p.stdout or p.stderr).strip()
            try: result=json.loads(raw)
            except Exception: result={"raw":raw}
            self._send(200 if p.returncode==0 else 502,{"ok":p.returncode==0,"operation":op,"result":result})
        except Exception as e: self._send(500,{"ok":False,"error":type(e).__name__,"detail":str(e)})
    def log_message(self,fmt,*args): pass

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--port",type=int,default=43127); ns=ap.parse_args()
    server=ThreadingHTTPServer(("127.0.0.1",ns.port),H)
    print(f"Doré Video Bridge: http://127.0.0.1:{ns.port}")
    server.serve_forever()
if __name__=="__main__": main()
