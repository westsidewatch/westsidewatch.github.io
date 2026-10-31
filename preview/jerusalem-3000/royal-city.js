import {compileRoyalSpatialLayout} from './royal-spatial-layout.js';
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
  const spatial=compileRoyalSpatialLayout(data);
  const pathMaterial=new THREE.MeshStandardMaterial({color:0x7d6c53,roughness:1});
  const meshes=[];
  const ledgerId=(kind,stage)=>'j3k:object:'+(kind==='first-temple'?'first-temple':kind==='city-wall'?(stage==='david'?'royal-city-wall-hypothesis':'solomon-northern-wall-hypothesis'):(stage==='david'?'david-royal-courtyard-hypothesis':'solomon-royal-courtyard-hypothesis'));

  const surface=(x,z)=>settlementSurfaceHeight(terrain,anchor.x+x,anchor.z+z);
  function box(id,kind,x,z,w,d,h,stage='david',material=stone,angle=0,lift=0,objectIdOverride=null,levelGround=null) {
    const cs=Math.cos(angle),sn=Math.sin(angle);
    const corners=[[-w/2,-d/2],[w/2,-d/2],[-w/2,d/2],[w/2,d/2]];
    const topGround=levelGround??Math.max(...corners.map(([a,b])=>surface(x+cs*a+sn*b,z-sn*a+cs*b)));
    if(!Number.isFinite(topGround))throw new Error('Royal city outside DEM');
    const geometry=new THREE.BoxGeometry(w,h,d),p=geometry.attributes.position;
    for(let i=0;i<p.count;i++)if(lift===0&&p.getY(i)<0)p.setY(i,surface(x+cs*p.getX(i)+sn*p.getZ(i),z-sn*p.getX(i)+cs*p.getZ(i))-topGround-h/2);
    geometry.computeVertexNormals();
    const mesh=new THREE.Mesh(geometry,material);mesh.position.set(anchor.x+x,topGround+h/2+lift,anchor.z+z);mesh.rotation.y=angle;
    mesh.castShadow=true;mesh.receiveShadow=true;
    const objectId=objectIdOverride||ledgerId(kind,stage);if(!core.get(objectId))throw new Error(`Missing royal ledger object ${objectId}`);
    mesh.userData.cityObject={objectId,componentId:`j3k:royal:${id}`,kind,confidence:core.get(objectId).confidence,stage,footprintVerified:false};
    mesh.userData.restPositions=Float32Array.from(p.array);
    mesh.userData.groundHeights=Float32Array.from(Array.from({length:p.count},(_,i)=>surface(x+cs*p.getX(i)+sn*p.getZ(i),z-sn*p.getX(i)+cs*p.getZ(i))-mesh.position.y));

    group.add(mesh);meshes.push(mesh);return mesh;
  }
  function circuit(points,stage,prefix){
    for(let j=1;j<points.length;j++){
      const a=points[j-1],b=points[j],dx=b[0]-a[0],dz=b[1]-a[1],length=Math.hypot(dx,dz),angle=-Math.atan2(dz,dx),intervals=[];
      let cursor=0,index=0;
      for(const gate of spatial.gates.filter(g=>g.wall===prefix&&g.segment===j).sort((a,b)=>a.t-b.t)){
        const left=gate.t*length-gate.width/2,right=gate.t*length+gate.width/2;
        intervals.push([cursor,left]);cursor=right;
      }
      intervals.push([cursor,length]);
      for(const [start,end] of intervals){const span=end-start,count=Math.ceil(span/5);
        for(let i=0;i<count;i++){const distance=start+span*(i+.5)/count;box(`${prefix}-${j}-${index++}`,'city-wall',a[0]+dx*distance/length,a[1]+dz*distance/length,span/count*.98,2.5,5,stage,stone,angle);}
      }
    }
  }
  circuit(data.royalCity.davidWall,'david','david-wall');
  circuit(data.royalCity.northernWall,'solomon','north-wall');
  function courtyard(prefix,x,z,stage) {
    box(`${prefix}-west`,'royal-palace',x-18,z,8,32,7,stage);
    box(`${prefix}-east`,'royal-palace',x+18,z,8,32,7,stage);
    box(`${prefix}-north`,'royal-palace',x,z-13,28,6,8,stage);
    for(const side of [-1,1])box(`${prefix}-south-${side}`,'royal-palace',x+side*7.75,z+13,12.5,6,6,stage);
  }
  for(const court of data.royalCity.courtyards)courtyard(court.id,...court.offset,court.stage);
  const t=data.royalCity.temple,c=t.cubitMetres,l=t.lengthCubits*c,w=t.widthCubits*c,h=t.heightCubits*c,[x,z]=t.offset;
  // One display datum for the ensemble; footing bottoms still meet the DEM.
  const templeGround=Math.max(...[[-l/2,-w/2-7*c],[-l/2,w/2+7*c],[l/2+10*c,-w/2-7*c],[l/2+10*c,w/2+7*c]].map(([dx,dz])=>surface(x+dx,z+dz)));
  const templeBox=(id,px,pz,pw,pd,ph,material=templeStone,lift=0)=>box(id,'first-temple',px,pz,pw,pd,ph,'solomon',material,0,lift,null,templeGround);
  templeBox('temple-main',x,z,l,w,h);
  // Existing illustrative doorway width/porch height are not textual measures.
  const opening=2.6,porchHeight=9,porchDepth=10*c,porchX=x+l/2+porchDepth/2;
  for(const side of [-1,1])templeBox(`temple-porch-jamb-${side}`,porchX,z+side*(opening/2+(w-opening)/4),porchDepth,(w-opening)/2,porchHeight);
  templeBox('temple-porch-lintel',porchX,z,porchDepth,opening,porchHeight-4.5,templeStone,4.5);
  templeBox('temple-door',x+l/2+.06,z,.12,opening,4.5,doorway);
  // 1Kings6:6,10: three five-cubit-high side-room tiers, widths5/6/7 cubits.
  for(let tier=0;tier<3;tier++)for(const side of [-1,1]){const depth=(5+tier)*c;templeBox(`temple-side-${side}-tier-${tier+1}`,x-1,z+side*(w/2+depth/2),l-2,depth,5*c,stone,tier*5*c);}
  for(const side of [-1,1])templeBox(`temple-pillar-${side}`,x+l/2+10*c+1,z+side*3,.8,.8,8,roof);
  templeBox('temple-altar',x+l/2+16,z,4,4,2.5,stone);
  for(const gate of spatial.gates){
    const [gx,gz]=gate.offset,id=`j3k:object:royal-gate:${gate.id}`;
    for(const side of [-1,1])box(`gate-${gate.id}-post-${side}`,'city-gate',gx+gate.unit[0]*side*(gate.width/2+.5),gz+gate.unit[1]*side*(gate.width/2+.5),1,2.5,4,gate.stage,stone,gate.angle,0,id);
    box(`gate-${gate.id}-lintel`,'city-gate',gx,gz,gate.width+2,2.5,1,gate.stage,stone,gate.angle,4,id);
  }
  for(const edge of spatial.edges){
    const vertices=[];
    for(let i=1;i<edge.points.length;i++){
      const a=edge.points[i-1],b=edge.points[i],dx=b[0]-a[0],dz=b[1]-a[1],length=Math.hypot(dx,dz),steps=Math.ceil(length/2),nx=-dz/length*spatial.roadWidth/2,nz=dx/length*spatial.roadWidth/2;
      for(let j=0;j<steps;j++)for(const [t,side] of [[j/steps,1],[(j+1)/steps,1],[j/steps,-1],[(j+1)/steps,1],[(j+1)/steps,-1],[j/steps,-1]]){
        const x=a[0]+dx*t+nx*side,z=a[1]+dz*t+nz*side;vertices.push(anchor.x+x,surface(x,z)+.09,anchor.z+z);
      }
    }
    const geometry=new THREE.BufferGeometry();geometry.setAttribute('position',new THREE.Float32BufferAttribute(vertices,3));geometry.computeVertexNormals();
    const mesh=new THREE.Mesh(geometry,pathMaterial),id=`j3k:object:royal-road:${edge.id}`;
    if(!core.get(id))throw new Error(`Missing spatial ledger object ${id}`);
    mesh.userData.cityObject={objectId:id,componentId:`j3k:royal:road:${edge.id}`,kind:'city-road',confidence:core.get(id).confidence};
    mesh.userData.restPositions=Float32Array.from(geometry.attributes.position.array);
    mesh.userData.groundHeights=Float32Array.from(Array.from({length:vertices.length/3},(_,i)=>vertices[i*3+1]));
    group.add(mesh);meshes.push(mesh);
  }
  const bindings=new Map();
  for(const m of meshes){const id=m.userData.cityObject.objectId;if(!bindings.has(id))bindings.set(id,[]);bindings.get(id).push(m);}
  const footprints=new Map();
  for(const [id,parts] of bindings){
    const bounds=new THREE.Box3();for(const mesh of parts)bounds.expandByObject(mesh);
    footprints.set(id,{polygon:[{x:bounds.min.x,z:bounds.min.z},{x:bounds.max.x,z:bounds.min.z},{x:bounds.max.x,z:bounds.max.z},{x:bounds.min.x,z:bounds.max.z}]});
    const edge=spatial.edges.find(e=>id===`j3k:object:royal-road:${e.id}`),gate=spatial.gates.find(g=>id===`j3k:object:royal-gate:${g.id}`);
    const topology=edge?{from:edge.from,to:edge.to,points:edge.points.map(([x,z])=>({x:anchor.x+x,z:anchor.z+z}))}:gate?{gateId:gate.id,wallId:gate.wall,center:{x:anchor.x+gate.offset[0],z:anchor.z+gate.offset[1]}}:null;
    const record=core.get(id);core.register({...record,geometry:{status:'inferred-component-assembly',frame:'canonical-dem-enu',primitive:'component-assembly',authority:'literary-and-illustrative-royal-city',bounds:{min:bounds.min.toArray(),max:bounds.max.toArray()}},metadata:{...record.metadata,rendererBinding:'royal-city-adapter-v1',componentIds:parts.map(m=>m.userData.cityObject.componentId),geometryVerified:false,spatialTopology:topology}});
  }
  for(const region of spatial.regions){
    const id=`j3k:object:royal-region:${region.id}`,record=core.get(id);if(!record)throw new Error(`Missing region ledger ${id}`);
    core.register({...record,geometry:{status:'inferred-region-envelope',frame:'canonical-dem-enu',primitive:'polygon',polygon:region.polygon.map(([x,z])=>({x:anchor.x+x,z:anchor.z+z}))},metadata:{...record.metadata,rendererBinding:'royal-spatial-layout-v1',geometryVerified:false,regionId:region.id}});
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
    diagnostics(){return {stage,position:currentPosition,spatialAuthority:spatial.authority,spatialRegions:spatial.regions.map(r=>r.id),reachableDestinations:spatial.reachable(stage),visibleGates:meshes.filter(m=>m.visible&&m.userData.cityObject.kind==='city-gate').length,visibleRoads:meshes.filter(m=>m.visible&&m.userData.cityObject.kind==='city-road').length,visibleWalls:meshes.filter(m=>m.visible&&m.userData.cityObject.kind==='city-wall').length,visibleTemple:meshes.filter(m=>m.visible&&m.userData.cityObject.kind==='first-temple').length,visiblePalace:meshes.filter(m=>m.visible&&m.userData.cityObject.kind==='royal-palace').length,templeState:stateAt('j3k:object:first-temple',currentPosition),templeCompressionFactor:bindings.get('j3k:object:first-temple')[0].userData.factor,bindingIds:[...bindings.keys()],componentIdentity:meshes.map(m=>m.userData.cityObject.componentId).join('|'),wallCircuitVerified:false,palaceGeometryVerified:false,templeDimensionsMetres:[l,w,h],geometryReuseVerified:false,ruinAuthority:'schematic-vertex-compression-not-excavated-collapse'};},
    dispose(){meshes.forEach(m=>m.geometry.dispose());[stone,templeStone,roof,doorway,pathMaterial].forEach(m=>m.dispose());group.removeFromParent();}
  };
}
