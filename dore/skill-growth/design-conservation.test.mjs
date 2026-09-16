import assert from 'node:assert/strict';
import { evaluateDesignConservation, preferenceDelta } from './design-conservation.js';

const allCanaries = {
  'design.visual-evidence': true,
  'design.taste': true,
  'design.beautiful-gate': true,
  'design.consumer-identity': true,
  'design.transfer': true
};

const baseline = {
  canaries: allCanaries,
  beauty: { realRender: true, beautifulGate: true },
  consumerIdentity: { preserved: true },
  transfer: { materiallyDifferentConsumer: true, capabilityReused: true, styleLeakage: false },
  antiForgetting: { previousCanariesPassed: true, regressions: [] }
};

const pass = evaluateDesignConservation(baseline);
assert.equal(pass.pass, true);
assert.equal(pass.disposition, 'conserve');
assert.equal(pass.beautyFirst, true);

// Functionally intact but aesthetically weaker is a hard failure.
const beautyLoss = evaluateDesignConservation({ ...baseline, beauty: { realRender: true, beautifulGate: false } });
assert.equal(beautyLoss.pass, false);
assert.equal(beautyLoss.disposition, 'block-concentration');
assert.deepEqual(beautyLoss.missing, ['design.beautiful-gate']);

// A transferable mechanism must not copy Living Water identity into another consumer.
const leaked = evaluateDesignConservation({
  ...baseline,
  transfer: { materiallyDifferentConsumer: true, capabilityReused: true, styleLeakage: true }
});
assert.equal(leaked.pass, false);
assert.equal(leaked.styleLeakage, true);

// A beautiful result that erases the consumer's own identity still fails conservation.
const identityLoss = evaluateDesignConservation({ ...baseline, consumerIdentity: { preserved: false } });
assert.equal(identityLoss.pass, false);
assert.deepEqual(identityLoss.missing, ['design.consumer-identity']);

// Existing capability regressions block a new concentration even if the new sample looks good.
const forgotten = evaluateDesignConservation({
  ...baseline,
  antiForgetting: { previousCanariesPassed: true, regressions: ['design.visual-evidence:Casabella-binding'] }
});
assert.equal(forgotten.pass, false);
assert.equal(forgotten.antiForgettingPassed, false);

// Taste learning stores causal comparison delta, not a scalar beauty score or copied CSS value.
const delta = preferenceDelta({
  before: 'candidate:A',
  after: 'candidate:B',
  change: 'reduce text-area density while preserving image vertical weight',
  conditions: ['hero image has strong vertical weight'],
  evidence: ['pairwise-judge:A-vs-B', 'real-render:B']
});
assert.equal(delta.kind, 'design.preference-delta');
assert.equal(delta.requiredNextStage, 'cross-context-validation');
assert.equal(delta.authority.maySelfPromote, false);
assert.equal('score' in delta, false);

console.log('DORE_DESIGN_CAPABILITY_CONSERVATION=PASS');
