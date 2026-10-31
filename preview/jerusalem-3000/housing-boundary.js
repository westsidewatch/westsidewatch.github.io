import * as THREE from 'three';
import {pointInPolygon} from './urban-exclusion.js';
import {geographicToENU} from './terrain-runtime.js';
import {cityObjectIdForMesh} from './city-lifecycle-projection.js';
const same=(a,b)=>Math.hypot(a.x-b.x,a.z-b.z)<.01;
const cross=(a,b,c)=>(b.x-a.x)*(c.z-a.z)-(b.z-a.z)*(c.x-a.x);
// Join only matching authored endpoints. Never invent a closing wall across a gap.
export function closedHousingRings(paths){
 const remaining=paths.map(p=>p.map(q=>({...q}))),rings=[];
 while(remaining.length){
  let chain=remaining.shift(),changed=true;
  while(!same(chain[0],chain.at(-1))&&changed){
   changed=false;
   for(let i=0;i<remaining.length;i++){
    const p=remaining[i];
    if(same(chain.at(-1),p[0]))chain.push(...p.slice(1));
    else if(same(chain.at(-1),p.at(-1)))chain.push(...p.slice(0,-1).reverse());
    else if(same(chain[0],p.at(-1)))chain=[...p.slice(0,-1),...chain];
    else if(same(chain[0],p[0]))chain=[...p.slice(1).reverse(),...chain];
    else continue;
    remaining.splice(i,1);changed=true;break;
   }
  }
  if(chain.length>=4&&same(chain[0],chain.at(-1)))rings.push(chain.slice(0,-1));
 }
 return rings;
}

function segmentDistance(p,a,b){const dx=b.x-a.x,dz=b.z-a.z,l=dx*dx+dz*dz,t=l?Math.max(0,Math.min(1,((p.x-a.x)*dx+(p.z-a.z)*dz)/l)):0;return Math.hypot(p.x-a.x-t*dx,p.z-a.z-t*dz);}
export function housingFitsRing(polygon,ring,clearance=2){
 if(polygon.length<3||!polygon.every(p=>pointInPolygon(p,ring)))return false;
 for(let i=0;i<polygon.length;i++){const a=polygon[i],b=polygon[(i+1)%polygon.length];for(let j=0;j<ring.length;j++){const c=ring[j],d=ring[(j+1)%ring.length];if(cross(a,b,c)*cross(a,b,d)<0&&cross(c,d,a)*cross(c,d,b)<0)return false;if(Math.min(segmentDistance(a,c,d),segmentDistance(b,c,d),segmentDistance(c,a,b),segmentDistance(d,a,b))<clearance-1e-5)return false;}}
 return true;
}
export function housingBoundaryAt({phaseId,offset,defenseData,wallReference,royalData,royalStage,origin}){
 const source=defenseData.phases.find(p=>p.id===phaseId);let rings=[],basis='no-closed-circuit-available';
 if(phaseId==='david-solomon'){
  const a=geographicToENU(royalData.spring.lat,royalData.spring.lon,origin),convert=path=>path.map(([x,z])=>({x:a.east+x,z:-a.north+z}));
  // The northern extension replaces the shared northern edge of the David enclosure.
  const path=royalStage==='solomon'?[...royalData.royalCity.northernWall,...royalData.royalCity.davidWall.slice(2)]:royalData.royalCity.davidWall;
  rings=closedHousingRings([convert(path)]);basis='existing-royal-authored-enclosure';
 }else if(['ottoman','outside-walls','modern'].includes(phaseId)){rings=[wallReference.envelope];basis='existing-modern-wall-reference-envelope';}
 else if(source?.owner==='network'){
  const active=w=>offset>=w.fromOffset&&offset<w.toOffset,paths=[...source.walls.filter(active).map(w=>defenseData.families[w.family].points),...(source.extentReconstructions||[]).filter(active).map(w=>defenseData.extentReconstructions[w.key].points)];
  rings=closedHousingRings(paths.map(path=>path.map(([x,z])=>({x,z}))));if(rings.length)basis='existing-authored-defense-circuit';
 }
 return {phaseId,rings,basis,clearance:2,geometryVerified:false,historicalCircuitVerified:false,allowsExpansion:['outside-walls','modern'].includes(phaseId)};
}
// Final admission guard shared by all four housing renderers. Withheld illustrative
// housing stays in the source ledger; it is never moved or relabelled as a suburb.
export function createHousingBoundaryAdmission({root,core,boundaryFor}){
 const masked=new Set(),meshFootprints=new WeakMap(),decisions=new Map(),boundaryIds=new Map();let stats=null;
 function restore(){for(const m of masked){m.visible=true;delete m.userData.housingBoundaryWithheld;}masked.clear();}
 function footprint(mesh){
  let polygons=meshFootprints.get(mesh);if(polygons)return polygons;
  const a=mesh.geometry.attributes.position,index=mesh.geometry.index,v=new THREE.Vector3();polygons=[];
  // Inspect projected surface triangles, not a convex hull that bridges an empty
  // courtyard or an inward bend in a wall-aligned block. Vertical faces vanish.
  for(let i=0;i<(index?.count||a.count);i+=3){const polygon=[];for(let j=0;j<3;j++){v.fromBufferAttribute(a,index?index.getX(i+j):i+j).applyMatrix4(mesh.matrixWorld);polygon.push({x:v.x,z:v.z});}if(Math.abs(cross(...polygon))>1e-5)polygons.push(polygon);}
  meshFootprints.set(mesh,polygons);return polygons;
 }
 function apply(){
  const boundary=boundaryFor();if(!boundary)return;root.updateMatrixWorld(true);const groups=new Map(),shapeKey=JSON.stringify([boundary.phaseId,boundary.rings]);if(!boundaryIds.has(shapeKey))boundaryIds.set(shapeKey,boundaryIds.size);const key=boundaryIds.get(shapeKey);
  root.traverse(mesh=>{if(!mesh.isMesh||!mesh.userData.overview)return;for(let p=mesh;p;p=p.parent)if(!p.visible)return;const id=cityObjectIdForMesh(mesh),record=id&&core.get(id);if(!record||!['building','block'].includes(record.type))return;if(!groups.has(id))groups.set(id,{id,record,meshes:[]});groups.get(id).meshes.push(mesh);});
  let admitted=0,withheld=0,expansion=0,unresolved=0;const withheldIds=[];
  for(const g of groups.values()){
   const districtId=g.record.source?.districtId||g.record.metadata?.districtId,district=districtId&&core.get(districtId),explicitExpansion=boundary.allowsExpansion&&district?.metadata?.layoutRole==='extra-mural-expansion';
   if(explicitExpansion){expansion++;continue;}if(!boundary.rings.length){unresolved++;continue;}
   const cacheKey=key+'|'+g.id+'|'+g.meshes.map(m=>m.geometry.uuid).join(',' );let fits=decisions.get(cacheKey);
   if(fits===undefined){const polygons=g.meshes.flatMap(footprint);fits=polygons.length>0&&polygons.every(p=>boundary.rings.some(r=>housingFitsRing(p,r,boundary.clearance)));decisions.set(cacheKey,fits);}
   if(fits)admitted++;else{withheld++;withheldIds.push(g.id);for(const mesh of g.meshes){mesh.visible=false;mesh.userData.housingBoundaryWithheld=true;masked.add(mesh);}}
  }
  stats={phase:boundary.phaseId,basis:boundary.basis,closedRings:boundary.rings.length,admitted,withheld,explicitExpansion:expansion,unresolved,withheldIds,clearanceMetres:boundary.clearance,historicalCircuitVerified:false,policy:'withhold-outside-housing-do-not-relocate-or-invent-suburbs'};
 }
 function snapshot({includeFootprints=false,includeIds=true}={}){
  if(!stats)return null;const result=structuredClone(stats);if(!includeIds)delete result.withheldIds;if(!includeFootprints)return result;
  const boundary=boundaryFor(),footprints=[];root.updateMatrixWorld(true);root.traverse(mesh=>{if(!mesh.isMesh||!mesh.userData.overview)return;for(let p=mesh;p;p=p.parent)if(!p.visible)return;const id=cityObjectIdForMesh(mesh),record=id&&core.get(id);if(!record||!['building','block'].includes(record.type))return;const district=core.get(record.source?.districtId||record.metadata?.districtId);footprints.push({id,polygons:footprint(mesh),explicitExpansion:boundary.allowsExpansion&&district?.metadata?.layoutRole==='extra-mural-expansion'});});return {...result,rings:structuredClone(boundary.rings),visibleFootprints:footprints};
 }
 return {restore,apply,snapshot};
}
