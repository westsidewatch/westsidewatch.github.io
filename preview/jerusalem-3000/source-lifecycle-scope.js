import {TemporalCityCore} from './temporal-city-core.js';
import {lifecycleStateAtPosition} from './construction-engine.js';
const SCOPES=new Map([
 ['j3k:district:temple-mount','source-context-only'],['j3k:district:southern-approach','source-context-only'],['j3k:district:antonia-northwest','source-context-only'],
 ['j3k:road:western-street','source-context-only'],['j3k:road:southern-pilgrimage-approach','source-context-only'],
 ['j3k:gate:eastern-access-unresolved','withheld'],['j3k:object:eastern-entry-unknown','withheld']
]);
const AUTHORITY='herodian-source-scopes-v1';
export function declaredEventScope(record){
 const declaration=record.metadata?.lifecycleDeclaration;
 return !record.lifecycle.events.length&&declaration?.authority===AUTHORITY&&SCOPES.get(record.id)===declaration.status?declaration.status:null;
}
// These declarations account for non-physical relations and withheld entries; they
// do not copy source events into district/road construction or invent lineage.
export function declareHerodianSourceScopes(core){
 const candidate=new TemporalCityCore({phases:[...core.phases.values()],terrain:core.terrain});candidate.objects=new Map(core.objects);candidate.byPhase=new Map([...core.byPhase].map(([id,set])=>[id,new Set(set)]));candidate.links=new Map(core.links);
 for(const [id,status]of SCOPES){
  const record=core.get(id);if(!record||record.lifecycle.events.length)throw new Error(`Source scope missing or conflicting events: ${id}`);
  const anchorIds=record.source?.anchorObjectIds||[record.source?.anchorObjectId].filter(Boolean);
  if(status==='source-context-only'&&!anchorIds.length)throw new Error(`Source scope requires context anchors: ${id}`);
  for(const anchorId of anchorIds){const anchor=core.get(anchorId);if(!anchor)throw new Error(`Missing source context anchor: ${anchorId}`);if(status==='source-context-only'&&!anchor.lifecycle.events.length)throw new Error(`Missing source context events: ${anchorId}`);}
  if(status==='withheld'&&record.geometry?.status!=='withheld')throw new Error(`Source entry must remain withheld: ${id}`);
  candidate.register({...record,lifecycle:{...record.lifecycle,built:null,destroyed:null},metadata:{...record.metadata,lifecycleDeclaration:{authority:AUTHORITY,status,anchorObjectIds:[...anchorIds],physicalEventsDeclared:false,reason:status==='withheld'?'geometry-and-object-fate-unresolved-no-draw':'relational-context-not-a-separate-physical-object-history',geometryVerified:false}}});
 }
 const validation=candidate.validate();if(!validation.ok)throw new Error(`Invalid source scope batch: ${validation.errors.join('; ')}`);
 core.objects=candidate.objects;core.byPhase=candidate.byPhase;core.links=candidate.links;
 return {objects:SCOPES.size,sourceContextOnly:5,withheld:2,physicalEventsInvented:0};
}
export function inspectSourceLifecycleContext(core,id,position){
 const record=core.get(id),status=record&&declaredEventScope(record);if(!status)return null;
 const timeline={phases:[...core.phases.values()]};
 return {id,status,ownPhysicalEventsDeclared:false,geometryVerified:false,sourceContextOnly:true,anchors:record.metadata.lifecycleDeclaration.anchorObjectIds.map(anchorId=>{
  const anchor=core.get(anchorId);return {id:anchorId,state:anchor?.lifecycle.events.length?lifecycleStateAtPosition({lifecycleEvents:anchor.lifecycle.events},timeline,position):'unresolved'};
 })};
}
