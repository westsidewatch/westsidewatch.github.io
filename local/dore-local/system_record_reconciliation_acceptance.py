#!/usr/bin/env python3
import fnmatch
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
atlas = json.loads((ROOT / 'data/system-atlas.v0.json').read_text())
registry = json.loads((ROOT / 'data/system-record-families.v0.json').read_text())

assert registry['schema'] == 'dore.system-record-families.v0'
assert registry['authority'] == 'github-main'
entity_ids = {item['id'] for item in atlas['entities']}
family_ids = [item['id'] for item in registry['families']]
assert len(family_ids) == len(set(family_ids)), 'record family IDs must be unique'

allowed_states = set(registry['states'])
matched_paths = {}
for family in registry['families']:
    assert family['owner'] in entity_ids, f"unknown System Atlas owner {family['owner']}"
    assert family['state'] in allowed_states
    assert family['patterns'], f"{family['id']} has no patterns"
    family_matches = set()
    for pattern in family['patterns']:
        matches = {p.relative_to(ROOT).as_posix() for p in ROOT.glob(pattern)}
        assert matches, f"record pattern matched nothing: {pattern}"
        family_matches |= matches
    matched_paths[family['id']] = family_matches

# Canonical families cannot silently overlap with historical/superseded classifications.
classification = {}
for family in registry['families']:
    for path in matched_paths[family['id']]:
        classification.setdefault(path, set()).add(family['state'])
for path, states in classification.items():
    assert not ('canonical' in states and ({'historical', 'superseded'} & states)), \
        f'conflicting current/historical classification for {path}: {sorted(states)}'

# Every Memory Sweep checkpoint currently in the repository must return home through one family.
all_checkpoints = {
    p.relative_to(ROOT).as_posix()
    for p in ROOT.glob('dore-core/projects/DORE-MEMORY-SWEEP-01-CHECKPOINT-*.md')
}
checkpoint_family = matched_paths['records:memory-sweep-checkpoints']
assert all_checkpoints, 'expected existing Memory Sweep checkpoints'
assert all_checkpoints == checkpoint_family, 'Memory Sweep checkpoint family has coverage drift'

# The two operational anchors must be represented explicitly, not only by broad globs.
master = 'dore-core/projects/DORÉ-MASTER-WORK-REGISTER.md'
sweep = 'dore-core/projects/DORÉ-MEMORY-CONSOLIDATION-SWEEP-01.md'
assert master in matched_paths['records:master-work-register']
assert sweep in matched_paths['records:master-work-register']

# Foundation canonical docs are not allowed to fall back to unreviewed.
for path in ('docs/MASTER_SITE_ARCHITECTURE.md', 'docs/dore-memory-core-boundary.md'):
    assert 'canonical' in classification.get(path, set()), f'canonical record lost: {path}'
    assert 'unreviewed' not in classification.get(path, set()), f'canonical record regressed to unreviewed: {path}'

unreviewed = sorted(path for path, states in classification.items() if 'unreviewed' in states)
print(
    'DORE_SYSTEM_RECORD_RECONCILIATION=PASS '
    f'families={len(registry["families"])} '
    f'covered={len(classification)} checkpoints={len(all_checkpoints)} '
    f'unreviewed={len(unreviewed)}'
)
