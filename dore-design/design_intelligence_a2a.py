#!/usr/bin/env python3
"""Doré Design -> Core/A2A exploration bridge.

This module owns no model client. It persists the bounded design request,
registers a durable A2A execution task, launches the local Core worker as a
separate process, verifies PASS evidence, then writes the observed critic winner
back through the canonical Phase 8 taste-memory API.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import uuid
from pathlib import Path

import design_intelligence_runtime as intelligence

REPO_ROOT = Path(__file__).resolve().parent.parent
LOCAL_DORE = REPO_ROOT / 'local' / 'dore-local'
if str(LOCAL_DORE) not in sys.path:
    sys.path.insert(0, str(LOCAL_DORE))

import a2a_execution_plane as plane


def _home() -> Path:
    return Path(os.environ.get('DORE_LOCAL_HOME', Path.home() / '.dore')).expanduser()


def _request_path(task_id: str) -> Path:
    return _home() / 'design-intelligence-a2a' / 'requests' / f'{task_id}.json'


def _write_request(task_id: str, payload: dict) -> Path:
    target = _request_path(task_id)
    target.parent.mkdir(parents=True, exist_ok=True)
    tmp = target.with_suffix('.tmp')
    tmp.write_text(json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + '\n', encoding='utf-8')
    tmp.replace(target)
    return target


def _worker(task_id: str) -> dict:
    env = dict(os.environ)
    env['DORE_REPO_ROOT'] = str(REPO_ROOT)
    cp = subprocess.run(
        [sys.executable, str(LOCAL_DORE / 'design_intelligence_a2a_worker.py'), task_id],
        cwd=str(REPO_ROOT), env=env, text=True, capture_output=True,
        timeout=max(30, int(os.environ.get('DORE_DESIGN_A2A_TIMEOUT', '360'))),
    )
    if cp.returncode != 0:
        raise RuntimeError('design_a2a_worker_failed:' + (cp.stderr or cp.stdout or '')[-3000:])
    try:
        return json.loads((cp.stdout or '').strip().splitlines()[-1])
    except Exception as exc:
        raise RuntimeError('design_a2a_worker_invalid_result') from exc


def explore(payload: dict) -> dict:
    routed = intelligence.route_task(payload)
    if routed.get('decision') != 'explore':
        return {
            'ok': True,
            'decision': 'exploit',
            'exploration_started': False,
            'route': routed,
            'reason': 'stable_contextual_preference_available',
        }

    task_id = 'design-explore-' + uuid.uuid4().hex
    request = {
        'schema': 'dore.design-intelligence-a2a-request.v1',
        'task_id': task_id,
        'surface_id': payload.get('surface_id'),
        'surface_family': payload.get('surface_family'),
        'task_context': payload.get('task_context'),
        'primary_axis': payload.get('primary_axis'),
        'viewport_context': payload.get('viewport_context'),
        'content_context': payload.get('content_context'),
        'constraints': payload.get('constraints') or [],
        'preference_pack': routed.get('preference_pack') or {},
        'inference_boundary': 'core-a2a-only',
    }
    request_path = _write_request(task_id, request)
    task = plane.register({
        'message_id': task_id,
        'kind': 'dore_design_intelligence_explore',
        'related_goal': 'dore-design-intelligence',
        'body': {'request_path': str(request_path)},
    })
    if task.get('status') != 'ACCEPTED':
        raise RuntimeError('design_a2a_task_not_accepted')

    worker_result = _worker(task_id)
    proof = plane.status(task_id)
    if not proof.get('completion_evidence'):
        raise RuntimeError('design_a2a_completion_evidence_missing')
    artifact = (proof.get('task') or {}).get('artifact') or {}
    variants = artifact.get('variants') or worker_result.get('variants') or []
    critic = artifact.get('critic') or worker_result.get('critic') or {}
    by_id = {str(v.get('id')): v for v in variants if isinstance(v, dict)}
    if set(by_id) != {'A', 'B'}:
        raise RuntimeError('design_a2a_exact_variants_missing')
    winner = str(critic.get('winner') or '')
    if winner not in by_id:
        raise RuntimeError('design_a2a_winner_missing')

    observed = intelligence.record_observed_comparison({
        **payload,
        'candidate_a': 'A',
        'candidate_b': 'B',
        'winner': winner,
        'winner_reason': str(critic.get('winner_reason') or ''),
        'loser_reason': str(critic.get('loser_reason') or ''),
        'brand_fit': critic.get('brand_fit'),
        'usability_floor_passed': bool(critic.get('usability_floor_passed')),
        'confidence': float(critic.get('confidence', 0.5)),
        'evidence_refs': [
            'a2a-task:' + task_id,
            'a2a-artifact:' + str(artifact.get('sha256') or 'recorded'),
            'visual-critic:' + winner,
        ],
        'scope': payload.get('scope') or 'local',
    })
    return {
        'ok': True,
        'decision': 'explore',
        'exploration_started': True,
        'task_id': task_id,
        'a2a_status': 'PASS',
        'completion_evidence': True,
        'provider': artifact.get('provider') or worker_result.get('provider'),
        'model': artifact.get('model') or worker_result.get('model'),
        'variants': variants,
        'critic': critic,
        'winner': winner,
        'writeback': observed,
        'route_before': routed,
        'route_after': observed.get('updated'),
        'production_promoted': False,
        'inference_boundary': 'core-a2a-only',
    }


def health() -> dict:
    worker = LOCAL_DORE / 'design_intelligence_a2a_worker.py'
    return {
        'ok': worker.exists(),
        'phase': 9,
        'policy': 'dore-design-core-a2a-loop-v1',
        'worker_available': worker.exists(),
        'inference_boundary': 'core-a2a-only',
        'design_process_has_model_client': False,
        'fixture_mode': os.environ.get('DORE_DESIGN_A2A_FIXTURE') == '1',
        'production_promotion': False,
    }
