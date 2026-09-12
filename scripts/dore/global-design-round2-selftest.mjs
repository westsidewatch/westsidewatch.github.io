#!/usr/bin/env node
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';

const curriculum = JSON.parse(await readFile('data/dore_global_design_round2_curriculum.json', 'utf8'));
const summary = JSON.parse(await readFile('data/dore_global_design_round2_run_summary.json', 'utf8'));
assert.equal(curriculum.schema, 'dore.global-design-curriculum.v1');
assert.equal(curriculum.round, 2);
assert.equal(curriculum.principle, 'more-capability-less-burden');
assert.equal(curriculum.curriculum.find(x => x.domain === 'christian-screen').generalFilmExplorationLocked, true);
assert.equal(curriculum.curriculum.find(x => x.domain === 'architecture-interior-furniture').researchLine, '光之教會');
assert.equal(curriculum.admission.theologyFailClosed, true);
assert.equal(curriculum.admission.religiousMaterialOutsideBoundary, 'design-only-semantic-isolation');
assert.equal(curriculum.selection.preferDiversityOverVolume, true);
assert.equal(curriculum.selection.stopResourceClassWhenCapabilityDeltaIsZero, true);
assert.equal(curriculum.exitGate.requiresCapabilityDelta, true);
assert.equal(curriculum.exitGate.requiresCrossDomainTransferDelta, true);
assert.equal(curriculum.exitGate.requiresEfficiencyNonRegression, true);

const capabilities = new Set(curriculum.priorityCapabilities);
for (const required of ['typography', 'negative-space', 'spatial-thinking', 'responsive-translation', 'cross-domain-transfer']) assert.ok(capabilities.has(required));
const transferTargets = new Set(curriculum.curriculum.flatMap(x => x.targetTransfer || []));
for (const required of ['journal', 'dore-folio', 'church', 'one', 'homepage', 'visual-fuzzy-search', 'shared-surface-engine', 'storybook']) assert.ok(transferTargets.has(required));

assert.equal(summary.schema, 'dore.global-design-nourishment-run-summary.v1');
assert.equal(summary.round, 2);
assert.ok(summary.run.candidateCount >= 100000);
assert.equal(summary.run.parseErrors, 0);
assert.ok(summary.run.retainedCount > 0);
assert.ok(summary.run.retentionRate <= 0.05);
assert.ok(summary.run.theologyReviewRequired > 0);
assert.equal(summary.interpretation.exploreMoreRetainLess, true);
assert.equal(summary.interpretation.theologyFailClosed, true);

console.log(JSON.stringify({
  status: 'PASS',
  round: curriculum.round,
  candidateCount: summary.run.candidateCount,
  retainedCount: summary.run.retainedCount,
  retentionRate: summary.run.retentionRate,
  theologyReviewRequired: summary.run.theologyReviewRequired,
  selectedDomainCounts: summary.selectedDomainCounts,
  capabilityPriorities: curriculum.priorityCapabilities.length,
  transferTargets: [...transferTargets],
  nextGate: 'capability-delta-on-judgment-action-transfer'
}, null, 2));
