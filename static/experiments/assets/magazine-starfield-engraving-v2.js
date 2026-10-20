/**
 * Magazine Morning Star FULL-BLEED Engraving Field v2.
 * One deterministic, original SVG generator: paper/night + desktop/mobile.
 * Source: protected v5.3 Three.js star's exact 240 angular/length law and
 * eight-point principal directions. This expands those lines into a field;
 * it does not clone the 3D star or start an unrelated pattern.
 * No external packages, bitmap images, animation or additional Design OS.
 */
export function renderMagazineStarfield({theme='paper',format='desktop'}={}){
 const night=theme==='night',mobile=format==='mobile';
 const W=mobile?900:1600,H=mobile?1600:900;
 const cx=mobile?634:1200,cy=mobile?975:465,scale=mobile?149:173;
 const far=Math.hypot(Math.max(cx,W-cx),Math.max(cy,H-cy))+140;
 const PI=Math.PI,round=n=>Number(n.toFixed(2));
 const pos=(a,r,side=0)=>[cx+Math.cos(a)*r-Math.sin(a)*side,cy+Math.sin(a)*r+Math.cos(a)*side];
 const xy=p=>round(p[0])+' '+round(p[1]);
 const stroke=(a,b)=>'M'+xy(a)+'L'+xy(b);
 const gold=night?{ink:'#ffdf96',core:'#fff2cf',burin:'#d5b176',grain:'#f4d19b'}:
 {ink:'#805023',core:'#9b6629',burin:'#967047',grain:'#a47a46'};
 const full=[[],[],[],[],[]],rootStrokes=[],sourceRays=[],major=[],burin=[[],[],[]],granules=[],specks=[];
 // 240 protected v5.3 angular laws, expanded fourfold without modifying
 // their primary angles. Every extension travels past every viewport edge.
 for(let i=0;i<240;i++){
  const base=i*2*PI/240+.009*Math.sin(i*2.399963229728653);
  const inner=.69+(i%11)*.028,outer=2.42+(i%17)*.093+(i%11===0?.62:0);
  sourceRays.push(stroke(pos(base,scale*inner),pos(base,scale*outer)));
  for(let subdivision=0;subdivision<4;subdivision++){
   const a=base+subdivision*(2*PI/240/4);
   const r0=scale*(.68+(i%17)*.036)+(subdivision%3)*13;
   const r1=far+36+(i%7)*8;
   full[(i+subdivision*7)%5].push(stroke(pos(a,r0),pos(a,r1)));
   if(subdivision===0)rootStrokes.push(stroke(pos(a,4+(i%11)*2.8),pos(a,r0+5)));

  }
  if(i%3===0){
   const near=scale*(inner+.24),further=near+scale*(.31+(i%7)*.022);
   burin[0].push(stroke(pos(base,near),pos(base,further)));
  }
  if(i%4===0){
   const q=pos(base,scale*(outer+.14+(i%3)*.20));
   specks.push('<circle cx="'+round(q[0])+'" cy="'+round(q[1])+'" r="'+(i%8===0?1.15:.65)+'"/>');
  }
 }
 // Fine directional burin marks fill *every* editorial region, including
 // reading areas. They follow the source-derived radial direction field.
 const columns=mobile?20:36,rows=mobile?38:22;
 for(let gy=0;gy<rows;gy++)for(let gx=0;gx<columns;gx++){
  const stepX=W/columns,stepY=H/rows;
  const x=(gx+.5)*stepX,y=(gy+.5)*stepY;
  const dir=Math.atan2(y-cy,x-cx);
  for(let lane=0;lane<5;lane++){
   const offset=(lane-2)*3.1;
   const jitter=Math.sin((gx+1)*12.9898+(gy+3)*78.233+(lane+4)*19.713)*.45;
   const a=dir+((lane%2)?-.16:.13);
   const center=[x-Math.sin(dir)*offset+jitter*6,y+Math.cos(dir)*offset+jitter*5];
   const len=8+(gx*3+gy*5+lane*7)%16;
   const p0=[center[0]-Math.cos(a)*len*.46,center[1]-Math.sin(a)*len*.46];
   const p1=[center[0]+Math.cos(a)*len*.54,center[1]+Math.sin(a)*len*.54];
   burin[(gx+gy+lane)%3].push(stroke(p0,p1));
  }
  // Sparse ink pinpoints are part of the engraved field, not random stars.
  if((gx+gy*3)%7===0){
   const q=[x+(gx%3)*2,y+(gy%3)*1.8];
   granules.push('<circle cx="'+round(q[0])+'" cy="'+round(q[1])+'" r=".55"/>');
  }
 }
 // Eight faint anchor axes are aligned with the approved 3D star.
 for(let arm=0;arm<8;arm++){
  const base=-PI/2+arm*PI/4;
  for(let j=-9;j<=9;j++){
   const a=base+j*.0025+Math.sin((arm*31+j)*2.4)*.0005;
   const length=scale*(3.3+.04*(9-Math.abs(j)));
   major.push(stroke(pos(a,scale*(.97+(Math.abs(j)%3)*.09)),pos(a,length)));
  }
  major.push(stroke(pos(base,scale*.96),pos(base,far+35)));
 }
 const fGroups=full.map((group,i)=>'<path d="'+group.join('')+'" opacity="'+([.24,.21,.17,.19,.15][i])+'" stroke-width="'+([.58,.47,.42,.5,.4][i])+'"/>').join('');
 const bGroups=burin.map((group,i)=>'<path d="'+group.join('')+'" opacity="'+([.24,.18,.13][i])+'" stroke-width="'+([.52,.48,.44][i])+'"/>').join('');
 const desc='Full-bleed transparent engraving from the approved v5.3 Morning Star 240 filaments and 8 tip axes. Continuous radial engraving reaches all four corners; microscopic burin cuts exist beneath text as well. No cutout mask, bitmap, or animation.';
 return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 '+W+' '+H+'" preserveAspectRatio="xMidYMid slice" data-asset="magazine-starfield-engraving-v2" data-origin="morning-star-v5.3" data-coverage="full-bleed" data-format="'+(mobile?'mobile':'desktop')+'" data-theme="'+(night?'night':'paper')+'">\n'+
 '<title>Westside Magazine — Morning Star Full-Bleed Engraving v2 / '+(night?'night':'paper')+' / '+(mobile?'mobile':'desktop')+'</title>\n'+
 '<desc>'+desc+'</desc>\n'+
 '<defs><clipPath id="full-crop"><rect x="0" y="0" width="'+W+'" height="'+H+'"/></clipPath></defs>\n'+
 '<g clip-path="url(#full-crop)" fill="none" stroke-linecap="round">\n'+
 '<g id="full-surface-intaglio" stroke="'+gold.ink+'">'+fGroups+'</g>\n'+
 '<g id="inner-source-continuity" stroke="'+gold.ink+'"><path d="'+rootStrokes.join('')+'" opacity=".085" stroke-width=".48"/></g>\n'+
 '<g id="approved-240-rays" stroke="'+gold.ink+'"><path d="'+sourceRays.join('')+'" opacity=".26" stroke-width=".60"/></g>\n'+
 '<g id="eight-point-origin-axes" stroke="'+gold.core+'"><path d="'+major.join('')+'" opacity=".22" stroke-width=".58"/></g>\n'+
 '<g id="all-surface-burin" stroke="'+gold.burin+'">'+bGroups+'</g>\n'+
 '<g id="engraved-ink-dust" fill="'+gold.grain+'" stroke="none" opacity=".31">'+granules.join('')+specks.join('')+'</g>\n'+
 '</g>\n</svg>';
}
