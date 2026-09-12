#!/usr/bin/env node
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { classifyNourishmentItem, globalDesignNourishmentContract, roundOneManifest } from './global-design-nourishment-contract.mjs';

assert.equal(globalDesignNourishmentContract.schema, 'dore.global-design-nourishment.v1');
assert.equal(roundOneManifest.christianScreen.generalFilmExplorationLocked, true);
assert.equal(roundOneManifest.churchArchitecture.researchLine, '光之教會');

const fixtures = [
  [{ provenance: 'authority-source', rights: 'reviewed', theologyStatus: 'approved' }, 'dawn+design'],
  [{ provenance: 'authority-source', rights: 'reviewed', theologyStatus: 'mixed' }, 'design-only'],
  [{ provenance: 'authority-source', rights: 'reviewed', theologyStatus: 'uncertain' }, 'theology-review-required'],
  [{ provenance: 'authority-source', theologyStatus: 'approved' }, 'reject'],
];
for (const [item, expected] of fixtures) assert.equal(classifyNourishmentItem(item).decision, expected);

const batch = JSON.parse(await readFile('data/dore_global_design_round1_batch01.json', 'utf8'));
assert.equal(batch.schema, 'dore.global-design-nourishment-batch.v1');
assert.ok(batch.items.length > 0);

const ids = new Set();
const domains = new Set();
const signals = new Set();
const decisions = {};
let reviewRequired = 0;
let semanticIsolation = 0;
let designAdmitted = 0;

for (const item of batch.items) {
  assert.ok(item.id && !ids.has(item.id)); ids.add(item.id);
  assert.ok(item.source && item.sourceUrl && item.provenance && item.rights);
  assert.ok(item.domain?.length && item.designSignals?.length);
  const result = classifyNourishmentItem(item);
  assert.equal(result.decision, item.expectedDecision);
  decisions[result.decision] = (decisions[result.decision] || 0) + 1;
  if (result.design) designAdmitted += 1;
  if (result.decision === 'theology-review-required') reviewRequired += 1;
  if (item.religiousSemanticIsolation) semanticIsolation += 1;
  item.domain.forEach(x => domains.add(x));
  item.designSignals.forEach(x => signals.add(x));
}

assert.equal(designAdmitted, batch.items.length);
assert.ok(reviewRequired > 0);
assert.ok(semanticIsolation > 0);
assert.equal(globalDesignNourishmentContract.evaluation.stopIfCorpusGrowsWithoutCapabilityDelta, true);

console.log(JSON.stringify({
  status: 'PASS',
  contract: globalDesignNourishmentContract.schema,
  batchId: batch.batchId,
  itemCount: batch.items.length,
  uniqueDomains: domains.size,
  uniqueDesignSignals: signals.size,
  decisions,
  theologyBoundary: { reviewRequired, semanticIsolation },
  learningYield: {
    domainsPerItem: Number((domains.size / batch.items.length).toFixed(3)),
    signalsPerItem: Number((signals.size / batch.items.length).toFixed(3)),
    designAdmissionRate: Number((designAdmitted / batch.items.length).toFixed(3)),
  },
  baselineDimensions: globalDesignNourishmentContract.evaluation.dimensions,
  nextGate: 'capability-delta',
}, null, 2));
