import * as THREE from 'three';
import {TemporalCityCore} from './temporal-city-core.js';
import {lifecycleStateAt} from './construction-engine.js';
let ownershipSequence=0;
export const residentialOwner=phase=>`generated-residence:${phase}:${++ownershipSequence}`;
// Stage validation before changing the shared ledger. A cancelled builder publishes nothing.
export function publishGeneratedResidentialLedger(ledger,staged,{registration,architecture,generationPhase,destroyedPhase=null,retainedPhase=null,includeRegistration=false,owner}){
 const records=[...staged.objects.values()].filter(r=>['block','parcel','building'].includes(r.type));
 if(!records.length||!owner)throw new Error('Missing residential publication');
 const candidate=new TemporalCityCore({phases:[...ledger.phases.values()],terrain:ledger.terrain});
 candidate.objects=new Map(ledger.objects);
 candidate.byPhase=new Map([...ledger.byPhase].map(([id,values])=>[id,new Set(values)]));
 candidate.links=new Map([...ledger.links].map(([id,value])=>[id,{predecessors:new Set(value.predecessors),successors:new Set(value.successors)}]));
 // Provisional parents and their children commit together. Copy only transformed geometry,
 // never the reference city's source IDs, lineage or historical confidence.
 const parents=includeRegistration?[...registration.districts.map(item=>({...item,type:'district'})),...registration.roads.map(item=>({...item,type:'road'}))].map(item=>{
  if(candidate.get(item.id))throw new Error(`Residential ID collision: ${item.id}`);
  const next=[...ledger.phases.keys()][[...ledger.phases.keys()].indexOf(generationPhase)+1];
  const events=[{phase:generationPhase,state:'build',authority:'generated-provisional-layout-not-historical-survey'},...(next?[{phase:next,state:'unresolved',authority:'later-layout-unverified'}]:[])];
  return {id:item.id,type:item.type,confidence:'inferred',geometry:{...item.geometry,frame:'canonical-dem-enu'},source:{authority:registration.authority,geometryVerified:false,dataset:`provisional-${generationPhase}-footprint-not-surveyed`},phaseIds:events.map(e=>e.phase),lifecycle:{events},metadata:{generatedOwner:owner,referenceLayoutDerived:true,geometryVerified:false,reuseLinksVerified:false}};
 }):[];
 for(const record of parents)candidate.register(record);
 const components=new Map();
 for(const mesh of architecture.meshes){const id=`${mesh.userData.cityObject.parcelId}:building`;if(!components.has(id))components.set(id,[]);components.get(id).push(mesh);}
 const prepared=records.map(record=>{
  if(candidate.get(record.id))throw new Error(`Residential ID collision: ${record.id}`);
  const source={...record.source,authority:registration.authority,geometryVerified:false};
  if(record.type==='parcel')source.blockId=`${generationPhase}:${source.blockId}`;
  if(record.type==='building'){
   const parcel=staged.get(source.parcelId);if(!parcel)throw new Error(`Missing residential parcel ${record.id}`);
   source.blockId=`${generationPhase}:${parcel.source.blockId}`;source.districtId=parcel.source.districtId;
  }
  if(!candidate.get(source.districtId))throw new Error(`Missing shared residential district ${record.id}`);
  const events=[{phase:generationPhase,state:generationPhase==='persian-nehemiah'?'rebuild':'build',authority:'generated-illustrative-residential-layout'}];
  if(destroyedPhase)events.push({phase:destroyedPhase,state:record.type==='building'?'ruin':'transform',authority:'schematic-destruction-not-excavated-object-fate'});
  if(retainedPhase)events.push({phase:retainedPhase,state:record.type==='building'?'ruin':'unresolved',authority:'optional-schematic-remains-not-verified-survival'});
  const lastIndex=[...ledger.phases.keys()].indexOf(retainedPhase||destroyedPhase||generationPhase),nextPhase=[...ledger.phases.keys()][lastIndex+1];
  if(nextPhase)events.push({phase:nextPhase,state:'unresolved',authority:'later-residential-geometry-unverified'});
  const parts=components.get(record.id),geometry={...record.geometry,frame:'canonical-dem-enu',status:'inferred-generated-residential'};
  if(record.type==='building'){
   if(!parts?.length)throw new Error(`Missing residential geometry ${record.id}`);
   const bounds=new THREE.Box3();parts.forEach(mesh=>bounds.expandByObject(mesh));geometry.bounds={min:bounds.min.toArray(),max:bounds.max.toArray()};
  }
  return {...record,source,geometry,phaseIds:events.map(e=>e.phase),lifecycle:{...record.lifecycle,reused:false,events},metadata:{...record.metadata,generatedOwner:owner,rendererBinding:'shared-residential-adapter-v1',generationPhase,geometryVerified:false,burialDepthVerified:false,reuseLinksVerified:false,componentCount:parts?.length||0}};
 });
 for(const record of prepared)candidate.register(record);
 for(const record of prepared){
  if(record.type==='parcel'&&candidate.get(record.source.blockId)?.type!=='block')throw new Error('Residential block relation invalid');
  if(record.type==='building'&&candidate.get(record.source.parcelId)?.type!=='parcel')throw new Error('Residential parcel relation invalid');
 }
 const validation=candidate.validate();if(!validation.ok)throw new Error(`Invalid residential ledger: ${validation.errors.join('; ')}`);
 ledger.objects=candidate.objects;ledger.byPhase=candidate.byPhase;ledger.links=candidate.links;
 // Bind the already finished geometry to the published records, with stable component IDs.
 for(const [id,parts] of components){const record=ledger.get(id);parts.forEach((mesh,index)=>Object.assign(mesh.userData.cityObject,{objectId:id,componentId:`${id}:component:${index}`,districtId:record.source.districtId}));}
 const ids=[...parents,...prepared].map(r=>r.id),buildingIds=prepared.filter(r=>r.type==='building').map(r=>r.id);
 const districts=registration.districts.map(d=>({id:d.id,blocks:prepared.filter(r=>r.type==='block'&&r.source.districtId===d.id).length,parcels:prepared.filter(r=>r.type==='parcel'&&r.source.districtId===d.id).length,buildings:prepared.filter(r=>r.type==='building'&&r.source.districtId===d.id).length}));
 const timeline={phases:[...ledger.phases.values()]};
 return{
  summary:{published:true,objects:ids.length,buildings:buildingIds.length,districts,sampleBuildingIds:buildingIds.slice(0,3),generationPhase,registrationObjects:parents.length,referenceLayoutDerived:includeRegistration,geometryVerified:false,reuseLinksVerified:false},
  stateFor(id,phase){const record=ledger.get(id);return record?lifecycleStateAt({lifecycleEvents:record.lifecycle.events},timeline,phase):'unresolved';},
  dispose(){for(const id of ids)if(ledger.get(id)?.metadata.generatedOwner===owner){ledger.objects.delete(id);ledger.links.delete(id);for(const values of ledger.byPhase.values())values.delete(id);}},
 };
}
