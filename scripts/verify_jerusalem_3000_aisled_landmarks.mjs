import assert from 'node:assert/strict';import * as THREE from 'three';
import {neaCore} from '../preview/jerusalem-3000/nea-core.js';import {aqsaCore} from '../preview/jerusalem-3000/aqsa-core.js';import {sacredCoreGeometry} from '../preview/jerusalem-3000/later-sacred-cores.js';
const terrain={heightAtWorld:()=>100},material=new THREE.MeshBasicMaterial(),rows=[];
for(const phase of['byzantine','early-islamic','crusader','ayyubid-mamluk','ottoman','outside-walls','modern']){
 const record=phase==='byzantine'?neaCore(phase):aqsaCore(phase),g=sacredCoreGeometry(record,terrain),mesh=new THREE.Mesh(g,material);mesh.updateMatrixWorld(true);
 const {x,z}=record.metadata.modelAnchor,nea=phase==='byzantine',widths=nea?[9.5,9.5,19,9.5,9.5]:[20/3,20/3,20/3,10,20/3,20/3,20/3],length=nea?105:80,total=widths.reduce((a,b)=>a+b,0);let cursor=-total/2;
 for(const width of widths){const mid=cursor+width/2,start=nea?new THREE.Vector3(x-length/2-1,102,z+mid):new THREE.Vector3(x+mid,103,z-length/2-1),ray=new THREE.Raycaster(start,nea?new THREE.Vector3(1,0,0):new THREE.Vector3(0,0,1),0,length);assert.equal(ray.intersectObject(mesh).length,0,`${phase} aisles must have actual entry and clear longitudinal volume`);cursor+=width;}
 const low=nea?14:11,high=nea?20:16,span=length-1.2,n=Math.ceil(span/8),u=-span/2+.5*span/n,gap=high-low-.25,wh=Math.min(1.8,gap*.6),windowY=(nea?100.2:101)+low+(gap-wh)/2+wh/2;
 const at=offset=>nea?new THREE.Vector3(x+u+offset,windowY,z):new THREE.Vector3(x,windowY,z+u+offset),direction=nea?new THREE.Vector3(0,0,1):new THREE.Vector3(1,0,0);
 assert.equal(new THREE.Raycaster(at(0),direction,0,nea?12:7).intersectObject(mesh).length,0,'clerestory must contain a real bounded window');assert.ok(new THREE.Raycaster(at(1),direction,0,nea?12:7).intersectObject(mesh).length>0,'clerestory window must retain solid wall piers');
 const roof=new THREE.Raycaster(new THREE.Vector3(x,200,z),new THREE.Vector3(0,-1,0)).intersectObject(mesh)[0];assert.ok(Math.abs(roof.point.y-(nea?123.2:119))<.001,'central roof profile must retain its previous height');
 if(nea){assert.equal(new THREE.Raycaster(new THREE.Vector3(x+length/2-1,102,z),new THREE.Vector3(1,0,0),0,8).intersectObject(mesh).length,0,'main apse must be an actual cavity connected through the rear opening');assert.ok(Math.abs(new THREE.Raycaster(new THREE.Vector3(x+length/2+3,200,z),new THREE.Vector3(0,-1,0)).intersectObject(mesh)[0].point.y-118.2)<.001,'apse roof must face upward');}
 assert.equal(record.metadata.geometryVerified,false);rows.push(phase);g.dispose();
}
material.dispose();console.log('PASS: seven dated landmark versions, five/seven clear aisles and actual entrances, retained central roof profiles and connected hollow Nea main apse');
