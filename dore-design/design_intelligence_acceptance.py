#!/usr/bin/env python3
"""Deterministic acceptance for Doré Design intelligence runtime v1."""
from __future__ import annotations

import json
import sqlite3

import design_intelligence_runtime as runtime
import ui_preference_field as preference
import ui_taste_memory as taste


def memory_db():
    conn = sqlite3.connect(':memory:')
    conn.row_factory = sqlite3.Row
    taste.ensure_schema(conn)
    return conn


def comparison(conn, *, surface_id, winner='A', confidence=0.9, family='living-water', axis='composition'):
    return taste.record_comparison(
        conn,
        surface_id=surface_id,
        surface_family=family,
        task_context='homepage visual hierarchy',
        primary_axis=axis,
        candidate_a='A',
        candidate_b='B',
        winner=winner,
        winner_reason=f'{winner} preserves hierarchy and authored identity',
        loser_reason='loser weakens hierarchy or geometry continuity',
        brand_fit='Living Water',
        usability_floor_passed=True,
        viewport_context='desktop',
        content_context='bilingual',
        evidence_refs=[f'acceptance:{surface_id}:{winner}'],
        confidence=confidence,
        scope='surface-family',
    )


def payload():
    return {
        'surface_id': 'living-water-candidate-01',
        'surface_family': 'living-water',
        'task_context': 'homepage visual hierarchy',
        'primary_axis': 'composition',
        'viewport_context': 'desktop',
        'content_context': 'bilingual',
        'candidates': ['A', 'B'],
    }


def check():
    results = {}

    # 1. Stable, repeated, context-matched preference must exploit.
    with memory_db() as conn:
        for i in range(4):
            comparison(conn, surface_id=f'candidate-{i}', winner='A')
        routed = runtime.route_task(payload(), conn=conn)
        assert routed['decision'] == 'exploit', routed
        assert routed['pair_prediction']['prediction'] == 'A', routed
        results['stable_preference_exploits'] = True

    # 2. No precedent must explore, never invent a preference.
    with memory_db() as conn:
        routed = runtime.route_task(payload(), conn=conn)
        assert routed['decision'] == 'explore', routed
        assert routed['preference_pack']['claims'] == [], routed
        assert routed['variant_generation_required'] is True, routed
        results['sparse_evidence_explores'] = True

    # 3. Contradictory evidence must explore rather than average into false certainty.
    with memory_db() as conn:
        comparison(conn, surface_id='a1', winner='A')
        comparison(conn, surface_id='a2', winner='A')
        comparison(conn, surface_id='b1', winner='B')
        comparison(conn, surface_id='b2', winner='B')
        routed = runtime.route_task(payload(), conn=conn)
        assert routed['decision'] == 'explore', routed
        assert routed['preference_pack']['uncertainty_warning'], routed
        results['contradiction_explores'] = True

    # 4. Observed winner writes through to ledger and immediately changes the field.
    with memory_db() as conn:
        comparison(conn, surface_id='seed-1', winner='A', confidence=0.7)
        comparison(conn, surface_id='seed-2', winner='A', confidence=0.7)
        ctx = preference.PreferenceContext(
            surface_family='living-water', primary_axis='composition',
            viewport_context='desktop', content_context='bilingual'
        )
        before = preference.predict_pair(conn, candidate_a='A', candidate_b='B', context=ctx)
        write = dict(payload())
        write.update({
            'surface_id': 'observed-new',
            'candidate_a': 'A',
            'candidate_b': 'B',
            'winner': 'B',
            'winner_reason': 'B wins observed runtime review after geometry correction',
            'loser_reason': 'A retains a visible geometry seam',
            'brand_fit': 'Living Water',
            'usability_floor_passed': True,
            'evidence_refs': ['runtime:observed-new'],
            'confidence': 1.0,
            'scope': 'surface-family',
        })
        recorded = runtime.record_observed_comparison(write, conn=conn)
        after = preference.predict_pair(conn, candidate_a='A', candidate_b='B', context=ctx)
        assert recorded['comparison_id'] > 0, recorded
        assert after['field']['comparison_count'] == before['field']['comparison_count'] + 1, (before, after)
        assert after['probability_a'] < before['probability_a'], (before, after)
        results['writeback_updates_field_immediately'] = True

    # 5. Context mismatch must not leak local preference into an unrelated family.
    with memory_db() as conn:
        for i in range(4):
            comparison(conn, surface_id=f'local-{i}', winner='A', family='living-water')
        other = payload()
        other['surface_family'] = 'dawn-library'
        routed = runtime.route_task(other, conn=conn)
        assert routed['decision'] == 'explore', routed
        assert routed['preference_pack']['comparison_count'] == 0, routed
        results['context_mismatch_does_not_leak'] = True

    return {'ok': all(results.values()), 'policy': 'design-intelligence-acceptance-v1', 'checks': results}


if __name__ == '__main__':
    out = check()
    print(json.dumps(out, ensure_ascii=False, sort_keys=True))
    raise SystemExit(0 if out['ok'] else 1)
