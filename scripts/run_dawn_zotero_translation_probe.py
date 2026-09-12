#!/usr/bin/env python3
from __future__ import annotations

import json
import os
from pathlib import Path

from dore_core.capabilities.zotero_reconciliation import ZoteroTranslationAdapter

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'reports/DAWN-ZOTERO-TRANSLATION.json'
# Saint Augustine, Confessions, Oxford World's Classics, Henry Chadwick.
ISBN = '0192833723'


def main() -> int:
    base_url = os.environ.get('DAWN_ZOTERO_TRANSLATE_URL', 'http://127.0.0.1:1969')
    adapter = ZoteroTranslationAdapter(base_url=base_url, timeout=45)
    items = adapter.search_identifier(ISBN)
    selected = next((item for item in items if item.title and item.creators), None)
    report = {
        'schema': 'dawn.zotero.translation.acceptance.v1',
        'provider': 'zotero/translation-server',
        'endpoint': '/search',
        'identifier': ISBN,
        'resultCount': len(items),
        'success': selected is not None,
        'identity': None if selected is None else {
            'source': selected.source,
            'itemType': selected.item_type,
            'title': selected.title,
            'creators': list(selected.creators),
            'date': selected.date,
            'publisher': selected.publisher,
            'isbn': selected.isbn,
            'doi': selected.doi,
            'libraryCatalog': selected.library_catalog,
            'authorityIds': selected.authority_ids,
        },
        'admission': 'none; bibliographic reconciliation evidence only',
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if not report['success']:
        return 1
    identity = report['identity'] or {}
    creators = ' '.join(identity.get('creators') or []).lower()
    title = str(identity.get('title') or '').lower()
    if 'augustine' not in creators:
        return 1
    if 'confession' not in title:
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
