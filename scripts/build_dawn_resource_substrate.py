#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / 'data/dawn-resource-queue.json'
OUT = ROOT / 'static/dawn-library/canonical-resource-index.json'
SURFACE = ROOT / 'static/dawn-library/surfaces/dawn-resources.json'


def main() -> int:
    queue = json.loads(QUEUE.read_text(encoding='utf-8'))
    if queue.get('schema') != 'dawn.library.resource-queue.v1':
        raise SystemExit('resource queue missing or schema mismatch')
    resources = {}
    for row in queue.get('items', []):
        rid = str(row.get('resourceId') or '').strip()
        if not rid:
            continue
        resources[rid] = {
            'resourceId': rid,
            'resourceType': row.get('resourceType') or 'resource',
            'title': row.get('title') or '',
            'authors': row.get('authors') or [],
            'languages': row.get('languages') or [],
            'authorityIds': row.get('authorityIds') or {},
            'providers': row.get('providers') or [],
            'pointers': row.get('pointers') or [],
            'relations': row.get('relations') or [],
            'rights': row.get('rights'),
            'provenance': row.get('provenance') or {},
            'status': row.get('status')
        }
    index = {
        'schema': 'dawn.library.canonical-resource-index.v1',
        'identityAuthority': 'Dawn',
        'runtimePolicy': {'wikisource': 'forbidden', 'surfaceOwnsIdentity': False},
        'resourceCount': len(resources),
        'resources': dict(sorted(resources.items()))
    }
    refs = [{'resourceId': rid} for rid, row in resources.items() if row.get('resourceType') != 'work']
    surface = {
        'schema': 'dawn.library.resource-surface.v1',
        'surfaceId': 'dawn-resources',
        'canonicalIndex': '../canonical-resource-index.json',
        'title': '黎明書局 · Resources',
        'items': refs
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    SURFACE.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(index, ensure_ascii=False, separators=(',', ':')) + '\n', encoding='utf-8')
    SURFACE.write_text(json.dumps(surface, ensure_ascii=False, separators=(',', ':')) + '\n', encoding='utf-8')
    print(json.dumps({'resourceCount': len(resources), 'surfaceRefs': len(refs)}, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
