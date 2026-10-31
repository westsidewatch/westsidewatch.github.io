import {foundationEdgePoints} from './foundation-contact.js';
// Raised approach ribbons have solid side support, not floating paving strips.
export function sanctuaryAccessVertices(points,width,surface,top,context=null){
 const vertices=[];
 const frame=context?.terrain?.mesh?{grid:context.terrain.grid,mesh:{geometry:context.terrain.mesh.geometry,position:{x:context.terrain.mesh.position.x-context.anchor.x,z:context.terrain.mesh.position.z-context.anchor.z}}}:null;
 const triangle=(a,b,c)=>vertices.push(...a,...b,...c);
 const face=(a,b,c)=>{triangle(a,b,c);triangle(c,b,a);};
 for(let i=1;i<points.length;i++){
  const [ax,az]=points[i-1],[bx,bz]=points[i],dx=bx-ax,dz=bz-az,len=Math.hypot(dx,dz),n=Math.ceil(len/2),nx=-dz/len*width/2,nz=dx/len*width/2;
  const point=(f,side)=>{const x=ax+dx*f+side*nx,z=az+dz*f+side*nz;return[x,top(x,z,i,f),z];};
  const ts=new Set(Array.from({length:n+1},(_,i)=>i/n));
  if(frame)for(const side of[-1,1]){const a={x:ax+side*nx,z:az+side*nz},b={x:bx+side*nx,z:bz+side*nz};for(const p of foundationEdgePoints(a,b,frame))ts.add(Math.max(0,Math.min(1,((p.x-a.x)*dx+(p.z-a.z)*dz)/(len*len))));}
  const breaks=[...ts].sort((a,b)=>a-b);
  for(let j=1;j<breaks.length;j++){
   const a=point(breaks[j-1],1),b=point(breaks[j],1),c=point(breaks[j-1],-1),d=point(breaks[j],-1);
   triangle(a,b,c);triangle(b,d,c);
   for(const [u,v]of[[a,b],[d,c]])if(Math.max(u[1]-surface(u[0],u[2]),v[1]-surface(v[0],v[2]))>.12){
    const bu=[u[0],surface(u[0],u[2]),u[2]],bv=[v[0],surface(v[0],v[2]),v[2]];
    face(u,bu,v);face(v,bu,bv);
   }
  }
 }
 return vertices;
}
