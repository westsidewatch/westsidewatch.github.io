import assert from 'node:assert/strict';
import fs from 'node:fs';
import * as THREE from 'three';
import {compileIndependentLaterSkeleton,buildIndependentLaterSkeleton} from '../preview/jerusalem-3000/independent-later-skeleton.js';
const rows=[],terrain={heightAtWorld:()=>100},material=new THREE.MeshStandardMaterial();
for(const pack of ['roman-byzantine-islamic','medieval-ottoman','expansion-modern']){
 const data=JSON.parse(fs.readFileSync(new URL(`../preview/jerusalem-3000/data/urban/${pack}.skeleton.v1.json`,import.meta.url))),snapshot=JSON.stringify(data);
 for(const phase of Object.keys(data.phases)){
  const r=compileIndependentLaterSkeleton(data,phase,data.origin),audit=r.precinctReservationAudit;
  assert.equal(audit.rows.length,data.phases[phase].reservations.length);
  assert.equal(audit.historicalLandUseVerified,false);
  assert.equal(r.reservations.length+r.planningReservations.length,audit.rows.length);
  for(const p of r.planningReservations){assert.equal(p.metadata.planningOnly,true);assert.equal(p.metadata.spatialExclusionVerified,false);assert.ok(!r.reservations.some(a=>a.id===p.id));}
  for(const p of r.reservations){assert.equal(p.metadata.groundRole,'public-context');assert.deepEqual(p.metadata.sourcePlanningPolygon,data.phases[phase].reservations.find(a=>p.id.endsWith(':'+a.id)).polygon.map(([x,z])=>({x,z})));}
  const runtime=buildIndependentLaterSkeleton(new THREE.Group(),r,{inferred:material},terrain);
  const before={...r,reservations:[...r.reservations,...r.planningReservations]};
  const old=buildIndependentLaterSkeleton(new THREE.Group(),before,{inferred:material},terrain);
  const blocks=x=>x.ledgerRecords.filter(q=>q.type==='block').length;
  if(r.planningReservations.length)assert.ok(blocks(runtime)>blocks(old),'releasing unlocated programme must restore actual geometry, not just recolour terrain');
  rows.push({phase,...audit,planning:r.planningReservations.length,blocks:blocks(runtime),blocksWithUnlocatedExclusions:blocks(old)});
  for(const x of [runtime,old]){x.meshes.forEach(m=>m.geometry.dispose());x.disposeMaterials();}
 }
 assert.equal(JSON.stringify(data),snapshot,'authored source vectors must remain unchanged');
}
material.dispose();assert.equal(rows.length,8);console.log(JSON.stringify(rows,null,2));console.log('PASS:8 later periods fully account original reservations; unlocated programmes preserved without sterilising real neighbourhoods; public envelopes protected and source data immutable');
