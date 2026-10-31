import * as THREE from 'three';
// Clip actual triangles (including vertical retaining faces), interpolating
// height/colour. Preserve source coordinates in the record; only display context
// is restricted to the selected contemporary circuit.
export function clipArchitectureToEnvelope(geometry,ring){
 const regions=THREE.ShapeUtils.triangulateShape(ring.map(p=>new THREE.Vector2(p.x,p.z)),[]).map(ids=>{const p=ids.map(i=>ring[i]);return (p[1].x-p[0].x)*(p[2].z-p[0].z)-(p[1].z-p[0].z)*(p[2].x-p[0].x)<0?p.reverse():p;}),position=geometry.attributes.position,colour=geometry.attributes.color,idx=geometry.index?.array||Array.from({length:position.count},(_,i)=>i),out=[],colors=[];
 for(let i=0;i<idx.length;i+=3){const tri=idx.slice(i,i+3).map(k=>[position.getX(k),position.getY(k),position.getZ(k),colour?.getX(k)??1,colour?.getY(k)??1,colour?.getZ(k)??1]);
  for(const region of regions){let poly=tri;for(let j=0;j<3&&poly.length;j++){const a=region[j],b=region[(j+1)%3],distance=p=>(b.x-a.x)*(p[2]-a.z)-(b.z-a.z)*(p[0]-a.x),next=[];for(let k=0;k<poly.length;k++){const p=poly[k],q=poly[(k+1)%poly.length],dp=distance(p),dq=distance(q),insideP=dp>=-1e-7,insideQ=dq>=-1e-7;if(insideP)next.push(p);if(insideP!==insideQ){const t=dp/(dp-dq);next.push(p.map((v,n)=>v+(q[n]-v)*t));}}poly=next;}
   for(let j=1;j+1<poly.length;j++){const t=[poly[0],poly[j],poly[j+1]],a=new THREE.Vector3(...t[0].slice(0,3)),b=new THREE.Vector3(...t[1].slice(0,3)),c=new THREE.Vector3(...t[2].slice(0,3));if(b.sub(a).cross(c.sub(a)).lengthSq()<1e-10)continue;for(const v of t){out.push(...v.slice(0,3));colors.push(...v.slice(3));}}
  }
 }
 const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(out,3));g.setAttribute('color',new THREE.Float32BufferAttribute(colors,3));g.computeVertexNormals();return g;
}
