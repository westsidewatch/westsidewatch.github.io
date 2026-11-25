import assert from 'node:assert/strict';
import * as THREE from 'three';
import {buildHerodianRoadGeometry} from '../preview/jerusalem-3000/herodian-road-geometry.js';
import {sampleRenderedTerrainHeight} from '../preview/jerusalem-3000/terrain-runtime.js';
const geometry=new THREE.PlaneGeometry(120,120,8,8);geometry.rotateX(-Math.PI/2);
const p=geometry.attributes.position;for(let i=0;i<p.count;i++)p.setY(i,.4*p.getZ(i)+8*Math.cos(p.getX(i)/14)+4*Math.sin(p.getZ(i)/11));geometry.computeVertexNormals();
const terrain={mesh:new THREE.Mesh(geometry),grid:{width:9,height:9}};terrain.heightAtWorld=(x,z)=>sampleRenderedTerrainHeight(terrain,x,z);
const record={id:'road-fixture',confidence:'inferred',geometry:{points:[{x:-40,z:0},{x:40,z:0}],widthMetres:5}},original=JSON.stringify(record),group=new THREE.Group(),material=new THREE.MeshStandardMaterial();
const meshes=buildHerodianRoadGeometry(group,[record],{inferred:material},terrain);group.updateMatrixWorld(true);
let samples=0,legacyMismatch=0;
for(let x=-39.73;x<40;x+=1.137)for(let z=-2.37;z<2.5;z+=.537){const expected=terrain.heightAtWorld(x,z)+.35,hits=new THREE.Raycaster(new THREE.Vector3(x,100,z),new THREE.Vector3(0,-1,0)).intersectObjects(meshes);assert.equal(hits.length,1,'every road interior point has one top');assert.ok(Math.abs(hits[0].point.y-expected)<.0001,'paving follows the rendered DEM triangles across its width');samples++;const cell=Math.floor((x+40)/(80/7)),a=-40+cell*80/7,b=a+80/7,t=(x-a)/(b-a),old=(1-t)*terrain.heightAtWorld(a,0)+t*terrain.heightAtWorld(b,0)+.35;if(Math.abs(old-expected)>.5)legacyMismatch++;}
assert.ok(legacyMismatch>samples*.5,'fixture reproduces old floating/penetrating strips');
const ring=(min,max)=>[{x:min,z:-10},{x:max,z:-10},{x:max,z:10},{x:min,z:10}];
const clipped=buildHerodianRoadGeometry(new THREE.Group(),[record],{inferred:material},terrain,{envelope:ring(-30,30),exclusions:[{polygon:ring(10,20)}]});
let area=0,min=Infinity,max=-Infinity;for(const m of clipped){const a=m.geometry.attributes.position;assert.equal(m.userData.cityObject.objectId,record.id);for(let i=0;i<a.count;i+=3){const x=[a.getX(i),a.getX(i+1),a.getX(i+2)],z=[a.getZ(i),a.getZ(i+1),a.getZ(i+2)];area+=Math.abs((x[1]-x[0])*(z[2]-z[0])-(x[2]-x[0])*(z[1]-z[0]))/2;for(const v of x){min=Math.min(min,v);max=Math.max(max,v);assert.ok(v<=10.00001||v>=19.99999);}}}
assert.ok(Math.abs(area-250)<.001,'court/circuit trim retains paving up to exact boundary instead of dropping complete cells');assert.equal(min,-30);assert.equal(max,30);assert.equal(JSON.stringify(record),original);assert.equal(material.userData.j3kVisualHierarchy,undefined);
for(const m of[...meshes,...clipped])m.geometry.dispose();geometry.dispose();material.dispose();console.log(JSON.stringify({ok:true,samples,legacyMismatch,clippedPavingArea:area,planUnchanged:true,ancientStreetLevelVerified:false}));
