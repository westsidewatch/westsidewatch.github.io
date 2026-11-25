import * as THREE from 'three';
import {courtEnvelopeDatum} from './temple-court-envelopes.js';
import {sanctuaryAccessVertices} from './sanctuary-access-geometry.js';
// Small illustrative frontage, not a digitized excavation or a claim that
// four observed Robinson-arch cells stood at these particular coordinates.
export function westernMarketPlan(route){
 const depth=route.clearance,cell=4.5,count=4,wall=.25,start=165,end=start+count*cell;
 return {depth,cell,count,wall,start,end,x:route.platformWest-depth/2,height:3.2,door:1.8,roof:.2,authority:'inferred-market-and-roof-lane-context-not-surveyed-cells',historicalGeometryAccepted:false};
}
export function buildWesternMarket(builder,r,route){
 const p=westernMarketPlan(route),surface=(x,z)=>r.terrain?.heightAtWorld?.(x,z)??r.up;
 const bounds=[p.x-p.depth/2,p.start,p.x+p.depth/2,p.end],ground=r.terrain?courtEnvelopeDatum(bounds,{x:0,z:0},r.terrain):r.up,base=ground+.12;
 const box=(size,pos,shade=1,contact=false)=>{
 const g=new THREE.BoxGeometry(...size),v=g.attributes.position;if(contact)for(let i=0;i<v.count;i++)if(v.getY(i)<0)v.setY(i,surface(pos[0]+v.getX(i),pos[2]+v.getZ(i))+.16-pos[1]);g.computeVertexNormals();builder.add(g,'inferred',.4,{p:pos,duration:.18,lift:60,shade,componentId:'western-market'});g.dispose();};
 const v=sanctuaryAccessVertices([[p.x,p.start],[p.x,p.end]],p.depth,surface,(x,z)=>surface(x,z)+.16,r.terrain?{terrain:r.terrain,anchor:{x:0,z:0}}:null),g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(v,3));g.computeVertexNormals();builder.add(g,'inferred',.35,{duration:.12,lift:40,componentId:'western-market'});g.dispose();
 // Closed rear against the platform; separate side partitions and real west doors.
 for(let z=p.start;z<p.end;z+=1.5)box([p.wall,p.height,Math.min(1.5,p.end-z)],[route.platformWest-p.wall/2,base+p.height/2,z+Math.min(1.5,p.end-z)/2],.94,true);
 for(let i=0;i<=p.count;i++)box([p.depth-p.wall,p.height,p.wall],[p.x-p.wall/2,base+p.height/2,p.start+i*p.cell],.95,true);
 for(let i=0;i<p.count;i++){
  const z=p.start+(i+.5)*p.cell,span=(p.cell-p.door)/2,x=p.x-p.depth/2+p.wall/2;
  for(const side of[-1,1])box([p.wall,p.height,span],[x,base+p.height/2,z+side*(p.door/2+span/2)],.97,true);
  const threshold=Math.max(...[-1,0,1].map(a=>surface(p.x-p.depth/2,z+a*p.door/2)))+.16,head=threshold+2.3,top=base+p.height;box([p.wall,top-head,p.door],[x,(head+top)/2,z],.97);
 }
 box([p.depth,p.roof,p.end-p.start],[p.x,base+p.height+p.roof/2,(p.start+p.end)/2],.9);
 // Low open edge, not an invented upper storey. Vertical street access remains unbuilt.
 box([.2,.55,p.end-p.start],[p.x-p.depth/2+.1,base+p.height+p.roof+.275,(p.start+p.end)/2],.96);
 return {...p,base,roofTop:base+p.height+p.roof,streetAccess:'unresolved-not-rendered',geometryVerified:false};
}
