export function createSandboxRun(candidate, experiment = {}) {
  if (!candidate || candidate.requiredNextStage !== 'exploration-sandbox') {
    throw new Error('candidate is not admitted to exploration-sandbox');
  }
  if (candidate.authority?.canonical !== false || candidate.authority?.mayWriteRegistry !== false) {
    throw new Error('sandbox requires non-canonical candidate authority');
  }

  return Object.freeze({
    id: experiment.id || `sandbox:${candidate.id}`,
    candidateId: candidate.id,
    hypothesis: experiment.hypothesis || '',
    prototypeRef: experiment.prototypeRef || null,
    taskSamples: [...(experiment.taskSamples || [])],
    researchEvidence: [...(experiment.researchEvidence || [])],
    baseline: experiment.baseline || null,
    result: null,
    state: 'ready',
    isolation: {
      registryWritable: false,
      canonicalRuntimeWritable: false,
      humanAuthorityWritable: false
    }
  });
}

export function recordSandboxResult(run, result = {}) {
  if (!run || run.state !== 'ready') throw new Error('sandbox run is not ready');
  const samples = (result.samples || []).map(sample => ({
    id: sample.id,
    passed: sample.passed === true,
    evidence: [...(sample.evidence || [])]
  }));
  const passed = samples.length > 0 && samples.every(sample => sample.passed);
  return Object.freeze({
    ...run,
    state: 'evaluated-in-sandbox',
    result: {
      passed,
      samples,
      regressions: [...(result.regressions || [])],
      transferEvidence: [...(result.transferEvidence || [])]
    },
    nextStage: 'independent-evaluation',
    authority: {
      canonical: false,
      mayPromoteCanonical: false,
      mayWriteRegistry: false
    }
  });
}
