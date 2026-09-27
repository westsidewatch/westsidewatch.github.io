import * as THREE from 'three';
import {inheritanceFor,applyInheritedMorphology} from './phase2-inheritance.js';
import {buildEraUrbanMorphology} from './phase2-era-morphology.js';
import {buildPhase2UrbanMorphology} from './phase2-urban-morphology.js';
import {buildOttomanUrbanMorphology} from './ottoman-urban-morphology.js';

const SPECIAL=new Set(['david-solomon','herodian-jesus','crusader']);
const GENERIC=new Set(['chalcolithic-early-bronze','middle-bronze','late-bronze-iron1','late-first-temple','persian-nehemiah','hellenistic-hasmonean','aelia','byzantine','early-islamic','ayyubid-mamluk','outside-walls','modern']);
function build(group,id,materials,terrain){if(id==='ottoman')return buildOttomanUrbanMorphology(group,materials,terrain,{progress:1});if(GENERIC.has(id))return buildEraUrbanMorphology(group,id,materials,terrain,{progress:1});if(SPECIAL.has(id))return buildPhase2UrbanMorphology(group,id,materials,terrain,{progress:1});return null}
export function createInheritanceLayer(parent){const group=new THREE.Group();group.name='phase2-inherited-city';parent.add(group);let runtime=null;function clear(){if(runtime?.meshes)for(const mesh of runtime.meshes){group.remove(mesh);mesh.geometry?.dispose?.()}runtime=null}function setPhase(phaseId,materials,terrain,progress=0){clear();const rule=inheritanceFor(phaseId);if(!rule)return null;runtime=build(group,rule.from,materials,terrain);if(!runtime)return null;applyInheritedMorphology(runtime,{retain:rule.retain,ruin:rule.ruin,progress});group.visible=true;return{phaseId,from:rule.from,retain:rule.retain,ruin:!!rule.ruin,meshes:runtime.meshes}}function setProgress(phaseId,progress=0){if(!runtime)return;const rule=inheritanceFor(phaseId);if(!rule)return;applyInheritedMorphology(runtime,{retain:rule.retain,ruin:rule.ruin,progress})}function setVisible(value){group.visible=!!value}function dispose(){clear();parent.remove(group)}return{group,setPhase,setProgress,setVisible,dispose,get runtime(){return runtime}}}
