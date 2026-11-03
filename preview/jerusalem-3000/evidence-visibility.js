const MODES=new Set(['all','observed','reconstructed','inferred','disputed']);
// Shared display policy; confidence belongs to the object/annotation, not its material color.
export function allowsEvidence(mode,confidence){
 if(!MODES.has(mode))throw new Error(`Unknown evidence mode: ${mode}`);
 if(mode==='all')return true;
 if(mode==='observed')return confidence==='observed';
 if(mode==='reconstructed')return confidence==='observed'||confidence==='reconstructed';
 if(mode==='inferred')return confidence!=='disputed';
 return confidence==='disputed';
}
