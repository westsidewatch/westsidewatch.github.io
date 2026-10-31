import * as THREE from 'three';
// Render-only exclusion of modern DSM fragments intruding into an occupied
// architectural foundation. Original DEM vertices, samplers and outside relief
// remain unchanged; this is not a reconstructed ancient ground surface.
export function createArchitecturalTerrainOcclusion(terrain,{platform,progress}){
 const materials=new Set();terrain.mesh.traverse(m=>{if(m.material)for(const material of [].concat(m.material))materials.add(material);});const originals=[];
 const bounds=new THREE.Box3().setFromObject(platform),floor=bounds.max.y-.12; // exclude decorative paving strips
 const textures=new Map();let selected=null;
 const uniforms={j3kFoundationUseMask:{value:0},j3kFoundationMask:{value:null},j3kFoundationActive:{value:0},j3kFoundationBounds:{value:new THREE.Vector4(bounds.min.x,bounds.max.x,bounds.min.z,bounds.max.z)},j3kFoundationFloor:{value:floor-.8}};
 for(const material of materials){const priorCompile=material.onBeforeCompile,priorKey=material.customProgramCacheKey;originals.push({material,priorCompile,priorKey});
 material.onBeforeCompile=function(shader,...args){priorCompile?.call(this,shader,...args);Object.assign(shader.uniforms,uniforms);shader.vertexShader='varying vec3 vJ3kGroundPosition;\n'+shader.vertexShader.replace('#include <begin_vertex>','#include <begin_vertex>\nvJ3kGroundPosition=(modelMatrix*vec4(transformed,1.0)).xyz;');shader.fragmentShader='varying vec3 vJ3kGroundPosition; uniform float j3kFoundationActive; uniform vec4 j3kFoundationBounds; uniform float j3kFoundationFloor; uniform float j3kFoundationUseMask; uniform sampler2D j3kFoundationMask;\n'+shader.fragmentShader.replace('void main() {',`void main() {
 if(j3kFoundationActive>.5 && vJ3kGroundPosition.x>j3kFoundationBounds.x && vJ3kGroundPosition.x<j3kFoundationBounds.y && vJ3kGroundPosition.z>j3kFoundationBounds.z && vJ3kGroundPosition.z<j3kFoundationBounds.w && vJ3kGroundPosition.y>j3kFoundationFloor && (j3kFoundationUseMask<.5 || texture2D(j3kFoundationMask,(vJ3kGroundPosition.xz-j3kFoundationBounds.xz)/(j3kFoundationBounds.yw-j3kFoundationBounds.xz)).r>.5)) discard;`);};
 material.customProgramCacheKey=()=>`${priorKey.call(material)}:j3k-occupied-foundation-v1`;material.needsUpdate=true;}
 function apply(alternative=null){
  const target=alternative||platform,foundation=alternative?.userData.occupiedFoundation;selected=foundation||null;
  let visible=true;for(let p=target;p;p=p.parent)visible&&=p.visible;
  const actualFloor=foundation?.floor??floor,clip=Array.isArray(target.material)?target.material[0].clippingPlanes:target.material.clippingPlanes,floorVisible=!clip?.some(p=>p.normal.y===-1&&p.constant<actualFloor);
  uniforms.j3kFoundationActive.value=visible&&(alternative||progress.value>=.16)&&floorVisible?1:0;
  uniforms.j3kFoundationFloor.value=foundation?actualFloor-.15:floor-.8;
  uniforms.j3kFoundationUseMask.value=foundation?1:0;
  if(foundation){const key=JSON.stringify(foundation.polygons||[foundation.polygon]);let cached=textures.get(key);if(!cached){const polygon=foundation.polygon,x=polygon.map(p=>p.x),z=polygon.map(p=>p.z),box=new THREE.Vector4(Math.min(...x),Math.max(...x),Math.min(...z),Math.max(...z)),canvas=document.createElement('canvas');canvas.width=canvas.height=1024;const c=canvas.getContext('2d');c.fillStyle='white';for(const part of foundation.polygons||[polygon]){c.beginPath();part.forEach((p,i)=>c[i?'lineTo':'moveTo']((p.x-box.x)/(box.y-box.x)*1024,(p.z-box.z)/(box.w-box.z)*1024));c.closePath();c.fill();}const rgba=c.getImageData(0,0,1024,1024).data,data=new Uint8Array(1024*1024);for(let i=0;i<data.length;i++)data[i]=rgba[i*4+3];const texture=new THREE.DataTexture(data,1024,1024,THREE.RedFormat);texture.needsUpdate=true;texture.flipY=false;texture.minFilter=texture.magFilter=THREE.NearestFilter;cached={box,texture};textures.set(key,cached);}uniforms.j3kFoundationBounds.value.copy(cached.box);uniforms.j3kFoundationMask.value=cached.texture;}
  else uniforms.j3kFoundationBounds.value.set(bounds.min.x,bounds.max.x,bounds.min.z,bounds.max.z);
 }
 return {apply,diagnostics:()=>({active:!!uniforms.j3kFoundationActive.value,bounds:uniforms.j3kFoundationBounds.value.toArray(),floor:uniforms.j3kFoundationFloor.value,foundationType:selected?'mapped-court':'herodian-rectangle',demPositionsChanged:false,ancientGroundVerified:false}),dispose(){for(const {texture}of textures.values())texture.dispose();for(const {material,priorCompile,priorKey}of originals){material.onBeforeCompile=priorCompile;material.customProgramCacheKey=priorKey;material.needsUpdate=true;}}};
}
