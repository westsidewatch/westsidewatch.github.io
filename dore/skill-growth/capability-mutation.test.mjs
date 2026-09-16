import assert from 'node:assert/strict';
import { DESIGN_CONSERVATION_CANARIES } from './design-conservation.js';
import { runDesignCapabilityMutationProbe, runDesignMutationSuite, antiForgettingGate } from './capability-mutation.js';

const baseline = {
  canaries: Object.fromEntries(DESIGN_CONSERVATION_CANARIES.map(id => [id, true])),
  beauty: { realRender: true, beautifulGate: true },
  consumerIdentity: { preserved: true },
  transfer: { materiallyDifferentConsumer: true, capabilityReused: true, styleLeakage: false },
  antiForgetting: { previousCanariesPassed: true, regressions: [] }
};

for (const capability of DESIGN_CONSERVATION_CANARIES) {
  const probe = runDesignCapabilityMutationProbe(baseline, capability);
  assert.equal(probe.detected, true, `${capability} mutation must be detected`);
  assert.equal(probe.conservation.pass, false);
  assert.ok(probe.conservation.missing.includes(capability));
}

const suite = runDesignMutationSuite(baseline);
assert.equal(suite.pass, true);
assert.deepEqual(suite.escaped, []);
assert.equal(suite.requiredAction, 'none');
assert.equal(suite.authority.maySelfPromote, false);

const protectedCapabilities = ['design.visual-evidence', 'design.taste', 'design.beautiful-gate'];
const pass = antiForgettingGate({
  previousProtected: protectedCapabilities,
  currentResults: Object.fromEntries(protectedCapabilities.map(id => [id, true])),
  newCapabilityPassed: true,
  transferPassed: true
});
assert.equal(pass.pass, true);
assert.equal(pass.disposition, 'admit-to-next-gate');

const regression = antiForgettingGate({
  previousProtected: protectedCapabilities,
  currentResults: {
    'design.visual-evidence': true,
    'design.taste': false,
    'design.beautiful-gate': true
  },
  newCapabilityPassed: true,
  transferPassed: true
});
assert.equal(regression.pass, false);
assert.deepEqual(regression.regressions, ['design.taste']);
assert.equal(regression.disposition, 'block-promotion');

const noTransfer = antiForgettingGate({
  previousProtected: protectedCapabilities,
  currentResults: Object.fromEntries(protectedCapabilities.map(id => [id, true])),
  newCapabilityPassed: true,
  transferPassed: false
});
assert.equal(noTransfer.pass, false);
assert.equal(noTransfer.disposition, 'hold');

console.log('DORE_CAPABILITY_MUTATION_ANTI_FORGETTING=PASS');
