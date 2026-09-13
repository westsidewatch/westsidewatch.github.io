#!/usr/bin/env python3
"""Executable pre-critic verifier for bounded rejection guardrails.

Generation-time self-reported risk is evidence, not authority. A historical
failure domain blocks a candidate only when the executable patch does not make
a domain-relevant change. The real raster critic remains the final visual
authority after this cheap preflight gate.
"""
from __future__ import annotations

DOMAIN_OPS = {
    'vertical-gravity': {'move'},
    'focal-competition': {'move', 'resize', 'font_size'},
    'text-density': {'resize', 'font_size'},
    'alignment-drift': {'move', 'text_align'},
    'spacing-rhythm': {'move', 'resize'},
    'scale-hierarchy': {'resize', 'font_size'},
    'edge-crowding': {'move', 'resize'},
    'image-text-balance': {'move', 'resize'},
}

# Current Design patch DSL has no color/contrast operation, so this domain
# cannot be proven avoided before raster critique and must remain blocked.
UNSATISFIABLE_WITH_CURRENT_DSL = {'contrast-hierarchy'}


def verify_candidate(candidate: dict, guardrails: list[dict]) -> dict:
    patch = candidate.get('patch') or {}
    ops = patch.get('ops') or []
    used_ops = {str((op or {}).get('op') or '').strip() for op in ops}
    used_ops.discard('')
    repeated = []
    avoided = []
    evidence = []
    for guardrail in guardrails or []:
        domain = str((guardrail or {}).get('failure_domain') or '').strip()
        if not domain:
            continue
        allowed = DOMAIN_OPS.get(domain)
        if domain in UNSATISFIABLE_WITH_CURRENT_DSL or not allowed:
            repeated.append(domain)
            evidence.append({'failure_domain': domain, 'status': 'blocked', 'reason': 'no-domain-relevant-executable-op'})
            continue
        matched = sorted(used_ops & allowed)
        if matched:
            avoided.append(domain)
            evidence.append({'failure_domain': domain, 'status': 'addressed', 'ops': matched})
        else:
            repeated.append(domain)
            evidence.append({'failure_domain': domain, 'status': 'blocked', 'required_any_op': sorted(allowed)})
    return {
        'policy': 'executable-guardrail-preflight-v1',
        'candidate_id': candidate.get('candidate_id') or candidate.get('id'),
        'used_ops': sorted(used_ops),
        'addressed_failure_domains': sorted(set(avoided)),
        'repeated_failure_domains': sorted(set(repeated)),
        'admitted_to_critic': not bool(repeated),
        'evidence': evidence,
        'authority': 'preflight-only-real-raster-critic-remains-final',
    }
