#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
STOREFRONT = ROOT / 'static/dawn-library/storefront.json'
IDENTITY_MAP = ROOT / '.dore-build/dawn-source-identity-map.json'
OUT = ROOT / '.dore-build/dawn-source-capability-map.json'
ENVELOPE_MODULE = ROOT / 'local/dore-local/source_capability_envelope.py'
FORBIDDEN = ('wikisource.org',)


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding='utf-8'))


def load_envelope_module():
    spec = importlib.util.spec_from_file_location('dore_source_capability_envelope', ENVELOPE_MODULE)
    if spec is None or spec.loader is None:
        raise RuntimeError('source capability envelope unavailable')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def source_items(storefront: dict) -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    for shelf in storefront.get('shelves', []):
        for item in shelf.get('items', []):
            ref = str(item.get('id') or '').strip()
            if ref:
                rows[ref] = item
    return rows


def static_probe(pointer: str, provider: str | None) -> dict[str, Any]:
    return {
        'ok': True, 'status': 'declared', 'schema': 'dore.source-probe.v0', 'profile': 'document',
        'sourcePointer': pointer, 'resolvedSourcePointer': pointer, 'sourceAuthority': True,
        'probeAuthority': False, 'reflexPersistent': False, 'providerHint': provider,
        'identity': {'title': None, 'creator': None, 'duration': None},
        'capabilities': {'poster': [], 'embed': [], 'media': [], 'manifest': [], 'caption': [], 'oembed': []},
        'needs': [],
        'provenance': {'networkUsed': False, 'declaredProtocolEvidence': True, 'layers': ['source-policy', 'declared-protocol', 'capability-envelope', 'source-dispatch'], 'confidence': 0.7},
        'rights': {'rehost': False, 'decision': 'not-inferred-by-probe'},
    }


def claims_for(pointer: str) -> dict[str, Any]:
    access = []
    if pointer.startswith('https://'): access.append('static-http')
    elif pointer.startswith('file://'): access.append('local-file')
    return {'declaredAccess': access, 'declaredOperations': ['read', 'cite', 'extract'], 'declaredRights': {'rehost': False}}


def build(storefront: dict, identity_map: dict) -> dict[str, Any]:
    if identity_map.get('schema') != 'dore.source-identity-admission.v1':
        raise ValueError('Dawn source identity admission map missing or invalid')
    envelope = load_envelope_module(); items = source_items(storefront); rows = {}; blocked = unresolved = static_ready = 0
    for ref, identity in (identity_map.get('claims') or {}).items():
        item = items.get(ref) or {}; source = item.get('source') or {}
        pointer = str(identity.get('sourcePointer') or source.get('url') or source.get('downloadUrl') or '').strip()
        provider = str(identity.get('sourceAuthority') or source.get('provider') or 'source')
        if not pointer:
            rows[ref] = {'sourceRef': ref, 'canonicalWorkId': identity.get('canonicalWorkId'), 'status': 'unresolved', 'reason': 'source pointer missing'}; unresolved += 1; continue
        if any(token in pointer.casefold() for token in FORBIDDEN):
            rows[ref] = {'sourceRef': ref, 'canonicalWorkId': identity.get('canonicalWorkId'), 'status': 'blocked', 'reason': 'source-policy-deny'}; blocked += 1; continue
        projected = envelope.project(static_probe(pointer, provider), claims_for(pointer))
        decision = projected.get('dispatch') or {}
        if not projected.get('ok') or not decision.get('ok'):
            rows[ref] = {'sourceRef': ref, 'canonicalWorkId': identity.get('canonicalWorkId'), 'status': 'blocked', 'reason': decision.get('reason') or (projected.get('sourcePolicy') or {}).get('reason') or 'source-dispatch-rejected'}; blocked += 1; continue
        status = 'static-ready' if decision.get('materializationReady') is True else 'deferred'
        if status == 'static-ready': static_ready += 1
        else: unresolved += 1
        rows[ref] = {'sourceRef': ref, 'canonicalWorkId': identity.get('canonicalWorkId'), 'identityAdmissionStatus': identity.get('status'), 'status': status, 'sourcePointer': pointer, 'sourceAuthority': provider, 'capabilityEnvelope': projected, 'dispatch': decision, 'ephemeralRepresentation': True, 'surfaceOwnsCapability': False}
    return {'schema': 'dore.dawn-source-capability-map.v1', 'policy': {'sourceCapabilityEnvelope': 'dore.source-capability-envelope.v1', 'sourceDispatcher': 'dore.source-dispatch.v1', 'identityAdmissionRequired': True, 'providerSpecificRoutingForbidden': True, 'browserRuntimeNotOwnedByDawn': True, 'runtimePersistence': False, 'wikisource': 'forbidden'}, 'claimCount': len(rows), 'staticReadyCount': static_ready, 'blockedCount': blocked, 'unresolvedCount': unresolved, 'claims': dict(sorted(rows.items()))}


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument('--storefront', type=Path, default=STOREFRONT); parser.add_argument('--identity-map', type=Path, default=IDENTITY_MAP); parser.add_argument('--out', type=Path, default=OUT); args = parser.parse_args()
    payload = build(read_json(args.storefront), read_json(args.identity_map)); args.out.parent.mkdir(parents=True, exist_ok=True); args.out.write_text(json.dumps(payload, ensure_ascii=False, separators=(',', ':')) + '\n', encoding='utf-8')
    print(json.dumps({k: payload[k] for k in ('claimCount', 'staticReadyCount', 'blockedCount', 'unresolvedCount')}, ensure_ascii=False))
    if payload['blockedCount']: raise SystemExit('Dawn source capability map contains blocked sources')
    return 0


if __name__ == '__main__': raise SystemExit(main())
