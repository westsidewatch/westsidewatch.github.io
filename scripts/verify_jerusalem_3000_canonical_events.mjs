import assert from 'node:assert/strict';
import * as THREE from 'three';
import {readFile} from 'node:fs/promises';
import {loadTemporalCityCore} from '../preview/jerusalem-3000/temporal-city-core-adapter.js';
import {registerHerodianUrbanCore} from '../preview/jerusalem-3000/herodian-urban-core-adapter.js';
import {buildHerodianParcelCore} from '../preview/jerusalem-3000/herodian-parcel-core.js';
import {buildHerodianParcelArchitecture} from '../preview/jerusalem-3000/herodian-typology-grammar.js';
import {buildHerodianRoadGeometry} from '../preview/jerusalem-3000/herodian-road-geometry.js';
import {publishHerodianGeneratedEvents} from '../preview/jerusalem-3000/herodian-generated-events.js';
import {createCityProjection} from '../preview/jerusalem-3000/city-lifecycle-projection.js';
import {invalidateCityData} from '../preview/jerusalem-3000/city-data-loader.js';
const root=new URL('../preview/jerusalem-3000/',import.meta.url),json=async path=>JSON.parse(await readFile(new URL(path,root))),timeline=await json('data/continuous-build-timeline.json'),registration=await json('data/urban/herodian-30ce.registration.json');
const original=globalThis.fetch,material=new THREE.MeshStandardMaterial(),materials={inferred:material,reconstructed:material,observed:material,facadeOpening:material},terrain={grid:{origin:{lat:31.778,lon:35.235}},heightAtWorld:(x,z)=>40+x*.01-z*.01},parent=new THREE.Group();
try{
 globalThis.fetch=async url=>({ok:true,json:()=>json(url)});invalidateCityData();const {core}=await loadTemporalCityCore(timeline.phases,{terrain});await registerHerodianUrbanCore(core);await buildHerodianParcelCore(core,terrain);
 const architecture=buildHerodianParcelArchitecture(parent,core,materials,terrain);architecture.meshes.push(...buildHerodianRoadGeometry(parent,registration.roads,materials,terrain));
 const source=core.get('j3k:object:inner-temple'),last=core.get(architecture.buildingIds.at(-1));
 core.register({...last,lifecycle:{...last.lifecycle,events:[{phase:'herodian-jesus',state:'build'}]}});
 const map=core.objects,index=[...core.byPhase].map(([id,set])=>[id,[...set]]),bindings=architecture.meshes.map(m=>m.userData.cityObject.objectId);
 assert.throws(()=>publishHerodianGeneratedEvents(core,{registration,buildingIds:architecture.buildingIds,meshes:architecture.meshes}),/Conflicting canonical lifecycle/);
 assert.strictEqual(core.objects,map);assert.deepEqual([...core.byPhase].map(([id,set])=>[id,[...set]]),index);assert.deepEqual(architecture.meshes.map(m=>m.userData.cityObject.objectId),bindings,'late failure must not partially bind geometry');core.register(last);
 const beforeFailure=core.objects;const invalid=new THREE.Mesh(new THREE.BoxGeometry(1,1,1),material);invalid.userData.cityObject={objectId:'unregistered-component'};
 assert.throws(()=>publishHerodianGeneratedEvents(core,{registration,buildingIds:architecture.buildingIds,meshes:[...architecture.meshes,invalid]}),/Unpublished canonical mesh/);assert.strictEqual(core.objects,beforeFailure);invalid.geometry.dispose();
 const missing=architecture.buildingIds[0];assert.throws(()=>publishHerodianGeneratedEvents(core,{registration,buildingIds:architecture.buildingIds,meshes:architecture.meshes.filter(m=>m.userData.cityObject.parcelId+':building'!==missing)}),/Missing canonical building geometry/);assert.strictEqual(core.objects,beforeFailure);
 const publication=publishHerodianGeneratedEvents(core,{registration,buildingIds:architecture.buildingIds,meshes:architecture.meshes});
 assert.equal(publication.stateFor(architecture.buildingIds[0],''),'absent');
 assert.equal(publication.summary.buildings,architecture.buildings);assert.equal(publication.summary.roads,8);assert.strictEqual(core.get(source.id),source,'sourced anchor events must remain untouched');
 for(const id of architecture.buildingIds){const record=core.get(id);assert.equal(publication.stateFor(id,'herodian-jesus'),'build');assert.equal(publication.stateFor(id,'roman-destruction'),'ruin');assert.equal(publication.stateFor(id,'aelia'),'unresolved');assert.ok(core.phase('roman-destruction').some(r=>r.id===id));assert.equal(core.get(record.source.parcelId).type,'parcel');assert.equal(core.get(record.source.blockId).type,'block');assert.equal(core.get(record.source.districtId).type,'district');assert.deepEqual(core.lineage(id),{predecessors:[],successors:[]});}
 const projection=createCityProjection(parent,architecture.meshes,{stateForObject:(id,phase)=>publication.stateFor(id,phase),stateForInfrastructure:true});projection.apply({phaseId:''});assert.ok(architecture.meshes.every(m=>!m.visible),'startup before timeline selection must stay hidden');projection.apply({phaseId:'herodian-jesus'});const initial=projection.diagnostics();
 for(const type of ['building','road']){const id=type==='building'?architecture.buildingIds[0]:registration.roads[0].id,record=core.get(id),parts=architecture.meshes.filter(m=>m.userData.cityObject.objectId===id);assert.ok(parts.length>0);assert.equal(new Set(parts.map(m=>m.userData.cityObject.componentId)).size,parts.length);core.register({...record,lifecycle:{events:[{phase:'herodian-jesus',state:'unresolved'}]}});projection.apply({phaseId:'herodian-jesus'});assert.ok(parts.every(m=>!m.visible));core.register(record);projection.apply({phaseId:'herodian-jesus'});assert.ok(parts.every(m=>m.visible));}
 projection.apply({phaseId:'roman-destruction',ruin:.9});projection.apply({phaseId:'aelia'});assert.ok(architecture.meshes.every(m=>!m.visible));projection.apply({phaseId:'herodian-jesus'});assert.equal(projection.diagnostics().identityFingerprint,initial.identityFingerprint);assert.equal(projection.diagnostics().transformFingerprint,initial.transformFingerprint);
 assert.ok(core.validate().ok);console.log(JSON.stringify(publication.summary));console.log('PASS: real canonical generated batch, atomic late-conflict rejection, parent chains, eight road bindings, shared event visibility, unknown later fate, exact return and source-anchor preservation');
}finally{globalThis.fetch=original;invalidateCityData();parent.traverse(m=>m.geometry?.dispose());material.dispose();}
