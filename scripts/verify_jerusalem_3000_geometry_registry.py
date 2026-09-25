#!/usr/bin/env python3
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
LEDGER=json.loads((ROOT/'preview/jerusalem-3000/data/objects/herodian-30ce.json').read_text())
REG=json.loads((ROOT/'preview/jerusalem-3000/data/geometry/herodian-30ce.registry.json').read_text())
objects={o['id']:o for o in LEDGER['objects']}
errors=[]
for g in REG['entries']:
    oid=g['objectId']
    if oid not in objects: errors.append(f'{oid}: orphan geometry')
    if g['status']=='withheld' and g.get('coordinatesENU') is not None: errors.append(f'{oid}: withheld geometry has coordinates')
    if g.get('coordinatesENU') is not None and not g.get('basis'): errors.append(f'{oid}: geometry lacks evidence basis')
    if 'observed' in g.get('status','') and 'reconstructed' in objects[oid].get('evidence','') and 'observed' not in objects[oid].get('evidence','') and objects[oid].get('evidence')!='archaeological':
        errors.append(f'{oid}: geometry overstates observed evidence')
if set(objects)-{g['objectId'] for g in REG['entries']}:
    errors.append('registry missing object IDs: '+','.join(sorted(set(objects)-{g['objectId'] for g in REG['entries']})))
if errors:
    print('\n'.join(errors)); raise SystemExit(1)
print(f'J3K_GEOMETRY_REGISTRY=PASS entries={len(REG["entries"])}')
