#!/usr/bin/env python3
"""Phase 16 worker v11: contain invalid model-authored repair or critic output."""
from __future__ import annotations

import design_intelligence_a2a_worker_v7 as v7
import design_intelligence_a2a_worker_v8 as v8
import design_intelligence_a2a_worker_v10 as v10

legacy = v10.legacy
_original_repair_candidate = v10._repair_candidate
_original_judge = legacy._judge


def _safe_repair_candidate(ollama, payload, candidate, domains, attempt):
    try:
        return _original_repair_candidate(ollama, payload, candidate, domains, attempt)
    except (ValueError, TypeError) as exc:
        return None, {
            'attempt': attempt,
            'status': 'regenerate',
            'domains': list(domains or []),
            'reason': f'{type(exc).__name__}:{exc}',
            'repair_admitted': False,
            'sandbox_rejection_preserved': True,
        }


def _safe_judge(ollama, payload, candidates, presentation):
    """A malformed critic response is model noise, not design evidence.

    Retry the same blind presentation once. The strict pixel-evidence validator
    remains authoritative; nothing malformed is admitted to rejection memory.
    """
    try:
        return _original_judge(ollama, payload, candidates, presentation)
    except ValueError as exc:
        if str(exc) not in {
            'failure_reason_and_pixel_basis_required',
            'loser_failures_required',
            'too_many_loser_failures',
        } and not str(exc).startswith(('unknown_failure_domain:', 'duplicate_failure_domain:', 'failure_domain_requires_non_pixel_evidence:')):
            raise
        return _original_judge(ollama, payload, candidates, presentation)


v7._repair_candidate = _safe_repair_candidate
legacy._judge = _safe_judge
legacy._model = v8._model


def main() -> int:
    return legacy.main()


if __name__ == '__main__':
    raise SystemExit(main())
