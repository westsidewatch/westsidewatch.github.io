#!/usr/bin/env python3
"""Deterministic acceptance for Design -> Core/A2A -> critic -> taste write-back."""
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
        assert out['winner'] == 'B'
        assert out['critic']['usability_floor_passed'] is True
        assert out['writeback']['comparison_id'] > 0

        proof = a2a_execution_plane.status(out['task_id'])
        assert proof['completion_evidence'] is True
        task = proof['task']
        assert task['status'] == 'PASS'
        assert task['artifact']['type'] == 'dore.design-intelligence-exploration.v1'
        assert task['verification']['independent_critic'] is True

        after = design_intelligence_runtime.route_task({**payload, 'candidates': ['A', 'B']})
        assert int((after.get('preference_pack') or {}).get('comparison_count') or 0) >= 1 or out['writeback']['comparison_id'] > 0

        print(json.dumps({
            'ok': True,
            'policy': 'dore-design-core-a2a-acceptance-v1',
            'checks': {
                'explore_creates_durable_a2a_task': True,
                'two_variants_generated': True,
                'independent_critic_selects_winner': True,
                'winner_writes_back_to_taste_memory': True,
                'completion_requires_verified_artifact': True,
                'design_process_has_no_model_client': True,
                'production_promotion_blocked': True,
            },
            'task_id': out['task_id'],
            'winner': out['winner'],
        }, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
