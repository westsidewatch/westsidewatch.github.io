import * as THREE from 'three';
const area=p=>Math.abs(p.reduce((s,a,i)=>{const b=p[(i+1)%p.length];return s+a.x*b.z-b.x*a.z;},0))/2;
function clip(p,nx,nz,limit){
 const out=[];for(let i=0;i<p.length;i++){const a=p[i],b=p[(i+1)%p.length],da=a.x*nx+a.z*nz-limit,db=b.x*nx+b.z*nz-limit;
  if(da<=0)out.push({...a});if((da<0&&db>0)||(da>0&&db<0)){const t=da/(da-db);out.push({x:a.x+(b.x-a.x)*t,z:a.z+(b.z-a.z)*t});}}
 return out;
}
function convex(p){let sign=0;for(let i=0;i<p.length;i++){const a=p[i],b=p[(i+1)%p.length],c=p[(i+2)%p.length],cross=(b.x-a.x)*(c.z-b.z)-(b.z-a.z)*(c.x-b.x);if(Math.abs(cross)<1e-7)continue;if(sign&&Math.sign(cross)!==sign)return false;sign=Math.sign(cross);}return true;}
// Display-module bounds, not measured historical house dimensions.
export const MAX_OVERVIEW_MODULE_SPAN_METRES=32;
export function overviewModuleMetrics(p){
 let span=0,width=Infinity;
 for(let i=0;i<p.length;i++){
  const a=p[i],b=p[(i+1)%p.length],L=Math.hypot(b.x-a.x,b.z-a.z);
  if(L>1e-8){const values=p.map(q=>((b.z-a.z)*q.x-(b.x-a.x)*q.z)/L);width=Math.min(width,Math.max(...values)-Math.min(...values));}
  for(const b of p){const d=Math.hypot(b.x-a.x,b.z-a.z);if(d>span+1e-6){span=d;}}
 }
 return {span,width:Number.isFinite(width)?width:0};
}
// Visual subdivision inside an already registered block. No parcels, houses or
// historical street events are created. Geometry, not era/ID/world grid, owns it.
export function partitionOverviewBlock(polygon){
 if(!Array.isArray(polygon)||polygon.length<3||polygon.some(p=>![p.x,p.z].every(Number.isFinite))||area(polygon)<1)throw new Error('Invalid overview block');
 const parts=convex(polygon)?[polygon]:THREE.ShapeUtils.triangulateShape(polygon.map(p=>new THREE.Vector2(p.x,p.z)),[]).map(t=>t.map(i=>polygon[i]));
 const cells=[];
 function divide(p,depth){
  const A=area(p),shape=overviewModuleMetrics(p);if((A<=900&&shape.span<=MAX_OVERVIEW_MODULE_SPAN_METRES+1e-6)||depth===16){cells.push(p);return;}
  let edge=null;for(let i=0;i<p.length;i++){const a=p[i],b=p[(i+1)%p.length],length=Math.hypot(b.x-a.x,b.z-a.z);if(!edge||length>edge.length+1e-6)edge={a,b,length};}
  if(!edge||edge.length<12){cells.push(p);return;}
  const forced=shape.span>MAX_OVERVIEW_MODULE_SPAN_METRES,nx=(edge.b.x-edge.a.x)/edge.length,nz=(edge.b.z-edge.a.z)/edge.length,projections=p.map(q=>q.x*nx+q.z*nz),min=Math.min(...projections),max=Math.max(...projections);
  // Vary split proportions using only intrinsic area/edge length. A rotated or
  // translated copy keeps the layout; changing phase identity cannot reshuffle it.
  const ratio=.43+(Math.round(A*10+edge.length*100)%15)/100,limit=min+(max-min)*ratio;
  // A narrow remnant must still split by length. Avoid cutting new access
  // gaps into strips too narrow to carry them; genuine streets stay upstream.
  const gap=shape.width<6?0:.9,pair=[clip(p,nx,nz,limit-gap),clip(p,-nx,-nz,-limit-gap)];
  if(pair.some(q=>q.length<3||area(q)<(forced?1e-6:120))){cells.push(p);return;}
  for(const q of pair)divide(q,depth+1);
 }
 for(const p of parts)divide(p,0);
 return cells;
}
