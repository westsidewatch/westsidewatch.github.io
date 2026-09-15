#!/usr/bin/env python3
import json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
D=ROOT/'static'/'dore-design'
C=D/'italian-editorial-grammar-candidates.v1.json'
E=D/'italian-editorial-evidence.v1.json'

def main():
    c=json.loads(C.read_text()); e=json.loads(E.read_text())
    evidence={x['id']:x for x in e.get('items',[])}; errors=[]; ids=set()
    required=('evidenceProvenance','generationComparison','noCanonicalRegression')
    if tuple(c.get('promotionContract',{}).get('requiredChecks',[])) != required:
        errors.append('registry promotion contract does not declare exact required checks')
    for x in c.get('items',[]):
        cid=x.get('id')
        if not cid or cid in ids: errors.append(f'duplicate/missing candidate id: {cid}')
        ids.add(cid)
        if x.get('state') not in {'candidate','admitted','rejected'}: errors.append(f'{cid}: invalid state')
        if not all(x.get(k) for k in ('family','era','module','value')): errors.append(f'{cid}: incomplete identity')
        refs=x.get('derivedFrom') or []
        if not refs: errors.append(f'{cid}: no evidence provenance')
        missing=[r for r in refs if r not in evidence]
        if missing: errors.append(f'{cid}: unknown evidence {missing}')
        if x.get('state')=='admitted':
            contract=x.get('promotionContract') or {}; checks=contract.get('checks') or {}
            absent=[k for k in required if checks.get(k) is not True]
            if absent: errors.append(f'{cid}: admitted without passing {absent}')
            comparison=contract.get('comparison') or {}
            if not comparison.get('baselinePrompt') or not comparison.get('candidatePrompt'): errors.append(f'{cid}: missing baseline/candidate comparison')
            if comparison.get('result')!='pass': errors.append(f'{cid}: comparison is not pass')
    if errors:
        for x in errors: print('FAIL:',x)
        return 1
    print(f'PASS: {len(ids)} candidates; admitted grammar cannot bypass evidence, comparison, or no-regression gates.')
    return 0
if __name__=='__main__': sys.exit(main())
