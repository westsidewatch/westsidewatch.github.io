import assert from 'node:assert/strict';
import {
  createExperience,
  consolidateExperiences,
  assertLifecycleTransition,
  evaluateConservation,
  learningPressure
} from './capability-lifecycle.js';

const correction = id => ({
  id,
  kind: 'correction',
  signal: 'human correction improves visual hierarchy without importing consumer style',
  recurrenceKey: 'design:human-correction:hierarchy',
  relatedCapabilities: ['design.taste'],
  evidence: [`evidence:${id}`]
});

const e1 = createExperience(correction('a'));
const e2 = createExperience(correction('b'));
assert.equal(e1.state, 'experience');
assert.equal(e1.authority.maySelfPromote, false);

// A single successful correction is experience, not automatically a Skill.
assert.equal(consolidateExperiences([e1], []).action, 'hold');
assert.equal(consolidateExperiences([e1, e2], []).action, 'create');

// Prefer improving the existing capability over creating a duplicate.
const improve = consolidateExperiences([e1, e2], [{ id: 'design.taste', kind: 'skill' }]);
assert.equal(improve.action, 'improve');
assert.deepEqual(improve.targets, ['design.taste']);

// Canonical maturity and compilation cannot bypass existing authority/conservation gates.
assert.throws(() => assertLifecycleTransition('candidate', 'skill'), /promotion gate/);
assert.equal(assertLifecycleTransition('candidate', 'skill', { promotionGate: 'skill-growth:v0' }), true);
assert.throws(() => assertLifecycleTransition('policy', 'compiled'), /conservation/);
assert.equal(assertLifecycleTransition('policy', 'compiled', { capabilityConservation: 'design:canaries:pass' }), true);
assert.throws(() => assertLifecycleTransition('compiled', 'retired'), /retirement requires/);
assert.equal(assertLifecycleTransition('compiled', 'retired', { supersededBy: 'design.taste:v2' }), true);

// Concentration is rejected when any protected specialist capability silently disappears.
const protectedDesign = ['design.visual-evidence', 'design.taste', 'design.beautiful-gate', 'design.transfer'];
const failed = evaluateConservation({
  protectedCapabilities: protectedDesign,
  results: {
    'design.visual-evidence': true,
    'design.taste': false,
    'design.beautiful-gate': true,
    'design.transfer': true
  },
  transfer: true,
  antiForgetting: true
});
assert.equal(failed.pass, false);
assert.deepEqual(failed.missing, ['design.taste']);

const passed = evaluateConservation({
  protectedCapabilities: protectedDesign,
  results: Object.fromEntries(protectedDesign.map(id => [id, true])),
  transfer: true,
  antiForgetting: true
});
assert.equal(passed.pass, true);
assert.equal(passed.authority.maySelfPromote, false);

// Evolution stays sparse: ordinary noise does not open an episode, high-value signals do.
assert.equal(learningPressure([{ kind: 'friction', severity: 1 }]).openEvolutionEpisode, false);
assert.equal(learningPressure([{ kind: 'correction', severity: 1 }, { kind: 'transfer-failure', severity: 1 }]).openEvolutionEpisode, true);

console.log('DORE_CAPABILITY_LIFECYCLE_RECONCILIATION=PASS');
