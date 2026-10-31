import {herodianSanctuaryPlan} from '../preview/jerusalem-3000/herodian-sanctuary.js';
import {createTempleSectionView} from '../preview/jerusalem-3000/temple-section-view.js';
import {herodianRitualLayout,firstTempleWaterLayout} from '../preview/jerusalem-3000/temple-precinct-layout.js';
import assert from 'node:assert/strict';import fs from 'node:fs/promises';import * as THREE from 'three';
import {HeritageBuilder} from '../preview/jerusalem-3000/heritage-builder.js';import {addEvidenceArchitecture} from '../preview/jerusalem-3000/jerusalem-architecture.js';import {HERODIAN_DIMENSIONS as D} from '../preview/jerusalem-3000/herodian-dimensions.js';
import {loadTemporalCityCore} from '../preview/jerusalem-3000/temporal-city-core-adapter.js';import {invalidateCityData} from '../preview/jerusalem-3000/city-data-loader.js';import {createRoyalCity} from '../preview/jerusalem-3000/royal-city.js';
const root=new URL('../preview/jerusalem-3000/',import.meta.url),read=async p=>JSON.parse(await fs.readFile(new URL(p,root))),mat=new THREE.MeshStandardMaterial(),objects=(await read('data/objects/herodian-30ce.json')).objects,object=objects.find(o=>o.kind==='sacred-complex'),terrain={grid:{origin:{lat:31.778,lon:35.235}},heightAtWorld:()=>200,sampleElevation:()=>200};
const builder=new HeritageBuilder({observed:mat,reconstructed:mat,inferred:mat,disputed:mat}),group=new THREE.Group();builder.currentObject=object;const r=addEvidenceArchitecture(builder,object,terrain);builder.finish(group);group.updateMatrixWorld(true);const geometry=builder.meshes[0].geometry,positions=geometry.attributes.position,bounds=new THREE.Box3().setFromObject(group),base=200+D.platform.pavingThickness,y=base+10*D.cubitMetres,west=bounds.min.x+11*D.cubitMetres,east=west+D.sanctuary.eastWest,z=-r.north,podium=6*D.cubitMetres;
const hit=(x,height)=>new THREE.Raycaster(new THREE.Vector3(x,height,z),new THREE.Vector3(-1,0,0)).intersectObjects(group.children,true)[0];assert.ok(hit(east+.1,y+podium+10).point.x<=east-10*D.cubitMetres+.01,'porch must contain an actual open volume, not a dark panel');assert.ok(hit(bounds.max.x+.1,y+2).point.x<bounds.max.x-1,'both courtyard gates must pass a central ray');assert.ok(hit(east+.1,y+podium+40*D.cubitMetres+1).point.x>east-.1,'upper porch lintel must remain solid');assert.ok(Math.abs(bounds.max.y-(y+D.sanctuary.height))<.001);
let stepLevels=new Set();for(let i=0;i<positions.count;i++)if(positions.getX(i)>east+.01&&positions.getX(i)<east+12*D.cubitMetres+.01&&Math.abs(positions.getZ(i)-z)<20*D.cubitMetres/2+.01&&positions.getY(i)>y+.1&&positions.getY(i)<=y+podium+.001)stepLevels.add(Math.round((positions.getY(i)-y)*10000));assert.equal(stepLevels.size,12,'all12 distinct stair rises must exist in generated geometry');const ritual=herodianRitualLayout();assert.ok(Math.abs(ritual.dimensionClosure-D.priestCourt.eastWest)<1e-9);
const minX=bounds.min.x,womenX=minX+D.priestCourt.eastWest+D.womenCourt.eastWest/2;
for(const sx of[-1,1])for(const sz of[-1,1]){
 const room=ritual.womenRoom,rx=womenX+sx*(ritual.women/2-room.inset-room.size/2),rz=z+sz*(ritual.women/2-room.inset-room.size/2);
 const down=new THREE.Raycaster(new THREE.Vector3(rx,y+20,rz),new THREE.Vector3(0,-1,0)).intersectObjects(group.children,true)[0];
 assert.ok(Math.abs(down.point.y-(base+.02))<.001,'corner chamber must be genuinely open-roofed');
 const innerZ=rz-sz*(room.size-room.wall)/2;
 assert.equal(new THREE.Raycaster(new THREE.Vector3(rx,base+1,innerZ-sz),new THREE.Vector3(0,0,sz),0,2).intersectObjects(group.children,true).length,0,'inward access must contain a real doorway');
}
const altarX=minX+ritual.altar.centreFromWest;
for(const f of[.1,.4,.8]){
 const rz=z+ritual.ramp.altarJoinOffset+ritual.ramp.length*f;
 const down=new THREE.Raycaster(new THREE.Vector3(altarX,y+20,rz),new THREE.Vector3(0,-1,0)).intersectObjects(group.children,true)[0];
 assert.ok(Math.abs(down.point.y-(y+.02+9*D.cubitMetres*(1-f)))<.001,'ramp must have a continuous slope');
}
const gateX=minX+D.priestCourt.eastWest;
const downAt=(x,zz=z)=>new THREE.Raycaster(new THREE.Vector3(x,y+100,zz),new THREE.Vector3(0,-1,0)).intersectObjects(group.children,true)[0].point.y;
for(let i=0;i<15;i++){
 const radius=10*D.cubitMetres/2+(i+.5)*ritual.stepTread;
 assert.ok(Math.abs(downAt(gateX+1+radius)-(base+.02+(15-i)*ritual.stepRise))<.001,`semicircular tread ${i+1} has the required physical height`);
}
assert.ok(Math.abs(downAt(gateX-2,z+20)-(base+ritual.levels.israel+.02))<.001,'Israel band must be at its own datum');
assert.ok(Math.abs(downAt(gateX-ritual.israelWidth-2,z+20)-(base+ritual.levels.priests+.02))<.001,'priest band must have the selected higher datum');
const sanctuaryPlan=herodianSanctuaryPlan();assert.ok(Math.abs(sanctuaryPlan.length-D.sanctuary.eastWest)<1e-9,'nine longitudinal segments must close100cubits');
assert.ok(hit(east+.1,y+podium+5).point.x<west+18*D.cubitMetres,'main and partition apertures must lead to a true hollow sanctuary');
const c=D.cubitMetres;
for(let tier=0;tier<3;tier++)for(const side of[-1,1])for(let i=0;i<5;i++){
 const xx=west+(11+(i+.5)*73/5)*c,zz=z+side*((17-tier+22)/2)*c,yy=y+(6+tier*6+1)*c;
 assert.equal(new THREE.Raycaster(new THREE.Vector3(xx,yy,zz),new THREE.Vector3(0,0,side),0,(29-(17-tier+22)/2)*c).intersectObjects(group.children,true).length,0,'each of30side cells has a real door into its service band');
 const back=new THREE.Raycaster(new THREE.Vector3(xx,yy,zz),new THREE.Vector3(0,0,-side)).intersectObjects(group.children,true)[0];assert.ok(Math.abs(Math.abs(back.point.z-z)-(17-tier)*c)<.001,'actual core-wall setback must leave the nominal5/6/7cubit chamber cavity clear');
}
for(let tier=0;tier<3;tier++)for(let i=0;i<(tier===2?2:3);i++){
 const n=tier===2?2:3,zz=z+(-16+(i+.5)*32/n)*c,yy=y+(6+tier*6+1)*c;
 assert.equal(new THREE.Raycaster(new THREE.Vector3(west+8*c,yy,zz),new THREE.Vector3(-1,0,0),0,9*c).intersectObjects(group.children,true).length,0,'each of8rear cells has an actual opening');
}
const section=createTempleSectionView(),mesh=builder.meshes[0],original=mesh.material,originalDepth=mesh.customDepthMaterial,vertexCopy=Array.from(geometry.attributes.position.array);mesh.userData.templeSectionHeight=y+podium+4;
section.set(true,group);assert.notEqual(mesh.material,original);assert.ok(mesh.material.clippingPlanes[0].distanceToPoint(new THREE.Vector3(west,y+podium+10,z))<0);section.set(false,group);assert.equal(mesh.material,original);assert.equal(mesh.customDepthMaterial,originalDepth);assert.deepEqual(Array.from(geometry.attributes.position.array),vertexCopy);section.dispose();
builder.dispose();
const prior=globalThis.fetch;let royal;try{globalThis.fetch=async url=>({ok:true,json:()=>read(url)});invalidateCityData();const timeline=await read('data/continuous-build-timeline.json'),data=await read('data/settlement/david-solomon.v1.json'),{core}=await loadTemporalCityCore(timeline.phases,{terrain}),parent=new THREE.Group();royal=createRoyalCity(parent,{data,terrain,core});royal.apply({position:3.9,evidenceAllowed:()=>true});parent.updateMatrixWorld(true);const parts=parent.children[0].children,main=parts.find(m=>m.userData.cityObject.componentId==='j3k:royal:temple-main'),box=new THREE.Box3().setFromObject(main),cz=(box.min.z+box.max.z)/2;
const ray=new THREE.Raycaster(new THREE.Vector3(box.max.x+10*data.royalCity.temple.cubitMetres+.5,box.max.y-13.5+3.5,cz),new THREE.Vector3(-1,0,0)),hits=ray.intersectObjects(parts.filter(m=>m.visible&&m.userData.cityObject.kind==='first-temple'));assert.ok(hits.length&&hits[0].point.x<=box.max.x+.2,'first temple porch ray must reach the recessed main doorway');const interiorRay=new THREE.Raycaster(new THREE.Vector3(box.max.x-.5,box.max.y-13.5+3.5,cz),new THREE.Vector3(-1,0,0));
const interiorHit=interiorRay.intersectObjects(parts.filter(m=>m.visible&&m.userData.cityObject.kind==='first-temple'))[0];assert.ok(interiorHit.point.x<box.min.x+1,'entry ray must traverse both internal chambers through their apertures');
assert.equal(parts.filter(m=>m.userData.cityObject.componentId.includes('temple-west-tier-')).length,3);
const water=firstTempleWaterLayout();assert.equal(parts.filter(m=>m.userData.cityObject.componentId.includes('temple-laver-stand-')).length,water.stands.count);const sea=parts.find(m=>m.userData.cityObject.componentId==='j3k:royal:temple-sea');assert.ok(sea);assert.equal(sea.geometry.type,'LatheGeometry');assert.equal(parts.filter(m=>m.geometry.type==='LatheGeometry').length,11,'vessels must each use one mesh rather than per-segment draw calls');const tiers=parts.filter(m=>m.userData.cityObject.componentId.includes('temple-side-')&&m.userData.cityObject.componentId.includes('-tier-'));assert.equal(tiers.length,6);for(const m of tiers){const tier=Number(m.userData.cityObject.componentId.split('-tier-')[1]);assert.ok(Math.abs(m.geometry.parameters.depth-(4+tier)*.45)<1e-6);assert.ok(Math.abs(m.geometry.parameters.height-5*.45)<1e-6);}royal.apply({position:3.2,evidenceAllowed:()=>true});assert.ok(tiers.every(m=>!m.visible),'Solomon components must not leak into David');royal.apply({position:5.9,evidenceAllowed:()=>true});assert.ok(royal.diagnostics().templeCompressionFactor<1);royal.apply({position:3.9,evidenceAllowed:()=>false});assert.ok(tiers.every(m=>!m.visible));}finally{royal?.dispose();globalThis.fetch=prior;invalidateCityData();mat.dispose();}
console.log('PASS: actual open porch and courtyard gate rays,12stair levels, unchanged100cubit sanctuary height above raised priest datum, six first-temple chamber tiers and phase/evidence/ruin control');
