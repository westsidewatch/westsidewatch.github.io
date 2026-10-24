import * as THREE from 'three';
import {TemporalCityCore} from './temporal-city-core.js';
import {lifecycleStateAt} from './construction-engine.js';
let sequence=0;
// Publish only illustrative dwellings and footpaths. Defense is owned by its source adapter;
// spring symbols, disputed support and royal location markers remain outside this batch.
export function publishSettlementLedger(core,meshes,data){
 const owner=`settlement:${data.phase}:${++sequence}`,groups=new Map();
 for(const mesh of meshes){const {objectId,kind}=mesh.userData.cityObject;
  if(!objectId.includes(':house:')&&kind!=='inferred-footpath')continue;
  if(!groups.has(objectId))groups.set(objectId,[]);groups.get(objectId).push(mesh);
 }
 const phases=[...core.phases.keys()],index=phases.indexOf(data.phase);
 if(index<0)throw new Error('Settlement phase missing from shared ledger');
 const candidate=new TemporalCityCore({phases:[...core.phases.values()],terrain:core.terrain});
 candidate.objects=new Map(core.objects);candidate.byPhase=new Map([...core.byPhase].map(([id,set])=>[id,new Set(set)]));
 candidate.links=new Map(core.links);
 for(const [id,parts]of groups){
  if(candidate.get(id))throw new Error(`Settlement ID collision: ${id}`);
  const building=id.includes(':house:'),bounds=new THREE.Box3();parts.forEach(mesh=>bounds.expandByObject(mesh));
  const events=[{phase:data.phase,state:'build',authority:'illustrative-settlement-generation-not-excavated-object'},...(phases[index+1]?[{phase:phases[index+1],state:'unresolved',authority:'later-object-fate-unverified'}]:[])];
  candidate.register({id,type:building?'building':'road',confidence:'inferred',phaseIds:events.map(e=>e.phase),
   geometry:{frame:'canonical-dem-enu',status:'illustrative-not-surveyed',bounds:{min:bounds.min.toArray(),max:bounds.max.toArray()}},
   source:{dataset:data.schema,authority:data.authority,contextSource:data.historicalSource,geometryVerified:false},
   typology:building?(data.houseTypology||'single-room-illustration'):null,lifecycle:{events},
   metadata:{generatedOwner:owner,generationPhase:data.phase,componentCount:parts.length,geometryVerified:false,ancientGroundVerified:false,reuseLinksVerified:false,rendererBinding:'early-settlement-v1'}});
 }
 const validation=candidate.validate();if(!validation.ok)throw new Error(`Invalid settlement ledger: ${validation.errors.join('; ')}`);
 core.objects=candidate.objects;core.byPhase=candidate.byPhase;core.links=candidate.links;
 for(const [id,parts]of groups)parts.forEach((mesh,index)=>{mesh.userData.cityObject.componentId=`${id}:component:${index}`;});
 const timeline={phases:[...core.phases.values()]};
 return {summary:{published:true,objects:groups.size,buildings:[...groups.keys()].filter(id=>id.includes(':house:')).length,roads:[...groups.keys()].filter(id=>id.includes(':path:')).length,geometryVerified:false},
  allows(id,phase){const record=core.get(id);return Boolean(record&&['build','rebuild','transform','ruin','expand'].includes(lifecycleStateAt({lifecycleEvents:record.lifecycle.events},timeline,phase)));},
  owns:id=>groups.has(id),
  dispose(){for(const id of groups.keys())if(core.get(id)?.metadata.generatedOwner===owner){core.objects.delete(id);core.links.delete(id);for(const ids of core.byPhase.values())ids.delete(id);}}
 };
}
