#!/usr/bin/env python3
"""Benchmark Dawn URL Surface routing against the real discovery candidate corpus.

This does not admit resources to the library. It asks a narrower question:
given a discovered pointer, can Dawn route it to a mature presentation capability
without copying the underlying resource into Dawn?
"""
import json
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
CANDIDATES = ROOT / 'static/dawn-library/biblical-world/discovery-candidates.json'
OUT = ROOT / 'reports/DAWN-URL-SURFACE-BENCHMARK.json'


def resolve_surface(item):
    url = (item.get('sourceUrl') or '').strip()
    parsed = urlparse(url)
    host = parsed.netloc.lower()
    path = parsed.path.lower()

    # Existing Dawn visual capability remains authoritative for IIIF resources.
    if 'iiif' in url.lower() or path.endswith('/manifest') or path.endswith('/manifest.json'):
        return {'surface': 'visual', 'adapter': 'iiif-visual-surface', 'confidence': 'high'}

    # Direct document pointers are routed to dedicated viewers, not generic embeds.
    if path.endswith('.pdf'):
        return {'surface': 'document', 'adapter': 'pdfjs', 'confidence': 'high'}
    if path.endswith(('.epub', '.mobi')):
        return {'surface': 'book', 'adapter': 'book-reader', 'confidence': 'high'}

    # Known bibliographic/catalog providers should first be interpreted as works.
    if host.endswith('gutenberg.org') and '/ebooks/' in path:
        return {'surface': 'book', 'adapter': 'bibliographic-page', 'confidence': 'high'}
    if host.endswith(('openlibrary.org', 'worldcat.org', 'loc.gov', 'hathitrust.org')):
        return {'surface': 'bibliographic', 'adapter': 'zotero-translate', 'confidence': 'medium'}

    # General web pointers stay lightweight: metadata/embed first, readable extraction second.
    if parsed.scheme in ('http', 'https') and host:
        return {'surface': 'web', 'adapter': 'oembed-opengraph', 'fallback': 'readability', 'confidence': 'medium'}

    return {'surface': 'unresolved', 'adapter': None, 'confidence': 'none'}


def main():
    data = json.loads(CANDIDATES.read_text())
    items = data.get('items', [])
    routes = []
    surfaces = Counter()
    adapters = Counter()
    unresolved = []

    for item in items:
        route = resolve_surface(item)
        surfaces[route['surface']] += 1
        adapters[str(route.get('adapter'))] += 1
        record = {
            'sourceId': item.get('sourceId'),
            'provider': item.get('provider'),
            'sourceUrl': item.get('sourceUrl'),
            **route,
        }
        routes.append(record)
        if route['surface'] == 'unresolved':
            unresolved.append(record)

    total = len(items)
    resolved = total - len(unresolved)
    report = {
        'schema': 'dawn.url-surface.benchmark.v1',
        'purpose': 'Use the existing Dawn discovery corpus as the acceptance benchmark for pointer-to-surface routing.',
        'corpus': {'total': total, 'source': str(CANDIDATES.relative_to(ROOT))},
        'results': {
            'resolved': resolved,
            'unresolved': len(unresolved),
            'routingCoverage': round(resolved / total, 4) if total else 0,
            'surfaces': dict(surfaces),
            'adapters': dict(adapters),
        },
        'acceptance': {
            'minimumCorpus': 900,
            'minimumRoutingCoverage': 0.95,
            'mustNotPromoteOrDeleteCandidates': True,
            'mustNotTreatPreviewAsRelevance': True,
            'mustPreserveExternalPointers': True,
        },
        'routes': routes,
        'unresolved': unresolved,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(report['results'], ensure_ascii=False, indent=2))

    ok = total >= 900 and report['results']['routingCoverage'] >= 0.95
    raise SystemExit(0 if ok else 1)


if __name__ == '__main__':
    main()
