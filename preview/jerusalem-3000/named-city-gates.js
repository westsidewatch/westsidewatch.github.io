import * as THREE from 'three';
import {geographicToENU} from './terrain-runtime.js';
import {pointInPolygon} from './urban-exclusion.js';
const PHASES=['ottoman','outside-walls','modern'];
export function compileNamedCityGates(data,reference,terrain){
 if(data.schema!=='j3k.named-city-gates.v1'||data.gates.length!==8)throw new Error('Named gate inventory requires all8 gates');
 return data.gates.map(raw=>{const q=geographicToENU(raw.point.lat,raw.point.lon,terrain.grid.origin),center={x:q.east,z:-q.north};let closest=null;
  for(const line of reference.lines)for(let i=1;i<line.length;i++){const a=line[i-1],b=line[i],dx=b.x-a.x,dz=b.z-a.z,L=Math.hypot(dx,dz);if(L<.1)continue;const t=Math.max(0,Math.min(1,((center.x-a.x)*dx+(center.z-a.z)*dz)/(L*L))),distance=Math.hypot(a.x+t*dx-center.x,a.z+t*dz-center.z);if(!closest||distance<closest.distance)closest={distance,point:{x:a.x+t*dx,z:a.z+t*dz},unit:{x:dx/L,z:dz/L}};}
  let unit=closest.unit,normal={x:-unit.z,z:unit.x};if(!pointInPolygon({x:closest.point.x+normal.x*3,z:closest.point.z+normal.z*3},reference.envelope)){normal={x:-normal.x,z:-normal.z};unit={x:-unit.x,z:-unit.z};}
  const bodyCenter=raw.osmNode?{x:center.x+normal.x*raw.designDepth/2,z:center.z+normal.z*raw.designDepth/2}:center,at=(u,v)=>({x:bodyCenter.x+unit.x*u+normal.x*v,z:bodyCenter.z+unit.z*u+normal.z*v}),w=raw.designWidth,d=raw.designDepth;
  return {...raw,x:center.x,z:center.z,center,bodyCenter,unit,normal,at,footprint:[at(-w/2-1,-d/2-1),at(w/2+1,-d/2-1),at(w/2+1,d/2+1),at(-w/2-1,d/2+1)],bent:['bent-square','towered-bent'].includes(raw.profile),sources:[...raw.sources,data.source.url]};
 });
}
// Choose the side opening toward the existing interior street; never force a
// straight road through the rear wall of an L-shaped gatehouse.
export function registerNamedGateApproaches(registration,gates){
 if(!PHASES.includes(registration.phase))return;
 const axes=registration.roads.filter(r=>!r.metadata?.gateReference&&!r.metadata?.coreReference),makeId=g=>`j3k:${registration.phase}:independent:road:${g.key}-approach-design`;
 for(const gate of gates){
  registration.reservations.push({id:`j3k:${registration.phase}:reservation:${gate.key}-gatehouse`,geometry:{polygon:gate.footprint},metadata:{groundRole:'public-context'},source:{urls:gate.sources}});
  if(gate.sealed)continue;let nearest=null;
  for(const road of axes)for(let i=1;i<road.geometry.points.length;i++){const a=road.geometry.points[i-1],b=road.geometry.points[i],dx=b.x-a.x,dz=b.z-a.z,L=dx*dx+dz*dz,t=L?Math.max(0,Math.min(1,((gate.center.x-a.x)*dx+(gate.center.z-a.z)*dz)/L)):0,p={x:a.x+t*dx,z:a.z+t*dz},v=(p.x-gate.center.x)*gate.normal.x+(p.z-gate.center.z)*gate.normal.z;if(v<gate.designDepth/2+4)continue;const distance=Math.hypot(p.x-gate.center.x,p.z-gate.center.z);if(!nearest||distance<nearest.distance)nearest={p,distance,road};}
  if(!nearest)throw new Error(`No interior street for ${gate.key}`);
  const direction=(nearest.p.x-gate.center.x)*gate.unit.x+(nearest.p.z-gate.center.z)*gate.unit.z>=0?1:-1;
  // Direction is a display-route decision, not a historical entrance survey.
  gate.exitSign=direction;
  const exit=gate.bent?gate.at(direction*(gate.designWidth/2+4),0):gate.at(0,gate.designDepth/2),via=gate.bent?gate.at(direction*(gate.designWidth/2+4),gate.designDepth/2+4):gate.at(0,gate.designDepth/2+4);
  const id=makeId(gate),old=registration.roads.find(r=>r.id===id),record={id,type:'road',confidence:'inferred',geometry:{frame:'canonical-dem-enu',status:'named-gate-display-link-not-surveyed-street',primitive:'polyline',points:[gate.center,...(gate.bodyCenter!==gate.center?[gate.bodyCenter]:[]),exit,via,nearest.p],widthMetres:gate.profile==='small-pointed'?2.4:gate.profile==='towered-bent'?5:3.6},source:{urls:gate.sources,authority:'authored traversable gatehouse connection'},metadata:{layoutRole:'old-city-route-context',gateReference:gate.id,axisReference:nearest.road.id,routeGeometryVerified:false}};
  if(old)Object.assign(old,record);else registration.roads.push(record);
 }
}
export function publishNamedCityGates(core,gates){
 for(const gate of gates){const existing=core.get(gate.id);if(existing)continue;
  const events=PHASES.flatMap(phase=>[...(gate.firstYear&&phase==='outside-walls'?[{phase,offset:0,state:'unresolved',authority:'pre1889 selected expansion context; not physical demolition'}]:[]),{phase,offset:gate.firstYear?(phase==='ottoman'?(gate.firstYear-1517)/400:phase==='outside-walls'?(gate.firstYear-1800)/117:0):0,state:'transform',authority:'selected later gate context; not verified original fabric'}]);
  core.register({id:gate.id,type:'gate',confidence:'inferred',phaseIds:PHASES,lifecycle:{events},source:{urls:gate.sources,label:gate.label},metadata:{name:gate.label,geometryVerified:false,geometryReuseVerified:false,referenceOnly:true}});
 }
}
// All gates use real open passages except the explicitly sealed Golden Gate.
// Forms are individual coarse references; no fine facade reconstruction claimed.
export function namedGateGeometry(gate,terrain){
 const parts=[],W=gate.designWidth,D=gate.designDepth,H=gate.designHeight,T=1.2,P=gate.profile==='small-pointed'?3:gate.profile==='towered-bent'?6:4,opening=6,ground=Math.max(...gate.footprint.map(p=>terrain.heightAtWorld(p.x,p.z)));
 const locate=g=>{const p=g.attributes.position;for(let i=0;i<p.count;i++){const q=gate.at(p.getX(i),p.getZ(i)),y=p.getY(i);p.setXYZ(i,q.x,(y<=1e-6?terrain.heightAtWorld(q.x,q.z):ground)+y+.12,q.z);}g.computeVertexNormals();parts.push(g);};
 const box=(x,z,w,d,h,y=0)=>{const g=new THREE.BoxGeometry(w,h,d);g.translate(x,y+h/2,z);locate(g);};
 const portal=(width,height,x,z,angle=0,sealed=false)=>{
  const r=P/2,spring=opening-r,shape=new THREE.Shape();shape.moveTo(-width/2,0);shape.lineTo(-r,0);shape.lineTo(-r,spring);
  if(['small-pointed','paired-relief','rosette-tower','bent-square','towered-bent'].includes(gate.profile)){shape.quadraticCurveTo(-r,opening-r*.3,0,opening);shape.quadraticCurveTo(r,opening-r*.3,r,spring);}else for(let i=1;i<=16;i++){const a=Math.PI-Math.PI*i/16;shape.lineTo(r*Math.cos(a),spring+r*Math.sin(a));}
  shape.lineTo(r,0);shape.lineTo(width/2,0);shape.lineTo(width/2,height);shape.lineTo(-width/2,height);shape.closePath();const g=new THREE.ExtrudeGeometry(shape,{depth:T,bevelEnabled:false});g.translate(0,0,-T/2);g.rotateY(angle);g.translate(x,0,z);locate(g);if(sealed){const panel=new THREE.BoxGeometry(P,opening,T*.4);panel.rotateY(angle);panel.translate(x,opening/2,z);locate(panel);}
 };
 if(gate.sealed){
  const third=W/2;for(const side of [-1,1])portal(third,H,side*W/4,-D/2,0,true);box(0,D/2,W,T,H);for(const side of [-1,1])box(side*(W/2-T/2),0,T,D,H);box(0,0,W,D,1,H);for(const side of [-1,1]){const g=new THREE.SphereGeometry(4,12,6,0,Math.PI*2,0,Math.PI/2);g.translate(side*W/4,H+1,0);locate(g);}
 }else{
  portal(W,H,0,-D/2);
  if(gate.bent){box(0,D/2,W,T,H);box(-gate.exitSign*(W/2-T/2),0,T,D,H);portal(D,H,gate.exitSign*W/2,0,Math.PI/2);}else{portal(W,H,0,D/2);for(const side of [-1,1])box(side*(W/2-T/2),0,T,D,H);}
  box(0,0,W,D,.8,H);
  if(gate.profile==='towered-bent')for(const side of [-1,1])box(side*(W/2-3),-D/2+3,6,8,3,H);
  if(gate.profile==='paired-relief')for(const side of [-1,1])for(const offset of [-.6,.6])box(side*(P/2+2)+offset,-D/2-T/2,.8,.35,.7,opening);
  if(gate.profile==='rosette-tower'){const g=new THREE.CylinderGeometry(.7,.7,.2,12);g.rotateX(Math.PI/2);g.translate(0,opening+1.5,-D/2-T/2);locate(g);}
 }
 // Parapet merlons follow the individual gate frontage, not a generic torus marker.
 for(let x=-W/2+.8;x<W/2;x+=2.5)box(x,-D/2,.9,1,1,H+.8);
 const positions=[];for(const g of parts){const p=g.attributes.position,indices=g.index?.array||Array.from({length:p.count},(_,i)=>i);for(const i of indices)positions.push(p.getX(i),p.getY(i),p.getZ(i));g.dispose();}const geometry=new THREE.BufferGeometry();geometry.setAttribute('position',new THREE.Float32BufferAttribute(positions,3));geometry.computeVertexNormals();return geometry;
}
