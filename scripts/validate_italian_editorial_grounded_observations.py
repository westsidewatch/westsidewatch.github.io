#!/usr/bin/env python3
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OBS=ROOT/'static/dore-design/italian-editorial-grounded-observations.v0.json'
EVIDENCE=ROOT/'static/dore-design/italian-editorial-evidence.v1.json'
FINGERPRINTS=ROOT/'static/dore-design/italian-editorial-visual-fingerprints.v1.json'
DIMS={'layout','image','typography','material','density','sequence','irony','emergence'}


def main():
    obs=json.loads(OBS.read_text(encoding='utf-8'))
    evidence={x['id']:x for x in json.loads(EVIDENCE.read_text(encoding='utf-8'))['items']}
    fps={x['evidenceId']:x for x in json.loads(FINGERPRINTS.read_text(encoding='utf-8'))['items']}
    errors=[]
    for item in obs.get('items',[]):
        eid=item.get('evidence',{}).get('id')
        ev=evidence.get(eid)
        if not ev: errors.append(f'{eid}: evidence missing'); continue
        if item.get('authority')!='historical-image-observation': errors.append(f'{eid}: wrong authority')
        if item.get('canonicalDoréLearning') is not False: errors.append(f'{eid}: teacher observation must not self-promote')
        if item.get('provenance',{}).get('imageInspected') is not True: errors.append(f'{eid}: image inspection provenance missing')
        if item.get('evidence',{}).get('imageUri')!=ev.get('image'): errors.append(f'{eid}: exact image identity drift')
        if set(item.get('dimensions',{}))!=DIMS: errors.append(f'{eid}: eight dimensions incomplete')
        for dim,val in item.get('dimensions',{}).items():
            if val.get('status') not in {'observed','insufficient'}: errors.append(f'{eid}/{dim}: bad status')
            facts=val.get('facts') or []
            if val.get('status')=='observed' and not facts: errors.append(f'{eid}/{dim}: observed without facts')
            if val.get('status')=='insufficient' and facts: errors.append(f'{eid}/{dim}: insufficient fabricated facts')

    # Known first-run drift assertions. These intentionally prove why the old manually
    # authored fingerprint registry cannot remain prompt authority.
    drift=[]
    il=fps.get('il-franchi-2008-03',{})
    il_text=' '.join(sum((v for v in (il.get('dimensions') or {}).values()),[])).lower()
    if 'extreme close-up' in il_text: drift.append('il-franchi-2008-03: manual fingerprint says extreme close-up; inspected evidence is head/shoulders/upper torso portrait')
    if 'oversized high-contrast serif headline' in il_text: drift.append('il-franchi-2008-03: manual fingerprint invents cross-field oversized serif headline; inspected evidence confines type to left column')
    if 'metallic-gold' in il_text: drift.append('il-franchi-2008-03: manual fingerprint invents metallic-gold translucent overlay; inspected evidence shows muted tan issue band inside left column')

    if errors:
        print('GROUNDED_OBSERVATION_GATE=FAIL')
        for e in errors: print('-',e)
        raise SystemExit(1)
    print('GROUNDED_OBSERVATION_GATE=PASS')
    print('REAL_IMAGE_OBSERVATIONS='+','.join(x['evidence']['id'] for x in obs['items']))
    print('MANUAL_FINGERPRINT_AUTHORITY=REJECTED')
    print('MANUAL_FINGERPRINT_DRIFT='+str(len(drift)))
    for d in drift: print('DRIFT:',d)
    if len(drift)<3:
        raise SystemExit('expected IL manual-fingerprint drift was not exposed')

if __name__=='__main__': main()
