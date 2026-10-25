import {lifecycleStateAtPosition} from './construction-engine.js';
import {allowsEvidence} from './evidence-visibility.js';
const ACTIVE=new Set(['build','rebuild','transform','ruin','expand']);
const FRAMES=new Set(['canonical-dem-enu','scene-local-metres']);
const DOMAINS={districts:['district'],routes:['road','route'],waterDefense:['water','wall','gate'],sacredCivic:['monument']};
export const SKELETON_WINDOW=Object.freeze({minX:-2000,maxX:1100,minZ:-1300,maxZ:1300});
const valid=p=>p&&Number.isFinite(p.x)&&Number.isFinite(p.z);
function planar(record){
 const g=record.geometry||{};if(!FRAMES.has(g.frame)||String(g.status).includes('withheld'))return null;
 const topology=record.metadata?.spatialTopology;
 if(g.polygon?.length>=3&&g.polygon.every(valid))return {kind:'polygon',points:g.polygon};
 const points=g.points||topology?.points;if(points?.length>=2&&points.every(valid))return {kind:'line',points};
 const point=g.point||topology?.point||topology?.center;if(valid(point))return {kind:'point',points:[point]};
 if(g.bounds?.min?.length===3&&g.bounds?.max?.length===3&&[...g.bounds.min,...g.bounds.max].every(Number.isFinite))return {kind:'point',points:[{x:(g.bounds.min[0]+g.bounds.max[0])/2,z:(g.bounds.min[2]+g.bounds.max[2])/2}],bounds:g.bounds};
 if(g.primitive==='box-mass'&&g.position?.length===3&&g.parameters&&[g.position[0],g.position[2],g.parameters.width,g.parameters.depth].every(Number.isFinite))return {kind:'point',points:[{x:g.position[0],z:g.position[2]}],mass:g};
 return null;
}
// Reads existing registrations only. Missing geometry is a gap, never a fabricated road/wall.
export function collectSpatialSkeleton(core,terrain,{phaseId,position,evidenceMode='all',includeRetained=false}){
 if(core.terrain!==terrain||typeof terrain.heightAtWorld!=='function')throw new Error('Skeleton requires canonical shared terrain');
 if(!core.phases.has(phaseId)||!Number.isFinite(position)||[...core.phases.keys()][Math.floor(position)]!==phaseId)throw new Error('Skeleton phase/position mismatch');
 allowsEvidence(evidenceMode,'inferred');
 const timeline={phases:[...core.phases.values()]},features=[],domains=Object.fromEntries(Object.keys(DOMAINS).map(d=>[d,{activeObjects:0,spatialObjects:0,gapIds:[]}])),layoutPoints=[];
 let filtered=0,unresolved=0;
 for(const record of core.phase(phaseId)){
  if(!allowsEvidence(evidenceMode,record.confidence)){filtered++;continue;}
  const state=record.lifecycle.events.length?lifecycleStateAtPosition({lifecycleEvents:record.lifecycle.events},timeline,position):'unresolved';
  if(!ACTIVE.has(state)){unresolved++;continue;}
  if(record.metadata.retainedPhase===phaseId&&!includeRetained)continue;
  if(record.metadata.geometryValidityPhases&&!record.metadata.geometryValidityPhases.includes(phaseId))continue;
  const shape=planar(record),domain=Object.keys(DOMAINS).find(d=>DOMAINS[d].includes(record.type));
  if(domain)domains[domain].activeObjects++;
  if(!shape){if(domain)domains[domain].gapIds.push(record.id);continue;}
  const sampled=shape.points.map(p=>({x:p.x,z:p.z,y:terrain.heightAtWorld(p.x,p.z)}));
  if(sampled.some(p=>!Number.isFinite(p.y))){if(domain)domains[domain].gapIds.push(record.id);continue;}
  if(['block','parcel','building'].includes(record.type)){
   if(shape.bounds){const b=shape.bounds;for(const x of [b.min[0],b.max[0]])for(const z of [b.min[2],b.max[2]])layoutPoints.push({x,z});}
   else if(shape.mass){const g=shape.mass,a=g.rotation?.[1]||0,c=Math.cos(a),s=Math.sin(a);for(const dx of [-g.parameters.width/2,g.parameters.width/2])for(const dz of [-g.parameters.depth/2,g.parameters.depth/2])layoutPoints.push({x:g.position[0]+c*dx+s*dz,z:g.position[2]-s*dx+c*dz});}
   else layoutPoints.push(...shape.points);
  }
  if(domain){domains[domain].spatialObjects++;features.push({id:record.id,domain,kind:domain==='districts'?shape.kind:shape.kind==='polygon'?'polygon':shape.kind,points:sampled,confidence:record.confidence,state,geometryVerified:false,representation:shape.bounds||shape.mass?'model-center-not-footprint':record.geometry.role||'registered-illustration'});}
 }
 const extent=layoutPoints.length?{minX:Math.min(...layoutPoints.map(p=>p.x)),maxX:Math.max(...layoutPoints.map(p=>p.x)),minZ:Math.min(...layoutPoints.map(p=>p.z)),maxZ:Math.max(...layoutPoints.map(p=>p.z)),role:'registered-layout-envelope-not-historical-city-boundary'}:null;
 return {phaseId,position,evidenceMode,window:{...SKELETON_WINDOW},terrain:'modern-dem-rendered-triangles',features,domains,layoutEnvelope:extent,filteredObjects:filtered,unresolvedObjects:unresolved,historicalFoundationAccepted:false};
}
