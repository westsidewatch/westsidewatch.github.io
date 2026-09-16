import assert from 'node:assert/strict';
import { createMetamorphicProbe, evaluateMetamorphicProbe, evaluateMetamorphicSuite } from './design-metamorphic.js';

const density = createMetamorphicProbe({
  id: 'living-water:density:+30',
  relation: 'content-density',
  source: { consumer: 'living-water', density: 1 },
  transformed: { consumer: 'living-water', density: 1.3 },
  evidence: ['render:living-water:base', 'render:living-water:density-130']
});
const densityPass = evaluateMetamorphicProbe(density, {
  'hierarchy-preserved': true,
  'beautiful-gate-pass': true,
  'no-generic-card-collapse': true
});
assert.equal(densityPass.pass, true);

// Merely squeezing more content into the same card geometry is not capability preservation.
const densityCollapse = evaluateMetamorphicProbe(density, {
  'hierarchy-preserved': true,
  'beautiful-gate-pass': true,
  'no-generic-card-collapse': false
});
assert.equal(densityCollapse.pass, false);
assert.deepEqual(densityCollapse.failed, ['no-generic-card-collapse']);

const aspect = createMetamorphicProbe({
  id: 'living-water:image:portrait-to-landscape',
  relation: 'image-aspect-ratio',
  source: { ratio: '3:4' },
  transformed: { ratio: '16:9' },
  evidence: ['render:image:3x4', 'render:image:16x9']
});
const aspectPass = evaluateMetamorphicProbe(aspect, {
  'composition-recomputed': true,
  'subject-weight-preserved': true,
  'beautiful-gate-pass': true
});
assert.equal(aspectPass.pass, true);

const transfer = createMetamorphicProbe({
  id: 'living-water-to-yangzoumi',
  relation: 'consumer-transfer',
  source: { consumer: 'living-water' },
  transformed: { consumer: 'yangzoumi' },
  evidence: ['render:living-water', 'render:yangzoumi', 'identity-check:yangzoumi']
});
const transferPass = evaluateMetamorphicProbe(transfer, {
  'capability-reused': true,
  'consumer-identity-preserved': true,
  'no-style-leakage': true
});
assert.equal(transferPass.pass, true);

// A beautiful Yangzoumi page that looks like Living Water is still a failed transfer.
const styleLeak = evaluateMetamorphicProbe(transfer, {
  'capability-reused': true,
  'consumer-identity-preserved': false,
  'no-style-leakage': false
});
assert.equal(styleLeak.pass, false);
assert.deepEqual(styleLeak.failed, ['consumer-identity-preserved', 'no-style-leakage']);

const suite = evaluateMetamorphicSuite([densityPass, aspectPass, transferPass]);
assert.equal(suite.pass, true);
assert.deepEqual(suite.relationsCovered, ['consumer-transfer', 'content-density', 'image-aspect-ratio']);

console.log('DORE_DESIGN_METAMORPHIC=PASS');
