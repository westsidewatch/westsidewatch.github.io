import * as THREE from 'three';
import {sanctuaryAccessVertices} from './sanctuary-access-geometry.js';
import {courtEnvelopeDatum} from './temple-court-envelopes.js';
import {foundationEdgePoints} from './foundation-contact.js';
// Selected reference width; individual risers/treads and exact placement authored.
export function southernApproachPlan(){let cursor=0;return{width:64,rise:.25,height:6.5,steps:Array.from({length:26},(_,i)=>{const depth=i%2?.8:.4,p={start:cursor,end:cursor+depth,height:(26-i)*.25};cursor+=depth;return p;}),authority:'reference-width-with-authored-26step-profile-not-excavation-plan'};}
export function southernApproachReservation(r,padding=2){const p=southernApproachPlan(),a=r.east-p.width/2-padding,b=r.east+p.width/2+padding,c=-r.north-padding,d=-r.north+p.steps.at(-1).end+padding;return{objectId:'j3k:object:southern-approach',authority:'actual-step-plan-plus-engineering-clearance-not-historical-plaza',polygon:[{x:a,z:c},{x:b,z:c},{x:b,z:d},{x:a,z:d}]};}
export function buildSouthernApproach(builder,r,surface){
 const plan=southernApproachPlan(),terrain=r.terrain,worldSurface=(x,z)=>terrain?.heightAtWorld?.(x,z)??r.up,north=-r.north;
 let lift=0;
 for(const step of plan.steps){const bounds=[r.east-plan.width/2,north+step.start,r.east+plan.width/2,north+step.end],ground=terrain?courtEnvelopeDatum(bounds,{x:0,z:0},terrain):r.up;lift=Math.max(lift,ground+.1-r.up-step.height);}
 for(const [i,step]of plan.steps.entries()){
  const top=r.up+lift+step.height,za=north+step.start,zb=north+step.end,vertices=sanctuaryAccessVertices([[r.east,za],[r.east,zb]],plan.width,worldSurface,()=>top,terrain?{terrain,anchor:{x:0,z:0}}:null);
  const face=(a,b,c,d)=>vertices.push(...a,...b,...c,...c,...b,...d,...c,...b,...a,...d,...b,...c);
  const cap=(z,low)=>{
   const a={x:r.east-plan.width/2,z},b={x:r.east+plan.width/2,z},points=terrain?foundationEdgePoints(a,b,terrain):[a,b];
   for(let j=1;j<points.length;j++){const p=points[j-1],q=points[j];face([p.x,top,z],[p.x,low(p.x,z),z],[q.x,top,z],[q.x,low(q.x,z),z]);}
  };
  cap(zb,i<plan.steps.length-1?()=>top-plan.rise:worldSurface);if(i===0)cap(za,worldSurface);
  const geometry=new THREE.BufferGeometry();geometry.setAttribute('position',new THREE.Float32BufferAttribute(vertices,3));geometry.computeVertexNormals();builder.add(geometry,surface,.24,{duration:.12,lift:95,shade:i%2?.94:1});geometry.dispose();
 }
 return{...plan,displayDatumLift:lift};
}
