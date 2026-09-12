#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data/dawn-10k-openlibrary-works.json'
API = 'https://openlibrary.org/search.json'
UA = 'Dore-Dawn-Library/1.2 (+https://westsidewatch.github.io; metadata-only)'
TARGET = int(os.environ.get('DAWN_TARGET_WORKS', '10500'))
CHINESE_TARGET = int(os.environ.get('DAWN_CHINESE_TARGET', '2000'))
PAGE_SIZE = min(100, int(os.environ.get('DAWN_OL_PAGE_SIZE', '100')))
MAX_PAGES = int(os.environ.get('DAWN_OL_MAX_PAGES_PER_QUERY', '30'))
DELAY = float(os.environ.get('DAWN_OL_DELAY_SECONDS', '0.20'))

SUBJECTS = (
    'Bible',
    'Theology',
    'Christianity',
    'Jesus Christ',
    'Christian life',
    'Church history',
    'Biblical studies',
    'Devotional literature',
    'Prayer',
    'Christian ethics',
    'Christian doctrine',
    'Spiritual life',
)
FIELDS = 'key,title,author_name,language,first_publish_year,edition_key,isbn,oclc,lccn,cover_i'


def fetch_json(params: dict, attempts: int = 3) -> dict:
    url = API + '?' + urllib.parse.urlencode(params)
    last = None
    for attempt in range(1, attempts + 1):
        req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': 'application/json'})
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode('utf-8'))
        except Exception as exc:  # bounded network retry; hard failure remains visible
            last = exc
            if attempt < attempts:
                time.sleep(attempt)
    raise RuntimeError(f'Open Library request failed: {type(last).__name__}: {last}')


def compact(doc: dict, matched_language: str, subject: str) -> dict | None:
    key = str(doc.get('key') or '').strip()
    title = str(doc.get('title') or '').strip()
    if not key.startswith('/works/OL') or not key.endswith('W') or not title:
        return None
    authors = [str(x).strip() for x in (doc.get('author_name') or []) if str(x).strip()]
    languages = [str(x).strip() for x in (doc.get('language') or []) if str(x).strip()]
    editions = [str(x).strip() for x in (doc.get('edition_key') or []) if str(x).strip()]
    isbn = [str(x).strip() for x in (doc.get('isbn') or []) if str(x).strip()]
    oclc = [str(x).strip() for x in (doc.get('oclc') or []) if str(x).strip()]
    lccn = [str(x).strip() for x in (doc.get('lccn') or []) if str(x).strip()]
    work_id = key.rsplit('/', 1)[-1]
    edition_id = editions[0] if editions else None
    return {
        'workId': work_id,
        'title': title,
        'authors': authors[:4],
        'languages': languages[:12],
        'matchedLanguage': matched_language,
        'firstPublishYear': doc.get('first_publish_year'),
        'authorityIds': {
            'openLibraryWork': work_id,
            **({'isbn': isbn[0]} if isbn else {}),
            **({'oclc': oclc[0]} if oclc else {}),
            **({'lccn': lccn[0]} if lccn else {}),
        },
        'preferredEdition': edition_id,
        'coverId': doc.get('cover_i'),
        'workPointer': f'https://openlibrary.org/works/{work_id}',
        'editionPointer': f'https://openlibrary.org/books/{edition_id}' if edition_id else None,
        'matchedSubject': subject,
        'provider': 'Open Library',
        'contentDownloaded': False,
        'admission': 'none',
    }


def collect(language: str, works: dict[str, dict], stop_at: int) -> tuple[int, int]:
    requests = 0
    before = len(works)
    for subject in SUBJECTS:
        if len(works) >= stop_at:
            break
        query = f'subject:"{subject}" AND language:{language}'
        for page in range(1, MAX_PAGES + 1):
            if len(works) >= stop_at:
                break
            data = fetch_json({'q': query, 'fields': FIELDS, 'limit': PAGE_SIZE, 'page': page})
            requests += 1
            docs = data.get('docs') or []
            if not docs:
                break
            for doc in docs:
                item = compact(doc, language, subject)
                if item and item['workId'] not in works:
                    works[item['workId']] = item
            if len(docs) < PAGE_SIZE:
                break
            time.sleep(DELAY)
    return len(works) - before, requests


def main() -> int:
    works: dict[str, dict] = {}
    chinese_added, chinese_requests = collect('chi', works, min(CHINESE_TARGET, TARGET))
    english_added, english_requests = collect('eng', works, TARGET)
    items = sorted(works.values(), key=lambda x: x['workId'])
    payload = {
        'schema': 'dawn.library.work-discovery.openlibrary.v1',
        'targetWorks': TARGET,
        'provider': 'Open Library Search API',
        'workLevel': True,
        'runtimeBackend': False,
        'contentDownloaded': False,
        'admission': 'none; metadata discovery and reconciliation input only',
        'policy': {
            'languagesRequested': ['chi', 'eng'],
            'wikisourceForbidden': True,
            'subjects': list(SUBJECTS),
        },
        'metrics': {
            'works': len(items),
            'chineseMatchedWorksAdded': chinese_added,
            'englishMatchedWorksAdded': english_added,
            'requests': chinese_requests + english_requests,
        },
        'items': items,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(payload['metrics'], ensure_ascii=False))
    if len(items) < min(TARGET, 10000):
        return 2
    if chinese_added < 1 or english_added < 1:
        return 3
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
