#!/usr/bin/env node
import assert from 'node:assert/strict';
import { classifyNourishmentItem, globalDesignNourishmentContract, roundOneManifest } from './global-design-nourishment-contract.mjs';

assert.equal(globalDesignNourishmentContract.schema, 'dore.global-design-nourishment.v1');
assert.equal(roundOneManifest.christianScreen.generalFilmExplorationLocked, true);
assert.equal(roundOneManifest.churchArchitecture.researchLine, '光之教會');

const approved = classifyNourishmentItem({ provenance: 'authority-source', rights: 'reviewed', theologyStatus: 'approved' });
assert.deepEqual(approved, { decision: 'dawn+design', dawn: true, design: true, religiousSemantics: true });

const mixed = classifyNourishmentItem({ provenance: 'authority-source', rights: 'reviewed', theologyStatus: 'mixed' });
assert.equal(mixed.decision, 'design-only');
assert.equal(mixed.dawn, false);
assert.equal(mixed.religiousSemantics, false);

const uncertain = classifyNourishmentItem({ provenance: 'authority-source', rights: 'reviewed', theologyStatus: 'uncertain' });
assert.equal(uncertain.decision, 'theology-review-required');
assert.equal(uncertain.dawn, false);
assert.equal(uncertain.religiousSemantics, false);

const missingRights = classifyNourishmentItem({ provenance: 'authority-source', theologyStatus: 'approved' });
assert.equal(missingRights.decision, 'reject');

const baseline = {
  schema: 'dore.design-capability-baseline.v1',
  dimensions: Object.fromEntries(globalDesignNourishmentContract.evaluation.dimensions.map(key => [key, null])),
  frozenBeforeRoundOne: true,
};
assert.equal(Object.keys(baseline.dimensions).length, 6);
assert.equal(globalDesignNourishmentContract.evaluation.stopIfCorpusGrowsWithoutCapabilityDelta, true);

console.log(JSON.stringify({
  status: 'PASS',
  contract: globalDesignNourishmentContract.schema,
  round: roundOneManifest.schema,
  churchArchitecture: roundOneManifest.churchArchitecture.researchLine,
  christianScreenGeneralFilmLocked: roundOneManifest.christianScreen.generalFilmExplorationLocked,
  boundaryFixtures: ['approved', 'mixed', 'uncertain', 'missing-rights'],
  baselineDimensions: Object.keys(baseline.dimensions),
}, null, 2));
