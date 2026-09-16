import assert from 'node:assert/strict';
import { createTasteEpisode, admitPairwisePreference, validatePreferenceTransfer, preferenceTransferToExperience } from './design-taste-episode.js';
import { consolidateTasteExperiences, admitTastePatternCandidate } from './design-taste-consolidation.js';
import { buildLearningAgenda, allocateLearningBudget } from './learning-agenda.js';
import { evaluateDesignConservation, DESIGN_CONSERVATION_CANARIES } from './design-conservation.js';
import { runDesignMutationSuite, antiForgettingGate } from './capability-mutation.js';
import { createMetamorphicProbe, evaluateMetamorphicProbe, evaluateMetamorphicSuite } from './design-metamorphic.js';

function learnedExperience(id, targetContext) {
  const episode = createTasteEpisode({
    id: `episode:${id}`,
    consumer: 'living-water',
    context: 'quiet-sacred-home',
    candidates: [{ id: `${id}:A` }, { id: `${id}:B` }]
  });
  const delta = admitPairwisePreference(episode, {
    preferred: `${id}:B`, rejected: `${id}:A`,
    change: 'spatial-weight',
    conditions: ['image-remains-dominant', 'text-density-is-subordinate'],
    evidence: [
      { id: `render:${id}:A`, kind: 'real-render', candidate: `${id}:A` },
      { id: `render:${id}:B`, kind: 'real-render', candidate: `${id}:B` },
      { id: `compare:${id}`, kind: 'pairwise-comparison' }
    ]
  });
  const transfer = validatePreferenceTransfer(delta, {
    sourceContext: 'quiet-sacred-home', targetContext,
    result: 'confirmed', styleLeakage: false,
    evidence: [`render:${targetContext}`, `identity:${targetContext}`]
  });
  return preferenceTransferToExperience(transfer, `observation:${id}`);
}

// 1. Two independently transferred preference experiences become one pattern, not two skills.
const experiences = [learnedExperience('one', 'editorial-archive'), learnedExperience('two', 'playful-game-world')];
const consolidation = consolidateTasteExperiences(experiences, [{ id: 'design.taste', state: 'skill' }]);
assert.equal(consolidation.action, 'improve');
assert.equal(consolidation.pattern.state, 'pattern');
assert.deepEqual(consolidation.targets, ['design.taste']);

// 2. Learning pressure chooses the capability intentionally; budget is finite.
const agenda = buildLearningAgenda([
  { id: 'human:spatial', capability: 'design.taste', kind: 'correction', severity: 2, evidence: ['compare:one'] },
  { id: 'variance:spatial', capability: 'design.taste', kind: 'high-variance', severity: 1, evidence: ['compare:two'] },
  { id: 'noise:spacing', capability: 'design.spacing', kind: 'friction', severity: 0.5 }
], { maxActive: 1, minScore: 8 });
assert.equal(agenda.active[0].capability, 'design.taste');
const budget = allocateLearningBudget(agenda, { total: 6, minimumPerActive: 2 });
assert.equal(budget.allocations[0].capability, 'design.taste');
assert.equal(budget.allocations[0].units, 6);

// 3. Conservation is beauty-first and requires identity-safe transfer.
const canaries = Object.fromEntries(DESIGN_CONSERVATION_CANARIES.map(id => [id, true]));
const conservation = evaluateDesignConservation({
  canaries,
  beauty: { realRender: true, beautifulGate: true },
  consumerIdentity: { preserved: true },
  transfer: { materiallyDifferentConsumer: true, capabilityReused: true, styleLeakage: false },
  antiForgetting: { previousCanariesPassed: true, regressions: [] }
});
assert.equal(conservation.pass, true);

// 4. A pattern may propose an improvement candidate only after conservation evidence.
const candidate = admitTastePatternCandidate(consolidation, {
  sandboxEvidence: ['sandbox:spatial-weight:v1'], conservation
});
assert.equal(candidate.disposition, 'improve');
assert.equal(candidate.authority.maySelfPromote, false);
assert.equal(candidate.requiredNextStage, 'existing-skill-growth-promotion-gate');

// 5. Mutation testing proves every protected Design canary is actually observed.
const mutation = runDesignMutationSuite({
  canaries,
  beauty: { realRender: true, beautifulGate: true },
  consumerIdentity: { preserved: true },
  transfer: { materiallyDifferentConsumer: true, capabilityReused: true, styleLeakage: false },
  antiForgetting: { previousCanariesPassed: true, regressions: [] }
});
assert.equal(mutation.pass, true);
assert.deepEqual(mutation.escaped, []);

// 6. Metamorphic transfer preserves capability while consumer identity changes.
const transferProbe = createMetamorphicProbe({
  id: 'living-water-to-yangzoumi:evolution-acceptance',
  relation: 'consumer-transfer',
  source: { consumer: 'living-water', identity: 'quiet-sacred' },
  transformed: { consumer: 'yangzoumi', identity: 'playful-game' },
  evidence: ['render:living-water:evolution', 'render:yangzoumi:evolution', 'identity:yangzoumi:evolution']
});
const transferResult = evaluateMetamorphicProbe(transferProbe, {
  'capability-reused': true,
  'consumer-identity-preserved': true,
  'no-style-leakage': true
});
assert.equal(evaluateMetamorphicSuite([transferResult]).pass, true);

// 7. New learning cannot promote if an old protected capability regresses.
const antiForget = antiForgettingGate({
  previousProtected: DESIGN_CONSERVATION_CANARIES,
  currentResults: canaries,
  newCapabilityPassed: true,
  transferPassed: transferResult.pass
});
assert.equal(antiForget.pass, true);
assert.equal(antiForget.disposition, 'admit-to-next-gate');

const brokenOldCapability = antiForgettingGate({
  previousProtected: DESIGN_CONSERVATION_CANARIES,
  currentResults: { ...canaries, 'design.visual-evidence': false },
  newCapabilityPassed: true,
  transferPassed: true
});
assert.equal(brokenOldCapability.pass, false);
assert.equal(brokenOldCapability.disposition, 'block-promotion');

console.log('DORE_DESIGN_CAPABILITY_EVOLUTION_E2E=PASS');
