#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import io
import json
import mimetypes
import time
import urllib.parse
import urllib.request
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STOREFRONT = ROOT / 'static/dawn-library/storefront.json'
SURFACE = ROOT / 'static/dawn-library/surfaces/dawn-storefront.json'
REGISTRY = ROOT / 'static/dawn-library/cover-registry.json'
COVER_DIR = ROOT / 'static/dawn-library/covers'
FORBIDDEN = ('wikisource', 'zh.wikisource.org')
MAX_SOURCE_BYTES = 24 * 1024 * 1024
MAX_CANONICAL_BYTES = 8 * 1024 * 1024
MAX_DIMENSION = (1600, 2400)
UA = 'Dore-Dawn-Cover-Reconciliation/1.1 (+https://westsidewatch.github.io)'


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding='utf-8'))


def norm(value: object) -> str:
    return ' '.join(str(value or '').casefold().split())


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
            work = item.get('work') or {}
            yield {
                'workId': work_id,
                'title': str(item.get('title') or work.get('title') or '').strip(),
                'author': str(item.get('author') or work.get('author') or '').strip(),
                'sourceUrl': source_url,
                'sourceMode': cover.get('mode') or 'source',
                'provider': cover.get('provider') or (item.get('source') or {}).get('provider') or 'source',
            }


def group_candidates(candidates: list[dict]) -> tuple[dict[str, list[dict]], list[dict]]:
    groups: dict[str, list[dict]] = defaultdict(list)
    for row in candidates:
        groups[row['workId']].append(row)
    collisions = []
    for work_id, rows in groups.items():
        signatures = {(norm(r.get('title')), norm(r.get('author'))) for r in rows}
        signatures.discard(('', ''))
        if len(signatures) > 1:
            collisions.append({
                'workId': work_id,
                'reason': 'conflicting storefront identities share one canonical Work ID',
                'candidates': [
                    {'title': r.get('title'), 'author': r.get('author'), 'provider': r.get('provider'), 'sourceUrl': r.get('sourceUrl')}
                    for r in rows
                ],
            })
    return groups, collisions


def extension_for(content_type: str, source_url: str) -> str:
    ct = (content_type or '').split(';', 1)[0].strip().lower()
    known = {'image/jpeg': '.jpg', 'image/png': '.png', 'image/webp': '.webp', 'image/gif': '.gif', 'image/avif': '.avif'}
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
                data = response.read(MAX_SOURCE_BYTES + 1)
                if not data or len(data) > MAX_SOURCE_BYTES:
                    raise ValueError('source cover size invalid')
                return data, content_type
        except Exception as exc:
            last = exc
            if attempt + 1 < attempts:
                time.sleep(1.25 * (attempt + 1))
    raise RuntimeError(f'cover download failed: {type(last).__name__}: {last}')


def normalize_oversize(data: bytes, content_type: str) -> tuple[bytes, str, bool]:
    if len(data) <= MAX_CANONICAL_BYTES:
        return data, content_type, False
    try:
        from PIL import Image
    except ImportError as exc:
        raise RuntimeError('oversize cover requires Pillow at build time') from exc
    with Image.open(io.BytesIO(data)) as image:
        image = image.convert('RGB')
        image.thumbnail(MAX_DIMENSION)
        for quality in (86, 80, 74, 68):
            out = io.BytesIO()
            image.save(out, format='JPEG', quality=quality, optimize=True, progressive=True)
            payload = out.getvalue()
            if len(payload) <= MAX_CANONICAL_BYTES:
                return payload, 'image/jpeg', True
    raise ValueError('normalized cover remains above canonical size limit')


def materialize(candidate: dict) -> dict:
    url = candidate['sourceUrl']
    data, content_type = download_image(url)
    data, content_type, normalized = normalize_oversize(data, content_type)
    digest_full = hashlib.sha256(data).hexdigest()
    ext = extension_for(content_type, url)
    filename = f'{digest_full[:24]}{ext}'
    target = COVER_DIR / filename
    if not target.exists():
        target.write_bytes(data)
    return {
        'pointer': f'/dawn-library/covers/{filename}',
        'sha256': digest_full,
        'bytes': len(data),
        'contentType': content_type.split(';', 1)[0].strip(),
        'provider': candidate['provider'],
        'sourceMode': candidate['sourceMode'],
        'sourceUrl': url,
        'normalized': normalized,
    }


def reconcile(storefront: dict, surface: dict, max_downloads: int | None = None) -> dict:
    COVER_DIR.mkdir(parents=True, exist_ok=True)
    candidate_rows = list(paired_candidates(storefront, surface))
    if max_downloads is not None:
        candidate_rows = candidate_rows[:max_downloads]
    groups, collisions = group_candidates(candidate_rows)
    collision_ids = {c['workId'] for c in collisions}
    rows: dict[str, dict] = {}
    failures: list[dict] = []

    for work_id, candidates in groups.items():
        if work_id in collision_ids:
            continue
        errors = []
        for candidate in candidates:
            try:
                rows[work_id] = materialize(candidate)
                if len(candidates) > 1:
                    rows[work_id]['alternateSources'] = [r['sourceUrl'] for r in candidates if r['sourceUrl'] != candidate['sourceUrl']]
                break
            except Exception as exc:
                errors.append({'sourceUrl': candidate['sourceUrl'], 'error': str(exc)[:240]})
        if work_id not in rows:
            failures.append({'workId': work_id, 'attempts': errors})

    unique_count = len(groups)
    duplicate_count = len(candidate_rows) - unique_count
    if len(rows) + len(failures) + len(collisions) != unique_count:
        raise ValueError('cover reconciliation accounting mismatch')

    return {
        'schema': 'dawn.library.cover-registry.v1',
        'runtimePolicy': {
            'browserExternalLookup': False,
            'canonicalPointerScheme': 'dawn://cover/<workId>',
            'assetScope': '/dawn-library/covers/',
            'wikisource': 'forbidden',
        },
        'candidateRowCount': len(candidate_rows),
        'candidateCount': unique_count,
        'duplicateCandidateCount': duplicate_count,
        'resolvedCount': len(rows),
        'failedCount': len(failures),
        'identityCollisionCount': len(collisions),
        'covers': dict(sorted(rows.items())),
        'failures': failures,
        'identityCollisions': collisions,
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
    keys = ('candidateRowCount', 'candidateCount', 'duplicateCandidateCount', 'resolvedCount', 'failedCount', 'identityCollisionCount')
    print(json.dumps({k: payload[k] for k in keys}, ensure_ascii=False))
    if payload['resolvedCount'] < args.minimum_resolved:
        raise SystemExit(f"cover reconciliation below minimum: {payload['resolvedCount']} < {args.minimum_resolved}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
