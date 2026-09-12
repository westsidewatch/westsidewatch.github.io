#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'static/dawn-library/biblical-world/discovery-candidates.json'
OUT = ROOT / 'data/dawn-10k-work-queue.json'


def norm(text: str) -> str:
    text = unicodedata.normalize('NFKC', text or '').casefold().strip()
    text = re.sub(r'[^\w\s-]+', ' ', text)
    return re.sub(r'\s+', ' ', text).strip()


def work_key(item: dict) -> str:
    title = norm(item.get('title', ''))
    author = norm(item.get('author', ''))
    return f'{title}::{author}'


def main() -> int:
    source = json.loads(SOURCE.read_text())
    previous = {}
    if OUT.exists():
        previous_data = json.loads(OUT.read_text())
        previous = {item['queueId']: item for item in previous_data.get('items', [])}

    grouped: dict[str, dict] = {}
    for candidate in source.get('items', []):
        key = work_key(candidate)
        if not key.split('::', 1)[0]:
            continue
        entry = grouped.setdefault(key, {
            'queueId': f'work::{key}',
            'title': candidate.get('title', ''),
            'author': candidate.get('author', ''),
            'languages': [],
            'providers': [],
            'pointers': [],
            'relations': [],
            'status': 'pending-reconciliation',
            'checkpoint': 0,
        })
        provider = candidate.get('provider')
        if provider and provider not in entry['providers']:
            entry['providers'].append(provider)
        pointer = candidate.get('sourceUrl')
        if pointer and pointer not in entry['pointers']:
            entry['pointers'].append(pointer)
        for relation in candidate.get('suggestedRelations', []):
            if relation not in entry['relations']:
                entry['relations'].append(relation)

    items = []
    for key in sorted(grouped):
        item = grouped[key]
        old = previous.get(item['queueId'])
        if old:
            item['status'] = old.get('status', item['status'])
            item['checkpoint'] = old.get('checkpoint', item['checkpoint'])
            for field in ('workId', 'authorityIds', 'languages', 'notes'):
                if field in old:
                    item[field] = old[field]
        items.append(item)

    report = {
        'schema': 'dawn.library.10k-work-queue.v1',
        'targetWorks': 10000,
        'source': str(SOURCE.relative_to(ROOT)),
        'sourceCandidates': len(source.get('items', [])),
        'deduplicatedWorks': len(items),
        'checkpointRule': 'Existing queue status, workId, authorityIds and checkpoint survive rebuilds.',
        'admission': 'none; this queue is technical reconciliation input only',
        'items': items,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({
        'sourceCandidates': report['sourceCandidates'],
        'deduplicatedWorks': report['deduplicatedWorks'],
        'targetWorks': report['targetWorks'],
    }, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
