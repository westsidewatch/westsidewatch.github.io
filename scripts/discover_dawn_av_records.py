#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data/dawn-corpus/records/open-av-discovery.json'
LIMIT = max(1, min(200, int(os.environ.get('DAWN_AV_DISCOVERY_LIMIT', '50'))))
TIMEOUT = 20
UA = 'WestsideWatch-Dawn/1.0 metadata-only discovery'

QUERIES = (
    'bible', 'christian sermon', 'church history', 'jerusalem documentary'
)


def get_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': 'application/json'})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as response:
        return json.load(response)


def ia_records() -> list[dict]:
    query = ' OR '.join(f'({q})' for q in QUERIES)
    params = {
        'q': f'({query}) AND mediatype:(movies OR audio)',
        'fl[]': ['identifier', 'title', 'creator', 'mediatype', 'language', 'date'],
        'rows': str(LIMIT),
        'page': '1',
        'output': 'json',
    }
    url = 'https://archive.org/advancedsearch.php?' + urllib.parse.urlencode(params, doseq=True)
    data = get_json(url)
    records = []
    for row in data.get('response', {}).get('docs', []):
        identifier = str(row.get('identifier') or '').strip()
        title = str(row.get('title') or '').strip()
        if not identifier or not title:
            continue
        mediatype = str(row.get('mediatype') or '').lower()
        resource_type = 'audio' if mediatype == 'audio' else 'video'
        records.append({
            'sourceRecordId': identifier,
            'title': title,
            'authors': [row['creator']] if isinstance(row.get('creator'), str) else (row.get('creator') or []),
            'language': row.get('language') if isinstance(row.get('language'), str) else None,
            'record': f'https://archive.org/details/{urllib.parse.quote(identifier)}',
            'resourceType': resource_type,
            'sourceMediaType': mediatype or None,
            'relations': [resource_type],
            'dateLabel': str(row.get('date') or ''),
        })
    return records


def main() -> int:
    items = ia_records()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        'schema': 'dawn.corpus.records.v1',
        'sourceId': 'internet-archive-av',
        'resourceType': 'av',
        'resourceTypePolicy': 'record-level',
        'acquisitionMode': 'metadata-pointer-only',
        'contentDownloaded': False,
        'rightsPolicy': 'source-record; verify item rights before reuse',
        'itemCount': len(items),
        'items': items,
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'source': payload['sourceId'], 'itemCount': len(items), 'contentDownloaded': False, 'resourceTypePolicy': 'record-level', 'output': str(OUT.relative_to(ROOT))}, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
