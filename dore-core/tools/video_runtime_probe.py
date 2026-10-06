#!/usr/bin/env python3
"""Experimental Doré-owned runtime media probe. Not wired to production."""
from __future__ import annotations
import argparse, json, sys
from urllib.parse import urlparse

MEDIA_MIME=("application/vnd.apple.mpegurl","application/x-mpegurl","application/dash+xml","application/vnd.ms-sstr+xml")
DRM_MARKERS=("widevine","playready","fairplay","com.widevine","skd://","license")

def media_kind(url, content_type=""):
    u=url.lower(); c=content_type.lower()
    if ".m3u8" in u or "mpegurl" in c: return "hls"
    if ".mpd" in u or "dash+xml" in c: return "dash"
    if ".ism" in u or "/manifest" in u or "ms-sstr" in c: return "mss"
    return None

def probe(url, timeout_ms=15000):
    if urlparse(url).scheme not in ("http","https"): raise ValueError("public_http_url_required")
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return {"ok":False,"error":"playwright_not_installed","install":"python3 -m pip install playwright && python3 -m playwright install chromium"}
    hits=[]
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True)
        context=browser.new_context()
        page=context.new_page()
        def on_response(response):
            try:
                ct=response.headers.get("content-type","")
                kind=media_kind(response.url,ct)
                if not kind: return
                req=response.request
                headers=dict(req.headers)
                blob=json.dumps({"url":response.url,"headers":headers},ensure_ascii=False).lower()
                if any(x in blob for x in DRM_MARKERS): return
                hits.append({"url":response.url,"kind":kind,"content_type":ct,"page_url":page.url,"headers":{k:v for k,v in headers.items() if k.lower() in ("referer","origin","user-agent")}})
            except Exception:
                pass
        page.on("response",on_response)
        page.goto(url,wait_until="domcontentloaded",timeout=timeout_ms)
        page.wait_for_timeout(min(timeout_ms,12000))
        title=page.title()
        browser.close()
    seen=set(); unique=[]
    for h in hits:
        if h["url"] not in seen: seen.add(h["url"]); unique.append(h)
    return {"ok":bool(unique),"engine":"playwright-runtime","title":title,"webpage_url":url,"manifests":unique}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("url"); ap.add_argument("--timeout-ms",type=int,default=15000); ns=ap.parse_args()
    try: print(json.dumps(probe(ns.url,ns.timeout_ms),ensure_ascii=False))
    except Exception as e: print(json.dumps({"ok":False,"error":type(e).__name__,"detail":str(e)},ensure_ascii=False)); sys.exit(1)
if __name__=="__main__": main()
