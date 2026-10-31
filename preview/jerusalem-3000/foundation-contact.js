import * as THREE from 'three';
// Sample every crossing of the actual DEM grid edges and rendered diagonals.
// Supporting faces are display foundations, not reconstructed ancient masonry.
export function foundationEdgePoints(a,b,terrain){
 const p=terrain.mesh?.geometry.attributes.position,g=terrain.grid,ts=new Set([0,1]);
 const cut=(start,end)=>{if(Math.abs(end-start)<1e-9)return;for(let k=Math.ceil(Math.min(start,end));k<=Math.floor(Math.max(start,end));k++){const t=(k-start)/(end-start);if(t>1e-8&&t<1-1e-8)ts.add(t);}};
 if(p&&g?.width&&g?.height){const x0=p.getX(0)+terrain.mesh.position.x,z0=p.getZ(0)+terrain.mesh.position.z,dx=(p.getX(g.width-1)-p.getX(0))/(g.width-1),dz=(p.getZ((g.height-1)*g.width)-p.getZ(0))/(g.height-1),u0=(a.x-x0)/dx,u1=(b.x-x0)/dx,v0=(a.z-z0)/dz,v1=(b.z-z0)/dz;cut(u0,u1);cut(v0,v1);cut(u0+v0,u1+v1);}
 else{const n=Math.ceil(Math.hypot(b.x-a.x,b.z-a.z)/2);for(let i=1;i<n;i++)ts.add(i/n);}
 return [...ts].sort((a,b)=>a-b).map(t=>({x:a.x+(b.x-a.x)*t,z:a.z+(b.z-a.z)*t}));
}
export function foundationContactGeometry(edges,terrain,floor){
 const vertices=[];
 for(const [a,b]of edges){const points=foundationEdgePoints(a,b,terrain);for(let i=1;i<points.length;i++){const a=points[i-1],b=points[i],ya=Math.min(floor,terrain.heightAtWorld(a.x,a.z)-.15),yb=Math.min(floor,terrain.heightAtWorld(b.x,b.z)-.15);if(![ya,yb].every(Number.isFinite))throw new Error('Foundation outside original DEM');if(ya===floor&&yb===floor)continue;vertices.push(a.x,floor,a.z,b.x,yb,b.z,b.x,floor,b.z,a.x,floor,a.z,a.x,ya,a.z,b.x,yb,b.z);}}
 // Thin retaining/support faces can be viewed from either side. Emit both
 // windings so original mesh materials need no global side/culling change.
 const front=[...vertices];for(let i=0;i<front.length;i+=9)vertices.push(...front.slice(i+6,i+9),...front.slice(i+3,i+6),...front.slice(i,i+3));
 const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(vertices,3));g.computeVertexNormals();return g;
}
