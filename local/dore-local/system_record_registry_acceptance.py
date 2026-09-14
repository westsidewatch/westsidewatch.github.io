#!/usr/bin/env python3
from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('record_registry', ROOT / 'local/dore-local/system_record_registry.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
manifest, families = mod.load_registry()
resolved = mod.resolve_paths(families)

assert manifest['resolution'] == 'highest-priority-match'
assert manifest['shards'] == ['data/system-record-families/nested.v1.json']

nested_roots = [ROOT / 'docs/dore/design', ROOT / 'docs/dore/film', ROOT / 'docs/dore/lessons']
nested_paths = {p.relative_to(ROOT).as_posix() for root in nested_roots for p in root.rglob('*') if p.is_file()}
assert nested_paths
for path in nested_paths:
    assert path in resolved, f'orphan nested record: {path}'
    assert resolved[path]['state'] != 'unreviewed', f'unreviewed nested record: {path}'

expected = {
    'docs/dore/design/README.md': 'canonical',
    'docs/dore/design/.candidate01-4w-deploy-request': 'historical',
    'docs/dore/design/.candidate01-4w-deploy-marker': 'historical',
    'docs/dore/design/candidate01-4w-transparent-label-hotfix.md': 'historical',
    'docs/dore/film/README.md': 'canonical',
    'docs/dore/film/DORÉ-FILM-PRODUCTION-HANDBOOK.md': 'operational',
    'docs/dore/film/DORÉ-ANCHORED-WORLD-ROUTE-01.md': 'operational',
    'docs/dore/film/CAMERA-SPINE-EXPERIMENT-01-ACCEPTANCE.md': 'evidence',
    'docs/dore/film/EXPERIMENTAL-FILM-01.md': 'evidence',
    'docs/dore/lessons/README.md': 'canonical',
    'docs/dore/lessons/ONE-LESSON-001-GOSPEL-HARMONY-AUDIT.md': 'evidence'
}
for path, state in expected.items():
    assert resolved[path]['state'] == state, (path, resolved[path])

assert resolved['docs/dore/film/README.md']['priority'] == 100
remaining = [path for path, item in resolved.items() if item['state'] == 'unreviewed']
print(f'DORE_RECORD_REGISTRY_ACCEPTANCE=PASS nested={len(nested_paths)} remaining_unreviewed={len(remaining)} shards={len(manifest["shards"])}')
