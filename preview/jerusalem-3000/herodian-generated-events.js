import {TemporalCityCore} from './temporal-city-core.js';
import {lifecycleStateAt} from './construction-engine.js';
// Normalize the finished canonical generator atomically, without touching sourced anchors.
export function publishHerodianGeneratedEvents(core,{registration,buildingIds,meshes}){
 const phase='herodian-jesus',ruin='roman-destruction',unknown='aelia';
 const generated=[...core.objects.values()].filter(r=>['block','parcel'].includes(r.type)&&r.source?.dataset==='herodian-30ce.registration');
 const buildings=buildingIds.map(id=>{const record=core.get(id);if(record?.type!=='building'||record.source?.grammar!=='herodian-typology-v5')throw new Error(`Invalid canonical generated building: ${id}`);return record;});
 if(!generated.length||!buildings.length||new Set(buildingIds).size!==buildingIds.length)throw new Error('Missing or duplicate canonical generated batch');
 const districtIds=new Set(generated.map(r=>r.source.districtId)),districts=[...districtIds].map(id=>{const record=core.get(id);if(record?.type!=='district')throw new Error(`Missing canonical district: ${id}`);return record;});
 const roads=registration.roads.map(road=>{if(core.get(road.id))throw new Error(`Canonical road ID collision: ${road.id}`);return {id:road.id,type:'road',confidence:road.confidence,geometry:{...road.geometry,frame:'canonical-dem-enu'},source:{dataset:'herodian-30ce.registration',authority:registration.authority},metadata:{generatedRoad:true},lifecycle:{events:[]}};});
 const candidate=new TemporalCityCore({phases:[...core.phases.values()],terrain:core.terrain});candidate.objects=new Map(core.objects);candidate.byPhase=new Map([...core.byPhase].map(([id,set])=>[id,new Set(set)]));candidate.links=new Map(core.links);
 const records=[...districts,...generated,...buildings,...roads],prepared=[];
 if(new Set(records.map(r=>r.id)).size!==records.length)throw new Error('Duplicate canonical publication ID');
 for(const record of records){
  if(record.lifecycle.events.length)throw new Error(`Conflicting canonical lifecycle: ${record.id}`);
  const source={...record.source,geometryVerified:false};
  if(record.type==='parcel')source.blockId=`${phase}:${source.blockId}`;
  if(record.type==='building'){const parcel=core.get(source.parcelId);if(parcel?.type!=='parcel')throw new Error(`Missing canonical parcel: ${record.id}`);source.districtId=parcel.source.districtId;source.blockId=`${phase}:${parcel.source.blockId}`;}
  const events=[{phase,state:'build',authority:'illustrative-canonical-generation-not-object-construction-date'},
   {phase:ruin,state:record.type==='building'?'ruin':'transform',authority:'schematic-destruction-not-excavated-object-fate'},
   {phase:unknown,state:'unresolved',authority:'later-generated-object-fate-unverified'}];
  const next={...record,source,phaseIds:[...(record.phaseIds||[]),...events.map(e=>e.phase)],lifecycle:{...record.lifecycle,reused:false,events},metadata:{...record.metadata,rendererBinding:'canonical-generated-events-v1',generationPhase:phase,geometryVerified:false,reuseLinksVerified:false}};
  candidate.register(next);prepared.push(next);
 }
 for(const record of prepared){if(record.type==='parcel'&&candidate.get(record.source.blockId)?.type!=='block')throw new Error(`Invalid canonical block relation: ${record.id}`);if(record.type==='building'&&candidate.get(record.source.parcelId)?.type!=='parcel')throw new Error(`Invalid canonical parcel relation: ${record.id}`);}
 const preparedIds=new Set(prepared.map(r=>r.id));
 const bindings=meshes.map(mesh=>{const meta=mesh.userData.cityObject,id=meta?.objectId||(meta?.parcelId?`${meta.parcelId}:building`:null),record=candidate.get(id);if(!record||!preparedIds.has(id))throw new Error(`Unpublished canonical mesh: ${id}`);return {mesh,id,record};});
 const boundIds=new Set(bindings.map(binding=>binding.id));if(buildingIds.some(id=>!boundIds.has(id)))throw new Error('Missing canonical building geometry');
 const validation=candidate.validate();if(!validation.ok)throw new Error(`Invalid canonical lifecycle batch: ${validation.errors.join('; ')}`);
 core.objects=candidate.objects;core.byPhase=candidate.byPhase;core.links=candidate.links;
 const indices=new Map();for(const {mesh,id,record}of bindings){const index=indices.get(id)||0;indices.set(id,index+1);Object.assign(mesh.userData.cityObject,{objectId:id,componentId:`${id}:component:${index}`,...(record.source.districtId?{districtId:record.source.districtId}:{})});}
 const timeline={phases:[...core.phases.values()]};
 return {summary:{objects:prepared.length,buildings:buildings.length,roads:roads.length,geometryVerified:false,reuseLinksVerified:false},stateFor(id,phaseId){if(!phaseId)return 'absent';const record=core.get(id);return record?lifecycleStateAt({lifecycleEvents:record.lifecycle.events},timeline,phaseId):'unresolved';}};
}
