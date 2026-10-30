import * as THREE from 'three';
// Render-only exclusion of modern DSM fragments intruding into an occupied
// architectural foundation. Original DEM vertices, samplers and outside relief
// remain unchanged; this is not a reconstructed ancient ground surface.
export function createArchitecturalTerrainOcclusion(terrain,{platform,progress}){
 const materials=new Set();terrain.mesh.traverse(m=>{if(m.material)for(const material of [].concat(m.material))materials.add(material);});const originals=[];
 const bounds=new THREE.Box3().setFromObject(platform),floor=bounds.max.y-.12; // exclude decorative paving strips
 const uniforms={j3kFoundationActive:{value:0},j3kFoundationBounds:{value:new THREE.Vector4(bounds.min.x,bounds.max.x,bounds.min.z,bounds.max.z)},j3kFoundationFloor:{value:floor-.8}};
 for(const material of materials){const priorCompile=material.onBeforeCompile,priorKey=material.customProgramCacheKey;originals.push({material,priorCompile,priorKey});
 material.onBeforeCompile=function(shader,...args){priorCompile?.call(this,shader,...args);Object.assign(shader.uniforms,uniforms);shader.vertexShader='varying vec3 vJ3kGroundPosition;\n'+shader.vertexShader.replace('#include <begin_vertex>','#include <begin_vertex>\nvJ3kGroundPosition=(modelMatrix*vec4(transformed,1.0)).xyz;');shader.fragmentShader='varying vec3 vJ3kGroundPosition; uniform float j3kFoundationActive; uniform vec4 j3kFoundationBounds; uniform float j3kFoundationFloor;\n'+shader.fragmentShader.replace('void main() {',`void main() {
 if(j3kFoundationActive>.5 && vJ3kGroundPosition.x>j3kFoundationBounds.x && vJ3kGroundPosition.x<j3kFoundationBounds.y && vJ3kGroundPosition.z>j3kFoundationBounds.z && vJ3kGroundPosition.z<j3kFoundationBounds.w && vJ3kGroundPosition.y>j3kFoundationFloor) discard;`);};
 material.customProgramCacheKey=()=>`${priorKey.call(material)}:j3k-occupied-foundation-v1`;material.needsUpdate=true;}
 function apply(){let visible=true;for(let p=platform;p;p=p.parent)visible&&=p.visible;const clip=Array.isArray(platform.material)?platform.material[0].clippingPlanes:platform.material.clippingPlanes;const floorVisible=!clip?.some(p=>p.normal.y===-1&&p.constant<floor);uniforms.j3kFoundationActive.value=visible&&progress.value>=.16&&floorVisible?1:0;}
 return {apply,diagnostics:()=>({active:!!uniforms.j3kFoundationActive.value,bounds:uniforms.j3kFoundationBounds.value.toArray(),floor:uniforms.j3kFoundationFloor.value,demPositionsChanged:false,ancientGroundVerified:false}),dispose(){for(const {material,priorCompile,priorKey}of originals){material.onBeforeCompile=priorCompile;material.customProgramCacheKey=priorKey;material.needsUpdate=true;}}};
}
