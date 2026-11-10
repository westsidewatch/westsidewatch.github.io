import * as THREE from 'three';
import {lifecycleStateAtPosition} from './construction-engine.js';
const IDS={'spring-tower':'j3k:object:gihon-spring-tower','protected-access':'j3k:object:gihon-protected-access-hypothesis','carved-installation-outline':'j3k:object:gihon-carved-installation-hypothesis'};
export function createWaterDefenseModelAdapter({runtime,core,registration}){
 const meshes=runtime.defenseMeshes(),variants=registration.towerVariants;
 if(!meshes.length||variants?.length!==2||variants[0].id!=='middle-bronze-hypothesis'||variants[0].displayPhase!=='middle-bronze'||variants[1].id!=='iron-age-dating'||variants[1].displayPhase!==null)throw new Error('Invalid water-defense variants');
 const timeline={phases:[...core.phases.values()]};let selected=variants[0].id,position=0;
 const bindings=new Map();
 for(const mesh of meshes){const kind=mesh.userData.cityObject.kind,id=IDS[kind];if(!core.get(id))throw new Error(`Missing water-defense object ${id}`);if(!bindings.has(id))bindings.set(id,[]);const parts=bindings.get(id);mesh.userData.cityObject={...mesh.userData.cityObject,objectId:id,componentId:`${id}:component:${parts.length}`,confidence:core.get(id).confidence};parts.push(mesh);}
 for(const [id,parts]of bindings){const bounds=new THREE.Box3();parts.forEach(m=>bounds.expandByObject(m));const r=core.get(id);core.register({...r,geometry:{primitive:'component-assembly',status:'inferred-middle-bronze-variant',frame:'canonical-dem-enu',bounds:{min:bounds.min.toArray(),max:bounds.max.toArray()}},metadata:{...r.metadata,rendererBinding:'water-defense-model-adapter-v1',geometryVerified:false,geometryReuseVerified:false,geometryValidityPhases:['middle-bronze'],componentIds:parts.map(m=>m.userData.cityObject.componentId),datingVariant:id===IDS['spring-tower']?selected:null}});}
 return{
  get selectedVariant(){return selected;},
  setVariant(id){if(!variants.some(v=>v.id===id))throw new Error('Unknown tower dating variant');selected=id;const r=core.get(IDS['spring-tower']);core.register({...r,metadata:{...r.metadata,datingVariant:selected}});},
  apply({position:value,evidenceAllowed=()=>true}){position=value;const phase=timeline.phases[Math.floor(value)]?.id;for(const m of meshes){const r=core.get(m.userData.cityObject.objectId),state=lifecycleStateAtPosition({lifecycleEvents:r.lifecycle.events},timeline,value),tower=m.userData.cityObject.kind==='spring-tower';m.userData.cityObject.ledgerState=state;m.visible=phase==='middle-bronze'&&evidenceAllowed(r.confidence)&&(tower?selected==='middle-bronze-hypothesis':['build','transform'].includes(state));}},
  diagnostics(){return{selectedVariant:selected,position,bindingIds:[...bindings.keys()],visibleTowerComponents:meshes.filter(m=>m.visible&&m.userData.cityObject.kind==='spring-tower').length,componentIdentity:meshes.map(m=>m.userData.cityObject.componentId).join('|'),geometryVerified:false,geometryReuseVerified:false,datingAuthority:'explicit-display-hypothesis-not-resolved-chronology'};},
 };
}
