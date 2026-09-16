import assert from 'node:assert/strict';
import { buildLearningAgenda, allocateLearningBudget } from './learning-agenda.js';

const signals = [
  { id: 't1', capability: 'design.typography', kind: 'friction', severity: 1, evidence: ['e:t1'] },
  { id: 't2', capability: 'design.typography', kind: 'friction', severity: 1, evidence: ['e:t2'] },
  { id: 'm1', capability: 'design.motion', kind: 'high-variance', severity: 1, evidence: ['e:m1'] },
  { id: 's1', capability: 'design.style-transfer', kind: 'transfer-failure', severity: 2, evidence: ['e:s1'] },
  { id: 'p1', capability: 'design.taste', kind: 'correction', severity: 2, evidence: ['e:p1', 'e:p2'] },
  { id: 'p2', capability: 'design.taste', kind: 'high-variance', severity: 1, evidence: ['e:p3'] }
];

const agenda = buildLearningAgenda(signals, { maxActive: 2, minScore: 8 });
assert.equal(agenda.kind, 'dore.learning-agenda');
assert.equal(agenda.active.length, 2);
assert.equal(agenda.active[0].capability, 'design.taste');
assert.equal(agenda.active[1].capability, 'design.style-transfer');
assert.ok(agenda.hold.some(x => x.capability === 'design.typography'));
assert.ok(agenda.hold.some(x => x.capability === 'design.motion'));
assert.equal(agenda.authority.maySelfPromote, false);

// Frequency alone must not outrank a rarer high-value correction/transfer failure.
const noisy = buildLearningAgenda([
  ...Array.from({ length: 12 }, (_, i) => ({ id: `noise:${i}`, capability: 'design.spacing', kind: 'friction', severity: 0.2 })),
  { id: 'human:1', capability: 'design.taste', kind: 'correction', severity: 2, evidence: ['human:A-B'] }
], { maxActive: 1, minScore: 5 });
assert.equal(noisy.active[0].capability, 'design.taste');

const allocation = allocateLearningBudget(agenda, { total: 10, minimumPerActive: 2, fullExplorationScore: 20 });
assert.equal(allocation.allocations.length, 2);
assert.equal(allocation.allocations.reduce((sum, x) => sum + x.units, 0), 10);
assert.ok(allocation.allocations.every(x => x.units >= 2));
assert.equal(allocation.authority.maySelfPromote, false);

const empty = allocateLearningBudget(buildLearningAgenda([], {}), { total: 7 });
assert.deepEqual(empty.allocations, []);
assert.equal(empty.unused, 7);

console.log('DORE_LEARNING_AGENDA_BUDGET=PASS');
