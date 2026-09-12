#!/usr/bin/env python3
from __future__ import annotations

import json
import math
import sqlite3
from collections import defaultdict
from dataclasses import dataclass
from typing import Iterable

from ui_taste_memory import ensure_schema


@dataclass(frozen=True)
class PreferenceContext:
    surface_family: str | None = None
    primary_axis: str | None = None
    viewport_context: str | None = None
    content_context: str | None = None


def _rows(conn: sqlite3.Connection, ctx: PreferenceContext, limit: int = 500) -> list[dict]:
    ensure_schema(conn)
    clauses, args = ["usability_floor_passed=1"], []
    if ctx.surface_family:
        clauses.append("(surface_family=? OR scope='brand-pattern')")
        args.append(ctx.surface_family)
    if ctx.primary_axis:
        clauses.append("primary_axis=?")
        args.append(ctx.primary_axis)
    if ctx.viewport_context:
        clauses.append("(viewport_context IS NULL OR viewport_context=?)")
        args.append(ctx.viewport_context)
    if ctx.content_context:
        clauses.append("(content_context IS NULL OR content_context=?)")
        args.append(ctx.content_context)
    sql = (
        "SELECT id,surface_id,surface_family,task_context,primary_axis,candidate_a,candidate_b,winner,"
        "winner_reason,loser_reason,viewport_context,content_context,evidence_refs_json,confidence,scope,created_at "
        "FROM dore_ui_taste_comparisons WHERE " + " AND ".join(clauses) +
        " ORDER BY created_at DESC LIMIT ?"
    )
    return [dict(r) for r in conn.execute(sql, (*args, max(1, min(limit, 2000))))]


def _sigmoid(x: float) -> float:
    if x >= 0:
        z = math.exp(-x)
        return 1.0 / (1.0 + z)
    z = math.exp(x)
    return z / (1.0 + z)


def fit_pairwise_strengths(
    conn: sqlite3.Connection,
    *,
    context: PreferenceContext,
    iterations: int = 80,
    learning_rate: float = 0.08,
    l2: float = 0.02,
) -> dict:
    """Fit a tiny Bradley-Terry-like field over context-near pairwise evidence.

    This is deliberately dependency-free. The canonical evidence remains the ledger;
    returned strengths are a disposable derived view.
    """
    rows = _rows(conn, context)
    names = sorted({r['candidate_a'] for r in rows} | {r['candidate_b'] for r in rows})
    beta = {name: 0.0 for name in names}
    weighted = []
    for r in rows:
        a, b, w = r['candidate_a'], r['candidate_b'], r['winner']
        if w not in {a, b}:
            continue
        confidence = max(0.05, min(1.0, float(r.get('confidence') or 0.5)))
        scope_weight = {'local': 0.70, 'surface-family': 0.90, 'brand-pattern': 1.0}.get(r.get('scope'), 0.7)
        weighted.append((a, b, 1.0 if w == a else 0.0, confidence * scope_weight, r))
    for _ in range(max(1, iterations)):
        grad = {name: -l2 * beta[name] for name in names}
        for a, b, y, weight, _ in weighted:
            p = _sigmoid(beta[a] - beta[b])
            e = weight * (y - p)
            grad[a] += e
            grad[b] -= e
        for name in names:
            beta[name] += learning_rate * grad[name]
        if names:
            mean = sum(beta.values()) / len(names)
            for name in names:
                beta[name] -= mean

    stats = {name: {'wins': 0, 'losses': 0, 'evidence': 0, 'weighted_evidence': 0.0} for name in names}
    pair_outcomes = defaultdict(lambda: [0, 0])
    surfaces = defaultdict(set)
    for a, b, y, weight, r in weighted:
        wa, wb = (a, b) if y == 1.0 else (b, a)
        stats[wa]['wins'] += 1
        stats[wb]['losses'] += 1
        for name in (a, b):
            stats[name]['evidence'] += 1
            stats[name]['weighted_evidence'] += weight
            surfaces[name].add(r['surface_id'])
        key = tuple(sorted((a, b)))
        if y == 1.0:
            pair_outcomes[key][0 if key[0] == a else 1] += 1
        else:
            pair_outcomes[key][0 if key[0] == b else 1] += 1

    contradiction_pairs = 0
    for left, right in pair_outcomes.values():
        if left and right:
            contradiction_pairs += 1
    contradiction_pressure = contradiction_pairs / max(1, len(pair_outcomes))

    ranking = []
    for name in names:
        evidence = stats[name]['evidence']
        breadth = len(surfaces[name])
        evidence_conf = min(1.0, math.log1p(stats[name]['weighted_evidence']) / math.log(6.0))
        breadth_conf = min(1.0, breadth / 3.0)
        confidence = max(0.0, min(1.0, 0.65 * evidence_conf + 0.35 * breadth_conf - 0.45 * contradiction_pressure))
        ranking.append({
            'candidate': name,
            'strength': round(beta[name], 6),
            'confidence': round(confidence, 4),
            'evidence': evidence,
            'surface_breadth': breadth,
            **stats[name],
        })
    ranking.sort(key=lambda x: x['strength'], reverse=True)
    return {
        'policy': 'contextual-pairwise-preference-field-v1',
        'context': context.__dict__,
        'comparison_count': len(weighted),
        'candidate_count': len(names),
        'contradiction_pressure': round(contradiction_pressure, 4),
        'ranking': ranking,
        'authority': 'derived-cache-only',
    }


def predict_pair(
    conn: sqlite3.Connection,
    *,
    candidate_a: str,
    candidate_b: str,
    context: PreferenceContext,
) -> dict:
    field = fit_pairwise_strengths(conn, context=context)
    by_name = {r['candidate']: r for r in field['ranking']}
    a = by_name.get(candidate_a)
    b = by_name.get(candidate_b)
    if not a or not b:
        return {
            'candidate_a': candidate_a,
            'candidate_b': candidate_b,
            'prediction': 'unknown',
            'probability_a': 0.5,
            'confidence': 0.0,
            'reason': 'insufficient-contextual-precedent',
            'field': field,
        }
    p = _sigmoid(a['strength'] - b['strength'])
    conf = min(a['confidence'], b['confidence'])
    margin = abs(p - 0.5) * 2.0
    confidence = conf * margin
    prediction = candidate_a if p > 0.5 else candidate_b if p < 0.5 else 'tie'
    if confidence < 0.25:
        prediction = 'uncertain'
    return {
        'candidate_a': candidate_a,
        'candidate_b': candidate_b,
        'prediction': prediction,
        'probability_a': round(p, 4),
        'confidence': round(confidence, 4),
        'reason': 'contextual-pairwise-field',
        'field': field,
    }


def next_comparison_candidates(
    conn: sqlite3.Connection,
    *,
    context: PreferenceContext,
    candidates: Iterable[str] | None = None,
    limit: int = 5,
) -> list[dict]:
    """Return high-information pairs: close, under-observed, or contradiction-prone."""
    field = fit_pairwise_strengths(conn, context=context)
    ranking = field['ranking']
    allowed = set(candidates or [r['candidate'] for r in ranking])
    rows = [r for r in ranking if r['candidate'] in allowed]
    out = []
    for i, a in enumerate(rows):
        for b in rows[i + 1:]:
            p = _sigmoid(a['strength'] - b['strength'])
            closeness = 1.0 - abs(p - 0.5) * 2.0
            low_evidence = 1.0 - min(1.0, min(a['evidence'], b['evidence']) / 4.0)
            uncertainty = 1.0 - min(a['confidence'], b['confidence'])
            score = 0.50 * closeness + 0.30 * uncertainty + 0.20 * low_evidence
            out.append({
                'candidate_a': a['candidate'],
                'candidate_b': b['candidate'],
                'information_score': round(score, 4),
                'estimated_probability_a': round(p, 4),
                'reason': 'close-strength/uncertain/sparse-evidence',
            })
    out.sort(key=lambda x: x['information_score'], reverse=True)
    return out[:max(1, min(int(limit), 12))]


def bounded_preference_pack(
    conn: sqlite3.Connection,
    *,
    context: PreferenceContext,
    max_claims: int = 3,
) -> dict:
    """Compress design history into a very small runtime hint pack."""
    field = fit_pairwise_strengths(conn, context=context)
    ranking = field['ranking']
    claims = []
    for row in ranking[:max(1, min(max_claims, 3))]:
        if row['confidence'] < 0.35 or row['evidence'] < 2:
            continue
        claims.append({
            'candidate': row['candidate'],
            'relative_strength': row['strength'],
            'confidence': row['confidence'],
            'evidence': row['evidence'],
            'scope': 'contextual-only',
        })
    warning = None
    if field['contradiction_pressure'] >= 0.25:
        warning = 'context contains contradictory preference evidence; do not promote a global rule'
    elif not claims:
        warning = 'insufficient stable precedent; explore rather than imitate history'
    return {
        'policy': 'bounded-preference-pack-v1',
        'context': context.__dict__,
        'claims': claims,
        'uncertainty_warning': warning,
        'comparison_count': field['comparison_count'],
        'authority': 'advisory-not-canonical',
    }
