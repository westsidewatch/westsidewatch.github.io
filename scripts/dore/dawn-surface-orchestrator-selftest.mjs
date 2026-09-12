#!/usr/bin/env node
import assert from 'node:assert/strict';
import { dawnSurfaceContract, orchestrateDawnSurfaces } from './dawn-surface-orchestrator.mjs';

const baseSelection = {
  id: 'dawn-library-featured',
  candidates: [
    { visualWorkId: 'a', score: .40, type: 'engraving', surfacePresetIds: ['card-8x5'], surfacePresets: [{ id: 'card-8x5', focalRegionId: 'a-focus' }] },
    { visualWorkId: 'b', score: .38, type: 'manuscript-illumination', surfacePresetIds: ['card-8x5'], surfacePresets: [{ id: 'card-8x5', focalRegionId: 'b-focus' }] },
    { visualWorkId: 'c', score: .36, type: 'photograph', surfacePresetIds: ['card-8x5'], surfacePresets: [{ id: 'card-8x5', focalRegionId: null }] },
  ],
};

const legacy = orchestrateDawnSurfaces(baseSelection);
assert.equal(legacy.schema, dawnSurfaceContract.schema);
assert.equal(legacy.surfaces.length, 3);
assert.equal(legacy.surfaces[0].role, 'primary');
assert.equal(legacy.surfaces[0].editorialWeight, 2);
assert.equal(legacy.surfaces[0].motion, 'near-still');
assert.deepEqual(legacy.surfaces[0].visualWorkIds, ['a']);
assert.deepEqual(legacy.surfaces[1].visualWorkIds, ['b', 'c']);
assert.equal('context' in legacy, false);

const pageTwo = orchestrateDawnSurfaces(baseSelection, {
  pageIndex: 2,
  pageCount: 4,
  contentRole: 'scripture-study',
  textDensity: .72,
  previousVisualWorkIds: ['a'],
  previousVisualTypes: ['engraving'],
  preferredPreset: 'card-8x5',
  needsNegativeSpace: true,
});
assert.equal(pageTwo.context.pagePosition, 'interior');
assert.deepEqual(pageTwo.surfaces[0].visualWorkIds, ['b']);
assert.equal(pageTwo.surfaces[0].contextDecision.picks[0].visualWorkId, 'b');
assert.ok(pageTwo.surfaces[0].contextDecision.picks[0].contextAdjustment > 0);

const pageThree = orchestrateDawnSurfaces(baseSelection, {
  pageIndex: 3,
  pageCount: 4,
  contentRole: 'witness-story',
  textDensity: .30,
  previousVisualWorkIds: ['a', 'b'],
  previousVisualTypes: ['engraving', 'manuscript-illumination'],
  preferredPreset: 'card-8x5',
});
assert.deepEqual(pageThree.surfaces[0].visualWorkIds, ['c']);

const ids = legacy.surfaces.flatMap(surface => surface.visualWorkIds);
assert.equal(new Set(ids).size, ids.length);
console.log(JSON.stringify({
  status: 'PASS',
  schema: legacy.schema,
  contextSchema: dawnSurfaceContract.context,
  legacyHero: legacy.surfaces[0].visualWorkIds[0],
  pageTwoHero: pageTwo.surfaces[0].visualWorkIds[0],
  pageThreeHero: pageThree.surfaces[0].visualWorkIds[0],
}));
