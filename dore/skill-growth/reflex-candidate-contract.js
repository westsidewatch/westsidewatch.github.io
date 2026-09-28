const REFLEX_CLASSES = Object.freeze(['R0-deterministic','R1-bounded-choice','R2-specialist','R3-deliberative']);

export function assessReflexCandidate(input = {}) {
  const evidence = [...new Set(input.evidence || [])];
  const reasons = [];
  if (!input.bounded) reasons.push('unbounded-state-or-action-space');
  if ((input.verifiedSuccesses || 0) < (input.minimumRepeatedSuccesses ?? 2)) reasons.push('insufficient-repeated-success');
  if (!input.independentlyVerifiable) reasons.push('no-independent-verifier');
  if (!input.recoverable) reasons.push('not-recoverable');
  if (!input.authoritySafe) reasons.push('authority-boundary-not-proven');

  const eligible = reasons.length === 0;
  const reflexClass = !eligible ? 'R3-deliberative'
    : input.deterministic ? 'R0-deterministic'
    : input.boundedChoice ? 'R1-bounded-choice'
    : input.specialist ? 'R2-specialist'
    : 'R3-deliberative';

  return Object.freeze({
    id: input.id || null,
    eligible,
    reflexClass,
    reasons,
    evidence,
    requiredNextStage: eligible && reflexClass !== 'R3-deliberative' ? 'shadow' : 'deliberative-intelligence',
    authority: Object.freeze({
      canonical: false,
      mayExecute: false,
      maySelfPromote: false,
      mayWriteRegistry: false,
      mayRewriteHumanAuthority: false
    })
  });
}

export { REFLEX_CLASSES };
