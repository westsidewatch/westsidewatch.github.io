import * as THREE from 'three';
export const ROMAN_GATE_SOURCES=['https://www.pami.co.il/en/attractions/the-roman-square-museum-at-damascus-gate/','https://hadashot.iaa.org.il/Report_Detail_Eng.aspx?id=26040'];
export const isRomanMonumentalGate=(phase,key)=>['aelia','byzantine'].includes(phase)&&key==='north';
// Replace the existing northern opening, never create a second semantic gate.
export function romanGateFootprint(gate){const u=gate.unit,v={x:-u.z,z:u.x};return [[-22,-6],[22,-6],[22,50],[-22,50]].map(([a,b])=>({x:gate.center.x+u.x*a+v.x*b,z:gate.center.z+u.z*a+v.z*b}));}
export function romanGateGeometry(gate,terrain){
 const u=gate.unit,v={x:-u.z,z:u.x},world=(a,b)=>({x:gate.center.x+u.x*a+v.x*b,z:gate.center.z+u.z*a+v.z*b});
 const ground=Math.max(...[-22,22].flatMap(a=>[-6,6].map(b=>{const p=world(a,b);return terrain.heightAtWorld(p.x,p.z);}))),parts=[];
 function locate(g,{surface=false}={}){const p=g.attributes.position;for(let i=0;i<p.count;i++){const q=world(p.getX(i),p.getZ(i)),y=p.getY(i),base=terrain.heightAtWorld(q.x,q.z);if(!Number.isFinite(base))throw new Error('Roman gate outside canonical DEM');p.setXYZ(i,q.x,(surface||y<1e-6?base:ground)+y+.12,q.z);}g.computeVertexNormals();parts.push(g);}
 const box=(x,z,w,d,h)=>{const g=new THREE.BoxGeometry(w,h,d);g.translate(x,h/2,z);locate(g);};
 for(const [a,b]of [[-18,-14.5],[-9.5,-6],[6,9.5],[14.5,18]])box((a+b)/2,0,b-a,8,18);
 for(const side of [-1,1])box(side*20,0,4,12,20);
 for(const [center,radius,spring]of [[-12,2.5,6],[0,6,9],[12,2.5,6]]){
  const shape=new THREE.Shape();shape.moveTo(center-radius,18);shape.lineTo(center+radius,18);shape.lineTo(center+radius,spring);
  for(let i=1;i<=16;i++){const angle=Math.PI*i/16;shape.lineTo(center+radius*Math.cos(angle),spring+radius*Math.sin(angle));}shape.closePath();
  const g=new THREE.ExtrudeGeometry(shape,{depth:8,bevelEnabled:false,steps:1});g.translate(0,0,-4);locate(g);
 }
 // The plaza extent and column height are authored context, not excavated bounds.
 const plaza=new THREE.PlaneGeometry(40,44,10,11);plaza.rotateX(-Math.PI/2);plaza.translate(0,0,28);locate(plaza,{surface:true});
 const at=world(0,29),base=terrain.heightAtWorld(at.x,at.z),column=new THREE.CylinderGeometry(1,1.2,10,12);const p=column.attributes.position;for(let i=0;i<p.count;i++)p.setXYZ(i,p.getX(i)+at.x,p.getY(i)+base+5+.12,p.getZ(i)+at.z);column.computeVertexNormals();parts.push(column);
 return parts;
}
