import assert from 'node:assert/strict';
import { createExperience } from './capability-lifecycle.js';
import { consolidateTasteExperiences, admitTastePatternCandidate } from './design-taste-consolidation.js';

const exp = (id, key = 'design:taste:spatial-weight') => createExperience({
  id,
  recurrenceKey: key,
  signal: 'reduce adjacent text density while preserving dominant image weight',
  relatedCapabilities: ['design.taste'],
  evidence: [`render:${id}`, `pairwise:${id}`, `transfer:${id}`]
});

const one = consolidateTasteExperiences([exp('one')]);
assert.equal(one.action, 'hold');
assert.equal(one.pattern, null);

const created = consolidateTasteExperiences([exp('one'), exp('two')]);
assert.equal(created.action, 'create');
assert.equal(created.pattern.state, 'pattern');
assert.equal(created.pattern.authority.maySelfPromote, false);
assert.equal(created.pattern.requiredNextStage, 'sandbox-candidate');

// Existing Design Taste should be improved, not duplicated.
const improved = consolidateTasteExperiences(
  [exp('one'), exp('two')],
  [{ id: 'design.taste', state: 'skill' }]
);
assert.equal(improved.action, 'improve');
assert.deepEqual(improved.targets, ['design.taste']);
assert.equal(improved.pattern.disposition, 'improve');

// Different causal deltas remain separate experiences rather than being over-compressed.
const mixed = consolidateTasteExperiences([exp('one'), exp('two', 'design:taste:motion-emergence')]);
assert.equal(mixed.action, 'hold');
assert.equal(mixed.pattern, null);

const conservationPass = Object.freeze({ pass: true, missing: [], transferPassed: true, antiForgettingPassed: true });
const candidate = admitTastePatternCandidate(improved, {
  sandboxEvidence: ['sandbox:design-taste:spatial-weight'],
  conservation: conservationPass
});
assert.equal(candidate.state, 'candidate');
assert.equal(candidate.disposition, 'improve');
assert.deepEqual(candidate.targetCapabilities, ['design.taste']);
assert.equal(candidate.requiredNextStage, 'existing-skill-growth-promotion-gate');
assert.equal(candidate.authority.maySelfPromote, false);

assert.throws(
  () => admitTastePatternCandidate(improved, { sandboxEvidence: ['sandbox:x'], conservation: { pass: false } }),
  /conservation PASS/
);

console.log('DORE_DESIGN_TASTE_CONSOLIDATION=PASS');
