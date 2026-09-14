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

# ONE reconciliation pass: every current docs/one markdown file must now have an explicit classification.
one_docs = {p.relative_to(ROOT).as_posix() for p in (ROOT / 'docs/one').glob('*.md')}
assert one_docs, 'expected ONE documentation records'
for path in one_docs:
    states = classification.get(path, set())
    assert states, f'ONE record is orphaned: {path}'
    assert 'unreviewed' not in states, f'ONE record regressed to unreviewed: {path}'

one_index = 'docs/one/README.md'
final_audit = 'docs/one/GOSPEL-HARMONY-FINAL-AUDIT-20260829.md'
preliminary = {
    'docs/one/GOSPEL-HARMONY-AUDIT-20260829.md',
    'docs/one/GOSPEL-HARMONY-CONSISTENCY-20260829.md',
}
assert classification.get(one_index) == {'canonical'}
assert classification.get(final_audit) == {'evidence'}
for path in preliminary:
    assert classification.get(path) == {'superseded'}, f'preliminary ONE audit must remain provenance: {path}'

one_entity = next(item for item in atlas['entities'] if item['id'] == 'tool:one')
assert one_index in one_entity.get('docs', []), 'System Atlas ONE entrypoint must include docs/one/README.md'

unreviewed = sorted(path for path, states in classification.items() if 'unreviewed' in states)
print(
    'DORE_SYSTEM_RECORD_RECONCILIATION=PASS '
    f'families={len(registry["families"])} '
    f'covered={len(classification)} checkpoints={len(all_checkpoints)} '
    f'one={len(one_docs)} unreviewed={len(unreviewed)}'
)
