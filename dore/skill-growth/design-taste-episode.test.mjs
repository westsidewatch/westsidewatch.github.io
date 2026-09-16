import assert from 'node:assert/strict';
import { createTasteEpisode, admitPairwisePreference, validatePreferenceTransfer, preferenceTransferToExperience } from './design-taste-episode.js';

const episode = createTasteEpisode({
  id: 'taste:living-water:001',
  consumer: 'living-water',
  context: 'quiet-threshold-homepage',
  candidates: [{ id: 'A', strategy: 'dense editorial field' }, { id: 'B', strategy: 'threshold breathing field' }]
});
assert.equal(episode.stage, 'awaiting-real-render');
assert.equal(episode.authority.maySelfPromote, false);

assert.throws(() => admitPairwisePreference(episode, {
  preferred: 'B', rejected: 'A', change: 'reduce adjacent text density',
  evidence: [{ id: 'render:B', kind: 'real-render', candidate: 'B' }]
}), /real renders for both/);

const delta = admitPairwisePreference(episode, {
  preferred: 'B', rejected: 'A',
  change: 'reduce adjacent text density while preserving image vertical weight',
  conditions: ['hero image carries dominant vertical weight'],
  evidence: [
    { id: 'render:A', kind: 'real-render', candidate: 'A' },
    { id: 'render:B', kind: 'real-render', candidate: 'B' },
    { id: 'compare:A:B', kind: 'pairwise-comparison' }
  ]
});
assert.equal(delta.requiredNextStage, 'cross-context-validation');
assert.equal('score' in delta, false);

const contradicted = validatePreferenceTransfer(delta, {
  sourceContext: 'quiet-threshold-homepage', targetContext: 'dense-editorial-article',
  result: 'contradicted', styleLeakage: false, evidence: ['render:article:test']
});
assert.equal(contradicted.promotionEligible, false);
assert.throws(() => preferenceTransferToExperience(contradicted, 'obs:bad'), /only confirmed/);

assert.throws(() => validatePreferenceTransfer(delta, {
  sourceContext: 'quiet-threshold-homepage', targetContext: 'game-world-entry',
  result: 'confirmed', styleLeakage: true, evidence: ['render:game:test']
}), /no-style-leakage/);

const confirmed = validatePreferenceTransfer(delta, {
  sourceContext: 'quiet-threshold-homepage', targetContext: 'game-world-entry',
  result: 'confirmed', styleLeakage: false,
  evidence: ['render:game:test', 'judge:no-living-water-style-leakage']
});
assert.equal(confirmed.promotionEligible, true);

const experience = preferenceTransferToExperience(confirmed, 'obs:taste-transfer:001');
assert.equal(experience.state, 'experience');
assert.equal(experience.authority.maySelfPromote, false);
assert.deepEqual(experience.relatedCapabilities, ['design.taste']);

console.log('DORE_DESIGN_TASTE_EPISODE=PASS');
