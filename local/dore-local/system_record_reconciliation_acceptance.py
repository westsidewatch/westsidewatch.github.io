#!/usr/bin/env python3
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

classification = {}
for family in registry['families']:
    for path in matched_paths[family['id']]:
        classification.setdefault(path, set()).add(family['state'])
for path, states in classification.items():
    assert not ('canonical' in states and ({'historical', 'superseded'} & states)), \
        f'conflicting current/historical classification for {path}: {sorted(states)}'

all_checkpoints = {
    p.relative_to(ROOT).as_posix()
    for p in ROOT.glob('dore-core/projects/DORE-MEMORY-SWEEP-01-CHECKPOINT-*.md')
}
checkpoint_family = matched_paths['records:memory-sweep-checkpoints']
assert all_checkpoints, 'expected existing Memory Sweep checkpoints'
assert all_checkpoints == checkpoint_family, 'Memory Sweep checkpoint family has coverage drift'

master = 'dore-core/projects/DORÉ-MASTER-WORK-REGISTER.md'
sweep = 'dore-core/projects/DORÉ-MEMORY-CONSOLIDATION-SWEEP-01.md'
assert master in matched_paths['records:master-work-register']
assert sweep in matched_paths['records:master-work-register']

for path in ('docs/MASTER_SITE_ARCHITECTURE.md', 'docs/dore-memory-core-boundary.md'):
    assert 'canonical' in classification.get(path, set()), f'canonical record lost: {path}'
    assert 'unreviewed' not in classification.get(path, set()), f'canonical record regressed to unreviewed: {path}'

# ONE pass: every current top-level ONE markdown record has an explicit classification.
one_docs = {p.relative_to(ROOT).as_posix() for p in (ROOT / 'docs/one').glob('*.md')}
assert one_docs
for path in one_docs:
    states = classification.get(path, set())
    assert states, f'ONE record is orphaned: {path}'
    assert 'unreviewed' not in states, f'ONE record regressed to unreviewed: {path}'
assert classification.get('docs/one/README.md') == {'canonical'}
assert classification.get('docs/one/GOSPEL-HARMONY-FINAL-AUDIT-20260829.md') == {'evidence'}
for path in (
    'docs/one/GOSPEL-HARMONY-AUDIT-20260829.md',
    'docs/one/GOSPEL-HARMONY-CONSISTENCY-20260829.md',
):
    assert classification.get(path) == {'superseded'}

# Doré pass: all top-level markdown records are now reconciled. Only nested queues may remain unreviewed.
dore_top = {p.relative_to(ROOT).as_posix() for p in (ROOT / 'docs/dore').glob('*.md')}
assert dore_top, 'expected top-level Doré records'
for path in dore_top:
    states = classification.get(path, set())
    assert states, f'Doré top-level record is orphaned: {path}'
    assert 'unreviewed' not in states, f'Doré top-level record still unreviewed: {path}'

assert classification.get('docs/dore/README.md') == {'canonical'}
assert classification.get('docs/dore/DORE-THEOLOGICAL-BOUNDARY-2026-09-08.md') == {'canonical'}
for path in ('docs/dore/THE-GATE.md', 'docs/dore/KNOCKING-HISTORY.md'):
    assert classification.get(path) == {'historical'}, f'coordination history must not become current authority: {path}'

unreviewed = sorted(path for path, states in classification.items() if 'unreviewed' in states)
assert all(path.startswith(('docs/dore/design/', 'docs/dore/film/', 'docs/dore/lessons/')) for path in unreviewed), \
    f'unreviewed records escaped bounded Doré queues: {unreviewed}'

print(
    'DORE_SYSTEM_RECORD_RECONCILIATION=PASS '
    f'families={len(registry["families"])} '
    f'covered={len(classification)} checkpoints={len(all_checkpoints)} '
    f'one={len(one_docs)} dore_top={len(dore_top)} unreviewed={len(unreviewed)}'
)
