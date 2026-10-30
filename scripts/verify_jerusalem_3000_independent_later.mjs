import {coreStageVisible} from '../preview/jerusalem-3000/landmark-chronology.js';
import {neaCore} from '../preview/jerusalem-3000/nea-core.js';
import {aqsaCore} from '../preview/jerusalem-3000/aqsa-core.js';
import {sacredCoreGeometry} from '../preview/jerusalem-3000/later-sacred-cores.js';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import * as THREE from 'three';
import {compileIndependentLaterSkeleton,buildIndependentLaterSkeleton} from '../preview/jerusalem-3000/independent-later-skeleton.js';
import {createLaterMorphologyLedger} from '../preview/jerusalem-3000/later-morphology-ledger.js';
import {TemporalCityCore} from '../preview/jerusalem-3000/temporal-city-core.js';
import {pointInPolygon,polygonsOverlap} from '../preview/jerusalem-3000/urban-exclusion.js';
import {roadClearancePolygons} from '../preview/jerusalem-3000/district-infill.js';
import {collectSpatialSkeleton} from '../preview/jerusalem-3000/spatial-skeleton.js';
const root=new URL('../preview/jerusalem-3000/',import.meta.url),json=p=>JSON.parse(fs.readFileSync(new URL(p,root))),packs=['roman-byzantine-islamic','medieval-ottoman','expansion-modern'].map(name=>json(`data/urban/${name}.skeleton.v1.json`)),data=packs[0],phases=json('data/continuous-build-timeline.json').phases;
const material=new THREE.MeshStandardMaterial({opacity:.2,transparent:true}),materials={inferred:material},terrain={grid:{origin:data.origin},heightAtWorld:(x,z)=>100+x*.03-z*.1},core=new TemporalCityCore({phases,terrain}),publisher=createLaterMorphologyLedger(core);
const fingerprints=[],originalData=JSON.stringify(packs),release=runtime=>{runtime.meshes.forEach(m=>{m.geometry.dispose();m.removeFromParent();});runtime.disposeMaterials();};
for(const pack of packs)for(const phase of Object.keys(pack.phases)){
 const registration=compileIndependentLaterSkeleton(pack,phase,data.origin),group=new THREE.Group(),runtime=buildIndependentLaterSkeleton(group,registration,materials,terrain),binding=publisher.bind(runtime);binding.apply(()=>true);
 assert.equal(registration.roads.length,pack.phases[phase].roads.length+registration.cores.length);const corridor=registration.roads.find(r=>r.metadata.placeId==='j3k:place:eastern-cardo-corridor');assert.ok(corridor);assert.deepEqual(corridor.geometry.points,[[-340,-610],[-300,-350],[-270,-100],[-240,200],[-220,380]].map(([x,z])=>({x,z})));assert.ok(corridor.source.urls.some(u=>u.includes('/vol138/iss1/57/')));assert.equal(corridor.metadata.placeRelation,'shared-route-corridor-not-surviving-pavement');assert.ok(runtime.meshes.length>0);assert.ok(runtime.ledgerRecords.every(r=>r.type!=='building'));assert.ok(core.validate().ok);
 for(const monument of registration.cores){
  const approach=registration.roads.find(r=>r.metadata.coreReference===monument.id),axis=registration.roads.find(r=>r.id===approach?.metadata.axisReference);
  assert.ok(approach&&axis,'every admitted landmark has a contemporary route relation');assert.equal(approach.metadata.entranceIdentified,false);assert.equal(approach.metadata.routeGeometryVerified,false);
  const [start,end]=approach.geometry.points;assert.equal(pointInPolygon(start,monument.geometry.polygon),false);assert.equal(pointInPolygon(end,monument.geometry.polygon),true);
  const onSegment=(p,a,b)=>{const dx=b.x-a.x,dz=b.z-a.z;return Math.abs(dx*(p.z-a.z)-dz*(p.x-a.x))<1e-6&&(p.x-a.x)*(p.x-b.x)+(p.z-a.z)*(p.z-b.z)<=1e-6;};
  assert.ok(axis.geometry.points.slice(1).some((b,i)=>onSegment(start,axis.geometry.points[i],b)),'approach starts on the actual axis segment, not off-road');
  assert.ok(monument.geometry.polygon.some((a,i)=>onSegment(end,a,monument.geometry.polygon[(i+1)%monument.geometry.polygon.length])),'approach stops at the core edge');
  for(let step=0;step<20;step++)assert.equal(pointInPolygon({x:start.x+(end.x-start.x)*step/20,z:start.z+(end.z-start.z)*step/20},monument.geometry.polygon),false,'connector must not run through its core');
 }
 const monuments=runtime.ledgerRecords.filter(r=>r.type==='monument');assert.equal(monuments.length,phase==='aelia'?0:phase==='byzantine'?2:3);for(const monument of monuments){assert.ok(registration.sources.includes(monument.source.urls[0]));assert.equal(monument.metadata.geometryVerified,false);assert.equal(monument.metadata.wholePhaseSimultaneity,false);const record=core.get(monument.id);assert.equal(record.predecessorIds.length,0);assert.equal(record.successorIds.length,0);assert.ok(record.lifecycle.events.every(e=>e.phase===phase||e.state==='unresolved'));assert.ok(runtime.meshes.some(m=>m.userData.cityObject.objectId===monument.id));}
 for(const block of runtime.ledgerRecords.filter(r=>r.type==='block')){assert.ok(monuments.every(r=>!polygonsOverlap(block.geometry.polygon,r.geometry.polygon)));assert.ok(registration.districts.some(d=>d.id===block.source.districtId));assert.ok(registration.reservations.every(r=>!polygonsOverlap(block.geometry.polygon,r.geometry.polygon)));assert.ok(roadClearancePolygons(registration.roads,5).every(r=>!polygonsOverlap(block.geometry.polygon,r.polygon)));}
 for(const mesh of runtime.meshes){const p=mesh.geometry.attributes.position;assert.ok(Array.from(p.array).every(Number.isFinite));if(mesh.userData.cityObject.kind==='block'){for(let i=0;i<p.count;i++){const d=p.getY(i)-terrain.heightAtWorld(p.getX(i),p.getZ(i));assert.ok(Math.abs(d-.2)<1e-4||Math.abs(d-6)<1e-4,'all coarse cell vertices follow the same slope');}const normal=mesh.geometry.attributes.normal;assert.ok(normal.getY(0)>0,'coarse cap must face up');}}
 for(const mesh of runtime.meshes.filter(m=>m.userData.cityObject.kind==='road')){const a=mesh.geometry.attributes.position;const polygon=[0,2,3,1].map(i=>({x:a.getX(i),z:a.getZ(i)}));assert.ok(monuments.every(r=>!polygonsOverlap(polygon,r.geometry.polygon)),'display roads must not cross core envelopes');}
 const snapshot=collectSpatialSkeleton(core,terrain,{phaseId:phase,position:phases.findIndex(p=>p.id===phase)+.9});assert.ok(snapshot.domains.districts.spatialObjects>0);assert.equal(snapshot.domains.routes.spatialObjects,registration.roads.length);assert.equal(snapshot.domains.sacredCivic.spatialObjects,monuments.length);
 const bad={...runtime,ledgerRecords:runtime.ledgerRecords.map(r=>r.type==='block'?{...r,source:{...r.source,districtId:'missing'}}:r)},isolated=new TemporalCityCore({phases,terrain}),rejected=createLaterMorphologyLedger(isolated);
 assert.throws(()=>rejected.bind(bad),/district relation missing/);assert.equal(isolated.objects.size,0);rejected.dispose();
 const ids=runtime.meshes.map(m=>m.userData.cityObject.objectId),geometry=runtime.meshes.map(m=>Array.from(m.geometry.attributes.position.array));fingerprints.push(JSON.stringify(registration.districts.map(d=>d.geometry.polygon)));assert.equal(new Set(runtime.meshes.map(m=>m.userData.cityObject.componentId)).size,runtime.meshes.length);assert.ok(runtime.meshes.every(m=>m.material!==material&&m.material.opacity===1&&!m.material.transparent));
 binding.apply(()=>true,{constructionProgress:0});assert.ok(runtime.meshes.filter(m=>m.userData.cityObject.kind==='block').every(m=>!m.visible));binding.apply(()=>true,{constructionProgress:.5});const half=runtime.meshes.filter(m=>m.userData.cityObject.kind==='block'&&m.visible).length;assert.ok(half>0);binding.apply(()=>true,{constructionProgress:1});assert.ok(runtime.meshes.filter(m=>m.userData.cityObject.kind==='block'&&m.visible).length>half);
 binding.apply(()=>false);assert.ok(runtime.meshes.every(m=>!m.visible));binding.apply(()=>true);assert.ok(runtime.meshes.every(m=>m.visible===(!m.userData.landmarkRepresentation||coreStageVisible(core.get(m.userData.cityObject.objectId),m.userData.landmarkRepresentation.profile,.999999))),'only the active cached landmark version should be visible');
 const rebuilt=buildIndependentLaterSkeleton(new THREE.Group(),registration,materials,terrain),count=core.objects.size;publisher.bind(rebuilt);assert.equal(core.objects.size,count);assert.deepEqual(rebuilt.meshes.map(m=>m.userData.cityObject.objectId),ids);assert.deepEqual(rebuilt.meshes.map(m=>Array.from(m.geometry.attributes.position.array)),geometry);
 release(runtime);release(rebuilt);
}
assert.equal(new Set(fingerprints).size,8,'eight eras must have distinct independently authored envelopes');
// The expansion pair must actually share the authored old-city background while extending outward.
const medieval=packs[1].phases.ottoman,pair=packs[2].phases;
for(const phase of ['outside-walls','modern']){
 const layout=pair[phase],background=layout.districts.filter(d=>d.layoutRole==='old-city-context');
 assert.deepEqual(background.map(d=>d.polygon),medieval.districts.map(d=>d.polygon));
 assert.deepEqual(layout.roads.filter(d=>d.layoutRole==='old-city-route-context').map(d=>d.points),medieval.roads.map(d=>d.points));
 assert.ok(layout.districts.some(d=>d.layoutRole==='extra-mural-expansion'));
 const source=compileIndependentLaterSkeleton(packs[2],phase,data.origin);assert.equal(source.districts.filter(d=>d.metadata.layoutRole==='old-city-context').length,6);
}
const west=layout=>Math.min(...layout.districts.flatMap(d=>d.polygon.map(p=>p[0])));
assert.ok(west(pair['outside-walls'])<west(medieval));assert.ok(west(pair.modern)<west(pair['outside-walls']));

assert.throws(()=>compileIndependentLaterSkeleton(data,'aelia',{lat:0,lon:0}));
for(const mutate of [d=>d.phases.aelia.roads[0].id='',d=>d.phases.aelia.roads[0].sources=[],d=>d.phases.aelia.roads[0].points=[[0,0],[0,0]],d=>d.phases.aelia.districts[0].polygon=[[0,0],[1,0],[2,0]]]){const bad=structuredClone(data);mutate(bad);assert.throws(()=>compileIndependentLaterSkeleton(bad,'aelia',data.origin));}
const failed=new THREE.Group();assert.throws(()=>buildIndependentLaterSkeleton(failed,compileIndependentLaterSkeleton(data,'aelia',data.origin),materials,{heightAtWorld:()=>NaN}));assert.equal(failed.children.length,0);
const neaPublished=core.get('j3k:byzantine:independent:monument:nea-context');assert.ok(neaPublished);assert.deepEqual(neaPublished.lifecycle.events.map(e=>[e.phase,e.state]),[['byzantine','build'],['early-islamic','unresolved']],'next phase is explicitly unknown, not an invented destruction/reuse event');
assert.equal(JSON.stringify(packs),originalData);publisher.dispose();assert.equal(core.objects.size,0);material.dispose();console.log('PASS: eight independent period skeletons, shared origin, roads/reservations constrain coarse cells, DEM-following caps, distinct phase IDs, evidence return, exact rebuild, malformed source/geometry rejection and owned cleanup');

const aqsaIds=[];
for(const phase of phases.map(p=>p.id)){
 const record=aqsaCore(phase),expected=['early-islamic','crusader','ayyubid-mamluk','ottoman','outside-walls','modern'].includes(phase);
 assert.equal(Boolean(record),expected,'Aqsa must not appear before its Islamic context');if(!record)continue;
 aqsaIds.push(record.id);assert.deepEqual(record.metadata.mainHallMetres,{width:50,length:80,authority:'present-main-hall-reference-not-phase-survey'});assert.equal(record.metadata.wholePhaseSimultaneity,false);assert.equal(record.metadata.geometryVerified,false);assert.deepEqual(record.metadata.modelAnchor,{x:35,z:220});
 const geometry=sacredCoreGeometry(record,terrain),p=geometry.attributes.position,n=geometry.attributes.normal;let upwardRoof=0,pitchedRoof=0;
 for(let i=0;i<p.count;i++){assert.ok(pointInPolygon({x:p.getX(i),z:p.getZ(i)},record.geometry.polygon),'whole landmark must stay inside its reserved envelope');if(n.getY(i)>.1&&n.getY(i)<.99){upwardRoof++;if(Math.abs(Math.abs(p.getZ(i)-220)-40)<1e-4)pitchedRoof++;}}
 assert.ok(upwardRoof>50,'dome must face the viewer rather than disappear from above');assert.ok(pitchedRoof>=12,'pitched roof surfaces must face upward independently of dome normals');geometry.dispose();
 if(phase==='early-islamic'){assert.equal(record.metadata.eastRecess,false);assert.ok(record.metadata.referencePeriod.includes('Fatimid'));}else assert.equal(record.metadata.eastRecess,true);
}
assert.equal(new Set(aqsaIds).size,6,'each selected era retains a separate model identity without claiming fabric inheritance');

for(const phase of phases.map(p=>p.id)){
 const nea=neaCore(phase);assert.equal(Boolean(nea),phase==='byzantine','a selected post-543 model must not appear in earlier or later phases');if(!nea)continue;
 assert.deepEqual(nea.metadata.mainChurchMetres,{length:115,width:57,authority:'published-excavation-overview-reference-not-digitized-plan'});assert.equal(nea.metadata.approachAxis,'western');assert.equal(nea.metadata.geometryVerified,false);assert.equal(nea.metadata.wholePhaseSimultaneity,false);assert.ok(nea.metadata.referencePeriod.includes('post-543'));
 const g=sacredCoreGeometry(nea,terrain),a=g.attributes.position,n=g.attributes.normal;let pitched=0;
 for(let i=0;i<a.count;i++){assert.ok(pointInPolygon({x:a.getX(i),z:a.getZ(i)},nea.geometry.polygon),'Nea assembly and forecourt must fit the reserved envelope');if(n.getY(i)>.1&&n.getY(i)<.99&&Math.abs(a.getX(i)-(-372.5))<1e-4)pitched++;}
 assert.ok(pitched>=4,'central roof must have upward-facing slopes');g.dispose();
}
