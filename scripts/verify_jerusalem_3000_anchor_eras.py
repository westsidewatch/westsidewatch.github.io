#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
packs=json.loads((ROOT/'preview/jerusalem-3000/data/anchor-era-packs.json').read_text())
life=json.loads((ROOT/'preview/jerusalem-3000/data/lifecycle/anchor-era.lifecycle.json').read_text())
timeline=json.loads((ROOT/'preview/jerusalem-3000/data/continuous-build-timeline.json').read_text())
phase_ids={p['id'] for p in timeline['phases']}
required={'david-solomon','persian-nehemiah','herodian-jesus','ottoman','modern'}
errors=[]
pack_phases={p['phase'] for p in packs['packs']}
if pack_phases!=required: errors.append(f'anchor phases mismatch: {pack_phases}')
ids=set()
for pack in packs['packs']:
    for obj in pack.get('objects',[]):
        if obj['id'] in ids: errors.append(f'duplicate object {obj["id"]}')
        ids.add(obj['id'])
        if not obj.get('evidence'): errors.append(f'{obj["id"]}: missing evidence')
        if obj.get('geometry') in ('survey-linework-required','survey-footprint-required','current-survey-required','current-geodata-required') and obj['evidence']!='observed':
            errors.append(f'{obj["id"]}: survey/current geometry must be observed')
for obj in life['objects']:
    if obj['id'] not in ids: errors.append(f'{obj["id"]}: lifecycle object absent from anchor packs')
    for event in obj['lifecycleEvents']:
        if event['phase'] not in phase_ids: errors.append(f'{obj["id"]}: unknown phase {event["phase"]}')
if errors:
    print('\n'.join(errors)); raise SystemExit(1)
print(f'J3K_ANCHOR_ERAS=PASS packs={len(packs["packs"])} lifecycleObjects={len(life["objects"])}')
