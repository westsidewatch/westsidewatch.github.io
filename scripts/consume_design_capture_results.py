#!/usr/bin/env python3
"""Admit real browser/render capture results into Design Intelligence comparison input.
No screenshot/result means no finding. No result can promote canonical design.
"""
import json, sys
from pathlib import Path

def fail(msg): print('FAIL:',msg); return 1

def main(argv):
    if len(argv)<2: return fail('provide capture-result JSON')
    payload=json.loads(Path(argv[1]).read_text())
    items=payload.get('items', [payload])
    admitted=[]
    for r in items:
        if r.get('schema')!='dore.design-capture-result.v1': return fail('wrong result schema')
        cap=r.get('capture') or {}; ev=r.get('evidence') or {}; auth=r.get('authority') or {}
        if not cap.get('screenshotRef'): return fail(f"{r.get('jobId')}: screenshot evidence missing")
        if ev.get('schema')!='dore.design-observation-evidence.v1': return fail(f"{r.get('jobId')}: observation envelope missing")
        if auth.get('class')!='observational-evidence' or auth.get('mayPromoteCanonical') is not False or auth.get('requiresBeautifulGate') is not True:
            return fail(f"{r.get('jobId')}: authority boundary violation")
        admitted.append({'jobId':r['jobId'],'sourceId':r['sourceId'],'viewport':r['viewport'],'screenshotRef':cap['screenshotRef'],'evidence':ev,'eligibleFor':'compare-only','canonicalPromotion':False})
    print(json.dumps({'schema':'dore.design-comparison-input.v1','status':'evidence-admitted','items':admitted,'next':'compare-distill'},ensure_ascii=False,indent=2))
    return 0
if __name__=='__main__': sys.exit(main(sys.argv))
