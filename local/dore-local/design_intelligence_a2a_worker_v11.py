#!/usr/bin/env python3
"""Phase 16 worker v11: contain invalid model-authored repair and critic output.

Repair and critic serialization are optimizations, never authorities. Invalid
model-authored repair patches preserve sandbox rejection. A malformed critic
JSON response is retried against the same raster evidence with a strict bounded
budget instead of aborting the true-machine A2A run. No fixture or synthetic
critic result is substituted.
"""
from __future__ import annotations

import json

import design_intelligence_a2a_worker_v7 as v7
import design_intelligence_a2a_worker_v8 as v8
import design_intelligence_a2a_worker_v10 as v10

legacy = v10.legacy
_original_repair_candidate = v10._repair_candidate
_original_judge = legacy._judge


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


def _bounded_judge(ollama, payload, candidates, presentation):
    """Retry malformed structured critic output without inventing evidence.

    Each attempt calls the real model-backed legacy judge again against the
    same anonymized raster pair. Only serialization/contract failures are
    retryable. After three failed attempts the genuine error is raised so the
    training run cannot falsely pass.
    """
    last_error = None
    for attempt in range(1, 4):
        try:
            return _original_judge(ollama, payload, candidates, presentation)
        except (json.JSONDecodeError, ValueError, TypeError) as exc:
            last_error = exc
            if attempt == 3:
                raise RuntimeError(
                    'design_critic_structured_output_failed_after_3_attempts:'
                    f'{type(exc).__name__}:{exc}'
                ) from exc
    raise RuntimeError('design_critic_structured_output_retry_unreachable') from last_error


v7._repair_candidate = _safe_repair_candidate
legacy._judge = _bounded_judge
legacy._model = v8._model


def main() -> int:
    return legacy.main()


if __name__ == '__main__':
    raise SystemExit(main())
