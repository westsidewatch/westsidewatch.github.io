#!/usr/bin/env python3
"""Deterministic acceptance for Design -> Core/A2A -> blind critic -> taste write-back."""
from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        os.environ['DORE_LOCAL_HOME'] = str(root / 'home')
        os.environ['DORE_UI_TASTE_DB'] = str(root / 'taste.sqlite3')
        os.environ['DORE_DESIGN_A2A_FIXTURE'] = '1'
        os.environ['DORE_DESIGN_A2A_TIMEOUT'] = '60'
        os.environ.pop('DORE_DESIGN_A2A_FIXTURE_DISAGREE', None)

        # Imports happen after env setup so the A2A execution plane uses the temp home.
        import importlib
        import a2a_execution_plane
        import design_intelligence_a2a
        import design_intelligence_runtime
        importlib.reload(a2a_execution_plane)
        importlib.reload(design_intelligence_a2a)

        payload = {
            'surface_id': 'candidate-01-page2',
            'surface_family': 'living-water-candidate',
            'task_context': 'repair four-pane assembly hierarchy without changing the accepted motion language',
            'primary_axis': 'visual-hierarchy',
            'viewport_context': 'desktop-1440',
            'content_context': 'four-pane-focus-current',
            'constraints': ['preserve 8:5 identity', 'preserve accepted motion', 'no production promotion'],
            'candidates': ['seed-A', 'seed-B'],
        }
        before = design_intelligence_runtime.route_task(payload)
        assert before['decision'] == 'explore', before
        out = design_intelligence_a2a.explore(payload)
        assert out['ok'] and out['decision'] == 'explore'
        assert out['a2a_status'] == 'PASS' and out['completion_evidence'] is True
        assert out['inference_boundary'] == 'core-a2a-only'
        assert out['production_promoted'] is False
        assert out['provider'] == 'deterministic-ci-fixture'
        assert [v['id'] for v in out['variants']] == ['A', 'B']
        assert out['judge_count'] == 2 and out['blind_order_reversal'] is True
        assert out['consensus'] is True and out['winner'] == 'B'
        assert out['critic']['order_bias_check'] == 'pass'
        assert out['critic']['usability_floor_passed'] is True
        assert out['memory_admitted'] is True
        assert out['writeback']['comparison_id'] > 0

        proof = a2a_execution_plane.status(out['task_id'])
        assert proof['completion_evidence'] is True
        task = proof['task']
        assert task['status'] == 'PASS'
        assert task['artifact']['type'] == 'dore.design-intelligence-exploration.v2'
        assert task['verification']['independent_critic'] is True
        assert task['verification']['blind_order_reversal'] is True
        assert task['verification']['judge_count'] == 2
        assert task['verification']['consensus'] is True
        assert task['verification']['memory_admission'] is True

        # A disagreement is still a valid exploration artifact, but it must not
        # contaminate durable taste memory.
        os.environ['DORE_DESIGN_A2A_FIXTURE_DISAGREE'] = '1'
        disagreement_payload = {
            **payload,
            'surface_id': 'fresh-disagreement-surface',
            'surface_family': 'fresh-disagreement-family',
            'task_context': 'test order-bias resistance on an unseen surface',
            'content_context': 'blind-disagreement-control',
        }
        disagree = design_intelligence_a2a.explore(disagreement_payload)
        assert disagree['ok'] and disagree['a2a_status'] == 'PASS'
        assert disagree['judge_count'] == 2
        assert disagree['consensus'] is False
        assert disagree['winner'] is None
        assert disagree['memory_admitted'] is False
        assert disagree['writeback'] is None
        assert disagree['writeback_block_reason'] == 'judge_disagreement'
        assert disagree['requires_more_evidence'] is True
        dproof = a2a_execution_plane.status(disagree['task_id'])
        assert dproof['completion_evidence'] is True
        assert dproof['task']['verification']['consensus'] is False
        assert dproof['task']['verification']['memory_admission'] is False

        print(json.dumps({
            'ok': True,
            'policy': 'dore-design-blind-consensus-acceptance-v1',
            'checks': {
                'explore_creates_durable_a2a_task': True,
                'two_variants_generated': True,
                'two_blind_judges_run': True,
                'presentation_order_reversed': True,
                'consensus_winner_writes_back': True,
                'judge_disagreement_blocks_memory': True,
                'disagreement_preserves_exploration_artifact': True,
                'completion_requires_verified_artifact': True,
                'design_process_has_no_model_client': True,
                'production_promotion_blocked': True,
            },
            'consensus_task_id': out['task_id'],
            'disagreement_task_id': disagree['task_id'],
            'winner': out['winner'],
        }, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
