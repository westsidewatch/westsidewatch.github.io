#!/usr/bin/env node
import assert from 'node:assert/strict';
import { runStorybookArtDirectionLoop, storybookArtDirectionContract } from './storybook-art-direction-loop.mjs';

const candidates = [
  { visualWorkId: 'cover-a', score: .92, type: 'engraving', surfacePresetIds: ['card-8x5'], surfacePresets: [{ id: 'card-8x5', focalRegionId: 'face' }] },
  { visualWorkId: 'study-b', score: .86, type: 'manuscript-illumination', surfacePresetIds: ['card-8x5'], surfacePresets: [{ id: 'card-8x5', focalRegionId: 'initial' }] },
  { visualWorkId: 'witness-c', score: .82, type: 'photograph', surfacePresetIds: ['card-8x5'], surfacePresets: [{ id: 'card-8x5', focalRegionId: 'subject' }] },
];

const result = runStorybookArtDirectionLoop({
  candidates,
  pages: [
    { contentRole: 'opening', textDensity: 'low' },
    { contentRole: 'scripture-study', textDensity: 'high', needsNegativeSpace: true },
    { contentRole: 'witness', textDensity: 'medium' },
  ],
});

assert.equal(result.schema, storybookArtDirectionContract.schema);
assert.equal(result.decisions.length, 3);
assert.equal(result.decisions[0].selectedVisualWorkId, 'cover-a');
assert.equal(result.decisions[1].selectedVisualWorkId, 'study-b');
assert.equal(result.decisions[2].selectedVisualWorkId, 'witness-c');
assert.equal(new Set(result.decisions.map(item => item.selectedVisualWorkId)).size, 3);
assert.equal(result.critique.pass, true);
assert.equal(result.critique.findings.some(item => item.code === 'visual-repeat'), false);
console.log(JSON.stringify({ status: 'PASS', schema: result.schema, pages: result.decisions.length, critique: result.critique.pass }));
