// Westside Watch / Emmaus V16 / native SVG engraving generator.
// Zero dependencies; run: node scripts/build-emmaus-engraving-v16.mjs > static/images/p2-emmaus-chronology-engraving-v16.svg
// Source: Luke 24:27; 2 Peter 3:8; Psalm 16:2. Experimental / not production.
function buildEmmausV16(){
 const W=1600,H=900,I="#102a43",G="#a2872a",P="#738077",out=[];
 const f=n=>Math.round(n*10)/10;
 const fmt=(a)=>a.map(f).join(" ");
 let n=0;
 function poly(points,{c=I,o=.25,w=.58,dash=""}={}){
  if(points.length<2)return;
  const d="M "+points.map(fmt).join(" L ");
  out.push(`<path d="${d}" stroke="${c}" stroke-opacity="${o.toFixed(3)}" stroke-width="${w.toFixed(2)}"${dash?` stroke-dasharray="${dash}"`:""}/>`);
  n++;
 }
 function segment(x1,y1,x2,y2,o=.2,w=.5,c=I,dash=""){poly([[x1,y1],[x2,y2]],{c,o,w,dash});}
 const bell=(x,center,width)=>Math.exp(-Math.pow((x-center)/width,2));
 const safe=(n,a,b)=>Math.max(a,Math.min(b,n));
 // Three broad directional distortions, each derived from a bounded local field;
 // none has a singularity or draws a black hole.
 function field(x,y){
  const s1=bell(x-230,0,470)*bell(y-270,0,310);
  const s2=bell(x-1260,0,550)*bell(y-605,0,340);
  const s3=bell(x-820,0,690)*bell(y-455,0,400);
  const X=x+ (75*((y-270)/310)*s1) - (98*((y-605)/340)*s2) + 26*((y-455)/400)*s3;
  const Y=y+ 56*((x-230)/470)*s1 - 70*((x-1260)/550)*s2
       + 32*((x-820)/690)*s3;
  return [X,Y];
 }
 out.push(`<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900" fill="none" role="img" aria-labelledby="em-title em-desc">`);
 out.push(`<title id="em-title">Emmaus — timeless scriptural concordance, V16</title>`);
 out.push(`<desc id="em-desc">Original native SVG engraving for the P2 film field. Time passes through the opened interpretation of Scripture: a field of measured temporal cross-sections, 66 interrelated registers and local engraved hatching. Luke 24:27; 2 Peter 3:8; Psalm 16:2. No physical scroll, black hole, or imagery of God.</desc>`);
 out.push(`<metadata>Westside Design OS / ONE colors: paper #ded096 (CSS backdrop); ink ${I}; accent ${G}. Experimental, not accepted. All graphic marks are paths; no raster, no gradients, no filters.</metadata>`);
 out.push(`<g stroke-linecap="round" stroke-linejoin="round">`);
 // Distorted orthogonal ruled field. This is the foundational graphic grammar,
 // not waves. It spans the complete outside-film field including all 4 edges.
 out.push(`<g id="time-longitudes" aria-hidden="true">`);
 for(let i=0;i<97;i++){
  const x=-50+i*17.85,points=[];
  for(let j=0;j<=55;j++){const y=-80+j*1060/55;points.push(field(x,y));}
  const emphasis=i%12===0;
  poly(points,{o:emphasis?.34:.09+.065*(i%7)/6,w:emphasis?.82:.38+(i%5===0?.08:0),c:emphasis?I:P});
 }
 out.push("</g>");
 out.push(`<g id="time-latitudes" aria-hidden="true">`);
 for(let i=0;i<59;i++){
  const y=-52+i*17.5,points=[];
  for(let j=0;j<=73;j++){const x=-80+j*1760/73;points.push(field(x,y));}
  poly(points,{o:i%8===0?.34:.105+.10*(i%7)/6,w:i%8===0?.84:.4,c:i%8===0?I:P});
 }
 out.push("</g>");
 // Main temporal passage is an embossed corridor of varying openness, not
 // a symmetrical dark throat. Each path spans both edges with no fill.
 out.push(`<g id="interpretive-passage" aria-hidden="true">`);
 for(let i=0;i<90;i++){
  const v=(i-44.5)/44.5,points=[];
  for(let j=0;j<=93;j++){
   const x=-95+j*1790/93;
   const pinch=.56+.44*(1-bell(x,785,275)); // compressed but never collapses
   const opening=.17*bell(x,300,490)+.14*bell(x,1300,550);
   const corr=440 + (v*310)*(pinch+opening);
   const offset=17*bell(x,270,540)-24*bell(x,1230,510);
   const y=corr+offset + v*17*Math.sin(x/230+v*3)*bell(x,800,620);
   points.push(field(x,y));
  }
  const density=.11+.19*bell(Math.abs(v),.66,.22)+.08*bell(Math.abs(v),.93,.16);
  poly(points,{o:density,w:i%9===0?.76:.43,c:i%15===0?G:I});
 }
 out.push("</g>");
 // Segmented exegesis: lines are cross references with distinct endpoints,
 // rather than continuous hydrological flow.
 out.push(`<g id="scripture-sixty-six" aria-hidden="true">`);
 for(let b=0;b<66;b++){
  const q=(b+.5)/66,side=b%2===0?1:-1;
  const y=84+q*746,anchor=side>0?80:1520,termination=side>0?680:930;
  const yshift=(q-.5)*52+13*Math.sin((b+1)*1.3);
  const t0=side>0?0:1;
  for(let k=0;k<4;k++){
   const begin=anchor+(side>0?1:-1)*k*61;
   const end=termination+(side>0?1:-1)*(k%3)*43;
   const pts=[];
   for(let j=0;j<23;j++){
    const t=j/22,x=begin+(end-begin)*t;
    const yy=y+(t*t*(3-2*t))*yshift+(t*(1-t))*((b%5)-2)*20;
    pts.push(field(x,yy));
   }
   poly(pts,{o:.11+.095*(k===0?1:.46),w:.44,c:b%11===0?G:I,dash:k===3?"4 7":""});
  }
  if(b%3===0){
   const x=side>0?285:1330,[xx,yy]=field(x,y);
   segment(xx-4.4,yy-4.4,xx+4.4,yy+4.4,.28,.66,G);
  }
 }
 out.push("</g>");
 // Seven separate microscopic tonal beds; not a monolithic ribbon pattern.
 // Hatch orientation obeys the local tangent/normal of each bounded region.
 const beds=[
 [95,155,330,180,-.31],[610,175,400,160,.47],[1270,155,390,200,-.56],
 [155,680,370,220,.52],[560,690,450,170,-.45],[1030,680,480,185,.30],[1500,635,360,235,-.62]
 ];
 out.push(`<g id="micro-engraved-lenses" aria-hidden="true">`);
 for(let z=0;z<beds.length;z++){
  const [cx,cy,ww,hh,theta]=beds[z],tx=Math.cos(theta),ty=Math.sin(theta),nx=-ty,ny=tx;
  for(let j=0;j<138;j++){
   const u=(j+.5)/138*2-1,L=ww*(1-.34*Math.pow(Math.abs(u),1.7));
   const normal=u*hh*.49;
   let x1=cx-tx*L*.52+nx*normal,y1=cy-ty*L*.52+ny*normal;
   let x2=cx+tx*L*.48+nx*normal,y2=cy+ty*L*.48+ny*normal;
   // no hard rectangular hatch-block endings; stagger with bounded taper
   const trim=16*(.5+.5*Math.sin(j*.31+z*2.4));
   x1+=tx*trim;y1+=ty*trim;x2-=tx*trim*.6;y2-=ty*trim*.6;
   const warped=Array.from({length:9},(_,k)=>{
    const t=k/8,xx=x1+(x2-x1)*t,yy=y1+(y2-y1)*t;
    return field(xx,yy);
   });
   const shade=(.12+.21*bell(Math.abs(u),.47,.30))*(z%2===0?1:.83);
   poly(warped,{o:shade,w:j%11===0?.62:.38,c:z===2||z===4?P:I});
   if(j%5===0 && Math.abs(u)<.74){
    const x=cx+nx*normal,y=cy+ny*normal,s=6+9*(1-Math.abs(u));
    poly([field(x-tx*s*.75,y-ty*s*.75),field(x+tx*s*.25,y+ty*s*.25)],{o:.25,w:.38,c:I});
   }
  }
 }
 out.push("</g>");
 out.push(`<g id="gloss-marginalia" aria-hidden="true">`);
 // Quantized editorial index marks remain sparse; no celestial orbits.
 for(let i=0;i<126;i++){
  const x=28+(i*283)%1540,y=28+(i*173)%846;
  const [xx,yy]=field(x,y),u=(i%7);
  if(u===0){
   segment(xx-4,yy-5,xx+4,yy+5,.4,.62,G);
   segment(xx-5,yy+4,xx+5,yy-4,.2,.38,G);
  } else if(u===1||u===3){
   segment(xx-4,yy,xx+5,yy,.17,.53,I);
  } else if(u===4){
   segment(xx,yy-4,xx,yy+5,.23,.4,I);
  }
 }
 for(let edge=0;edge<4;edge++){
  for(let i=0;i<21;i++){
   const v=i/20;
   const a=edge===0?[0+v*1600,15,12+v*1600,15]:
     edge===1?[0+v*1600,885,12+v*1600,885]:
     edge===2?[15,0+v*900,15,12+v*900]:
     [1585,0+v*900,1585,12+v*900];
   segment(...a,.11,.55,G);
  }
 }
 out.push("</g></g></svg>");
 return {content:out.join("\n"), paths:n, brief:"No dark fills. ONE paper controlled by parent CSS; all edges active. Orthogonal manuscript-time field + spatial passage; no water flow, no black-hole singularity."};
}
process.stdout.write(buildEmmausV16().content);
