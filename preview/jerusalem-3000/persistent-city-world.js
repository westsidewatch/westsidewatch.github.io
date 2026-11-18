import * as THREE from 'three';

const geometryBytes=g=>Object.values(g.attributes).reduce((n,a)=>n+a.array.byteLength,0)+(g.index?.array.byteLength||0);
function signature(g){
 let hash=2166136261;
 for(const [name,a] of [...Object.entries(g.attributes).sort(),['index',g.index]].filter(([,a])=>a)){
  for(const c of name)hash=Math.imul(hash^c.charCodeAt(0),16777619)>>>0;
  const bytes=new Uint8Array(a.array.buffer,a.array.byteOffset,a.array.byteLength);
  for(const b of bytes)hash=Math.imul(hash^b,16777619)>>>0;
 }
 return `${geometryBytes(g)}:${hash}`;
}
function equalGeometry(a,b){
 if(JSON.stringify(a.userData)!==JSON.stringify(b.userData)||JSON.stringify(a.groups)!==JSON.stringify(b.groups)||JSON.stringify(a.drawRange)!==JSON.stringify(b.drawRange))return false;
 const keys=Object.keys(a.attributes).sort();if(JSON.stringify(keys)!==JSON.stringify(Object.keys(b.attributes).sort()))return false;
 for(const key of [...keys,'index']){
  const x=key==='index'?a.index:a.attributes[key],y=key==='index'?b.index:b.attributes[key];
  if(!x!==!y)return false;if(!x)continue;
  if(x.itemSize!==y.itemSize||x.normalized!==y.normalized||x.array.constructor!==y.array.constructor||x.array.length!==y.array.length)return false;
  for(let i=0;i<x.array.length;i++)if(x.array[i]!==y.array[i])return false;
 }
 return true;
}

// One persistent scene owner. Phase-specific evidence/events remain with the ledger.
// Sharing an identical GPU buffer is a display optimisation, NEVER historical reuse.
export function createPersistentCityWorld({parent,phases,build,publish}){
 if(!parent?.isObject3D||!phases?.length||new Set(phases).size!==phases.length||typeof build!=='function'||typeof publish!=='function')throw new Error('Invalid persistent city world');
 const allowed=new Set(phases),entries=new Map(),pool=new Map();let active=null,builds=0,hits=0,disposed=false;
 const releaseRaw=runtime=>{for(const mesh of runtime?.meshes||[]){mesh.removeFromParent();mesh.geometry.dispose();}runtime?.disposeMaterials?.();};
 function activate(phase){
  if(disposed)throw new Error('Persistent city world disposed');
  if(phase!==null&&!allowed.has(phase))throw new Error(`Unsupported persistent phase: ${phase}`);
  let next=phase===null?null:entries.get(phase);
  if(phase!==null&&!next){
   const group=new THREE.Group();group.name=`j3k-world:${phase}`;group.visible=false;let runtime;
   try{
    runtime=build(group,phase);
    if(runtime.phaseId!==phase||!runtime.meshes?.length||runtime.meshes.some(m=>m.parent!==group))throw new Error('Invalid persistent phase runtime');
    const binding=publish(runtime);
    for(const mesh of runtime.meshes){
     const raw=mesh.geometry,key=signature(raw),bucket=pool.get(key)||[],existing=bucket.find(g=>equalGeometry(g,raw));
     if(existing){mesh.geometry=existing;raw.dispose();}else{bucket.push(raw);pool.set(key,bucket);}
    }
    next={group,runtime,binding};parent.add(group);entries.set(phase,next);builds++;
   }catch(error){group.removeFromParent();releaseRaw(runtime);throw error;}
  }else if(next)hits++;
  // Build and validate first: a failed target must leave the current city intact.
  if(active)active.group.visible=false;
  active=next;if(active)active.group.visible=true;
  return next;
 }
 return {
  activate,
  diagnostics(){
   const geometries=[...pool.values()].flat(),instances=[...entries.values()].flatMap(e=>e.runtime.meshes);
   return {activePhase:active?.runtime.phaseId||null,phaseCapacity:allowed.size,cachedPhases:[...entries.keys()],builds,cacheHits:hits,meshInstances:instances.length,uniqueGeometries:geometries.length,geometryBufferBytes:geometries.reduce((n,g)=>n+geometryBytes(g),0),sameGeometryIsHistoricalReuse:false,historicalContinuityAccepted:false};
  },
  inspectPhase(phase){const entry=entries.get(phase);return entry?{groupId:entry.group.uuid,meshIds:entry.runtime.meshes.map(m=>m.uuid),geometryIds:entry.runtime.meshes.map(m=>m.geometry.uuid)}:null;},
  dispose(){if(disposed)return;disposed=true;for(const entry of entries.values()){entry.group.removeFromParent();entry.runtime.disposeMaterials?.();}for(const g of [...pool.values()].flat())g.dispose();entries.clear();pool.clear();active=null;}
 };
}
