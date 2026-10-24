import {allowsEvidence} from './evidence-visibility.js';
import * as THREE from 'three';
import {inheritanceFor,applyInheritedMorphology,inheritanceTransitionIndex} from './phase2-inheritance.js';
import {buildEraUrbanMorphology} from './phase2-era-morphology.js';
import {buildPhase2UrbanMorphology} from './phase2-urban-morphology.js';
import {buildOttomanUrbanMorphology} from './ottoman-urban-morphology.js';
import {deboxHerodianLowerCity} from './herodian-lower-city-debox.js';
import {applyArchitectureAssembly} from './architecture-assembly-core.js';

const SPECIAL=new Set(['david-solomon','herodian-jesus','crusader']);
const GENERIC=new Set(['chalcolithic-early-bronze','middle-bronze','late-bronze-iron1','late-first-temple','persian-nehemiah','hellenistic-hasmonean','aelia','byzantine','early-islamic','ayyubid-mamluk','outside-walls','modern']);
const COLORS={observed:0x8d8069,reconstructed:0xb49b70,inferred:0xa99b84,disputed:0x8e665c};
function makeMaterials(){const out={};for(const[name,color]of Object.entries(COLORS))out[name]=new THREE.MeshStandardMaterial({color,roughness:.94,transparent:true,opacity:name==='disputed'?.5:.82});return out}
function build(group,id,materials,terrain){let runtime;if(id==='ottoman')runtime=buildOttomanUrbanMorphology(group,materials,terrain,{progress:1});else if(GENERIC.has(id))runtime=buildEraUrbanMorphology(group,id,materials,terrain,{progress:1});else if(SPECIAL.has(id))runtime=buildPhase2UrbanMorphology(group,id,materials,terrain,{progress:1});else return null;if(id==='herodian-jesus'&&runtime)runtime=deboxHerodianLowerCity(group,runtime,materials,terrain);if(runtime)runtime=applyArchitectureAssembly(group,runtime,{replaceRatio:.42});return runtime}
export {inheritanceTransitionIndex};
export function createInheritanceLayer(parent,{terrain,phases=null}={}){
 if(!terrain?.mesh||!terrain?.grid||typeof terrain.heightAtWorld!=='function')throw new Error('Inheritance requires canonical DEM terrain');
 const transitions=phases?inheritanceTransitionIndex(phases):[],group=new THREE.Group();group.name='phase2-inherited-city';parent.add(group);
 const materials=makeMaterials();let runtime=null,currentPhase='',requestedPhase='',evidenceMode='all',requestedVisible=true;
 function refreshVisibility(){group.visible=requestedVisible&&Boolean(runtime)&&allowsEvidence(evidenceMode,'inferred');}
 function clear(){if(runtime?.meshes)for(const mesh of runtime.meshes){group.remove(mesh);mesh.geometry?.dispose?.();}runtime=null;currentPhase='';}
 function setPhase(phaseId,progress=0){
  requestedPhase=phaseId;
  if(currentPhase===phaseId&&runtime){setProgress(phaseId,progress);return runtime;}
  clear();const rule=inheritanceFor(phaseId);if(!rule){group.visible=false;return null;}
  runtime=build(group,rule.from,materials,terrain);if(!runtime){group.visible=false;return null;}
  currentPhase=phaseId;
  // These IDs identify display instructions, not surviving city objects. Never bind
  // them to source object IDs or fabricate predecessor/successor links.
  runtime.meshes.forEach((mesh,index)=>{mesh.userData.provisionalInheritance={id:`j3k:inheritance-preview:${phaseId}:${index}`,sourcePhase:rule.from,targetPhase:phaseId,sourceObjectId:null,selectionIndex:index,survivalVerified:false,geometryVerified:false};});
  applyInheritedMorphology(runtime,{retain:rule.retain,ruin:rule.ruin,progress});requestedVisible=true;refreshVisibility();
  return {phaseId,from:rule.from,retain:rule.retain,ruin:!!rule.ruin,meshes:runtime.meshes,architectureAssembly:runtime.architectureAssembly};
 }
 function setProgress(phaseId,progress=0){if(!runtime||currentPhase!==phaseId)return;const rule=inheritanceFor(phaseId);if(rule)applyInheritedMorphology(runtime,{retain:rule.retain,ruin:rule.ruin,progress});}
 function diagnostics(phaseId=requestedPhase){
  const entry=transitions.find(t=>t.to===phaseId),active=group.visible&&currentPhase===phaseId&&Boolean(runtime);
  return {phase:phaseId,transition:entry?structuredClone(entry):null,status:active?'provisional-overlay-visible':currentPhase===phaseId?'hidden':requestedPhase===phaseId?'source-generator-unavailable':'not-requested',
   evidenceMode,confidence:'inferred',visibleComponents:active?runtime.meshes.filter(m=>m.visible).length:0,tracedComponents:active?runtime.meshes.filter(m=>m.visible&&m.userData.provisionalInheritance).length:0,historicalFate:'unresolved',survivalVerified:false,reuseLinksVerified:false};
 }
 function dispose(){clear();for(const material of Object.values(materials))material.dispose?.();parent.remove(group);}
 return {group,setPhase,setProgress,setVisible(value){requestedVisible=Boolean(value);refreshVisibility();},setEvidenceMode(mode){allowsEvidence(mode,'inferred');evidenceMode=mode;refreshVisibility();},dispose,diagnostics,transitionIndex:()=>structuredClone(transitions),terrainAuthority:'canonical-dem-rendered-triangles',get runtime(){return runtime;}};
}
