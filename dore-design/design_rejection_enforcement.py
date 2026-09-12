#!/usr/bin/env python3
"""Deterministic pre-critic enforcement of bounded rejection guardrails."""
from __future__ import annotations

MAX_REGENERATIONS = 2


def enforce(candidates: list[dict], guardrails: list[dict]) -> dict:
    """Reject candidates that explicitly reproduce a guarded failure domain.

    The executable candidate may expose `risk_domains` produced by generation or
    deterministic geometry checks. Guardrails remain advisory until a candidate
    declares/matches the same domain; then admission to visual critique is blocked.
    """
    guarded = {str(g.get('failure_domain') or '').strip() for g in (guardrails or [])}
    guarded.discard('')
    results = []
    for candidate in candidates:
        risks = {str(x).strip() for x in (candidate.get('risk_domains') or []) if str(x).strip()}
        repeated = sorted(guarded & risks)
        results.append({
            'candidate_id': candidate.get('candidate_id') or candidate.get('id'),
            'admitted_to_critic': not bool(repeated),
            'repeated_failure_domains': repeated,
        })
    blocked = [r for r in results if not r['admitted_to_critic']]
    return {
        'policy': 'rejection-enforcement-v1',
        'guarded_domains': sorted(guarded),
        'candidates': results,
        'all_admitted': not blocked,
        'regeneration_required': bool(blocked),
        'blocked_count': len(blocked),
        'max_regenerations': MAX_REGENERATIONS,
    }
