#!/usr/bin/env python3
import json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
D=ROOT/'static'/'dore-design'
CP=D/'italian-editorial-grammar-candidates.v1.json'
FP=D/'italian-editorial-generation-feedback.v1.json'
DIMS=('grammarLegibility','lineageFidelity','subjectPreservation','canonicalRegression')

def complete(item):
    ev=item.get('evaluation') or {}
    return item.get('baseline',{}).get('artifact') and item.get('candidate',{}).get('artifact') and all(ev.get(k) is not None for k in DIMS)

def expected_verdict(item):
    ev=item['evaluation']
    if ev['canonicalRegression'] is True or ev['subjectPreservation'] is False: return 'reject'
    if ev['grammarLegibility'] is True and ev['lineageFidelity'] is True and ev['subjectPreservation'] is True and ev['canonicalRegression'] is False: return 'promote'
    return 'retain'

def main():
    candidates=json.loads(CP.read_text()); feedback=json.loads(FP.read_text())
    by_id={x['id']:x for x in candidates['items']}; errors=[]; decisions=[]
    for f in feedback['items']:
        cid=f.get('candidateId'); c=by_id.get(cid)
        if not c: errors.append(f"{f.get('id')}: unknown candidate {cid}"); continue
        if not complete(f):
            if f.get('verdict')!='retain': errors.append(f"{f['id']}: incomplete pair must retain")
            decisions.append((cid,'retain','incomplete comparison'))
            continue
        verdict=expected_verdict(f)
        if f.get('verdict')!=verdict: errors.append(f"{f['id']}: verdict {f.get('verdict')} disagrees with evaluation {verdict}")
        decisions.append((cid,verdict,'complete comparison'))
        if verdict=='promote':
            contract=c.get('promotionContract') or {}; checks=contract.get('checks') or {}
            if not checks.get('evidenceProvenance'): errors.append(f'{cid}: promotion lacks evidence provenance')
            if not checks.get('generationComparison'): errors.append(f'{cid}: promotion lacks generationComparison pass')
            if not checks.get('noCanonicalRegression'): errors.append(f'{cid}: promotion lacks noCanonicalRegression pass')
    if errors:
        for e in errors: print('FAIL:',e)
        return 1
    for cid,v,why in decisions: print(f'{cid}: {v} ({why})')
    print('PASS: generation feedback cannot silently promote incomplete or regressive grammar.')
    return 0
if __name__=='__main__': sys.exit(main())
