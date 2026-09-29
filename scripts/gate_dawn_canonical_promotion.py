#!/usr/bin/env python3
from __future__ import annotations

import json
import os
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / 'data/dawn-resource-queue.json'
CANONICAL = ROOT / 'static/dawn-library/canonical-resource-index.json'
REPORT = ROOT / 'data/dawn-promotion-gate-report.json'
MAX_BATCH = max(1, int(os.environ.get('DAWN_PROMOTION_BATCH', '250')))

SURFACE_ROUTES = {
    'work': ['dawn-library'],
    'book': ['dawn-library'],
    'publication': ['dawn-library'],
    'bible': ['emmaus'],
    'commentary': ['emmaus'],
    'study': ['emmaus'],
    'map': ['emmaus', 'jerusalem-3000'],
    'place': ['emmaus', 'jerusalem-3000'],
    'manuscript': ['emmaus', 'dawn-library'],
    'sermon': ['olive-mountain'],
    'audio': ['olive-mountain', 'cinema'],
    'video': ['cinema', 'olive-mountain'],
    'film': ['cinema'],
    'image': ['resource-fabric'],
    'dataset': ['dore', 'resource-fabric'],
    'tool': ['dore'],
    'api': ['dore'],
    'resource': ['resource-fabric'],
}


def load(path: Path, fallback=None):
    if not path.exists():
        return {} if fallback is None else fallback
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


def identity(item: dict) -> str:
    return text(item.get('resourceId') or item.get('workId') or item.get('id'))


def canonical_ids(payload) -> set[str]:
    resources = payload.get('resources') if isinstance(payload, dict) else None
    if isinstance(resources, dict):
        return {text(key) for key in resources if text(key)}
    return {identity(item) for item in rows(payload) if isinstance(item, dict) and identity(item)}


def resource_type(item: dict) -> str:
    return text(item.get('resourceType') or 'resource').lower()


def routes_for(item: dict) -> list[str]:
    kind = resource_type(item)
    routes = list(SURFACE_ROUTES.get(kind, ['resource-fabric']))
    relations = [text(x).lower() for x in (item.get('relations') or []) if text(x)]
    hay = ' '.join([kind, text(item.get('title')).lower(), *relations])
    if any(token in hay for token in ('bible', 'scripture', 'commentary', 'biblical', 'theology', 'study')) and 'emmaus' not in routes:
        routes.append('emmaus')
    if any(token in hay for token in ('jerusalem', 'map', 'geo', 'place')) and 'jerusalem-3000' not in routes:
        routes.append('jerusalem-3000')
    return routes


def eligible(item: dict) -> tuple[bool, list[str]]:
    reasons = []
    rid = identity(item)
    title = text(item.get('title'))
    providers = item.get('providers') or ([item.get('provider')] if item.get('provider') else [])
    pointers = item.get('pointers') or [p for p in (item.get('readingPointer'), item.get('editionPointer'), item.get('workPointer')) if p]
    status = text(item.get('status') or item.get('disposition')).lower()
    admission = text(item.get('admission')).lower()
    if not rid: reasons.append('missing-resource-id')
    if not title: reasons.append('missing-title')
    if not providers: reasons.append('missing-provider')
    if not pointers: reasons.append('missing-pointer')
    if admission in {'none', 'rejected', 'blocked'}: reasons.append('not-admitted')
    if status in {'duplicate', 'rejected', 'deferred', 'blocked'}: reasons.append(f'status:{status}')
    return not reasons, reasons


def main() -> int:
    payload = load(QUEUE)
    candidates = rows(payload)
    existing_ids = canonical_ids(load(CANONICAL, {'resources': {}}))
    eligible_new, eligible_existing, blocked = [], [], []
    reason_counts: Counter[str] = Counter()
    type_counts: Counter[str] = Counter()
    route_counts: Counter[str] = Counter()

    for item in candidates:
        if not isinstance(item, dict):
            continue
        kind = resource_type(item)
        type_counts[kind] += 1
        ok, reasons = eligible(item)
        if ok:
            routes = routes_for(item)
            for route in routes:
                route_counts[route] += 1
            accepted_row = {
                'resourceId': identity(item),
                'resourceType': kind,
                'routes': routes,
            }
            if accepted_row['resourceId'] in existing_ids:
                eligible_existing.append(accepted_row)
            else:
                eligible_new.append(accepted_row)
        else:
            reason_counts.update(reasons)
            blocked.append({
                'resourceId': identity(item),
                'resourceType': kind,
                'reasons': reasons,
            })

    # Growth-first selection: fill every batch with resources that are not yet
    # canonical before spending remaining capacity refreshing existing records.
    ordered = eligible_new + eligible_existing
    accepted = ordered[:MAX_BATCH]
    selected_new = sum(1 for item in accepted if item['resourceId'] not in existing_ids)
    selected_existing = len(accepted) - selected_new
    total_eligible = len(ordered)

    report = {
        'schema': 'dawn.resource-fabric.promotion-gate.v3',
        'selectionPolicy': 'uncatalogued-first',
        'inputCandidates': len(candidates),
        'canonicalBaseline': len(existing_ids),
        'batchLimit': MAX_BATCH,
        'eligible': len(accepted),
        'eligibleUncatalogued': len(eligible_new),
        'eligibleExisting': len(eligible_existing),
        'selectedUncatalogued': selected_new,
        'selectedExisting': selected_existing,
        'blocked': len(blocked),
        'remainingEligible': max(0, total_eligible - len(accepted)),
        'resourceTypeCounts': dict(type_counts.most_common()),
        'surfaceRouteCounts': dict(route_counts.most_common()),
        'blockedReasonCounts': dict(reason_counts.most_common()),
        'acceptedResources': accepted,
        'acceptedResourceIds': [x['resourceId'] for x in accepted],
        'acceptedWorkIds': [x['resourceId'] for x in accepted if x['resourceType'] in {'work', 'book', 'publication'}],
        'blockedRecords': blocked[:500],
    }
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({
        'inputCandidates': report['inputCandidates'],
        'canonicalBaseline': report['canonicalBaseline'],
        'eligible': report['eligible'],
        'eligibleUncatalogued': report['eligibleUncatalogued'],
        'eligibleExisting': report['eligibleExisting'],
        'selectedUncatalogued': report['selectedUncatalogued'],
        'selectedExisting': report['selectedExisting'],
        'blocked': report['blocked'],
        'remainingEligible': report['remainingEligible'],
        'resourceTypeCounts': report['resourceTypeCounts'],
        'surfaceRouteCounts': report['surfaceRouteCounts'],
        'blockedReasonCounts': report['blockedReasonCounts'],
    }, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
