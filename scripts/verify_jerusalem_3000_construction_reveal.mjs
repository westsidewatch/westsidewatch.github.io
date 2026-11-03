import assert from 'node:assert/strict';
import * as THREE from 'three';
import {createCityProjection} from '../preview/jerusalem-3000/city-lifecycle-projection.js';
const group=new THREE.Group(),material=new THREE.MeshBasicMaterial(),meshes=[];
for(let i=0;i<10;i++){const mesh=new THREE.Mesh(new THREE.BoxGeometry(),material);mesh.userData.cityObject={objectId:`house-${i}`,parcelId:`parcel-${i}`,terrainGround:0,confidence:'inferred'};group.add(mesh);meshes.push(mesh);}
const projection=createCityProjection(group,meshes),counts=[];
for(const constructionProgress of [0,.2,.5,1]){projection.apply({phaseId:'herodian-jesus',constructionProgress});counts.push(projection.visibility().visibleBuildings);}
assert.deepEqual(counts,[0,2,5,10]);projection.apply({phaseId:'roman-destruction',constructionProgress:0,ruin:1});assert.equal(projection.visibility().visibleBuildings,10,'ruins must not replay construction');projection.apply({phaseId:'herodian-jesus'});assert.equal(projection.visibility().visibleBuildings,10,'manual inspection remains complete');projection.apply({phaseId:'herodian-jesus',constructionProgress:.5,evidenceAllowed:()=>false});assert.equal(projection.visibility().visibleBuildings,0);projection.apply({phaseId:'herodian-jesus',constructionProgress:.5});assert.equal(projection.visibility().visibleBuildings,5);meshes.forEach(m=>m.geometry.dispose());material.dispose();console.log('PASS: actual building visibility progresses, completes, reverses and respects evidence without re-building ruins');
