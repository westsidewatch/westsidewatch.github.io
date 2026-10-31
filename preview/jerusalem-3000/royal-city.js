import {buildRoyalPrecinctHalls} from './royal-precinct-halls.js';
import {firstTempleOuterCourt} from './temple-context-layout.js';
import {sanctuaryAccessVertices} from './sanctuary-access-geometry.js';
import {firstTempleCourt,courtEnvelopeDatum} from './temple-court-envelopes.js';
import {firstTempleWaterLayout} from './temple-precinct-layout.js';
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
  const bronze=new THREE.MeshStandardMaterial({color:0x8c6a42,metalness:.45,roughness:.6});
  const doorway=new THREE.MeshStandardMaterial({color:0x3e3327,roughness:1});
  if(!core)throw new Error('Royal geometry requires the shared object ledger');
  const timeline={phases:[...core.phases.values()]};
  const spatial=compileRoyalSpatialLayout(data);
  const pathMaterial=new THREE.MeshStandardMaterial({color:0x7d6c53,roughness:1});
  const meshes=[];
  const ledgerId=(kind,stage)=>'j3k:object:'+(kind==='first-temple'?'first-temple':kind==='city-wall'?(stage==='david'?'royal-city-wall-hypothesis':'solomon-northern-wall-hypothesis'):(stage==='david'?'david-royal-courtyard-hypothesis':'solomon-royal-courtyard-hypothesis'));

  const surface=(x,z)=>settlementSurfaceHeight(terrain,anchor.x+x,anchor.z+z);
  function box(id,kind,x,z,w,d,h,stage='david',material=stone,angle=0,lift=0,objectIdOverride=null,levelGround=null,shapeGeometry=null) {
    const cs=Math.cos(angle),sn=Math.sin(angle);
    const corners=[[-w/2,-d/2],[w/2,-d/2],[-w/2,d/2],[w/2,d/2]];
    const topGround=levelGround??Math.max(...corners.map(([a,b])=>surface(x+cs*a+sn*b,z-sn*a+cs*b)));
    if(!Number.isFinite(topGround))throw new Error('Royal city outside DEM');
    const geometry=shapeGeometry??new THREE.BoxGeometry(w,h,d),p=geometry.attributes.position;
    for(let i=0;i<p.count;i++)if(lift===0&&p.getY(i)<0)p.setY(i,surface(x+cs*p.getX(i)+sn*p.getZ(i),z-sn*p.getX(i)+cs*p.getZ(i))-topGround-h/2);
    geometry.computeVertexNormals();
    const mesh=new THREE.Mesh(geometry,material);mesh.position.set(anchor.x+x,topGround+h/2+lift,anchor.z+z);mesh.rotation.y=angle;
    mesh.castShadow=true;mesh.receiveShadow=true;
    const objectId=objectIdOverride||ledgerId(kind,stage);if(!core.get(objectId))throw new Error(`Missing royal ledger object ${objectId}`);
    mesh.userData.cityObject={objectId,componentId:`j3k:royal:${id}`,kind,confidence:core.get(objectId).confidence,stage,footprintVerified:false};
    if(kind==='first-temple')mesh.userData.templeSectionHeight=templeGround+4;
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
  buildRoyalPrecinctHalls(data,{
    stone:templeStone,timber:roof,datum:bounds=>courtEnvelopeDatum(bounds,anchor,terrain),
    emit:(id,x,z,w,d,h,material,lift,ground)=>{
      let geometry=null;
      if(id.endsWith('-floor')){const points=w>d?[[x-w/2,z],[x+w/2,z]]:[[x,z-d/2],[x,z+d/2]],vertices=sanctuaryAccessVertices(points,Math.min(w,d),surface,()=>ground+h);for(let i=0;i<vertices.length;i+=3){vertices[i]-=x;vertices[i+1]-=ground+h/2;vertices[i+2]-=z;}geometry=new THREE.BufferGeometry();geometry.setAttribute('position',new THREE.Float32BufferAttribute(vertices,3));}
      return box(id,'royal-palace',x,z,w,d,h,'solomon',material,0,lift,null,ground,geometry);
    }
  });
  const t=data.royalCity.temple,c=t.cubitMetres,l=t.lengthCubits*c,w=t.widthCubits*c,h=t.heightCubits*c,[x,z]=t.offset;
  // One display datum for the ensemble; footing bottoms still meet the DEM.
  const court=firstTempleCourt(data,spatial),templeGround=courtEnvelopeDatum(court.bounds,anchor,terrain);
  const templeBox=(id,px,pz,pw,pd,ph,material=templeStone,lift=0,angle=0)=>box(id,'first-temple',px,pz,pw,pd,ph,'solomon',material,angle,lift,null,templeGround);
  // Keep the inherited outside envelope; wall thickness and door widths are
  // display choices, so the nominal40/20-cubit internal budget is not a survey.
  const wall=.3;
  const [courtWest,courtNorth,courtEast,courtSouth]=court.bounds;
  const courtFloor=templeBox('temple-court-floor',(courtWest+courtEast)/2,(courtNorth+courtSouth)/2,courtEast-courtWest,courtSouth-courtNorth,.06);courtFloor.userData.cityObject.role='walkable-floor';
  const courtWall=(id,px,pz,pw,pd)=>{
    for(let course=0;course<3;course++)templeBox(`${id}-stone-${course}`,px,pz,pw,pd,court.stoneCourseHeight,templeStone,course*court.stoneCourseHeight);
    templeBox(`${id}-cedar`,px,pz,pw,pd,court.timberHeight,roof,3*court.stoneCourseHeight);
  };
  for(const px of[courtWest,courtEast])courtWall(`temple-court-wall-${px}`,px,(courtNorth+courtSouth)/2,court.wallThickness,courtSouth-courtNorth);
  courtWall('temple-court-north',(courtWest+courtEast)/2,courtNorth,courtEast-courtWest,court.wallThickness);
  for(const [a,b]of[[courtWest,court.gateX-court.gateWidth/2],[court.gateX+court.gateWidth/2,courtEast]])courtWall(`temple-court-south-${a}`,(a+b)/2,courtSouth,b-a,court.wallThickness);
  // An outer context boundary makes the reserved land legible without filling a court.
  // Route-derived gaps preserve every registered crossing, including the north gate.
  for(const seg of firstTempleOuterCourt(data,spatial)){
    const length=seg.end-seg.start,mid=(seg.start+seg.end)/2,px=seg.axis==='x'?mid:seg.fixed,pz=seg.axis==='x'?seg.fixed:mid,pw=seg.axis==='x'?length:.5,pd=seg.axis==='x'?.5:length;
    for(let course=0;course<4;course++){
      const height=course===3?.2:.35,lift=course===3?1.05:course*.35;
      const mesh=box(`temple-${seg.id}-${course}`,'first-temple',px,pz,pw,pd,height,'solomon',course===3?roof:templeStone,0,lift);
      delete mesh.userData.templeSectionHeight;
    }
  }
  templeBox('temple-main',x,z,l,w,wall,templeStone,h-wall);
  templeBox('temple-interior-floor',x,z,l,w,.12);
  // 1Kings6:4 supports high windows, not their count/profile or measured sill.
  // Six authored openings per side sit above the three low chamber tiers.
  const sill=9,windowH=1.5,windowW=1.1,pitch=(l-2*wall)/6;
  for(const side of[-1,1]){
    const zz=z+side*(w-wall)/2;
    templeBox(`temple-main-side-${side}`,x,zz,l,wall,sill);
    templeBox(`temple-window-head-${side}`,x,zz,l,wall,h-wall-sill-windowH,templeStone,sill+windowH);
    for(let i=0;i<=6;i++){
      const left=i===0?x-l/2:x-l/2+wall+(i-.5)*pitch+windowW/2;
      const right=i===6?x+l/2:x-l/2+wall+(i+.5)*pitch-windowW/2;
      templeBox(`temple-window-pier-${side}-${i}`,(left+right)/2,zz,right-left,wall,windowH,templeStone,sill);
    }
  }
  templeBox('temple-main-west',x-(l-wall)/2,z,wall,w,h-wall);
  const clearDoor=2.6;
  for(const side of[-1,1])templeBox(`temple-main-entry-jamb-${side}`,x+(l-wall)/2,z+side*(clearDoor/2+(w-clearDoor)/4),wall,(w-clearDoor)/2,h-wall);
  templeBox('temple-main-entry-lintel',x+(l-wall)/2,z,wall,clearDoor,h-wall-4.5,templeStone,4.5);
  const partitionX=x-l/2+20*c,innerDoor=2;
  for(const side of[-1,1])templeBox(`temple-inner-partition-${side}`,partitionX,z+side*(innerDoor/2+(w-innerDoor)/4),wall,(w-innerDoor)/2,h-wall);
  templeBox('temple-inner-lintel',partitionX,z,wall,innerDoor,h-wall-4.5,templeStone,4.5);
  // Existing illustrative doorway width/porch height are not textual measures.
  const opening=2.6,porchHeight=9,porchDepth=10*c,porchX=x+l/2+porchDepth/2;
  for(const side of [-1,1])templeBox(`temple-porch-jamb-${side}`,porchX,z+side*(opening/2+(w-opening)/4),porchDepth,(w-opening)/2,porchHeight);
  templeBox('temple-porch-lintel',porchX,z,porchDepth,opening,porchHeight-4.5,templeStone,4.5);
  // Door aperture is physical; no opaque dark panel substitutes for the interior.
  for(const side of[-1,1])templeBox(`temple-open-door-${side}`,x+l/2-wall-clearDoor/4,z+side*(clearDoor/2-.06),clearDoor/2,.12,4.38,doorway,.12);
  // 1Kings6:6,10: three five-cubit-high side-room tiers, widths5/6/7 cubits.
  // Hollow side-storey envelopes within the inherited outside5/6/7cubit widths.
  // Wall/slab thickness and south entrance position are authored, not clear textual widths.
  const chamberWall=.18,chamberSlab=.15,chamberLength=l-2;
  for(let tier=0;tier<3;tier++)for(const side of[-1,1]){
    const depth=(5+tier)*c,cx=x-1,cz=z+side*(w/2+depth/2),bottom=tier*5*c,height=5*c,prefix=`temple-side-${side}-tier-${tier+1}`;
    templeBox(prefix,cx,cz,chamberLength,depth,chamberSlab,stone,bottom);
    templeBox(prefix+'-roof',cx,cz,chamberLength,depth,chamberSlab,stone,bottom+height-chamberSlab);
    for(const end of[-1,1])templeBox(prefix+`-end-${end}`,cx+end*(chamberLength-chamberWall)/2,cz,chamberWall,depth,height-2*chamberSlab,stone,bottom+chamberSlab);
    const wallZ=cz+side*(depth-chamberWall)/2;
    if(tier===0&&side===1){
      const door=1,doorH=1.7,doorX=cx+chamberLength/2-2;
      for(const [left,right]of[[cx-chamberLength/2,doorX-door/2],[doorX+door/2,cx+chamberLength/2]])templeBox(prefix+`-outer-${left}`,(left+right)/2,wallZ,right-left,chamberWall,height-2*chamberSlab,stone,bottom+chamberSlab);
      templeBox(prefix+'-lintel',doorX,wallZ,door,chamberWall,height-chamberSlab-doorH,stone,bottom+doorH);
    }else templeBox(prefix+'-outer',cx,wallZ,chamberLength,chamberWall,height-2*chamberSlab,stone,bottom+chamberSlab);
  }
  for(let tier=0;tier<3;tier++){
    const depth=(5+tier)*c;
    templeBox(`temple-west-tier-${tier+1}`,x-l/2-depth/2,z,depth,w+2*depth,5*c,stone,tier*5*c);
  }
  const pillar=t.pillars,shaftH=pillar.heightCubits*c,capH=pillar.capitalHeightCubits*c,radius=pillar.circumferenceCubits*c/(2*Math.PI);
  for(const side of[-1,1]){
    const px=x+l/2+10*c+1.5,pz=z+side*3;
    box(`temple-pillar-${side}`,'first-temple',px,pz,radius*2,radius*2,shaftH,'solomon',bronze,0,.06,null,templeGround,new THREE.CylinderGeometry(radius,radius,shaftH,20));
    const profile=[[radius,-capH/2],[radius*.9,-capH*.3],[radius*1.3,capH*.3],[radius*1.4,capH/2]].map(([r,y])=>new THREE.Vector2(r,y));
    box(`temple-pillar-cap-${side}`,'first-temple',px,pz,radius*2.8,radius*2.8,capH,'solomon',bronze,0,shaftH+.06,null,templeGround,new THREE.LatheGeometry(profile,20));
  }
  const altar=t.altar,al=altar.lengthCubits*c,ad=altar.widthCubits*c,ah=altar.heightCubits*c,altarX=x+l/2+16;
  templeBox('temple-altar',altarX,z,al,ad,ah*.2,bronze);
  templeBox('temple-altar-body',altarX,z,al*.9,ad*.9,ah*.6,bronze,ah*.2);
  templeBox('temple-altar-rim',altarX,z,al,ad,ah*.1,bronze,ah*.8);
  for(const sx of[-1,1])for(const sz of[-1,1])templeBox(`temple-altar-horn-${sx}-${sz}`,altarX+sx*(al/2-c/2),z+sz*(ad/2-c/2),c,c,ah*.1,bronze,ah*.9);
  // 1Kings7 sea and ten mobile basin stands; relative placement is schematic.
  const water=firstTempleWaterLayout(c),seaX=x+l/2+water.sea.eastFromBodyEnd,seaZ=z+water.sea.southFromAxis;
  const basin=(id,bx,bz,diameter,height,lift)=>{
    const radius=diameter/2,thickness=.12;
    const profile=[[0,-height/2],[radius,-height/2],[radius,height/2],[radius-thickness,height/2],[radius-thickness,-height/2+thickness],[0,-height/2+thickness]].map(([r,y])=>new THREE.Vector2(r,y));
    const geometry=new THREE.LatheGeometry(profile,16);
    box(id,'first-temple',bx,bz,diameter,diameter,height,'solomon',roof,0,lift,null,templeGround,geometry);
  };
  templeBox('temple-sea-pedestal',seaX,seaZ,2,2,.6,stone);
  basin('temple-sea',seaX,seaZ,water.sea.diameter,water.sea.height,.6);
  for(const side of[-1,1])for(const [i,dx]of water.stands.eastOffsets.entries()){
    const bx=x+dx,bz=z+side*water.stands.sideOffset;
    templeBox(`temple-laver-stand-${side}-${i}`,bx,bz,water.stands.size,water.stands.size,water.stands.height,roof);
    // Basin depth/diameter are display choices; the stand dimensions are textual.
    basin(`temple-laver-${side}-${i}`,bx,bz,water.stands.size,.45,water.stands.height);
  }
  for(const gate of spatial.gates){
    const [gx,gz]=gate.offset,id=`j3k:object:royal-gate:${gate.id}`;
    for(const side of [-1,1])box(`gate-${gate.id}-post-${side}`,'city-gate',gx+gate.unit[0]*side*(gate.width/2+.5),gz+gate.unit[1]*side*(gate.width/2+.5),1,2.5,4,gate.stage,stone,gate.angle,0,id);
    box(`gate-${gate.id}-lintel`,'city-gate',gx,gz,gate.width+2,2.5,1,gate.stage,stone,gate.angle,4,id);
  }
  for(const edge of spatial.edges){
    const localVertices=sanctuaryAccessVertices(edge.points,spatial.roadWidth,surface,(px,pz)=>{
      const ground=surface(px,pz)+.09;
      if(edge.id!=='temple-entry')return ground;
      const f=Math.max(0,Math.min(1,(courtSouth+5-pz)/5));
      return ground+f*Math.max(0,templeGround+.09-ground);
    },{terrain,anchor});
    const vertices=localVertices.map((value,i)=>i%3===0?value+anchor.x:i%3===2?value+anchor.z:value);
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
    const clusters=new Map();for(const mesh of parts){const key=mesh.userData.cityObject.reservationCluster||id;if(!clusters.has(key))clusters.set(key,new THREE.Box3());clusters.get(key).expandByObject(mesh);}
    for(const [key,b]of clusters)footprints.set(key,{objectId:id,polygon:[{x:b.min.x,z:b.min.z},{x:b.max.x,z:b.min.z},{x:b.max.x,z:b.max.z},{x:b.min.x,z:b.max.z}]});
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
    ritualFocus:new THREE.Vector3(anchor.x+altarX,templeGround+2,anchor.z+z),
    precinctFocus:new THREE.Vector3(anchor.x-102.5,surface(-102.5,-462.5)+4,anchor.z-462.5),precinctSpan:135,
    templeFocus:new THREE.Vector3(anchor.x+x,surface(x,z)+5,anchor.z+z),
    exclusionsFor(phaseId){
      if(!['late-first-temple','babylonian-destruction'].includes(phaseId))return [];
      const position=timeline.phases.findIndex(p=>p.id===phaseId)+.5;
      return [...footprints].filter(([,zone])=>['first-temple','royal-palace'].includes(bindings.get(zone.objectId)[0].userData.cityObject.kind)&&['build','transform','ruin'].includes(stateAt(zone.objectId,position))).map(([id,zone])=>({...zone,id,authority:'inferred-royal-footprint-exclusion-not-survey'}));
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
    dispose(){meshes.forEach(m=>m.geometry.dispose());[stone,templeStone,roof,bronze,doorway,pathMaterial].forEach(m=>m.dispose());group.removeFromParent();}
  };
}
