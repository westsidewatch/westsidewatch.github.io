#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / 'data/dawn-resource-queue.json'
GATE = ROOT / 'data/dawn-promotion-gate-report.json'
CURRENT = ROOT / 'static/dawn-library/canonical-resource-index.json'
OUT = ROOT / 'data/dawn-promoted-canonical-resource-index.json'
REPORT = ROOT / 'data/dawn-promotion-batch-report.json'


def load(path: Path, fallback=None):
    if not path.exists():
        return {} if fallback is None else fallback
    return json.loads(path.read_text(encoding='utf-8'))


def queue_items(payload):
    if isinstance(payload, dict):
        return payload.get('items') or payload.get('resources') or []
    return payload if isinstance(payload, list) else []


def canonicalize(row: dict) -> tuple[str, dict] | None:
    rid = str(row.get('resourceId') or row.get('workId') or row.get('id') or '').strip()
    if not rid:
        return None
    return rid, {
        'resourceId': rid,
        'resourceType': row.get('resourceType') or 'work',
        'title': row.get('title') or '',
        'authors': row.get('authors') or [],
        'languages': row.get('languages') or [],
        'authorityIds': row.get('authorityIds') or {},
        'providers': row.get('providers') or ([row.get('provider')] if row.get('provider') else []),
        'pointers': row.get('pointers') or [p for p in (row.get('readingPointer'), row.get('editionPointer'), row.get('workPointer')) if p],
        'relations': row.get('relations') or [],
        'rights': row.get('rights'),
        'provenance': row.get('provenance') or {},
        'status': 'canonical'
    }


def main() -> int:
    queue = load(QUEUE)
    gate = load(GATE)
    accepted = {str(x) for x in gate.get('acceptedWorkIds', []) if x}
    existing = load(CURRENT, {'resources': {}})
    resources = dict(existing.get('resources') or {})
    by_identity = {}
    for row in queue_items(queue):
        if not isinstance(row, dict):
            continue
        identities = {str(x) for x in (row.get('workId'), row.get('resourceId'), row.get('id')) if x}
        if identities & accepted:
            result = canonicalize(row)
            if result:
                by_identity[result[0]] = result[1]
    inserted = 0
    updated = 0
    for rid, resource in by_identity.items():
        if rid in resources:
            if resources[rid] != resource:
                resources[rid] = resource
                updated += 1
        else:
            resources[rid] = resource
            inserted += 1
    output = {
        'schema': 'dawn.library.canonical-resource-index.v1',
        'identityAuthority': 'Dawn',
        'runtimePolicy': {'wikisource': 'forbidden', 'surfaceOwnsIdentity': False},
        'resourceCount': len(resources),
        'resources': dict(sorted(resources.items()))
    }
    report = {
        'schema': 'dawn.library.promotion-batch.v1',
        'gateAccepted': len(accepted),
        'matchedQueueRows': len(by_identity),
        'inserted': inserted,
        'updated': updated,
        'unchangedOrUnmatched': max(0, len(accepted) - inserted - updated),
        'canonicalResourceCount': len(resources)
    }
    OUT.write_text(json.dumps(output, ensure_ascii=False, separators=(',', ':')) + '\n', encoding='utf-8')
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
