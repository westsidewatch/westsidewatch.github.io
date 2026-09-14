#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import mimetypes
import os
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STOREFRONT = ROOT / 'static/dawn-library/storefront.json'
SURFACE = ROOT / 'static/dawn-library/surfaces/dawn-storefront.json'
REGISTRY = ROOT / 'static/dawn-library/cover-registry.json'
COVER_DIR = ROOT / 'static/dawn-library/covers'
FORBIDDEN = ('wikisource', 'zh.wikisource.org')
MAX_BYTES = 8 * 1024 * 1024
UA = 'Dore-Dawn-Cover-Reconciliation/1.0 (+https://westsidewatch.github.io)'


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding='utf-8'))


def valid_source_url(value: object) -> str | None:
    url = str(value or '').strip()
    if not url.startswith('https://'):
        return None
    lower = url.casefold()
    if any(token in lower for token in FORBIDDEN):
        return None
    return url


def paired_candidates(storefront: dict, surface: dict):
    surface_shelves = {s.get('id'): s for s in surface.get('shelves', [])}
    for store_shelf in storefront.get('shelves', []):
        canonical_shelf = surface_shelves.get(store_shelf.get('id')) or {}
        refs = canonical_shelf.get('items', [])
        for idx, item in enumerate(store_shelf.get('items', [])):
            work_id = (refs[idx] if idx < len(refs) else {}).get('workId') or item.get('workId')
            if not work_id:
                continue
            cover = item.get('cover') or {}
            source_url = valid_source_url(cover.get('url'))
            if not source_url:
                continue
            yield {
                'workId': work_id,
                'sourceUrl': source_url,
                'sourceMode': cover.get('mode') or 'source',
                'provider': cover.get('provider') or (item.get('source') or {}).get('provider') or 'source',
            }


def extension_for(content_type: str, source_url: str) -> str:
    ct = (content_type or '').split(';', 1)[0].strip().lower()
    known = {
        'image/jpeg': '.jpg',
        'image/png': '.png',
        'image/webp': '.webp',
        'image/gif': '.gif',
        'image/avif': '.avif',
    }
    if ct in known:
        return known[ct]
    ext = Path(urllib.parse.urlparse(source_url).path).suffix.lower()
    if ext in {'.jpg', '.jpeg', '.png', '.webp', '.gif', '.avif'}:
        return '.jpg' if ext == '.jpeg' else ext
    guessed = mimetypes.guess_extension(ct) or '.img'
    return '.jpg' if guessed == '.jpe' else guessed


def download_image(url: str, attempts: int = 3) -> tuple[bytes, str]:
    last = None
    for attempt in range(attempts):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': 'image/avif,image/webp,image/*,*/*;q=0.8'})
            with urllib.request.urlopen(req, timeout=35) as response:
                content_type = response.headers.get('Content-Type', '')
                if not content_type.lower().startswith('image/'):
                    raise ValueError(f'not image content: {content_type}')
                data = response.read(MAX_BYTES + 1)
                if not data or len(data) > MAX_BYTES:
                    raise ValueError('cover size invalid')
                return data, content_type
        except Exception as exc:
            last = exc
            if attempt + 1 < attempts:
                time.sleep(1.25 * (attempt + 1))
    raise RuntimeError(f'cover download failed: {type(last).__name__}: {last}')


def reconcile(storefront: dict, surface: dict, max_downloads: int | None = None) -> dict:
    COVER_DIR.mkdir(parents=True, exist_ok=True)
    rows: dict[str, dict] = {}
    failures: list[dict] = []
    candidates = list(paired_candidates(storefront, surface))
    if max_downloads is not None:
        candidates = candidates[:max_downloads]

    for candidate in candidates:
        work_id = candidate['workId']
        url = candidate['sourceUrl']
        try:
            data, content_type = download_image(url)
            digest = hashlib.sha256(data).hexdigest()[:24]
            ext = extension_for(content_type, url)
            filename = f'{digest}{ext}'
            target = COVER_DIR / filename
            if not target.exists():
                target.write_bytes(data)
            rows[work_id] = {
                'pointer': f'/dawn-library/covers/{filename}',
                'sha256': hashlib.sha256(data).hexdigest(),
                'bytes': len(data),
                'contentType': content_type.split(';', 1)[0].strip(),
                'provider': candidate['provider'],
                'sourceMode': candidate['sourceMode'],
                'sourceUrl': url,
            }
        except Exception as exc:
            failures.append({'workId': work_id, 'sourceUrl': url, 'error': str(exc)[:240]})

    return {
        'schema': 'dawn.library.cover-registry.v1',
        'runtimePolicy': {
            'browserExternalLookup': False,
            'canonicalPointerScheme': 'dawn://cover/<workId>',
            'assetScope': '/dawn-library/covers/',
            'wikisource': 'forbidden',
        },
        'candidateCount': len(candidates),
        'resolvedCount': len(rows),
        'failedCount': len(failures),
        'covers': dict(sorted(rows.items())),
        'failures': failures,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--storefront', type=Path, default=STOREFRONT)
    parser.add_argument('--surface', type=Path, default=SURFACE)
    parser.add_argument('--registry', type=Path, default=REGISTRY)
    parser.add_argument('--max-downloads', type=int)
    parser.add_argument('--minimum-resolved', type=int, default=1)
    args = parser.parse_args()

    payload = reconcile(read_json(args.storefront), read_json(args.surface), args.max_downloads)
    args.registry.parent.mkdir(parents=True, exist_ok=True)
    args.registry.write_text(json.dumps(payload, ensure_ascii=False, separators=(',', ':')) + '\n', encoding='utf-8')
    print(json.dumps({k: payload[k] for k in ('candidateCount', 'resolvedCount', 'failedCount')}, ensure_ascii=False))
    if payload['resolvedCount'] < args.minimum_resolved:
        raise SystemExit(f"cover reconciliation below minimum: {payload['resolvedCount']} < {args.minimum_resolved}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
