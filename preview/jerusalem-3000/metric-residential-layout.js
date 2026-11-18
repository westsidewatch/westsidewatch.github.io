import {compileRoyalSpatialLayout} from './royal-spatial-layout.js';
import * as THREE from 'three';
import {polygonsOverlap,pointInPolygon} from './urban-exclusion.js';
import {geographicToENU} from './terrain-runtime.js';
export const METRIC_RESIDENTIAL_PHASES=Object.freeze(['chalcolithic-early-bronze','middle-bronze','late-bronze-iron1','david-solomon','late-first-temple','babylonian-destruction','persian-nehemiah','hellenistic-hasmonean','herodian-jesus','roman-destruction','aelia','byzantine','early-islamic','crusader','ayyubid-mamluk','ottoman','outside-walls','modern']);
const phasePolicy=phase=>({phase,frame:'canonical-dem-enu',metresPerSceneUnit:1,horizontalScale:1,verticalScale:1,maxParcelSpanMetres:18,minParcelAreaSquareMetres:65,accessGapMetres:1.6,setbackMetres:.6,maxUnterracedReliefMetres:8,authority:'engineering-layout-within-existing-inferred-residential-zones-not-surveyed-houses',dimensionsHistoricallyVerified:false,densityTarget:null});
export const METRIC_RESIDENTIAL_POLICIES=Object.freeze(Object.fromEntries(METRIC_RESIDENTIAL_PHASES.map(id=>[id,Object.freeze(phasePolicy(id))])));
export function metricResidentialPolicy(phase){const p=METRIC_RESIDENTIAL_POLICIES[phase];if(!p)throw new Error(`Missing metric residential policy: ${phase}`);return {...p};}
export const polygonArea=p=>Math.abs(p.reduce((s,a,i)=>{const b=p[(i+1)%p.length];return s+a.x*b.z-b.x*a.z;},0))/2;
const cross=(a,b,c)=>(b.x-a.x)*(c.z-a.z)-(b.z-a.z)*(c.x-a.x);
function clip(p,nx,nz,limit){const out=[];for(let i=0;i<p.length;i++){const a=p[i],b=p[(i+1)%p.length],da=a.x*nx+a.z*nz-limit,db=b.x*nx+b.z*nz-limit;if(da<=1e-7)out.push(a);if((da<0&&db>0)||(da>0&&db<0)){const t=da/(da-db);out.push({x:a.x+(b.x-a.x)*t,z:a.z+(b.z-a.z)*t});}}return out;}
function convex(p){let sign=0;for(let i=0;i<p.length;i++){const v=cross(p[i],p[(i+1)%p.length],p[(i+2)%p.length]);if(Math.abs(v)<1e-7)continue;if(sign&&Math.sign(v)!==sign)return false;sign=Math.sign(v);}return true;}
export function metricInset(p,distance){let out=p;const signed=p.reduce((s,a,i)=>{const b=p[(i+1)%p.length];return s+a.x*b.z-b.x*a.z;},0),q=signed<0?[...p].reverse():p;for(let i=0;i<q.length&&out.length>=3;i++){const a=q[i],b=q[(i+1)%q.length],length=Math.hypot(b.x-a.x,b.z-a.z);if(!length)continue;const nx=(b.z-a.z)/length,nz=(a.x-b.x)/length;out=clip(out,nx,nz,a.x*nx+a.z*nz-distance);}return out;}
// Geometry-aligned subdivision with metre limits, never a phase/world-grid scale
// or a percentage-of-enclosure population target. No historical street is asserted.
export function partitionMetricResidential(polygon,policy){
 if(!policy||policy.metresPerSceneUnit!==1||policy.horizontalScale!==1||polygon.length<3)throw new Error('Metric housing requires canonical metre units');
 const parts=convex(polygon)?[polygon]:THREE.ShapeUtils.triangulateShape(polygon.map(p=>new THREE.Vector2(p.x,p.z)),[]).map(t=>t.map(i=>polygon[i])),cells=[];
 function divide(p,depth=0){if(p.length<3||polygonArea(p)<policy.minParcelAreaSquareMetres)return;let edge=null;for(let i=0;i<p.length;i++){const a=p[i],b=p[(i+1)%p.length],length=Math.hypot(b.x-a.x,b.z-a.z);if(!edge||length>edge.length+1e-6)edge={a,b,length};}const nx=(edge.b.x-edge.a.x)/edge.length,nz=(edge.b.z-edge.a.z)/edge.length,projections=p.map(q=>q.x*nx+q.z*nz),min=Math.min(...projections),max=Math.max(...projections);
  if(max-min<=policy.maxParcelSpanMetres||depth>=16){const inset=metricInset(p,policy.setbackMetres);if(inset.length>=3&&polygonArea(inset)>=policy.minParcelAreaSquareMetres)cells.push(inset);return;}
  const mid=(min+max)/2,gap=policy.accessGapMetres/2;for(const q of [clip(p,nx,nz,mid-gap),clip(p,-nx,-nz,-mid-gap)])divide(q,depth+1);
 }
 parts.forEach(p=>divide(p));
 // Binary halves can leave almost every terminal piece below the minimum lot
 // area (especially in long ridge quarters). Keep ALL existing cells first;
 // add balanced metre-width strips only in the unused remainder. No old ID,
 // dimensions or position is changed and no minimum-area rule is relaxed.
 const occupied=cells.map(p=>metricInset(p,-policy.accessGapMetres/2)),extra=[];
 function complete(p,depth=0){
  if(p.length<3||polygonArea(p)<policy.minParcelAreaSquareMetres||depth>16)return;
  let edge=null;for(let i=0;i<p.length;i++){const a=p[i],b=p[(i+1)%p.length],length=Math.hypot(b.x-a.x,b.z-a.z);if(!edge||length>edge.length+1e-6)edge={a,b,length};}
  const nx=(edge.b.x-edge.a.x)/edge.length,nz=(edge.b.z-edge.a.z)/edge.length,values=p.map(v=>v.x*nx+v.z*nz),min=Math.min(...values),max=Math.max(...values),count=Math.ceil((max-min-1e-7)/policy.maxParcelSpanMetres);
  if(count<=1){const q=metricInset(p,policy.setbackMetres);if(q.length>=3&&polygonArea(q)>=policy.minParcelAreaSquareMetres&&!occupied.some(o=>polygonsOverlap(q,o))){extra.push(q);occupied.push(metricInset(q,-policy.accessGapMetres/2));}return;}
  for(let k=0;k<count;k++){let q=clip(p,nx,nz,min+(max-min)*(k+1)/count-(k<count-1?policy.accessGapMetres/2:0));q=clip(q,-nx,-nz,-min-(max-min)*k/count-(k?policy.accessGapMetres/2:0));complete(q,depth+1);}
 }
 parts.forEach(p=>complete(p));return [...cells,...extra];
}
export function terrainResidentialAdmission(polygon,terrain,policy){const values=polygon.map(p=>terrain.heightAtWorld(p.x,p.z));if(values.some(v=>!Number.isFinite(v)))return{allowed:false,reason:'outside-canonical-terrain'};const relief=Math.max(...values)-Math.min(...values);return{allowed:relief<=policy.maxUnterracedReliefMetres,reason:relief<=policy.maxUnterracedReliefMetres?'within-engineering-relief-limit':'slope-needs-terrace-evidence',reliefMetres:relief};}
export function metricParcelsForBlock(block,terrain,policy){return partitionMetricResidential(block.geometry.polygon,policy).filter(p=>terrainResidentialAdmission(p,terrain,policy).allowed).map((polygon,i)=>({id:`${block.id}:metric-parcel:${i+1}`,type:'parcel',districtId:block.districtId,blockId:block.id,confidence:'inferred',geometry:{primitive:'polygon',polygon,terrainFollowing:true},orientation:{source:'metric-boundary-subdivision',tangent:{x:1,z:0}},typologyPool:['courtyard-house'],metadata:{generator:'metric-residential-layout-v1',metricPolicy:policy,semanticBox:false,gridGenerated:false,subdivisionAuthority:'engineering-layout-not-excavated-parcels'}}));}
export function applyMetricResidentialRegistration(registration,phase=registration.phase){registration.metricResidentialPolicy=metricResidentialPolicy(phase);registration.generation={...registration.generation,metricCompleteInfill:true};return registration;}
function hull(points){const p=[...points].sort((a,b)=>a.x-b.x||a.z-b.z),half=values=>{const out=[];for(const v of values){while(out.length>=2&&cross(out.at(-2),out.at(-1),v)<=0)out.pop();out.push(v);}return out;};return [...half(p).slice(0,-1),...half([...p].reverse()).slice(0,-1)];}
// Preserve authored offsets/dimensions. Pre-urban additions stay in the existing
// dwelling cloud; David uses the existing ridge region, excluding northern sacred
// ground, royal courtyards and the registered paths.
export function augmentMetricEarlySettlement(data,terrain){
 const policy=metricResidentialPolicy(data.phase),a=geographicToENU(data.spring.lat,data.spring.lon,terrain.grid.origin),spring={x:a.east,z:-a.north},royal=data.houseTypology==='four-room-analogy',w=royal?(data.houseDimensions?.[0]||10):6.2,d=royal?(data.houseDimensions?.[1]||13):6.8;
 const rectangle=([x,z],pad=0)=>[{x:x-w/2-pad,z:z-d/2-pad},{x:x+w/2+pad,z:z-d/2-pad},{x:x+w/2+pad,z:z+d/2+pad},{x:x-w/2-pad,z:z+d/2+pad}],occupied=data.houseOffsets.map(p=>rectangle(p,1)),zone=royal?data.royalCity.davidWall.slice(0,-1).map(([x,z])=>({x,z})):hull(occupied.flat()),paths=royal?compileRoyalSpatialLayout(data).edges.flatMap(e=>e.points.slice(1).map((b,i)=>[e.points[i],b])):data.pathOffsets.slice(1).map((b,i)=>[data.pathOffsets[i],b]);
 const reserved=(data.royalCity?.courtyards||[]).map(c=>{const [x,z]=c.offset;return [{x:x-24,z:z-18},{x:x+24,z:z-18},{x:x+24,z:z+18},{x:x-24,z:z+18}];});
 const cells=partitionMetricResidential(zone,{...policy,maxParcelSpanMetres:royal?18:12,minParcelAreaSquareMetres:royal?80:35}),added=[];
 for(const cell of cells){const candidate=[cell.reduce((s,p)=>s+p.x,0)/cell.length,cell.reduce((s,p)=>s+p.z,0)/cell.length],p=rectangle(candidate);if(!p.every(v=>pointInPolygon(v,zone))||occupied.some(q=>polygonsOverlap(p,q))||reserved.some(q=>polygonsOverlap(p,q)))continue;const world=p.map(v=>({x:spring.x+v.x,z:spring.z+v.z}));if(!terrainResidentialAdmission(world,terrain,policy).allowed)continue;
  if(paths.some(([a,b])=>{const dx=b[0]-a[0],dz=b[1]-a[1],L=dx*dx+dz*dz,t=L?Math.max(0,Math.min(1,((candidate[0]-a[0])*dx+(candidate[1]-a[1])*dz)/L)):0;return Math.hypot(candidate[0]-a[0]-t*dx,candidate[1]-a[1]-t*dz)<Math.max(w,d)/2+2;}))continue;
  occupied.push(rectangle(candidate,1));added.push(candidate);
 }
 return {...data,houseOffsets:[...data.houseOffsets,...added],metricResidentialPolicy:policy,metricResidentialAudit:{originalHouses:data.houseOffsets.length,addedIllustrativeHouses:added.length,zone:royal?'existing-david-ridge-region-not-northern-sacred-precinct':'existing-dwelling-cloud-only',knownDimensionsRescaled:false,populationVerified:false}};
}
