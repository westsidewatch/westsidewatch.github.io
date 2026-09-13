#!/usr/bin/env python3
"""Phase 16 worker v10: executable guardrail verification before critique."""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[1]
DESIGN_ROOT = REPO_ROOT / 'dore-design'
if str(DESIGN_ROOT) not in sys.path:
    sys.path.insert(0, str(DESIGN_ROOT))

import design_guardrail_verifier as guardrail_verifier
import design_intelligence_a2a_worker_v6 as v6
import design_intelligence_a2a_worker_v7 as v7
import design_intelligence_a2a_worker_v8 as v8
import design_intelligence_a2a_worker_v9 as v9

legacy = v9.legacy
_original_generate = v6._generate
_original_repair_candidate = v7._repair_candidate


def _apply_executable_guardrail_evidence(payload, variants, candidates):
    guardrails = v6._guardrails(payload)
    for variant, candidate in zip(variants, candidates):
        model_risks = [str(x) for x in (candidate.get('risk_domains') or [])]
        verification = guardrail_verifier.verify_candidate(candidate, guardrails)
        candidate['model_risk_domains'] = model_risks
        candidate['guardrail_verification'] = verification
        candidate['risk_domains'] = list(verification['repeated_failure_domains'])
        variant['model_risk_domains'] = [str(x) for x in (variant.get('risk_domains') or [])]
        variant['risk_domains'] = list(verification['repeated_failure_domains'])
        variant['addressed_failure_domains'] = list(verification['addressed_failure_domains'])
    return variants, candidates


def _generate(ollama, payload, base, nodes, attempt, structured_json=None):
    variants, candidates = _original_generate(
        ollama, payload, base, nodes, attempt, structured_json=structured_json
    )
    return _apply_executable_guardrail_evidence(payload, variants, candidates)


def _repair_candidate(ollama, payload, candidate, domains, attempt):
    repaired, event = _original_repair_candidate(
        ollama, payload, candidate, domains, attempt
    )
    if repaired is None:
        return None, event
    model_risks = [str(x) for x in (repaired.get('risk_domains') or [])]
    verification = guardrail_verifier.verify_candidate(
        repaired, v6._guardrails(payload)
    )
    repaired['model_risk_domains'] = model_risks
    repaired['guardrail_verification'] = verification
    repaired['risk_domains'] = list(verification['repeated_failure_domains'])
    event = {
        **event,
        'guardrail_verification': verification,
        'model_risk_domains': model_risks,
    }
    return repaired, event


v6._generate = _generate
v7._repair_candidate = _repair_candidate
legacy._model = v8._model


def main() -> int:
    return legacy.main()


if __name__ == '__main__':
    raise SystemExit(main())
