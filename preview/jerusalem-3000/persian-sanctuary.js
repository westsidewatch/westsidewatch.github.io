import * as THREE from 'three';
import {compilePersianSanctuary} from './persian-sanctuary-layout.js';
import {geographicToENU} from './terrain-runtime.js';
import {settlementSurfaceHeight} from './earliest-settlement.js';
import {lifecycleStateAtPosition} from './construction-engine.js';
// Independent illustrative component assembly, never a clone of the First Temple.
export function createPersianSanctuary(parent,{data,terrain,core}) {
 const layout=compilePersianSanctuary(data),origin=geographicToENU(data.anchor.lat,data.anchor.lon,terrain.grid.origin),anchor={x:origin.east,z:-origin.north};
 const timeline={phases:[...core.phases.values()]},ids=[layout.objectId,layout.gate.id,layout.access.id];
 for(const id of ids)if(!core.get(id))throw new Error(`Missing shared sanctuary object ${id}`);
 const stone=new THREE.MeshStandardMaterial({color:0xd1bb96,roughness:1}),roof=new THREE.MeshStandardMaterial({color:0x8c7554,roughness:1}),path=new THREE.MeshStandardMaterial({color:0x79694f,roughness:1});
 const group=new THREE.Group();group.name='persian-sanctuary-reconstruction';group.visible=false;parent.add(group);const meshes=[];
 const surface=(x,z)=>{const y=settlementSurfaceHeight(terrain,anchor.x+x,anchor.z+z);if(!Number.isFinite(y))throw new Error('Persian sanctuary outside DEM');return y;};
 for(const part of layout.components){
  const {x,z,w,d,height,lift}=part,ground=Math.max(...[-1,1].flatMap(a=>[-1,1].map(b=>surface(x+a*w/2,z+b*d/2))));
  const geometry=new THREE.BoxGeometry(w,height,d),p=geometry.attributes.position;
  for(let i=0;i<p.count;i++)if(!lift&&p.getY(i)<0)p.setY(i,surface(x+p.getX(i),z+p.getZ(i))-ground-height/2);
  geometry.computeVertexNormals();const mesh=new THREE.Mesh(geometry,part.role==='roof'?roof:stone);
  mesh.position.set(anchor.x+x,ground+height/2+lift,anchor.z+z);mesh.castShadow=true;mesh.receiveShadow=true;
  mesh.userData.cityObject={objectId:part.role==='gate'?layout.gate.id:layout.objectId,componentId:`j3k:persian-sanctuary:${part.id}`,confidence:'inferred',role:part.role};group.add(mesh);meshes.push(mesh);
 }
 const vertices=[],pts=layout.access.points;
 for(let i=1;i<pts.length;i++){
  const [ax,az]=pts[i-1],[bx,bz]=pts[i],dx=bx-ax,dz=bz-az,length=Math.hypot(dx,dz),steps=Math.ceil(length/2),nx=-dz/length*layout.access.width/2,nz=dx/length*layout.access.width/2;
  for(let j=0;j<steps;j++)for(const [t,side] of [[j/steps,1],[(j+1)/steps,1],[j/steps,-1],[(j+1)/steps,1],[(j+1)/steps,-1],[j/steps,-1]]){const x=ax+dx*t+nx*side,z=az+dz*t+nz*side;vertices.push(anchor.x+x,surface(x,z)+.1,anchor.z+z);}
 }
 const geometry=new THREE.BufferGeometry();geometry.setAttribute('position',new THREE.Float32BufferAttribute(vertices,3));geometry.computeVertexNormals();const road=new THREE.Mesh(geometry,path);
 road.userData.cityObject={objectId:layout.access.id,componentId:'j3k:persian-sanctuary:access',confidence:'inferred',role:'access'};group.add(road);meshes.push(road);
 for(const id of ids){
  const parts=meshes.filter(m=>m.userData.cityObject.objectId===id),bounds=new THREE.Box3();for(const part of parts)bounds.expandByObject(part);
  const record=core.get(id);core.register({...record,geometry:{primitive:'component-assembly',frame:'canonical-dem-enu',status:'independent-inferred-sanctuary',bounds:{min:bounds.min.toArray(),max:bounds.max.toArray()}},metadata:{...record.metadata,rendererBinding:'persian-sanctuary-adapter-v1',geometryVerified:false,geometryReuseVerified:false,geometryValidityPhases:layout.geometryValidityPhases,componentIds:parts.map(p=>p.userData.cityObject.componentId),spatialTopology:id===layout.access.id?{from:layout.access.from,to:layout.objectId,points:pts.map(([x,z])=>({x:anchor.x+x,z:anchor.z+z}))}:id===layout.gate.id?{point:{x:anchor.x+layout.gate.point[0],z:anchor.z+layout.gate.point[1]}}:null}});
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
