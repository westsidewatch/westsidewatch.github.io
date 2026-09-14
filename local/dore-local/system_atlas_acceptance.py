#!/usr/bin/env python3
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ATLAS_PATH = ROOT / 'data/system-atlas.v0.json'
SCHEMA_PATH = ROOT / 'data/system-atlas.schema.json'

atlas = json.loads(ATLAS_PATH.read_text())
schema = json.loads(SCHEMA_PATH.read_text())

assert atlas['schema'] == 'dore.system-atlas.v0'
assert atlas['authority'] == 'github-main'
assert schema['$id'] == 'dore.system-atlas.schema.v0'
assert atlas['governance']['schema'] == 'data/system-atlas.schema.json'
assert atlas['governance']['adrIndex'] == 'docs/adr/README.md'
assert atlas['governance']['mainline'] == 'docs/CURRENT_MAINLINE.md'
assert atlas['governance']['workRegister'] == 'dore-core/projects/DORÉ-MASTER-WORK-REGISTER.md'
assert atlas['governance']['memorySweep'] == 'dore-core/projects/DORÉ-MEMORY-CONSOLIDATION-SWEEP-01.md'
for path in atlas['governance'].values():
    assert (ROOT / path).exists(), f'missing governance path {path}'

entities = atlas['entities']
ids = [item['id'] for item in entities]
assert len(entities) >= 10
assert len(ids) == len(set(ids)), 'system atlas IDs must be unique'
by_id = {item['id']: item for item in entities}
id_pattern = re.compile(r'^[a-z][a-z0-9-]*:[a-z0-9][a-z0-9-]*$')

required = {
    'system:main-site', 'system:journal', 'system:mount-of-olives', 'system:church',
    'system:dawn-library', 'system:paradise-cinema', 'tool:one', 'tool:dore-folio',
    'capability:dore-search', 'system:dore-memory', 'system:a2a', 'capability:emergence',
    'register:master-work', 'authority:bible-index', 'authority:system-atlas',
    'authority:github-canonical'
}
assert required <= set(ids)

for item in entities:
    assert id_pattern.match(item['id']), f"unstable/invalid system id {item['id']}"
    assert item['kind'] and item['name']
    for rel in item.get('relations', []):
        assert rel['target'] in by_id, f"unknown relation target {rel['target']} from {item['id']}"
    for doc in item.get('docs', []):
        assert (ROOT / doc).exists(), f"missing canonical doc {doc} for {item['id']}"
    for root in item.get('roots', []):
        assert (ROOT / root).exists(), f"missing root {root} for {item['id']}"

# Branches/PRs are provenance, never stable system identity or canonical location.
serialized = json.dumps(atlas).lower()
for forbidden in ('refs/heads/', '/pull/', 'pr #'):
    assert forbidden not in serialized, f'transient identity leaked into atlas: {forbidden}'

# Every non-authority entity resolves current truth through GitHub canonical records.
for item in entities:
    if item['kind'] == 'authority':
        continue
    assert any(
        rel['type'] == 'canonical-record' and rel['target'] == 'authority:github-canonical'
        for rel in item.get('relations', [])
    ), f"{item['id']} lacks canonical-record relation"

# Bible is the shared content/world coordinate authority for core products.
for entity_id in ('system:dawn-library', 'system:paradise-cinema', 'tool:one', 'tool:dore-folio'):
    assert any(
        rel['type'] == 'indexed-by' and rel['target'] == 'authority:bible-index'
        for rel in by_id[entity_id]['relations']
    ), f'{entity_id} is not indexed by Bible Index'

# Memory recalls canonical truth; the existing Master Work Register is the operational
# reconciliation map, so System Atlas must connect to it instead of creating a second sweep.
memory_relations = by_id['system:dore-memory']['relations']
assert any(r['type'] == 'retrieves-from' and r['target'] == 'authority:github-canonical' for r in memory_relations)
assert any(r['type'] == 'must-not-replace' and r['target'] == 'authority:github-canonical' for r in memory_relations)
assert any(r['type'] == 'reconciled-by' and r['target'] == 'register:master-work' for r in memory_relations)
register = by_id['register:master-work']
assert register['kind'] == 'register'
assert atlas['governance']['workRegister'] in register['docs']
assert atlas['governance']['memorySweep'] in register['docs']

# A2A executes against the atlas but is not the memory owner.
a2a_relations = by_id['system:a2a']['relations']
assert any(r['type'] == 'executes-against' and r['target'] == 'authority:system-atlas' for r in a2a_relations)
assert any(r['type'] == 'must-not-own-memory' and r['target'] == 'system:dore-memory' for r in a2a_relations)

# The accepted architecture decision and the temporary detour return marker must remain discoverable.
adr = (ROOT / 'docs/adr/ADR-0001-two-index-authority-model.md').read_text()
mainline = (ROOT / 'docs/CURRENT_MAINLINE.md').read_text()
sweep = (ROOT / atlas['governance']['memorySweep']).read_text()
assert 'Status: accepted' in adr
assert 'Bible Index' in adr and 'System Atlas' in adr
assert 'Master Work Register' in adr
assert 'Paradise Cinema' in adr and 'Doré Emergence' in adr
assert 'Paradise' in mainline or '天堂' in mainline
assert 'Primary index' in sweep and 'DORÉ-MASTER-WORK-REGISTER.md' in sweep

print(f"DORE_SYSTEM_ATLAS=PASS entities={len(entities)} authorities=3 register=master-work")
