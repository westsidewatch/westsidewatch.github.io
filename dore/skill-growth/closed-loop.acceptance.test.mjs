import assert from 'node:assert/strict';
import { clusterObservations } from './pattern-detector.js';
import { generateSkillCandidate } from './candidate-generator.js';
import { createSandboxRun, recordSandboxResult } from './sandbox-evolution.js';
import { evaluateForPromotion, assertPromotionEligible } from './promotion-gate.js';

// Real correction class: a single-source isolation operation must never delete sibling sources.
const observations = [
  {
    id: 'obs:source-isolation:1', kind: 'correction',
    source: { surface: 'multiwrite', eventRef: 'incident:single-source-delete' },
    signal: 'single source isolation must preserve sibling sources',
    scope: 'cross-capability', relatedCapabilities: ['source.isolation'],
    recurrenceKey: 'source-isolation-preserve-siblings', evidence: ['incident:resource-set-loss'],
    authority: { mayPromoteCanonical: false, mayRewriteHumanAuthority: false }, status: 'observed'
  },
  {
    id: 'obs:source-isolation:2', kind: 'transfer-signal',
    source: { surface: 'dawn', eventRef: 'acceptance:canonical-admission' },
    signal: 'single source isolation must preserve sibling sources',
    scope: 'cross-capability', relatedCapabilities: ['source.isolation'],
    recurrenceKey: 'source-isolation-preserve-siblings', evidence: ['consumer:dawn'],
    authority: { mayPromoteCanonical: false, mayRewriteHumanAuthority: false }, status: 'observed'
  }
];

const pattern = clusterObservations(observations)[0];
assert.equal(pattern.disposition, 'transfer-candidate');

const registry = [
  { id: 'source.isolation', kind: 'skill', family: 'source' },
  { id: 'source.admission', kind: 'skill', family: 'source' }
];
const candidate = generateSkillCandidate(pattern, registry);
assert.equal(candidate.mode, 'improve-skill-family');
assert.equal(candidate.authority.mayWriteRegistry, false);

const run = createSandboxRun(candidate, {
  id: 'sandbox:source-isolation-preserve-siblings:v1',
  hypothesis: 'isolating one denied source preserves all unrelated admitted sources',
  prototypeRef: 'prototype:source-isolation:v1',
  taskSamples: ['multiwrite-resource-set', 'dawn-canonical-admission'],
  researchEvidence: candidate.evidence
});
const sandbox = recordSandboxResult(run, {
  samples: [
    { id: 'multiwrite-resource-set', passed: true, evidence: ['siblings-preserved'] },
    { id: 'dawn-canonical-admission', passed: true, evidence: ['denied-source-only-blocked'] }
  ],
  regressions: [],
  transferEvidence: ['source-family:multi-consumer']
});
assert.equal(sandbox.result.passed, true);

const promotion = evaluateForPromotion(candidate, sandbox, {
  deterministicTests: { passed: true, ref: 'closed-loop:deterministic' },
  qualityEvaluation: { passed: true, ref: 'closed-loop:independent-quality' },
  authorityEvaluation: { passed: true, ref: 'closed-loop:authority' },
  execution: { entrypoint: 'source.isolation.execute', binding: 'capability:source.isolation' },
  provenance: [...candidate.evidence, run.id],
  rollback: { version: 'skill-growth-v0', strategy: 'registry-version-revert' }
});
assert.equal(assertPromotionEligible(promotion), true);
assert.equal(promotion.authority.registryWritten, false);
assert.equal(promotion.authority.maySelfPromote, false);

// Reuse proof: the learned rule can be consumed as an explicit guard by the next work item.
const learnedRule = Object.freeze({
  id: 'rule:source-isolation-preserve-siblings',
  candidateId: candidate.id,
  promotionEvidence: promotion.evidence,
  enforce(change) {
    return change.targetSource && change.removedSources?.every(id => id === change.targetSource);
  }
});
assert.equal(learnedRule.enforce({ targetSource: 'wikisource', removedSources: ['wikisource'] }), true);
assert.equal(learnedRule.enforce({ targetSource: 'wikisource', removedSources: ['wikisource', 'other-source'] }), false);

console.log('DORE_SKILL_GROWTH_CLOSED_LOOP=PASS');
