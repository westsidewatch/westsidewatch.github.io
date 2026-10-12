import assert from 'node:assert/strict';
import * as THREE from 'three';
import {readFileSync} from 'node:fs';
import {compilePeriodRegistration} from '../preview/jerusalem-3000/period-spatial-registration.js';
import {buildEraParcelCore} from '../preview/jerusalem-3000/herodian-parcel-core.js';
import {TemporalCityCore} from '../preview/jerusalem-3000/temporal-city-core.js';
import {polygonsOverlap} from '../preview/jerusalem-3000/urban-exclusion.js';
import {roadClearancePolygons} from '../preview/jerusalem-3000/district-infill.js';
import {fitCityOverview} from '../preview/jerusalem-3000/city-overview.js';
const data=JSON.parse(readFileSync(new URL('../preview/jerusalem-3000/data/urban/first-temple-persian.spatial.v1.json',import.meta.url)));
const inside=(p,poly)=>{let hit=false;for(let i=0,j=poly.length-1;i<poly.length;j=i++){const a=poly[i],b=poly[j];if((a.z>p.z)!==(b.z>p.z)&&p.x<(b.x-a.x)*(p.z-a.z)/(b.z-a.z)+a.x)hit=!hit;}return hit;};
const distance=(p,a,b)=>{const dx=b.x-a.x,dz=b.z-a.z,t=Math.max(0,Math.min(1,((p.x-a.x)*dx+(p.z-a.z)*dz)/(dx*dx+dz*dz)));return Math.hypot(p.x-a.x-dx*t,p.z-a.z-dz*t);};
for(const phase of Object.keys(data.phases)){
 const registration=compilePeriodRegistration(data,phase,data.anchor),reserved=[...registration.reservations,...roadClearancePolygons(registration.roads,6)],all=[];
 const make=()=>new TemporalCityCore({phases:[{id:phase}]});const core=make(),other=make();
 for(const district of registration.districts){
  const opts={phaseId:phase,registration,districtId:district.id,exclusions:registration.reservations};
  const result=buildEraParcelCore(core,{},opts),repeated=buildEraParcelCore(other,{},opts);
  assert.deepEqual(result.parcels,repeated.parcels,'deterministic subdivision and IDs');assert.ok(result.count>0);
  for(const parcel of result.parcels){
   for(let i=0;i<parcel.geometry.polygon.length;i++){const a=parcel.geometry.polygon[i],b=parcel.geometry.polygon[(i+1)%parcel.geometry.polygon.length];for(const t of [0,.25,.5,.75])assert.ok(inside({x:a.x+(b.x-a.x)*t,z:a.z+(b.z-a.z)*t},district.geometry.polygon),'parcel edges must remain inside concave district');}
   assert.ok(reserved.every(zone=>!polygonsOverlap(parcel.geometry.polygon,zone.polygon)),'housing must leave sacred and road clearance');
  }
  if(district.id.endsWith('western-hill')){
   const centres=result.parcels.map(p=>({x:p.geometry.polygon.reduce((s,v)=>s+v.x,0)/p.geometry.polygon.length,z:p.geometry.polygon.reduce((s,v)=>s+v.z,0)/p.geometry.polygon.length}));
   const interior=centres.filter(p=>registration.roads.every(r=>r.geometry.points.slice(1).every((b,i)=>distance(p,r.geometry.points[i],b)>45)));
   assert.ok(interior.length>20,'infill must populate western interior, beyond former short street-front ribbons');
  }
  all.push(...result.parcels);
 }
 for(let i=0;i<all.length;i++)for(let j=i+1;j<all.length;j++)assert.ok(!polygonsOverlap(all[i].geometry.polygon,all[j].geometry.polygon),'district and internal parcels must not overlap');
 assert.ok(core.validate().ok);
 const points=registration.districts.flatMap(d=>d.geometry.polygon.flatMap(p=>[new THREE.Vector3(p.x,50,p.z),new THREE.Vector3(p.x,82,p.z)]));
 for(const aspect of [1.77,.55]){
  const framing=fitCityOverview({points,aspect}),camera=new THREE.PerspectiveCamera(34,aspect,.1,18000);camera.position.copy(framing.position);camera.lookAt(framing.target);camera.updateMatrixWorld();
  for(const point of points){const projected=point.clone().project(camera);assert.ok(Math.abs(projected.x)<.85&&projected.y>-.35&&projected.y<.8,'period envelope must fit above caption on desktop and portrait');}
 }
}
assert.throws(()=>fitCityOverview({points:[],aspect:1}));
console.log('PASS: interior infill, deterministic IDs, concave containment, parcel/road/sanctuary clearance and aspect-aware overview');
