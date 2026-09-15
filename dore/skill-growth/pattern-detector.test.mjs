import assert from 'node:assert/strict';
import { clusterObservations } from './pattern-detector.js';

const obs = (id, overrides = {}) => ({
  id,
  kind: 'friction',
  source: { surface: 'multiwrite', eventRef: `event:${id}` },
  signal: 'repeated manual correction',
  scope: 'local',
  relatedCapabilities: ['publishing'],
  recurrenceKey: 'manual-correction',
  authority: { mayPromoteCanonical: false, mayRewriteHumanAuthority: false },
  status: 'observed',
  ...overrides
});

assert.equal(clusterObservations([obs('1')])[0].disposition, 'local-defect');
assert.equal(clusterObservations([obs('1'), obs('2')])[0].disposition, 'watch-pattern');
assert.equal(clusterObservations([obs('1'), obs('2'), obs('3')])[0].disposition, 'skill-candidate');

const transfer = clusterObservations([
  obs('1'),
  obs('2', { source: { surface: 'journal', eventRef: 'event:2' } })
])[0];
assert.equal(transfer.disposition, 'transfer-candidate');

const principle = clusterObservations([
  obs('p1', { kind: 'correction', scope: 'core-principle', recurrenceKey: 'human-authority' })
])[0];
assert.equal(principle.disposition, 'principle-candidate');
assert.equal(principle.authority.mayPromoteCanonical, false);

const gap = clusterObservations([
  obs('g1', { kind: 'capability-gap', recurrenceKey: 'missing-capability' })
])[0];
assert.equal(gap.disposition, 'skill-candidate');

console.log('DORE_SKILL_GROWTH_PATTERN_DETECTOR=PASS');
