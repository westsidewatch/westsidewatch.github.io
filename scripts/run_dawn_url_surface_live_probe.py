#!/usr/bin/env python3
"""Live-probe Dawn discovery pointers without mutating library state.

This probe is intentionally shallow: it verifies that external pointers can be
resolved into a renderable response envelope. It does not ingest or persist
remote content, and it does not affect relevance/admission.
"""
from __future__ import annotations

import json
import socket
import ssl
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
CANDIDATES = ROOT / 'static/dawn-library/biblical-world/discovery-candidates.json'
OUT = ROOT / 'reports/DAWN-URL-SURFACE-LIVE.json'

TIMEOUT = 10
MAX_WORKERS = 12
MAX_READ = 131072
USER_AGENT = 'DawnLibrarySurfaceProbe/1.0 (+https://westsidewatch.github.io/)'
RENDERABLE_TYPES = (
    'text/html', 'application/xhtml+xml', 'application/pdf', 'application/epub+zip',
    'image/', 'application/json', 'application/ld+json',
)


def classify_error(exc: Exception) -> str:
    if isinstance(exc, HTTPError):
        if exc.code in (401, 403, 429):
            return 'blocked'
        return 'http-error'
    if isinstance(exc, (TimeoutError, socket.timeout)):
        return 'timeout'
    if isinstance(exc, ssl.SSLError):
        return 'tls-error'
    if isinstance(exc, URLError):
        reason = getattr(exc, 'reason', None)
        if isinstance(reason, (TimeoutError, socket.timeout)):
            return 'timeout'
        return 'network-error'
    return 'error'


def probe(item: dict) -> dict:
    url = (item.get('sourceUrl') or '').strip()
    base = {
        'sourceId': item.get('sourceId'),
        'provider': item.get('provider'),
        'sourceUrl': url,
    }
    if not url.startswith(('http://', 'https://')):
        return {**base, 'status': 'unresolved', 'reason': 'invalid-url'}

    req = Request(
        url,
        method='GET',
        headers={
            'User-Agent': USER_AGENT,
            'Accept': 'text/html,application/xhtml+xml,application/pdf,application/json,image/*;q=0.8,*/*;q=0.5',
            'Range': f'bytes=0-{MAX_READ - 1}',
        },
    )
    try:
        with urlopen(req, timeout=TIMEOUT) as response:
            status_code = getattr(response, 'status', 200)
            final_url = response.geturl()
            content_type = (response.headers.get('Content-Type') or '').split(';', 1)[0].strip().lower()
            xfo = response.headers.get('X-Frame-Options')
            csp = response.headers.get('Content-Security-Policy')
            sample = response.read(MAX_READ)
            renderable = any(content_type.startswith(t) for t in RENDERABLE_TYPES)
            if 200 <= status_code < 400 and renderable:
                status = 'success'
            elif 200 <= status_code < 400:
                status = 'fallback'
            else:
                status = 'http-error'
            return {
                **base,
                'status': status,
                'httpStatus': status_code,
                'finalUrl': final_url,
                'contentType': content_type,
                'bytesSampled': len(sample),
                'frameRestricted': bool(xfo or (csp and 'frame-ancestors' in csp.lower())),
                'xFrameOptions': xfo,
                'hasFrameAncestorsCsp': bool(csp and 'frame-ancestors' in csp.lower()),
            }
    except Exception as exc:
        return {
            **base,
            'status': classify_error(exc),
            'reason': f'{type(exc).__name__}: {exc}'[:300],
        }


def main() -> int:
    data = json.loads(CANDIDATES.read_text())
    items = data.get('items', [])
    results = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        futures = [pool.submit(probe, item) for item in items]
        for future in as_completed(futures):
            results.append(future.result())

    results.sort(key=lambda x: str(x.get('sourceId') or ''))
    counts = Counter(r['status'] for r in results)
    total = len(results)
    live = counts['success'] + counts['fallback']
    report = {
        'schema': 'dawn.url-surface.live.v1',
        'purpose': 'Measure whether real Dawn external pointers can produce a renderable response envelope.',
        'corpus': {'total': total, 'source': str(CANDIDATES.relative_to(ROOT))},
        'settings': {
            'timeoutSeconds': TIMEOUT,
            'maxWorkers': MAX_WORKERS,
            'maxBytesPerPointer': MAX_READ,
            'mutation': False,
        },
        'results': {
            'counts': dict(counts),
            'liveOrFallback': live,
            'liveCoverage': round(live / total, 4) if total else 0,
            'frameRestricted': sum(1 for r in results if r.get('frameRestricted')),
        },
        'acceptance': {
            'minimumCorpus': 900,
            'minimumLiveCoverage': 0.90,
            'blockedIsNotAdmissionFailure': True,
            'mustNotMutateCandidates': True,
        },
        'items': results,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(report['results'], ensure_ascii=False, indent=2))

    return 0 if total >= 900 and report['results']['liveCoverage'] >= 0.90 else 1


if __name__ == '__main__':
    raise SystemExit(main())
