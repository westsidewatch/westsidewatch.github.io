import * as THREE from 'three';

function groundAt(terrain,x,z){const y=terrain?.heightAtWorld?.(x,z);return Number.isFinite(y)?y:0}
function register(group,meshes,mesh,stage,start,groundY,height){mesh.castShadow=true;mesh.receiveShadow=true;mesh.userData.phase2={stage,start,baseHeight:height,groundY};group.add(mesh);meshes.push(mesh);return mesh}

export function polygonMass(group,meshes,material,terrain,points,height,stage,start,{lift=0,rotation=0}={}){
 const shape=new THREE.Shape();
 points.forEach(([x,z],i)=>i?shape.lineTo(x,z):shape.moveTo(x,z));shape.closePath();
 const geometry=new THREE.ExtrudeGeometry(shape,{depth:height,bevelEnabled:false,steps:1});
 geometry.rotateX(-Math.PI/2);
 const mesh=new THREE.Mesh(geometry,material);
 const cx=points.reduce((s,p)=>s+p[0],0)/points.length,cz=points.reduce((s,p)=>s+p[1],0)/points.length;
 const ground=groundAt(terrain,cx,cz)+lift;mesh.position.y=ground+1.5;mesh.rotation.y=rotation;
 return register(group,meshes,mesh,stage,start,ground,height);
}

export function irregularHouse(group,meshes,material,terrain,x,z,w,d,h,stage,start,{lift=0,variant=0}={}){
 const n=(variant%5)*.035;
 const pts=variant%3===0?[[-w*.5,-d*.5],[w*.44,-d*.5],[w*.5,d*.18],[w*.28,d*.5],[-w*.5,d*.43]]:
 variant%3===1?[[-w*.5,-d*.42],[w*.22,-d*.5],[w*.5,-d*.18],[w*.42,d*.5],[-w*.16,d*.42],[-w*.5,d*.12]]:
 [[-w*.46,-d*.5],[w*.5,-d*.38],[w*.43,d*.5],[w*.04,d*.38],[-w*.5,d*.5]];
 const shifted=pts.map(([px,pz],i)=>[x+px+(i%2?n*w:0),z+pz]);
 return polygonMass(group,meshes,material,terrain,shifted,h,stage,start,{lift});
}

export function taperedTower(group,meshes,material,terrain,x,z,radius,height,stage,start,{lift=0,sides=7}={}){
 const geometry=new THREE.CylinderGeometry(radius*.72,radius,height,sides,1,false);
 const ground=groundAt(terrain,x,z)+lift;const mesh=new THREE.Mesh(geometry,material);mesh.position.set(x,ground+height/2+1.5,z);
 return register(group,meshes,mesh,stage,start,ground,height);
}

export function ribbon(group,meshes,material,terrain,points,width,stage,start){
 const positions=[],indices=[];
 for(let i=0;i<points.length;i++){
  const p=points[i],prev=points[Math.max(0,i-1)],next=points[Math.min(points.length-1,i+1)],dx=next[0]-prev[0],dz=next[1]-prev[1],len=Math.hypot(dx,dz)||1,nx=-dz/len,nz=dx/len,y=groundAt(terrain,p[0],p[1])+(p[2]||0)+1.8;
  positions.push(p[0]+nx*width/2,y,p[1]+nz*width/2,p[0]-nx*width/2,y,p[1]-nz*width/2);
  if(i<points.length-1){const a=i*2;indices.push(a,a+2,a+1,a+1,a+2,a+3)}
 }
 const geometry=new THREE.BufferGeometry();geometry.setAttribute('position',new THREE.Float32BufferAttribute(positions,3));geometry.setIndex(indices);geometry.computeVertexNormals();
 const mesh=new THREE.Mesh(geometry,material);const avg=points.reduce((s,p)=>s+groundAt(terrain,p[0],p[1])+(p[2]||0),0)/points.length;
 mesh.userData.phase2={stage,start,baseHeight:1,groundY:avg};mesh.receiveShadow=true;group.add(mesh);meshes.push(mesh);return mesh;
}
