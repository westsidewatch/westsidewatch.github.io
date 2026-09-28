#!/usr/bin/env python3
"""Compile admitted public discovery sources into bounded capture jobs.
Execution is delegated to Doré's existing browser/render runtime; this module owns no browser.
"""
import json, sys
from pathlib import Path
from datetime import datetime, timezone
ROOT=Path(__file__).resolve().parents[1]
D=ROOT/'static'/'dore-design'
SOURCES=D/'design-discovery-sources.v1.json'
LOOP=D/'design-learning-loop.v1.json'

def main():
    sources=json.loads(SOURCES.read_text())
    loop=json.loads(LOOP.read_text())
    lanes={x['id'] for x in loop['sourceLanes']}
    jobs=[]; errors=[]
    for s in sources['sources']:
        if s['lane'] not in lanes: errors.append(f"unknown lane: {s['id']}"); continue
        if s.get('status')!='verified-public': continue
        if not s['url'].startswith('https://'): errors.append(f"non-https source: {s['id']}"); continue
        jobs.append({
          'jobId':f"design-capture:{s['id']}", 'lane':s['lane'], 'sourceId':s['id'], 'url':s['url'],
          'capture':s['capture'], 'viewportSet':['desktop','mobile'],
          'emitSchema':'dore.design-observation-evidence.v1',
          'authority':'observation-only', 'mayPromoteCanonical':False,
          'requiresBeautifulGate':True
        })
    if errors:
        for e in errors: print('FAIL:',e)
        return 1
    out={'schema':'dore.design-capture-queue.v1','generatedAt':datetime.now(timezone.utc).isoformat(),'executor':'dore-existing-browser-render-runtime','jobs':jobs}
    print(json.dumps(out,ensure_ascii=False,indent=2)); return 0
if __name__=='__main__': sys.exit(main())
