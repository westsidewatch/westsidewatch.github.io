export function runShadowReflex(candidate, liveDecision, actualOutcome) {
  if (!candidate?.eligible || candidate?.requiredNextStage !== 'shadow') {
    return Object.freeze({ status: 'NOT_ELIGIBLE', executed: false, agreement: null });
  }

  const reflexDecision = candidate.proposedDecision ?? candidate.decision ?? null;
  const live = liveDecision?.decision ?? liveDecision ?? null;
  const verification = actualOutcome?.verification ?? actualOutcome ?? 'UNKNOWN';

  const agreement = reflexDecision !== null && live !== null
    ? (reflexDecision === live ? 'AGREE' : 'DISAGREE')
    : 'UNRESOLVED';

  const classification = verification === 'UNKNOWN' ? 'unknown'
    : verification === 'PASS'
      ? (agreement === 'AGREE' ? 'agreement-pass' : 'disagreement-pass')
      : (agreement === 'AGREE' ? 'agreement-fail' : 'disagreement-fail');

  return Object.freeze({
    candidateId: candidate.id,
    status: 'SHADOW',
    executed: false,
    reflexDecision,
    liveDecision: live,
    agreement,
    verification,
    classification,
    authority: Object.freeze({
      mayExecute: false,
      mayMutateLiveDecision: false,
      mayClaimPassFromAgreement: false,
      requiresIndependentVerification: true
    })
  });
}

export function summarizeShadowRuns(runs = []) {
  const shadow = runs.filter(x => x?.status === 'SHADOW');
  const counts = shadow.reduce((acc, run) => {
    acc[run.classification] = (acc[run.classification] || 0) + 1;
    return acc;
  }, {});
  return Object.freeze({
    total: shadow.length,
    counts: Object.freeze(counts),
    promotableEvidence: shadow.filter(x => x.verification === 'PASS').length,
    unknownIsPass: false
  });
}
