import * as THREE from 'three';
// Coplanar front/back copies are one surface, not a crease or roof diagonal.
export function majorVolumeEdges(geometry,{minLength=3}={}){
 const p=geometry.attributes.position,index=geometry.index,edges=new Map(),a=new THREE.Vector3(),b=new THREE.Vector3(),c=new THREE.Vector3(),ab=new THREE.Vector3(),ac=new THREE.Vector3();
 const key=v=>`${Math.round(v.x*1000)},${Math.round(v.y*1000)},${Math.round(v.z*1000)}`;
 for(let i=0;i<(index?.count??p.count);i+=3){const ids=[0,1,2].map(j=>index?index.getX(i+j):i+j);a.fromBufferAttribute(p,ids[0]);b.fromBufferAttribute(p,ids[1]);c.fromBufferAttribute(p,ids[2]);const normal=ab.subVectors(b,a).cross(ac.subVectors(c,a)).normalize();if(normal.lengthSq()===0)continue;const points=[a,b,c],keys=points.map(key),face=[...keys].sort().join('|');for(let j=0;j<3;j++){const k=(j+1)%3;if(points[j].distanceToSquared(points[k])<minLength*minLength)continue;const edge=[keys[j],keys[k]].sort().join('|');let e=edges.get(edge);if(!e){e={a:points[j].toArray(),b:points[k].toArray(),faces:new Set(),normals:[]};edges.set(edge,e);}if(!e.faces.has(face)){e.faces.add(face);e.normals.push(normal.clone());}}}
 const result=[],threshold=Math.cos(THREE.MathUtils.degToRad(35));for(const e of edges.values())if(e.faces.size===1||e.normals.some(n=>Math.abs(n.dot(e.normals[0]))<threshold))result.push(...e.a,...e.b);return result;
}
