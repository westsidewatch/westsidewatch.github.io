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
export function createPersistentCityWorld({parent,phases,build,buildAsync,publish}){
 if(!parent?.isObject3D||!phases?.length||new Set(phases).size!==phases.length||typeof build!=='function'||typeof publish!=='function')throw new Error('Invalid persistent city world');
 const allowed=new Set(phases),entries=new Map(),pool=new Map();let active=null,builds=0,hits=0,disposed=false;const timings=new Map();let lastActivation=null,pending=null,requestState={phase:null,status:'idle'};
 const releaseRaw=runtime=>{for(const mesh of runtime?.meshes||[]){mesh.removeFromParent();mesh.geometry.dispose();}runtime?.disposeMaterials?.();};
 function activate(phase,prepared=null){
  if(disposed)throw new Error('Persistent city world disposed');
  if(phase!==null&&!allowed.has(phase))throw new Error(`Unsupported persistent phase: ${phase}`);
  const started=performance.now();let cacheHit=false;
  let next=phase===null?null:entries.get(phase);
  if(phase!==null&&!next){
   const group=prepared?.group||new THREE.Group();group.name=`j3k-world:${phase}`;group.visible=false;let runtime;
   try{
    const buildStarted=performance.now();runtime=prepared?.runtime||build(group,phase);const buildMilliseconds=prepared?.buildMilliseconds??(performance.now()-buildStarted);
    if(runtime.phaseId!==phase||!runtime.meshes?.length||runtime.meshes.some(m=>m.parent!==group))throw new Error('Invalid persistent phase runtime');
    const publishStarted=performance.now(),binding=publish(runtime),publicationMilliseconds=performance.now()-publishStarted,dedupStarted=performance.now();
    for(const mesh of runtime.meshes){
     const raw=mesh.geometry,key=signature(raw),bucket=pool.get(key)||[],existing=bucket.find(g=>equalGeometry(g,raw));
     if(existing){mesh.geometry=existing;raw.dispose();}else{bucket.push(raw);pool.set(key,bucket);}
    }
    timings.set(phase,{buildMilliseconds,publicationMilliseconds,deduplicationMilliseconds:performance.now()-dedupStarted,totalMilliseconds:prepared?performance.now()-prepared.started:performance.now()-started});
    next={group,runtime,binding};parent.add(group);entries.set(phase,next);builds++;
   }catch(error){group.removeFromParent();releaseRaw(runtime);throw error;}
  }else if(next){hits++;cacheHit=true;}
  // Build and validate first: a failed target must leave the current city intact.
  if(active)active.group.visible=false;
  active=next;if(active)active.group.visible=true;
  lastActivation={phase,cacheHit,milliseconds:performance.now()-started};return next;
 }
 function cancel(){if(pending){pending.controller.abort();pending=null;}requestState={phase:null,status:'idle'};}
 async function request(phase){
  if(disposed)throw new Error('Persistent city world disposed');
  if(!allowed.has(phase))throw new Error(`Unsupported persistent phase: ${phase}`);
  if(pending?.phase===phase)return pending.promise;
  cancel();
  if(entries.has(phase)||!buildAsync){const cacheHit=entries.has(phase),entry=activate(phase);requestState={phase,status:'ready',cacheHit};return entry;}
  const group=new THREE.Group(),controller=new AbortController(),task={phase,controller,group};pending=task;requestState={phase,status:'generating',completed:0};const started=performance.now();
  task.promise=(async()=>{
   let runtime;
   try{
    runtime=await buildAsync(group,phase,{signal:controller.signal,onProgress:progress=>{if(pending===task)requestState={phase,status:'generating',...progress};}});
    if(disposed||controller.signal.aborted||pending!==task){releaseRaw(runtime);return null;}
    const entry=activate(phase,{group,runtime,started,buildMilliseconds:performance.now()-started});requestState={phase,status:'ready',cacheHit:false,schedule:runtime.generationSchedule};return entry;
   }catch(error){if(controller.signal.aborted||error.name==='AbortError')return null;if(pending===task)requestState={phase,status:'error',error:String(error)};throw error;}
   finally{if(pending===task)pending=null;}
  })();return task.promise;
 }
 return {
  activate,request,cancel,
  generationStatus:()=>({...requestState}),
  diagnostics(){
   const geometries=[...pool.values()].flat(),instances=[...entries.values()].flatMap(e=>e.runtime.meshes);
   return {generationStatus:{...requestState},generationTimings:Object.fromEntries([...timings].map(([k,v])=>[k,{...v}])),lastActivation:lastActivation?{...lastActivation}:null,timingScope:'build wall time includes cooperative yields on async requests; publication/deduplication are synchronous; excludes fetch, GPU and first visible frame',activePhase:active?.runtime.phaseId||null,phaseCapacity:allowed.size,cachedPhases:[...entries.keys()],builds,cacheHits:hits,meshInstances:instances.length,uniqueGeometries:geometries.length,geometryBufferBytes:geometries.reduce((n,g)=>n+geometryBytes(g),0),sameGeometryIsHistoricalReuse:false,historicalContinuityAccepted:false};
  },
  inspectPhase(phase){const entry=entries.get(phase);return entry?{groupId:entry.group.uuid,meshIds:entry.runtime.meshes.map(m=>m.uuid),geometryIds:entry.runtime.meshes.map(m=>m.geometry.uuid)}:null;},
  dispose(){if(disposed)return;disposed=true;cancel();for(const entry of entries.values()){entry.group.removeFromParent();entry.runtime.disposeMaterials?.();}for(const g of [...pool.values()].flat())g.dispose();entries.clear();pool.clear();timings.clear();lastActivation=null;active=null;}
 };
}
