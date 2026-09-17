#!/usr/bin/env python3
"""Thin external-page collector for Doré Design Observation.

Owns no daemon or learning authority. It uses an installed Playwright runtime
only as the navigation/render transport, injects the canonical Doré observer,
and emits dore.runtime-design-capture.v1 for the existing A2A admission path.
"""
from __future__ import annotations
import hashlib,json,os,tempfile
from datetime import datetime,timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

SCHEMA='dore.runtime-design-capture.v1'

def _repo()->Path:return Path(os.environ.get('DORE_REPO_ROOT') or Path(__file__).resolve().parents[2]).resolve()
def _allowed(url:str)->bool:
 p=urlparse(url);host=(p.hostname or '').lower();return p.scheme=='https' and bool(host) and not (host=='wikisource.org' or host.endswith('.wikisource.org'))
def _viewport(name:str)->dict[str,int]:return {'width':390,'height':844} if name=='mobile' else {'width':1440,'height':1000}

def collect(url:str,source_id:str,viewport:str='desktop',artifact_dir:str|None=None)->dict[str,Any]:
 if not _allowed(url):return {'ok':False,'status':'blocked','error':{'code':'source_policy_deny','message':url}}
 try:from playwright.sync_api import sync_playwright
 except Exception:return {'ok':False,'status':'not_ready','error':{'code':'playwright_unavailable','message':'canonical host has no installed Playwright transport'}}
 root=_repo();observer_path=root/'static'/'dore-design'/'dore-design-observer.js'
 if not observer_path.exists():return {'ok':False,'status':'not_ready','error':{'code':'observer_unavailable','message':str(observer_path)}}
 observer=observer_path.read_text(encoding='utf-8');vp=_viewport(viewport)
 out=Path(artifact_dir) if artifact_dir else root/'artifacts'/'design-observation'/'captures';out.mkdir(parents=True,exist_ok=True)
 with sync_playwright() as pw:
  browser=pw.chromium.launch(headless=True)
  try:
   page=browser.new_page(viewport=vp);response=page.goto(url,wait_until='networkidle',timeout=30000);final=page.url
   page.add_script_tag(content=observer)
   evidence=page.evaluate("([id,url]) => window.DoreDesignObserver.observe({id:id,locator:url})",[f'observation.{source_id}.{viewport}',final])
   png=page.screenshot(full_page=True);sha=hashlib.sha256(png).hexdigest();ref=out/f'{source_id}-{viewport}-{sha[:12]}.png';ref.write_bytes(png)
   resources=page.evaluate("performance.getEntriesByType('resource').map(r=>({name:r.name,initiatorType:r.initiatorType}))")
   captured=datetime.now(timezone.utc).isoformat()
   return {'ok':True,'status':'completed','schema':SCHEMA,'sourceId':source_id,'requestedUrl':url,'finalUrl':final,'httpStatus':response.status if response else None,'renderedAt':captured,'viewport':viewport,'screenshot':{'ref':str(ref),'sha256':sha,'real_browser_render':True},'observerPayload':evidence,'resources':resources,'canonical_workspace_mutated':False,'production_promoted':False,'authority':{'class':'observational-evidence','mayPromoteCanonical':False,'requiresBeautifulGate':True}}
  finally:browser.close()

def main()->int:
 import argparse
 p=argparse.ArgumentParser();p.add_argument('url');p.add_argument('--source-id',required=True);p.add_argument('--viewport',choices=['desktop','mobile'],default='desktop');a=p.parse_args();r=collect(a.url,a.source_id,a.viewport);print(json.dumps(r,ensure_ascii=False));return 0 if r.get('ok') else 2
if __name__=='__main__':raise SystemExit(main())
