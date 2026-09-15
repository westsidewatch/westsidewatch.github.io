#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / 'static/dore-design/italian-editorial-evidence.v1.json'
FINGERPRINTS = ROOT / 'static/dore-design/italian-editorial-visual-fingerprints.v1.json'
ALLOWED = {'layout','image','typography','material','density','sequence','irony','emergence'}

def main():
    evidence = json.loads(EVIDENCE.read_text())
    fpdb = json.loads(FINGERPRINTS.read_text())
    evidence_by_id = {x['id']: x for x in evidence['items']}
    errors = []
    policy = fpdb.get('compilerPolicy') or {}
    if not policy.get('lineageMayInfluenceDesignLogicNotConcreteContent'):
        errors.append('compilerPolicy: lineage/content authority boundary missing')
    if not policy.get('unsupportedConcreteElementsAreForbidden'):
        errors.append('compilerPolicy: unsupported concrete invention gate missing')
    for fp in fpdb['items']:
        eid = fp.get('evidenceId')
        ev = evidence_by_id.get(eid)
        if not ev:
            errors.append(f'{eid}: missing historical evidence')
            continue
        dims = fp.get('dimensions') or {}
        unknown = set(dims) - ALLOWED
        if unknown:
            errors.append(f'{eid}: unknown dimensions {sorted(unknown)}')
        for dim, rules in dims.items():
            if dim not in (ev.get('modules') or []):
                errors.append(f'{eid}: fingerprint dimension {dim} is not evidenced by item modules')
            if not rules or not all(isinstance(x,str) and x.strip() for x in rules):
                errors.append(f'{eid}: empty fingerprint rules for {dim}')
        if not fp.get('transferable'):
            errors.append(f'{eid}: transferable contract missing')
        if not fp.get('forbidden'):
            errors.append(f'{eid}: forbidden-invention contract missing')
        if not fp.get('unsupportedInvention'):
            errors.append(f'{eid}: DNA leakage / unsupported-invention contract missing')
        if not fp.get('fidelityQuestion'):
            errors.append(f'{eid}: fidelity question missing')
    if errors:
        print('VISUAL_FINGERPRINT_CONTRACT=FAIL')
        for e in errors: print('-', e)
        raise SystemExit(1)
    print('VISUAL_FINGERPRINT_CONTRACT=PASS')
    print(f'FINGERPRINTS={len(fpdb["items"])}')
    print('REGRESSION_SEEDS=' + ','.join(x['evidenceId'] for x in fpdb['items'] if x.get('status')=='regression-seed'))
    print('DNA_LEAKAGE_GATE=PASS')

if __name__ == '__main__':
    main()
