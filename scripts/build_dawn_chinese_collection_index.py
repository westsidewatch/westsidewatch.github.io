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
PREVIEW_OUT = ROOT / 'static/dawn-library/cover-preview/chinese-collection.json'
COLLECTIONS = ROOT / 'static/dawn-library/collections.json'


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
            'workId': work_id,
            'work': {'title': row['title'], 'creator': row.get('author', ''), 'language': 'zh-Hant', 'form': 'book'},
            'edition': {'year': row.get('year'), 'provenance': 'CLSC pre-1931 canonical batch'},
            'classification': {'label': row['domain']},
            'rights': {'status': 'public-domain-per-source-year-policy', 'declaredBy': source['name']},
            'source': {'provider': source['name'], 'catalogUrl': source['collectionUrl'], 'delivery': 'remote-first'},
            'access': {'kind': 'catalogue', 'label': '查看館藏', 'url': source['collectionUrl']},
            'cover': {'mode': 'one-fallback', 'title': row['title'], 'creator': row.get('author', ''), 'pointer': f"dawn://cover/{work_id}"}
        })
    work = song['work']
    works.insert(0, {
        'workId': 'dawn:zh:lingli-jiguang',
        'work': {'title': work['titleTraditional'], 'creator': work['author'], 'language': 'zh-Hant', 'form': 'book'},
        'edition': {'provenance': 'Project Gutenberg'},
        'classification': {'label': 'biography/testimony/diary/reflection'},
        'rights': {'status': song['rights']['sourceStatement'], 'declaredBy': 'Project Gutenberg'},
        'source': {'provider': 'Project Gutenberg', 'catalogUrl': song['source']['readOnline'], 'delivery': 'remote-first'},
        'access': {'kind': 'full-text', 'label': '閱讀全文', 'url': song['source']['readOnline']},
        'cover': {'mode': 'source', 'url': 'https://www.gutenberg.org/cache/epub/25716/pg25716.cover.medium.jpg', 'title': work['titleTraditional'], 'creator': work['author'], 'pointer': 'dawn://cover/dawn:zh:lingli-jiguang'}
    })
    domains = Counter(row['classification']['label'] for row in works)
    years = defaultdict(list)
    for row in works:
        if row['edition'].get('year'):
            years[str(row['edition']['year'])].append(row['workId'])
    index = {
        'schema': 'dawn.library.collection-index.v1', 'collectionId': 'zh',
        'title': '中文館藏', 'count': len(works),
        'authority': 'Dawn canonical work / edition / cover / source substrate',
        'source': {'name': source['name'], 'url': source['collectionUrl'], 'delivery': 'remote-first'},
        'policy': {'bibleWorldExcluded': True, 'localTextDownloaded': False, 'identityRule': 'Work identity is independent of delivery endpoint resolution.', 'cardRule': 'Every card has a source cover or a Dawn one-fallback cover and a reader-facing access link.'},
        'facets': {'domain': dict(sorted(domains.items())), 'year': dict(sorted(years.items()))},
        'coverPreview': {'href': 'cover-preview/chinese-collection.json', 'schema': 'dawn.library.cover-preview-shard.v1', 'count': len(works)},
        'works': works
    }
    OUT.write_text(json.dumps(index, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    # This is a scoped member of the existing cover-preview-shard contract.  It
    # lets the Chinese Collection load 47 cover records directly instead of
    # scanning the 407 general-catalogue shards for every card.
    previews = []
    for row in works:
        cover = row['cover']
        previews.append({
            'workId': row['workId'],
            'motionKey': f"dawn-work:{row['workId']}",
            'title': row['work']['title'],
            'authors': [row['work']['creator']] if row['work']['creator'] else [],
            'languages': [row['work']['language']],
            'cover': {'src': cover.get('url'), 'source': 'source' if cover['mode'] == 'source' else 'dawn-placeholder', 'width': None, 'height': None, 'aspectRatio': None},
            'motion': {'layer': 'cover', 'detachable': True, 'layoutStable': False, 'preferredProperties': ['transform', 'opacity']}
        })
    PREVIEW_OUT.parent.mkdir(parents=True, exist_ok=True)
    PREVIEW_OUT.write_text(json.dumps({'schema': 'dawn.library.cover-preview-shard.v1', 'collectionId': 'zh', 'offset': 0, 'count': len(previews), 'items': previews}, ensure_ascii=False, separators=(',', ':')) + '\n', encoding='utf-8')
    # Register the projection in the same collection registry used by every
    # Dawn Library surface. A collection build may update its own counters,
    # but never creates a separate storefront runtime.
    registry = load(COLLECTIONS)
    entry = {'id': 'zh', 'title': '中文館藏', 'kind': 'books', 'status': 'active-building', 'published': len(works), 'fullText': sum(1 for row in works if row['access']['kind'] == 'full-text'), 'output': '/dawn-library/chinese-collection.json', 'coverPreview': '/dawn-library/cover-preview/chinese-collection.json', 'delivery': 'remote-first'}
    rows = [row for row in registry.get('collections', []) if row.get('id') != 'zh']
    registry['collections'] = [entry, *rows]
    COLLECTIONS.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
