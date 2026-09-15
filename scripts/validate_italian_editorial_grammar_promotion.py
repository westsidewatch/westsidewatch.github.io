#!/usr/bin/env python3
import json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
D=ROOT/'static'/'dore-design'
C=D/'italian-editorial-grammar-candidates.v1.json'
E=D/'italian-editorial-evidence.v1.json'

def fail(msg):
    print('FAIL:',msg); return False

def main():
    c=json.loads(C.read_text())
    e=json.loads(E.read_text())
    evidence={x['id']:x for x in e.get('items',[])}
    ok=True
    ids=set()
    for x in c.get('items',[]):
        cid=x.get('id')
        if not cid or cid in ids: ok=fail(f'duplicate/missing candidate id: {cid}') and ok
        ids.add(cid)
        if x.get('state') not in {'candidate','admitted','rejected'}: ok=fail(f'{cid}: invalid state') and ok
        if not x.get('family') or not x.get('era') or not x.get('module') or not x.get('value'): ok=fail(f'{cid}: incomplete identity') and ok
        refs=x.get('derivedFrom') or []
        if not refs: ok=fail(f'{cid}: no evidence provenance') and ok
        missing=[r for r in refs if r not in evidence]
        if missing: ok=fail(f'{cid}: unknown evidence {missing}') and ok
        if x.get('state')=='admitted':
            contract=x.get('promotionContract') or {}
            checks=contract.get('checks') or {}
            required=['evidenceProvenance','generationComparison','noCanonicalRegression']
            absent=[k for k in required if checks.get(k) is not True]
            if absent: ok=fail(f'{cid}: admitted without passing {absent}') and ok
            comparison=contract.get('comparison') or {}
            if not comparison.get('baselinePrompt') or not comparison.get('candidatePrompt'):
                ok=fail(f'{cid}: admitted without baseline/candidate prompt comparison') and ok
            if comparison.get('result')!='pass': ok=fail(f'{cid}: admitted comparison is not pass') and ok
    if ok:
        print(f'PASS: {len(ids)} grammar candidates; every admitted rule satisfies promotion contract.')
        return 0
    return 1
if __name__=='__main__': sys.exit(main())
