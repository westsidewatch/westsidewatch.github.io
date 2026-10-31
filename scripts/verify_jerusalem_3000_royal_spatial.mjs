import {loadAnchorCityLedger} from '../preview/jerusalem-3000/anchor-ledger-loader.js';
import assert from 'node:assert/strict';
import * as THREE from 'three';
import {readFile} from 'node:fs/promises';
import {compileRoyalSpatialLayout} from '../preview/jerusalem-3000/royal-spatial-layout.js';
import {polygonsOverlap} from '../preview/jerusalem-3000/urban-exclusion.js';
import {createRoyalCity} from '../preview/jerusalem-3000/royal-city.js';
import {loadTemporalCityCore} from '../preview/jerusalem-3000/temporal-city-core-adapter.js';
import {invalidateCityData} from '../preview/jerusalem-3000/city-data-loader.js';
const base=new URL('../preview/jerusalem-3000/',import.meta.url),json=async p=>JSON.parse(await readFile(new URL(p,base)));
const data=await json('data/settlement/david-solomon.v1.json'),timeline=await json('data/continuous-build-timeline.json'),layout=compileRoyalSpatialLayout(data);
assert.equal(layout.regions.length,2);
for(const [x,z] of data.houseOffsets)for(const [dx,dz] of [[-5.25,-6.75],[5.25,-6.75],[-5.25,6.75],[5.25,6.75]])assert.ok(polygonsOverlap([{x:x+dx-.001,z:z+dz-.001},{x:x+dx+.001,z:z+dz-.001},{x:x+dx+.001,z:z+dz+.001},{x:x+dx-.001,z:z+dz+.001}],layout.regions[0].polygon.map(([x,z])=>({x,z}))),'dwelling outside ridge envelope');
assert.ok(layout.reachable('david').includes('david-court'));assert.ok(!layout.reachable('david').includes('temple-entry'));assert.ok(layout.reachable('solomon').includes('temple-entry'));
const broken=structuredClone(data);broken.royalCity.spatial.edges=broken.royalCity.spatial.edges.filter(e=>e.id!=='gate-to-ridge');assert.throws(()=>compileRoyalSpatialLayout(broken),/Disconnected/);
const badGate=structuredClone(data);badGate.royalCity.spatial.gates[0].t=.001;assert.throws(()=>compileRoyalSpatialLayout(badGate),/Gate/);
const premature=structuredClone(data);premature.royalCity.spatial.nodes.find(n=>n.id==='northern-gate').stage='david';assert.throws(()=>compileRoyalSpatialLayout(premature),/stage/);
const badFrame=structuredClone(data);badFrame.royalCity.spatial.frame='degrees';assert.throws(()=>compileRoyalSpatialLayout(badFrame),/frame/);
const moved=structuredClone(data);moved.royalCity.davidWall[2][0]-=2;assert.notDeepEqual(compileRoyalSpatialLayout(moved).nodes.find(n=>n.id==='east-gate').offset,layout.nodes.find(n=>n.id==='east-gate').offset,'gate and road endpoint follow common wall parameters');
const rect=(x,z,w,d)=>[{x:x-w/2,z:z-d/2},{x:x+w/2,z:z-d/2},{x:x+w/2,z:z+d/2},{x:x-w/2,z:z+d/2}];
for(const e of layout.edges)for(let i=1;i<e.points.length;i++){
 const a=e.points[i-1],b=e.points[i],len=Math.hypot(b[0]-a[0],b[1]-a[1]),nx=-(b[1]-a[1])/len*layout.roadWidth/2,nz=(b[0]-a[0])/len*layout.roadWidth/2;
 const road=[{x:a[0]+nx,z:a[1]+nz},{x:b[0]+nx,z:b[1]+nz},{x:b[0]-nx,z:b[1]-nz},{x:a[0]-nx,z:a[1]-nz}];
 for(const [x,z] of data.houseOffsets)assert.ok(!polygonsOverlap(road,rect(x,z,data.houseDimensions[0]+.5,data.houseDimensions[1]+.5)),`${e.id} crosses dwelling ${x},${z}`);
}
const original=globalThis.fetch;
try {
 globalThis.fetch=async url=>({ok:true,json:()=>json(url)});invalidateCityData();
 const terrain={grid:{origin:{lat:31.778,lon:35.235}},heightAtWorld:()=>40},{core}=await loadTemporalCityCore(timeline.phases,{terrain}),parent=new THREE.Group();
 const rawAnchor=await json('data/anchor-era-packs.json');assert.ok(!rawAnchor.packs.flatMap(p=>p.objects||[]).some(o=>o.id==='j3k:object:royal-road:spring-access'),'spatial records must not be duplicated in editable anchor packs');
 const [a,b]=await Promise.all([loadAnchorCityLedger(),loadAnchorCityLedger()]);assert.equal(a.lifecycle.objects.length,b.lifecycle.objects.length);assert.equal(a.lifecycle.objects.filter(o=>o.id==='j3k:object:royal-road:spring-access').length,1);
 const runtime=createRoyalCity(parent,{data,terrain,core});assert.equal(core.get('j3k:object:royal-region:ridge').geometry.frame,'canonical-dem-enu');assert.equal(core.get('j3k:object:royal-road:spring-access').metadata.spatialTopology.from,'spring');runtime.apply({position:3.9,evidenceAllowed:()=>true});
 const parts=parent.children[0].children,roads=parts.filter(m=>m.userData.cityObject.kind==='city-road'),obstacles=parts.filter(m=>m.userData.cityObject.kind!=='city-road'&&m.userData.cityObject.role!=='walkable-floor'&&!m.userData.cityObject.componentId.endsWith('lintel'));
 for(const road of roads){const p=road.geometry.attributes.position;assert.ok(road.geometry.attributes.normal.getY(0)>0);for(let i=0;i<p.count;i+=3){const triangle=[0,1,2].map(k=>({x:p.getX(i+k),z:p.getZ(i+k)}));for(const obstacle of obstacles){const b=new THREE.Box3().setFromObject(obstacle);assert.ok(!polygonsOverlap(triangle,rect((b.min.x+b.max.x)/2,(b.min.z+b.max.z)/2,b.max.x-b.min.x,b.max.z-b.min.z)),`${road.userData.cityObject.componentId} crosses ${obstacle.userData.cityObject.componentId}`);}}}
 assert.equal(runtime.diagnostics().visibleGates,9);assert.equal(runtime.diagnostics().visibleRoads,layout.edges.length);
 runtime.apply({position:3.2,evidenceAllowed:()=>true});assert.equal(runtime.diagnostics().visibleGates,6);assert.ok(runtime.diagnostics().visibleRoads<layout.edges.length);
 runtime.apply({position:4.9,evidenceAllowed:()=>true});assert.equal(runtime.diagnostics().visibleGates,0);assert.equal(runtime.diagnostics().visibleRoads,0,'later route continuity is not presumed');
 runtime.dispose();console.log('PASS: connected staged destinations, derived gateway/entrance endpoints, dwelling/wall/monument clearance and lifecycle binding');
} finally {globalThis.fetch=original;invalidateCityData();}
