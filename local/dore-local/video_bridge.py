#!/usr/bin/env python3
"""Loopback-only HTTP bridge for Doré Video Acquisition."""
from __future__ import annotations
import argparse, json, subprocess, sys
from collections import deque
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
ADAPTER=ROOT/"dore-core"/"tools"/"video_acquisition.py"
ORIGINS={"https://westsidewatch.github.io","http://localhost","http://127.0.0.1"}
CAPTURES=deque(maxlen=100)

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
        if self.path=="/captures": return self._send(200,{"ok":True,"captures":list(CAPTURES)})
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
            p=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True,timeout=3600)
            raw=(p.stdout or p.stderr).strip()
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
