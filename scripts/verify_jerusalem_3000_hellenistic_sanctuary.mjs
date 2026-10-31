import assert from 'node:assert/strict';
import fs from 'node:fs';
import * as THREE from 'three';
import {TemporalCityCore} from '../preview/jerusalem-3000/temporal-city-core.js';
import {compileHellenisticSanctuary,createHellenisticSanctuary} from '../preview/jerusalem-3000/hellenistic-sanctuary.js';
import {buildHerodianRoadGeometry} from '../preview/jerusalem-3000/herodian-road-geometry.js';
import {buildEraParcelCore} from '../preview/jerusalem-3000/herodian-parcel-core.js';
import {applyMetricResidentialRegistration} from '../preview/jerusalem-3000/metric-residential-layout.js';
import {polygonsOverlap} from '../preview/jerusalem-3000/urban-exclusion.js';
const read=p=>JSON.parse(fs.readFileSync(new URL('../preview/jerusalem-3000/'+p,import.meta.url)));
const data=read('data/urban/hellenistic-sanctuary.v1.json'),registration=applyMetricResidentialRegistration(read('data/urban/hellenistic-metric.registration.v1.json')),phases=read('data/continuous-build-timeline.json').phases;
const terrain={grid:{origin:registration.origin},heightAtWorld:(x,z)=>60+x*.01+z*.02},layout=compileHellenisticSanctuary(data,registration,terrain.grid.origin),core=new TemporalCityCore({phases,terrain});
const institution={id:'j3k:object:second-temple-early',type:'monument',phaseIds:['persian-nehemiah','hellenistic-hasmonean'],confidence:'inferred',lifecycle:{events:[{phase:'persian-nehemiah',state:'rebuild'},{phase:'hellenistic-hasmonean',state:'transform'}]}};core.register(institution);const original=core.get(institution.id);
const group=new THREE.Group(),runtime=createHellenisticSanctuary(group,{data,layout,terrain,core});runtime.apply({position:7.9});assert.ok(runtime.diagnostics().visibleTemple>10);assert.equal(runtime.diagnostics().visibleAccess,true);assert.equal(core.get(institution.id),original,'new illustrative version must not overwrite Persian institution/geometry authority');
const meshes=group.children[0].children,identity=meshes.map(m=>m.geometry.uuid),positions=meshes.map(m=>Array.from(m.geometry.attributes.position.array));

meshes.forEach(m=>m.updateMatrixWorld(true));
const actual=id=>meshes.find(m=>m.userData.cityObject.componentId===`j3k:hellenistic-sanctuary:${id}`),roofBox=new THREE.Box3().setFromObject(actual('hall-roof')),roofCentre=roofBox.getCenter(new THREE.Vector3());
const edgeBox=new THREE.Box3().setFromObject(actual('hall-roof-edge-1'));
assert.ok(Math.abs(edgeBox.max.y-roofBox.max.y-.4)<1e-4,'actual roof must be recessed below perimeter');
const floorBox=new THREE.Box3().setFromObject(actual('hall-floor')),boundaryBox=new THREE.Box3().setFromObject(actual('hall-inner-lintel')),boundaryCentre=boundaryBox.getCenter(new THREE.Vector3());
const portalRay=new THREE.Raycaster(new THREE.Vector3(boundaryCentre.x+1,floorBox.max.y+1,roofCentre.z),new THREE.Vector3(-1,0,0),0,2);
assert.equal(portalRay.intersectObjects(meshes,true).length,0,'internal boundary must contain an actual clear doorway');

for(const side of[-1,1])for(let i=0;i<3;i++){
 const id=`hall-priest-room-${side}-${i}`,roomBox=new THREE.Box3().setFromObject(actual(id+'-floor')),centre=roomBox.getCenter(new THREE.Vector3()),front=new THREE.Box3().setFromObject(actual(id+'-lintel'));
 const doorRay=new THREE.Raycaster(new THREE.Vector3(centre.x,roomBox.max.y+1,front.getCenter(new THREE.Vector3()).z+side),new THREE.Vector3(0,0,-side),0,2);
 assert.equal(doorRay.intersectObjects(meshes,true).length,0,'each priests chamber must have a real doorway');
 assert.ok(Math.abs(new THREE.Box3().setFromObject(actual(id+'-roof')).min.y-new THREE.Box3().setFromObject(actual(id+'-back')).max.y)<1e-4,'annex roofs and walls must share the datum');
}
// Actual upper faces must join despite a sloping ground surface.
const box=id=>new THREE.Box3().setFromObject(meshes.find(m=>m.userData.cityObject.componentId===`j3k:hellenistic-sanctuary:${id}`));
for(const id of ['hall-west','hall-side--1','hall-side-1','hall-front--1','hall-front-1','hall-door-lintel'])assert.ok(Math.abs(box(id).max.y-box('hall-roof').min.y)<1e-5,`${id} must meet roof datum`);
for(const id of ['porch-side--1','porch-side-1'])assert.ok(Math.abs(box(id).max.y-box('porch-roof').min.y)<1e-5,'porch roof must meet side walls');
const access=meshes.find(m=>m.userData.cityObject.role==='access'),p=access.geometry.attributes.position;
for(let i=0;i<p.count;i+=3){const triangle=[0,1,2].map(k=>({x:p.getX(i+k),z:p.getZ(i+k)}));for(const obstacle of meshes.filter(m=>!['access','roof','floor'].includes(m.userData.cityObject.role)&&!m.userData.cityObject.componentId.includes('lintel'))){const b=new THREE.Box3().setFromObject(obstacle);assert.ok(!polygonsOverlap(triangle,[{x:b.min.x,z:b.min.z},{x:b.max.x,z:b.min.z},{x:b.max.x,z:b.max.z},{x:b.min.x,z:b.max.z}]),`route crosses actual ${obstacle.userData.cityObject.componentId}`);}}
for(const mesh of meshes){mesh.updateMatrix();const p=mesh.geometry.attributes.position;for(let i=0;i<p.count;i++){const v=new THREE.Vector3().fromBufferAttribute(p,i).applyMatrix4(mesh.matrix);assert.ok(v.y>=terrain.heightAtWorld(v.x,v.z)-1e-4,'geometry must remain above canonical terrain');}}
const streetGroup=new THREE.Group(),material=new THREE.MeshStandardMaterial(),streetMeshes=buildHerodianRoadGeometry(streetGroup,registration.roads,{inferred:material},terrain,{exclusions:layout.roadExclusions});
const arrival=core.get(layout.access.id).metadata.spatialTopology.points[0];let hit=false;
for(const mesh of streetMeshes){const p=mesh.geometry.attributes.position,poly=Array.from({length:p.count},(_,i)=>({x:p.getX(i),z:p.getZ(i)}));const boundary=[poly[0],poly[1],poly[3],poly[2]];assert.ok(layout.roadExclusions.every(r=>!polygonsOverlap(boundary,r.polygon)),'rendered street must not cross reserved precinct');if(mesh.userData.cityObject.objectId===layout.access.from){const b=new THREE.Box3().setFromObject(mesh);if(arrival.x>=b.min.x&&arrival.x<=b.max.x&&arrival.z>=b.min.z&&arrival.z<=b.max.z)hit=true;}}
assert.ok(hit,'access must reach an actual retained street mesh');
const parcels=buildEraParcelCore(core,terrain,{phaseId:registration.phase,registration,districtId:registration.districts[0].id,exclusions:layout.reservations});assert.ok(parcels.count>0);for(const parcel of parcels.parcels)for(const r of layout.reservations)assert.ok(!polygonsOverlap(parcel.geometry.polygon,r.polygon),'no housing parcel inside sanctuary or approach');
for(const position of [6.9,8.1,11.9]){runtime.apply({position});assert.equal(runtime.diagnostics().visibleTemple,0,'selected profile must never leak into earlier/later phases');}
runtime.apply({position:7.9});assert.deepEqual(meshes.map(m=>m.geometry.uuid),identity);assert.deepEqual(meshes.map(m=>Array.from(m.geometry.attributes.position.array)),positions);runtime.apply({position:7.9,evidenceAllowed:()=>false});assert.equal(runtime.diagnostics().visibleTemple,0);assert.equal(runtime.diagnostics().visibleAccess,false);
assert.deepEqual(core.lineage(layout.objectId),{predecessors:[],successors:[]});assert.ok(core.validate().ok);runtime.dispose();streetMeshes.forEach(m=>m.geometry.dispose());material.dispose();console.log('PASS: selected Hellenistic sanctuary version, preserved Persian authority, actual portal/route/terrain clearance, street connection, housing reservation, phase isolation, cached return and evidence filtering');
