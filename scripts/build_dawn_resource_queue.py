#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEGACY = ROOT / 'data/dawn-10k-work-queue.json'
CORPUS = ROOT / 'data/dawn-corpus/bulk'
RECORDS = ROOT / 'data/dawn-corpus/records'
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
                items.append({
                    'resourceId': stable_id(f'corpus::{sid}'),
                    'resourceType': infer_type(source, path.name),
                    'title': name,
                    'authors': [], 'languages': [],
                    'authorityIds': {'corpusSource': sid},
                    'providers': [name],
                    'pointers': [v for v in [source.get('upstream'), source.get('iiifManifestPattern'), source.get('clone')] if v],
                    'relations': list(dict.fromkeys(source.get('targetScope', []) + source.get('scope', []))),
                    'rights': source.get('rights') or source.get('imagePolicy'),
                    'provenance': {'source': str(path.relative_to(ROOT)), 'sourceId': sid},
                    'status': 'corpus-source-established'
                })

    # Harvested records are the actual canonical growth units. External manifests remain
    # evidence/pointers; Dawn owns only the local canonical Resource identity.
    if RECORDS.exists():
        for path in sorted(RECORDS.glob('*.json')):
            doc = json.loads(path.read_text(encoding='utf-8'))
            if doc.get('schema') != 'dawn.corpus.records.v1':
                continue
            source_id = str(doc.get('sourceId') or '').strip()
            resource_type = str(doc.get('resourceType') or 'resource').strip()
            rights = doc.get('rightsPolicy')
            for row in doc.get('items', []):
                source_record_id = str(row.get('sourceRecordId') or '').strip()
                title = str(row.get('title') or '').strip()
                if not source_id or not source_record_id or not title:
                    continue
                serialized = json.dumps(row, ensure_ascii=False).lower()
                if 'wikisource' in serialized:
                    continue
                rid = stable_id(f'{source_id}::{source_record_id}')
                items.append({
                    'resourceId': rid,
                    'resourceType': resource_type,
                    'title': title,
                    'authors': row.get('authors') or [],
                    'languages': [row['language']] if row.get('language') else [],
                    'authorityIds': {'source': source_id, 'sourceRecord': source_record_id, 'shelfmark': row.get('shelfmark')},
                    'providers': [source_id],
                    'pointers': [v for v in [row.get('manifest'), row.get('record')] if v],
                    'relations': row.get('relations') or [],
                    'rights': rights,
                    'dateLabel': row.get('dateLabel'),
                    'provenance': {'source': str(path.relative_to(ROOT)), 'sourceId': source_id, 'sourceRecordId': source_record_id},
                    'status': 'identity-established'
                })

    unique = {item['resourceId']: item for item in items}
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
