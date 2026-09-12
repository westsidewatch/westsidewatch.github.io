#!/usr/bin/env python3
"""Core/A2A worker for Doré Design exploration.

The Design resident never imports a model provider. It writes a durable request,
registers an A2A execution task, then starts this worker as a separate local
process. Real inference reuses Doré's established local model path. CI can use a
strict deterministic fixture without changing the resident boundary.
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


def _fixture(payload: dict) -> dict:
    axis = str(payload.get('primary_axis') or 'composition')
    context = str(payload.get('task_context') or 'design task')
    variants = [
        {'id': 'A', 'direction': f'preserve-{axis}-hierarchy', 'changes': ['reduce competing emphasis', 'retain brand geometry'], 'rationale': f'Conservative response to {context}.'},
        {'id': 'B', 'direction': f'clarify-{axis}-rhythm', 'changes': ['increase focal contrast', 'simplify secondary motion'], 'rationale': f'Clearer response to {context}.'},
    ]
    critic = {
        'winner': 'B',
        'winner_reason': 'B creates a clearer focal hierarchy while preserving the requested brand constraints.',
        'loser_reason': 'A preserves the current hierarchy but does not resolve the focal ambiguity strongly enough.',
        'brand_fit': 'pass',
        'usability_floor_passed': True,
        'confidence': 0.86,
        'failure_domains': [],
    }
    return {'variants': variants, 'critic': critic, 'provider': 'deterministic-ci-fixture', 'model': 'fixture'}


def _model(payload: dict) -> dict:
    # Reuse Doré's established local inference path; do not introduce a second provider.
    from dore_local import ollama

    taste = payload.get('preference_pack') or {}
    system = (
        'You are Doré Design Core. Generate exactly two materially different but brand-faithful '
        'UI directions. Return JSON only with key variants, an array of two objects. Each object '
        'must contain id (A or B), direction, changes (array), rationale. Do not choose a winner.'
    )
    user = json.dumps({
        'task_context': payload.get('task_context'),
        'surface_id': payload.get('surface_id'),
        'surface_family': payload.get('surface_family'),
        'primary_axis': payload.get('primary_axis'),
        'viewport_context': payload.get('viewport_context'),
        'content_context': payload.get('content_context'),
        'bounded_taste': taste,
        'constraints': payload.get('constraints') or [],
    }, ensure_ascii=False)
    generated = _json_object(ollama([{'role': 'system', 'content': system}, {'role': 'user', 'content': user}]))
    variants = generated.get('variants') or []
    if not isinstance(variants, list) or len(variants) != 2:
        raise ValueError('exactly_two_variants_required')
    ids = [str(x.get('id') or '') for x in variants if isinstance(x, dict)]
    if ids != ['A', 'B']:
        raise ValueError('variant_ids_must_be_A_B')

    critic_system = (
        'You are an independent Doré visual critic. Compare A and B against the supplied context, '
        'brand constraints, accessibility/usability floor, and bounded taste evidence. Do not reward '
        'novelty by itself. Return JSON only with winner (A or B), winner_reason, loser_reason, '
        'brand_fit, usability_floor_passed (boolean), confidence (0..1), failure_domains (array).'
    )
    critic_user = json.dumps({
        'context': user,
        'variants': variants,
    }, ensure_ascii=False)
    critic = _json_object(ollama([{'role': 'system', 'content': critic_system}, {'role': 'user', 'content': critic_user}]))
    if critic.get('winner') not in {'A', 'B'}:
        raise ValueError('critic_winner_required')
    critic['confidence'] = max(0.0, min(1.0, float(critic.get('confidence', 0.5))))
    critic['usability_floor_passed'] = bool(critic.get('usability_floor_passed'))
    if not str(critic.get('winner_reason') or '').strip() or not str(critic.get('loser_reason') or '').strip():
        raise ValueError('critic_reasons_required')
    return {'variants': variants, 'critic': critic, 'provider': 'dore-local', 'model': os.environ.get('DORE_MODEL') or os.environ.get('OLLAMA_MODEL') or 'local-default'}


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
            'type': 'dore.design-intelligence-exploration.v1',
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
        verification = {
            'ok': len(result['variants']) == 2 and critic.get('winner') in {'A', 'B'} and bool(critic.get('winner_reason')) and bool(critic.get('loser_reason')),
            'method': 'dore.design-intelligence-a2a-worker.v1',
            'independent_critic': True,
            'variant_count': len(result['variants']),
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
