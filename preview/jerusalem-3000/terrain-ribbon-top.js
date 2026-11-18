// Clip each paving strip to the *rendered* DEM triangles. Sampling only the
// ribbon edges lets a roof triangle cut across a terrain diagonal and flicker.
export function terrainRibbonTop(corners,terrain,anchor,height){
 const mesh=terrain.mesh,g=terrain.grid,p=mesh.geometry.attributes.position,index=mesh.geometry.index;
 if(!index||!g?.width||!g?.height)throw new Error('Indexed canonical terrain required');
 const ox=mesh.position.x-anchor.x,oz=mesh.position.z-anchor.z,x0=p.getX(0)+ox,z0=p.getZ(0)+oz;
 const dx=(p.getX(g.width-1)-p.getX(0))/(g.width-1),dz=(p.getZ((g.height-1)*g.width)-p.getZ(0))/(g.height-1);
 const range=(values,start,step,max)=>[Math.max(0,Math.floor((Math.min(...values)-start)/step)),Math.min(max-2,Math.floor((Math.max(...values)-start)/step))];
 const [c0,c1]=range(corners.map(v=>v[0]),x0,dx,g.width),[r0,r1]=range(corners.map(v=>v[1]),z0,dz,g.height),vertices=[];
 const signed=(a,b,v)=>(b[0]-a[0])*(v[1]-a[1])-(b[1]-a[1])*(v[0]-a[0]);
 let area=0;for(let i=0;i<corners.length;i++){const a=corners[i],b=corners[(i+1)%corners.length];area+=a[0]*b[1]-b[0]*a[1];}const winding=Math.sign(area);
 const clip=(poly,a,b)=>{const out=[];for(let i=0;i<poly.length;i++){const u=poly[i],v=poly[(i+1)%poly.length],du=winding*signed(a,b,u),dv=winding*signed(a,b,v);if(du>=-1e-8)out.push(u);if((du>1e-8&&dv< -1e-8)||(du< -1e-8&&dv>1e-8)){const t=du/(du-dv);out.push([u[0]+t*(v[0]-u[0]),u[1]+t*(v[1]-u[1])]);}}return out;};
 for(let row=r0;row<=r1;row++)for(let col=c0;col<=c1;col++)for(let tri=0;tri<2;tri++){
  const first=(row*(g.width-1)+col)*6+tri*3;let polygon=Array.from({length:3},(_,k)=>{const i=index.getX(first+k);return[p.getX(i)+ox,p.getZ(i)+oz];});
  for(let k=0;k<corners.length&&polygon.length;k++)polygon=clip(polygon,corners[k],corners[(k+1)%corners.length]);
  for(let k=1;k<polygon.length-1;k++){
   let [a,b,c]=[polygon[0],polygon[k],polygon[k+1]];if(Math.abs(signed(a,b,c))<1e-9)continue;
   // Positive XZ signed area points downward in the world coordinate frame.
   if(signed(a,b,c)>0)[b,c]=[c,b];
   for(const v of[a,b,c])vertices.push(v[0],height(v[0],v[1]),v[1]);
  }
 }
 return vertices;
}
