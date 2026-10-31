import * as THREE from 'three';
// Relative literary relationships; small-object sizes and lateral spacing authored.
export function herodianServiceLayout(c=.525){
 return {laver:{xFromCourtWest:122*c,z:14*c,radius:1.5*c,bowlHeight:2*c,baseHeight:c},
  rings:Array.from({length:24},(_,i)=>({x:(i%4-1.5)*8*c,z:-(26+Math.floor(i/4)*4)*c})),
  pillars:Array.from({length:8},(_,i)=>({x:(i-3.5)*4*c,z:-56*c})),
  tables:Array.from({length:7},(_,i)=>({x:(i-3)*4*c,z:-52*c})),
  ringArrangement:'selected-six-rows-of-four; four-by-six-alternative-not-combined',geometryVerified:false};
}
export function buildHerodianService({builder,minX,altarX,y,z,c,surface,emit}){
 const layout=herodianServiceLayout(c),floor=y+.02;
 const box=(size,p,shade=1)=>emit(builder,size,p,surface,'superstructure',shade);
 const add=(g,p,shade=1,r=[0,0,0])=>builder.add(g,surface,.38,{p,r,shade,duration:.18,lift:180});
 const laver=layout.laver,lx=minX+laver.xFromCourtWest,lz=z+laver.z;
 const support=builder.geo('laver-base',()=>new THREE.CylinderGeometry(.5*c,.6*c,laver.baseHeight,16));
 add(support,[lx,floor+laver.baseHeight/2,lz],.86);
 const h=laver.bowlHeight,R=laver.radius,t=.1*c;
 const profile=[[0,-h/2],[R*.65,-h/2],[R,h/2],[R-t,h/2],[R*.65-t,-h/2+t],[0,-h/2+t]].map(([x,y])=>new THREE.Vector2(x,y));
 add(builder.geo('laver-open-bowl',()=>new THREE.LatheGeometry(profile,20)),[lx,floor+laver.baseHeight+h/2,lz],.86);
 const ring=builder.geo('north-service-ring',()=>new THREE.TorusGeometry(.5*c,.07*c,6,16));
 for(const p of layout.rings)add(ring,[altarX+p.x,floor+.07*c,z+p.z],.7,[Math.PI/2,0,0]);
 for(const p of layout.pillars){box([.6*c,2.2,.6*c],[altarX+p.x,floor+1.1,z+p.z],.97);box([1.2*c,.2,1.2*c],[altarX+p.x,floor+2.3,z+p.z],.76);}
 for(const p of layout.tables){const x=altarX+p.x,zz=z+p.z;for(const side of[-1,1])box([.2,.7,.7],[x+side*.45,floor+.35,zz],.96);box([1.4,.15,.9],[x,floor+.775,zz],1.05);}
 return layout;
}
