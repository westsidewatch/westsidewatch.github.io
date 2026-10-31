import * as THREE from 'three';
import {herodianRitualLayout} from './temple-precinct-layout.js';
import {HERODIAN_DIMENSIONS as D} from './herodian-dimensions.js';
const SCHEDULE={foundation:{start:.06,duration:.10,lift:90},retaining:{start:.12,duration:.13,lift:120},circulation:{start:.24,duration:.12,lift:95},superstructure:{start:.38,duration:.18,lift:180},colonnade:{start:.52,duration:.18,lift:145},roof:{start:.68,duration:.14,lift:120}};
function box(builder,size,p,surface,phase,shade=1){const s=SCHEDULE[phase];builder.box(size,p,surface,s.start,{duration:s.duration,lift:s.lift,shade});}
function column(builder,x,y,z,surface,height=13.125){box(builder,[1.2,height,1.2],[x,y+height/2,z],surface,'colonnade',.97);box(builder,[1.8,.6,1.8],[x,y+.3,z],surface,'colonnade',.9);box(builder,[1.8,.6,1.8],[x,y+height-.3,z],surface,'colonnade',1);}
function precinctY(r){return r.precinctUp??r.up;}
function platform(builder,r,surface){const y=precinctY(r),w=D.platform.eastWest,d=D.platform.northSouth,top=y+D.platform.pavingThickness;box(builder,[w,.8,d],[r.east,y+.4,-r.north],surface,'foundation',.94);const retain=(x,z,width,depth)=>{const samples=[[-width/2,-depth/2],[width/2,-depth/2],[width/2,depth/2],[-width/2,depth/2],[0,0]].map(([dx,dz])=>r.terrain?.heightAtWorld?.(x+dx,z+dz)).filter(Number.isFinite),bottom=Math.min(top-16,...samples.map(y=>y-.3));box(builder,[width,top-bottom,depth],[x,(top+bottom)/2,z],surface,'retaining');};for(const z of[-d/2+2,d/2-2])for(let x=-w/2;x<w/2;x+=10)retain(r.east+x+5,-r.north+z,10,4);for(const x of[-w/2+2,w/2-2])for(let z=-d/2;z<d/2;z+=10)retain(r.east+x,-r.north+z+5,4,10);for(let z=-d/2+12;z<d/2;z+=40)box(builder,[w-12,.12,1.2],[r.east,top+.06,-r.north+z],surface,'circulation',.94);}
function stoa(builder,r,surface){const y=precinctY(r)+D.platform.pavingThickness,w=D.stoa.eastWest,d=D.stoa.depth;box(builder,[w,1,d],[r.east,y+.5,-r.north],surface,'foundation');for(let i=0;i<12;i++)for(let row=0;row<4;row++){const x=r.east-w/2+4+i*(w-8)/11,z=-r.north-d/2+2+row*(d-4)/3,h=row===0||row===3?D.stoa.sideHeight-2:D.stoa.centreHeight-2;column(builder,x,y+1,z,surface,h);}
 for(const z of[-d*.35,d*.35])box(builder,[w,1.2,d*.3],[r.east,y+D.stoa.sideHeight-.6,-r.north+z],surface,'roof',.94);box(builder,[w,1.2,d*.4],[r.east,y+D.stoa.centreHeight-.6,-r.north],surface,'roof',1);}
function fortress(builder,r,surface){const y=r.up;box(builder,[126,2,106],[r.east,y+1,-r.north],surface,'foundation');box(builder,[100,21,80],[r.east,y+12.5,-r.north],surface,'superstructure',.94);for(const[x,z]of[[-50,-40],[50,-40],[-50,40],[50,40]]){const h=x>0&&z>0?70*D.cubitMetres:50*D.cubitMetres;box(builder,[22,h-1,22],[r.east+x,y+2+(h-1)/2,-r.north+z],surface,'superstructure');box(builder,[24,1,24],[r.east+x,y+2+h-.5,-r.north+z],surface,'roof',.95)}box(builder,[104,1,84],[r.east,y+23.5,-r.north],surface,'roof',.96);}
function sacredComplex(builder,r,surface){
 const base=precinctY(r)+D.platform.pavingThickness,layout=herodianRitualLayout(D.cubitMetres),c=D.cubitMetres;
 const y=base+layout.levels.priests,israelY=base+layout.levels.israel,w=D.priestCourt.eastWest,d=D.priestCourt.northSouth,ww=D.womenCourt.eastWest,courtX=r.east-ww/2;
 const minX=courtX-w/2,innerEast=courtX+w/2,maxX=innerEast+ww,israelWest=innerEast-layout.israelWidth,transition=4*layout.stepTread;
 // Solid substructure: the level change must not leave a floating courtyard.
 box(builder,[w,layout.levels.israel+.6,d],[courtX,base+(layout.levels.israel-.6)/2+.02,-r.north],surface,'foundation',.96);
 const raisedWidth=israelWest-transition-minX;
 box(builder,[raisedWidth,layout.levels.priests-layout.levels.israel,d],[minX+raisedWidth/2,(y+israelY)/2+.02,-r.north],surface,'foundation',.96);
 box(builder,[ww,.6,d],[innerEast+ww/2,base-.28,-r.north],surface,'foundation',.96);
 // Selected Middot2:6 tradition: one-cubit platform plus three half-cubit rises.
 for(let i=0;i<4;i++){const rise=(1+i/2)*c;box(builder,[layout.stepTread,rise,d-4],[israelWest-(i+.5)*layout.stepTread,israelY+.02+rise/2,-r.north],surface,'circulation',.94);}
 for(const z of[-d/2+1,d/2-1]){
  box(builder,[w,layout.levels.priests+4,2],[courtX,base+(layout.levels.priests+4)/2,-r.north+z],surface,'retaining',.94);
  box(builder,[ww,4,2],[innerEast+ww/2,base+2,-r.north+z],surface,'retaining',.94);
 }
 box(builder,[2,layout.levels.priests+4,d],[minX+1,base+(layout.levels.priests+4)/2,-r.north],surface,'retaining',.94);
 const gateWidth=10*c,gateHeight=20*c;
 for(const [x,datum] of [[maxX-1,base],[innerEast,israelY]]){
  for(const sign of[-1,1]){const span=(d-gateWidth)/2,height=datum-base+4;
   box(builder,[2,height,span],[x,base+height/2,-r.north+sign*(gateWidth/2+span/2)],surface,'retaining',.94);
   box(builder,[2,gateHeight,1.5],[x,datum+.02+gateHeight/2,-r.north+sign*(gateWidth/2+.75)],surface,'superstructure',.98);
  }
  box(builder,[2,.8,gateWidth+3],[x,datum+.02+gateHeight+.4,-r.north],surface,'roof',.98);
 }
 // Fifteen semicircular steps to the elevated Israel threshold, separate from
 // the twelve porch steps. Each solid half-disc is one batched primitive.
 for(let i=0;i<15;i++){
  const radius=gateWidth/2+(i+1)*layout.stepTread,height=(15-i)*layout.stepRise;
  const g=builder.geo(`court-semicircle:${i}`,()=>new THREE.CylinderGeometry(radius,radius,height,32,1,false,0,Math.PI));
  const schedule=SCHEDULE.circulation;
  builder.add(g,surface,schedule.start,{p:[innerEast+1,base+.02+height/2,-r.north],duration:schedule.duration,lift:schedule.lift,shade:.96});
 }
 box(builder,[2,layout.levels.israel,gateWidth],[innerEast,base+.02+layout.levels.israel/2,-r.north],surface,'foundation',.96);
 const altarX=minX+layout.altar.centreFromWest;
 // Stepped altar mass; upper-body height is an authored display interpretation.
 for(const [size,bottom,height]of[[32,0,1],[30,1,5],[28,6,3]])box(builder,[size*c,height*c,size*c],[altarX,y+.02+(bottom+height/2)*c,-r.north],surface,'superstructure',.96);
 for(const sx of[-1,1])for(const sz of[-1,1])box(builder,[c,c,c],[altarX+sx*13*c,y+.02+9.5*c,-r.north+sz*13*c],surface,'superstructure',1);
 // Continuous ramp assembled from sloped boxes; no staircase substituted for a ramp.
 const rise=9*c,run=layout.ramp.length,schedule=SCHEDULE.circulation;
 const ramp=builder.geo(`temple-ramp:${c}`,()=>{
  const g=new THREE.BoxGeometry(layout.ramp.width,rise,run),p=g.attributes.position;
  for(let i=0;i<p.count;i++)p.setY(i,p.getY(i)>0?(p.getZ(i)<0?rise:0):0);
  g.computeVertexNormals();return g;
 });
 builder.add(ramp,surface,schedule.start,{p:[altarX,y+.02,-r.north+layout.ramp.altarJoinOffset+run/2],duration:schedule.duration,lift:schedule.lift,shade:.95});
 // Four open-roof corner chambers, with real inward-facing access gaps.
 const wc=(courtX+w/2+ww/2),room=layout.womenRoom;
 for(const sx of[-1,1])for(const sz of[-1,1]){
  const rx=wc+sx*(ww/2-room.inset-room.size/2),rz=-r.north+sz*(d/2-room.inset-room.size/2),b=base+.02;
  box(builder,[room.size,room.height,room.wall],[rx,b+room.height/2,rz+sz*(room.size-room.wall)/2],surface,'superstructure',.94);
  for(const side of[-1,1])box(builder,[room.wall,room.height,room.size],[rx+side*(room.size-room.wall)/2,b+room.height/2,rz],surface,'superstructure',.94);
  const opening=3,span=(room.size-opening)/2;
  for(const side of[-1,1])box(builder,[span,room.height,room.wall],[rx+side*(opening/2+span/2),b+room.height/2,rz-sz*(room.size-room.wall)/2],surface,'superstructure',.94);
 }
 const west=minX+11*D.cubitMetres,porchDepth=10*D.cubitMetres,bodyLength=D.sanctuary.eastWest-porchDepth,h=D.sanctuary.height;
 box(builder,[D.sanctuary.eastWest,6*D.cubitMetres,D.sanctuary.porchNorthSouth],[west+D.sanctuary.eastWest/2,y+3*D.cubitMetres,-r.north],surface,'foundation',.98);
 box(builder,[bodyLength,h-6*D.cubitMetres-1.2,D.sanctuary.bodyNorthSouth],[west+bodyLength/2,y+(h+6*D.cubitMetres-1.2)/2,-r.north],surface,'superstructure',1);
 const openingWidth=20*D.cubitMetres,openingHeight=40*D.cubitMetres,podium=6*D.cubitMetres,porchX=west+bodyLength+porchDepth/2,side=(D.sanctuary.porchNorthSouth-openingWidth)/2;
 for(const sign of[-1,1])box(builder,[porchDepth,h-podium-1.2,side],[porchX,y+(h+podium-1.2)/2,-r.north+sign*(openingWidth/2+side/2)],surface,'superstructure',.98);
 box(builder,[porchDepth,h-podium-openingHeight-1.2,openingWidth],[porchX,y+(h-1.2+podium+openingHeight)/2,-r.north],surface,'superstructure',.98);
 // Middot3:6 gives12 half-cubit rises and one-cubit treads; landings remain unmodelled.
 for(let i=0;i<12;i++){const rise=(12-i)*D.cubitMetres/2;box(builder,[D.cubitMetres,rise,openingWidth],[west+D.sanctuary.eastWest+(i+.5)*D.cubitMetres,y+rise/2,-r.north],surface,'circulation',.96);}
 box(builder,[bodyLength,1.2,D.sanctuary.bodyNorthSouth],[west+bodyLength/2,y+h-.6,-r.north],surface,'roof',.98);
 box(builder,[porchDepth,1.2,D.sanctuary.porchNorthSouth],[west+bodyLength+porchDepth/2,y+h-.6,-r.north],surface,'roof',1);
 for(let i=0;i<10;i++)for(const sign of[-1,1]){const x=minX+4+i*(maxX-minX-8)/9,datum=x<israelWest-transition?y:x<innerEast?israelY:base;column(builder,x,datum+.02,-r.north+sign*(d/2-3),surface,10.5);}
}
function approach(builder,r,surface){const y=r.up;for(let i=0;i<13;i++){const width=184-i*3;box(builder,[width,4.5,16],[r.east,y+i*2,-r.north+(i-6)*15],surface,'circulation',i%2?.94:1)}for(const x of[-58,58])box(builder,[24,30,20],[r.east+x,y+27,-r.north+104],surface,'superstructure',.95);}
function street(builder,r,surface){const y=r.up;for(let i=-10;i<=10;i++)for(let j=-1;j<=1;j++)box(builder,[16,4.5,17],[r.east+j*17,y+2.25,-r.north+i*17],surface,'circulation',(i+j)%2?.91:.98);box(builder,[10,24,360],[r.east-34,y+12,-r.north],surface,'retaining',.9);}
export const ARCHITECTURAL_GRAMMAR_VERSION='j3k.architecture.v6-court-sections';
export const SUPPORTED_ARCHITECTURAL_KINDS=Object.freeze(['platform-enclosure','portico-basilica','fortress','sacred-complex','pilgrimage-access','street']);
export function buildArchitecturalGrammar(builder,object,registration,surface){switch(object.kind){case'platform-enclosure':platform(builder,registration,surface);break;case'portico-basilica':stoa(builder,registration,surface);break;case'fortress':fortress(builder,registration,surface);break;case'sacred-complex':sacredComplex(builder,registration,surface);break;case'pilgrimage-access':approach(builder,registration,surface);break;case'street':street(builder,registration,surface);break;default:return false}return true;}
