import * as THREE from 'three';
// Display structure inside the existing width/height budget, not a surveyed
// ancient wall section. Unknown traces and candidate bands keep their own renderer.
export function wallSection(width,height,{mode='standing'}={}){
 if(!(width>0&&height>0))throw new Error('Invalid wall section');
 const w=width/2,b=Math.min(.12,width*.04);
 if(mode==='candidate'||mode==='extent')return[[-w,-.15],[w,-.15],[w,height],[-w,height]];
 if(mode==='ruin')return[[-w,-.15],[w,-.15],[w*.9,height*.6],[0,height],[-w*.9,height*.72]];
 if(width<1.8||height<3)return[[-w,-.15],[w,-.15],[w-b,height-.18],[w-b*.5,height],[-w+b*.5,height],[-w+b,height-.18]];
 const t=Math.min(.45,Math.max(.25,width*.14)),deck=height-Math.min(.85,height*.25);
 return[[-w,-.15],[w,-.15],[w-b,deck],[w-b,height],[w-b-t,height],[w-b-t,deck],[-w+b+t,deck],[-w+b+t,height],[-w+b,height],[-w+b,deck]];
}
export function wallJoinSkew(points,index,edgeIndex){
 const n=points.length,closed=n>2&&Math.hypot(points[0].x-points[n-1].x,points[0].z-points[n-1].z)<1e-6;
 let i=index;if(closed&&i===n-1)i=0;const prev=i>0?points[i-1]:closed?points[n-2]:null,next=i<n-1?points[i+1]:null;if(!prev||!next)return 0;
 const p=points[i],a=new THREE.Vector2(p.x-prev.x,p.z-prev.z).normalize(),b=new THREE.Vector2(next.x-p.x,next.z-p.z).normalize(),normal=new THREE.Vector2(-a.y-b.y,a.x+b.x);if(normal.lengthSq()<1e-8)return 0;normal.normalize();const e=new THREE.Vector2(points[edgeIndex+1].x-points[edgeIndex].x,points[edgeIndex+1].z-points[edgeIndex].z).normalize(),side=new THREE.Vector2(-e.y,e.x),den=normal.dot(side);return Math.abs(den)<.1?0:THREE.MathUtils.clamp(normal.dot(e)/den,-1,1);
}
export function appendWallPrism(vertices,a,b,terrain,{width,height,startSkew=0,endSkew=0,mode='standing',heightFactor=1}={}){
 const L=Math.hypot(b.x-a.x,b.z-a.z);if(L<.001)return;const tx=(b.x-a.x)/L,tz=(b.z-a.z)/L,nx=-tz,nz=tx,section=wallSection(width,height,{mode});
 const rings=[a,b].map((p,end)=>section.map(([u,y])=>{const k=end?endSkew:startSkew,x=p.x+nx*u+tx*u*k,z=p.z+nz*u+tz*u*k,ground=terrain.heightAtWorld(x,z);if(!Number.isFinite(ground))throw new Error('Wall outside terrain');return[x,ground+(y<0?y:y*heightFactor),z];}));
 const emit=(ring,i)=>vertices.push(...rings[ring][i]),triangles=THREE.ShapeUtils.triangulateShape(section.map(([u,y])=>new THREE.Vector2(u,y)),[]);
 for(const t of triangles){for(const i of t)emit(0,i);for(const i of [...t].reverse())emit(1,i);}
 for(let i=0;i<section.length;i++){const j=(i+1)%section.length;for(const[r,k]of[[0,i],[1,i],[1,j],[0,i],[1,j],[0,j]])emit(r,k);}
}
export function wallPrismGeometry(length,width,height,{startSkew=0,endSkew=0}={}){
 const v=[];appendWallPrism(v,{x:-length/2,z:0},{x:length/2,z:0},{heightAtWorld:()=>-height/2},{width,height,startSkew,endSkew});const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(v,3));g.computeVertexNormals();g.userData.wallArchitecture={profile:width>=1.8&&height>=3?'walkway-parapets':'coped-wall',dimensionsVerified:false};return g;
}
export function structuredGateParts(gate,terrain,{height=7,depth=2.8}={}){
 const u=gate.unit,v={x:-u.z,z:u.x},at=(x,z)=>({x:gate.center.x+u.x*x+v.x*z,z:gate.center.z+u.z*x+v.z*z}),W=gate.width,ground=Math.max(...[-W/2-2,W/2+2].flatMap(x=>[-depth/2,depth/2].map(z=>{const p=at(x,z);return terrain.heightAtWorld(p.x,p.z);}))),parts=[];
 for(const side of[-1,1]){const g=wallPrismGeometry(2,depth,height);g.translate(0,height/2,0); // local floor datum, with real lower contact
  const p=g.attributes.position;for(let i=0;i<p.count;i++){const q=at(p.getX(i)+side*(W/2+1),p.getZ(i)),y=p.getY(i);p.setXYZ(i,q.x,y<0?terrain.heightAtWorld(q.x,q.z)-.15:ground+y,q.z);}g.computeVertexNormals();parts.push(g);}
 const positions=[],addBox=(x,y,z,w,h,d)=>{const g=new THREE.BoxGeometry(w,h,d);g.translate(x,y+h/2,z);const p=g.attributes.position,idx=g.index.array;for(const i of idx){const q=at(p.getX(i),p.getZ(i));positions.push(q.x,ground+p.getY(i),q.z);}g.dispose();};
 // Keep the previous header envelope (height-.65 .. height+.65), with an
 // actual overhead passage/deck and parapets instead of one solid header block.
 addBox(0,height-.65,0,W+4,.45,depth);for(const side of[-1,1])addBox(0,height-.2,side*(depth/2-.2),W+4,.85,.4);
 const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(positions,3));g.computeVertexNormals();parts.push(g);for(const p of parts)p.userData.wallArchitecture={profile:'recessed-passage-and-deck',dimensionsVerified:false};return parts;
}

// Local header, centred vertically like BoxGeometry; same outside envelope.
export function gateHeaderGeometry(width,depth,height=1){
 const vertices=[],t=Math.min(.4,depth*.2),slab=height*.25;
 for(const [x,y,z,w,h,d]of[[0,-height/2+slab/2,0,width,slab,depth],[0,slab/2,-(depth-t)/2,width,height-slab,t],[0,slab/2,(depth-t)/2,width,height-slab,t]]){
  const box=new THREE.BoxGeometry(w,h,d);box.translate(x,y,z);const a=box.attributes.position;for(const i of box.index.array)vertices.push(a.getX(i),a.getY(i),a.getZ(i));box.dispose();
 }
 const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(vertices,3));g.computeVertexNormals();return g;
}

// Coarse structural display inside the inherited tower envelope. The bevel,
// wall thickness and deck are authored; this is not an excavated tower plan.
export function towerShellGeometry(width,depth,height,{bevel=.35,wall=.65}={}){
 if(!(width>2*wall&&depth>2*wall&&height>2))throw new Error('Invalid tower envelope');
 const outline=(w,d,b)=>{const x=w/2,z=d/2;return[[-x+b,-z],[x-b,-z],[x,-z+b],[x,z-b],[x-b,z],[-x+b,z],[-x,z-b],[-x,-z+b]];},outer=outline(width,depth,Math.min(bevel,width/6,depth/6)),inner=outline(width-2*wall,depth-2*wall,Math.min(bevel*.5,(width-2*wall)/6,(depth-2*wall)/6)),vertices=[];
 const layer=(low,high,hollow)=>{
  const shape=new THREE.Shape(outer.map(([x,z])=>new THREE.Vector2(x,-z)));if(hollow)shape.holes.push(new THREE.Path(inner.map(([x,z])=>new THREE.Vector2(x,-z))));
  const g=new THREE.ExtrudeGeometry(shape,{depth:high-low,bevelEnabled:false,steps:1});g.rotateX(-Math.PI/2);g.translate(0,low,0);const p=g.attributes.position;for(const i of g.index?.array||Array.from({length:p.count},(_,i)=>i))vertices.push(p.getX(i),p.getY(i),p.getZ(i));g.dispose();
 };
 layer(0,height-.85,true);layer(height-1.05,height-.85,false);layer(height-.85,height,true);
 const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(vertices,3));g.computeVertexNormals();g.userData.wallArchitecture={profile:'tower-shell-recessed-deck',dimensionsVerified:false};return g;
}
export function parapetRingGeometry(width,depth,height=.7,thickness=.4){
 if(!(width>2*thickness&&depth>2*thickness&&height>0))throw new Error('Invalid parapet envelope');const vertices=[];
 for(const [x,z,w,d]of[[0,-(depth-thickness)/2,width,thickness],[0,(depth-thickness)/2,width,thickness],[-(width-thickness)/2,0,thickness,depth-2*thickness],[(width-thickness)/2,0,thickness,depth-2*thickness]]){
  const g=new THREE.BoxGeometry(w,height,d);g.translate(x,height/2,z);const p=g.attributes.position;for(const i of g.index.array)vertices.push(p.getX(i),p.getY(i),p.getZ(i));g.dispose();
 }
 const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(vertices,3));g.computeVertexNormals();return g;
}
