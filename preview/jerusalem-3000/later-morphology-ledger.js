import {TemporalCityCore} from './temporal-city-core.js';
import {lifecycleStateAt} from './construction-engine.js';
let sequence=0;
const PHASES=new Set(['crusader','ottoman','aelia','byzantine','early-islamic','ayyubid-mamluk','outside-walls','modern']);
// Registry survives renderer rebuilds; scene disposal removes only its own records.
// Anonymous box masses remain blocks, never semantic buildings or named monuments.
export function createLaterMorphologyLedger(core){
 const owner=`later-morphology:${++sequence}`,batches=new Map(),timeline={phases:[...core.phases.values()]};
 return {
  bind(runtime){
   const phase=runtime.phaseId;if(!PHASES.has(phase)||!runtime.meshes?.length)throw new Error('Unsupported later morphology batch');
   const recipes=runtime.meshes.map((mesh,index)=>{
    const meta=mesh.userData.phase2;if(!meta?.stage||!Number.isFinite(meta.start))throw new Error('Missing morphology recipe');
    const id=`j3k:${phase}:scaffold:${index}`,type=meta.stage==='road'?'road':meta.stage==='wall'?'wall':meta.stage==='gate'?'gate':'block';
    const geometry={frame:'canonical-dem-enu',status:'provisional-morphology-not-surveyed',primitive:'box-mass',parameters:{...mesh.geometry.parameters},position:mesh.position.toArray(),rotation:mesh.rotation.toArray()};
    if([...mesh.position.toArray(),...mesh.rotation.toArray().slice(0,3),...Object.values(mesh.geometry.parameters)].some(v=>!Number.isFinite(v)))throw new Error('Invalid morphology geometry');
    return {id,type,geometry,stage:meta.stage,start:meta.start};
   });
   const fingerprint=JSON.stringify(recipes),prior=batches.get(phase);
   if(prior&&prior.fingerprint!==fingerprint)throw new Error('Later morphology recipe changed without registration migration');
   const candidate=new TemporalCityCore({phases:timeline.phases,terrain:core.terrain});
   candidate.objects=new Map(core.objects);candidate.byPhase=new Map([...core.byPhase].map(([id,set])=>[id,new Set(set)]));candidate.links=new Map(core.links);
   const next=timeline.phases[timeline.phases.findIndex(p=>p.id===phase)+1]?.id;
   for(const recipe of recipes){
    const existing=core.get(recipe.id);
    if(prior){if(existing?.metadata.generatedOwner!==owner)throw new Error(`Lost later morphology ownership: ${recipe.id}`);continue;}
    if(existing)throw new Error(`Later morphology ID collision: ${recipe.id}`);
    const events=[{phase,state:'build',authority:'illustrative-morphology-generation-not-historical-construction'},...(next?[{phase:next,state:'unresolved',authority:'later-morphology-fate-unverified'}]:[])];
    candidate.register({id:recipe.id,type:recipe.type,confidence:'inferred',geometry:recipe.geometry,phaseIds:events.map(e=>e.phase),lifecycle:{events},
     source:{dataset:runtime.grammar,authority:'legacy-procedural-scaffold-not-historical-survey',geometryVerified:false},
     metadata:{generatedOwner:owner,generationPhase:phase,scaffoldRole:recipe.stage,constructionStart:recipe.start,geometryVerified:false,ancientGroundVerified:false,reuseLinksVerified:false,semanticBuilding:false,rendererBinding:'later-morphology-v1'}});
   }
   const validation=candidate.validate();if(!validation.ok)throw new Error(`Invalid later ledger: ${validation.errors.join('; ')}`);
   if(!prior){core.objects=candidate.objects;core.byPhase=candidate.byPhase;core.links=candidate.links;batches.set(phase,{fingerprint,ids:recipes.map(r=>r.id)});}
   // Bind only after the complete batch has passed. Rebinding preserves edited events.
   runtime.meshes.forEach((mesh,index)=>{const recipe=recipes[index];mesh.userData.cityObject={objectId:recipe.id,componentId:`${recipe.id}:component:0`,confidence:'inferred',phaseIds:[phase],kind:recipe.stage};});
   const summary={published:true,phase,objects:recipes.length,geometryVerified:false,semanticBuildings:0};
   return {summary,apply(evidenceAllowed){for(const mesh of runtime.meshes){const record=core.get(mesh.userData.cityObject.objectId),state=record?lifecycleStateAt({lifecycleEvents:record.lifecycle.events},timeline,phase):'unresolved';mesh.visible=(runtime.fixedVisibility||mesh.visible)&&evidenceAllowed('inferred')&&['build','rebuild','transform','ruin','expand'].includes(state);}}};
  },
  dispose(){for(const batch of batches.values())for(const id of batch.ids)if(core.get(id)?.metadata.generatedOwner===owner){core.objects.delete(id);core.links.delete(id);for(const ids of core.byPhase.values())ids.delete(id);}batches.clear();}
 };
}
