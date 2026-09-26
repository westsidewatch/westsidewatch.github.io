const LEVELS=['observed','reconstructed','inferred','disputed','withheld'];
const RANK=Object.fromEntries(LEVELS.map((level,index)=>[level,index]));

export function resolveEvidenceLevel(object={}){
  const registration=String(object.spatial?.registration||'').toLowerCase();
  const geometry=String(object.geometry?.status||'').toLowerCase();
  const evidence=String(object.evidence||'').toLowerCase();
  if(registration.startsWith('withheld')||geometry==='withheld'||evidence.includes('withheld'))return'withheld';
  if(evidence.includes('disputed'))return'disputed';
  if(evidence.includes('observed')||evidence.includes('archaeological'))return'observed';
  if(evidence.includes('reconstructed')||evidence.includes('textual'))return'reconstructed';
  return'inferred';
}

export class EvidenceResolutionEngine{
  constructor(objects=[]){
    this.objects=objects;
    this.levelById=new Map(objects.map(object=>[object.id,resolveEvidenceLevel(object)]));
  }
  levelFor(object){return this.levelById.get(object.id)||resolveEvidenceLevel(object)}
  allows(object,mode='all'){
    const level=this.levelFor(object);
    if(level==='withheld')return false;
    if(mode==='all')return true;
    if(mode==='observed')return level==='observed';
    if(mode==='reconstructed')return RANK[level]<=RANK.reconstructed;
    if(mode==='inferred')return RANK[level]<=RANK.inferred;
    if(mode==='disputed')return level==='disputed';
    return true;
  }
  summary(){
    const counts=Object.fromEntries(LEVELS.map(level=>[level,0]));
    for(const object of this.objects)counts[this.levelFor(object)]++;
    return counts;
  }
}
