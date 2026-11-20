#!/usr/bin/env python3
"""Doré research acquisition adapter. Standard library; optional Firecrawl/Scrapling.
Usage: python3 dore_acquire.py https://example.org --output result.json
Never runs downloaded code. Firecrawl and Scrapling are optional, not silently claimed installed.
"""
import argparse, datetime, importlib.util, json, pathlib, shutil, subprocess, sys, urllib.parse
def acquire(url, engine="auto", timeout=30):
    parsed=urllib.parse.urlsplit(url)
    if parsed.scheme!="https" or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError("Only HTTPS URLs without embedded credentials are accepted")
    engines=([engine] if engine!="auto" else ["firecrawl","scrapling","playwright"])
    errors={}
    for name in engines:
        try:
            if name=="firecrawl":
                if not shutil.which("firecrawl"): raise RuntimeError("firecrawl executable unavailable")
                p=subprocess.run(["firecrawl","scrape",url],capture_output=True,text=True,timeout=timeout)
                if p.returncode: raise RuntimeError(p.stderr[:250] or "nonzero exit")
                content=p.stdout
            elif name=="scrapling":
                if not importlib.util.find_spec("scrapling"): raise RuntimeError("scrapling package unavailable")
                from scrapling.fetchers import Fetcher
                page=Fetcher.get(url,timeout=timeout)
                content=str(page.html_content)
            elif name=="playwright":
                if not importlib.util.find_spec("playwright"): raise RuntimeError("playwright package unavailable")
                from playwright.sync_api import sync_playwright
                with sync_playwright() as p:
                    browser=p.chromium.launch(headless=True)
                    try:
                        page=browser.new_page()
                        page.goto(url,wait_until="domcontentloaded",timeout=timeout*1000)
                        content=page.content()
                    finally: browser.close()
            else: raise ValueError("unknown engine")
            if not content.strip(): raise RuntimeError("empty response")
            return {"url":url,"retrieved_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"engine":name,"content":content,"license_status":"unverified","status":"retrieved","errors":errors}
        except Exception as e: errors[name]=str(e)[:350]
    return {"url":url,"status":"unavailable","errors":errors,"license_status":"unverified"}
def main():
    p=argparse.ArgumentParser()
    p.add_argument("url")
    p.add_argument("--engine",choices=["auto","firecrawl","scrapling","playwright"],default="auto")
    p.add_argument("--output",required=True)
    p.add_argument("--timeout",type=int,default=30)
    a=p.parse_args()
    result=acquire(a.url,a.engine,a.timeout)
    target=pathlib.Path(a.output);target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps({"status":result["status"],"engine":result.get("engine"),"errors":result.get("errors")},ensure_ascii=False))
    return 0 if result["status"]=="retrieved" else 2
if __name__=="__main__":sys.exit(main())
