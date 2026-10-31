import {geographicToENU} from './terrain-runtime.js';
import {lifecycleStateAtPosition} from './construction-engine.js';
export function compileWaterDefenseRegistration(data,origin){
 if(data?.schema!=='j3k.water-defense.registration.v1'||!Array.isArray(data.objects)||!Array.isArray(data.scope)||!data.scope.length||![origin?.lat,origin?.lon].every(Number.isFinite))throw new Error('Invalid water/defense registration');
 const ids=new Set();
 const objects=data.objects.map(object=>{
  if(!object.id||!object.label||ids.has(object.id)||!object.sources?.length||!object.sources.every(url=>typeof url==='string'&&url.startsWith('https://'))||!['fortification','water-fortification'].includes(object.kind)||!object.gap||!['observed','reconstructed','inferred','disputed'].includes(object.confidence)||!object.lifecycleEvents?.length)throw new Error('Invalid water/defense object');ids.add(object.id);
  if(object.geometry||object.linework||object.footprint)throw new Error('Unreviewed historical geometry is not permitted in point registration');
  let point=null;
  if(object.reference){const r=object.reference;if(![r.lat,r.lon].every(Number.isFinite)||Math.abs(r.lat)>90||Math.abs(r.lon)>180||!r.source||!r.attribution||r.accuracy!=='approximate-modern-map-point-not-ancient-survey'||object.geometryStatus!=='modern-reference-point-only')throw new Error('Invalid modern reference point');const enu=geographicToENU(r.lat,r.lon,origin);point={x:enu.east,z:-enu.north};}
  if(object.geometryStatus==='modern-reference-point-only'&&!point)throw new Error('Missing reference coordinates');
  return{...object,point,geometry:{primitive:point?'point':null,status:object.geometryStatus,frame:'canonical-dem-enu',...(point?{point,role:'modern-reference-only'}:{})},geometryVerified:false};
 });
 return{...data,objects};
}
export function appendWaterDefenseLedger(packs,lifecycle,data){
 const compiled=compileWaterDefenseRegistration(data,{lat:31.773235,lon:35.2368303});
 for(const object of compiled.objects){
  if(packs.packs.some(p=>p.objects?.some(o=>o.id===object.id))||lifecycle.objects.some(o=>o.id===object.id))throw new Error(`Duplicate water/defense object ${object.id}`);
  const phase=object.lifecycleEvents[0].phase;let pack=packs.packs.find(p=>p.phase===phase);if(!pack){pack={phase,label:phase,objects:[],derived:true};packs.packs.push(pack);}
  pack.objects.push({...object,geometry:{status:object.geometryStatus,primitive:null,authority:'reference-pending-terrain-registration'},evidence:object.confidence,limitations:[object.gap,...data.limitations],rendererBinding:'water-defense-reference-only'});
  lifecycle.objects.push({id:object.id,lifecycleEvents:object.lifecycleEvents});
 }
}
export function bindWaterDefenseCore(core,compiled){for(const object of compiled.objects){const record=core.get(object.id);if(!record)throw new Error('Missing water/defense ledger object');core.register({...record,lifecycle:{...record.lifecycle,built:object.lifecycleEvents.find(e=>['build','rebuild'].includes(e.state))?.phase??null},geometry:object.geometry,metadata:{...record.metadata,rendererBinding:'water-defense-reference-only',geometryVerified:false,reference:object.reference||null,geometryGap:object.gap}});}}
export function waterDefenseState(compiled,timeline,position){const phase=timeline.phases[Math.floor(position)]?.id;if(!compiled.scope.includes(phase))return null;return{phase,objects:compiled.objects.map(o=>({...o,state:lifecycleStateAtPosition({lifecycleEvents:o.lifecycleEvents},timeline,position)})),limitations:compiled.limitations};}
