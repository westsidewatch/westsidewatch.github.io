#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
timeline=json.loads((ROOT/'preview/jerusalem-3000/data/continuous-build-timeline.json').read_text())
ledger=json.loads((ROOT/'preview/jerusalem-3000/data/lifecycle/herodian-30ce.lifecycle.json').read_text())
phases=[p['id'] for p in timeline['phases']]
allowed={'settlement','build','expand','transform','ruin','buried','rebuild'}
errors=[]
for obj in ledger['objects']:
    last=-1
    for event in obj['lifecycleEvents']:
        if event['phase'] not in phases: errors.append(f"{obj['id']}: unknown phase {event['phase']}"); continue
        i=phases.index(event['phase'])
        if i<last: errors.append(f"{obj['id']}: lifecycle events out of order")
        last=i
        if event['state'] not in allowed: errors.append(f"{obj['id']}: invalid state {event['state']}")
if len(phases)!=18: errors.append(f'expected 18 canonical phases, got {len(phases)}')
if errors:
    print('\n'.join(errors)); raise SystemExit(1)
print(f'J3K_CONSTRUCTION_ENGINE=PASS phases={len(phases)} objects={len(ledger["objects"])}')
