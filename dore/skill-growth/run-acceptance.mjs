const suites = [
  './pattern-detector.test.mjs',
  './candidate-generator.test.mjs',
  './sandbox-evolution.test.mjs',
  './promotion-gate.test.mjs',
  './closed-loop.acceptance.test.mjs'
];

for (const suite of suites) await import(suite);
console.log('DORE_SKILL_GROWTH_V0=PASS');
