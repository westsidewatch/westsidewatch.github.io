#!/usr/bin/env python3
import json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
placement=json.loads((ROOT/'docs/dore/film/canvas-placement-experiment-01.json').read_text(encoding='utf-8'))
spine=json.loads((ROOT/'docs/dore/film/camera-spine-experiment-01.json').read_text(encoding='utf-8'))
registry=(ROOT/'static/one/one-dore-cover-registry.js').read_text(encoding='utf-8')
assets=(ROOT/'static/one/one-dore-assets-241.js').read_text(encoding='utf-8')
lab=(ROOT/'static/dore/film/canvas-motion-lab-01.html').read_text(encoding='utf-8')
node_ids={n['id'] for n in spine['nodes']}; failures=[]; seen=set()
for a in placement['anchors']:
    did=a['doreId']; title=a['title']; file=a['file']
    if did in seen: failures.append(f'duplicate Doré ID {did}')
    seen.add(did)
    if a['frameNode'] not in node_ids: failures.append(f"{a['anchorId']} missing frame node {a['frameNode']}")
    if not re.search(rf'{did}:\s*"{re.escape(title)}"',registry): failures.append(f'{did} title not canonical registry exact match')
    if not re.search(rf'"{did}":\s*"{re.escape(file)}"',assets): failures.append(f'{did} file not canonical 241 exact match')
    if not a.get('canonicalFrameMoment'): failures.append(f'{did} missing canonical frame moment')
policy=placement['assetPolicy']; rules=placement['rules']
if policy.get('origin')!='DORE_ORIGINAL_LIBRARY': failures.append('wrong asset origin')
if policy.get('master')!='ONE-DORE-241-MASTER-MAPPING': failures.append('wrong asset master')
if not policy.get('preserveFullComposition'): failures.append('full composition must be preserved')
if policy.get('allowGeneratedReplacement'): failures.append('generated replacement forbidden')
if not rules.get('cameraFirst') or not rules.get('oneCamera') or rules.get('conventionalCuts')!=0: failures.append('camera-first one-camera zero-cut contract broken')
for k in ('goldenLightEnabled','lifeAnimationEnabled','scriptureEnabled','nvsEnabled','full3DEnabled'):
    if rules.get(k): failures.append(f'{k} must remain false in Canvas Lab 01')
if 'curve.getPoint(u)' not in lab or 'getPointAt(u)' in lab: failures.append('lab must hit authored control-point parameterization exactly')
if 'CANONICAL FRAME MOMENT · FULL COMPOSITION' not in lab: failures.append('frame moment HUD missing')
print('DORÉ FILM CANVAS PLACEMENT VALIDATION')
print('anchors=',[(a['doreId'],a['frameNode']) for a in placement['anchors']])
if failures:
    print('FAIL'); [print(' -',f) for f in failures]; sys.exit(1)
print('PASS — canonical IDs/files, Camera Spine nodes, no-generation rules, and exact control-point parameterization are consistent')
