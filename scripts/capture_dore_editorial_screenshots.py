#!/usr/bin/env python3
"""Capture browser-rendered Doré proof at four viewport sizes using Playwright.

Requires an existing local preview.html and an installed Playwright Chromium.
No network, browser installation, or publication is performed by this script.
"""
import argparse,json
from pathlib import Path

WIDTHS=(320,375,768,1440)
def capture(preview,out,headless=True):
 preview=Path(preview).resolve()
 if not preview.is_file():raise FileNotFoundError(preview)
 out=Path(out).resolve();out.mkdir(parents=True,exist_ok=True)
 try:
  from playwright.sync_api import sync_playwright
 except ImportError as exc:
  raise RuntimeError('Playwright Python package not installed; no screenshot captured') from exc
 entries=[]
 with sync_playwright() as pw:
  browser=pw.chromium.launch(headless=headless)
  try:
   for width in WIDTHS:
    page=browser.new_page(viewport={'width':width,'height':1000},device_scale_factor=1)
    try:
     page.goto(preview.as_uri(),wait_until='load')
     page.locator('img').first.wait_for(state='visible',timeout=10000)
     page.evaluate('document.fonts.ready')
     loaded=page.locator('img').first.evaluate('(el) => el.complete && el.naturalWidth > 0')
     if not loaded:raise RuntimeError('Image failed to decode at '+str(width))
     target=out/('proof-'+str(width)+'.png')
     page.screenshot(path=str(target),full_page=True,animations='disabled')
     entries.append({'viewport_width':width,'screenshot':target.name,
                     'image_decoded':True,'title_visible':page.locator('.type strong').first.is_visible()})
    finally:page.close()
  finally:browser.close()
 manifest={'schema':'dore.editorial.screenshots.v1','preview':str(preview),
           'screenshots':entries,'visual_qa_status':'pending_human_review',
           'publication_approved':False}
 (out/'screenshots-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
 return manifest
def main():
 p=argparse.ArgumentParser()
 p.add_argument('--preview',required=True)
 p.add_argument('--out',default='local/dore-editorial-screenshots')
 a=p.parse_args()
 r=capture(a.preview,a.out)
 print(json.dumps({'captured':len(r['screenshots']),'out':a.out}))
if __name__=='__main__':main()
