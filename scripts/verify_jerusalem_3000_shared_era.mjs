import assert from 'node:assert/strict';
import * as THREE from 'three';
import { TemporalCityCore } from '../preview/jerusalem-3000/temporal-city-core.js';
import { buildEraParcelArchitecture, buildEraParcelArchitectureAsync } from '../preview/jerusalem-3000/herodian-typology-grammar.js';
import { createSharedEraRuntime } from '../preview/jerusalem-3000/shared-era-runtime.js';
import { RuinTransformationEngine } from '../preview/jerusalem-3000/ruin-transformation-engine.js';
import { readFileSync } from 'node:fs';
const phases = [{id:'late-first-temple'}, {id:'babylonian-destruction'}];
const makeCore = () => {
  const core = new TemporalCityCore({ phases });
  for(let i=0;i<12;i++) core.register({id:`parcel-${i}`,type:'parcel',phaseIds:[phases[0].id],
    source:{blockId:'block'},geometry:{primitive:'polygon',polygon:[{x:i*25,z:0},{x:i*25+20,z:0},{x:i*25+20,z:20},{x:i*25,z:20}]},
    metadata:{typologyPool:['courtyard-house','street-house','workshop-house']}});
  return core;
};
const material = new THREE.MeshStandardMaterial(), materials = {inferred:material, facadeOpening:material};
const terrain={heightAtWorld:()=>100};
const options={phaseId:phases[0].id,destroyedPhase:phases[1].id};
const syncGroup=new THREE.Group(), asyncGroup=new THREE.Group();
const sync=buildEraParcelArchitecture(syncGroup,makeCore(),materials,terrain,options);
let yields=0;
const asyncCore=makeCore();
const asyncResult=await buildEraParcelArchitectureAsync(asyncGroup,asyncCore,materials,terrain,{
  ...options,maxBatch:2,yieldControl:async()=>{yields++;},
});
assert.deepEqual(asyncResult.buildingIds,sync.buildingIds);
assert.ok(yields>=7);
assert.equal(asyncResult.meshes.length,sync.meshes.length);
for(let i=0;i<sync.meshes.length;i++){
  assert.deepEqual(asyncResult.meshes[i].position.toArray(),sync.meshes[i].position.toArray());
  assert.deepEqual(Array.from(asyncResult.meshes[i].geometry.attributes.position.array),Array.from(sync.meshes[i].geometry.attributes.position.array));
}
assert.equal(asyncCore.phase(phases[1].id).filter(o=>o.type==='building').length,12);
const controller=new AbortController();
await assert.rejects(buildEraParcelArchitectureAsync(new THREE.Group(),makeCore(),materials,terrain,{
  ...options,signal:controller.signal,yieldControl:async()=>controller.abort(),
}),{name:'AbortError'});
const parent=new THREE.Group();
const runtime=createSharedEraRuntime(parent,{reference:{},footprint:{},terrain,materials});
runtime.request(phases[0].id); runtime.request('modern');
await new Promise(resolve=>setTimeout(resolve,20));
assert.equal(runtime.diagnostics().status,'cancelled');
assert.equal(parent.children.length,0,'cancelled generation must release its staging group');
runtime.dispose();
const failed=createSharedEraRuntime(new THREE.Group(),{reference:{},footprint:{},terrain,materials});
failed.request(phases[0].id);
await new Promise(resolve=>setTimeout(resolve,20));
assert.equal(failed.diagnostics().status,'error','generation failures must not masquerade as success');
failed.dispose();
const timeline=JSON.parse(readFileSync(new URL('../preview/jerusalem-3000/data/continuous-build-timeline.json',import.meta.url))).phases;
const ruin=new RuinTransformationEngine(timeline);
assert.equal(ruin.sample(5.5,'babylonian-destruction').ruin,.5);
assert.equal(ruin.sample(9.5).ruin,.5);
assert.equal(ruin.sample(4.9,'babylonian-destruction').ruin,0);
assert.throws(()=>ruin.sample(4,'late-first-temple'),/Unknown destruction/);
for(const group of [syncGroup,asyncGroup]) group.traverse(o=>o.geometry?.dispose());
material.dispose();
console.log('PASS: deterministic batched geometry, inherited identities, cancellation cleanup, independent destruction boundary');
