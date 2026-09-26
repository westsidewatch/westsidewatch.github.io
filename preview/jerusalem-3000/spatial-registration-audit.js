import {resolveSpatialRegistration} from './spatial-registration.js';

export function auditSpatialRegistrations(objects,terrain){
  const results=[];
  for(const object of objects){
    const resolved=resolveSpatialRegistration(object,terrain);
    results.push({
      id:object.id,
      label:object.label,
      renderable:resolved.renderable,
      reason:resolved.reason||null,
      frame:resolved.frame||null,
      east:resolved.east??null,
      north:resolved.north??null,
      up:resolved.up??null,
      accuracy:resolved.accuracy||object.spatial?.accuracy||null,
      sourceRegistration:resolved.sourceRegistration||object.spatial?.registration||null
    });
  }
  const rendered=results.filter(r=>r.renderable);
  const withheld=results.filter(r=>!r.renderable&&r.reason==='withheld');
  const invalid=results.filter(r=>!r.renderable&&r.reason!=='withheld');
  if(invalid.length)throw new Error(`Spatial registration audit failed: ${invalid.map(r=>`${r.id}:${r.reason}`).join(', ')}`);
  if(!rendered.length)throw new Error('Spatial registration audit failed: no renderable historical objects');
  for(const r of rendered){
    if(r.frame!=='canonical-dem-enu'||![r.east,r.north,r.up].every(Number.isFinite))throw new Error(`Spatial registration audit failed: ${r.id} has invalid canonical coordinates`);
  }
  return{status:'pass',total:results.length,rendered:rendered.length,withheld:withheld.length,invalid:0,results};
}
