// Westside P2 Emmaus V17 / original native SVG engraving — no dependencies.
// Generate with: node scripts/build-emmaus-engraving-v17.mjs > static/images/p2-emmaus-time-held-open-v17.svg
function buildV17(){
const W=1600,H=900,ink='#102a43',ink2='#334d54',gold='#a2872a',paper='#ded096';
const out=[], f=n=>Math.round(n*100)/100;
const clamp=(v,a,b)=>Math.min(b,Math.max(a,v));
const g=(v,c,s)=>Math.exp(-Math.pow((v-c)/s,2));
const polar=(t,rx,ry,p=3.75,off=0)=>{
 let a=t+off,C=Math.cos(a),S=Math.sin(a),q=2/p;
 let x=800+rx*Math.sign(C)*Math.pow(Math.abs(C),q), y=450+ry*Math.sign(S)*Math.pow(Math.abs(S),q);
 x+=22*S*Math.cos(a*1.3);y+=12*C*Math.sin(a*.8);
 return [x,y];
};
let count=0;
const draw=(pts,opacity=.3,w=.65,color=ink,dash='')=>{
 if(pts.length<2)return;count++;
 out.push(`<path d="M${pts.map(([x,y])=>`${f(x)} ${f(y)}`).join(' L')}" stroke="${color}" stroke-opacity="${f(opacity)}" stroke-width="${f(w)}"${dash?` stroke-dasharray="${dash}"`:''}/>`);
};
const ln=(x,y,X,Y,o=.3,w=.6,c=ink,d='')=>draw([[x,y],[X,Y]],o,w,c,d);
const arc=(t0,t1,rx,ry,step=85,p=3.75,off=0)=>Array.from({length:step+1},(_,i)=>polar(t0+(t1-t0)*i/step,rx,ry,p,off));
const ellipseBandPath=(rx,ry,p=3.75)=>'M'+arc(0,2*Math.PI,rx,ry,240,p).map(([x,y])=>`${f(x)},${f(y)}`).join(' L')+' Z';
out.push(`<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900" fill="none" role="img" aria-labelledby="title desc"><title id="title">EMMAUS / V17 — TIME HELD OPEN</title><desc id="desc">Intaglio field derived from an open editorial aperture, scripture concordance and layered time. Luke 24:27; 2 Peter 3:8. No literal scroll, flow-field or wormhole. Native SVG only.</desc><metadata>Westside Design OS / ONE paper #ded096, ink #102a43, accent #a2872a. Not approved. Measured Magazine geometry defines the actual aperture in P2; this vector field is clipped by the existing runtime.</metadata><rect width="1600" height="900" fill="${paper}"/>`);
out.push(`<defs><clipPath id="bound"><rect width="1600" height="900"/></clipPath><clipPath id="ink-belt" clipPathUnits="userSpaceOnUse"><path fill-rule="evenodd" d="M0 0 H1600 V900 H0 Z ${ellipseBandPath(535,322)}"/></clipPath></defs><g stroke-linecap="round" stroke-linejoin="round" clip-path="url(#bound)">`);
out.push('<g id="time-sectioned-aperture">');
for(let k=0;k<53;k++){
 const v=k/52,rx=520+400*v,ry=288+300*v,p=3.7+(.25*Math.sin(k/10));
 const depth=(.18+.26*g(v,.27,.16)+.16*g(v,.83,.18));
 const w=k%11===0?1.13:.38+.15*g(v,.3,.24);
 const off=.005*Math.sin(k*.27);
 const spans=[[-.12,.86],[1.04,1.56],[1.76,2.89],[3.09,4.47],[4.64,5.18],[5.31,6.26]];
 for(let h=0;h<spans.length;h++){
  let [a,b]=spans[h];const d=.018*Math.sin(k*.33+h*.45);
  const points=arc(a+d,b+d,rx,ry,58,p,off);
  draw(points,depth*(k%5===0?1.3:.85),w,h===1||h===4?ink2:ink);
 }
}
out.push('</g>');
out.push('<g id="pressed-plate-highlights">');
for(const [layer,rx,ry,o] of [[0,550,308,.43],[1,570,325,.60],[2,603,351,.32],[3,671,395,.26]]){
 for(const [a,b] of [[3.47,4.83],[5.14,6.22],[.16,1.43],[1.88,2.98]]){
  const span=.03*Math.sin(layer*2+a);
  draw(arc(a+span,b+span,rx,ry,79,3.83),o*(layer%2?1:.8),layer===1?1.28:.80,layer===1?ink:gold);
 }
}
for(const [side,lo,hi] of [['northwest',3.54,4.36],['northeast',4.77,5.63],['southeast',.12,.93],['southwest',2.08,2.99]]){
 for(let i=0;i<110;i++){
  const u=(i+.5)/110,t=lo+(hi-lo)*u;
  const r=558+86*u,ry=315+94*u;
  const a=polar(t,r,ry,3.86),b=polar(t+.03+u*.018,r+94,ry+85,3.86);
  const op=.12+.30*g(u,.48,.32);
  draw([a,b],op,i%17===0?.88:.42,i%13===0?gold:ink);
 }
}
out.push('</g>');
out.push('<g id="engraved-distance-registers">');
const quadrants=[[-.73,-.33],[.25,.72],[1.2,1.73],[2.37,2.89],[3.18,3.7],[4.19,4.7],[5.05,5.53]];
for(let group=0;group<quadrants.length;group++){
 const [a,b]=quadrants[group];
 for(let j=0;j<83;j++){
  const s=(j+.5)/83,t=a+(b-a)*s;
  const n=(.1+.8*((j*31)%83)/83),r1=512+430*n,r2=512+470*n;
  const p0=polar(t,r1,285+288*n),p1=polar(t+.08,r2+13,305+300*n);
  const mid=polar(t+.045,(r1+r2)/2,(590+588*n)/2);
  draw([p0,mid,p1],.14+.19*g(s,.37,.22),.34+(j%17===0?.26:0),group%3===0?gold:ink2);
  if(j%4===0){let x=mid[0],y=mid[1];ln(x-5,y-4,x+5,y+4,.23,.51,ink)}
 }
}
out.push('</g>');
out.push('<g id="sixty-six-canonical-cross-references">');
for(let book=0;book<66;book++){
 const q=(book+.5)/66,branch=book%4;
 const x=34+q*1532,y=35+q*830;
 let start,end,phase;
 if(branch===0){ start=[x,-65];end=[x-70+48*Math.sin(book*1.7),204];phase=0; }
 else if(branch===1){start=[x,955];end=[x+70-42*Math.sin(book),684];phase=1;}
 else if(branch===2){start=[-55,y];end=[315,y-45+25*Math.sin(book*.5)];phase=2;}
 else {start=[1655,y];end=[1285,y+35+32*Math.sin(book*.65)];phase=3;}
 const wig=17*Math.sin(book*.91),p1=[start[0]+(end[0]-start[0])*.41+wig,start[1]+(end[1]-start[1])*.41];
 const p2=[start[0]+(end[0]-start[0])*.76-wig*.4,start[1]+(end[1]-start[1])*.76];
 draw([start,p1,p2,end],.17+(book%11===0?.19:0),book%7===0?.8:.48,book%11===0?gold:ink);
 const [xx,yy]=end; ln(xx-5,yy,xx+5,yy,.42,.82,book%11===0?gold:ink);
 ln(xx,yy-3,xx,yy+3,.27,.48,ink);
 if(book%3===0){const t=[start[0]*.28+end[0]*.72,start[1]*.28+end[1]*.72];ln(t[0]-7,t[1],t[0]+7,t[1],.22,.46,ink2)}
}
out.push('</g>');
out.push('<g id="time-plate-crosshatch" clip-path="url(#ink-belt)">');
for(const [sector,lo,hi] of [['upper',3.70,5.75],['right',5.63,6.78],['lower',.55,2.53],['left',2.39,3.94]]){
 for(let band=0;band<92;band++){
  const v=(band+.5)/92,rx=510+340*v,ry=289+302*v;
  const ps=arc(lo,hi,rx,ry,55,3.7);
  const opacity=(.11+.35*g(v,.32,.23)+.13*g(v,.78,.11))*(sector==='left'?.94:1);
  draw(ps,opacity,band%11===0?.78:.43,band%9===0?gold:ink);
 }
 for(let j=0;j<67;j++){
  const t=lo+(hi-lo)*(j+.5)/67;
  const p0=polar(t,575,328,3.7),p1=polar(t+.017,740,478,3.7);
  draw([p0,p1],.13+.29*g((j+.5)/67,.55,.33),.44,ink2);
 }
}
out.push('</g>');
out.push('<g id="editorial-chapter-indexing">');
const ticks=(x0,y0,dx,dy,n,step)=>{
 for(let j=0;j<n;j++){
  const major=j%11===0,len=major?13:j%5===0?9:4;
  const x=x0+j*step*dx,y=y0+j*step*dy;
  ln(x,y,x-dy*len,y+dx*len,major?.5:.23,major?.82:.5,major?gold:ink);
 }
};
ticks(26,42,1,0,79,19.8);ticks(26,861,1,0,79,19.8);
ticks(35,26,0,1,42,20);ticks(1562,26,0,1,42,20);
for(let i=0;i<14;i++){
 const yy=55+i*56;let xa=50+i*1.4,xb=1550-i*1.9;
 if(i%2===0){
  ln(xa-5,yy,xa+17,yy,.3,.7,gold);
  ln(xb-17,yy,xb+5,yy,.3,.7,gold);
 }
}
out.push('</g></g></svg>');
return {svg:out.join('\n'),paths:count};
}
process.stdout.write(buildV17().svg);
