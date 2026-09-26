#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEGACY = ROOT / 'data/dawn-10k-work-queue.json'
CORPUS = ROOT / 'data/dawn-corpus/bulk'
OUT = ROOT / 'data/dawn-resource-queue.json'

TYPE_MAP = {
    'iiif': 'manuscript', 'manuscript': 'manuscript', 'image': 'image',
    'audio': 'audio', 'video': 'video', 'map': 'map', 'geo': 'place',
    'sermon': 'audio', 'bible': 'work', 'book': 'work', 'text': 'work'
}


def stable_id(seed: str) -> str:
    return 'dawn-resource:' + hashlib.sha256(seed.encode('utf-8')).hexdigest()[:24]


def infer_type(source: dict, filename: str) -> str:
    hay = ' '.join([filename, source.get('id', ''), source.get('name', ''), *source.get('targetScope', []), *source.get('resourceTypes', [])]).lower()
    for token, kind in TYPE_MAP.items():
        if token in hay:
            return kind
    return 'resource'


def main() -> int:
    items = []
    if LEGACY.exists():
        legacy = json.loads(LEGACY.read_text(encoding='utf-8'))
        for row in legacy.get('items', []):
            items.append({
                'resourceId': str(row.get('workId') or stable_id(row.get('queueId', ''))),
                'resourceType': 'work',
                'title': row.get('title'),
                'authors': row.get('authors') or ([row.get('author')] if row.get('author') else []),
                'languages': row.get('languages') or [],
                'authorityIds': row.get('authorityIds') or {},
                'providers': row.get('providers') or [],
                'pointers': row.get('pointers') or [],
                'relations': row.get('relations') or [],
                'provenance': {'queueId': row.get('queueId'), 'source': 'data/dawn-10k-work-queue.json'},
                'status': row.get('status', 'identity-established')
            })

    # Bulk acquisition manifests are first-class corpus inputs. At this stage they create
    # source/resource collection identities; harvested records/manifests later expand under
    # these identities without inventing a second pipeline.
    if CORPUS.exists():
        for path in sorted(CORPUS.glob('*.json')):
            doc = json.loads(path.read_text(encoding='utf-8'))
            sources = doc.get('sources')
            if not isinstance(sources, list):
                source = doc.get('source')
                sources = [source] if isinstance(source, dict) else []
            for source in sources:
                sid = str(source.get('id') or '').strip()
                name = str(source.get('name') or sid).strip()
                if not sid or not name:
                    continue
                serialized = json.dumps(source, ensure_ascii=False).lower()
                if 'wikisource' in serialized and source.get('wikisourceAdmission') != 'forbidden':
                    continue
                rid = stable_id(f'corpus::{sid}')
                items.append({
                    'resourceId': rid,
                    'resourceType': infer_type(source, path.name),
                    'title': name,
                    'authors': [],
                    'languages': [],
                    'authorityIds': {'corpusSource': sid},
                    'providers': [name],
                    'pointers': [v for v in [source.get('upstream'), source.get('iiifManifestPattern'), source.get('clone')] if v],
                    'relations': list(dict.fromkeys(source.get('targetScope', []) + source.get('scope', []))),
                    'rights': source.get('rights') or source.get('imagePolicy'),
                    'provenance': {'source': str(path.relative_to(ROOT)), 'sourceId': sid},
                    'status': 'corpus-source-established'
                })

    unique = {}
    for item in items:
        unique[item['resourceId']] = item
    payload = {
        'schema': 'dawn.library.resource-queue.v1',
        'identityAuthority': 'Dawn',
        'legacyWorkCompatible': True,
        'wikisource': 'forbidden',
        'resourceCount': len(unique),
        'items': list(unique.values())
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'resourceCount': payload['resourceCount'], 'output': str(OUT.relative_to(ROOT))}, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
