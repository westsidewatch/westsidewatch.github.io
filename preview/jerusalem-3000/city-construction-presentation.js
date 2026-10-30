import {isPresentedLandmark} from './landmark-presentation-policy.js';
import * as THREE from 'three';
import {cityObjectIdForMesh} from './city-lifecycle-projection.js';
const clamp=v=>Math.max(0,Math.min(1,v)),smooth=v=>{v=clamp(v);return v*v*(3-2*v);};
const LANDMARK_NAMES={'j3k:object:temple-mount-enclosure-herodian':'聖殿山平台','j3k:object:inner-temple':'希律聖殿','j3k:object:royal-stoa':'皇家柱廊','j3k:object:antonia':'安東尼堡'};
const LATE=new Set(['ottoman','outside-walls','modern']);
function visible(m){for(let p=m;p;p=p.parent)if(!p.visible)return false;return true;}
function role(record,mesh){if(['road','route','water','wall','gate'].includes(record.type))return'infrastructure';if(record.type==='monument')return'core';return mesh.userData.overview?'housing':null;}
// Display staging only. It never writes records/events, moves geometry, or turns
// equal renderer buffers into evidence for physical survival.
export function createCityConstructionPresentation({root,getRecord}){
 const entries=new Map(),phases=new Map();let lastPhase=null,previous=null,stats={},landmarks=[];
 function entry(mesh){
  let e=entries.get(mesh);if(e)return e;
  const original=mesh.material,plane=new THREE.Plane(new THREE.Vector3(0,-1,0),1e9),materials=(Array.isArray(original)?original:[original]).map(m=>{const c=m.clone();c.clippingPlanes=[...(m.clippingPlanes||[]),plane];c.clipShadows=true;return c;});
  mesh.material=Array.isArray(original)?materials:materials[0];e={mesh,original,materials,plane};entries.set(mesh,e);return e;
 }
 function apply({phaseId,phaseIndex,position,active=false,ruin=false}){
  root.updateMatrixWorld(true);const groups=new Map();
  root.traverse(mesh=>{
   if(!mesh.isMesh||!visible(mesh)||mesh.userData.displayAnnotation)return;
   const id=cityObjectIdForMesh(mesh),record=id&&getRecord(id);if(!record)return;const kind=role(record,mesh);if(!kind)return;
   if(!groups.has(id))groups.set(id,{id,record,kind,items:[],box:new THREE.Box3()});
   const g=groups.get(id);g.items.push(mesh);g.box.union(new THREE.Box3().setFromObject(mesh));
  });
  const descriptors=new Map([...groups].map(([id,g])=>[id,g.items.map(m=>`${m.geometry.uuid}:${m.matrixWorld.elements.join(',')}:${m.userData.cityRuinFactor??1}`).sort().join('|')]));
  if(lastPhase!==phaseId){previous=lastPhase?{phase:lastPhase,index:phases.get(lastPhase)?.index,descriptors:phases.get(lastPhase)?.descriptors,defenseDescriptors:phases.get(lastPhase)?.defenseDescriptors}:null;lastPhase=phaseId;}
  const adjacent=active&&previous?.index===phaseIndex-1;
  const equalPrior=new Set(adjacent&&LATE.has(previous.phase)&&LATE.has(phaseId)?previous.descriptors.values():[]);
  const ranks=new Map();for(const kind of ['infrastructure','core','housing']){
   const list=[...groups.values()].filter(g=>g.kind===kind).sort((a,b)=>(a.box.min.x+a.box.min.z)-(b.box.min.x+b.box.min.z)||a.id.localeCompare(b.id));list.forEach((g,i)=>ranks.set(g.id,i/Math.max(1,list.length-1)));
  }
  const fraction=position-phaseIndex;let growing=0,complete=0,waiting=0,kept=0;const counts={infrastructure:0,core:0,housing:0},growingByRole={infrastructure:0,core:0,housing:0};
  landmarks=[];
  for(const g of groups.values()){
   const r=ranks.get(g.id),same=adjacent&&(previous.descriptors.get(g.id)===descriptors.get(g.id)||equalPrior.has(descriptors.get(g.id))||(g.record.metadata?.defenseTimeline&&previous.defenseDescriptors?.has(descriptors.get(g.id))));
   const offsets=(g.record.lifecycle?.events||[]).filter(e=>e.phase===phaseId&&['build','rebuild','transform','expand'].includes(e.state)&&(e.offset||0)<=fraction).map(e=>e.offset||0),offset=Math.max(0,...offsets);
   const base=g.kind==='housing'?.08+r*.42:g.kind==='core'?.06+r*.18:.01+r*.08,duration=g.kind==='core'?.38:.22;
   const start=Math.max(base,offset),end=Math.min(.95,Math.max(start+.08,start+duration));
   const amount=!active||ruin||same||g.items.every(m=>m.userData.defenseMode==='ruin')?1:smooth((fraction-start)/(end-start));
   if(same)kept++;if(amount>=1)complete++;else if(amount>0){growing++;growingByRole[g.kind]++;}else waiting++;
   if(amount>0)counts[g.kind]++;
   if(isPresentedLandmark(g.record)&&amount>0){const name=LANDMARK_NAMES[g.id]||g.record.metadata?.name||g.record.metadata?.label||g.record.source?.label||'公共核心';landmarks.push({id:g.id,kind:g.record.type,label:name.replace('（概略量體）','')+'（示意）',x:(g.box.min.x+g.box.max.x)/2,z:(g.box.min.z+g.box.max.z)/2,y:g.box.min.y+amount*(g.box.max.y-g.box.min.y),confidence:g.record.confidence,description:`${name}；${g.record.confidence}。${g.record.metadata?.referencePeriod||''}。標記指向實際顯示量體中心，非測繪位置；不證明古地表或跨期原構件存續。`});}
   for(const mesh of g.items){if(active){const e=entry(mesh);e.plane.constant=amount>=1?1e9:g.box.min.y-.01+amount*(g.box.max.y-g.box.min.y+.02);}else if(entries.has(mesh))entries.get(mesh).plane.constant=1e9;}
  }
  phases.set(phaseId,{index:phaseIndex,descriptors,defenseDescriptors:new Set([...groups.values()].filter(g=>g.record.metadata?.defenseTimeline).map(g=>descriptors.get(g.id)))});
  stats={phase:phaseId,active,fraction,objects:groups.size,complete,growing,waiting,displayKept:kept,visibleByRole:counts,growingByRole,ownedMaterials:[...entries.values()].reduce((n,e)=>n+e.materials.length,0),historicalSurvivalInferred:false,geometryTransformsChanged:false};
  return stats;
 }
 return {apply,landmarks:()=>structuredClone(landmarks),diagnostics:()=>structuredClone(stats),dispose(){for(const e of entries.values()){e.mesh.material=e.original;for(const m of e.materials)m.dispose();}entries.clear();phases.clear();}};
}
