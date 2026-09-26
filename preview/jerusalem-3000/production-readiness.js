const REQUIRED_RUNTIME_FLAGS=['three','timeline','evidence','timeEngine','ruinEngine'];

export function auditProductionReadiness(runtime={}){
  const missing=REQUIRED_RUNTIME_FLAGS.filter(key=>runtime[key]!==true);
  const evidenceAudit=runtime.evidenceObjects?.evidenceResolutionAudit;
  const registrationAudit=runtime.evidenceObjects?.registrationAudit;
  const grammarAudit=runtime.evidenceObjects?.architecturalGrammarAudit;
  const pieceAudit=runtime.evidenceObjects?.architecturalPieceAudit;
  const failures=[];
  if(runtime.status!=='ready')failures.push(`runtime:${runtime.status||'unknown'}`);
  if(missing.length)failures.push(`flags:${missing.join(',')}`);
  if(!evidenceAudit?.ok)failures.push('evidence-resolution-audit');
  if(registrationAudit&&registrationAudit.rendered!==runtime.evidenceObjects?.renderableObjects)failures.push('spatial-registration-count');
  if(grammarAudit&&registrationAudit&&grammarAudit.eligible!==registrationAudit.rendered)failures.push('architectural-grammar-count');
  if(pieceAudit?.ok===false)failures.push('architectural-piece-density');
  return{
    ok:failures.length===0,
    failures,
    runtimeFlags:Object.fromEntries(REQUIRED_RUNTIME_FLAGS.map(key=>[key,runtime[key]===true])),
    evidenceObjects:runtime.evidenceObjects?.renderableObjects??0,
    constructionPieces:runtime.evidenceObjects?.constructionPieces??0,
    terrain:runtime.evidenceObjects?.terrain||null,
    spatialRegistration:runtime.evidenceObjects?.spatialRegistration||null,
    evidenceMode:runtime.evidenceMode||'all'
  };
}
