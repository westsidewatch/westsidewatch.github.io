#!/usr/bin/env python3
"""Run one admitted Design Learning cycle through the canonical A2A host.
Real-Mac execution only. A result is persisted only when design.observe.capture
returns proven real-browser raster evidence. Partial cycles remain resumable.
"""
from __future__ import annotations
import argparse, hashlib, json, os, sys, time
from pathlib import Path

def _repo(): return Path(os.environ.get('DORE_REPO_ROOT') or Path(__file__).resolve().parents[2]).resolve()
def _load(path): return json.loads(path.read_text(encoding='utf-8'))
def _atomic(path,data):
 path.parent.mkdir(parents=True,exist_ok=True); tmp=path.with_suffix(path.suffix+'.tmp'); tmp.write_text(json.dumps(data,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8'); tmp.replace(path)
def _id(source,viewport): return hashlib.sha256(f"{source['id']}|{viewport}|{source['url']}".encode()).hexdigest()[:20]
def main(argv=None):
 p=argparse.ArgumentParser();p.add_argument('--cycle',default='001');p.add_argument('--limit',type=int,default=0);a=p.parse_args(argv)
 repo=_repo(); local=repo/'local'/'dore-local'; static=repo/'static'/'dore-design'
 if str(local) not in sys.path:sys.path.insert(0,str(local))
 import native_host
 registry=_load(static/'design-discovery-sources.v1.json'); sources=[s for s in registry['sources'] if s.get('status')=='verified-public']
 out=repo/'artifacts'/'design-observation'/f'cycle-{a.cycle}.results.json'; previous=_load(out) if out.exists() else {'results':[]}; done={(x['sourceId'],x['viewport']) for x in previous.get('results',[]) if x.get('status')=='completed'}
 results=list(previous.get('results',[])); attempted=0
 for source in sources:
  for viewport in ('desktop','mobile'):
   if (source['id'],viewport) in done:continue
   if a.limit and attempted>=a.limit:break
   attempted+=1; request={'capability':'design.observe.capture','args':{'sourceId':source['id'],'url':source['url'],'viewport':viewport},'caller_product':'dore-design-learning','request_id':f"observe-{_id(source,viewport)}"}
   response=native_host.route_payload(request); ok=response.get('ok') is True and response.get('status')=='completed'; rasters=response.get('rasterEvidence') or []
   proven=ok and bool(rasters) and all(r.get('real_browser_render') is True and r.get('sha256') for r in rasters) and response.get('canonical_workspace_mutated') is False and response.get('production_promoted') is False
   record={'jobId':_id(source,viewport),'sourceId':source['id'],'lane':source['lane'],'url':source['url'],'viewport':viewport,'status':'completed' if proven else 'blocked','capturedAt':int(time.time()),'rasterEvidence':rasters if proven else [],'authority':{'class':'observational-evidence','mayPromoteCanonical':False,'requiresBeautifulGate':True}}
   if not proven:record['blockReason']=response.get('reason') or (response.get('error') or {}).get('code') or 'unproven_capture'
   results=[x for x in results if (x.get('sourceId'),x.get('viewport'))!=(source['id'],viewport)];results.append(record);_atomic(out,{'schema':'dore.design-observation-cycle-results.v1','cycle':a.cycle,'status':'partial','results':results})
  if a.limit and attempted>=a.limit:break
 expected=len(sources)*2; completed=sum(x.get('status')=='completed' for x in results); status='captured' if completed==expected else 'partial'
 report={'schema':'dore.design-observation-cycle-results.v1','cycle':a.cycle,'status':status,'expectedJobs':expected,'completedJobs':completed,'results':results,'canonicalWrites':0,'automaticPromotion':False};_atomic(out,report);print(json.dumps({'status':status,'completed':completed,'expected':expected,'artifact':str(out)},ensure_ascii=False));return 0 if status=='captured' else 2
if __name__=='__main__':raise SystemExit(main())
