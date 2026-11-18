import assert from 'node:assert/strict';
import * as THREE from 'three';
import {courtCutEdges,closeClippedCourt} from '../preview/jerusalem-3000/clipped-court-contact.js';
import {clipArchitectureToEnvelope} from '../preview/jerusalem-3000/clip-architecture-to-envelope.js';
const footprint=[{x:-20,z:-20},{x:20,z:-20},{x:20,z:20},{x:-20,z:20}],boundary=[{x:-30,z:-30},{x:0,z:-30},{x:0,z:30},{x:-30,z:30}];
assert.deepEqual(courtCutEdges(footprint,footprint),[],'unchanged source perimeter must not get duplicate faces');
const edges=courtCutEdges(footprint,boundary);assert.equal(edges.length,1);assert.ok(edges[0].every(p=>p.x===0));assert.equal(Math.abs(edges[0][1].z-edges[0][0].z),40);
const plane=new THREE.PlaneGeometry(40,40);plane.rotateX(-Math.PI/2);plane.translate(0,15,0);plane.setAttribute('color',new THREE.Float32BufferAttribute(new Float32Array(plane.attributes.position.count*3).fill(.5),3));
const clipped=clipArchitectureToEnvelope(plane,boundary),terrain={heightAtWorld:(x,z)=>2+z*.1},closed=closeClippedCourt(clipped,{footprint,boundary,terrain,floor:15});
const mesh=new THREE.Mesh(closed,new THREE.MeshBasicMaterial()),ray=new THREE.Raycaster();
for(const z of[-19,-10,0,10,19])for(const y of[terrain.heightAtWorld(0,z)+.001,7,14.99]){ray.set(new THREE.Vector3(10,y,z),new THREE.Vector3(-1,0,0));assert.ok(ray.intersectObject(mesh).some(h=>Math.abs(h.point.x)<1e-5),`new cut must meet DEM at z${z},y${y}`);}
const steep={heightAtWorld:(x,z)=>15+z*.4},excavated=closeClippedCourt(clipped,{footprint,boundary,terrain:steep,floor:15}),cutMesh=new THREE.Mesh(excavated,mesh.material);for(const z of[-19,-10,10,19])for(const fraction of[.01,.5,.99]){const y=15+(steep.heightAtWorld(0,z)-15)*fraction;ray.set(new THREE.Vector3(10,y,z),new THREE.Vector3(-1,0,0));assert.ok(ray.intersectObject(cutMesh).length,'both fill and excavation contact must close, including DEM higher than court');}excavated.dispose();
assert.deepEqual(Array.from(closed.attributes.position.array.slice(0,clipped.attributes.position.array.length)),Array.from(clipped.attributes.position.array),'existing top/outline must remain byte-identical');assert.equal(closed.userData.cutContact.historicalGeometryVerified,false);for(const g of[plane,clipped,closed])g.dispose();mesh.material.dispose();
console.log('PASS: clipped platform cut closes to sloping DEM at low/upper and excavation rays; unchanged top and no duplicate source perimeter');
