import assert from 'node:assert/strict';import * as THREE from 'three';import {laterSacredCores,sacredCoreGeometry} from '../preview/jerusalem-3000/later-sacred-cores.js';
const terrain={heightAtWorld:()=>100},material=new THREE.MeshBasicMaterial();
for(const profile of['constantinian-rotunda-east-basilica','sepulchre-1009-fragments','sepulchre-1048-rotunda','medieval-rotunda-church']){
 const record=structuredClone(laterSacredCores('byzantine').find(r=>r.id.endsWith('holy-sepulchre-context')));record.metadata.coreProfile=profile;const g=sacredCoreGeometry(record,terrain),mesh=new THREE.Mesh(g,material);mesh.updateMatrixWorld(true);const cx=record.geometry.polygon.reduce((s,p)=>s+p.x,0)/4,cz=record.geometry.polygon.reduce((s,p)=>s+p.z,0)/4,rx=cx-25;
 const down=new THREE.Raycaster(new THREE.Vector3(rx,200,cz),new THREE.Vector3(0,-1,0)).intersectObject(mesh)[0];
 if(profile==='sepulchre-1009-fragments'){assert.ok(!down,'1009 fragment version must not regain floor/dome/intact hall');g.dispose();continue;}
 assert.ok(Math.abs(down.point.y-132.2)<.01,'rotunda dome height must remain unchanged');
 assert.equal(new THREE.Raycaster(new THREE.Vector3(rx,102,cz),new THREE.Vector3(1,0,0),0,28).intersectObject(mesh).length,0,'rotunda east opening must lead to actual hollow space');
 assert.ok(new THREE.Raycaster(new THREE.Vector3(rx,102,cz),new THREE.Vector3(Math.SQRT1_2,0,Math.SQRT1_2),0,22).intersectObject(mesh).length>0,'rotunda must retain a real circular wall');
 const floor=new THREE.Raycaster(new THREE.Vector3(rx,110,cz),new THREE.Vector3(0,-1,0)).intersectObject(mesh)[0];assert.ok(Math.abs(floor.point.y-100.32)<.001,'rotunda floor must be physically present');
 if(profile==='sepulchre-1048-rotunda'){for(const side of[-1,1])assert.equal(new THREE.Raycaster(new THREE.Vector3(rx,102,cz),new THREE.Vector3(0,0,side),0,29).intersectObject(mesh).length,0,'1048 chapel links must be real openings');}
 if(profile==='medieval-rotunda-church')assert.equal(new THREE.Raycaster(new THREE.Vector3(cx+20,120,cz+32),new THREE.Vector3(1,0,0),0,8).intersectObject(mesh).length,0,'bell tower upper stage must be genuinely open');
 if(profile==='medieval-rotunda-church')assert.ok(Math.abs(new THREE.Raycaster(new THREE.Vector3(cx+20,180,cz+32),new THREE.Vector3(0,-1,0)).intersectObject(mesh)[0].point.y-125.2)<.001,'bell silhouette must stay in inherited height budget');
 g.dispose();
}
material.dispose();console.log('PASS: four distinct Sepulchre states, unchanged dome/bell budgets, hollow round hall and floor, real portals/chapel links, and no restored1009 dome');
