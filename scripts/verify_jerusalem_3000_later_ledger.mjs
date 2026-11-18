import {ERA_FOOTPRINTS,addEraFabric} from '../preview/jerusalem-3000/legacy-era-fabric.js';
import assert from 'node:assert/strict';
import * as THREE from 'three';
import {readFileSync} from 'node:fs';
import {TemporalCityCore} from '../preview/jerusalem-3000/temporal-city-core.js';
import {createLaterMorphologyLedger} from '../preview/jerusalem-3000/later-morphology-ledger.js';
import {buildPhase2UrbanMorphology,setPhase2MorphologyProgress} from '../preview/jerusalem-3000/phase2-urban-morphology.js';
import {buildOttomanUrbanMorphology,setOttomanMorphologyProgress} from '../preview/jerusalem-3000/ottoman-urban-morphology.js';
import {lifecycleStateAt} from '../preview/jerusalem-3000/construction-engine.js';
const timeline=JSON.parse(readFileSync(new URL('../preview/jerusalem-3000/data/continuous-build-timeline.json',import.meta.url))),terrain={heightAtWorld:(x,z)=>40+x*.02-z*.01},core=new TemporalCityCore({phases:timeline.phases,terrain});
core.register({id:'foreign',type:'water',confidence:'inferred',phaseIds:['ottoman']});
const publisher=createLaterMorphologyLedger(core),materials=Object.fromEntries(['observed','reconstructed','inferred'].map(k=>[k,new THREE.MeshStandardMaterial()]));
const buildMorphology=(phase,progress)=>phase==='ottoman'?buildOttomanUrbanMorphology(new THREE.Group(),materials,terrain,{progress}):buildPhase2UrbanMorphology(new THREE.Group(),phase,materials,terrain,{progress});
const build=(phase,progress)=>['crusader','ottoman'].includes(phase)?buildMorphology(phase,progress):{phaseId:phase,meshes:addEraFabric(new THREE.Group(),phase,materials.reconstructed,false,terrain),grammar:'legacy-era-footprint-masses',fixedVisibility:true};
const progress=(runtime,value)=>runtime.fixedVisibility?null:runtime.phaseId==='ottoman'?setOttomanMorphologyProgress(runtime,value):setPhase2MorphologyProgress(runtime,value);
const release=runtime=>runtime.meshes.forEach(mesh=>mesh.geometry.dispose());
for(const phase of ['crusader','ottoman','aelia','byzantine','early-islamic','ayyubid-mamluk','outside-walls','modern']){
 const runtime=build(phase,.9),binding=publisher.bind(runtime),records=core.phase(phase).filter(r=>r.metadata.generationPhase===phase);
 assert.equal(records.length,runtime.meshes.length);if(runtime.fixedVisibility)assert.equal(records.length,ERA_FOOTPRINTS[phase].density);assert.equal(binding.summary.semanticBuildings,0);
 binding.apply(()=>true);assert.ok(runtime.meshes.some(m=>m.visible));
 const identity=runtime.meshes.map(m=>m.userData.cityObject.objectId),transforms=runtime.meshes.map(m=>[m.position.toArray(),m.scale.toArray(),m.rotation.toArray()]);
 for(const record of records){assert.notEqual(record.type,'building');assert.equal(record.confidence,'inferred');assert.equal(record.source.geometryVerified,false);assert.deepEqual(core.lineage(record.id),{predecessors:[],successors:[]});const next=timeline.phases[timeline.phases.findIndex(p=>p.id===phase)+1]?.id;if(next)assert.equal(lifecycleStateAt({lifecycleEvents:record.lifecycle.events},timeline,next),'unresolved');else assert.equal(record.lifecycle.events.length,1,'timeline end must not invent a future phase');}
 const target=records.find(r=>runtime.meshes.some(m=>m.visible&&m.userData.cityObject.objectId===r.id));
 core.register({...target,lifecycle:{events:[{phase,state:'unresolved'}]}});progress(runtime,.9);binding.apply(()=>true);assert.equal(runtime.meshes.find(m=>m.userData.cityObject.objectId===target.id).visible,false);
 const rebuilt=build(phase,.9),size=core.objects.size,rebinding=publisher.bind(rebuilt);rebinding.apply(()=>true);assert.equal(core.objects.size,size);assert.equal(rebuilt.meshes.find(m=>m.userData.cityObject.objectId===target.id).visible,false,'rebuild must preserve shared event edits');
 core.register(target);progress(rebuilt,.9);rebinding.apply(()=>true);assert.deepEqual(rebuilt.meshes.map(m=>m.userData.cityObject.objectId),identity);assert.deepEqual(rebuilt.meshes.map(m=>[m.position.toArray(),m.scale.toArray(),m.rotation.toArray()]),transforms);
 progress(rebuilt,.9);rebinding.apply(()=>false);assert.ok(rebuilt.meshes.every(m=>!m.visible));progress(rebuilt,.9);rebinding.apply(()=>true);assert.ok(rebuilt.meshes.some(m=>m.visible));
 const changed=build(phase,.9);changed.meshes.at(-1).position.x+=1;assert.throws(()=>publisher.bind(changed),/migration/);assert.ok(changed.meshes.every(m=>!m.userData.cityObject));assert.equal(core.objects.size,size);
 const other=createLaterMorphologyLedger(core),duplicate=build(phase,.9);assert.throws(()=>other.bind(duplicate),/collision/);other.dispose();assert.equal(core.objects.size,size);
 const isolated=new TemporalCityCore({phases:timeline.phases,terrain});isolated.register(records.at(-1));const failing=createLaterMorphologyLedger(isolated),partial=build(phase,.9);assert.throws(()=>failing.bind(partial),/collision/);assert.deepEqual([...isolated.objects.keys()],[records.at(-1).id]);assert.ok(partial.meshes.every(m=>!m.userData.cityObject));failing.dispose();
 [runtime,rebuilt,changed,duplicate,partial].forEach(release);
}
assert.ok(core.validate().ok);publisher.dispose();assert.deepEqual([...core.objects.keys()],['foreign']);assert.ok(core.validate().ok);Object.values(materials).forEach(m=>m.dispose());
console.log('PASS: eight later-era whole batches, stable rebuild IDs/transforms, scaffold semantics, unknown later fate, live event/evidence visibility, migration rejection, late collision rollback and owned cleanup');
