import {accessRibbonSections,ribbonFraction} from './access-ribbon-plan.js';
import {terrainRibbonTop} from './terrain-ribbon-top.js';
import {foundationEdgePoints} from './foundation-contact.js';
// Raised approach ribbons have solid side support, not floating paving strips.
export function sanctuaryAccessVertices(points,width,surface,top,context=null){
 const vertices=[],sections=accessRibbonSections(points,width);
 const frame=context?.terrain?.mesh?{grid:context.terrain.grid,mesh:{geometry:context.terrain.mesh.geometry,position:{x:context.terrain.mesh.position.x-context.anchor.x,z:context.terrain.mesh.position.z-context.anchor.z}}}:null;
 const triangle=(a,b,c)=>vertices.push(...a,...b,...c);
 const face=(a,b,c)=>{triangle(a,b,c);triangle(c,b,a);};
 for(let i=1;i<points.length;i++){
  const [ax,az]=points[i-1],[bx,bz]=points[i],len=Math.hypot(bx-ax,bz-az),n=Math.ceil(len/2),start=sections[i-1],end=sections[i];
  const point=(f,side)=>{const a=side>0?start.left:start.right,b=side>0?end.left:end.right,x=a[0]+(b[0]-a[0])*f,z=a[1]+(b[1]-a[1])*f;return[x,top(x,z,i,f),z];};
  const ts=new Set(Array.from({length:n+1},(_,i)=>i/n));
  if(frame)for(const side of[-1,1]){const u=side>0?start.left:start.right,v=side>0?end.left:end.right,a={x:u[0],z:u[1]},b={x:v[0],z:v[1]},dx=b.x-a.x,dz=b.z-a.z;for(const p of foundationEdgePoints(a,b,frame))ts.add(Math.max(0,Math.min(1,((p.x-a.x)*dx+(p.z-a.z)*dz)/(dx*dx+dz*dz))));}
  const breaks=[...ts].sort((a,b)=>a-b);
  for(let j=1;j<breaks.length;j++){
   const a=point(breaks[j-1],1),b=point(breaks[j],1),c=point(breaks[j-1],-1),d=point(breaks[j],-1);
   if(frame){
    const height=(x,z)=>top(x,z,i,ribbonFraction(x,z,start.left,end.left,start.right,end.right));
    vertices.push(...terrainRibbonTop([[a[0],a[2]],[b[0],b[2]],[d[0],d[2]],[c[0],c[2]]],context.terrain,context.anchor,height));
   }else{triangle(a,b,c);triangle(b,d,c);}
   for(const [u,v]of[[a,b],[d,c]])if(Math.max(u[1]-surface(u[0],u[2]),v[1]-surface(v[0],v[2]))>.12){
    const bu=[u[0],surface(u[0],u[2]),u[2]],bv=[v[0],surface(v[0],v[2]),v[2]];
    face(u,bu,v);face(v,bu,bv);
   }
  }
 }
 return vertices;
}
