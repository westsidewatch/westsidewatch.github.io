#!/usr/bin/env python3
"""Phase 16 worker v9: invalid repair proposals safely fall back to regeneration.

A local model may decline or emit an empty/out-of-domain repair patch. That is
not grounds to admit the candidate and should not crash the A2A loop. Preserve
the repair safety gate, record the rejection, and use the already bounded full
regeneration fallback.
"""
from __future__ import annotations

import design_intelligence_a2a_worker_v7 as v7
import design_intelligence_a2a_worker_v8 as v8

legacy = v8.legacy
_original_repair_candidate = v7._repair_candidate


def _safe_repair_candidate(ollama, payload, candidate, domains, attempt):
    try:
        return _original_repair_candidate(ollama, payload, candidate, domains, attempt)
    except ValueError as exc:
        message = str(exc)
        if not message.startswith('repair_patch_invalid:'):
            raise
        return None, {
            'attempt': attempt,
            'status': 'regenerate',
            'domains': list(domains or []),
            'reason': message,
            'repair_admitted': False,
        }


v7._repair_candidate = _safe_repair_candidate
legacy._model = v8._model


def main() -> int:
    return legacy.main()


if __name__ == '__main__':
    raise SystemExit(main())
