import assert from 'node:assert/strict';
import { createSandboxRun, recordSandboxResult } from './sandbox-evolution.js';

const candidate = {
  id: 'candidate:human-authority',
  requiredNextStage: 'exploration-sandbox',
  authority: {
    canonical: false,
    mayWriteRegistry: false,
    mayRewriteHumanAuthority: false,
    requiresIndependentEvaluation: true
  }
};

const run = createSandboxRun(candidate, {
  id: 'sandbox:human-authority:v1',
  hypothesis: 'preserve author thesis across publishing consumers',
  prototypeRef: 'prototype:human-authority:v1',
  taskSamples: ['book', 'journal'],
  researchEvidence: ['observation:o1', 'observation:o2']
});

assert.equal(run.isolation.registryWritable, false);
assert.equal(run.isolation.canonicalRuntimeWritable, false);
assert.equal(run.isolation.humanAuthorityWritable, false);

const evaluated = recordSandboxResult(run, {
  samples: [
    { id: 'book', passed: true, evidence: ['book:test:pass'] },
    { id: 'journal', passed: true, evidence: ['journal:test:pass'] }
  ],
  transferEvidence: ['publishing-family:2-consumers']
});

assert.equal(evaluated.result.passed, true);
assert.equal(evaluated.nextStage, 'independent-evaluation');
assert.equal(evaluated.authority.mayPromoteCanonical, false);

const failed = recordSandboxResult(createSandboxRun(candidate), {
  samples: [{ id: 'book', passed: false, evidence: ['regression'] }],
  regressions: ['author-thesis-overwrite']
});
assert.equal(failed.result.passed, false);
assert.deepEqual(failed.result.regressions, ['author-thesis-overwrite']);

assert.throws(() => createSandboxRun({ ...candidate, authority: { canonical: true, mayWriteRegistry: false } }));

console.log('DORE_SKILL_GROWTH_SANDBOX_EVOLUTION=PASS');
