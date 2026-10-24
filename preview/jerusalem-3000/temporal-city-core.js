import {CONSTRUCTION_STATES} from './construction-engine.js';
export const EVIDENCE_CONFIDENCE=Object.freeze({OBSERVED:'observed',RECONSTRUCTED:'reconstructed',INFERRED:'inferred',DISPUTED:'disputed'});
export const CITY_OBJECT_TYPES=Object.freeze({DISTRICT:'district',ROAD:'road',GATE:'gate',WALL:'wall',BLOCK:'block',PARCEL:'parcel',BUILDING:'building',MONUMENT:'monument',WATER:'water',ROUTE:'route'});

function freezeRecord(value){return Object.freeze({...value});}
function requireId(value,label){if(!value||typeof value!=='string')throw new Error(`${label} requires a stable string id`);return value}
function confidence(value){const allowed=Object.values(EVIDENCE_CONFIDENCE);if(!allowed.includes(value))throw new Error(`invalid evidence confidence: ${value}`);return value}

export class TemporalCityCore{
 constructor({phases=[],terrain=null}={}){this.phases=new Map(phases.map(p=>[p.id,freezeRecord(p)]));this.terrain=terrain;this.objects=new Map();this.byPhase=new Map();this.links=new Map();}
 register(input){
  const id=requireId(input.id,'city object'),type=input.type;
  if(!Object.values(CITY_OBJECT_TYPES).includes(type))throw new Error(`invalid city object type: ${type}`);
  const events=(input.lifecycle?.events||[]).map(event=>({...event})),eventKeys=new Set();
  for(const event of events){
   if(!this.phases.has(event.phase))throw new Error(`unknown lifecycle phase: ${event.phase}`);
   if(!CONSTRUCTION_STATES.has(event.state))throw new Error(`invalid lifecycle state: ${event.state}`);
   const offset=event.offset??0;
   if(!Number.isFinite(offset)||offset<0||offset>=1)throw new Error('invalid lifecycle offset');
   const key=`${event.phase}:${offset}`;
   if(eventKeys.has(key))throw new Error(`duplicate lifecycle instant: ${key}`);
   eventKeys.add(key);
  }
  const phaseIds=[...new Set([...(input.phaseIds||[]),...events.map(event=>event.phase)])];
  for(const phaseId of phaseIds)if(!this.phases.has(phaseId))throw new Error(`unknown phase: ${phaseId}`);
  const record=freezeRecord({
   id,type,phaseIds:Object.freeze(phaseIds),geometry:input.geometry||null,typology:input.typology||null,
   source:input.source||null,confidence:confidence(input.confidence||EVIDENCE_CONFIDENCE.INFERRED),
   lifecycle:freezeRecord({built:input.lifecycle?.built??null,destroyed:input.lifecycle?.destroyed??null,
    ruined:input.lifecycle?.ruined??false,reused:input.lifecycle?.reused??false,
    events:Object.freeze(events.map(event=>Object.freeze({...event})))}),
   predecessorIds:[...(input.predecessorIds||[])],successorIds:[...(input.successorIds||[])],
   metadata:freezeRecord(input.metadata||{})
  });
  // Reject invalid input before changing either the object or any phase index.
  this.objects.set(id,record);
  for(const [phaseId,values]of this.byPhase)if(!phaseIds.includes(phaseId))values.delete(id);
  for(const phaseId of phaseIds){
   if(!this.byPhase.has(phaseId))this.byPhase.set(phaseId,new Set());
   this.byPhase.get(phaseId).add(id);
  }
  this.links.set(id,{predecessors:new Set(record.predecessorIds),successors:new Set(record.successorIds)});
  return record;
 }
 get(id){return this.objects.get(id)||null}
 phase(phaseId){return [...(this.byPhase.get(phaseId)||[])].map(id=>this.objects.get(id)).filter(object=>object?.phaseIds.includes(phaseId))}
 connect(predecessorId,successorId){if(!this.objects.has(predecessorId)||!this.objects.has(successorId))throw new Error('lifecycle link requires registered objects');this.links.get(predecessorId).successors.add(successorId);this.links.get(successorId).predecessors.add(predecessorId);return this;}
 lineage(id){const link=this.links.get(id);if(!link)return null;return{predecessors:[...link.predecessors],successors:[...link.successors]}}
 summary(phaseId){const objects=this.phase(phaseId),types={},evidence={};for(const object of objects){types[object.type]=(types[object.type]||0)+1;evidence[object.confidence]=(evidence[object.confidence]||0)+1}return{phaseId,total:objects.length,types,evidence}}
 validate(){const errors=[];for(const[phaseId,ids]of this.byPhase)for(const id of ids)if(!this.objects.get(id)?.phaseIds.includes(phaseId))errors.push(`${id}: stale phase index ${phaseId}`);for(const[id,object]of this.objects)for(const phaseId of object.phaseIds)if(!this.byPhase.get(phaseId)?.has(id))errors.push(`${id}: missing phase index ${phaseId}`);for(const [id,object] of this.objects){for(const predecessor of object.predecessorIds)if(!this.objects.has(predecessor))errors.push(`${id}: missing predecessor ${predecessor}`);for(const successor of object.successorIds)if(!this.objects.has(successor))errors.push(`${id}: missing successor ${successor}`);if(object.type===CITY_OBJECT_TYPES.BUILDING&&object.geometry?.primitive==='box')errors.push(`${id}: BoxGeometry cannot be a semantic building primitive`);if(object.type===CITY_OBJECT_TYPES.MONUMENT&&object.geometry?.primitive==='slab')errors.push(`${id}: naked slab cannot represent a monument`);if(object.type===CITY_OBJECT_TYPES.PARCEL&&!object.source?.blockId)errors.push(`${id}: parcel must belong to an urban block`)}return{ok:errors.length===0,errors,count:this.objects.size}}
}

export function createTemporalCityCore({phases,terrain}={}){return new TemporalCityCore({phases,terrain});}
