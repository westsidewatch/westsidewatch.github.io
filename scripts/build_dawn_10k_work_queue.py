#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
GUTENBERG = ROOT / 'static/dawn-library/biblical-world/discovery-candidates.json'
OPENLIBRARY = ROOT / 'data/dawn-10k-openlibrary-works.json'
OUT = ROOT / 'data/dawn-10k-work-queue.json'

WIKISOURCE_PROVIDER_TOKENS = ('wikisource', 'zh-wikisource')
CHINESE_LANGUAGE_CODES = {'chi', 'zho', 'zh', 'zh-cn', 'zh-hans', 'zh-hant', 'zh-tw', 'zh-hk'}
ENGLISH_LANGUAGE_CODES = {'eng', 'en'}


def norm(text: str) -> str:
    text = unicodedata.normalize('NFKC', text or '').casefold().strip()
    text = re.sub(r'[^\w\s-]+', ' ', text)
    return re.sub(r'\s+', ' ', text).strip()


def signature(title: str, author: str) -> str:
    return f'{norm(title)}::{norm(author)}'


def add_unique(target: list, value) -> None:
    if value and value not in target:
        target.append(value)


def is_wikisource_url(value: object) -> bool:
    text = str(value or '').strip()
    if not text:
        return False
    try:
        host = (urlparse(text).hostname or '').casefold().rstrip('.')
    except ValueError:
        host = ''
    return host == 'wikisource.org' or host.endswith('.wikisource.org')


def contains_forbidden_wikisource(value: object) -> bool:
    """Hard discovery gate. Historical reports cannot reintroduce Wikisource."""
    if isinstance(value, dict):
        for key, nested in value.items():
            key_norm = str(key).casefold()
            if key_norm in {'provider', 'providerid', 'source', 'sourceid', 'sourcekey'}:
                text = str(nested or '').casefold()
                if any(token in text for token in WIKISOURCE_PROVIDER_TOKENS):
                    return True
            if contains_forbidden_wikisource(nested):
                return True
        return False
    if isinstance(value, (list, tuple, set)):
        return any(contains_forbidden_wikisource(item) for item in value)
    text = str(value or '').casefold()
    return is_wikisource_url(value) or 'zh-wikisource' in text or 'wikisource.org' in text


def normalized_languages(item: dict) -> set[str]:
    values = list(item.get('languages') or [])
    matched = item.get('matchedLanguage')
    if matched:
        values.append(matched)
    return {str(value).casefold().replace('_', '-') for value in values if str(value).strip()}


def language_priority(item: dict) -> int:
    """Chinese is promoted first; this changes order only, never admission quality."""
    languages = normalized_languages(item)
    if languages & CHINESE_LANGUAGE_CODES or any(code.startswith('zh-') for code in languages):
        return 0
    if languages & ENGLISH_LANGUAGE_CODES:
        return 2
    return 1


def main() -> int:
    gutenberg = json.loads(GUTENBERG.read_text()) if GUTENBERG.exists() else {'items': []}
    openlibrary = json.loads(OPENLIBRARY.read_text()) if OPENLIBRARY.exists() else {'items': []}

    previous = {}
    if OUT.exists():
        previous_data = json.loads(OUT.read_text())
        previous = {item['queueId']: item for item in previous_data.get('items', [])}

    grouped: dict[str, dict] = {}
    signature_to_key: dict[str, str] = {}

    # Authority-backed Work identities come first. Open Library search returns Work-level
    # records; editions and translations already grouped by that authority remain one Work.
    for work in openlibrary.get('items', []):
        if contains_forbidden_wikisource(work):
            continue
        work_id = str(work.get('workId') or '').strip()
        title = str(work.get('title') or '').strip()
        authors = [str(x).strip() for x in (work.get('authors') or []) if str(x).strip()]
        if not work_id or not title:
            continue
        primary_author = authors[0] if authors else ''
        key = f'openlibrary::{work_id}'
        entry = {
            'queueId': f'work::{key}',
            'workId': work_id,
            'title': title,
            'author': primary_author,
            'authors': authors,
            'languages': list(dict.fromkeys(work.get('languages') or [])),
            'providers': ['Open Library'],
            'pointers': [p for p in (work.get('workPointer'), work.get('editionPointer')) if p],
            'relations': [],
            'authorityIds': dict(work.get('authorityIds') or {}),
            'preferredEdition': work.get('preferredEdition'),
            'coverId': work.get('coverId'),
            'firstPublishYear': work.get('firstPublishYear'),
            'status': 'identity-established',
            'checkpoint': 1,
            'admission': 'none',
        }
        grouped[key] = entry
        sig = signature(title, primary_author)
        if sig != '::' and sig not in signature_to_key:
            signature_to_key[sig] = key

    # Legacy discovery remains pointer evidence only. Wikisource is rejected before any
    # provider, URL, relation, or provisional identity can enter the reconciliation queue.
    for candidate in gutenberg.get('items', []):
        if contains_forbidden_wikisource(candidate):
            continue
        title = str(candidate.get('title') or '').strip()
        author = str(candidate.get('author') or '').strip()
        sig = signature(title, author)
        if not norm(title):
            continue
        key = signature_to_key.get(sig)
        if key is None:
            key = f'provisional::{sig}'
            grouped.setdefault(key, {
                'queueId': f'work::{key}',
                'title': title,
                'author': author,
                'authors': [author] if author else [],
                'languages': list(dict.fromkeys(candidate.get('languages') or ([candidate.get('matchedLanguage')] if candidate.get('matchedLanguage') else []))),
                'providers': [],
                'pointers': [],
                'relations': [],
                'authorityIds': {},
                'status': 'pending-reconciliation',
                'checkpoint': 0,
                'admission': 'none',
            })
        entry = grouped[key]
        add_unique(entry['providers'], candidate.get('provider'))
        add_unique(entry['pointers'], candidate.get('sourceUrl'))
        for relation in candidate.get('suggestedRelations', []):
            add_unique(entry['relations'], relation)

    items = []
    for key in sorted(grouped):
        item = grouped[key]
        old = previous.get(item['queueId'])
        if old:
            # Never downgrade an established authority identity with older provisional state.
            if item['checkpoint'] == 0:
                item['status'] = old.get('status', item['status'])
                item['checkpoint'] = old.get('checkpoint', item['checkpoint'])
            for field in ('notes',):
                if field in old:
                    item[field] = old[field]
        if contains_forbidden_wikisource(item):
            continue
        items.append(item)

    # Promotion order only. Rights/relevance/authority gates remain untouched.
    items.sort(key=lambda item: (language_priority(item), str(item.get('queueId') or '')))

    authority_backed = sum(1 for item in items if item.get('authorityIds', {}).get('openLibraryWork'))
    chinese = sum(1 for item in items if language_priority(item) == 0)
    english = sum(1 for item in items if language_priority(item) == 2)
    report = {
        'schema': 'dawn.library.10k-work-queue.v2',
        'targetWorks': 10000,
        'sources': [str(GUTENBERG.relative_to(ROOT)), str(OPENLIBRARY.relative_to(ROOT))],
        'sourceCandidates': len(gutenberg.get('items', [])) + len(openlibrary.get('items', [])),
        'deduplicatedWorks': len(items),
        'authorityBackedWorks': authority_backed,
        'languageSignals': {'chi': chinese, 'eng': english},
        'promotionPolicy': 'Chinese-first ordering after unchanged source/rights/relevance/authority qualification; ordering never grants admission.',
        'sourcePolicy': {'wikisource': 'forbidden-at-discovery-and-reconciliation'},
        'checkpointRule': 'Authority-backed Work IDs are checkpoint 1; prior provisional progress survives rebuilds without downgrading established identities.',
        'admission': 'none; this queue is technical reconciliation input only',
        'items': items,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({
        'sourceCandidates': report['sourceCandidates'],
        'deduplicatedWorks': report['deduplicatedWorks'],
        'authorityBackedWorks': authority_backed,
        'languageSignals': report['languageSignals'],
        'targetWorks': report['targetWorks'],
    }, ensure_ascii=False))
    if OPENLIBRARY.exists() and (len(items) < 10000 or authority_backed < 9000):
        return 2
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
