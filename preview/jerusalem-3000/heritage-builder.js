import * as THREE from 'three';
import {mergeGeometries} from 'three/addons/utils/BufferGeometryUtils.js';

/**
 * Jerusalem 3000 port of lhlGitHub/threejs-architecture-effects HeritageBuilder.
 * Source authority: assets/starter/src/heritage/builder.ts @ 693ca2ec1193e7355054f14d7deb1427439a24d0 (MIT).
 *
 * The important source grammar is preserved rather than approximated:
 * - each physical piece carries aBuild = [start,duration,lift]
 * - all batches share one uBuildProgress uniform
 * - vertex motion is deterministic and therefore exactly reversible by scrubbing progress
 * - custom depth materials receive the identical construction motion, so shadows agree with geometry
 *
 * Jerusalem evidence ledgers remain the geometry authority. This class only supplies construction mechanics.
 */
export class HeritageBuilder{
  constructor(materials){this.materials=materials;this.batches=new Map();this.cache=new Map();this.transform=new THREE.Object3D();this.progress={value:0};this.meshes=[];this.depths=[];this.pieces=0;}
  add(geometry,material,start,options={}){
    const {p=[0,0,0],r=[0,0,0],s=[1,1,1],shade=1,tint=[1,1,1],duration=.013,lift=.45}=options;
    this.transform.position.set(...p);this.transform.rotation.set(...r);this.transform.scale.set(...s);this.transform.updateMatrix();
    const g=geometry.index?geometry.toNonIndexed():geometry.clone();g.applyMatrix4(this.transform.matrix);const n=g.getAttribute('position').count;
    const schedule=new Float32Array(n*3),color=new Float32Array(n*3);const normal=g.getAttribute('normal');
    for(let i=0;i<n;i++){schedule.set([start,duration,lift],i*3);const underside=normal?THREE.MathUtils.lerp(.76,1,THREE.MathUtils.smoothstep(normal.getY(i),-.8,.2)):1;color.set(tint.map(v=>v*shade*underside),i*3);}
    g.setAttribute('aBuild',new THREE.BufferAttribute(schedule,3));g.setAttribute('color',new THREE.BufferAttribute(color,3));
    if(!g.getAttribute('uv'))g.setAttribute('uv',new THREE.BufferAttribute(new Float32Array(n*2),2));if(!g.getAttribute('normal'))g.computeVertexNormals();
    for(const name of Object.keys(g.attributes))if(!['position','normal','uv','aBuild','color'].includes(name))g.deleteAttribute(name);
    if(!this.batches.has(material))this.batches.set(material,[]);this.batches.get(material).push(g);this.pieces++;
  }
  geo(key,fn){if(!this.cache.has(key))this.cache.set(key,fn());return this.cache.get(key);}
  box(size,p,material,start,options={}){const key=`box:${size.join(',')}`;const geometry=this.geo(key,()=>new THREE.BoxGeometry(...size));this.add(geometry,material,start,{...options,p});}
  finish(scene){
    const inject=m=>{m.onBeforeCompile=shader=>{shader.uniforms.uBuildProgress=this.progress;shader.vertexShader='attribute vec3 aBuild; uniform float uBuildProgress; varying float vConstruction;\n'+shader.vertexShader.replace('#include <begin_vertex>',`#include <begin_vertex>\nfloat buildT=clamp((uBuildProgress-aBuild.x)/max(.0001,aBuild.y),0.0,1.0);\nvConstruction=buildT;\nfloat settle=sin(buildT*6.2831853)*pow(1.0-buildT,2.0)*0.035;\ntransformed.y+=aBuild.z*(pow(1.0-buildT,3.0)-settle);`);shader.fragmentShader='varying float vConstruction;\n'+shader.fragmentShader.replace('void main() {','void main() { if(vConstruction<=0.0) discard;');};m.customProgramCacheKey=()=> 'j3k-heritage-solid-assembly-v1';};
    for(const [name,geometries] of this.batches){const combined=mergeGeometries(geometries,false);if(!combined)throw new Error(`Unable to merge Jerusalem construction batch: ${name}`);combined.computeBoundingSphere();geometries.forEach(g=>g.dispose());const material=this.materials[name];inject(material);const mesh=new THREE.Mesh(combined,material);mesh.name=`heritage-${name}`;mesh.receiveShadow=true;mesh.castShadow=true;const depth=new THREE.MeshDepthMaterial({depthPacking:THREE.RGBADepthPacking});inject(depth);mesh.customDepthMaterial=depth;this.depths.push(depth);this.meshes.push(mesh);scene.add(mesh);}
    this.cache.forEach(g=>g.dispose());this.cache.clear();this.batches.clear();return this.meshes;
  }
  setProgress(value){this.progress.value=Math.max(0,Math.min(1,value));}
  dispose(){this.meshes.forEach(m=>{m.geometry.dispose();m.removeFromParent();});this.depths.forEach(m=>m.dispose());this.meshes.length=0;this.depths.length=0;}
}
