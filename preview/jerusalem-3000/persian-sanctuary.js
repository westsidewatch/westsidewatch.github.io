import {sanctuaryAccessVertices} from './sanctuary-access-geometry.js';
import * as THREE from 'three';
import {compilePersianSanctuary} from './persian-sanctuary-layout.js';
import {geographicToENU} from './terrain-runtime.js';
import {settlementSurfaceHeight} from './earliest-settlement.js';
import {lifecycleStateAtPosition} from './construction-engine.js';
// Independent illustrative component assembly, never a clone of the First Temple.
export function createPersianSanctuary(parent,{data,terrain,core}) {
 return createSanctuaryAssembly(parent,{data,terrain,core,layout:compilePersianSanctuary(data),prefix:'persian-sanctuary',binding:'persian-sanctuary-adapter-v1'});
}
// Geometry cache shared by independently authored period profiles, not reused historical fabric.
export function createSanctuaryAssembly(parent,{data,terrain,core,layout,prefix,binding}) {
 const origin=geographicToENU(data.anchor.lat,data.anchor.lon,terrain.grid.origin),anchor={x:origin.east,z:-origin.north};
 const timeline={phases:[...core.phases.values()]},ids=[layout.objectId,layout.gate.id,layout.access.id];
 for(const id of ids)if(!core.get(id))throw new Error(`Missing shared sanctuary object ${id}`);
 const stone=new THREE.MeshStandardMaterial({color:0xd1bb96,roughness:1}),roof=new THREE.MeshStandardMaterial({color:0x8c7554,roughness:1}),path=new THREE.MeshStandardMaterial({color:0x79694f,roughness:1});
 const group=new THREE.Group();group.name=`${prefix}-reconstruction`;group.visible=false;parent.add(group);const meshes=[];
 const surface=(x,z)=>{const y=settlementSurfaceHeight(terrain,anchor.x+x,anchor.z+z);if(!Number.isFinite(y))throw new Error(`${prefix} outside DEM`);return y;};
 const isHallPart=part=>part.id.startsWith('hall-')||part.id.startsWith('porch-');
 // One upper datum keeps the hall walls, lintel and roofs joined on sloping DEM.
 // Only ground-contact vertices follow terrain; this is not an ancient platform survey.
 const hallGround=Math.max(...layout.components.filter(isHallPart).flatMap(({x,z,w,d})=>[-1,1].flatMap(a=>[-1,1].map(b=>surface(x+a*w/2,z+b*d/2)))));
 for(const part of layout.components){
  const {x,z,w,d,height,lift}=part,ground=isHallPart(part)?hallGround:Math.max(...[-1,1].flatMap(a=>[-1,1].map(b=>surface(x+a*w/2,z+b*d/2))));
  const geometry=new THREE.BoxGeometry(w,height,d),p=geometry.attributes.position;
  for(let i=0;i<p.count;i++)if(!lift&&p.getY(i)<0)p.setY(i,surface(x+p.getX(i),z+p.getZ(i))-ground-height/2);
  geometry.computeVertexNormals();const mesh=new THREE.Mesh(geometry,part.role==='roof'?roof:stone);
  mesh.position.set(anchor.x+x,ground+height/2+lift,anchor.z+z);mesh.castShadow=true;mesh.receiveShadow=true;
  if(isHallPart(part))mesh.userData.templeSectionHeight=hallGround+4;
  mesh.userData.cityObject={objectId:part.role==='gate'?layout.gate.id:layout.objectId,componentId:`j3k:${prefix}:${part.id}`,confidence:'inferred',role:part.role};group.add(mesh);meshes.push(mesh);
 }
 const pts=layout.access.points,localVertices=sanctuaryAccessVertices(pts,layout.access.width,surface,(x,z,i,f)=>{
  const ground=surface(x,z)+.1;
  return i===pts.length-1?ground+f*Math.max(0,hallGround+.12-ground):ground;
 },{terrain,anchor});
 const vertices=localVertices.map((value,i)=>i%3===0?value+anchor.x:i%3===2?value+anchor.z:value);
 const geometry=new THREE.BufferGeometry();geometry.setAttribute('position',new THREE.Float32BufferAttribute(vertices,3));geometry.computeVertexNormals();const road=new THREE.Mesh(geometry,path);
 road.userData.cityObject={objectId:layout.access.id,componentId:`j3k:${prefix}:access`,confidence:'inferred',role:'access'};group.add(road);meshes.push(road);
 for(const id of ids){
  const parts=meshes.filter(m=>m.userData.cityObject.objectId===id),bounds=new THREE.Box3();for(const part of parts)bounds.expandByObject(part);
  const record=core.get(id);core.register({...record,geometry:{primitive:'component-assembly',frame:'canonical-dem-enu',status:'independent-inferred-sanctuary',bounds:{min:bounds.min.toArray(),max:bounds.max.toArray()}},metadata:{...record.metadata,rendererBinding:binding,geometryVerified:false,geometryReuseVerified:false,geometryValidityPhases:layout.geometryValidityPhases,componentIds:parts.map(p=>p.userData.cityObject.componentId),spatialTopology:id===layout.access.id?{from:layout.access.from,to:layout.objectId,points:pts.map(([x,z])=>({x:anchor.x+x,z:anchor.z+z}))}:id===layout.gate.id?{point:{x:anchor.x+layout.gate.point[0],z:anchor.z+layout.gate.point[1]}}:null}});
 }
 let position=0;
 const stateAt=(id)=>lifecycleStateAtPosition({lifecycleEvents:core.get(id).lifecycle.events},timeline,position);
 return {
  focus:new THREE.Vector3(anchor.x+layout.hall.offset[0],surface(...layout.hall.offset)+6,anchor.z+layout.hall.offset[1]),
  apply({position:value=0,evidenceAllowed=()=>true}){position=value;const phase=timeline.phases[Math.floor(position)]?.id;group.visible=false;for(const m of meshes){const record=core.get(m.userData.cityObject.objectId),state=stateAt(record.id);m.visible=layout.geometryValidityPhases.includes(phase)&&['build','rebuild','transform'].includes(state)&&evidenceAllowed(record.confidence);m.userData.cityObject.lifecycleState=state;group.visible ||= m.visible;}},
  diagnostics(){return{position,templeState:stateAt(layout.objectId),visibleTemple:meshes.filter(m=>m.visible&&m.userData.cityObject.objectId===layout.objectId).length,visibleGate:meshes.filter(m=>m.visible&&m.userData.cityObject.role==='gate').length,visibleAccess:road.visible,bindingIds:ids,componentIdentity:meshes.map(m=>m.userData.cityObject.componentId).join('|'),geometryValidityPhases:layout.geometryValidityPhases,geometryReuseVerified:false,geometryVerified:false,authority:layout.authority};},
  dispose(){meshes.forEach(m=>m.geometry.dispose());[stone,roof,path].forEach(m=>m.dispose());group.removeFromParent();}
 };
}
