#!/usr/bin/env python3
"""Core/A2A worker for Doré Design exploration.

The Design resident never imports a model provider. It writes a durable request,
registers an A2A execution task, then starts this worker as a separate local
process. Real inference reuses Doré's established local model path.

Phase 10 hardens taste formation: one model preference is not design memory.
Each A/B pair is judged twice under blinded aliases with reversed presentation
order. Only canonical-candidate consensus may become a preference winner.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import a2a_execution_plane as plane

HOME = Path(os.environ.get('DORE_LOCAL_HOME', Path.home() / '.dore')).expanduser()
ROOT = HOME / 'design-intelligence-a2a'
REQUESTS = ROOT / 'requests'


def _request_path(task_id: str) -> Path:
    return REQUESTS / f'{task_id}.json'


def _json_object(text: str) -> dict:
    raw = str(text or '').strip()
    if raw.startswith('```'):
        lines = raw.splitlines()
        if lines and lines[0].startswith('```'):
            lines = lines[1:]
        if lines and lines[-1].strip() == '```':
            lines = lines[:-1]
        raw = '\n'.join(lines).strip()
    start, end = raw.find('{'), raw.rfind('}')
    if start < 0 or end < start:
        raise ValueError('model_json_object_missing')
    obj = json.loads(raw[start:end + 1])
    if not isinstance(obj, dict):
        raise ValueError('model_json_object_required')
    return obj


def _normalize_vote(raw: dict, alias_to_candidate: dict[str, str], round_name: str) -> dict:
    alias = str(raw.get('winner') or '').strip()
    if alias not in alias_to_candidate:
        raise ValueError('critic_blind_winner_required')
    winner = alias_to_candidate[alias]
    winner_reason = str(raw.get('winner_reason') or '').strip()
    loser_reason = str(raw.get('loser_reason') or '').strip()
    if not winner_reason or not loser_reason:
        raise ValueError('critic_reasons_required')
    return {
        'round': round_name,
        'blind_winner': alias,
        'winner': winner,
        'winner_reason': winner_reason,
        'loser_reason': loser_reason,
        'brand_fit': str(raw.get('brand_fit') or '').strip() or 'unknown',
        'usability_floor_passed': bool(raw.get('usability_floor_passed')),
        'confidence': max(0.0, min(1.0, float(raw.get('confidence', 0.5)))),
        'failure_domains': [str(x) for x in (raw.get('failure_domains') or [])],
    }


def _aggregate_votes(votes: list[dict]) -> dict:
    if len(votes) != 2:
        raise ValueError('exactly_two_blind_votes_required')
    consensus = votes[0]['winner'] == votes[1]['winner']
    winner = votes[0]['winner'] if consensus else None
    confidence = sum(float(v.get('confidence', 0.5)) for v in votes) / 2.0
    usability = all(bool(v.get('usability_floor_passed')) for v in votes)
    brand_fit = 'pass' if all(v.get('brand_fit') == 'pass' for v in votes) else 'mixed'
    domains = sorted({d for v in votes for d in (v.get('failure_domains') or [])})
    return {
        'consensus': consensus,
        'winner': winner,
        'winner_reason': votes[0]['winner_reason'] if consensus else 'Blind judges disagreed; no canonical preference may be written.',
        'loser_reason': votes[0]['loser_reason'] if consensus else 'No loser is admitted without blind-order consensus.',
        'brand_fit': brand_fit,
        'usability_floor_passed': usability,
        'confidence': confidence if consensus else min(confidence, 0.49),
        'failure_domains': domains,
        'votes': votes,
        'order_bias_check': 'pass' if consensus else 'fail',
        'memory_admission': bool(consensus and usability),
    }


def _fixture(payload: dict) -> dict:
    axis = str(payload.get('primary_axis') or 'composition')
    context = str(payload.get('task_context') or 'design task')
    variants = [
        {'id': 'A', 'direction': f'preserve-{axis}-hierarchy', 'changes': ['reduce competing emphasis', 'retain brand geometry'], 'rationale': f'Conservative response to {context}.'},
        {'id': 'B', 'direction': f'clarify-{axis}-rhythm', 'changes': ['increase focal contrast', 'simplify secondary motion'], 'rationale': f'Clearer response to {context}.'},
    ]
    vote1 = {
        'round': 'blind-1', 'blind_winner': 'Y', 'winner': 'B',
        'winner_reason': 'The stronger focal hierarchy resolves ambiguity without weakening brand geometry.',
        'loser_reason': 'The alternative preserves ambiguity in the focal structure.',
        'brand_fit': 'pass', 'usability_floor_passed': True, 'confidence': 0.87,
        'failure_domains': [],
    }
    disagree = os.environ.get('DORE_DESIGN_A2A_FIXTURE_DISAGREE') == '1'
    vote2 = {
        'round': 'blind-2', 'blind_winner': 'Y' if disagree else 'X', 'winner': 'A' if disagree else 'B',
        'winner_reason': 'Second blind-order judgment.',
        'loser_reason': 'Second blind-order comparison loser.',
        'brand_fit': 'pass', 'usability_floor_passed': True, 'confidence': 0.85,
        'failure_domains': [],
    }
    critic = _aggregate_votes([vote1, vote2])
    return {'variants': variants, 'critic': critic, 'provider': 'deterministic-ci-fixture', 'model': 'fixture'}


def _blind_vote(ollama, *, variants: list[dict], context: dict, mapping: dict[str, str], round_name: str) -> dict:
    by_id = {str(v.get('id')): v for v in variants}
    alias_variants = [
        {'id': alias, 'direction': by_id[candidate].get('direction'), 'changes': by_id[candidate].get('changes'), 'rationale': by_id[candidate].get('rationale')}
        for alias, candidate in mapping.items()
    ]
    system = (
        'You are an independent Doré visual critic. Candidate identities are intentionally blinded. '
        'Compare X and Y against the supplied context, brand constraints, accessibility/usability floor, '
        'and bounded taste evidence. Do not infer the original labels and do not reward novelty by itself. '
        'Return JSON only with winner (X or Y), winner_reason, loser_reason, brand_fit, '
        'usability_floor_passed (boolean), confidence (0..1), failure_domains (array).'
    )
    raw = _json_object(ollama([
        {'role': 'system', 'content': system},
        {'role': 'user', 'content': json.dumps({'context': context, 'variants': alias_variants}, ensure_ascii=False)},
    ]))
    return _normalize_vote(raw, mapping, round_name)


def _model(payload: dict) -> dict:
    # Reuse Doré's established local inference path; do not introduce a second provider.
    from dore_local import ollama

    taste = payload.get('preference_pack') or {}
    system = (
        'You are Doré Design Core. Generate exactly two materially different but brand-faithful '
        'UI directions. Return JSON only with key variants, an array of two objects. Each object '
        'must contain id (A or B), direction, changes (array), rationale. Do not choose a winner.'
    )
    context = {
        'task_context': payload.get('task_context'),
        'surface_id': payload.get('surface_id'),
        'surface_family': payload.get('surface_family'),
        'primary_axis': payload.get('primary_axis'),
        'viewport_context': payload.get('viewport_context'),
        'content_context': payload.get('content_context'),
        'bounded_taste': taste,
        'constraints': payload.get('constraints') or [],
    }
    generated = _json_object(ollama([
        {'role': 'system', 'content': system},
        {'role': 'user', 'content': json.dumps(context, ensure_ascii=False)},
    ]))
    variants = generated.get('variants') or []
    if not isinstance(variants, list) or len(variants) != 2:
        raise ValueError('exactly_two_variants_required')
    ids = [str(x.get('id') or '') for x in variants if isinstance(x, dict)]
    if ids != ['A', 'B']:
        raise ValueError('variant_ids_must_be_A_B')

    # Round 1 shows A as X and B as Y. Round 2 reverses that order and alias mapping.
    vote1 = _blind_vote(ollama, variants=variants, context=context, mapping={'X': 'A', 'Y': 'B'}, round_name='blind-1')
    vote2 = _blind_vote(ollama, variants=variants, context=context, mapping={'X': 'B', 'Y': 'A'}, round_name='blind-2')
    critic = _aggregate_votes([vote1, vote2])
    return {
        'variants': variants,
        'critic': critic,
        'provider': 'dore-local',
        'model': os.environ.get('DORE_MODEL') or os.environ.get('OLLAMA_MODEL') or 'local-default',
    }


def execute(task_id: str) -> dict:
    request_path = _request_path(task_id)
    if not request_path.exists():
        raise FileNotFoundError('design_intelligence_request_missing:' + task_id)
    payload = json.loads(request_path.read_text(encoding='utf-8'))
    owner = plane.worker_id()
    claimed = plane.claim(task_id, owner)
    if not claimed.get('ok'):
        raise RuntimeError('a2a_claim_failed:' + str(claimed.get('code')))
    started = plane.transition(task_id, 'RUNNING', consumer=owner)
    if not started.get('ok'):
        raise RuntimeError('a2a_start_failed:' + str(started.get('code')))
    try:
        result = _fixture(payload) if os.environ.get('DORE_DESIGN_A2A_FIXTURE') == '1' else _model(payload)
        artifact = {
            'type': 'dore.design-intelligence-exploration.v2',
            'task_id': task_id,
            'surface_id': payload.get('surface_id'),
            'variants': result['variants'],
            'critic': result['critic'],
            'provider': result['provider'],
            'model': result['model'],
        }
        recorded = plane.record_artifact(task_id, artifact, consumer=owner)
        if not recorded.get('ok'):
            raise RuntimeError('a2a_artifact_failed:' + str(recorded.get('code')))
        critic = result['critic']
        votes = critic.get('votes') or []
        verification = {
            'ok': len(result['variants']) == 2 and len(votes) == 2 and all(v.get('winner') in {'A', 'B'} for v in votes),
            'method': 'dore.design-intelligence-a2a-worker.v2',
            'independent_critic': True,
            'blind_order_reversal': True,
            'variant_count': len(result['variants']),
            'judge_count': len(votes),
            'consensus': bool(critic.get('consensus')),
            'memory_admission': bool(critic.get('memory_admission')),
        }
        verified = plane.verify(task_id, verification, consumer=owner)
        if not verified.get('ok'):
            raise RuntimeError('a2a_verification_failed')
        completed = plane.complete(task_id, {'ok': True, **result}, consumer=owner)
        if not completed.get('ok'):
            raise RuntimeError('a2a_complete_failed:' + str(completed.get('code')))
        return {'ok': True, 'task_id': task_id, 'status': 'PASS', **result}
    except Exception as exc:
        plane.transition(task_id, 'FAIL', consumer=owner, result={'ok': False, 'error': type(exc).__name__ + ': ' + str(exc)})
        raise


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit('usage: design_intelligence_a2a_worker.py <task-id>')
    result = execute(sys.argv[1])
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
