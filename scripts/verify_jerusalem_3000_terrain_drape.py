#!/usr/bin/env python3
"""Static contract verifier for Jerusalem 3000 geometry draping.
Real elevation assertions run only after canonical DEM mesh exists.
"""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
reg=json.loads((ROOT/'preview/jerusalem-3000/data/geometry/herodian-30ce.registry.json').read_text())
contract=json.loads((ROOT/'preview/jerusalem-3000/data/terrain-registration-contract.json').read_text())
errors=[]
for g in reg['entries']:
    if g['status']=='withheld' and g.get('coordinatesENU') is not None:
        errors.append(f"{g['objectId']}: withheld geometry must not drape")
    if g.get('coordinatesENU') is not None and g['geometryType'] not in {'Polygon','LineString','MultiLineString'}:
        errors.append(f"{g['objectId']}: unsupported terrain-drape geometry type")
if 'Terrain sampling never changes object east/north.' not in contract['gates']:
    errors.append('terrain contract lost horizontal immutability gate')
if errors:
    print('\n'.join(errors)); raise SystemExit(1)
print(f'J3K_TERRAIN_DRAPE_CONTRACT=PASS entries={len(reg["entries"])}')
