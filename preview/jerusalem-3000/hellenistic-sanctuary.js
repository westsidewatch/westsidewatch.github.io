import {geographicToENU} from './terrain-runtime.js';
import {compileSanctuaryComponents} from './sanctuary-component-layout.js';
import {createSanctuaryAssembly} from './persian-sanctuary.js';
const PHASE='hellenistic-hasmonean';
export function compileHellenisticSanctuary(data,registration,origin) {
 if(data?.schema!=='j3k.hellenistic-sanctuary.v1'||registration.phase!==PHASE||data.sanctuary.geometryValidityPhases?.join()!==PHASE)throw new Error('Invalid Hellenistic sanctuary scope');
 const a=geographicToENU(data.anchor.lat,data.anchor.lon,origin),anchor={x:a.east,z:-a.north},s=data.sanctuary;
 const [xmin,zmin,xmax,zmax]=s.court.bounds,gateX=anchor.x+s.court.gateX,gateZ=anchor.z+zmax;
 // Join the existing street at its actual polyline, on the exterior side of the south gate.
 const road=registration.roads.find(r=>r.id===`j3k:${PHASE}:road:0`);let arrival=null;
 for(let i=1;i<(road?.geometry.points.length||0);i++){
  const a=road.geometry.points[i-1],b=road.geometry.points[i];if(a.x===b.x)continue;
  const t=(gateX-a.x)/(b.x-a.x),z=a.z+t*(b.z-a.z);
  if(t>=0&&t<=1&&z>gateZ+10)arrival=[s.court.gateX,z-anchor.z];
 }
 if(!arrival)throw new Error('No contemporary sanctuary street arrival');
 const reservationId=`j3k:${PHASE}:reservation:sanctuary`,accessId=`j3k:${PHASE}:road:sanctuary-access`,gateId=`j3k:${PHASE}:gate:sanctuary-south`;
 const reservation={id:reservationId,polygon:[[xmin-3,zmin-3],[xmax+3,zmin-3],[xmax+3,zmax+3],[xmin-3,zmax+3]].map(([x,z])=>({x:anchor.x+x,z:anchor.z+z}))};
 const accessReservation={id:`${reservationId}-approach`,polygon:[{x:gateX-3,z:gateZ},{x:gateX+3,z:gateZ},{x:gateX+3,z:anchor.z+arrival[1]},{x:gateX-3,z:anchor.z+arrival[1]}]};
 const localReservation={id:reservationId,polygon:reservation.polygon.map(p=>[p.x-anchor.x,p.z-anchor.z])};
 const layout=compileSanctuaryComponents({sanctuary:s,roads:[{id:road.id,points:[arrival]}],reservations:[localReservation]}, {phaseId:PHASE,gateId,accessId,approachId:road.id,approachObjectId:road.id,reservationId});
 return {...layout,reservations:[reservation,accessReservation],roadExclusions:[reservation]};
}
export function createHellenisticSanctuary(parent,{data,layout,terrain,core}) {
 const institution='j3k:object:second-temple-early';if(!core.get(institution))throw new Error('Missing shared Second Temple institution');
 for(const [id,type,label]of [[layout.objectId,'monument','哈斯蒙尼重新奉獻聖所'],[layout.gate.id,'gate','聖域南側示意入口'],[layout.access.id,'road','聖域示意通路']])core.register({id,type,phaseIds:[PHASE],confidence:'inferred',source:{label,urls:layout.sources},lifecycle:{events:[{phase:PHASE,state:'transform'}]},metadata:{name:label,institutionId:institution,referencePeriod:'選取前164年重新奉獻後語境；尺寸、位置與形制未核定，不代表整期',geometryValidityPhases:[PHASE],geometryVerified:false,geometryReuseVerified:false,nextEraFate:'representation-withheld-not-demolition',limitations:layout.limitations}});
 return createSanctuaryAssembly(parent,{data,layout,terrain,core,prefix:'hellenistic-sanctuary',binding:'hellenistic-sanctuary-adapter-v1'});
}
