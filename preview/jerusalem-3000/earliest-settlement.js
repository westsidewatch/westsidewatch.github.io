import * as THREE from 'three';
import { geographicToENU } from './terrain-runtime.js';
export const EARLIEST_PHASE='chalcolithic-early-bronze';
export const isEarliestPhase=id=>id===EARLIEST_PHASE;
export const MIDDLE_BRONZE_PHASE='middle-bronze';
export const isEarlyLandscapePhase=id=>isEarliestPhase(id)||id===MIDDLE_BRONZE_PHASE;
// Sample the rendered DEM triangles, avoiding bilinear heights that can hide
// narrow footpaths beneath the triangulated terrain surface.
export function settlementSurfaceHeight(terrain,x,z) {
  const p=terrain.mesh?.geometry?.attributes?.position,g=terrain.grid;
  if(!p||!g?.width||!g?.height) return terrain.heightAtWorld(x,z);
  const u=(x-terrain.mesh.position.x-p.getX(0))/(p.getX(g.width-1)-p.getX(0))*(g.width-1);
  const v=(z-terrain.mesh.position.z-p.getZ(0))/(p.getZ((g.height-1)*g.width)-p.getZ(0))*(g.height-1);
  if(u<0||v<0||u>g.width-1||v>g.height-1) return NaN;
  const col=Math.min(g.width-2,Math.floor(u)),row=Math.min(g.height-2,Math.floor(v)),a=u-col,b=v-row,i=row*g.width+col;
  const h00=p.getY(i),h10=p.getY(i+1),h01=p.getY(i+g.width),h11=p.getY(i+g.width+1);
  return (a+b<=1?h00+a*(h10-h00)+b*(h01-h00):h11+(1-a)*(h01-h11)+(1-b)*(h10-h11))+terrain.mesh.position.y;
}
export function createLandscapeSettlement(parent,{data,terrain}) {
  if(!terrain?.grid?.origin||!isEarlyLandscapePhase(data.phase)) throw new Error('Earliest settlement requires canonical DEM and its own phase data');
  const anchor=geographicToENU(data.spring.lat,data.spring.lon,terrain.grid.origin);
  const spring={x:anchor.east,z:-anchor.north};
  const group=new THREE.Group(); group.name=`${data.phase}-ridge-settlement`; group.visible=false; parent.add(group);
  const stone=new THREE.MeshStandardMaterial({color:0xc4ae87,roughness:1});
  const timber=new THREE.MeshStandardMaterial({color:0x655743,roughness:1});
  const earth=new THREE.MeshStandardMaterial({color:0x9f8762,roughness:1});
  const pathMaterial=new THREE.MeshStandardMaterial({color:0x7d6c53,roughness:1});
  const surface=(x,z)=>settlementSurfaceHeight(terrain,x,z);
  const water=new THREE.MeshStandardMaterial({color:0x537c83,roughness:.7});
  const disputedStone=new THREE.MeshStandardMaterial({color:0x986e5c,roughness:1});
  const meshes=[],houseIds=[];
  const namespace=data.phase===EARLIEST_PHASE?'earliest':data.phase;
  function add(geometry,material,x,y,z,id,kind,confidence='inferred') {
    const mesh=new THREE.Mesh(geometry,material);mesh.position.set(x,y,z);
    mesh.receiveShadow=true;mesh.castShadow=true;
    mesh.userData.cityObject={objectId:id,kind,confidence,phaseIds:[data.phase]};
    group.add(mesh);meshes.push(mesh);return mesh;
  }
  for(const [i,[dx,dz]] of data.houseOffsets.entries()) {
    const x=spring.x+dx,z=spring.z+dz,w=5+(i%3)*.6,d=6+(i%2)*.8,h=2.3+(i%3)*.15;
    const samples=[[-w/2,-d/2],[w/2,-d/2],[-w/2,d/2],[w/2,d/2]].map(([a,b])=>surface(x+a,z+b));
    if(samples.some(v=>!Number.isFinite(v))) throw new Error('Settlement outside canonical terrain');
    const ground=Math.max(...samples)+.08,id=`j3k:${namespace}:house:${i+1}`;houseIds.push(id);
    // Low single-room illustrative dwellings: stone footing, mud walls and timber roof.
    const footing=new THREE.BoxGeometry(w,1,d),fp=footing.attributes.position;
    for(let j=0;j<fp.count;j++) fp.setY(j,fp.getY(j)>0?.2:surface(x+fp.getX(j),z+fp.getZ(j))-ground);
    footing.computeVertexNormals();
    add(footing,stone,x,ground,z,id,'footing');
    add(new THREE.BoxGeometry(w,h,.4),stone,x,ground+h/2+.2,z-d/2,id,'wall');
    for(const side of [-1,1]) add(new THREE.BoxGeometry(.4,h,d),stone,x+side*w/2,ground+h/2+.2,z,id,'wall');
    for(const side of [-1,1]) add(new THREE.BoxGeometry((w-1)/2,h,.4),stone,x+side*(w+1)/4,ground+h/2+.2,z+d/2,id,'door-wall');
    add(new THREE.BoxGeometry(w+.4,.18,d+.4),earth,x,ground+h+.3,z,id,'earthen-roof');
    for(let j=0;j<4;j++) add(new THREE.CylinderGeometry(.08,.08,d+.3,6),timber,x+(j-1.5)*w/4,ground+h+.17,z,id,'roof-beam').rotation.x=Math.PI/2;
  }
  const points=data.pathOffsets.map(([dx,dz])=>({x:spring.x+dx,z:spring.z+dz}));
  for(let i=1;i<points.length;i++) {
    const a=points[i-1],b=points[i],length=Math.hypot(b.x-a.x,b.z-a.z),nx=-(b.z-a.z)/length*.45,nz=(b.x-a.x)/length*.45;
    const vertices=[];
    for(let j=0;j<Math.ceil(length/2);j++) {
      const t=j/Math.ceil(length/2),u=(j+1)/Math.ceil(length/2);
      for(const [v,side] of [[t,1],[u,1],[t,-1],[u,1],[u,-1],[t,-1]]) {
        const x=a.x+(b.x-a.x)*v+nx*side,z=a.z+(b.z-a.z)*v+nz*side;
        vertices.push(x,surface(x,z)+.09,z);
      }
    }
    const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(vertices,3));g.computeVertexNormals();
    add(g,pathMaterial,0,0,0,`j3k:${namespace}:path:${i}`,'inferred-footpath');
  }
  add(new THREE.CylinderGeometry(1.5,1.5,.08,24),water,spring.x,surface(spring.x,spring.z)+.12,spring.z,`j3k:${namespace}:spring-marker`,'approximate-spring-location');
  if(data.defense) {
    let blockIndex=0;
    function wall(a,b,width,height,kind,confidence) {
      const dx=b[0]-a[0],dz=b[1]-a[1],length=Math.hypot(dx,dz),count=Math.ceil(length/2.4),angle=-Math.atan2(dz,dx);
      for(let i=0;i<count;i++) {
        const x=spring.x+a[0]+dx*(i+.5)/count,z=spring.z+a[1]+dz*(i+.5)/count;
        const span=length/count*.97,cs=Math.cos(angle),sn=Math.sin(angle);
        const corners=[[-span/2,-width/2],[span/2,-width/2],[-span/2,width/2],[span/2,width/2]];
        const ground=Math.max(...corners.map(([a,b])=>surface(x+cs*a+sn*b,z-sn*a+cs*b))),rows=Math.ceil(height/1.1),course=height/rows;
        const footing=new THREE.BoxGeometry(span,1,width),fp=footing.attributes.position;
        for(let j=0;j<fp.count;j++)fp.setY(j,fp.getY(j)>0?0:surface(x+cs*fp.getX(j)+sn*fp.getZ(j),z-sn*fp.getX(j)+cs*fp.getZ(j))-ground);
        footing.computeVertexNormals();
        add(footing,confidence==='disputed'?disputedStone:stone,x,ground,z,`j3k:${namespace}:defense:${blockIndex++}`,kind,confidence).rotation.y=angle;
        for(let row=0;row<rows;row++) {
          const mesh=add(new THREE.BoxGeometry(length/count*.97,course*.95,width),confidence==='disputed'?disputedStone:stone,
            x,ground+(row+.5)*course,z,`j3k:${namespace}:defense:${blockIndex++}`,kind,confidence);
          mesh.rotation.y=angle;
        }
      }
    }
    const t=data.defense.tower,half=t.outerSize/2,c=half-t.wallWidth/2;
    wall([-half,-c],[half,-c],t.wallWidth,t.height,'spring-tower',t.confidence);
    wall([-half,c],[half,c],t.wallWidth,t.height,'spring-tower',t.confidence);
    wall([c,-half+t.wallWidth],[c,half-t.wallWidth],t.wallWidth,t.height,'spring-tower',t.confidence);
    wall([-c,-half+t.wallWidth],[-c,-.8],t.wallWidth,t.height,'spring-tower',t.confidence);
    wall([-c,.8],[-c,half-t.wallWidth],t.wallWidth,t.height,'spring-tower',t.confidence);
    const corridor=data.defense.corridor;
    for(const [a,b] of corridor.lines)wall(a,b,corridor.wallWidth,corridor.height,'protected-access',corridor.confidence);
    const pit=data.defense.carvedInstallation,[x,z]=pit.offset,w=pit.width/2,d=pit.depth/2;
    for(const [a,b] of [[[x-w,z-d],[x+w,z-d]],[[x+w,z-d],[x+w,z+d]],[[x+w,z+d],[x-w,z+d]],[[x-w,z+d],[x-w,z-d]]])wall(a,b,.5,.25,'carved-installation-outline',pit.confidence);
  }
  const focus=new THREE.Vector3(spring.x-78,surface(spring.x-78,spring.z)+5,spring.z);
  let phase='',visibleHouses=0;
  return {
    focus,
    apply({phaseId,evidenceAllowed}) {phase=phaseId;group.visible=phaseId===data.phase;for(const m of meshes)m.visible=group.visible&&evidenceAllowed(m.userData.cityObject.confidence);visibleHouses=group.visible&&evidenceAllowed('inferred')?houseIds.length:0;},
    diagnostics(){return {phase,houses:houseIds.length,visibleHouses,components:meshes.length,identityFingerprint:houseIds.join('|'),spring,source:data.historicalSource,historicalFootprintsVerified:false,modernTerrain:true,visibleDefenseComponents:meshes.filter(m=>m.visible&&['spring-tower','protected-access','carved-installation-outline'].includes(m.userData.cityObject.kind)).length,visibleTowerComponents:meshes.filter(m=>m.visible&&m.userData.cityObject.kind==='spring-tower').length,towerDatingDisputed:Boolean(data.defense),terrainSampling:'rendered-dem-triangles'};},
    dispose(){meshes.forEach(m=>m.geometry.dispose());[stone,timber,earth,water,pathMaterial,disputedStone].forEach(m=>m.dispose());group.removeFromParent();}
  };
}

export const createEarliestSettlement=createLandscapeSettlement;
