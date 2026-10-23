import * as THREE from 'three';
import {geographicToENU} from './terrain-runtime.js';
import {settlementSurfaceHeight} from './earliest-settlement.js';
// Analytical transect through existing illustrative locations, not an ancient road.
export function sampleRoyalRelief(data,terrain){
 const a=geographicToENU(data.spring.lat,data.spring.lon,terrain.grid.origin),nodes=data.royalCity.spatial.nodes;
 const offsets=[nodes.find(n=>n.id==='ridge-south')?.offset,nodes.find(n=>n.id==='ridge-junction')?.offset,data.royalCity.temple.offset];
 if(offsets.some(p=>!p||p.length!==2||!p.every(Number.isFinite)))throw new Error('Royal relief needs existing south/middle/temple locations');
 const datum=terrain.grid.verticalDatumOffsetMetres;
 const at=([x,z])=>{const world={x:a.east+x,z:-a.north+z};const y=settlementSurfaceHeight(terrain,world.x,world.z);if(!Number.isFinite(y))throw new Error('Royal relief outside DEM');return {...world,y,elevation:y+datum};};
 const anchors=offsets.map(at),samples=[];let distance=0;
 anchors.forEach((p,i)=>{if(i)distance+=Math.hypot(p.x-anchors[i-1].x,p.z-anchors[i-1].z);p.distance=distance;});
 for(let i=1;i<offsets.length;i++){
  const from=offsets[i-1],to=offsets[i],length=anchors[i].distance-anchors[i-1].distance,steps=Math.ceil(length/10);
  for(let j=i===1?0:1;j<=steps;j++){const t=j/steps,p=at([from[0]+(to[0]-from[0])*t,from[1]+(to[1]-from[1])*t]);samples.push({...p,distance:anchors[i-1].distance+length*t});}
 }
 return {anchors,samples,distance,deltaSouth:anchors[2].y-anchors[0].y,deltaMiddle:anchors[2].y-anchors[1].y,verticalScale:1,authority:'existing-inferred-locations-on-modern-dem-not-ancient-ground',threshingFloorLocationVerified:false};
}
export function createRoyalRelief(parent,mount,{data,terrain}){
 const profile=sampleRoyalRelief(data,terrain),group=new THREE.Group();group.name='royal-relief-analytical-overlay';parent.add(group);
 const geometry=new THREE.BufferGeometry().setFromPoints(profile.samples.map(p=>new THREE.Vector3(p.x,p.y+.5,p.z))),lineMaterial=new THREE.LineBasicMaterial({color:0x8b422b});
 group.add(new THREE.Line(geometry,lineMaterial));
 const markerGeometry=new THREE.SphereGeometry(2,8,6),markerMaterial=new THREE.MeshBasicMaterial({color:0x8b422b});
 const labels=document.createElement('div');labels.className='j3k-relief-labels';mount.append(labels);
 const names=['大衛城南段','大衛城中段','北部高處'];
 const entries=profile.anchors.map((p,i)=>{const marker=new THREE.Mesh(markerGeometry,markerMaterial);marker.position.set(p.x,p.y+2,p.z);group.add(marker);const label=document.createElement('span');label.textContent=names[i];labels.append(label);return {p,label};});
 let shown=false;
 return {profile,
  apply({phaseId,stage,evidenceAllowed}){shown=phaseId==='david-solomon'&&evidenceAllowed('inferred');group.visible=shown;labels.hidden=!shown;entries[2].label.textContent=stage==='david'?'北部高處 · 禾場關聯區（示意）':'北部高處 · 所羅門聖殿（示意）';},
  project(camera){if(!shown)return;const width=mount.clientWidth,height=mount.clientHeight;for(const {p,label} of entries){const q=new THREE.Vector3(p.x,p.y+8,p.z).project(camera);label.hidden=q.z< -1||q.z>1||Math.abs(q.x)>1||Math.abs(q.y)>1;const margin=label.offsetWidth/2+4;label.style.left=`${Math.max(margin,Math.min(width-margin,(q.x+1)*width/2))}px`;label.style.top=`${(1-q.y)*height/2}px`;}},
  dispose(){geometry.dispose();lineMaterial.dispose();markerGeometry.dispose();markerMaterial.dispose();group.removeFromParent();labels.remove();}
 };
}
