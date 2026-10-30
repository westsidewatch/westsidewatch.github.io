import {pointInPolygon} from './urban-exclusion.js';
// Display registration only: an inferred connector is not a historical street.
const distance=(a,b)=>Math.hypot(a.x-b.x,a.z-b.z);
function closestPoint(a,b,c){
 const dx=b.x-a.x,dz=b.z-a.z,length2=dx*dx+dz*dz;
 const t=length2?Math.max(0,Math.min(1,((c.x-a.x)*dx+(c.z-a.z)*dz)/length2)):0;
 return {x:a.x+t*dx,z:a.z+t*dz};
}
export function registerLandmarkApproaches(registration){
 for(const core of registration.cores){
  const polygon=core.geometry.polygon,c={x:polygon.reduce((s,p)=>s+p.x,0)/polygon.length,z:polygon.reduce((s,p)=>s+p.z,0)/polygon.length};
  const halfX=(Math.max(...polygon.map(p=>p.x))-Math.min(...polygon.map(p=>p.x)))/2,halfZ=(Math.max(...polygon.map(p=>p.z))-Math.min(...polygon.map(p=>p.z)))/2;
  const church=core.metadata.approachAxis==='western'||core.id.endsWith('holy-sepulchre-context');
  const axis=registration.roads.find(r=>r.id.endsWith(church?':western-market-axis-context':':eastern-valley-link-illustrative'))||registration.roads.find(r=>r.id.includes(church?':western-':':eastern-'));
  if(!axis)throw new Error(`Missing landmark approach axis: ${core.id}`);
  const points=axis.geometry.points,candidates=[];
  for(let i=1;i<points.length;i++)candidates.push(closestPoint(points[i-1],points[i],c));
  candidates.push(...points);
  const outside=p=>Math.max(Math.abs(p.x-c.x)/halfX,Math.abs(p.z-c.z)/halfZ)>1+1e-8;
  const start=candidates.filter(outside).sort((a,b)=>distance(a,c)-distance(b,c))[0];
  if(!start)throw new Error(`Landmark axis lies entirely inside core: ${core.id}`);
  const dx=start.x-c.x,dz=start.z-c.z,scale=Math.max(Math.abs(dx)/halfX,Math.abs(dz)/halfZ);
  let end={x:c.x+dx/scale,z:c.z+dz/scale};
  if(core.metadata.precinctContext){let first=Infinity;for(let i=0;i<polygon.length;i++){const a=polygon[i],b=polygon[(i+1)%polygon.length],ex=b.x-a.x,ez=b.z-a.z,den=dx*ez-dz*ex;if(Math.abs(den)<1e-8)continue;const ax=a.x-c.x,az=a.z-c.z,t=(ax*ez-az*ex)/den,u=(ax*dz-az*dx)/den;if(t>0&&t<=1&&u>=0&&u<=1)first=Math.min(first,t);}if(!Number.isFinite(first))throw new Error('Mapped courtyard approach has no boundary intersection');end={x:c.x+dx*first,z:c.z+dz*first};}
  registration.roads.push({id:`${core.id.replace(':monument:',':road:')}-approach-design`,type:'road',confidence:'inferred',geometry:{frame:'canonical-dem-enu',status:'authored-core-link-not-surveyed-street',primitive:'polyline',points:[{...start},end]},source:{urls:[...new Set([...core.source.urls,...axis.source.urls])],authority:'authored connection between contemporary illustrative axis and schematic core edge; not an identified entrance'},metadata:{layoutRole:'old-city-route-context',coreReference:core.id,axisReference:axis.id,routeGeometryVerified:false,entranceIdentified:false}});
 }
}
