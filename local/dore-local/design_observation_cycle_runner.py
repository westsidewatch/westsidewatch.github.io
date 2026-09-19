#!/usr/bin/env python3
"""Run one admitted Design Learning cycle through canonical A2A."""
from __future__ import annotations
import argparse,hashlib,json,os,sys,time
from pathlib import Path
def _repo():return Path(os.environ.get('DORE_REPO_ROOT') or Path(__file__).resolve().parents[2]).resolve()
def _load(p):return json.loads(p.read_text(encoding='utf-8'))
def _atomic(p,d):p.parent.mkdir(parents=True,exist_ok=True);t=p.with_suffix(p.suffix+'.tmp');t.write_text(json.dumps(d,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8');t.replace(p)
def _id(s,v):return hashlib.sha256(f"{s['id']}|{v}|{s['url']}".encode()).hexdigest()[:20]
def main(argv=None):
 p=argparse.ArgumentParser();p.add_argument('--cycle',default='001');p.add_argument('--limit',type=int,default=0);a=p.parse_args(argv);repo=_repo();local=repo/'local'/'dore-local';static=repo/'static'/'dore-design'
 if str(local) not in sys.path:sys.path.insert(0,str(local))
 import native_host
 registry=_load(static/'design-discovery-sources.v1.json');cycle=_load(static/f'design-learning-cycle-{a.cycle}.v1.json');admitted=set(cycle.get('admittedSources') or []);sources=[s for s in registry['sources'] if s['id'] in admitted and s.get('status')=='verified-public']
 out=repo/'artifacts'/'design-observation'/f'cycle-{a.cycle}.results.json';previous=_load(out) if out.exists() else {'results':[]};done={(x['sourceId'],x['viewport']) for x in previous.get('results',[]) if x.get('status')=='completed'};results=list(previous.get('results',[]));attempted=0
 for s in sources:
  for v in ('desktop','mobile'):
   if (s['id'],v) in done:continue
   if a.limit and attempted>=a.limit:break
   attempted+=1;r=native_host.route_payload({'capability':'design.observe.capture','args':{'sourceId':s['id'],'url':s['url'],'viewport':v},'caller_product':'dore-design-learning','request_id':f'observe-{_id(s,v)}'})
   ras=r.get('rasterEvidence') or [];obs=r.get('observerPayload');proven=r.get('ok') is True and r.get('status')=='completed' and bool(ras) and all(x.get('real_browser_render') is True and x.get('sha256') for x in ras) and isinstance(obs,dict) and obs.get('schema')=='dore.design-observation-evidence.v1' and r.get('canonical_workspace_mutated') is False and r.get('production_promoted') is False
   rec={'jobId':_id(s,v),'sourceId':s['id'],'lane':s['lane'],'url':s['url'],'viewport':v,'status':'completed' if proven else 'blocked','capturedAt':int(time.time()),'rasterEvidence':ras if proven else [],'observerPayload':obs if proven else None,'sourceProbe':r.get('sourceProbe') if proven else None,'finalUrl':r.get('finalUrl') if proven else None,'screenshotRef':r.get('screenshotRef') if proven else None,'authority':{'class':'observational-evidence','mayPromoteCanonical':False,'requiresBeautifulGate':True}}
   if not proven:rec['blockReason']=r.get('reason') or (r.get('error') or {}).get('code') or 'incomplete_evidence'
   results=[x for x in results if (x.get('sourceId'),x.get('viewport'))!=(s['id'],v)];results.append(rec);_atomic(out,{'schema':'dore.design-observation-cycle-results.v1','cycle':a.cycle,'status':'partial','results':results})
  if a.limit and attempted>=a.limit:break
 expected=len(sources)*2;completed=sum(x.get('status')=='completed' for x in results);status='captured' if completed==expected and len(sources)==len(admitted) else 'partial';report={'schema':'dore.design-observation-cycle-results.v1','cycle':a.cycle,'status':status,'expectedJobs':expected,'completedJobs':completed,'results':results,'canonicalWrites':0,'automaticPromotion':False};_atomic(out,report);print(json.dumps({'status':status,'completed':completed,'expected':expected,'artifact':str(out)},ensure_ascii=False));return 0 if status=='captured' else 2
if __name__=='__main__':raise SystemExit(main())
