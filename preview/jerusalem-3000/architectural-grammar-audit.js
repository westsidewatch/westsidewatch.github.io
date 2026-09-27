import {SUPPORTED_ARCHITECTURAL_KINDS,ARCHITECTURAL_GRAMMAR_VERSION} from './architectural-grammar.js';
const GRAMMAR_KINDS=new Set(SUPPORTED_ARCHITECTURAL_KINDS);
const PHASE2_BOUNDED_IDS=new Set(['j3k:object:inner-temple']);
const MIN_PIECES={'platform-enclosure':15,'portico-basilica':100,fortress:10,'sacred-complex':24,'pilgrimage-access':15,street:60};
function isWithheld(object){return(String(object.spatial?.registration||'').startsWith('withheld')||object.geometry?.status==='withheld')&&!PHASE2_BOUNDED_IDS.has(object.id)}
export function auditArchitecturalGrammar(objects){
 const report={version:ARCHITECTURAL_GRAMMAR_VERSION,eligible:0,withheld:0,bounded:0,unsupported:[],missingEvidence:[],missingConfidence:[],missingLifecycle:[],kinds:{}};
 for(const object of objects){const withheld=isWithheld(object);if(withheld){report.withheld++;continue}if(PHASE2_BOUNDED_IDS.has(object.id))report.bounded++;if(!GRAMMAR_KINDS.has(object.kind)){report.unsupported.push({id:object.id,kind:object.kind});continue}report.eligible++;report.kinds[object.kind]=(report.kinds[object.kind]||0)+1;if(!object.evidence)report.missingEvidence.push(object.id);if(!object.confidence)report.missingConfidence.push(object.id);if(!object.lifecycle?.stateAt30CE)report.missingLifecycle.push(object.id)}
 if(report.unsupported.length)throw new Error(`Architectural grammar missing supported kinds: ${report.unsupported.map(x=>`${x.id}:${x.kind}`).join(', ')}`);if(report.missingEvidence.length||report.missingConfidence.length||report.missingLifecycle.length)throw new Error('Architectural grammar authority incomplete');for(const kind of GRAMMAR_KINDS)if(!report.kinds[kind])throw new Error(`Architectural grammar coverage missing: ${kind}`);return report;
}
export function auditArchitecturalPieceDensity(objects,piecesBefore,piecesAfter){const expected=objects.filter(o=>!isWithheld(o)).reduce((n,o)=>n+(MIN_PIECES[o.kind]||0),0);const generated=piecesAfter-piecesBefore;if(generated<expected)throw new Error(`Architectural grammar under-detailed: generated=${generated}, minimum=${expected}`);return{generated,minimum:expected,status:'pass'};}
