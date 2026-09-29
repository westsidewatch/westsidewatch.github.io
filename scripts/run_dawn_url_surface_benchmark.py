#!/usr/bin/env python3
"""Benchmark Dawn URL Surface routing against the checked-in candidate corpus.

This does not admit resources to the library. It asks a narrower question:
given every currently checked-in discovered pointer, can Dawn route it to a mature
presentation capability without copying the underlying resource into Dawn?
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

    if 'iiif' in url.lower() or path.endswith('/manifest') or path.endswith('/manifest.json'):
        return {'surface': 'visual', 'adapter': 'iiif-visual-surface', 'confidence': 'high'}

    if path.endswith('.pdf'):
        return {'surface': 'document', 'adapter': 'pdfjs', 'confidence': 'high'}
    if path.endswith(('.epub', '.mobi')):
        return {'surface': 'book', 'adapter': 'book-reader', 'confidence': 'high'}

    if host.endswith('gutenberg.org') and '/ebooks/' in path:
        return {'surface': 'book', 'adapter': 'bibliographic-page', 'confidence': 'high'}
    if host.endswith(('openlibrary.org', 'worldcat.org', 'loc.gov', 'hathitrust.org')):
        return {'surface': 'bibliographic', 'adapter': 'zotero-translate', 'confidence': 'medium'}

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
        'schema': 'dawn.url-surface.benchmark.v2',
        'purpose': 'Use the complete checked-in candidate corpus as the acceptance benchmark for pointer-to-surface routing.',
        'corpus': {'total': total, 'source': str(CANDIDATES.relative_to(ROOT))},
        'results': {
            'resolved': resolved,
            'unresolved': len(unresolved),
            'routingCoverage': round(resolved / total, 4) if total else 0,
            'surfaces': dict(surfaces),
            'adapters': dict(adapters),
        },
        'acceptance': {
            'corpusPolicy': 'complete-checked-in-corpus',
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

    corpus_ok = total > 0 and len(routes) == total
    coverage_ok = report['results']['routingCoverage'] >= 0.95
    raise SystemExit(0 if corpus_ok and coverage_ok else 1)


if __name__ == '__main__':
    main()
