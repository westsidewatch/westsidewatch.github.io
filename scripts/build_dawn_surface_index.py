#!/usr/bin/env python3
import json
from pathlib import Path

from dore_core.capabilities.url_surface import UrlSurfaceResolver

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'static/dawn-library/biblical-world/discovery-candidates.json'
OUT = ROOT / 'static/dawn-library/biblical-world/surface-index.json'


def main():
    data = json.loads(SRC.read_text())
    items = data.get('items', [])
    resolver = UrlSurfaceResolver()

    surfaces = []
    for item in items:
        payload = resolver.payload(item.get('sourceUrl', '')).as_dict()
        surfaces.append({
            'sourceId': item.get('sourceId'),
            'provider': item.get('provider'),
            'title': item.get('title'),
            'author': item.get('author'),
            **payload,
        })

    document = {
        'schema': 'dawn.library.surface-index.v1',
        'source': str(SRC.relative_to(ROOT)),
        'count': len(surfaces),
        'invariant': 'This index contains pointers and presentation routing only; source content remains external.',
        'items': surfaces,
    }
    OUT.write_text(json.dumps(document, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'count': len(surfaces), 'output': str(OUT.relative_to(ROOT))}, ensure_ascii=False))


if __name__ == '__main__':
    main()
