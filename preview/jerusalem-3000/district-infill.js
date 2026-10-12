import * as THREE from 'three';
const area=p=>Math.abs(p.reduce((sum,a,i)=>{const b=p[(i+1)%p.length];return sum+a.x*b.z-b.x*a.z;},0))/2;
const clip=(poly,nx,nz,limit)=>{
 const out=[];for(let i=0;i<poly.length;i++){const a=poly[i],b=poly[(i+1)%poly.length],da=a.x*nx+a.z*nz-limit,db=b.x*nx+b.z*nz-limit;
  if(da<=1e-7)out.push(a);if((da<0&&db>0)||(da>0&&db<0)){const t=da/(da-db);out.push({x:a.x+(b.x-a.x)*t,z:a.z+(b.z-a.z)*t});}}
 return out.filter((p,i)=>!i||Math.hypot(p.x-out[i-1].x,p.z-out[i-1].z)>1e-6);
};
function convex(poly){let sign=0;for(let i=0;i<poly.length;i++){const a=poly[i],b=poly[(i+1)%poly.length],c=poly[(i+2)%poly.length],cross=(b.x-a.x)*(c.z-b.z)-(b.z-a.z)*(c.x-b.x);if(Math.abs(cross)<1e-6)continue;if(sign&&Math.sign(cross)!==sign)return false;sign=Math.sign(cross);}return true;}
function convexParts(poly){if(convex(poly))return[poly];return THREE.ShapeUtils.triangulateShape(poly.map(p=>new THREE.Vector2(p.x,p.z)),[]).map(indices=>indices.map(i=>poly[i]));}
// Inferred subdivision of an authored district, never population/survey authority.
// Convex clipping preserves concave district notches without bridging outside them.
export function generateDistrictInfill({district,roads=[],maxBlockArea=6000,roadClearance=6,maxDepth=12}={}) {
 const boundary=district?.geometry?.polygon;
 if(!boundary?.length||!roads.length)return{blocks:[],count:0,withheld:true,reason:'district-or-roads-missing'};
 if(!Number.isFinite(maxBlockArea)||maxBlockArea<1200||!Number.isFinite(roadClearance)||roadClearance<5)throw new Error('Invalid district infill budget');
 let cells=convexParts(boundary).map((polygon,i)=>({polygon,key:`part-${i}`}));
 for(const road of roads)for(let i=1;i<road.geometry.points.length;i++){
  const a=road.geometry.points[i-1],b=road.geometry.points[i],dx=b.x-a.x,dz=b.z-a.z,L=Math.hypot(dx,dz);if(L<1)continue;
  const nx=-dz/L,nz=dx/L,limit=a.x*nx+a.z*nz,tx=dx/L,tz=dz/L,from=a.x*tx+a.z*tz,to=b.x*tx+b.z*tz;
  cells=cells.flatMap(cell=>{
   const projections=cell.polygon.map(p=>p.x*tx+p.z*tz);
   if(Math.max(...projections)<from||Math.min(...projections)>to)return[cell];
   // Extend the street clearance through its local cell; not an invented drawn road.
   const left=clip(cell.polygon,nx,nz,limit-roadClearance/2),right=clip(cell.polygon,-nx,-nz,-limit-roadClearance/2);
   if(left.length===cell.polygon.length&&area(left)>=area(cell.polygon)-1e-4)return[cell];
   if(right.length===cell.polygon.length&&area(right)>=area(cell.polygon)-1e-4)return[cell];
   return [[left,'left'],[right,'right']].filter(([p])=>p.length>=3&&area(p)>650).map(([polygon,side])=>({polygon,key:`${cell.key}:${road.id.split(':').at(-1)}-${i}-${side}`}));
  });
 }
 const finished=[];
 function divide(cell,depth=0){
  const p=cell.polygon,A=area(p);
  if(A<=maxBlockArea||depth>=maxDepth){finished.push(cell);return;}
  const xs=p.map(v=>v.x),zs=p.map(v=>v.z),xmin=Math.min(...xs),xmax=Math.max(...xs),zmin=Math.min(...zs),zmax=Math.max(...zs),alongX=xmax-xmin>=zmax-zmin;
  let hash=2166136261;for(const c of cell.key)hash=Math.imul(hash^c.charCodeAt(0),16777619)>>>0;
  const ratio=.44+(hash%13)/100,nx=alongX?1:0,nz=alongX?0:1,limit=alongX?xmin+(xmax-xmin)*ratio:zmin+(zmax-zmin)*ratio;
  const parts=[clip(p,nx,nz,limit-1.2),clip(p,-nx,-nz,-limit-1.2)];
  if(parts.some(q=>q.length<3||area(q)<650)){finished.push(cell);return;}
  parts.forEach((polygon,i)=>divide({polygon,key:`${cell.key}:${i}`},depth+1));
 }
 cells.forEach(cell=>divide(cell));
 const blocks=finished.map(cell=>({id:`${district.id}:infill:${cell.key}`,type:'block',districtId:district.id,confidence:'inferred',geometry:{primitive:'polygon',polygon:cell.polygon,terrainFollowing:true},metadata:{generator:'district-constrained-infill-v1',area:area(cell.polygon),closedFace:true,roadBounded:false,gridPopulation:false,semanticBox:false,subdivisionAuthority:'illustrative-partition-not-excavated-blocks',accessGapMetres:2.4}}));
 return{blocks,count:blocks.length,withheld:false,generator:'district-constrained-infill-v1'};
}
export function roadClearancePolygons(roads,width=6){return roads.flatMap(road=>road.geometry.points.slice(1).map((b,i)=>{const a=road.geometry.points[i],L=Math.hypot(b.x-a.x,b.z-a.z);if(!L)return null;const nx=-(b.z-a.z)/L*width/2,nz=(b.x-a.x)/L*width/2;return{polygon:[{x:a.x+nx,z:a.z+nz},{x:b.x+nx,z:b.z+nz},{x:b.x-nx,z:b.z-nz},{x:a.x-nx,z:a.z-nz}]};}).filter(Boolean));}
