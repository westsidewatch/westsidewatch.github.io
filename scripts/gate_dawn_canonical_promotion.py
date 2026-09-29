#!/usr/bin/env python3
from __future__ import annotations

import json
import os
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / 'data/dawn-resource-queue.json'
REPORT = ROOT / 'data/dawn-promotion-gate-report.json'
MAX_BATCH = max(1, int(os.environ.get('DAWN_PROMOTION_BATCH', '250')))


def load(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


def rows(payload):
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for key in ('items', 'resources', 'queue', 'works'):
            value = payload.get(key)
            if isinstance(value, list):
                return value
    return []


def text(value):
    return str(value or '').strip()


def eligible(item: dict) -> tuple[bool, list[str]]:
    reasons = []
    work_id = text(item.get('workId') or item.get('id'))
    title = text(item.get('title'))
    provider = text(item.get('provider') or item.get('source'))
    pointer = item.get('readingPointer') or item.get('editionPointer') or item.get('workPointer')
    admission = text(item.get('admission')).lower()
    disposition = text(item.get('disposition') or item.get('status')).lower()
    if not work_id: reasons.append('missing-work-id')
    if not title: reasons.append('missing-title')
    if not provider: reasons.append('missing-provider')
    if not pointer: reasons.append('missing-reading-pointer')
    if admission in {'none', 'rejected', 'blocked'}: reasons.append('not-admitted')
    if disposition in {'duplicate', 'rejected', 'deferred', 'blocked'}: reasons.append(f'disposition:{disposition}')
    return not reasons, reasons


def main() -> int:
    payload = load(QUEUE)
    candidates = rows(payload)
    accepted, blocked = [], []
    reason_counts: Counter[str] = Counter()
    total_eligible = 0
    for item in candidates:
        if not isinstance(item, dict):
            continue
        ok, reasons = eligible(item)
        if ok:
            total_eligible += 1
            if len(accepted) < MAX_BATCH:
                accepted.append(item)
        else:
            reason_counts.update(reasons)
            blocked.append({'workId': item.get('workId') or item.get('id'), 'reasons': reasons})
    report = {
        'schema': 'dawn.library.promotion-gate.v1',
        'inputCandidates': len(candidates),
        'batchLimit': MAX_BATCH,
        'eligible': len(accepted),
        'blocked': len(blocked),
        'remainingEligible': max(0, total_eligible - len(accepted)),
        'blockedReasonCounts': dict(reason_counts.most_common()),
        'acceptedWorkIds': [x.get('workId') or x.get('id') for x in accepted],
        'blockedRecords': blocked[:500],
    }
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({
        'inputCandidates': report['inputCandidates'],
        'eligible': report['eligible'],
        'blocked': report['blocked'],
        'remainingEligible': report['remainingEligible'],
        'blockedReasonCounts': report['blockedReasonCounts'],
    }, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
