import {lifecycleStateAtPosition} from './construction-engine.js';
import * as THREE from 'three';
import {geographicToENU} from './terrain-runtime.js';
import {settlementSurfaceHeight} from './earliest-settlement.js';
// Literary/interpretive reconstruction. No excavated wall circuit is asserted.
export function createRoyalCity(parent,{data,terrain,core}) {
  const origin=geographicToENU(data.spring.lat,data.spring.lon,terrain.grid.origin);
  const anchor={x:origin.east,z:-origin.north};
  const group=new THREE.Group();group.name='royal-city-reconstruction';group.visible=false;parent.add(group);
  const stone=new THREE.MeshStandardMaterial({color:0xb99c72,roughness:1});
  const templeStone=new THREE.MeshStandardMaterial({color:0xd8c6a1,roughness:.9});
  const roof=new THREE.MeshStandardMaterial({color:0x806549,roughness:1});
  const doorway=new THREE.MeshStandardMaterial({color:0x3e3327,roughness:1});
  if(!core)throw new Error('Royal geometry requires the shared object ledger');
  const timeline={phases:[...core.phases.values()]};
  const meshes=[];
  const ledgerId=(kind,stage)=>'j3k:object:'+(kind==='first-temple'?'first-temple':kind==='city-wall'?(stage==='david'?'royal-city-wall-hypothesis':'solomon-northern-wall-hypothesis'):(stage==='david'?'david-royal-courtyard-hypothesis':'solomon-royal-courtyard-hypothesis'));

  const surface=(x,z)=>settlementSurfaceHeight(terrain,anchor.x+x,anchor.z+z);
  function box(id,kind,x,z,w,d,h,stage='david',material=stone,angle=0) {
    const cs=Math.cos(angle),sn=Math.sin(angle);
    const corners=[[-w/2,-d/2],[w/2,-d/2],[-w/2,d/2],[w/2,d/2]];
    const topGround=Math.max(...corners.map(([a,b])=>surface(x+cs*a+sn*b,z-sn*a+cs*b)));
    if(!Number.isFinite(topGround))throw new Error('Royal city outside DEM');
    const geometry=new THREE.BoxGeometry(w,h,d),p=geometry.attributes.position;
    for(let i=0;i<p.count;i++)if(p.getY(i)<0)p.setY(i,surface(x+cs*p.getX(i)+sn*p.getZ(i),z-sn*p.getX(i)+cs*p.getZ(i))-topGround-h/2);
    geometry.computeVertexNormals();
    const mesh=new THREE.Mesh(geometry,material);mesh.position.set(anchor.x+x,topGround+h/2,anchor.z+z);mesh.rotation.y=angle;
    mesh.castShadow=true;mesh.receiveShadow=true;
    const objectId=ledgerId(kind,stage);if(!core.get(objectId))throw new Error(`Missing royal ledger object ${objectId}`);
    mesh.userData.cityObject={objectId,componentId:`j3k:royal:${id}`,kind,confidence:core.get(objectId).confidence,stage,footprintVerified:false};
    mesh.userData.restPositions=Float32Array.from(p.array);
    mesh.userData.groundHeights=Float32Array.from(Array.from({length:p.count},(_,i)=>surface(x+cs*p.getX(i)+sn*p.getZ(i),z-sn*p.getX(i)+cs*p.getZ(i))-mesh.position.y));

    group.add(mesh);meshes.push(mesh);return mesh;
  }
  function circuit(points,stage,prefix) {
    for(let j=1;j<points.length;j++) {
      const a=points[j-1],b=points[j],dx=b[0]-a[0],dz=b[1]-a[1],length=Math.hypot(dx,dz),count=Math.ceil(length/5),angle=-Math.atan2(dz,dx);
      for(let i=0;i<count;i++) {
        // Deliberate gateway gap; location and dimensions are illustrative.
        if(j===2&&i===Math.floor(count*(stage==='david'?.6:.5)))continue;
        box(`${prefix}-${j}-${i}`,'city-wall',a[0]+dx*(i+.5)/count,a[1]+dz*(i+.5)/count,length/count*.98,2.5,5,stage,stone,angle);
      }
    }
  }
  circuit(data.royalCity.davidWall,'david','david-wall');
  circuit(data.royalCity.northernWall,'solomon','north-wall');
  function courtyard(prefix,x,z,stage) {
    box(`${prefix}-west`,'royal-palace',x-18,z,8,32,7,stage);
    box(`${prefix}-east`,'royal-palace',x+18,z,8,32,7,stage);
    box(`${prefix}-north`,'royal-palace',x,z-13,28,6,8,stage);
    box(`${prefix}-south`,'royal-palace',x,z+13,28,6,6,stage);
  }
  courtyard('david-palace',-150,-115,'david');
  courtyard('solomon-palace',-110,-285,'solomon');
  const t=data.royalCity.temple,c=t.cubitMetres,l=t.lengthCubits*c,w=t.widthCubits*c,h=t.heightCubits*c,[x,z]=t.offset;
  box('temple-main','first-temple',x,z,l,w,h,'solomon',templeStone);
  box('temple-porch','first-temple',x+l/2+2.25,z,4.5,w,9,'solomon',templeStone);
  box('temple-door','first-temple',x+l/2+4.56,z,.12,2.6,4.5,'solomon',doorway);
  for(const side of [-1,1])box(`temple-side-${side}`,'first-temple',x-1,z+side*(w/2+1.5),l-2,3,6,'solomon');
  for(const side of [-1,1])box(`temple-pillar-${side}`,'first-temple',x+l/2+5.5,z+side*3,.8,.8,8,'solomon',roof);
  box('temple-altar','first-temple',x+l/2+16,z,4,4,2.5,'solomon');
  const bindings=new Map();
  for(const m of meshes){const id=m.userData.cityObject.objectId;if(!bindings.has(id))bindings.set(id,[]);bindings.get(id).push(m);}
  const footprints=new Map();
  for(const [id,parts] of bindings){
    const bounds=new THREE.Box3();for(const mesh of parts)bounds.expandByObject(mesh);
    footprints.set(id,{polygon:[{x:bounds.min.x,z:bounds.min.z},{x:bounds.max.x,z:bounds.min.z},{x:bounds.max.x,z:bounds.max.z},{x:bounds.min.x,z:bounds.max.z}]});
    const record=core.get(id);core.register({...record,geometry:{status:'inferred-component-assembly',frame:'canonical-dem-enu',primitive:'component-assembly',authority:'literary-and-illustrative-royal-city',bounds:{min:bounds.min.toArray(),max:bounds.max.toArray()}},metadata:{...record.metadata,rendererBinding:'royal-city-adapter-v1',componentIds:parts.map(m=>m.userData.cityObject.componentId),geometryVerified:false}});
  }
  const stateAt=(id,position)=>lifecycleStateAtPosition({lifecycleEvents:core.get(id).lifecycle.events},timeline,position);
  let stage='david',currentPosition=0;
  return {
    focus:new THREE.Vector3(anchor.x-110,surface(-110,-210)+5,anchor.z-210),
    templeFocus:new THREE.Vector3(anchor.x+x,surface(x,z)+5,anchor.z+z),
    exclusionsFor(phaseId){
      if(!['late-first-temple','babylonian-destruction'].includes(phaseId))return [];
      const position=timeline.phases.findIndex(p=>p.id===phaseId)+.5;
      return [...footprints].filter(([id])=>['first-temple','royal-palace'].includes(bindings.get(id)[0].userData.cityObject.kind)&&['build','transform','ruin'].includes(stateAt(id,position))).map(([id,zone])=>({...zone,id,authority:'inferred-royal-footprint-exclusion-not-survey'}));
    },
    apply({position=0,evidenceAllowed,ruin=1}) {
      currentPosition=position;stage=stateAt('j3k:object:first-temple',position)==='absent'?'david':'solomon';group.visible=false;
      for(const m of meshes){
        const record=core.get(m.userData.cityObject.objectId),state=stateAt(record.id,position);
        m.userData.cityObject.lifecycleState=state;
        m.visible=['build','transform','ruin'].includes(state)&&evidenceAllowed(record.confidence);group.visible ||= m.visible;
        const factor=state==='ruin'?1-.82*Math.max(0,Math.min(1,ruin)):1;
        if(m.userData.factor!==factor){
          const p=m.geometry.attributes.position,rest=m.userData.restPositions,ground=m.userData.groundHeights;
          for(let i=0;i<p.count;i++)p.setY(i,factor===1?rest[i*3+1]:ground[i]+(rest[i*3+1]-ground[i])*factor);
          p.needsUpdate=true;m.geometry.computeVertexNormals();m.userData.factor=factor;
        }
      }
    },
    diagnostics(){return {stage,position:currentPosition,visibleWalls:meshes.filter(m=>m.visible&&m.userData.cityObject.kind==='city-wall').length,visibleTemple:meshes.filter(m=>m.visible&&m.userData.cityObject.kind==='first-temple').length,visiblePalace:meshes.filter(m=>m.visible&&m.userData.cityObject.kind==='royal-palace').length,templeState:stateAt('j3k:object:first-temple',currentPosition),templeCompressionFactor:bindings.get('j3k:object:first-temple')[0].userData.factor,bindingIds:[...bindings.keys()],componentIdentity:meshes.map(m=>m.userData.cityObject.componentId).join('|'),wallCircuitVerified:false,palaceGeometryVerified:false,templeDimensionsMetres:[l,w,h],geometryReuseVerified:false,ruinAuthority:'schematic-vertex-compression-not-excavated-collapse'};},
    dispose(){meshes.forEach(m=>m.geometry.dispose());[stone,templeStone,roof,doorway].forEach(m=>m.dispose());group.removeFromParent();}
  };
}
