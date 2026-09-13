#!/usr/bin/env python3
"""Phase 16 worker v11: contain any invalid model-authored repair patch.

Repair is an optimization, never an authority. If the local model returns a
malformed numeric value, unknown node, or other invalid executable repair, the
sandbox rejection is preserved and the loop falls back to bounded regeneration
instead of aborting the true-machine A2A run.
"""
from __future__ import annotations

import design_intelligence_a2a_worker_v7 as v7
import design_intelligence_a2a_worker_v8 as v8
import design_intelligence_a2a_worker_v10 as v10

legacy = v10.legacy
_original_repair_candidate = v10._repair_candidate


def _safe_repair_candidate(ollama, payload, candidate, domains, attempt):
    try:
        return _original_repair_candidate(
            ollama, payload, candidate, domains, attempt
        )
    except (ValueError, TypeError) as exc:
        return None, {
            'attempt': attempt,
            'status': 'regenerate',
            'domains': list(domains or []),
            'reason': f'{type(exc).__name__}:{exc}',
            'repair_admitted': False,
            'sandbox_rejection_preserved': True,
        }


v7._repair_candidate = _safe_repair_candidate
legacy._model = v8._model


def main() -> int:
    return legacy.main()


if __name__ == '__main__':
    raise SystemExit(main())
