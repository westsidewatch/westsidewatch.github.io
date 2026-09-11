#!/usr/bin/env node
import assert from 'node:assert/strict';
import { dawnSurfaceContract, orchestrateDawnSurfaces } from './dawn-surface-orchestrator.mjs';

const result = orchestrateDawnSurfaces({
  id: 'dawn-library-featured',
  candidates: [
    { visualWorkId: 'a', surfacePresetIds: ['card-8x5'] },
    { visualWorkId: 'b', surfacePresetIds: ['card-8x5'] },
    { visualWorkId: 'c', surfacePresetIds: ['card-8x5'] },
  ],
});
assert.equal(result.schema, dawnSurfaceContract.schema);
assert.equal(result.surfaces.length, 3);
assert.equal(result.surfaces[0].role, 'primary');
assert.equal(result.surfaces[0].editorialWeight, 2);
assert.equal(result.surfaces[0].motion, 'near-still');
assert.deepEqual(result.surfaces[0].visualWorkIds, ['a']);
assert.deepEqual(result.surfaces[1].visualWorkIds, ['b', 'c']);
const ids = result.surfaces.flatMap(surface => surface.visualWorkIds);
assert.equal(new Set(ids).size, ids.length);
console.log(JSON.stringify({ status: 'PASS', schema: result.schema, surfaces: result.surfaces.length }));
