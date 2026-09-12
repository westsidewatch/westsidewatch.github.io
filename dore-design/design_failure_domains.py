#!/usr/bin/env python3
"""Bounded failure-domain vocabulary for Doré Design raster critique.

Only domains that can be supported by a static browser raster may enter the
pixel-grounded rejection ledger. Motion/interaction failures require separate
motion evidence and are intentionally excluded here.
"""
from __future__ import annotations

PIXEL_DOMAINS = {
    'vertical-gravity',
    'focal-competition',
    'text-density',
    'alignment-drift',
    'spacing-rhythm',
    'scale-hierarchy',
    'edge-crowding',
    'contrast-hierarchy',
    'image-text-balance',
}

NON_PIXEL_DOMAINS = {
    'motion-frame-mismatch',
    'interaction-timing',
    'scroll-rhythm',
}

MAX_FAILURES = 3


def normalize_failure(item: dict) -> dict:
    if not isinstance(item, dict):
        raise ValueError('failure_domain_object_required')
    domain = str(item.get('domain') or '').strip()
    if domain not in PIXEL_DOMAINS:
        if domain in NON_PIXEL_DOMAINS:
            raise ValueError('failure_domain_requires_non_pixel_evidence:' + domain)
        raise ValueError('unknown_failure_domain:' + domain)
    reason = str(item.get('reason') or '').strip()
    pixel_basis = str(item.get('pixel_basis') or '').strip()
    if not reason or not pixel_basis:
        raise ValueError('failure_reason_and_pixel_basis_required')
    confidence = max(0.0, min(1.0, float(item.get('confidence', 0.5))))
    return {
        'domain': domain,
        'reason': reason,
        'pixel_basis': pixel_basis,
        'confidence': confidence,
    }


def normalize_failures(values) -> list[dict]:
    if not isinstance(values, list) or not values:
        raise ValueError('loser_failures_required')
    if len(values) > MAX_FAILURES:
        raise ValueError('too_many_loser_failures')
    out, seen = [], set()
    for value in values:
        item = normalize_failure(value)
        if item['domain'] in seen:
            raise ValueError('duplicate_failure_domain:' + item['domain'])
        seen.add(item['domain'])
        out.append(item)
    return out


def prompt_contract() -> dict:
    return {
        'allowed_pixel_domains': sorted(PIXEL_DOMAINS),
        'forbidden_without_motion_evidence': sorted(NON_PIXEL_DOMAINS),
        'max_failures': MAX_FAILURES,
        'required_fields': ['domain', 'reason', 'pixel_basis', 'confidence'],
    }
