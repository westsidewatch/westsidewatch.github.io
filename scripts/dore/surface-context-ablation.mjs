#!/usr/bin/env node
import assert from 'node:assert/strict';
import { orchestrateDawnSurfaces } from './dawn-surface-orchestrator.mjs';

const selection={id:'surface-ablation',candidates:[
{visualWorkId:'a',score:.44,type:'engraving',surfacePresetIds:['card-8x5'],surfacePresets:[{id:'card-8x5',focalRegionId:'a-focus'}]},
{visualWorkId:'b',score:.42,type:'manuscript-illumination',surfacePresetIds:['card-8x5'],surfacePresets:[{id:'card-8x5',focalRegionId:'b-focus'}]},
{visualWorkId:'c',score:.40,type:'photograph',surfacePresetIds:['card-8x5'],surfacePresets:[{id:'card-8x5',focalRegionId:null}]}
]};

const plain=orchestrateDawnSurfaces(selection);
const contextual=orchestrateDawnSurfaces(selection,{pageIndex:2,pageCount:4,contentRole:'scripture-study',textDensity:.76,previousVisualWorkIds:['a'],previousVisualTypes:['engraving'],preferredPreset:'card-8x5',needsNegativeSpace:true});
const before=plain.surfaces[0].visualWorkIds[0];
const after=contextual.surfaces[0].visualWorkIds[0];
assert.equal(before,'a');
assert.equal(after,'b');
assert.notEqual(before,after);
const pick=contextual.surfaces[0].contextDecision.picks[0];
assert.ok(pick.contextAdjustment>0);
console.log(JSON.stringify({status:'PASS',schema:'dore.surface-context-ablation.v1',before,after,contextAdjustment:pick.contextAdjustment}));
