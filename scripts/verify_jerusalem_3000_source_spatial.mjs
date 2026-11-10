import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {sourceSpatialTopology} from '../preview/jerusalem-3000/source-spatial-topology.js';
import {loadTemporalCityCore} from '../preview/jerusalem-3000/temporal-city-core-adapter.js';
import {collectSpatialSkeleton} from '../preview/jerusalem-3000/spatial-skeleton.js';
import {invalidateCityData} from '../preview/jerusalem-3000/city-data-loader.js';
const base=new URL('../preview/jerusalem-3000/',import.meta.url),read=async p=>JSON.parse(await readFile(new URL(p,base))),data=await read('data/objects/herodian-30ce.json'),phases=(await read('data/continuous-build-timeline.json')).phases;
const terrain={grid:{origin:{lat:31.778,lon:35.235}},heightAtWorld:(x,z)=>100+x*.02-z*.1},before=JSON.stringify(data),eligible=data.objects.filter(o=>sourceSpatialTopology(o,terrain));assert.equal(eligible.length,6);
for(const object of data.objects){const topology=sourceSpatialTopology(object,terrain);if(topology){assert.equal(topology.point.x,object.spatial.enuMetres.east);assert.equal(topology.point.z,-object.spatial.enuMetres.north);assert.equal(topology.geometryVerified,false);assert.equal(topology.confidence,'inferred');}}
assert.equal(sourceSpatialTopology(data.objects.find(o=>o.id.endsWith('inner-temple')),terrain),null);assert.equal(sourceSpatialTopology(data.objects.find(o=>o.id.endsWith('eastern-entry-unknown')),terrain),null);
assert.equal(sourceSpatialTopology(data.objects[0],{}),null);
for(const mutate of [o=>o.spatial.enuMetres.east=NaN,o=>o.spatial.enuMetres.east=500,o=>o.spatial.anchor=null]){const bad=structuredClone(data.objects[0]);mutate(bad);assert.throws(()=>sourceSpatialTopology(bad,terrain));}
assert.throws(()=>sourceSpatialTopology(data.objects[0],{...terrain,grid:{origin:{lat:0,lon:0}}}));assert.throws(()=>sourceSpatialTopology(data.objects[0],{...terrain,heightAtWorld:()=>NaN}));assert.equal(JSON.stringify(data),before);
const original=globalThis.fetch;
try{
 globalThis.fetch=async url=>({ok:true,json:()=>read(url)});invalidateCityData();const {core}=await loadTemporalCityCore(phases,{terrain});
 const topologies=[...core.objects.values()].filter(o=>o.metadata.spatialTopology?.authority==='source-provisional-anchor-v1');assert.equal(topologies.length,6);
 const originalRecords=JSON.stringify([...core.objects.values()]);
 for(const [phaseId,position] of [['herodian-jesus',8.9],['roman-destruction',9.9]]){
  const all=collectSpatialSkeleton(core,terrain,{phaseId,position}),features=all.features.filter(f=>f.representation==='source-provisional-zone-not-footprint');assert.equal(features.length,6);assert.equal(features.filter(f=>f.domain==='sacredCivic').length,4);assert.equal(features.filter(f=>f.domain==='routes').length,2);assert.ok(features.every(f=>f.kind==='point'&&f.confidence==='inferred'&&!f.geometryVerified));
  const observed=collectSpatialSkeleton(core,terrain,{phaseId,position,evidenceMode:'observed'});assert.ok(observed.features.every(f=>f.representation!=='source-provisional-zone-not-footprint'));
  assert.deepEqual(collectSpatialSkeleton(core,terrain,{phaseId,position}).features,all.features);
 }
 assert.ok(collectSpatialSkeleton(core,terrain,{phaseId:'aelia',position:10.9}).features.every(f=>f.representation!=='source-provisional-zone-not-footprint'));
 assert.ok(!core.get('j3k:object:inner-temple').metadata.spatialTopology);assert.ok(!core.get('j3k:object:eastern-entry-unknown').metadata.spatialTopology);assert.equal(JSON.stringify([...core.objects.values()]),originalRecords);
 console.log('PASS: six source-zone anchors including the separately inferred perimeter porticoes, canonical origin/ENU/DEM validation, withheld exact temple and eastern gate preserved, phase/event and inferred evidence filtering, unchanged records and no new meshes');
}finally{globalThis.fetch=original;invalidateCityData();}
