import * as THREE from 'three';
import {pointInPolygon} from './urban-exclusion.js';
import {foundationContactGeometry} from './foundation-contact.js';
// Close only new display cut faces. No platform expansion, terrain edits,
// invented ancient wall, or change to the source footprint/floor.
export function courtCutEdges(footprint,boundary){
 const edges=[],cross=(a,b)=>a.x*b.z-a.z*b.x;
 const onSource=q=>footprint.some((a,i)=>{const b=footprint[(i+1)%footprint.length],dx=b.x-a.x,dz=b.z-a.z,t=Math.max(0,Math.min(1,((q.x-a.x)*dx+(q.z-a.z)*dz)/(dx*dx+dz*dz)));return Math.hypot(q.x-a.x-t*dx,q.z-a.z-t*dz)<1e-5;});
 for(let i=0;i<boundary.length;i++){
  const a=boundary[i],b=boundary[(i+1)%boundary.length],d={x:b.x-a.x,z:b.z-a.z},ts=[0,1];
  for(let j=0;j<footprint.length;j++){const p=footprint[j],q=footprint[(j+1)%footprint.length],e={x:q.x-p.x,z:q.z-p.z},delta={x:p.x-a.x,z:p.z-a.z},den=cross(d,e);if(Math.abs(den)<1e-9)continue;const t=cross(delta,e)/den,u=cross(delta,d)/den;if(t>0&&t<1&&u>=0&&u<=1)ts.push(t);}
  const at=t=>({x:a.x+d.x*t,z:a.z+d.z*t});ts.sort((a,b)=>a-b);
  for(let j=1;j<ts.length;j++){if(ts[j]-ts[j-1]<1e-8)continue;const mid=at((ts[j]+ts[j-1])/2);if(pointInPolygon(mid,footprint)&&!onSource(mid))edges.push([at(ts[j-1]),at(ts[j])]);}
 }
 return edges;
}
export function closeClippedCourt(geometry,{footprint,boundary,terrain,floor}){
 const edges=courtCutEdges(footprint,boundary),support=foundationContactGeometry(edges,terrain,floor,{excavation:true}),p=geometry.attributes.position,c=geometry.attributes.color,sp=support.attributes.position;
 const positions=new Float32Array(p.array.length+sp.array.length);positions.set(p.array);positions.set(sp.array,p.array.length);
 const colors=new Float32Array(positions.length);colors.set(c.array);const stone=new THREE.Color(0xb9a27b);for(let i=c.array.length;i<colors.length;i+=3){colors[i]=stone.r;colors[i+1]=stone.g;colors[i+2]=stone.b;}
 const result=new THREE.BufferGeometry();result.setAttribute('position',new THREE.BufferAttribute(positions,3));result.setAttribute('color',new THREE.BufferAttribute(colors,3));result.computeVertexNormals();result.userData.cutContact={edges:edges.length,vertices:sp.count,sourceFootprintChanged:false,floorChanged:false,historicalGeometryVerified:false};support.dispose();return result;
}
