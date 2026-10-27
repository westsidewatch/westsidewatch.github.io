import * as THREE from 'three';
import {geographicToENU} from './terrain-runtime.js';
import {TemporalCityCore} from './temporal-city-core.js';
import {lifecycleStateAtPosition} from './construction-engine.js';
const PHASES=['ottoman','outside-walls','modern'],WALL='j3k:object:ottoman-wall';
export function compileWallReference(data,terrain){
 const origin=terrain?.grid?.origin;
 if(data?.schema!=='j3k.modern-wall-reference.v1'||origin?.lat!==data.origin?.lat||origin?.lon!==data.origin?.lon||!/^[a-f0-9]{64}$/.test(data.source?.rawSubsetSha256||'')||data.lines?.length!==7||data.gates?.length!==2)throw new Error('Invalid modern wall reference');
 const at=p=>{if(!Number.isFinite(p.lat)||!Number.isFinite(p.lon)||p.lat<31.77||p.lat>31.785||p.lon<35.222||p.lon>35.242)throw new Error('Invalid wall reference coordinate');const q=geographicToENU(p.lat,p.lon,origin),point={x:q.east,z:-q.north};if(!Number.isFinite(terrain.heightAtWorld(point.x,point.z)))throw new Error('Wall reference outside terrain');return point;};
 const lines=data.lines.map(l=>{if(!Number.isInteger(l.osmWay)||!Number.isInteger(l.version)||l.points.length<2||l.nodeIds.length!==l.points.length)throw new Error('Invalid OSM wall line');return l.points.map(at);});
 const envelope=data.occupationEnvelope.map(at),gates=data.gates.map(g=>({...g,...at(g.point)}));
 if(data.lines.map(l=>l.osmWay).join(',')!=='137726904,391433919,391433915,511655207,391433911,1080613976,391433907'||new Set(gates.map(g=>g.objectId)).size!==2||gates.some(g=>!['j3k:object:jaffa-gate-ottoman','j3k:object:damascus-gate-ottoman'].includes(g.objectId))||envelope.length<100)throw new Error('Invalid wall reference identity/envelope');
 const height=data.display.heightMetres,width=data.display.widthMetres;if(!(height>0&&height<=20&&width>0&&width<=5))throw new Error('Invalid illustrative wall dimensions');
 return {lines,envelope,gates,height,width,source:structuredClone(data.source),gaps:structuredClone(data.gaps),phases:[...PHASES],geometryVerified:false};
}
export function wallGateApproaches(registration,reference){
 if(!reference||!PHASES.includes(registration.phase))return;
 registration.occupationEnvelope=reference.envelope.map(p=>({...p}));
 const jaffa=reference.gates.find(g=>g.objectId.endsWith('jaffa-gate-ottoman')),damascus=reference.gates.find(g=>g.objectId.endsWith('damascus-gate-ottoman'));
 const make=(key,gate,to)=>({id:`j3k:${registration.phase}:independent:road:${key}`,type:'road',confidence:'inferred',geometry:{frame:'canonical-dem-enu',status:'authored-gate-link-not-surveyed-street',primitive:'polyline',points:[{x:gate.x,z:gate.z},{...to}]},source:{authority:'modern gate point and authored connection to existing illustrative spine',urls:[`${reference.source.url}`, ...reference.source.historicalContext]},metadata:{layoutRole:'old-city-route-context',gateReference:gate.objectId,routeGeometryVerified:false}});
 const spine=registration.roads.find(r=>r.id.endsWith(':western-market-axis-context'));
 if(!spine)throw new Error('Wall reference needs existing western spine');
 registration.roads.push(make('jaffa-approach-design',jaffa,spine.geometry.points[2]),make('damascus-approach-design',damascus,spine.geometry.points[1]));
 for(const road of registration.roads)if(['westward-road-context','southwest-access-illustrative'].some(id=>road.id.endsWith(':'+id)))road.geometry.points[0]={x:jaffa.x,z:jaffa.z};
 // Connect to the edge of each illustrative core, keeping paths out of its mass.
 for(const core of registration.cores){
  const p=core.geometry.polygon,c={x:p.reduce((s,q)=>s+q.x,0)/p.length,z:p.reduce((s,q)=>s+q.z,0)/p.length};
  const axis=registration.roads.find(r=>r.id.endsWith(core.id.endsWith('holy-sepulchre-context')?':western-market-axis-context':':eastern-valley-link-illustrative'));
  if(!axis)throw new Error('Missing shared core approach axis');
  const start=axis.geometry.points.reduce((a,b)=>Math.hypot(a.x-c.x,a.z-c.z)<Math.hypot(b.x-c.x,b.z-c.z)?a:b);
  const dx=start.x-c.x,dz=start.z-c.z,halfX=(Math.max(...p.map(q=>q.x))-Math.min(...p.map(q=>q.x)))/2,halfZ=(Math.max(...p.map(q=>q.z))-Math.min(...p.map(q=>q.z)))/2;
  const scale=Math.max(Math.abs(dx)/halfX,Math.abs(dz)/halfZ);if(scale<=1)throw new Error('Core approach starts inside core');
  registration.roads.push({id:`${core.id.replace(':monument:',':road:')}-approach-design`,type:'road',confidence:'inferred',geometry:{frame:'canonical-dem-enu',status:'authored-core-link-not-surveyed-street',primitive:'polyline',points:[{...start},{x:c.x+dx/scale,z:c.z+dz/scale}]},source:{urls:[...core.source.urls],authority:'authored approach from shared illustrative axis to modern core position'},metadata:{layoutRole:'old-city-route-context',coreReference:core.id,routeGeometryVerified:false}});
 }
 registration.sources=[...new Set([...registration.sources,reference.source.url,...reference.source.historicalContext])];
 registration.limitations.push('後期舊城量體受現代地圖外城牆參照包絡約束；雅法門、大馬士革門動線是設計連接，非歷史街道測繪。現代開口只在規劃包絡閉合，城牆模型不補齊。');
}
export function createWallReferenceModel(parent,{reference,terrain,core}){
 const group=new THREE.Group();group.name='j3k-persistent-wall-reference';group.visible=false;parent.add(group);
 const material=new THREE.MeshStandardMaterial({color:0xc6b089,roughness:.95}),markerMaterial=new THREE.MeshStandardMaterial({color:0x715a32,roughness:.9}),meshes=[];
 const add=(geometry,id)=>{const mesh=new THREE.Mesh(geometry,id===WALL?material:markerMaterial);mesh.castShadow=true;mesh.receiveShadow=true;mesh.userData.cityObject={objectId:id,componentId:`${id}:modern-reference:${meshes.filter(m=>m.userData.cityObject.objectId===id).length}`,confidence:'inferred',kind:id===WALL?'wall-reference':'gate-location-marker'};group.add(mesh);meshes.push(mesh);};
 try{
  for(const line of reference.lines)for(let i=1;i<line.length;i++){
   const a=line[i-1],b=line[i],L=Math.hypot(b.x-a.x,b.z-a.z);if(L<.01)continue;const nx=-(b.z-a.z)/L*reference.width/2,nz=(b.x-a.x)/L*reference.width/2;
   const positions=[],steps=Math.ceil(L/8);
   for(let step=0;step<steps;step++){
    const from={x:a.x+(b.x-a.x)*step/steps,z:a.z+(b.z-a.z)*step/steps},to={x:a.x+(b.x-a.x)*(step+1)/steps,z:a.z+(b.z-a.z)*(step+1)/steps};
    let p=[{x:from.x+nx,z:from.z+nz},{x:to.x+nx,z:to.z+nz},{x:to.x-nx,z:to.z-nz},{x:from.x-nx,z:from.z-nz}];if(p.reduce((s,a,i)=>{const b=p[(i+1)%4];return s+a.x*b.z-b.x*a.z;},0)<0)p.reverse();
    const push=(i,top)=>positions.push(p[i].x,terrain.heightAtWorld(p[i].x,p[i].z)+(top?reference.height:.15),p[i].z);
    for(const i of [0,2,1,0,3,2])push(i,true);for(let j=0;j<4;j++){const k=(j+1)%4;for(const [n,t] of [[j,false],[k,true],[k,false],[j,false],[j,true],[k,true]])push(n,t);}
   }
   const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(positions,3));g.computeVertexNormals();add(g,WALL);
  }
  for(const gate of reference.gates){const g=new THREE.TorusGeometry(5,1.1,6,16);g.rotateX(-Math.PI/2);g.translate(gate.x,terrain.heightAtWorld(gate.x,gate.z)+1.5,gate.z);add(g,gate.objectId);}
  if(meshes.some(m=>Array.from(m.geometry.attributes.position.array).some(v=>!Number.isFinite(v))))throw new Error('Invalid wall model terrain fit');
  const candidate=new TemporalCityCore({phases:[...core.phases.values()],terrain});candidate.objects=new Map(core.objects);candidate.byPhase=new Map([...core.byPhase].map(([id,set])=>[id,new Set(set)]));candidate.links=new Map(core.links);
  for(const id of [WALL,...reference.gates.map(g=>g.objectId)]){
   const record=core.get(id);if(!record)throw new Error(`Missing existing wall/gate object ${id}`);const gate=reference.gates.find(g=>g.objectId===id);
   candidate.register({...record,confidence:'inferred',geometry:{frame:'canonical-dem-enu',status:'modern-map-reference-not-historical-survey',primitive:gate?'point':'multi-polyline',...(gate?{point:{x:gate.x,z:gate.z}}:{lines:reference.lines})},source:{...record.source,urls:[reference.source.url,...reference.source.historicalContext],modernReference:reference.source,historicalExistenceConfidence:record.confidence},metadata:{...record.metadata,rendererBinding:'modern-wall-reference-v1',geometryValidityPhases:[...PHASES],geometryVerified:false,referenceOnly:true,illustrativeDimensions:gate?null:{height:reference.height,width:reference.width},gapsNotFilled:true}});
  }
  const validation=candidate.validate();if(!validation.ok)throw new Error(validation.errors.join('; '));core.objects=candidate.objects;core.byPhase=candidate.byPhase;core.links=candidate.links;
 }catch(error){for(const m of meshes)m.geometry.dispose();material.dispose();markerMaterial.dispose();group.removeFromParent();throw error;}
 const timeline={phases:[...core.phases.values()]};let phase=null;
 return {meshes,anchors:()=>reference.gates.map(g=>({id:g.objectId,label:g.label+'（現代定位）',x:g.x,z:g.z,y:terrain.heightAtWorld(g.x,g.z)})),
  apply({position,evidenceAllowed}){phase=timeline.phases[Math.floor(position)]?.id;group.visible=PHASES.includes(phase);for(const m of meshes){const r=core.get(m.userData.cityObject.objectId),state=lifecycleStateAtPosition({lifecycleEvents:r.lifecycle.events},timeline,position);m.visible=evidenceAllowed('inferred')&&['build','transform','rebuild','expand'].includes(state);}},
  diagnostics(){return{phase,visible:group.visible&&meshes.some(m=>m.visible),visibleComponents:group.visible?meshes.filter(m=>m.visible).length:0,componentIds:meshes.map(m=>m.uuid),referenceOnly:true,geometryVerified:false,sourceGaps:reference.gaps.length};},
  dispose(){for(const m of meshes)m.geometry.dispose();material.dispose();markerMaterial.dispose();group.removeFromParent();}
 };
}
