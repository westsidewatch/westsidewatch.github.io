import assert from 'node:assert/strict';
import * as THREE from 'three';
import {readFile} from 'node:fs/promises';
import {createRoyalCity} from '../preview/jerusalem-3000/royal-city.js';
import {loadTemporalCityCore} from '../preview/jerusalem-3000/temporal-city-core-adapter.js';
import {invalidateCityData} from '../preview/jerusalem-3000/city-data-loader.js';
import {buildHerodianRoadGeometry} from '../preview/jerusalem-3000/herodian-road-geometry.js';
const base=new URL('../preview/jerusalem-3000/',import.meta.url),json=async p=>JSON.parse(await readFile(new URL(p,base)));
const timeline=await json('data/continuous-build-timeline.json'),data=await json('data/settlement/david-solomon.v1.json');
const original=globalThis.fetch;
try {
 globalThis.fetch=async url=>({ok:true,json:()=>json(url)});invalidateCityData();
 const terrain={grid:{origin:data.spring},heightAtWorld:(x,z)=>40+x*.03+z*.01};
 const {core}=await loadTemporalCityCore(timeline.phases,{terrain}),parent=new THREE.Group();
 const runtime=createRoyalCity(parent,{data,terrain,core});const apply=position=>runtime.apply({position,evidenceAllowed:()=>true,ruin:1});
 apply(3.2);assert.equal(runtime.diagnostics().visibleTemple,0);assert.ok(runtime.diagnostics().visibleWalls>0);
 apply(3.9);assert.ok(runtime.diagnostics().visibleTemple>0);
 const identity=runtime.diagnostics().componentIdentity;
 const snapshots=parent.children[0].children.map(m=>Array.from(m.geometry.attributes.position.array));
 apply(4.9);assert.equal(runtime.diagnostics().templeState,'transform');assert.ok(runtime.diagnostics().visibleTemple>0);assert.equal(runtime.diagnostics().visibleWalls,0,'unverified wall continuity must not be projected');
 assert.ok(runtime.exclusionsFor('late-first-temple').length>0);
 apply(5.5);assert.equal(runtime.diagnostics().templeState,'ruin');
 for(const m of parent.children[0].children){const p=m.geometry.attributes.position;m.updateMatrix();for(let i=0;i<p.count;i++){const v=new THREE.Vector3(p.getX(i),p.getY(i),p.getZ(i)).applyMatrix4(m.matrix);assert.ok(v.y>=terrain.heightAtWorld(v.x,v.z)-1e-4);}}
 apply(6.5);assert.equal(runtime.diagnostics().visibleTemple,0);assert.equal(runtime.diagnostics().visiblePalace,0);
 apply(3.9);assert.equal(runtime.diagnostics().componentIdentity,identity);
 parent.children[0].children.forEach((m,i)=>assert.deepEqual(Array.from(m.geometry.attributes.position.array),snapshots[i],'reverse must restore exact vertex positions'));
 runtime.apply({position:3.9,evidenceAllowed:()=>false});assert.equal(runtime.diagnostics().visibleTemple,0);
 assert.equal(core.get('j3k:object:first-temple').geometry.status,'inferred-component-assembly');assert.equal(core.validate().ok,true);
 const roads=new THREE.Group(),material=new THREE.MeshBasicMaterial();
 const meshes=buildHerodianRoadGeometry(roads,[{id:'test',confidence:'inferred',geometry:{points:[{x:-20,z:0},{x:20,z:0}]}}],{inferred:material},terrain,{exclusions:[{polygon:[{x:-6,z:-6},{x:6,z:-6},{x:6,z:6},{x:-6,z:6}]}]});
 assert.equal(meshes.length,2,'road fragments crossing reserved monument must be omitted');
 meshes.forEach(m=>m.geometry.dispose());material.dispose();runtime.dispose();assert.equal(parent.children.length,0);
 console.log('PASS: shared ledger bindings, stable geometry through ruin/reverse, unknown fate filtering, grounded collapse and road exclusions');
} finally {globalThis.fetch=original;invalidateCityData();}
