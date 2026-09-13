#!/usr/bin/env python3
"""Phase 16 worker: separate visual winner consensus from learning consensus.

A real-model A/B decision may agree on the winner while the two blind judges
still disagree about the pixel-grounded failure domain. That is valid visual
evidence, but it is not sufficient to write rejection memory. Treat that case
as unresolved for learning and request another bounded exploration instead of
failing the A2A execution or fabricating a failure reason.
"""
from __future__ import annotations

import design_intelligence_a2a_worker_v7 as v7

legacy = v7.legacy
_base_model = v7._model


def _model(payload: dict) -> dict:
    result = _base_model(payload)
    critic = result.get('critic') or {}
    if critic.get('consensus') and not (critic.get('loser_failures') or []):
        critic['visual_winner_consensus'] = True
        critic['visual_winner'] = critic.get('winner')
        critic['learning_consensus'] = False
        critic['learning_consensus_block_reason'] = 'failure-domain-disagreement'
        critic['consensus'] = False
        critic['winner'] = None
        critic['memory_admission'] = False
        critic['winner_reason'] = ''
        critic['loser_reason'] = ''
        critic['failure_domains'] = []
    elif critic.get('consensus'):
        critic['visual_winner_consensus'] = True
        critic['visual_winner'] = critic.get('winner')
        critic['learning_consensus'] = True
    else:
        critic['visual_winner_consensus'] = False
        critic['learning_consensus'] = False
    return result


legacy._model = _model


def main() -> int:
    return legacy.main()


if __name__ == '__main__':
    raise SystemExit(main())
