#!/usr/bin/env python3
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
atlas=json.loads((ROOT/'data/system-atlas.v0.json').read_text())

assert atlas['schema']=='dore.system-atlas.v0'
entities=atlas['entities']
ids=[item['id'] for item in entities]
assert len(ids)==len(set(ids)), 'system atlas IDs must be unique'
by_id={item['id']:item for item in entities}

required={
  'system:main-site','system:journal','system:mount-of-olives','system:dawn-library',
  'system:paradise-cinema','tool:one','tool:dore-folio','capability:dore-search',
  'system:dore-memory','system:a2a','capability:emergence','authority:bible-index',
  'authority:system-atlas','authority:github-canonical'
}
assert required <= set(ids)

for item in entities:
    assert item['id'] and item['kind'] and item['name']
    for rel in item.get('relations',[]):
        assert rel['target'] in by_id, f"unknown relation target {rel['target']} from {item['id']}"
    for doc in item.get('docs',[]):
        assert (ROOT/doc).exists(), f"missing canonical doc {doc} for {item['id']}"
    for root in item.get('roots',[]):
        assert (ROOT/root).exists(), f"missing root {root} for {item['id']}"

# Identity must not be tied to transient branch or PR names.
serialized=json.dumps(atlas).lower()
assert 'refs/heads/' not in serialized
assert 'pull/' not in serialized
assert 'pr #' not in serialized

# Architectural boundaries.
assert any(r['type']=='indexed-by' and r['target']=='authority:bible-index' for r in by_id['system:dawn-library']['relations'])
assert any(r['type']=='indexed-by' and r['target']=='authority:bible-index' for r in by_id['system:paradise-cinema']['relations'])
assert any(r['type']=='indexed-by' and r['target']=='authority:bible-index' for r in by_id['tool:one']['relations'])
assert any(r['type']=='indexed-by' and r['target']=='authority:bible-index' for r in by_id['tool:dore-folio']['relations'])
assert any(r['type']=='recalls' and r['target']=='authority:github-canonical' for r in by_id['system:dore-memory']['relations'])
assert any(r['type']=='executes-from' and r['target']=='authority:system-atlas' for r in by_id['system:a2a']['relations'])

print(f"DORE_SYSTEM_ATLAS=PASS entities={len(entities)}")
