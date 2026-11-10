import {foundationEdgePoints} from './foundation-contact.js';
// Model envelopes derive from existing building/ritual positions, not ancient surveys.
export function firstTempleCourt(data,spatial){
 const t=data.royalCity.temple,[x,z]=t.offset,c=t.cubitMetres,l=t.lengthCubits*c;
 const bounds=[x-l/2-7*c-4,z-14,x+l/2+24,z+14],gateWidth=Math.max(3,spatial.roadWidth+1.4);
 const edge=spatial.edges.find(e=>e.id==='temple-entry');let gateX=null;
 for(let i=1;i<(edge?.points.length||0);i++){const [ax,az]=edge.points[i-1],[bx,bz]=edge.points[i];if(az===bz)continue;const f=(bounds[3]-az)/(bz-az);if(f>=0&&f<=1)gateX=ax+f*(bx-ax);}
 if(!Number.isFinite(gateX)||gateX-gateWidth/2<=bounds[0]||gateX+gateWidth/2>=bounds[2])throw new Error('First temple court must open onto its existing approach');
 return {bounds,gateX,gateWidth,stoneCourseHeight:.35,timberHeight:.2,wallThickness:.6,geometryVerified:false,authority:'authored-envelope-with-1Kings6:36-course-pattern-not-measured-court'};
}
export function courtEnvelopeDatum(bounds,anchor,terrain){
 const [a,b,c,d]=bounds,world=[{x:anchor.x+a,z:anchor.z+b},{x:anchor.x+c,z:anchor.z+b},{x:anchor.x+c,z:anchor.z+d},{x:anchor.x+a,z:anchor.z+d}],samples=[];
 const sample=(x,z)=>{const h=terrain.heightAtWorld(x,z);if(!Number.isFinite(h))throw new Error('Court outside canonical terrain');samples.push(h);};
 for(let i=0;i<4;i++)for(const p of foundationEdgePoints(world[i],world[(i+1)%4],terrain))sample(p.x,p.z);
 const mesh=terrain.mesh,p=mesh?.geometry.attributes.position;
 if(p){for(let i=0;i<p.count;i++){const x=p.getX(i)+mesh.position.x,z=p.getZ(i)+mesh.position.z;if(x>=world[0].x&&x<=world[1].x&&z>=world[0].z&&z<=world[2].z)sample(x,z);}}
 else for(let x=a;x<=c;x+=2)for(let z=b;z<=d;z+=2)sample(anchor.x+x,anchor.z+z);
 return Math.max(...samples);
}
