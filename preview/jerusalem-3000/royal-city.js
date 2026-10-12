import * as THREE from 'three';
import {geographicToENU} from './terrain-runtime.js';
import {settlementSurfaceHeight} from './earliest-settlement.js';
// Literary/interpretive reconstruction. No excavated wall circuit is asserted.
export function createRoyalCity(parent,{data,terrain}) {
  const origin=geographicToENU(data.spring.lat,data.spring.lon,terrain.grid.origin);
  const anchor={x:origin.east,z:-origin.north};
  const group=new THREE.Group();group.name='royal-city-reconstruction';group.visible=false;parent.add(group);
  const stone=new THREE.MeshStandardMaterial({color:0xb99c72,roughness:1});
  const templeStone=new THREE.MeshStandardMaterial({color:0xd8c6a1,roughness:.9});
  const roof=new THREE.MeshStandardMaterial({color:0x806549,roughness:1});
  const doorway=new THREE.MeshStandardMaterial({color:0x3e3327,roughness:1});
  const meshes=[];
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
    mesh.userData.cityObject={objectId:`j3k:royal:${id}`,kind,confidence:'inferred',stage,footprintVerified:false};
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
  let stage='david';
  return {
    focus:new THREE.Vector3(anchor.x-110,surface(-110,-210)+5,anchor.z-210),
    templeFocus:new THREE.Vector3(anchor.x+x,surface(x,z)+5,anchor.z+z),
    apply({phaseId,progress=0,evidenceAllowed}) {
      stage=progress>=.45?'solomon':'david';group.visible=phaseId==='david-solomon';
      for(const m of meshes)m.visible=group.visible&&evidenceAllowed('inferred')&&(m.userData.cityObject.stage==='david'||stage==='solomon');
    },
    diagnostics(){return {stage,visibleWalls:meshes.filter(m=>m.visible&&m.userData.cityObject.kind==='city-wall').length,visibleTemple:meshes.filter(m=>m.visible&&m.userData.cityObject.kind==='first-temple').length,visiblePalace:meshes.filter(m=>m.visible&&m.userData.cityObject.kind==='royal-palace').length,wallCircuitVerified:false,palaceGeometryVerified:false,templeSource:'1 Kings 6:2–3',cubitMetres:c,templeDimensionsMetres:[l,w,h],placementVerified:false,substageTiming:'illustrative-not-calendar-dates'};},
    dispose(){meshes.forEach(m=>m.geometry.dispose());[stone,templeStone,roof,doorway].forEach(m=>m.dispose());group.removeFromParent();}
  };
}
