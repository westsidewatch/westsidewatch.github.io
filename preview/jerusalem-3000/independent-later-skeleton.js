import {residentialEraProfile} from './residential-era-profiles.js';
import {registerLandmarkApproaches} from './landmark-approaches.js';
import {terrainResidentialAdmission} from './metric-residential-layout.js';
import {housingFitsRing} from './housing-boundary.js';
import {wallGateApproaches} from './old-city-wall-reference.js';
import {commonCorridorFor} from './shared-urban-places.js';
import {laterSacredCores,sacredCoreGeometry} from './later-sacred-cores.js';
import {overviewHousingGeometry} from './overview-housing.js';
import * as THREE from 'three';
import {generateDistrictInfill,clipBlockToEnvelope} from './district-infill.js';
import {polygonsOverlap} from './urban-exclusion.js';
import {buildHerodianRoadGeometry} from './herodian-road-geometry.js';
const PHASES=new Set(['aelia','byzantine','early-islamic','crusader','ayyubid-mamluk','ottoman','outside-walls','modern']);
export const isIndependentLaterPhase=id=>PHASES.has(id);
export function compileIndependentLaterSkeleton(data,phase,origin,{wallReference=null}={}){
 if(data?.schema!=='j3k.independent-later-skeleton.v1'||data.frame!=='canonical-origin-east-x-south-z-metres'||!PHASES.has(phase)||![origin?.lat,origin?.lon,data.origin?.lat,data.origin?.lon].every(Number.isFinite)||origin?.lat!==data.origin?.lat||origin?.lon!==data.origin?.lon)throw new Error('Independent skeleton origin/schema/phase mismatch');
 const layout=data.phases[phase],ids=new Set();if(!layout?.districts?.length||!layout?.roads?.length)throw new Error('Missing independent later layout');
 const make=(item,type,key,min)=>{if(typeof item.id!=='string'||!item.id)throw new Error('Missing independent feature ID');const id=`j3k:${phase}:independent:${type}:${item.id}`,points=item[key];if(ids.has(id)||!Array.isArray(points)||points.length<min||points.some(p=>!Array.isArray(p)||p.length!==2||!p.every(Number.isFinite)))throw new Error('Invalid independent skeleton feature');if(key==='polygon'&&Math.abs(points.reduce((sum,p,i)=>{const q=points[(i+1)%points.length];return sum+p[0]*q[1]-q[0]*p[1];},0))<2)throw new Error('Degenerate independent polygon');if(key==='points'&&points.every(p=>p[0]===points[0][0]&&p[1]===points[0][1]))throw new Error('Degenerate independent route');const urls=item.sources||layout.sources;if(!Array.isArray(urls)||!urls.length||urls.some(url=>typeof url!=='string'||!url.startsWith('https://')))throw new Error('Missing independent source context');ids.add(id);return {id,type,confidence:'inferred',geometry:{frame:'canonical-dem-enu',status:'independent-design-not-surveyed',primitive:key==='polygon'?'polygon':'polyline',[key]:points.map(([x,z])=>({x,z}))},source:{authority:data.authority,urls:[...urls],limitations:[...data.limitations]},metadata:{independentSpatialSkeleton:true,...(item.layoutRole?{layoutRole:item.layoutRole}:{})}};};
 const cores=laterSacredCores(phase);
 const roads=layout.roads.map(r=>{const record=make(r,'road','points',2),corridor=commonCorridorFor(phase,r.id);if(corridor){record.geometry.points=corridor.points;record.geometry.status='shared-illustrative-corridor-not-surveyed-road';record.source.urls=[...new Set([...record.source.urls,corridor.source])];record.metadata={...record.metadata,placeId:corridor.placeId,placeRelation:corridor.relation,modernScope:corridor.modernScope};}return record;});
 const generation=data.generation;if(!Number.isFinite(generation?.modelHeight)||generation.modelHeight<=0||generation.modelHeight>12)throw new Error('Invalid coarse model height');
 const registration={phase,authority:data.authority,districts:layout.districts.map(d=>make(d,'district','polygon',3)),roads,reservations:(layout.reservations||[]).map(r=>make(r,'reservation','polygon',3)),cores,generation:{...generation},sources:[...new Set([...layout.sources,...cores.flatMap(c=>c.source.urls),...roads.flatMap(r=>r.source.urls)])],limitations:[...data.limitations,'共同東側通道僅表示歷史軸線的示意位置，不代表鋪面、寬度與標高相同；現代期不代表完整現行道路，部分沿線在1967年已改變。',...(cores.length?['宗教核心為來源支持建築類型的示意量體；座標、尺寸與高程適配未經古建測繪。各期為選定階段概覽，不表示整段年代同時存在，也未證明跨期原構件存續。']:[])]};
 wallGateApproaches(registration,wallReference);registerLandmarkApproaches(registration);return registration;
}
// Coarse terrain-following occupied cells, not architectural buildings.
export function buildIndependentLaterSkeleton(group,registration,materials,terrain){
 const ownedMaterial=materials.inferred.clone();ownedMaterial.opacity=1;ownedMaterial.transparent=false;ownedMaterial.color.setHex(0xb9a27e);const ownedMaterials={...materials,inferred:ownedMaterial};
 const meshes=[],ledgerRecords=[...registration.districts,...registration.roads,...registration.cores],bindingIds=[];
 try{
  for(const district of registration.districts){
   const districtRoads=district.metadata.layoutRole==='old-city-context'?registration.roads.filter(r=>r.metadata.layoutRole==='old-city-route-context'):registration.roads;
   const result=generateDistrictInfill({district,roads:districtRoads,maxBlockArea:registration.generation.maxBlockArea,roadClearance:registration.generation.roadClearance,partitionSeed:'geometry'});
   for(const original of result.blocks){const polygons=registration.occupationEnvelope&&(registration.phase==='ottoman'||district.metadata.layoutRole==='old-city-context')?clipBlockToEnvelope(original.geometry.polygon,registration.occupationEnvelope):[original.geometry.polygon];
   for(const [part,polygon] of polygons.entries()){const block=polygon===original.geometry.polygon?original:{...original,id:`${original.id}:reference-clip:${part}`,geometry:{...original.geometry,polygon},metadata:{...original.metadata,referenceEnvelopeClip:true,originalDesignBlock:original.id}};const occupiedReservations=[...registration.reservations,...registration.cores,...(registration.defenseReservations||[]).map(r=>({geometry:{polygon:r.polygon}}))],legacyRejected=occupiedReservations.some(r=>polygonsOverlap(block.geometry.polygon,r.geometry.polygon));if(!registration.metricResidentialPolicy&&legacyRejected)continue;
    const boundedHousing=registration.housingBoundaryRings?.length&&(registration.phase!=='outside-walls'&&registration.phase!=='modern'||district.metadata.layoutRole==='old-city-context');
    const geometry=overviewHousingGeometry(block.geometry.polygon,terrain,registration.generation.modelHeight,{block:true,planForm:residentialEraProfile(registration.phase).planForms[0],metricPolicy:registration.metricResidentialPolicy,admitPolygon:p=>(!boundedHousing||registration.housingBoundaryRings.some(r=>housingFitsRing(p,r,2)))&&(!registration.metricResidentialPolicy||(!legacyRejected||terrainResidentialAdmission(p,terrain,registration.metricResidentialPolicy).allowed)&&!occupiedReservations.some(r=>polygonsOverlap(p,r.geometry.polygon)))});if(!geometry.attributes.position.count){geometry.dispose();continue;}const mesh=new THREE.Mesh(geometry,ownedMaterial);mesh.receiveShadow=true;mesh.castShadow=true;mesh.userData.overview={grammar:'terrain-courtyard-mass-v1',scope:'visual-modules-of-one-registered-block-not-individual-houses'};mesh.userData.phase2={stage:'coarse-layout-cell',start:0,baseHeight:registration.generation.modelHeight};group.add(mesh);meshes.push(mesh);bindingIds.push(block.id);
    ledgerRecords.push({id:block.id,type:'block',geometry:{...block.geometry,frame:'canonical-dem-enu',status:'independent-coarse-layout-not-buildings'},source:{districtId:district.id,authority:registration.authority,urls:registration.sources},metadata:{...block.metadata,independentSpatialSkeleton:true,modelHeight:registration.generation.modelHeight}});
   }}
  }
  for(const record of registration.cores){const mesh=new THREE.Mesh(sacredCoreGeometry(record,terrain),ownedMaterial);mesh.castShadow=true;mesh.receiveShadow=true;mesh.userData.phase2={stage:'monument',start:0,baseHeight:32};group.add(mesh);meshes.push(mesh);bindingIds.push(record.id);}
  const boundedRoads=registration.occupationEnvelope?registration.roads.filter(r=>registration.phase==='ottoman'||r.metadata.layoutRole==='old-city-route-context'):[],otherRoads=registration.roads.filter(r=>!boundedRoads.includes(r)),exclusions=registration.cores.map(c=>({polygon:c.geometry.polygon}));
  const roads=[...buildHerodianRoadGeometry(group,boundedRoads,ownedMaterials,terrain,{exclusions,envelope:registration.occupationEnvelope}),...buildHerodianRoadGeometry(group,otherRoads,ownedMaterials,terrain,{exclusions})];for(const mesh of roads){mesh.userData.phase2={stage:'road',start:0,baseHeight:.35};meshes.push(mesh);bindingIds.push(mesh.userData.cityObject.objectId);}
  if(meshes.some(mesh=>Array.from(mesh.geometry.attributes.position.array).some(v=>!Number.isFinite(v))))throw new Error('Independent layout outside canonical terrain');
  return {phaseId:registration.phase,meshes,ledgerRecords,bindingIds,grammar:'independent-later-spatial-skeleton-v1',registration,fixedVisibility:true,disposeMaterials(){ownedMaterial.dispose();}};
 }catch(error){for(const mesh of meshes){mesh.removeFromParent();mesh.geometry.dispose();}ownedMaterial.dispose();throw error;}
}
