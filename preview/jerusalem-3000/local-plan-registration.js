import {geographicToENU} from './terrain-runtime.js';
const finitePoint=p=>Array.isArray(p)&&p.length===2&&p.every(Number.isFinite);
const https=v=>typeof v==='string'&&v.startsWith('https://');
// Uniform scale + rotation, preserving image-down coordinates. No affine stretch.
export function registerLocalPlan(entry,origin){
 const missing=[];
 if(!entry.objectId||!['wall-footprint','underground-centerline'].includes(entry.kind))throw new Error('Invalid local geometry target');
 if(!entry.source?.sha256||!entry.source?.url||!entry.source?.locator)missing.push('source-plan');
 if(!entry.controls?.length)missing.push('survey-controls');
 if(!entry.checkpoints?.length)missing.push('independent-checkpoints');
 if(!entry.points?.length)missing.push('digitized-geometry');
 if(!entry.vertical)missing.push('vertical-authority');
 if(!entry.datingVariant)missing.push('dating-variant');
 if(missing.length)return{objectId:entry.objectId,renderable:false,status:'withheld',missing};
 if(!https(entry.source.url)||!/^[a-f0-9]{64}$/.test(entry.source.sha256)||typeof entry.source.locator!=='string'||!entry.source.locator.trim()||entry.controls.length!==2||!entry.checkpoints.length||![origin?.lat,origin?.lon].every(Number.isFinite))throw new Error('Invalid plan provenance or calibration');
 const read=c=>{
  if(!finitePoint(c.local)||![c.lat,c.lon].every(Number.isFinite)||Math.abs(c.lat)>90||Math.abs(c.lon)>180||!https(c.source)||c.authority!=='registered-survey-control')throw new Error('Modern map points cannot substitute for survey controls');
  return geographicToENU(c.lat,c.lon,origin);
 };
 const [c0,c1]=entry.controls,[p0,p1]=entry.controls.map(read),du=c1.local[0]-c0.local[0],dv=c1.local[1]-c0.local[1],den=du*du+dv*dv;
 if(den<1e-6)throw new Error('Degenerate control baseline');
 const de=p1.east-p0.east,dn=p1.north-p0.north,a=(de*du-dn*dv)/den,b=(de*dv+dn*du)/den,scale=Math.hypot(a,b);
 if(!(entry.metresPerUnit>0)||!(entry.scaleToleranceFraction>0&&entry.scaleToleranceFraction<=.1)||Math.abs(scale/entry.metresPerUnit-1)>entry.scaleToleranceFraction)throw new Error('Plan scale mismatch');
 const transform=p=>{if(!finitePoint(p))throw new Error('Invalid digitized point');const u=p[0]-c0.local[0],v=p[1]-c0.local[1];return{x:p0.east+a*u+b*v,z:-(p0.north+b*u-a*v)};};
 if(!(entry.maxResidualMetres>0&&entry.maxResidualMetres<=5))throw new Error('Invalid checkpoint tolerance');
 let independent=false,maxResidual=0;
 for(const c of entry.checkpoints){const expected=read(c),actual=transform(c.local);if(Math.abs(du*(c.local[1]-c0.local[1])-dv*(c.local[0]-c0.local[0]))>1e-6)independent=true;maxResidual=Math.max(maxResidual,Math.hypot(actual.x-expected.east,actual.z+expected.north));}
 if(!independent||maxResidual>entry.maxResidualMetres)throw new Error('Independent orientation/checkpoint validation failed');
 const minimum=entry.kind==='wall-footprint'?3:2;if(entry.points.length<minimum)throw new Error('Incomplete local geometry');
 const points=entry.points.map(transform);
 if(entry.kind==='wall-footprint'){const area=points.reduce((sum,p,i)=>{const q=points[(i+1)%points.length];return sum+p.x*q.z-q.x*p.z;},0);if(Math.abs(area)<1e-6)throw new Error('Degenerate wall footprint');const cross=(a,b,c)=>(b.x-a.x)*(c.z-a.z)-(b.z-a.z)*(c.x-a.x);for(let i=0;i<points.length;i++)for(let j=i+1;j<points.length;j++){if(j===i+1||(i===0&&j===points.length-1))continue;const a=points[i],b=points[(i+1)%points.length],c=points[j],d=points[(j+1)%points.length];if(cross(a,b,c)*cross(a,b,d)<0&&cross(c,d,a)*cross(c,d,b)<0)throw new Error('Self-intersecting wall footprint');}}
 else if(points.some((p,i)=>i&&Math.hypot(p.x-points[i-1].x,p.z-points[i-1].z)<1e-6))throw new Error('Degenerate centerline segment');
 if(typeof entry.datingVariant!=='string'||!entry.datingVariant.trim())throw new Error('Invalid dating variant');
 const vertical=entry.vertical;
 if(!https(vertical.source)||vertical.datum!=='canonical-scene-metres'||!Array.isArray(vertical.elevations)||vertical.elevations.length!==points.length||!vertical.elevations.every(Number.isFinite))throw new Error('Missing sourced vertical registration');
 return{objectId:entry.objectId,status:'registered-plan-candidate',renderable:true,frame:'canonical-dem-enu',geometryVerified:false,scale,maxResidualMetres:maxResidual,datingVariant:entry.datingVariant,source:entry.source,geometry:{primitive:entry.kind==='wall-footprint'?'polygon':'polyline',[entry.kind==='wall-footprint'?'polygon':'points']:points.map((p,i)=>({...p,y:vertical.elevations[i]}))},renderPolicy:'reviewed-local-geometry-only-not-complete-city-or-hydraulic-simulation'};
}
export function auditLocalPlanRegistry(data,origin){
 if(data?.schema!=='j3k.local-plan-registry.v1'||!Array.isArray(data.entries))throw new Error('Invalid local plan registry');
 const ids=new Set();return data.entries.map(entry=>{if(ids.has(entry.objectId))throw new Error('Duplicate local plan object');ids.add(entry.objectId);return registerLocalPlan(entry,origin);});
}
