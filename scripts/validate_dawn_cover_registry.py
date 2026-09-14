#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATIC_ROOT = ROOT / 'static'
REGISTRY = STATIC_ROOT / 'dawn-library/cover-registry.json'
FORBIDDEN_RUNTIME = ('openlibrary.org', 'wikisource', 'zh.wikisource.org')


def main() -> int:
    payload = json.loads(REGISTRY.read_text(encoding='utf-8'))
    candidate_count = int(payload.get('candidateCount') or 0)
    resolved = int(payload.get('resolvedCount') or 0)
    failed = int(payload.get('failedCount') or 0)
    collisions = int(payload.get('identityCollisionCount') or 0)
    if resolved + failed + collisions != candidate_count:
        raise SystemExit('cover registry accounting mismatch')
    if int(payload.get('candidateRowCount') or 0) - candidate_count != int(payload.get('duplicateCandidateCount') or 0):
        raise SystemExit('cover duplicate accounting mismatch')
    covers = payload.get('covers') or {}
    if len(covers) != resolved:
        raise SystemExit('resolvedCount does not match cover rows')
    for work_id, row in covers.items():
        pointer = str((row or {}).get('pointer') or '')
        lower = pointer.casefold()
        if not pointer.startswith('/dawn-library/covers/'):
            raise SystemExit(f'non-local canonical cover pointer: {work_id}')
        if any(token in lower for token in FORBIDDEN_RUNTIME):
            raise SystemExit(f'forbidden runtime dependency: {work_id}')
        # Public site pointers are rooted at Hugo's static/ directory before build.
        path = STATIC_ROOT / pointer.lstrip('/')
        if not path.is_file():
            raise SystemExit(f'missing canonical cover asset: {work_id}: {path.relative_to(ROOT)}')
        if path.stat().st_size > 8 * 1024 * 1024:
            raise SystemExit(f'canonical cover exceeds 8 MiB: {work_id}')
    collision_ids = [c.get('workId') for c in payload.get('identityCollisions') or []]
    if len(collision_ids) != len(set(collision_ids)) or len(collision_ids) != collisions:
        raise SystemExit('identity collision accounting mismatch')
    print(json.dumps({
        'candidateRows': payload.get('candidateRowCount'),
        'uniqueCandidates': candidate_count,
        'duplicates': payload.get('duplicateCandidateCount'),
        'resolved': resolved,
        'failed': failed,
        'identityCollisions': collisions,
    }, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
