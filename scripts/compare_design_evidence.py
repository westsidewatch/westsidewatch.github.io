#!/usr/bin/env python3
"""Compare captured Doré design evidence without granting design authority."""
from __future__ import annotations
import argparse,json
from pathlib import Path

def claims(obs,layer):
 v=(obs.get('observations') or {}).get(layer) or []
 return [{'statement':x.get('statement'),'confidence':x.get('confidence'),'evidenceRefs':x.get('evidenceRefs') or []} for x in v if isinstance(x,dict) and x.get('statement')]
def main():
 p=argparse.ArgumentParser();p.add_argument('cycle_result');p.add_argument('-o','--output');a=p.parse_args();src=Path(a.cycle_result);cycle=json.loads(src.read_text(encoding='utf-8'))
 if cycle.get('status')!='captured':raise SystemExit('cycle evidence is not fully captured')
 rows=[]
 for r in cycle.get('results',[]):
  obs=r.get('observerPayload') or {}
  if obs.get('schema')!='dore.design-observation-evidence.v1':raise SystemExit(f"missing observation envelope: {r.get('jobId')}")
  rows.append({'sourceId':r['sourceId'],'lane':r.get('lane'),'viewport':r['viewport'],'finalUrl':r.get('finalUrl'),'screenshotRef':r.get('screenshotRef'),'facts':(obs.get('observations') or {}).get('visualFacts') or {},'claims':{k:claims(obs,k) for k in ('componentGrammar','compositionGrammar','editorialGrammar','motionGrammar','responsiveBehavior')}})
 by_source={}
 for x in rows:by_source.setdefault(x['sourceId'],{})[x['viewport']]=x
 responsive=[]
 for sid,pair in by_source.items():
  if 'desktop' in pair and 'mobile' in pair:responsive.append({'sourceId':sid,'desktopEvidence':pair['desktop']['screenshotRef'],'mobileEvidence':pair['mobile']['screenshotRef'],'status':'comparison-ready','inference':None})
 out={'schema':'dore.design-comparison-input.v1','cycle':cycle.get('cycle'),'status':'comparison-ready','observations':rows,'responsivePairs':responsive,'distillation':{'factsOnly':True,'inferenceStatus':'pending-evidence-backed-distillation','grammarCandidates':[]},'authority':{'class':'comparison-evidence','mayPromoteCanonical':False,'requiresBeautifulGate':True,'humanAuthorityForCanonicalPromotion':True},'canonicalWrites':0}
 dest=Path(a.output) if a.output else src.with_name(src.stem+'.comparison.json');dest.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(dest)
if __name__=='__main__':main()
