import {EvidenceResolutionEngine,resolveEvidenceLevel} from './evidence-resolution-engine.js';

const MODES=['all','observed','reconstructed','inferred','disputed'];

export function auditEvidenceResolution(objects=[]){
  const engine=new EvidenceResolutionEngine(objects);
  const summary=engine.summary();
  const total=Object.values(summary).reduce((sum,value)=>sum+value,0);
  if(total!==objects.length)throw new Error(`Evidence resolution count mismatch: ${total}/${objects.length}`);
  for(const object of objects){
    const level=resolveEvidenceLevel(object);
    if(level!==engine.levelFor(object))throw new Error(`Evidence resolution unstable for ${object.id||'unknown'}`);
    if(level==='withheld'&&MODES.some(mode=>engine.allows(object,mode)))throw new Error(`Withheld evidence leaked into render modes: ${object.id||'unknown'}`);
  }
  const visibleByMode=Object.fromEntries(MODES.map(mode=>[mode,objects.filter(object=>engine.allows(object,mode)).length]));
  if(visibleByMode.all!==objects.length-summary.withheld)throw new Error('All-mode evidence visibility violates withheld boundary');
  if(visibleByMode.observed!==summary.observed)throw new Error('Observed-mode evidence visibility mismatch');
  if(visibleByMode.disputed!==summary.disputed)throw new Error('Disputed-mode evidence visibility mismatch');
  if(visibleByMode.reconstructed<visibleByMode.observed)throw new Error('Reconstructed resolution must include observed evidence');
  if(visibleByMode.inferred<visibleByMode.reconstructed)throw new Error('Inferred resolution must include reconstructed evidence');
  return{ok:true,total,summary,visibleByMode,modes:MODES};
}
