#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DESIGN = ROOT / 'dore-design'
LOCAL = ROOT / 'local' / 'dore-local'


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    contract = json.loads((DESIGN / 'design_intelligence_release_contract.json').read_text(encoding='utf-8'))
    require(contract.get('schema') == 'dore.design-intelligence.release-contract.v1', 'release contract schema')
    require(contract.get('release') == '1.0.0', 'release version')
    require(contract.get('status') == 'graduated', 'graduation status')
    require(contract.get('capability_phase') == 16, 'capability phase')

    runtime = contract.get('runtime') or {}
    require(runtime.get('active_worker') == 'design_intelligence_a2a_worker_v11', 'active worker frozen')
    require(runtime.get('inference_boundary') == 'core-a2a-only', 'inference boundary frozen')
    require(runtime.get('real_browser_raster_required') is True, 'real browser evidence required')
    require(runtime.get('blind_judges') == 2 and runtime.get('blind_order_reversal') is True, 'blind judge contract')

    entry = (LOCAL / 'design_intelligence_a2a_worker.py').read_text(encoding='utf-8')
    require("design_intelligence_a2a_worker_v11" in entry, 'runtime entrypoint does not target frozen worker')

    learner = (LOCAL / 'ui_capability_learner.py').read_text(encoding='utf-8')
    require("UI_POLICY = 'dore-ui-capability-learning-v4'" in learner, 'UI v4 policy missing')
    for name in ('ui-v1.json', 'ui-v2.json', 'ui-v3.json', 'ui-v4.json'):
        require((LOCAL / 'learning-gates' / name).is_file(), f'missing {name}')
        require(name in learner, f'loader does not reference {name}')

    bridge = (DESIGN / 'design_intelligence_a2a.py').read_text(encoding='utf-8')
    require("'real_browser_raster_required':True" in bridge, 'bridge health lost real-browser requirement')
    require("'pixel_evidence_primary':True" in bridge, 'bridge health lost pixel authority')
    require("'canonical_workspace_mutation_allowed':False" in bridge, 'canonical mutation invariant lost')
    require("'production_promotion':False" in bridge, 'production default invariant lost')

    learning = contract.get('learning') or {}
    require(learning.get('gate_count') == 25, 'gate count not frozen at 25')
    require(learning.get('anti_recurrence_enforcement') is True, 'anti recurrence missing')
    require(learning.get('bounded_repair_loop') is True, 'repair loop missing')

    authority = contract.get('authority') or {}
    require(authority.get('pixel_evidence_primary') is True, 'pixel authority missing')
    require(authority.get('canonical_workspace_mutation_allowed') is False, 'workspace mutation invariant')
    require(authority.get('production_promotion_default') is False, 'production promotion default')

    freeze = contract.get('freeze') or {}
    require(freeze.get('contract_change_requires_regression') is True, 'regression freeze missing')
    require(freeze.get('production_promotion_requires_explicit_action') is True, 'explicit promotion invariant missing')
    require(freeze.get('candidate_auto_promotion_forbidden') is True, 'candidate auto promotion must remain forbidden')

    print(json.dumps({
        'ok': True,
        'release': contract['release'],
        'status': contract['status'],
        'capability_phase': contract['capability_phase'],
        'active_worker': runtime['active_worker'],
        'ui_policy': learning['policy'],
        'gate_count': learning['gate_count'],
        'production_promoted': False,
    }, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
