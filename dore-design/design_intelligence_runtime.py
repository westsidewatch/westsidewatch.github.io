#!/usr/bin/env python3
"""Lightweight Doré Design intelligence runtime.

Canonical taste evidence stays in local/dore-local. This bridge only retrieves a
bounded contextual preference pack, decides exploit vs explore, and writes
observed outcomes back to the canonical taste ledger.
"""
from __future__ import annotations

import os
import sqlite3
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
LOCAL_DORE = REPO_ROOT / 'local' / 'dore-local'
if str(LOCAL_DORE) not in sys.path:
    sys.path.insert(0, str(LOCAL_DORE))

import ui_preference_field as preference
import ui_taste_memory as taste


def db_path() -> Path:
    override = os.environ.get('DORE_UI_TASTE_DB')
    if override:
        return Path(override).expanduser()
    home = Path(os.environ.get('DORE_LOCAL_HOME', Path.home() / '.dore')).expanduser()
    return home / 'design' / 'ui-taste.sqlite3'


def connect(path: Path | str | None = None) -> sqlite3.Connection:
    target = Path(path).expanduser() if path else db_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(target)
    conn.row_factory = sqlite3.Row
    taste.ensure_schema(conn)
    return conn


def _context(payload: dict) -> preference.PreferenceContext:
    return preference.PreferenceContext(
        surface_family=payload.get('surface_family'),
        primary_axis=payload.get('primary_axis'),
        viewport_context=payload.get('viewport_context'),
        content_context=payload.get('content_context'),
    )


def _candidates(payload: dict) -> list[str]:
    out = []
    for value in payload.get('candidates') or []:
        value = str(value).strip()
        if value and value not in out:
            out.append(value)
    return out[:12]


def route_task(payload: dict, conn: sqlite3.Connection | None = None) -> dict:
    """Return the smallest contextual hint pack and an exploit/explore verdict."""
    own = conn is None
    conn = conn or connect()
    try:
        ctx = _context(payload)
        pack = preference.bounded_preference_pack(conn, context=ctx, max_claims=3)
        field = preference.fit_pairwise_strengths(conn, context=ctx)
        candidates = _candidates(payload)
        pair = None
        if len(candidates) == 2:
            pair = preference.predict_pair(
                conn, candidate_a=candidates[0], candidate_b=candidates[1], context=ctx
            )

        contradictory = float(field.get('contradiction_pressure') or 0) >= 0.25
        stable_pack = bool(pack.get('claims')) and not pack.get('uncertainty_warning')
        stable_pair = pair is None or pair.get('prediction') not in {'unknown', 'uncertain', 'tie'}
        enough_evidence = int(field.get('comparison_count') or 0) >= 3
        decision = 'exploit' if stable_pack and stable_pair and enough_evidence and not contradictory else 'explore'

        next_pairs = []
        if decision == 'explore' and len(candidates) >= 2:
            next_pairs = preference.next_comparison_candidates(
                conn, context=ctx, candidates=candidates, limit=3
            )
            if not next_pairs:
                next_pairs = [{
                    'candidate_a': candidates[0],
                    'candidate_b': candidates[1],
                    'information_score': 1.0,
                    'estimated_probability_a': 0.5,
                    'reason': 'no-contextual-precedent',
                }]

        return {
            'ok': True,
            'policy': 'dore-design-intelligence-runtime-v1',
            'decision': decision,
            'surface_id': payload.get('surface_id'),
            'task_context': payload.get('task_context'),
            'context': ctx.__dict__,
            'preference_pack': pack,
            'pair_prediction': pair,
            'next_comparisons': next_pairs,
            'variant_generation_required': decision == 'explore',
            'visual_critique_required': True,
            'writeback_required': True,
            'model_inference_connected': False,
            'authority': 'advisory-taste-memory; structured workspace remains canonical',
        }
    finally:
        if own:
            conn.close()


def record_observed_comparison(payload: dict, conn: sqlite3.Connection | None = None) -> dict:
    """Write an observed A/B result and immediately recompute the field."""
    own = conn is None
    conn = conn or connect()
    try:
        a = str(payload.get('candidate_a') or '').strip()
        b = str(payload.get('candidate_b') or '').strip()
        winner = str(payload.get('winner') or '').strip()
        if not a or not b or winner not in {a, b}:
            raise ValueError('candidate_a, candidate_b and valid winner are required')
        surface_id = str(payload.get('surface_id') or '').strip()
        task_context = str(payload.get('task_context') or '').strip()
        primary_axis = str(payload.get('primary_axis') or '').strip()
        winner_reason = str(payload.get('winner_reason') or '').strip()
        loser_reason = str(payload.get('loser_reason') or '').strip()
        evidence_refs = payload.get('evidence_refs') or []
        if not all((surface_id, task_context, primary_axis, winner_reason, loser_reason)):
            raise ValueError('surface_id, task_context, primary_axis and comparison reasons are required')
        if not evidence_refs:
            raise ValueError('evidence_refs required')
        comparison_id = taste.record_comparison(
            conn,
            surface_id=surface_id,
            surface_family=payload.get('surface_family'),
            task_context=task_context,
            primary_axis=primary_axis,
            candidate_a=a,
            candidate_b=b,
            winner=winner,
            winner_reason=winner_reason,
            loser_reason=loser_reason,
            brand_fit=payload.get('brand_fit'),
            usability_floor_passed=bool(payload.get('usability_floor_passed', False)),
            viewport_context=payload.get('viewport_context'),
            content_context=payload.get('content_context'),
            evidence_refs=[str(x) for x in evidence_refs],
            confidence=float(payload.get('confidence', 0.5)),
            scope=payload.get('scope') or 'local',
            supersedes_id=payload.get('supersedes_id'),
        )
        reroute_payload = dict(payload)
        reroute_payload['candidates'] = [a, b]
        return {
            'ok': True,
            'comparison_id': comparison_id,
            'updated': route_task(reroute_payload, conn=conn),
        }
    finally:
        if own:
            conn.close()


def record_observed_rejection(payload: dict, conn: sqlite3.Connection | None = None) -> dict:
    own = conn is None
    conn = conn or connect()
    try:
        surface_id = str(payload.get('surface_id') or '').strip()
        direction = str(payload.get('direction') or '').strip()
        reason = str(payload.get('reason') or '').strip()
        failure_domain = str(payload.get('failure_domain') or '').strip()
        evidence_refs = payload.get('evidence_refs') or []
        if not all((surface_id, direction, reason, failure_domain)) or not evidence_refs:
            raise ValueError('surface_id, direction, reason, failure_domain and evidence_refs are required')
        rejection_id = taste.record_rejection(
            conn,
            surface_id=surface_id,
            surface_family=payload.get('surface_family'),
            direction=direction,
            reason=reason,
            failure_domain=failure_domain,
            scope=payload.get('scope') or 'local',
            evidence_refs=[str(x) for x in evidence_refs],
            confidence=float(payload.get('confidence', 0.5)),
            contradicted_by_id=payload.get('contradicted_by_id'),
        )
        return {'ok': True, 'rejection_id': rejection_id}
    finally:
        if own:
            conn.close()
