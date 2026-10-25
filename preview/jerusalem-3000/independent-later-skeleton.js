import * as THREE from 'three';
import {generateDistrictInfill} from './district-infill.js';
import {polygonsOverlap} from './urban-exclusion.js';
import {buildHerodianRoadGeometry} from './herodian-road-geometry.js';
const PHASES=new Set(['aelia','byzantine','early-islamic']);
export const isIndependentLaterPhase=id=>PHASES.has(id);
export function compileIndependentLaterSkeleton(data,phase,origin){
 if(data?.schema!=='j3k.independent-later-skeleton.v1'||data.frame!=='canonical-origin-east-x-south-z-metres'||!PHASES.has(phase)||![origin?.lat,origin?.lon,data.origin?.lat,data.origin?.lon].every(Number.isFinite)||origin?.lat!==data.origin?.lat||origin?.lon!==data.origin?.lon)throw new Error('Independent skeleton origin/schema/phase mismatch');
 const layout=data.phases[phase],ids=new Set();if(!layout?.districts?.length||!layout?.roads?.length)throw new Error('Missing independent later layout');
 const make=(item,type,key,min)=>{if(typeof item.id!=='string'||!item.id)throw new Error('Missing independent feature ID');const id=`j3k:${phase}:independent:${type}:${item.id}`,points=item[key];if(ids.has(id)||!Array.isArray(points)||points.length<min||points.some(p=>!Array.isArray(p)||p.length!==2||!p.every(Number.isFinite)))throw new Error('Invalid independent skeleton feature');if(key==='polygon'&&Math.abs(points.reduce((sum,p,i)=>{const q=points[(i+1)%points.length];return sum+p[0]*q[1]-q[0]*p[1];},0))<2)throw new Error('Degenerate independent polygon');if(key==='points'&&points.every(p=>p[0]===points[0][0]&&p[1]===points[0][1]))throw new Error('Degenerate independent route');const urls=item.sources||layout.sources;if(!Array.isArray(urls)||!urls.length||urls.some(url=>typeof url!=='string'||!url.startsWith('https://')))throw new Error('Missing independent source context');ids.add(id);return {id,type,confidence:'inferred',geometry:{frame:'canonical-dem-enu',status:'independent-design-not-surveyed',primitive:key==='polygon'?'polygon':'polyline',[key]:points.map(([x,z])=>({x,z}))},source:{authority:data.authority,urls:[...urls],limitations:[...data.limitations]},metadata:{independentSpatialSkeleton:true}};};
 const generation=data.generation;if(!Number.isFinite(generation?.modelHeight)||generation.modelHeight<=0||generation.modelHeight>12)throw new Error('Invalid coarse model height');
 return {phase,authority:data.authority,districts:layout.districts.map(d=>make(d,'district','polygon',3)),roads:layout.roads.map(r=>make(r,'road','points',2)),reservations:(layout.reservations||[]).map(r=>make(r,'reservation','polygon',3)),generation:{...generation},sources:[...layout.sources],limitations:[...data.limitations]};
}
function blockGeometry(polygon,terrain,height){
 const area=polygon.reduce((sum,p,i)=>{const q=polygon[(i+1)%polygon.length];return sum+p.x*q.z-q.x*p.z;},0);if(area<0)polygon=[...polygon].reverse();
 const vertices=[],base=polygon.map(p=>terrain.heightAtWorld(p.x,p.z));if(base.some(y=>!Number.isFinite(y)))throw new Error('Independent block outside canonical DEM');
 const push=(i,top)=>vertices.push(polygon[i].x,base[i]+(top?height:.2),polygon[i].z);
 for(const triangle of THREE.ShapeUtils.triangulateShape(polygon.map(p=>new THREE.Vector2(p.x,p.z)),[]))for(const i of [...triangle].reverse())push(i,true);
 for(let i=0;i<polygon.length;i++){const j=(i+1)%polygon.length;for(const [k,top]of [[i,false],[j,true],[j,false],[i,false],[i,true],[j,true]])push(k,top);}
 const geometry=new THREE.BufferGeometry();geometry.setAttribute('position',new THREE.Float32BufferAttribute(vertices,3));geometry.computeVertexNormals();return geometry;
}
// Coarse terrain-following occupied cells, not architectural buildings.
export function buildIndependentLaterSkeleton(group,registration,materials,terrain){
 const ownedMaterial=materials.inferred.clone();ownedMaterial.opacity=1;ownedMaterial.transparent=false;const ownedMaterials={...materials,inferred:ownedMaterial};
 const meshes=[],ledgerRecords=[...registration.districts,...registration.roads],bindingIds=[];
 try{
  for(const district of registration.districts){
   const result=generateDistrictInfill({district,roads:registration.roads,maxBlockArea:registration.generation.maxBlockArea,roadClearance:registration.generation.roadClearance});
   for(const block of result.blocks){if(registration.reservations.some(r=>polygonsOverlap(block.geometry.polygon,r.geometry.polygon)))continue;
    const geometry=blockGeometry(block.geometry.polygon,terrain,registration.generation.modelHeight),mesh=new THREE.Mesh(geometry,ownedMaterial);mesh.receiveShadow=true;mesh.castShadow=true;mesh.userData.phase2={stage:'coarse-layout-cell',start:0,baseHeight:registration.generation.modelHeight};group.add(mesh);meshes.push(mesh);bindingIds.push(block.id);
    ledgerRecords.push({id:block.id,type:'block',geometry:{...block.geometry,frame:'canonical-dem-enu',status:'independent-coarse-layout-not-buildings'},source:{districtId:district.id,authority:registration.authority,urls:registration.sources},metadata:{...block.metadata,independentSpatialSkeleton:true,modelHeight:registration.generation.modelHeight}});
   }
  }
  const roads=buildHerodianRoadGeometry(group,registration.roads,ownedMaterials,terrain);for(const mesh of roads){mesh.userData.phase2={stage:'road',start:0,baseHeight:.35};meshes.push(mesh);bindingIds.push(mesh.userData.cityObject.objectId);}
  if(meshes.some(mesh=>Array.from(mesh.geometry.attributes.position.array).some(v=>!Number.isFinite(v))))throw new Error('Independent layout outside canonical terrain');
  return {phaseId:registration.phase,meshes,ledgerRecords,bindingIds,grammar:'independent-later-spatial-skeleton-v1',registration,fixedVisibility:true,disposeMaterials(){ownedMaterial.dispose();}};
 }catch(error){for(const mesh of meshes){mesh.removeFromParent();mesh.geometry.dispose();}ownedMaterial.dispose();throw error;}
}
