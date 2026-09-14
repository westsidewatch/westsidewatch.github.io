#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import unicodedata
from collections import defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
STOREFRONT = ROOT / 'static/dawn-library/storefront.json'
CANONICAL = ROOT / 'static/dawn-library/canonical-index.json'
SURFACE = ROOT / 'static/dawn-library/surfaces/dawn-storefront.json'
MAP = ROOT / '.dore-build/dawn-source-identity-map.json'


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding='utf-8'))


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, separators=(',', ':')) + '\n', encoding='utf-8')


def norm(value: object) -> str:
    text = unicodedata.normalize('NFKC', str(value or '')).casefold().strip()
    text = re.sub(r'[^\w\s-]+', ' ', text)
    return re.sub(r'\s+', ' ', text).strip()


def normalize_work_id(value: object) -> str:
    value = str(value or '').strip()
    return value[len('/works/'):] if value.startswith('/works/') else value


def item_signature(item: dict) -> tuple[str, str]:
    work = item.get('work') or {}
    return norm(item.get('title') or work.get('title')), norm(item.get('author') or work.get('author'))


def work_signature(work: dict) -> tuple[str, str]:
    authors = work.get('authors') or []
    return norm(work.get('title')), norm(authors[0] if authors else '')


def source_ref(item: dict) -> str:
    if item.get('id'):
        return str(item['id'])
    source = item.get('source') or {}
    seed = '|'.join([str(source.get('provider') or ''), str(source.get('url') or ''), str(item.get('title') or ''), str(item.get('author') or '')])
    return 'source:' + hashlib.sha256(seed.encode('utf-8')).hexdigest()[:24]


def fallback_work_id(item: dict) -> str:
    source = item.get('source') or {}
    seed = '|'.join([source_ref(item), str(source.get('provider') or ''), str(source.get('url') or '')])
    return 'dawn:' + hashlib.sha256(seed.encode('utf-8')).hexdigest()[:20]


def explicit_claim(item: dict) -> str:
    identity = item.get('identity') or {}
    identifiers = item.get('identifiers') or {}
    for value in (item.get('workId'), identity.get('workId'), identifiers.get('openLibraryWork')):
        work_id = normalize_work_id(value)
        if work_id:
            return work_id
    return ''


def compatible(source_sig: tuple[str, str], canonical_sig: tuple[str, str]) -> bool:
    st, sa = source_sig
    ct, ca = canonical_sig
    if not st or not ct or st != ct:
        return False
    if sa and ca and sa != ca:
        return False
    return True


def ensure_fallback_work(works: dict[str, dict], item: dict, work_id: str) -> None:
    if work_id in works:
        return
    work = item.get('work') or {}
    title = str(item.get('title') or work.get('title') or '').strip()
    author = str(item.get('author') or work.get('author') or '').strip()
    language = str(item.get('language') or work.get('language') or '').strip()
    works[work_id] = {
        'workId': work_id,
        'title': title,
        'authors': [author] if author else [],
        'languages': [language] if language else [],
        'authorityIds': {},
        'edition': {'editionId': None},
        'cover': {'pointer': f'dawn://cover/{work_id}', 'mode': 'canonical-fallback'},
        'readingPointer': None,
        'firstPublishYear': item.get('firstPublishYear'),
        'authorityBacked': False,
        'identityReconciliation': {
            'status': 'fallback-local',
            'sourceRef': source_ref(item),
            'principle': 'source identity claims require admission before becoming canonical identity',
        },
    }


def reconcile(storefront: dict, canonical: dict) -> tuple[dict, dict, dict]:
    works = canonical.get('works') or {}
    signature_index: dict[tuple[str, str], list[str]] = defaultdict(list)
    for work_id, work in works.items():
        sig = work_signature(work)
        if sig[0]:
            signature_index[sig].append(work_id)

    shelves = []
    claims: dict[str, dict] = {}
    assigned_signatures: dict[str, tuple[str, str]] = {}
    accepted = matched = fallback = rejected = 0

    for shelf in storefront.get('shelves', []):
        refs = []
        for item in shelf.get('items', []):
            ref = source_ref(item)
            sig = item_signature(item)
            claim = explicit_claim(item)
            chosen = ''
            status = ''
            reason = ''

            if claim:
                canonical_work = works.get(claim)
                if canonical_work and compatible(sig, work_signature(canonical_work)):
                    chosen = claim
                    status = 'authority-claim-admitted'
                    reason = 'explicit authority claim matches canonical title/author signature'
                    accepted += 1
                else:
                    rejected += 1
                    reason = 'explicit authority claim rejected by canonical signature gate'

            if not chosen and sig[0]:
                exact = signature_index.get(sig) or []
                if len(exact) == 1:
                    chosen = exact[0]
                    status = 'canonical-signature-match'
                    reason = 'unique exact canonical title/author signature'
                    matched += 1

            if not chosen:
                chosen = fallback_work_id(item)
                status = 'fallback-local'
                if not reason:
                    reason = 'no admissible unique canonical authority claim'
                ensure_fallback_work(works, item, chosen)
                fallback += 1

            previous = assigned_signatures.get(chosen)
            if previous and previous != sig:
                old = chosen
                chosen = fallback_work_id(item)
                ensure_fallback_work(works, item, chosen)
                status = 'fallback-local'
                reason = f'collision prevented: {old} already assigned to a different source signature'
                fallback += 1
            assigned_signatures[chosen] = sig

            refs.append({'workId': chosen})
            source = item.get('source') or {}
            claims[ref] = {
                'sourceRef': ref,
                'sourceAuthority': source.get('provider') or 'source',
                'sourcePointer': source.get('url') or source.get('downloadUrl'),
                'authorityClaim': claim or None,
                'canonicalWorkId': chosen,
                'status': status,
                'reason': reason,
                'ephemeralRepresentation': True,
                'surfaceOwnsIdentity': False,
            }

        shelves.append({
            'id': shelf.get('id'),
            'title': shelf.get('title'),
            'kind': shelf.get('kind'),
            'items': refs,
        })

    canonical['works'] = dict(sorted(works.items()))
    canonical['workCount'] = len(works)
    canonical['authorityBackedWorks'] = sum(1 for work in works.values() if work.get('authorityBacked'))
    canonical.setdefault('runtimePolicy', {})['sourceIdentityAdmission'] = 'required'

    surface = {
        'schema': 'dawn.library.surface.v1',
        'surfaceId': 'dawn-storefront',
        'canonicalIndex': '../canonical-index.json',
        'title': storefront.get('title') or '黎明書局',
        'shelves': shelves,
    }
    identity_map = {
        'schema': 'dore.source-identity-admission.v1',
        'policy': {
            'sourceAuthorityIsClaimNotCanonicalIdentity': True,
            'positionalPairingForbidden': True,
            'surfaceOwnsIdentity': False,
            'ephemeralRepresentation': True,
        },
        'claimCount': len(claims),
        'authorityClaimsAdmitted': accepted,
        'canonicalSignatureMatches': matched,
        'fallbackLocal': fallback,
        'authorityClaimsRejected': rejected,
        'claims': dict(sorted(claims.items())),
    }

    work_to_sigs: dict[str, set[tuple[str, str]]] = defaultdict(set)
    for shelf, store_shelf in zip(surface['shelves'], storefront.get('shelves', [])):
        for ref, item in zip(shelf.get('items', []), store_shelf.get('items', [])):
            work_to_sigs[ref['workId']].add(item_signature(item))
    conflicts = {wid: sigs for wid, sigs in work_to_sigs.items() if len(sigs) > 1}
    if conflicts:
        raise ValueError(f'canonical source identity collision remains: {sorted(conflicts)[:3]}')

    return canonical, surface, identity_map


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--storefront', type=Path, default=STOREFRONT)
    parser.add_argument('--canonical', type=Path, default=CANONICAL)
    parser.add_argument('--surface', type=Path, default=SURFACE)
    parser.add_argument('--map', type=Path, default=MAP)
    args = parser.parse_args()

    canonical, surface, identity_map = reconcile(read_json(args.storefront), read_json(args.canonical))
    write_json(args.canonical, canonical)
    write_json(args.surface, surface)
    write_json(args.map, identity_map)
    print(json.dumps({
        'claimCount': identity_map['claimCount'],
        'authorityClaimsAdmitted': identity_map['authorityClaimsAdmitted'],
        'canonicalSignatureMatches': identity_map['canonicalSignatureMatches'],
        'fallbackLocal': identity_map['fallbackLocal'],
        'authorityClaimsRejected': identity_map['authorityClaimsRejected'],
        'workCount': canonical['workCount'],
    }, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
