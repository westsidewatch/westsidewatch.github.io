import assert from 'node:assert/strict';import fs from 'node:fs/promises';import * as THREE from 'three';
import {HeritageBuilder} from '../preview/jerusalem-3000/heritage-builder.js';import {addEvidenceArchitecture} from '../preview/jerusalem-3000/jerusalem-architecture.js';import {HERODIAN_DIMENSIONS as D} from '../preview/jerusalem-3000/herodian-dimensions.js';import {herodianServiceLayout} from '../preview/jerusalem-3000/temple-ritual-service.js';
const root=new URL('../preview/jerusalem-3000/',import.meta.url),objects=JSON.parse(await fs.readFile(new URL('data/objects/herodian-30ce.json',root))).objects,object=objects.find(o=>o.kind==='sacred-complex'),mat=new THREE.MeshStandardMaterial(),builder=new HeritageBuilder({reconstructed:mat}),group=new THREE.Group();builder.currentObject=object;
addEvidenceArchitecture(builder,object,{grid:{origin:{lat:31.778,lon:35.235}},sampleElevation:()=>200,heightAtWorld:()=>200});builder.finish(group);group.updateMatrixWorld(true);
const c=D.cubitMetres,layout=herodianServiceLayout(c),base=200+.8+10*c+.02,minX=-D.womenCourt.eastWest/2-D.priestCourt.eastWest/2,altarX=minX+149*c;
const down=(x,z)=>new THREE.Raycaster(new THREE.Vector3(x,base+30,z),new THREE.Vector3(0,-1,0)).intersectObjects(group.children,true)[0].point.y;
assert.equal(layout.rings.length,24);assert.equal(layout.pillars.length,8);assert.equal(layout.tables.length,7);
for(const p of layout.rings){const x=altarX+p.x;assert.ok(Math.abs(down(x,p.z)-base)<.001,'ring hole must expose court floor');assert.ok(down(x+.5*c,p.z)>base+.04,'each ring must contain real elevated geometry');assert.ok(p.z< -16*c-8*c,'ring grid must remain north of altar with reserved gap');}
for(const p of layout.pillars)assert.ok(Math.abs(down(altarX+p.x,p.z)-(base+2.4))<.001);
for(const p of layout.tables)assert.ok(Math.abs(down(altarX+p.x,p.z)-(base+.85))<.001);
for(const p of layout.pillars)for(const height of[1.4,1.75,2.1]){
 const zz=p.z-.6*c/2-.20,ray=new THREE.Raycaster(new THREE.Vector3(altarX+p.x-.1,base+height+.0663,p.z-1),new THREE.Vector3(0,0,1),0,1);
 const hit=ray.intersectObjects(group.children,true)[0];assert.ok(hit&&Math.abs(hit.point.z-zz)<.04,'each of24 hooks must exist outside its post as curved geometry');
}
const l=layout.laver,h=down(minX+l.xFromCourtWest,l.z);assert.ok(h>base+l.baseHeight&&h<base+l.baseHeight+l.bowlHeight-.2,'laver must have a real open bowl');assert.ok(l.z-l.radius>10*c,'laver must clear the20cubit-wide porch stair');
assert.equal(builder.meshes.length,1,'all service pieces must stay within the existing temple evidence batch');const bounds=new THREE.Box3().setFromObject(group);assert.ok(Math.abs(bounds.max.y-(200+.8+10*c+D.sanctuary.height))<.001);builder.dispose();mat.dispose();
console.log('PASS:24 actual open rings,8 pillar caps,7 authored marble-table positions, hollow laver, stair clearance, unchanged sanctuary height and one evidence batch');
