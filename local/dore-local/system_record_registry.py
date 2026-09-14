#!/usr/bin/env python3
import fnmatch
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PATH = ROOT / 'data/system-record-families/manifest.v1.json'


def load_json(rel):
    return json.loads((ROOT / rel).read_text())


def load_registry():
    manifest = json.loads(MANIFEST_PATH.read_text())
    assert manifest['schema'] == 'dore.system-record-family-manifest.v1'
    base = load_json(manifest['base'])
    states = set(manifest['states'])

    families = []
    for family in base['families']:
        item = dict(family)
        item['_priority'] = 0
        item['_source'] = manifest['base']
        families.append(item)

    active_ids = set()
    for shard_path in manifest.get('shards', []):
        shard = load_json(shard_path)
        assert shard['schema'] == 'dore.system-record-family-shard.v1'
        priority = int(shard.get('priority', 10))
        for family in shard['families']:
            assert family['id'] not in active_ids, f"duplicate active shard family {family['id']}"
            active_ids.add(family['id'])
            assert family['state'] in states
            item = dict(family)
            item['_priority'] = priority
            item['_source'] = shard_path
            families.append(item)

    base_by_id = {item['id']: item for item in base['families']}
    for mirror_path in manifest.get('mirrors', []):
        mirror = load_json(mirror_path)
        assert mirror['schema'] == 'dore.system-record-family-shard.v1'
        for family in mirror['families']:
            assert family['id'] in base_by_id, f"mirror family missing from base: {family['id']}"
            assert family == base_by_id[family['id']], f"mirror drift: {family['id']}"

    return manifest, families


def family_matches(family):
    matches = set()
    for pattern in family['patterns']:
        matches |= {p.relative_to(ROOT).as_posix() for p in ROOT.glob(pattern)}
    return matches


def resolve_paths(families):
    candidates = {}
    for family in families:
        for path in family_matches(family):
            candidates.setdefault(path, []).append(family)

    resolved = {}
    for path, matches in candidates.items():
        highest = max(item['_priority'] for item in matches)
        winners = [item for item in matches if item['_priority'] == highest]
        states = {item['state'] for item in winners}
        assert len(states) == 1, f"same-priority state conflict for {path}: {sorted(states)}"
        resolved[path] = {
            'state': next(iter(states)),
            'families': sorted(item['id'] for item in winners),
            'priority': highest,
            'sources': sorted({item['_source'] for item in winners}),
        }
    return resolved


if __name__ == '__main__':
    manifest, families = load_registry()
    resolved = resolve_paths(families)
    print(f"DORE_RECORD_REGISTRY=PASS families={len(families)} resolved={len(resolved)} shards={len(manifest.get('shards', []))}")
