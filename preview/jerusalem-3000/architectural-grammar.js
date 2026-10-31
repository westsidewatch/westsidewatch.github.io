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
 const y=precinctY(r)+D.platform.pavingThickness,w=D.priestCourt.eastWest,d=D.priestCourt.northSouth,ww=D.womenCourt.eastWest,courtX=r.east-ww/2;
 box(builder,[w,.6,d],[courtX,y-.28,-r.north],surface,'foundation',.96);box(builder,[ww,.6,d],[courtX+w/2+ww/2,y-.28,-r.north],surface,'foundation',.96);
 const minX=courtX-w/2,maxX=courtX+w/2+ww;
 for(const z of[-d/2+1,d/2-1])box(builder,[w+ww,4,2],[(minX+maxX)/2,y+2,-r.north+z],surface,'retaining',.94);
 box(builder,[2,4,d],[minX+1,y+2,-r.north],surface,'retaining',.94);
 const gateWidth=10*D.cubitMetres,gateHeight=20*D.cubitMetres;
 for(const x of[maxX-1,courtX+w/2]){for(const sign of[-1,1]){const span=(d-gateWidth)/2;box(builder,[2,4,span],[x,y+2,-r.north+sign*(gateWidth/2+span/2)],surface,'retaining',.94);box(builder,[2,gateHeight,1.5],[x,y+.02+gateHeight/2,-r.north+sign*(gateWidth/2+.75)],surface,'superstructure',.98);}box(builder,[2,.8,gateWidth+3],[x,y+.02+gateHeight+.4,-r.north],surface,'roof',.98);}
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
 for(let i=0;i<10;i++)for(const sign of[-1,1])column(builder,minX+4+i*(maxX-minX-8)/9,y+.6,-r.north+sign*(d/2-3),surface,10.5);
}
function approach(builder,r,surface){const y=r.up;for(let i=0;i<13;i++){const width=184-i*3;box(builder,[width,4.5,16],[r.east,y+i*2,-r.north+(i-6)*15],surface,'circulation',i%2?.94:1)}for(const x of[-58,58])box(builder,[24,30,20],[r.east+x,y+27,-r.north+104],surface,'superstructure',.95);}
function street(builder,r,surface){const y=r.up;for(let i=-10;i<=10;i++)for(let j=-1;j<=1;j++)box(builder,[16,4.5,17],[r.east+j*17,y+2.25,-r.north+i*17],surface,'circulation',(i+j)%2?.91:.98);box(builder,[10,24,360],[r.east-34,y+12,-r.north],surface,'retaining',.9);}
export const ARCHITECTURAL_GRAMMAR_VERSION='j3k.architecture.v4-temple-entries';
export const SUPPORTED_ARCHITECTURAL_KINDS=Object.freeze(['platform-enclosure','portico-basilica','fortress','sacred-complex','pilgrimage-access','street']);
export function buildArchitecturalGrammar(builder,object,registration,surface){switch(object.kind){case'platform-enclosure':platform(builder,registration,surface);break;case'portico-basilica':stoa(builder,registration,surface);break;case'fortress':fortress(builder,registration,surface);break;case'sacred-complex':sacredComplex(builder,registration,surface);break;case'pilgrimage-access':approach(builder,registration,surface);break;case'street':street(builder,registration,surface);break;default:return false}return true;}
