#!/usr/bin/env python3
"""Persist Dawn canonical Works below GitHub's single-file limit.

The monolithic canonical-index remains a build-time compatibility input during the
migration. This writer projects the exact same canonical authority into stable,
bounded shards plus a compact root manifest. Sharding has no admission authority.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANON = ROOT / 'static/dawn-library/canonical-index.json'
OUT = ROOT / 'static/dawn-library/canonical'
SHARD_SIZE = int(os.environ.get('DAWN_CANONICAL_SHARD_SIZE', '10000'))


def compact_bytes(payload: dict) -> bytes:
    return (json.dumps(payload, ensure_ascii=False, separators=(',', ':')) + '\n').encode('utf-8')


def main() -> int:
    canonical = json.loads(CANON.read_text(encoding='utf-8'))
    works = canonical.get('works') or {}
    if canonical.get('workCount') != len(works):
        raise SystemExit('canonical workCount mismatch before sharding')
    if SHARD_SIZE < 1000 or SHARD_SIZE > 25000:
        raise SystemExit('DAWN_CANONICAL_SHARD_SIZE must be between 1000 and 25000')

    OUT.mkdir(parents=True, exist_ok=True)
    ordered = sorted(works.items())
    manifest = []
    keep = {'root.json'}
    seen = 0
    for number, offset in enumerate(range(0, len(ordered), SHARD_SIZE), start=1):
        chunk = ordered[offset:offset + SHARD_SIZE]
        name = f'works-{number:06d}.json'
        keep.add(name)
        payload = {
            'schema': 'dawn.library.canonical-shard.v1',
            'identityAuthority': 'Dawn',
            'admissionAuthority': False,
            'offset': offset,
            'workCount': len(chunk),
            'works': {work_id: work for work_id, work in chunk},
        }
        raw = compact_bytes(payload)
        (OUT / name).write_bytes(raw)
        manifest.append({
            'offset': offset,
            'workCount': len(chunk),
            'href': name,
            'sha256': hashlib.sha256(raw).hexdigest(),
            'firstWorkId': chunk[0][0],
            'lastWorkId': chunk[-1][0],
        })
        seen += len(chunk)

    for path in OUT.glob('works-*.json'):
        if path.name not in keep:
            path.unlink()

    root = {
        'schema': 'dawn.library.canonical-root.v1',
        'identityAuthority': canonical.get('identityAuthority') or 'Dawn',
        'runtimePolicy': canonical.get('runtimePolicy') or {},
        'step6Baseline': canonical.get('step6Baseline') or {},
        'workCount': canonical.get('workCount'),
        'authorityBackedWorks': canonical.get('authorityBackedWorks'),
        'shardSize': SHARD_SIZE,
        'shardCount': len(manifest),
        'shards': manifest,
        'migration': {
            'monolith': '../canonical-index.json',
            'monolithRole': 'build-time-compatibility-only',
            'canonicalRuntime': 'root-and-shards',
        },
    }
    if seen != root['workCount']:
        raise SystemExit('canonical shard coverage mismatch')
    (OUT / 'root.json').write_bytes(compact_bytes(root))
    print(json.dumps({
        'canonicalWorkCount': seen,
        'authorityBackedWorks': root['authorityBackedWorks'],
        'canonicalShards': len(manifest),
        'shardSize': SHARD_SIZE,
    }, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
