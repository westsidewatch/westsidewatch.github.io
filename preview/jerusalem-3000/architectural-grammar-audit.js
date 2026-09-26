const GRAMMAR_KINDS=new Set(['platform-enclosure','portico-basilica','fortress','pilgrimage-access','street']);
export function auditArchitecturalGrammar(objects){
 const report={eligible:0,withheld:0,unsupported:[],missingEvidence:[],missingConfidence:[],missingLifecycle:[]};
 for(const object of objects){
  const withheld=String(object.spatial?.registration||'').startsWith('withheld')||object.geometry?.status==='withheld';
  if(withheld){report.withheld++;continue}
  if(!GRAMMAR_KINDS.has(object.kind)){report.unsupported.push({id:object.id,kind:object.kind});continue}
  report.eligible++;
  if(!object.evidence)report.missingEvidence.push(object.id);
  if(!object.confidence)report.missingConfidence.push(object.id);
  if(!object.lifecycle?.stateAt30CE)report.missingLifecycle.push(object.id);
 }
 if(report.unsupported.length)throw new Error(`Architectural grammar missing supported kinds: ${report.unsupported.map(x=>`${x.id}:${x.kind}`).join(', ')}`);
 if(report.missingEvidence.length||report.missingConfidence.length||report.missingLifecycle.length)throw new Error('Architectural grammar authority incomplete');
 return report;
}
