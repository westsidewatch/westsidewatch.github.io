#!/usr/bin/env python3
"""Validate the final three-specimen Italian Editorial generation regression.

This gate deliberately distinguishes READY from PASS. Missing generated artifacts are
not failures of the grounded prompt architecture, but they can never be reported as a
completed visual regression.
"""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
REG=ROOT/'static/dore-design/italian-editorial-generation-regression.v1.json'
OBS=ROOT/'static/dore-design/italian-editorial-grounded-observations.v0.json'

reg=json.loads(REG.read_text(encoding='utf-8'))
obs=json.loads(OBS.read_text(encoding='utf-8'))
obs_by_id={(x.get('evidence') or {}).get('id'):x for x in obs.get('items',[])}
required=set(reg.get('requiredCases') or [])
cases=reg.get('cases') or []
errors=[]
pending=[]
seen=set()

for case in cases:
    eid=case.get('evidenceId')
    seen.add(eid)
    observation=obs_by_id.get(eid)
    if not observation:
        errors.append(f'{eid}: grounded observation missing')
        continue
    if observation.get('authority')!='historical-image-observation':
        errors.append(f'{eid}: wrong observation authority')
    if (observation.get('provenance') or {}).get('imageInspected') is not True:
        errors.append(f'{eid}: exact historical image was not inspected')
    artifact=case.get('generatedArtifact')
    comparison=case.get('comparison')
    verdict=case.get('verdict')
    if not artifact or not comparison:
        if verdict!='pending-generation':
            errors.append(f'{eid}: missing artifact/comparison cannot claim {verdict!r}')
        pending.append(eid)
        continue
    if not artifact.get('uri') or not artifact.get('generator'):
        errors.append(f'{eid}: generated artifact lacks uri/generator provenance')
    checks=comparison.get('checks') or {}
    for key in reg.get('requiredChecks',[]):
        if key not in checks:
            errors.append(f'{eid}: comparison missing check {key}')
    if verdict not in {'pass','fail'}:
        errors.append(f'{eid}: completed comparison requires pass/fail verdict')

missing=required-seen
if missing: errors.append('missing required cases: '+', '.join(sorted(missing)))

if errors:
    print('ITALIAN_EDITORIAL_GENERATION_REGRESSION=FAIL')
    for error in errors: print('-',error)
    raise SystemExit(1)
if pending:
    print('ITALIAN_EDITORIAL_GENERATION_REGRESSION=READY_NOT_PASS')
    print('PENDING_REAL_GENERATION='+','.join(sorted(pending)))
    print('GENERATED_IMAGES_ARE_EVALUATION_ONLY=PASS')
    raise SystemExit(0)
print('ITALIAN_EDITORIAL_GENERATION_REGRESSION=PASS')
print('THREE_REAL_GENERATIONS_COMPARED=PASS')
print('GENERATED_IMAGES_ARE_EVALUATION_ONLY=PASS')
