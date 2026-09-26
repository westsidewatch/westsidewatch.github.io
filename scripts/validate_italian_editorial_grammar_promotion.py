#!/usr/bin/env python3
import json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
D=ROOT/'static'/'dore-design'
C=D/'italian-editorial-grammar-candidates.v1.json'; E=D/'italian-editorial-evidence.v1.json'; F=D/'italian-editorial-generation-feedback.v1.json'

# These aliases were already reconciled to canonical evidence IDs. Keep them here as
# regression sentinels so an old snapshot cannot silently make the promotion gate red again.
RETIRED_EVIDENCE_IDS={
    'cg-1933-issue-07':'cg-1933-issue07-insert',
    'domus-ponti-268':'domus-ponti-250',
    'ottagono-39-1975':'ottagono-39',
    'casabella-370-1972':'casabella-370',
    'casabella-official-index':'casabella-370',
}

def main():
    c=json.loads(C.read_text()); e=json.loads(E.read_text()); f=json.loads(F.read_text())
    evidence={x['id']:x for x in e.get('items',[])}; feedback={x['candidateId']:x for x in f.get('items',[])}; errors=[]; ids=set()
    required=('evidenceProvenance','generationComparison','noCanonicalRegression')
    if tuple(c.get('promotionContract',{}).get('requiredChecks',[])) != required: errors.append('registry promotion contract does not declare exact required checks')
    for x in c.get('items',[]):
        cid=x.get('id')
        if not cid or cid in ids: errors.append(f'duplicate/missing candidate id: {cid}')
        ids.add(cid)
        if x.get('state') not in {'candidate','admitted','rejected'}: errors.append(f'{cid}: invalid state')
        if not all(x.get(k) for k in ('family','era','module','value')): errors.append(f'{cid}: incomplete identity')
        refs=x.get('derivedFrom') or []
        if not refs: errors.append(f'{cid}: no evidence provenance')
        retired=[r for r in refs if r in RETIRED_EVIDENCE_IDS]
        if retired:
            replacements={r:RETIRED_EVIDENCE_IDS[r] for r in retired}
            errors.append(f'{cid}: retired evidence id regression {replacements}')
        missing=[r for r in refs if r not in evidence]
        if missing: errors.append(f'{cid}: unknown evidence {missing}')
        fb=feedback.get(cid)
        if x.get('state')=='admitted':
            contract=x.get('promotionContract') or {}; checks=contract.get('checks') or {}; absent=[k for k in required if checks.get(k) is not True]
            if absent: errors.append(f'{cid}: admitted without passing {absent}')
            comparison=contract.get('comparison') or {}
            if not comparison.get('baselinePrompt') or not comparison.get('candidatePrompt') or comparison.get('result')!='pass': errors.append(f'{cid}: promotion contract comparison is not pass')
            if not fb: errors.append(f'{cid}: admitted without generation feedback record')
            else:
                ev=fb.get('evaluation') or {}; dims=f.get('requiredDimensions',[])
                if fb.get('status')!='evaluated' or fb.get('verdict')!='promote': errors.append(f'{cid}: generation feedback does not promote')
                if any(ev.get(k) is None for k in dims): errors.append(f'{cid}: incomplete generation feedback dimensions')
                if not fb.get('baseline',{}).get('artifact') or not fb.get('candidate',{}).get('artifact'): errors.append(f'{cid}: missing paired generation artifacts')
                if ev.get('canonicalRegression') is not False: errors.append(f'{cid}: canonical regression not cleared')
        if x.get('state')=='rejected' and fb and fb.get('verdict')=='promote': errors.append(f'{cid}: rejected candidate conflicts with promote feedback')
    if errors:
        for x in errors: print('FAIL:',x)
        return 1
    print(f'PASS: {len(ids)} candidates; canonical evidence IDs intact; generation feedback is authoritative for promotion outcome but never historical authority.')
    return 0
if __name__=='__main__': sys.exit(main())
