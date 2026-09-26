import {resolveSpatialRegistration} from './spatial-registration.js';
const KIND_SCHEDULE={
  'platform-enclosure':{start:.08,duration:.16,lift:210},'pilgrimage-access':{start:.22,duration:.12,lift:150},street:{start:.29,duration:.12,lift:120},fortress:{start:.37,duration:.16,lift:230},'portico-basilica':{start:.50,duration:.17,lift:190},'sacred-complex':{start:.62,duration:.18,lift:250}
};
const KIND_DIMENSIONS={'platform-enclosure':[520,34,340],'portico-basilica':[390,70,70],fortress:[150,150,150],'sacred-complex':[210,125,160],'pilgrimage-access':[190,22,95],street:[55,8,300]};
const EVIDENCE_SURFACE={observed:'observed',reconstructed:'reconstructed',inferred:'inferred',disputed:'disputed'};
export function evidenceClass(value=''){if(value.includes('disputed'))return'disputed';if(value.includes('observed')||value.includes('archaeological'))return'observed';if(value.includes('reconstructed')||value.includes('textual'))return'reconstructed';return'inferred'}
export function isWithheld(object){return String(object.spatial?.registration||'').startsWith('withheld')||object.geometry?.status==='withheld'}
export function addEvidenceArchitecture(builder,object,terrain){
  const registered=resolveSpatialRegistration(object,terrain);if(!registered.renderable)return false;
  const dimensions=KIND_DIMENSIONS[object.kind]||[90,55,90],schedule=KIND_SCHEDULE[object.kind]||{start:.42,duration:.14,lift:160},surface=EVIDENCE_SURFACE[evidenceClass(object.evidence)];
  builder.box(dimensions,[registered.east,registered.up+dimensions[1]/2,-registered.north],surface,schedule.start,{duration:schedule.duration,lift:schedule.lift});return registered;
}
