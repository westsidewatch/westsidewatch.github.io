export function evaluateForPromotion(candidate, sandboxRun, evaluation = {}) {
  const failures = [];

  if (!candidate) failures.push('candidate-required');
  if (!sandboxRun || sandboxRun.candidateId !== candidate?.id) failures.push('matching-sandbox-run-required');
  if (sandboxRun?.state !== 'evaluated-in-sandbox' || sandboxRun?.result?.passed !== true) failures.push('sandbox-pass-required');
  if (sandboxRun?.nextStage !== 'independent-evaluation') failures.push('independent-evaluation-stage-required');
  if (candidate?.authority?.canonical !== false || candidate?.authority?.mayWriteRegistry !== false) failures.push('candidate-authority-boundary');

  const deterministic = evaluation.deterministicTests?.passed === true;
  const quality = evaluation.qualityEvaluation?.passed === true;
  const authority = evaluation.authorityEvaluation?.passed === true;
  const executable = Boolean(evaluation.execution?.entrypoint && evaluation.execution?.binding);
  const provenance = Array.isArray(evaluation.provenance) && evaluation.provenance.length > 0;
  const rollback = Boolean(evaluation.rollback?.version && evaluation.rollback?.strategy);

  if (!deterministic) failures.push('deterministic-tests-required');
  if (!quality) failures.push('independent-quality-evaluation-required');
  if (!authority) failures.push('authority-evaluation-required');
  if (!executable) failures.push('execution-entrypoint-and-binding-required');
  if (!provenance) failures.push('provenance-required');
  if (!rollback) failures.push('rollback-required');

  const passed = failures.length === 0;
  return Object.freeze({
    candidateId: candidate?.id || null,
    passed,
    decision: passed ? 'eligible-for-registry-promotion' : 'rejected',
    failures,
    evidence: {
      deterministicTests: evaluation.deterministicTests || null,
      qualityEvaluation: evaluation.qualityEvaluation || null,
      authorityEvaluation: evaluation.authorityEvaluation || null,
      execution: evaluation.execution || null,
      provenance: evaluation.provenance || [],
      rollback: evaluation.rollback || null
    },
    authority: {
      canonical: false,
      registryWritten: false,
      maySelfPromote: false,
      requiresExternalPromotionAction: passed
    }
  });
}

export function assertPromotionEligible(report) {
  if (!report?.passed || report.decision !== 'eligible-for-registry-promotion') {
    throw new Error(`skill candidate is not promotion eligible: ${(report?.failures || ['missing-report']).join(',')}`);
  }
  return true;
}
