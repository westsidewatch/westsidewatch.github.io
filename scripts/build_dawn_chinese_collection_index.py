#!/usr/bin/env python3
"""Publish the Chinese Collection as a Dawn-derived index, never a hand list."""
from __future__ import annotations

import json
import hashlib
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLSC = ROOT / 'data/dawn-corpus/acquisition/zh-non-bible/clsc-pre1931-expanded-canonical-batch.v1.json'
SONG = ROOT / 'data/dawn-corpus/acquisition/zh-non-bible/song-shangjie-lingli-jiguang.v1.json'
OUT = ROOT / 'static/dawn-library/chinese-collection.json'


def load(path):
    return json.loads(path.read_text(encoding='utf-8'))


def main():
    clsc, song = load(CLSC), load(SONG)
    source = clsc['source']
    works = []
    for row in clsc['works']:
        stable = hashlib.sha256(f"{row['title']}|{row.get('author', '')}|{row.get('year', '')}".encode()).hexdigest()[:16]
        work_id = f'dawn:zh:clsc:{stable}'
        works.append({
            'workId': work_id, 'title': row['title'], 'creator': row.get('author', ''),
            'year': row.get('year'), 'domain': row['domain'],
            'identity': {'state': 'canonical', 'source': 'CLSC pre-1931 canonical batch'},
            'rights': 'public-domain-per-source-year-policy',
            'reading': {'state': 'lookup-required', 'provider': source['name'], 'url': source['collectionUrl']},
            'cover': {'state': 'unresolved', 'pointer': f"dawn://cover/{work_id}"}
        })
    work = song['work']
    works.insert(0, {
        'workId': 'dawn:zh:lingli-jiguang', 'title': work['titleTraditional'], 'creator': work['author'],
        'year': None, 'domain': 'biography/testimony/diary/reflection',
        'identity': {'state': 'promotable-source-verified', 'source': 'Project Gutenberg'},
        'rights': song['rights']['sourceStatement'],
        'reading': {'state': 'ready', 'provider': 'Project Gutenberg', 'url': song['source']['readOnline']},
        'cover': {'state': 'source-resolved', 'src': 'https://www.gutenberg.org/cache/epub/25716/pg25716.cover.medium.jpg', 'pointer': 'dawn://cover/dawn:zh:lingli-jiguang'}
    })
    domains = Counter(row['domain'] for row in works)
    years = defaultdict(list)
    for row in works:
        if row['year']:
            years[str(row['year'])].append(row['workId'])
    index = {
        'schema': 'dawn.library.collection-index.v1', 'collectionId': 'zh',
        'title': '中文館藏', 'count': len(works),
        'authority': 'Dawn canonical work/edition/cover/pointer substrate',
        'source': {'name': source['name'], 'url': source['collectionUrl'], 'delivery': 'remote-first'},
        'policy': {'bibleWorldExcluded': True, 'localTextDownloaded': False, 'identityRule': 'Work identity is independent of delivery endpoint resolution.'},
        'facets': {'domain': dict(sorted(domains.items())), 'year': dict(sorted(years.items()))},
        'works': works
    }
    OUT.write_text(json.dumps(index, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
