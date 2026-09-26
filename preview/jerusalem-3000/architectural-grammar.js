const SCHEDULE={
  foundation:{start:.06,duration:.10,lift:90},
  retaining:{start:.12,duration:.13,lift:120},
  circulation:{start:.24,duration:.12,lift:95},
  superstructure:{start:.38,duration:.18,lift:180},
  colonnade:{start:.52,duration:.18,lift:145}
};
function box(builder,size,p,surface,phase,shade=1){const s=SCHEDULE[phase];builder.box(size,p,surface,s.start,{duration:s.duration,lift:s.lift,shade});}
function platform(builder,r,surface){const y=r.up;box(builder,[520,18,340],[r.east,y+9,-r.north],surface,'foundation',.94);for(const z of[-170,170])box(builder,[520,28,14],[r.east,y+14,-r.north+z],surface,'retaining');for(const x of[-260,260])box(builder,[14,28,340],[r.east+x,y+14,-r.north],surface,'retaining');}
function stoa(builder,r,surface){const y=r.up;box(builder,[390,12,70],[r.east,y+6,-r.north],surface,'foundation');for(let i=-9;i<=9;i++){const x=r.east+i*20;box(builder,[6,48,6],[x,y+30,-r.north-24],surface,'colonnade',.98);box(builder,[6,48,6],[x,y+30,-r.north+24],surface,'colonnade',.92)}box(builder,[390,10,70],[r.east,y+59,-r.north],surface,'superstructure');}
function fortress(builder,r,surface){const y=r.up;box(builder,[120,18,100],[r.east,y+9,-r.north],surface,'foundation');for(const[x,z]of[[-50,-40],[50,-40],[-50,40],[50,40]])box(builder,[28,86,28],[r.east+x,y+52,-r.north+z],surface,'superstructure');box(builder,[100,54,80],[r.east,y+36,-r.north],surface,'superstructure',.94);}
function approach(builder,r,surface){const y=r.up;for(let i=0;i<9;i++)box(builder,[170,5,20],[r.east,y+i*2.2,-r.north+(i-4)*18],surface,'circulation',.96);}
function street(builder,r,surface){const y=r.up;for(let i=-7;i<=7;i++)box(builder,[48,5,18],[r.east,y+2.5,-r.north+i*18],surface,'circulation',i%2?.92:1);}
export function buildArchitecturalGrammar(builder,object,registration,surface){switch(object.kind){case'platform-enclosure':platform(builder,registration,surface);break;case'portico-basilica':stoa(builder,registration,surface);break;case'fortress':fortress(builder,registration,surface);break;case'pilgrimage-access':approach(builder,registration,surface);break;case'street':street(builder,registration,surface);break;default:return false}return true;}
