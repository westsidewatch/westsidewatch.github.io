#!/usr/bin/env python3
"""Compress contextual rejection memory into tiny generation-time guardrails.

Raw rejection evidence remains canonical in ui_taste_memory. This module only
produces a bounded advisory view for the next design generation request.
"""
from __future__ import annotations

import sqlite3

from ui_taste_memory import ensure_schema

MIN_CONFIDENCE = 0.65
MAX_GUARDRAILS = 3


def bounded_rejection_guardrails(
    conn: sqlite3.Connection,
    *,
    surface_family: str | None,
    limit: int = MAX_GUARDRAILS,
    min_confidence: float = MIN_CONFIDENCE,
) -> dict:
    ensure_schema(conn)
    limit = max(1, min(int(limit), MAX_GUARDRAILS))
    threshold = max(0.0, min(1.0, float(min_confidence)))
    clauses = ['contradicted_by_id IS NULL', 'confidence>=?']
    args: list[object] = [threshold]
    if surface_family:
        clauses.append("(surface_family=? OR scope='brand-pattern')")
        args.append(surface_family)
    else:
        clauses.append("scope='brand-pattern'")
    rows = [dict(r) for r in conn.execute(
        '''SELECT id,surface_id,surface_family,direction,reason,failure_domain,scope,confidence,created_at
           FROM dore_ui_taste_rejections
           WHERE ''' + ' AND '.join(clauses) + '''
           ORDER BY confidence DESC, created_at DESC
           LIMIT 24''',
        tuple(args),
    )]
    seen: set[str] = set()
    guardrails = []
    for row in rows:
        domain = str(row.get('failure_domain') or '').strip()
        reason = str(row.get('reason') or '').strip()
        if not domain or not reason or domain in seen:
            continue
        seen.add(domain)
        guardrails.append({
            'failure_domain': domain,
            'avoid': reason,
            'confidence': round(float(row.get('confidence') or 0.0), 4),
            'scope': row.get('scope') or 'local',
            'source_rejection_id': int(row['id']),
        })
        if len(guardrails) >= limit:
            break
    return {
        'policy': 'bounded-rejection-guardrails-v1',
        'surface_family': surface_family,
        'guardrails': guardrails,
        'count': len(guardrails),
        'max_guardrails': limit,
        'min_confidence': threshold,
        'authority': 'advisory-negative-precedent-not-canonical',
    }
