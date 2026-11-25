import {appendAisledHall} from './aisled-hall-shell.js';
// Inherited display envelopes; opening locations/sections remain authored.
export function appendSepulchreShell(profile,{append,dome,THREE},cx,cz){
 const rx=cx-25,r=20,inner=19.2,height=15,n=64,positions=[],tri=(a,b,c)=>positions.push(...a,...b,...c),quad=(a,b,c,d)=>{tri(a,b,c);tri(c,b,d);tri(c,b,a);tri(d,b,c);},point=(radius,a,y)=>[rx+radius*Math.cos(a),y,cz+radius*Math.sin(a)];
 const doors=profile==='sepulchre-1048-rotunda'?[0,Math.PI/2,Math.PI,3*Math.PI/2]:[0,Math.PI];
 append(new THREE.CylinderGeometry(r,r,.12,64),rx,cz,.06);
 for(let i=0;i<n;i++){
  const a=i*2*Math.PI/n,b=(i+1)*2*Math.PI/n,m=(a+b)/2,portal=doors.some(d=>Math.abs(Math.atan2(Math.sin(m-d),Math.cos(m-d)))<Math.PI/32+.0001),bottom=portal?4:.12;
  quad(point(r,a,bottom),point(r,a,height),point(r,b,bottom),point(r,b,height));
  quad(point(inner,a,bottom),point(inner,a,height),point(inner,b,bottom),point(inner,b,height));
  if(portal)quad(point(r,a,4),point(inner,a,4),point(r,b,4),point(inner,b,4));
 }
 for(const door of doors)for(const side of[-1,1]){const a=door+side*Math.PI/32;quad(point(r,a,.12),point(inner,a,.12),point(r,a,4),point(inner,a,4));}
 const walls=new THREE.BufferGeometry();walls.setAttribute('position',new THREE.Float32BufferAttribute(positions,3));walls.computeVertexNormals();append(walls,0,0);
 const roof=new THREE.RingGeometry(16.8,r,64);roof.rotateX(-Math.PI/2);append(roof,rx,cz,15);dome(rx,cz,17,15);
 const inside=new THREE.SphereGeometry(16.8,32,12,0,Math.PI*2,0,Math.PI/2);inside.scale(-1,1,1);append(inside,rx,cz,15);
 if(profile==='sepulchre-1048-rotunda'){
  for(const side of[-1,1])appendAisledHall({append,THREE},{cx:rx,cz:cz+side*25,length:10,widths:[20],heights:[8],axis:'z',rearOpen:[0]});
 }else if(profile==='constantinian-rotunda-east-basilica'){
  appendAisledHall({append,THREE},{cx:cx+35,cz,length:70,widths:[7.5,7.5,15,7.5,7.5],heights:[11,13,16,13,11],axis:'x',frontEnd:1,rearOpen:[2]});
 }else{
  // Remove the old5m overlap into the rotunda, keeping the same union's east edge.
  appendAisledHall({append,THREE},{cx:cx+17.5,cz,length:45,widths:[50],heights:[16],axis:'x'});
  const x=cx+20,z=cz+32,t=.7,w=12;
  append(new THREE.BoxGeometry(w,.12,w),x,z,.06);
  for(const side of[-1,1]){
   append(new THREE.BoxGeometry(w,17.88,t),x,z+side*(w-t)/2,9.06);
   append(new THREE.BoxGeometry(t,17.88,w-2*t),x+side*(w-t)/2,z,9.06);
  }
  append(new THREE.BoxGeometry(w,.2,w),x,z,18.1);
  for(const sx of[-1,1])for(const sz of[-1,1])append(new THREE.BoxGeometry(1,4.8,1),x+sx*5.5,z+sz*5.5,20.6);
  const cap=new THREE.ConeGeometry(6*Math.SQRT2,2,4);cap.rotateY(Math.PI/4);append(cap,x,z,24);
 }
}
