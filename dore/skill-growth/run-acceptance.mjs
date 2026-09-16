const suites = [
  './pattern-detector.test.mjs',
  './candidate-generator.test.mjs',
  './sandbox-evolution.test.mjs',
  './promotion-gate.test.mjs',
  './closed-loop.acceptance.test.mjs',
  './capability-lifecycle.test.mjs',
  './design-conservation.test.mjs',
  './design-taste-episode.test.mjs',
  './design-taste-consolidation.test.mjs',
  './learning-agenda.test.mjs',
  './capability-mutation.test.mjs',
  './design-metamorphic.test.mjs'
];

for (const suite of suites) await import(suite);
console.log('DORE_SKILL_GROWTH_V0=PASS');
