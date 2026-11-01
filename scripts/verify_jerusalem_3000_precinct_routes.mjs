import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import * as THREE from 'three';
import {loadCanonicalTerrain} from '../preview/jerusalem-3000/terrain-runtime.js';
import {HeritageBuilder} from '../preview/jerusalem-3000/heritage-builder.js';
import {addEvidenceArchitecture} from '../preview/jerusalem-3000/jerusalem-architecture.js';
import {westernRouteReservation} from '../preview/jerusalem-3000/western-precinct-route.js';
const root=new URL('../preview/jerusalem-3000/',import.meta.url),read=async p=>JSON.parse(await fs.readFile(new URL(p,root)));
const manifest=await read('data/terrain-manifest.json'),grid=await read('data/'+manifest.elevationGrid.replace('./','')),prior=globalThis.fetch;
let terrain;try{globalThis.fetch=async()=>({ok:true,json:async()=>grid});terrain=await loadCanonicalTerrain(manifest,new THREE.Group());}finally{globalThis.fetch=prior;}
const data=await read('data/objects/herodian-30ce.json'),street=data.objects.find(o=>o.kind==='street'),anchor=structuredClone(street.spatial.anchor),mat=new THREE.MeshStandardMaterial(),builder=new HeritageBuilder({inferred:mat,observed:mat,reconstructed:mat,disputed:mat}),parent=new THREE.Group();
try{
 builder.currentObject=street;const r=addEvidenceArchitecture(builder,street,terrain);builder.finish(parent);parent.updateMatrixWorld(true);
 const b=new THREE.Box3().setFromObject(parent),plan=r.displayRoute;
 assert.deepEqual(street.spatial.anchor,anchor,'source geographic candidate must remain unchanged');
 assert.equal(street.evidence,'inferred','an authored exterior candidate cannot inherit archaeological surface styling');
 assert.ok(Math.abs(b.max.x-(plan.platformWest-plan.clearance))<.001,'every street vertex must remain outside the rounded platform');
 assert.ok(Math.abs(b.max.x-b.min.x-8)<.001&&Math.abs(b.max.z-b.min.z-357)<.001,'selected narrow route, no giant slabs or replacement wall');
 assert.equal(plan.historicalGeometryAccepted,false);assert.ok(Math.abs(plan.displayOffsetEast)>20,'old anchor conflict must be recorded, not silently overwritten');
 const reservation=westernRouteReservation(r);assert.ok(Math.abs(reservation.polygon[1].x-b.max.x-1)<.001);
 const positions=builder.meshes[0].geometry.attributes.position;let vertices=0;
 for(let i=0;i<positions.count;i++){
  const x=positions.getX(i),z=positions.getZ(i),offset=positions.getY(i)-terrain.heightAtWorld(x,z);
  assert.ok(offset>=-.002&&offset<=.162,`street contact vertex ${i} offset ${offset}`);vertices++;
 }
 let samples=0,maxIntrusion=0,maxClearance=0;
 for(let z=b.min.z+.5;z<b.max.z;z+=1)for(const dx of[-3,-1,0,1,3]){
  const x=(b.min.x+b.max.x)/2+dx,hit=new THREE.Raycaster(new THREE.Vector3(x,b.max.y+5,z),new THREE.Vector3(0,-1,0)).intersectObjects(parent.children,true)[0];assert.ok(hit,'paving must contain no holes');
  const gap=hit.point.y-terrain.heightAtWorld(x,z);maxIntrusion=Math.max(maxIntrusion,-gap);maxClearance=Math.max(maxClearance,gap);samples++;
 }
 assert.ok(maxIntrusion<.03,`terrain must not cut road; maximum intrusion ${maxIntrusion}`);
 assert.ok(maxClearance<.2,`paving must follow the original terrain; maximum gap ${maxClearance}`);
 console.log(JSON.stringify({ok:true,vertices,samples,maxIntrusion,maxClearance,plan,historicalGeometryAccepted:false}));
}finally{builder.dispose();mat.dispose();terrain.dispose();}
