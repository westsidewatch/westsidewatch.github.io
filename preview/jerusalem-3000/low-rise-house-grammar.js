import * as THREE from 'three';
import {settlementSurfaceHeight} from './earliest-settlement.js';
// Period-specific illustrative housing. Parcel placement is not an excavation plan.
export function buildLowRiseHouse(group,meshes,materials,terrain,parcel,index,profile){
 if(!Number.isFinite(profile.wallHeightMetres)||profile.wallHeightMetres<2.2||profile.wallHeightMetres>4.6)throw new Error('Invalid low-rise wall height');
 if(!['iron-age-four-room-analogy','persian-courtyard-analogy'].includes(profile.id))throw new Error('Unknown low-rise profile');
 const fp=parcel.geometry.polygon;if(fp.length!==4)throw new Error('Low-rise house requires a four-sided parcel');
 const before=meshes.length,centre={x:fp.reduce((s,p)=>s+p.x,0)/4,z:fp.reduce((s,p)=>s+p.z,0)/4};
 const points=fp.map(p=>({x:centre.x+(p.x-centre.x)*.89,z:centre.z+(p.z-centre.z)*.89}));
 const width=Math.hypot(points[1].x-points[0].x,points[1].z-points[0].z),depth=Math.hypot(points[3].x-points[0].x,points[3].z-points[0].z);
 const point=(u,v)=>({x:points[0].x*(1-u)*(1-v)+points[1].x*u*(1-v)+points[2].x*u*v+points[3].x*(1-u)*v,z:points[0].z*(1-u)*(1-v)+points[1].z*u*(1-v)+points[2].z*u*v+points[3].z*(1-u)*v});
 const surface=(x,z)=>{const y=settlementSurfaceHeight(terrain,x,z);if(!Number.isFinite(y))throw new Error('Low-rise house outside terrain');return y;};
 const ground=Math.min(...points.map(p=>surface(p.x,p.z))),houseGround=Math.max(...points.map(p=>surface(p.x,p.z))),h=profile.wallHeightMetres+(index%3)*.2,t=Math.min(.13,.5/Math.max(1,Math.min(width,depth))),door=Math.min(.22,1.1/Math.max(1,width));
 function add(poly,height,kind,offset=0){
  const c={x:poly.reduce((s,p)=>s+p.x,0)/poly.length,z:poly.reduce((s,p)=>s+p.z,0)/poly.length},shape=new THREE.Shape();poly.forEach((p,i)=>i?shape.lineTo(p.x-c.x,-(p.z-c.z)):shape.moveTo(p.x-c.x,-(p.z-c.z)));shape.closePath();
  const geometry=new THREE.ExtrudeGeometry(shape,{depth:height,bevelEnabled:false,steps:1});geometry.rotateX(-Math.PI/2);
  const topGround=houseGround,positions=geometry.attributes.position;
  // Sloping footings meet the same rendered DEM; upper components retain clear headroom.
  if(offset===0)for(let i=0;i<positions.count;i++)if(positions.getY(i)<1e-5)positions.setY(i,surface(c.x+positions.getX(i),c.z+positions.getZ(i))-topGround);
  geometry.computeVertexNormals();const mesh=new THREE.Mesh(geometry,materials.lowRise||materials.inferred||materials.reconstructed);mesh.position.set(c.x,topGround+offset,c.z);mesh.castShadow=true;mesh.receiveShadow=true;
  mesh.userData.restPositions=Float32Array.from(positions.array);mesh.userData.groundHeights=Float32Array.from(Array.from({length:positions.count},(_,i)=>surface(c.x+positions.getX(i),c.z+positions.getZ(i))-mesh.position.y));mesh.userData.cityRuinFactor=1;
  mesh.userData.phase2={stage:kind,start:.25,baseHeight:height,groundY:ground};mesh.userData.cityObject={parcelId:parcel.id,terrainGround:ground,kind,confidence:'inferred',semantic:true,architectureProfile:profile.id};group.add(mesh);meshes.push(mesh);
 }
 const rect=(u0,v0,u1,v1,height,kind,offset=0)=>add([point(u0,v0),point(u1,v0),point(u1,v1),point(u0,v1)],height,kind,offset);
 rect(0,0,t,1,h,'low-rise-side-wall');rect(1-t,0,1,1,h,'low-rise-side-wall');rect(t,1-t,1-t,1,h,'low-rise-rear-wall');
 rect(t,0,.5-door/2,t,h,'low-rise-entry-jamb');rect(.5+door/2,0,1-t,t,h,'low-rise-entry-jamb');rect(.5-door/2,0,.5+door/2,t,h-2.1,'low-rise-entry-lintel',2.1);
 if(profile.id==='iron-age-four-room-analogy'){
  // Three longitudinal spaces and a broad rear room; no claimed excavated footprint.
  const rear=.72;
  for(const u of [.3,.7]){rect(u-t/2,0,u+t/2,rear*.18,h,'four-room-partition');for(const v of [.25,.52])rect(u-.025,v-.025,u+.025,v+.025,h,'four-room-support');}
  rect(t,rear-t/2,.42,rear+t/2,h,'four-room-cross-wall');rect(.58,rear-t/2,1-t,rear+t/2,h,'four-room-cross-wall');
  rect(0,0,.3,rear,.28,'low-rise-flat-roof',h);rect(.7,0,1,rear,.28,'low-rise-flat-roof',h);rect(0,rear,1,1,.28,'low-rise-flat-roof',h);
 }else{
  // Open courtyard with two roofed ranges; form is an explicit Persian-period analogy.
  rect(0,0,.27,1,.28,'low-rise-flat-roof',h);rect(.73,0,1,1,.28,'low-rise-flat-roof',h);rect(.27,.74,.73,1,.28,'low-rise-flat-roof',h);
  rect(t,.74,.43,.74+t,h,'courtyard-rear-partition');rect(.57,.74,1-t,.74+t,h,'courtyard-rear-partition');
 }
 return{typology:profile.id,components:meshes.length-before};
}
