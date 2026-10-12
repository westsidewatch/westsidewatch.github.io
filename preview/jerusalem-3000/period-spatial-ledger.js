import {compilePersianSanctuary} from './persian-sanctuary-layout.js';
import {compilePeriodRegistration} from './period-spatial-registration.js';
// One spatial source derives both the public ledger and renderer registration IDs.
export function appendPeriodSpatialLedger(packs,lifecycle,data) {
 const sanctuary=compilePersianSanctuary(data);
 const existing=new Set(packs.packs.flatMap(p=>(p.objects||[]).map(o=>o.id)));
 const append=(pack,id,label,kind,events,sources=data.sources,limitations=data.limitations)=>{
  if(existing.has(id)||lifecycle.objects.some(o=>o.id===id))throw new Error(`Duplicate period spatial object ${id}`);
  existing.add(id);pack.objects.push({id,label,kind,confidence:'inferred',evidence:'inferred',geometry:'withheld-pending-period-spatial-adapter',rendererBinding:'ledger-only-pending-adapter',sources,limitations});
  lifecycle.objects.push({id,lifecycleEvents:events});
 };
 for(const phase of Object.keys(data.phases)){
  let pack=packs.packs.find(p=>p.phase===phase);
  if(!pack){pack={phase,label:phase,objects:[],derived:true};packs.packs.push(pack);}
  pack.objects ||= [];
  const registration=compilePeriodRegistration(data,phase,data.anchor);
  const events=phase==='late-first-temple'?[{phase,state:'build',authority:'independent-illustrative-spatial-layout'},{phase:'babylonian-destruction',state:'transform',authority:'schematic-layout-through-destruction-not-verified-street-survival'},{phase:'persian-nehemiah',state:'unresolved',authority:'specific-layout-continuity-unverified'}]:[{phase,state:'rebuild',authority:'independent-illustrative-spatial-layout'},{phase:'hellenistic-hasmonean',state:'unresolved',authority:'later-layout-continuity-unverified'}];
  for(const [kind,items,type] of [['地區',registration.districts,'urban-envelope'],['道路',registration.roads,'transport-network'],['聖區保留',registration.reservations,'urban-envelope']])for(const item of items)append(pack,item.id,`${kind} · ${item.id.split(':').at(-1)}（推定）`,type,events);
 }
 const pack=packs.packs.find(p=>p.phase===sanctuary.phase),events=[{phase:sanctuary.phase,state:'build',authority:'illustrative-sanctuary-access'},{phase:'hellenistic-hasmonean',state:'unresolved',authority:'later-geometry-unverified'}];
 append(pack,sanctuary.gate.id,'早期第二聖殿院落入口（推定）','gate',events,sanctuary.sources,sanctuary.limitations);
 append(pack,sanctuary.access.id,'波斯聖區入口動線（推定）','transport-network',events,sanctuary.sources,sanctuary.limitations);
}
export function bindPeriodSpatialCore(core,registration) {
 for(const items of [registration.districts,registration.roads,registration.reservations])for(const item of items){
  const record=core.get(item.id);if(!record)throw new Error(`Missing shared period object ${item.id}`);
  core.register({...record,geometry:item.geometry||{primitive:'polygon',frame:'scene-local-metres',polygon:item.polygon,status:'inferred-sanctuary-reservation'},metadata:{...record.metadata,rendererBinding:'period-spatial-adapter-v1',geometryVerified:false,geometryValidityPhases:registration.phase==='late-first-temple'?['late-first-temple','babylonian-destruction']:[registration.phase]}});
 }
}
