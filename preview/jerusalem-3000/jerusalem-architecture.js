import {resolveSpatialRegistration} from './spatial-registration.js';
import {buildArchitecturalGrammar} from './architectural-grammar.js';
const EVIDENCE_SURFACE={observed:'observed',reconstructed:'reconstructed',inferred:'inferred',disputed:'disputed'};
export function evidenceClass(value=''){if(value.includes('disputed'))return'disputed';if(value.includes('observed')||value.includes('archaeological'))return'observed';if(value.includes('reconstructed')||value.includes('textual'))return'reconstructed';return'inferred'}
export function isWithheld(object){return String(object.spatial?.registration||'').startsWith('withheld')||object.geometry?.status==='withheld'}
export function addEvidenceArchitecture(builder,object,terrain){
  const registered=resolveSpatialRegistration(object,terrain);if(!registered.renderable)return false;
  const surface=EVIDENCE_SURFACE[evidenceClass(object.evidence)];
  if(!buildArchitecturalGrammar(builder,object,registered,surface))return false;
  return registered;
}
