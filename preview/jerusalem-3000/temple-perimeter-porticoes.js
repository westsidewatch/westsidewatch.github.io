import {HERODIAN_DIMENSIONS as D} from './herodian-dimensions.js';
import * as THREE from 'three';
// Provisional colonnades within the inherited300×480m model, not surveyed lines.
// Stop before the existing Antonia envelope; do not move the fortress or city.
export const PERIMETER_PORTICO_SEGMENTS=Object.freeze([
 {id:'east',axis:'z',fixed:133.5,start:-235.5,end:150,width:20},
 {id:'west',axis:'z',fixed:-133.5,start:-158,end:150,width:20},
 {id:'north',axis:'x',fixed:-225.5,start:-2,end:123.5,width:20}
]);
export function buildPerimeterPorticoes(builder,r,surface,emit){
 const y=(r.precinctUp??r.up)+D.platform.pavingThickness,columnHeight=25*D.cubitMetres,roofThickness=.8;
 for(const s of PERIMETER_PORTICO_SEGMENTS){
  const mid=(s.start+s.end)/2,span=s.end-s.start;
  const position=(along,across,up)=>s.axis==='z'?[r.east+s.fixed+across,up,-r.north+along]:[r.east+along,up,-r.north+s.fixed+across];
  const size=(along,height,across)=>s.axis==='z'?[across,height,along]:[along,height,across];
  emit(builder,size(span,.12,s.width),position(mid,0,y+.06),surface,'foundation',.95);
  const bays=Math.ceil((span-4)/7);
  for(let i=0;i<=bays;i++)for(const row of[-1,1]){
   const p=position(s.start+2+(span-4)*i/bays,row*6,y+.12),shaft=builder.geo('perimeter-portico-shaft',()=>new THREE.CylinderGeometry(.48,.6,columnHeight-1.2,12));
   builder.add(shaft,surface,.52,{p:[p[0],p[1]+columnHeight/2,p[2]],duration:.18,lift:145,shade:.97});
   emit(builder,[1.6,.6,1.6],[p[0],p[1]+.3,p[2]],surface,'colonnade',.94);
   emit(builder,[1.6,.6,1.6],[p[0],p[1]+columnHeight-.3,p[2]],surface,'colonnade',1);
  }
  emit(builder,size(span,roofThickness,s.width),position(mid,0,y+.12+columnHeight+roofThickness/2),surface,'roof',.97);
 }
}
