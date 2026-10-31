import {laterSacredCores,sacredCoreGeometry} from '../preview/jerusalem-3000/later-sacred-cores.js';
import assert from 'node:assert/strict';import fs from 'node:fs';import * as THREE from 'three';
import {compileIndependentLaterSkeleton,buildIndependentLaterSkeleton} from '../preview/jerusalem-3000/independent-later-skeleton.js';
import {createLaterMorphologyLedger} from '../preview/jerusalem-3000/later-morphology-ledger.js';
import {TemporalCityCore} from '../preview/jerusalem-3000/temporal-city-core.js';
import {coreStageAt} from '../preview/jerusalem-3000/landmark-chronology.js';
const read=p=>JSON.parse(fs.readFileSync(new URL('../preview/jerusalem-3000/'+p,import.meta.url))),packs=['roman-byzantine-islamic','medieval-ottoman','expansion-modern'].map(n=>read(`data/urban/${n}.skeleton.v1.json`)),phases=read('data/continuous-build-timeline.json').phases;
const terrain={grid:{origin:packs[0].origin},heightAtWorld:(x,z)=>100+x*.02+z*.01},core=new TemporalCityCore({phases,terrain}),publisher=createLaterMorphologyLedger(core),material=new THREE.MeshStandardMaterial(),runtimes=[];
const visible=(runtime,id)=>runtime.meshes.filter(m=>m.visible&&m.userData.cityObject.objectId===id);
for(const phase of ['byzantine','early-islamic','crusader']){
 const pack=packs.find(p=>p.phases[phase]),registration=compileIndependentLaterSkeleton(pack,phase,terrain.grid.origin),runtime=buildIndependentLaterSkeleton(new THREE.Group(),registration,{inferred:material},terrain),binding=publisher.bind(runtime),index=phases.findIndex(p=>p.id===phase);runtimes.push(runtime);
 const snapshots=runtime.meshes.map(m=>[m.uuid,m.geometry.uuid,Array.from(m.geometry.attributes.position.array)]);
 for(const record of registration.cores.filter(c=>c.metadata.landmarkChronology)){
  const actual=core.get(record.id),plan=actual.metadata.landmarkChronology;assert.deepEqual(actual.predecessorIds,[]);assert.deepEqual(actual.successorIds,[]);
  assert.equal(actual.lifecycle.events.at(-1).state,'unresolved','following era fate remains unknown');
  for(const stage of plan.stages){
   const position=index+stage.offset;
   binding.apply(()=>true,{position:position+1e-8});const meshes=visible(runtime,record.id);assert.equal(meshes.length,1,'exactly one cached version at a date');assert.equal(meshes[0].userData.landmarkRepresentation.profile,stage.profile);assert.equal(coreStageAt(actual,stage.offset).year,stage.year);
   binding.apply(()=>true,{position:Math.max(index,position-1e-8)});if(stage.offset>0)assert.ok(visible(runtime,record.id).every(m=>m.userData.landmarkRepresentation.profile!==stage.profile),'future form must not appear before its event');
   binding.apply(()=>false,{position:position+1e-8});assert.equal(visible(runtime,record.id).length,0);
  }
  if(record.id.endsWith('nea-context')){binding.apply(()=>true,{position:index+.1});assert.equal(visible(runtime,record.id).length,0);assert.ok(runtime.meshes.filter(m=>core.get(m.userData.cityObject.objectId)?.metadata.coreReference===record.id).every(m=>!m.visible),'future church must not have a visible dedicated access road');}
  if(phase==='early-islamic'){
   const original=core.get(record.id),edited=original.lifecycle.events.map(e=>e.year===1009?{...e,offset:.7}:e);
   core.register({...original,lifecycle:{events:edited}});binding.apply(()=>true,{position:index+.75});assert.equal(visible(runtime,record.id)[0].userData.landmarkRepresentation.profile,'sepulchre-1009-fragments','live ledger event offsets override source declarations without rebuilding');core.register(original);
  }
  const original=core.get(record.id);core.register({...original,lifecycle:{events:[{phase,state:'unresolved'}]}});binding.apply(()=>true);assert.equal(visible(runtime,record.id).length,0,'edited common events control every variant');core.register(original);
 }
 binding.apply(()=>true,{position:index+.95});binding.apply(()=>true,{position:index+.1});binding.apply(()=>true,{position:index+.95});assert.deepEqual(runtime.meshes.map(m=>[m.uuid,m.geometry.uuid,Array.from(m.geometry.attributes.position.array)]),snapshots,'date scrubbing does not regenerate/deform geometry');
}
const islamic=runtimes[1],id='j3k:early-islamic:independent:monument:holy-sepulchre-context',versions=islamic.meshes.filter(m=>m.userData.cityObject.objectId===id),boxes=new Map(versions.map(m=>[m.userData.landmarkRepresentation.profile,new THREE.Box3().setFromObject(m)]));
const ruin=boxes.get('sepulchre-1009-fragments'),restored=boxes.get('sepulchre-1048-rotunda'),old=boxes.get('constantinian-rotunda-east-basilica');assert.ok(ruin.max.y<restored.max.y-20,'actual destroyed version has no intact dome');assert.ok(restored.max.x<old.max.x-50,'1048 version must not restore the eastern Martyrium');
for(const runtime of runtimes)for(const mesh of runtime.landmarkMeshes){const record=core.get(mesh.userData.cityObject.objectId),p=mesh.geometry.attributes.position;for(let i=0;i<p.count;i++){if(record.metadata.precinctContext)continue;const structured=['octagonal-rock-shrine','aqsa-seven-aisle-context'].includes(record.metadata.coreProfile),base=structured?terrain.heightAtWorld(0,0)+.8:terrain.heightAtWorld(p.getX(i),p.getZ(i));assert.ok(p.getY(i)>=base-1e-4||(structured&&Math.abs(p.getY(i)-Math.min(terrain.heightAtWorld(0,0)+.8+(record.metadata.coreProfile==='octagonal-rock-shrine'?3:0),terrain.heightAtWorld(p.getX(i),p.getZ(i))-.15))<1e-4),'upper masses stay above their floor; render-only footings meet the original terrain');}const box=new THREE.Box3().setFromObject(mesh);assert.ok(box.min.x>=Math.min(...record.geometry.polygon.map(p=>p.x))-1e-4&&box.max.x<=Math.max(...record.geometry.polygon.map(p=>p.x))+1e-4,'all variants fit the common reserved precinct');}
// The rotunda must not slide20m when the surrounding church version changes.
let rotundaApex=null;
for(const phase of ['byzantine','early-islamic','crusader','ayyubid-mamluk','ottoman','outside-walls','modern']){
 const record=laterSacredCores(phase).find(c=>c.id.endsWith('holy-sepulchre-context')),geometry=sacredCoreGeometry(record,terrain),p=geometry.attributes.position;let top=0;for(let i=1;i<p.count;i++)if(p.getY(i)>p.getY(top))top=i;
 const apex=[p.getX(top),p.getY(top),p.getZ(top)];if(rotundaApex)assert.deepEqual(apex,rotundaApex,'same displayed rotunda anchor and modern DEM upper datum in all7 periods');else rotundaApex=apex;geometry.dispose();
}
assert.ok(core.validate().ok);publisher.dispose();for(const runtime of runtimes){runtime.meshes.forEach(m=>m.geometry.dispose());runtime.disposeMaterials();}material.dispose();console.log('PASS: dated335/543/1009/1048/1149 source stages, actual loss of dome/Martyrium, no future access, one cached form, event/evidence control, exact reverse identity, reserved footprint and DEM clearance');
