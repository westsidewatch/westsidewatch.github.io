import assert from 'node:assert/strict';
import fs from 'node:fs';
import * as THREE from 'three';
import {compileIndependentLaterSkeleton,buildIndependentLaterSkeleton} from '../preview/jerusalem-3000/independent-later-skeleton.js';
import {createLaterMorphologyLedger} from '../preview/jerusalem-3000/later-morphology-ledger.js';
import {TemporalCityCore} from '../preview/jerusalem-3000/temporal-city-core.js';
import {polygonsOverlap} from '../preview/jerusalem-3000/urban-exclusion.js';
import {roadClearancePolygons} from '../preview/jerusalem-3000/district-infill.js';
import {collectSpatialSkeleton} from '../preview/jerusalem-3000/spatial-skeleton.js';
const root=new URL('../preview/jerusalem-3000/',import.meta.url),json=p=>JSON.parse(fs.readFileSync(new URL(p,root))),data=json('data/urban/roman-byzantine-islamic.skeleton.v1.json'),phases=json('data/continuous-build-timeline.json').phases;
const material=new THREE.MeshStandardMaterial({opacity:.2,transparent:true}),materials={inferred:material},terrain={grid:{origin:data.origin},heightAtWorld:(x,z)=>100+x*.03-z*.1},core=new TemporalCityCore({phases,terrain}),publisher=createLaterMorphologyLedger(core);
const fingerprints=[],originalData=JSON.stringify(data),release=runtime=>{runtime.meshes.forEach(m=>{m.geometry.dispose();m.removeFromParent();});runtime.disposeMaterials();};
for(const phase of Object.keys(data.phases)){
 const registration=compileIndependentLaterSkeleton(data,phase,data.origin),group=new THREE.Group(),runtime=buildIndependentLaterSkeleton(group,registration,materials,terrain),binding=publisher.bind(runtime);binding.apply(()=>true);
 assert.equal(registration.roads.length,3);assert.ok(runtime.meshes.length>0);assert.ok(runtime.ledgerRecords.every(r=>r.type!=='building'));assert.ok(core.validate().ok);
 for(const block of runtime.ledgerRecords.filter(r=>r.type==='block')){assert.ok(registration.districts.some(d=>d.id===block.source.districtId));assert.ok(registration.reservations.every(r=>!polygonsOverlap(block.geometry.polygon,r.geometry.polygon)));assert.ok(roadClearancePolygons(registration.roads,5).every(r=>!polygonsOverlap(block.geometry.polygon,r.polygon)));}
 for(const mesh of runtime.meshes){const p=mesh.geometry.attributes.position;assert.ok(Array.from(p.array).every(Number.isFinite));if(mesh.userData.cityObject.kind==='block'){for(let i=0;i<p.count;i++){const d=p.getY(i)-terrain.heightAtWorld(p.getX(i),p.getZ(i));assert.ok(Math.abs(d-.2)<1e-4||Math.abs(d-6)<1e-4,'all coarse cell vertices follow the same slope');}const normal=mesh.geometry.attributes.normal;assert.ok(normal.getY(0)>0,'coarse cap must face up');}}
 const snapshot=collectSpatialSkeleton(core,terrain,{phaseId:phase,position:phases.findIndex(p=>p.id===phase)+.9});assert.ok(snapshot.domains.districts.spatialObjects>0);assert.equal(snapshot.domains.routes.spatialObjects,3);
 const bad={...runtime,ledgerRecords:runtime.ledgerRecords.map(r=>r.type==='block'?{...r,source:{...r.source,districtId:'missing'}}:r)},isolated=new TemporalCityCore({phases,terrain}),rejected=createLaterMorphologyLedger(isolated);
 assert.throws(()=>rejected.bind(bad),/district relation missing/);assert.equal(isolated.objects.size,0);rejected.dispose();
 const ids=runtime.meshes.map(m=>m.userData.cityObject.objectId),geometry=runtime.meshes.map(m=>Array.from(m.geometry.attributes.position.array));fingerprints.push(JSON.stringify(registration.districts.map(d=>d.geometry.polygon)));assert.equal(new Set(runtime.meshes.map(m=>m.userData.cityObject.componentId)).size,runtime.meshes.length);assert.ok(runtime.meshes.every(m=>m.material!==material&&m.material.opacity===1&&!m.material.transparent));
 binding.apply(()=>false);assert.ok(runtime.meshes.every(m=>!m.visible));binding.apply(()=>true);assert.ok(runtime.meshes.every(m=>m.visible));
 const rebuilt=buildIndependentLaterSkeleton(new THREE.Group(),registration,materials,terrain),count=core.objects.size;publisher.bind(rebuilt);assert.equal(core.objects.size,count);assert.deepEqual(rebuilt.meshes.map(m=>m.userData.cityObject.objectId),ids);assert.deepEqual(rebuilt.meshes.map(m=>Array.from(m.geometry.attributes.position.array)),geometry);
 release(runtime);release(rebuilt);
}
assert.equal(new Set(fingerprints).size,3,'three eras must have distinct independently authored envelopes');
assert.throws(()=>compileIndependentLaterSkeleton(data,'aelia',{lat:0,lon:0}));
for(const mutate of [d=>d.phases.aelia.roads[0].id='',d=>d.phases.aelia.roads[0].sources=[],d=>d.phases.aelia.roads[0].points=[[0,0],[0,0]],d=>d.phases.aelia.districts[0].polygon=[[0,0],[1,0],[2,0]]]){const bad=structuredClone(data);mutate(bad);assert.throws(()=>compileIndependentLaterSkeleton(bad,'aelia',data.origin));}
const failed=new THREE.Group();assert.throws(()=>buildIndependentLaterSkeleton(failed,compileIndependentLaterSkeleton(data,'aelia',data.origin),materials,{heightAtWorld:()=>NaN}));assert.equal(failed.children.length,0);
assert.equal(JSON.stringify(data),originalData);publisher.dispose();assert.equal(core.objects.size,0);material.dispose();console.log('PASS: three independent period skeletons, shared origin, roads/reservations constrain coarse cells, DEM-following caps, distinct phase IDs, evidence return, exact rebuild, malformed source/geometry rejection and owned cleanup');
