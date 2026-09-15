import assert from 'node:assert/strict';
import { generateSkillCandidate } from './candidate-generator.js';

const registry = [
  { id: 'publishing.book', kind: 'skill', family: 'publishing' },
  { id: 'publishing.journal', kind: 'skill', family: 'publishing' },
  { id: 'design.cover', kind: 'skill', family: 'design' }
];

const pattern = (disposition, capabilities = [], key = disposition) => ({
  key, disposition, capabilities, observationIds: ['o1', 'o2']
});

const create = generateSkillCandidate(pattern('skill-candidate', ['unknown.skill']), registry);
assert.equal(create.mode, 'create-new-skill');

const improve = generateSkillCandidate(pattern('skill-candidate', ['publishing.book']), registry);
assert.equal(improve.mode, 'improve-existing-skill');
assert.deepEqual(improve.targets, ['publishing.book']);
assert.deepEqual(improve.siblingSkills, ['publishing.book', 'publishing.journal']);

const transfer = generateSkillCandidate(pattern('transfer-candidate', ['publishing.book']), registry);
assert.equal(transfer.mode, 'improve-skill-family');
assert.deepEqual(transfer.siblingSkills, ['publishing.book', 'publishing.journal']);

const principle = generateSkillCandidate(pattern('principle-candidate', ['publishing.book']), registry);
assert.equal(principle.mode, 'propose-core-principle');
assert.equal(principle.authority.mayWriteRegistry, false);
assert.equal(principle.authority.mayRewriteHumanAuthority, false);
assert.equal(principle.requiredNextStage, 'exploration-sandbox');

assert.equal(generateSkillCandidate(pattern('local-defect'), registry), null);
assert.equal(generateSkillCandidate(pattern('watch-pattern'), registry), null);

console.log('DORE_SKILL_GROWTH_CANDIDATE_GENERATOR=PASS');
