import * as THREE from 'three';
import {cityObjectIdForMesh} from './city-lifecycle-projection.js';
import {housingFitsRing} from './housing-boundary.js';
import {clipBlockToEnvelope} from './district-infill.js';
const area=p=>Math.abs(p.reduce((s,a,i)=>{const b=p[(i+1)%p.length];return s+a.x*b.z-b.x*a.z;},0))/2;
const visible=o=>{for(let p=o;p;p=p.parent)if(!p.visible)return false;return true;};
// Read-only inspection of actual visible physical masses, including public cores.
// Gates/walls can straddle the perimeter; source zones/annotations are not houses.
export function createCityEnclosureAudit({root,core,boundaryFor}){
 const footprints=new WeakMap();
 function triangles(mesh){const transform=mesh.matrixWorld.elements.join(',');let cached=footprints.get(mesh);if(cached?.transform===transform)return cached.triangles;let result;const p=mesh.geometry.attributes.position,index=mesh.geometry.index,v=new THREE.Vector3();result=[];
  for(let i=0;i<(index?.count||p.count);i+=3){const poly=[];for(let j=0;j<3;j++){v.fromBufferAttribute(p,index?index.getX(i+j):i+j).applyMatrix4(mesh.matrixWorld);poly.push({x:v.x,z:v.z});}if(area(poly)>1e-5)result.push(poly);}
  footprints.set(mesh,{transform,triangles:result});return result;
 }
 return {snapshot(){const boundary=boundaryFor();root.updateMatrixWorld(true);const groups=new Map();
  root.traverse(mesh=>{if(!mesh.isMesh||!visible(mesh)||mesh.userData.displayAnnotation)return;const record=core.get(cityObjectIdForMesh(mesh));if(!record||!['building','block','monument'].includes(record.type))return;
   if(!groups.has(record.id))groups.set(record.id,{record,meshes:[],bounds:new THREE.Box3()});const g=groups.get(record.id);g.meshes.push(mesh);g.bounds.expandByObject(mesh);
  });
  const violations=[],exceptions=[];let inside=0,unresolved=0;
  for(const {record,meshes,bounds}of groups.values()){
   const district=core.get(record.source?.districtId||record.metadata?.districtId),expansion=boundary.allowsExpansion&&district?.metadata.layoutRole==='extra-mural-expansion';
   if(expansion){exceptions.push({id:record.id,reason:'explicit-dated-extramural-expansion'});continue;}
   if(!boundary.rings.length){unresolved++;continue;}
   const box=[{x:bounds.min.x,z:bounds.min.z},{x:bounds.max.x,z:bounds.min.z},{x:bounds.max.x,z:bounds.max.z},{x:bounds.min.x,z:bounds.max.z}];
   if(boundary.rings.some(r=>housingFitsRing(box,r,0))){inside++;continue;}
   let total=0,outside=0;
   for(const polygon of meshes.flatMap(triangles)){const a=area(polygon);total+=a;if(boundary.rings.some(r=>housingFitsRing(polygon,r,0)))continue;const clipped=boundary.rings.flatMap(r=>clipBlockToEnvelope(polygon,r,{minArea:1e-8}));outside+=Math.max(0,a-clipped.reduce((s,p)=>s+area(p),0));}
   if(outside>.1)violations.push({id:record.id,type:record.type,label:record.metadata.name||record.source?.label||record.id,projectedArea:total,outsideArea:outside,outsideFraction:outside/total});else inside++;
  }
  return {phase:boundary.phaseId,basis:boundary.basis,closedRings:boundary.rings.length,inside,unresolved,exceptions,violations,examined:groups.size,historicalGeometryAccepted:false,scope:'actual-visible-housing-and-public-masses; gates/walls and explicit suburbs separate'};
 }};
}
