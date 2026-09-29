#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / 'static/dawn-library/catalogue-ui/view-model.json'
MORNING = ROOT / 'static/dawn-library/surfaces/dawn-launch.json'
BOUNDARY = ROOT / 'static/dawn-library/product/library-renderer-boundary.js'
FINALIZER = ROOT / 'static/dawn-library/product/product-finalize.js'

FORBIDDEN_TEXT = ('203,448', '黎明選讀', '館藏流')
REQUIRED_TYPES = {'work', 'book', 'publication', 'manuscript'}
FORBIDDEN_TYPES = {'video', 'audio', 'map', 'place', 'tool', 'dataset', 'resource'}


def load(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


def main() -> int:
    contract = load(CONTRACT)
    morning = load(MORNING)
    boundary = BOUNDARY.read_text(encoding='utf-8')
    finalizer = FINALIZER.read_text(encoding='utf-8')

    entries = {row.get('id') for row in contract.get('leftPage', {}).get('primaryEntries', [])}
    if entries != {'morning-stars', 'catalogue', 'search'}:
        raise SystemExit(f'library navigation drift: {sorted(entries)}')

    modes = {row.get('id') for row in contract.get('rightPage', {}).get('modes', [])}
    if modes != {'source', 'zh-Hant', 'bilingual'}:
        raise SystemExit(f'reader mode drift: {sorted(modes)}')

    items = morning.get('items') or []
    if morning.get('surfaceId') != 'morning-stars' or len(items) != 3:
        raise SystemExit('Three Morning Stars must be exactly three canonical works')

    invariants = contract.get('invariants') or {}
    if invariants.get('audioVideoBelongToLibrary') is not False:
        raise SystemExit('AV ownership drifted into Dawn Library')
    if invariants.get('hardCodedCatalogueCountForbidden') is not True:
        raise SystemExit('hard-coded catalogue count guard missing')

    combined = '\n'.join((boundary, finalizer))
    for token in FORBIDDEN_TEXT:
        if token in combined:
            raise SystemExit(f'legacy Dawn Library token remains: {token}')
    for kind in REQUIRED_TYPES:
        if f"'{kind}'" not in boundary:
            raise SystemExit(f'missing publication type: {kind}')
    for kind in FORBIDDEN_TYPES:
        if f"'{kind}'" not in boundary:
            raise SystemExit(f'missing explicit rejection type: {kind}')

    if 'resourceManifest()' not in finalizer:
        raise SystemExit('canonical count authority missing')

    print(json.dumps({
        'schema': 'dawn.library.final-acceptance.v1',
        'status': 'pass',
        'navigation': sorted(entries),
        'readerModes': sorted(modes),
        'morningStars': len(items),
        'publicationTypes': sorted(REQUIRED_TYPES),
        'legacyTokens': 0,
        'countAuthority': 'resource-manifest'
    }, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
