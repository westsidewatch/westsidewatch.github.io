import * as THREE from 'three';
import {cityObjectIdForMesh} from './city-lifecycle-projection.js';
// Presentation roles only: no new street ranking, walls, certainty or geometry.
export function cityVisualRole(record,mesh){
 if(!record)return null;
 if(mesh.userData.extentReconstruction||mesh.userData.defenseMode==='candidate'||record.confidence==='disputed')return 'uncertain';
 if(mesh.userData.heritageComponent==='western-market')return 'housing';
 if(record.type==='wall'||record.type==='gate')return 'defense';
 if(record.type==='road'||record.type==='route')return 'road';
 if(record.type==='monument')return 'core';
 if(mesh.userData.overview||['building','block'].includes(record.type))return 'housing';
 return null;
}
export function hierarchyColor(color,role,confidence){
 if(role==='uncertain')return color.clone();
 const c=color.clone(),hsl={};c.getHSL(hsl);let l=hsl.l;
 if(role==='housing')l+=.28*(1-l);
 if(role==='road')l+=.58*(1-l);
 if(role==='connector')l*=.55;
 if(role==='defense')l*=confidence==='inferred'?.78:.62;
 if(role==='core')l*=.88;
 return c.setHSL(hsl.h,hsl.s,THREE.MathUtils.clamp(l,0,1));
}
export function createCityVisualHierarchy({root,getRecord}){
 const bases=new Map(),variants=new Map(),originals=new Map(),owned=new Set();let enabled=true,stats={};
 function styled(material,role,confidence,damage=0){
  if(!material?.color)return material;
  if(material.userData.j3kVisualHierarchy&&material.userData.j3kVisualHierarchy.damage===damage)return material;
  if(material.userData.j3kVisualHierarchy)material=bases.get(material.userData.j3kVisualHierarchy.base)||material;
  bases.set(material.uuid,material);const key=`${material.uuid}:${role}:${confidence}:${damage}`;
  if(!variants.has(key)){
   const copy=material.clone();copy.onBeforeCompile=material.onBeforeCompile;copy.customProgramCacheKey=material.customProgramCacheKey.bind(material);
   copy.userData.j3kVisualHierarchy={base:material.uuid,role,confidence,damage};variants.set(key,copy);owned.add(copy);
  }
  return variants.get(key);
 }
 function apply(phase){
  const counts={housing:0,road:0,defense:0,core:0,uncertain:0},ids={housing:new Set(),road:new Set(),defense:new Set(),core:new Set(),uncertain:new Set()},updated=new Set();let suppressedShadows=0,emphasizedOuterRoadMeshes=0;
  root.traverse(mesh=>{
   if(!mesh.isMesh||mesh.userData.displayAnnotation)return;for(let p=mesh;p;p=p.parent)if(!p.visible)return;
   const id=cityObjectIdForMesh(mesh),record=id&&getRecord(id),role=cityVisualRole(record,mesh);if(!role)return;
   counts[role]++;ids[role].add(id);if(role==='uncertain')return;
   if(!originals.has(mesh))originals.set(mesh,{material:mesh.material,castShadow:mesh.castShadow});
   if(enabled&&mesh.userData.outerConnectionContext)emphasizedOuterRoadMeshes++;
   const original=originals.get(mesh);mesh.castShadow=role==='housing'&&enabled?false:original.castShadow;if(role==='housing'&&enabled&&original.castShadow)suppressedShadows++;
   const ruinPhase=['babylonian-destruction','roman-destruction'].includes(phase),factor=mesh.userData.cityRuinFactor??mesh.userData.factor??1,damage=ruinPhase&&['housing','core'].includes(role)?Math.round(Math.max(0,Math.min(1,1-factor))*4)/4:0;
   mesh.material=Array.isArray(mesh.material)?mesh.material.map(m=>styled(m,mesh.userData.outerConnectionContext?'connector':role,record.confidence,damage)):styled(mesh.material,mesh.userData.outerConnectionContext?'connector':role,record.confidence,damage);
   for(const material of Array.isArray(mesh.material)?mesh.material:[mesh.material]){
    if(updated.has(material))continue;updated.add(material);const tag=material.userData.j3kVisualHierarchy,base=tag&&bases.get(tag.base);if(!base?.color)continue;
    material.color.copy(enabled?hierarchyColor(base.color,tag.role,tag.confidence):base.color);if(enabled&&tag.damage)material.color.multiplyScalar(1-.5*tag.damage);
   }
  });
  stats={phase,enabled,meshes:counts,objects:Object.fromEntries(Object.entries(ids).map(([k,v])=>[k,v.size])),suppressedHousingShadows:suppressedShadows,emphasizedOuterRoadMeshes,ownedMaterialVariants:owned.size,geometryChanged:false,evidenceReclassified:false,missingGeometryAdded:false,historicalGeometryAccepted:false};return stats;
 }
 return {apply,set(value){enabled=Boolean(value);return enabled;},diagnostics:()=>structuredClone(stats),dispose(){for(const [mesh,o]of originals){mesh.material=o.material;mesh.castShadow=o.castShadow;}for(const m of owned)m.dispose();originals.clear();bases.clear();variants.clear();owned.clear();}};
}
