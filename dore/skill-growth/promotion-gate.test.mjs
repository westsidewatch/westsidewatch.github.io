import assert from 'node:assert/strict';
import { evaluateForPromotion, assertPromotionEligible } from './promotion-gate.js';

const candidate = {
  id: 'candidate:human-authority',
  authority: { canonical: false, mayWriteRegistry: false }
};
const sandbox = {
  candidateId: candidate.id,
  state: 'evaluated-in-sandbox',
  result: { passed: true },
  nextStage: 'independent-evaluation'
};
const evidence = {
  deterministicTests: { passed: true, ref: 'tests:skill-growth' },
  qualityEvaluation: { passed: true, ref: 'eval:blind-quality' },
  authorityEvaluation: { passed: true, ref: 'eval:authority-boundary' },
  execution: { entrypoint: 'skill.execute', binding: 'capability:skill-growth' },
  provenance: ['observation:o1', 'pattern:p1', 'sandbox:s1'],
  rollback: { version: 'v0', strategy: 'registry-version-revert' }
};

const pass = evaluateForPromotion(candidate, sandbox, evidence);
assert.equal(pass.passed, true);
assert.equal(pass.decision, 'eligible-for-registry-promotion');
assert.equal(pass.authority.registryWritten, false);
assert.equal(pass.authority.maySelfPromote, false);
assert.equal(assertPromotionEligible(pass), true);

const missingExecution = evaluateForPromotion(candidate, sandbox, { ...evidence, execution: {} });
assert.equal(missingExecution.passed, false);
assert.ok(missingExecution.failures.includes('execution-entrypoint-and-binding-required'));

const failedSandbox = evaluateForPromotion(candidate, { ...sandbox, result: { passed: false } }, evidence);
assert.equal(failedSandbox.passed, false);
assert.ok(failedSandbox.failures.includes('sandbox-pass-required'));

const selfCanonical = evaluateForPromotion({ ...candidate, authority: { canonical: true, mayWriteRegistry: false } }, sandbox, evidence);
assert.equal(selfCanonical.passed, false);
assert.ok(selfCanonical.failures.includes('candidate-authority-boundary'));

assert.throws(() => assertPromotionEligible(missingExecution));
console.log('DORE_SKILL_GROWTH_PROMOTION_GATE=PASS');
