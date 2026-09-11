#!/usr/bin/env node
import assert from 'node:assert/strict';
import { selectEditorialVisualsFromGraph } from './visual-editorial-director-runtime.mjs';

const result = await selectEditorialVisualsFromGraph({
  content: 'Sea of Galilee storm boat',
  w: 'WATCH',
  scriptureRefs: ['Mark 4:35–41'],
  aspectRatio: '8:5',
  operation: 'display',
  limit: 4,
});

assert.equal(result.schema, 'dore.visual-editorial-director.v1');
assert.equal(result.source, 'dawn.visual-graph.v1');
assert.equal(result.graphBound, true);
assert.ok(result.candidateCount > 0);
assert.equal(result.candidates[0].visualWorkId, 'visual-princeton-galilee-storm-1591');
assert.ok(result.candidates[0].representations.length > 0);
assert.ok(result.candidates[0].representations.every(rep => rep.imageUrl));
assert.ok(result.candidates[0].surfacePresets.some(preset => preset.id === 'card-8x5'));
assert.ok(result.candidates.every(candidate => candidate.authorityClass !== 'D'));

const design = await selectEditorialVisualsFromGraph({
  content: 'Moses Leviticus',
  operation: 'design',
  limit: 12,
});
assert.equal(design.candidates.some(candidate => candidate.visualWorkId === 'visual-initiale-lev1-god-speaking-moses'), false);

console.log('Editorial Director runtime PASS', result.candidateCount, 'ranked graph-bound candidates');
