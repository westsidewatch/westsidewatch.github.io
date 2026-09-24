#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
r=json.loads((ROOT/'preview/jerusalem-3000/data/events/jesus-entry.json').read_text())
errors=[]
nodes={n['id'] for n in r['nodes']}
for s in r['segments']:
    if s['from'] not in nodes or s['to'] not in nodes: errors.append(f"{s['id']}: orphan endpoint")
    if s['geometry']=='withheld' and s.get('coordinatesENU') is not None: errors.append(f"{s['id']}: withheld geometry has coordinates")
if r['phase']!='herodian-jesus': errors.append('Jesus entry must bind to herodian-jesus phase')
if not any(s['status']=='disputed-exact-gate' for s in r['segments']): errors.append('exact eastern entry dispute gate missing')
if errors:
    print('\n'.join(errors)); raise SystemExit(1)
print(f'J3K_JESUS_ENTRY=PASS segments={len(r["segments"])} nodes={len(nodes)}')
