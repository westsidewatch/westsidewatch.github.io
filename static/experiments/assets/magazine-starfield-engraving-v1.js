/**
 * Magazine Morning Star Engraving Field v1, original deterministic SVG generator.
 * Source geometry: protected Morning Star 3D Lab v5.3. This generator
 * projects (not duplicates) its 240 filament angular law and eight major axes
 * into an editorial, text-safe directional field. No DOM, external packages,
 * animation, bitmap, or additional design system.
 * Palette is an immutable-art trial; the Lab's backgrounds use Design OS.
 */
export function renderMagazineStarfield(options={}){
 const theme=options.theme==='night'?'night':'paper';
 const colors=theme==='night'
 ?{fine:'#ffdf96',major:'#fff2cf',hatch:'#d5b176',dust:'#f4d19b'}
 :{fine:'#805023',major:'#9b6629',hatch:'#967047',dust:'#a47a46'};
 const W=1600,H=900,cx=1270,cy=445,k=178,PI=Math.PI;
 const f=n=>Number(n.toFixed(2)),q=(x,y)=>`${f(x)} ${f(y)}`;
 const point=(a,r,lateral=0)=>[cx+Math.cos(a)*r-Math.sin(a)*lateral,cy+Math.sin(a)*r+Math.cos(a)*lateral];
 const line=(p0,p1)=>`M ${q(...p0)} L ${q(...p1)}`;
 const rays=[],major=[],engrave=[],dust=[],spark=[];
 // The exact eight-armed and 240-filament angular laws are inherited from
 // Morning Star 3D Lab v5.3. Only the viewBox projection and editorial
 // attenuation differ. This is not a new competing star drawing.
 for(let i=0;i<240;i++){
  const a=i*2*PI/240 + .009*Math.sin(i*2.399963229728653);
  const inner=.69+(i%11)*.028,outer=2.42+(i%17)*.093+(i%11===0?.62:0);
  const p0=point(a,k*inner),p1=point(a,k*outer);
  const strong=i%13===0,op=f(strong?.40:.16+(i%7)*.019);
  rays.push(`<path d="${line(p0,p1)}" stroke="${colors.fine}" stroke-width="${strong?1.04:.54}" opacity="${op}"/>`);
  // A small internal burin cut makes each filament a stroke with direction
  // and tonal hierarchy, not a uniform spoke wheel.
  if(i%3===0){
   const r=k*(inner+.20),to=k*(inner+.55+(i%5)*.075);
   engrave.push(`<path d="${line(point(a,r),point(a,to))}" stroke="${colors.hatch}" stroke-width=".56" opacity="${f(.20+(i%4)*.07)}"/>`);
  }
  if(i%4===0){
   const r=k*(outer-(i%5)*.16),p=point(a,r,(i%3-1)*.75);
   dust.push(`<circle cx="${f(p[0])}" cy="${f(p[1])}" r="${i%12===0?1.16:.65}" fill="${colors.dust}" opacity="${f(.19+(i%5)*.055)}"/>`);
  }
 }
 // Eight principal directions from the approved star; line-bundles are
 // asymmetrically spaced, avoiding the detached 'brush/feather' failure.
 for(let arm=0;arm<8;arm++){
  const a=-PI/2+arm*PI/4;
  for(let j=-14;j<=14;j++){
   if(j===0)continue;
   const aj=a+j*.00325+Math.sin((j+arm*7)*2.4)*.0008;
   const from=1.04+.055*(Math.abs(j)%5),length=2.67+.075*(14-Math.abs(j))+.09*((arm+j+56)%4);
   const near=point(aj,k*from),far=point(aj,k*(from+length));
   major.push(`<path d="${line(near,far)}" stroke="${j%6===0?colors.major:colors.hatch}" stroke-width="${Math.abs(j)<4?.77:.43}" opacity="${f((.24-.008*Math.abs(j))*(theme==='night'?1.1:1.0))}"/>`);
  }
  // Long, precisely tapered point along each principal beam, as a field
  // extension of the 3D star's existing tip-anchored ribbon geometry.
  const p0=point(a,k*1.08),p1=point(a,k*3.95),p2=point(a,k*4.42);
  major.push(`<path d="${line(p0,p1)}" stroke="${colors.major}" stroke-width="1.22" opacity="${theme==='night'?.62:.49}"/>`);
  major.push(`<path d="${line(p1,p2)}" stroke="${colors.major}" stroke-width=".46" opacity=".31"/>`);
  // Short off-axis etched cuts engraved into the main ray, not circular rings.
  for(let j=0;j<18;j++){
   const rr=k*(1.18+j*.135),lateral=(j%2===0?1:-1)*(2+(j%3)*1.4);
   const p=point(a,rr,lateral),pp=point(a,rr+9,lateral*.34);
   engrave.push(`<path d="${line(p,pp)}" stroke="${colors.hatch}" stroke-width=".43" opacity=".23"/>`);
  }
 }
 // Sparse four-point engraved glints, derived from the same radial ray ends,
 // never repeated standalone stars, circular halos or photographic textures.
 for(let i=0;i<12;i++){
  const a=(i*19+7)*2*PI/240,k0=2.78+(i%5)*.22;
  const [x,y]=point(a,k*k0);
  const l=2.6+(i%3)*1.3,w=.54;
  spark.push(`<path d="M ${q(x,y-l)} L ${q(x+w,y-w)} L ${q(x+l,y)} L ${q(x+w,y+w)} L ${q(x,y+l)} L ${q(x-w,y+w)} L ${q(x-l,y)} L ${q(x-w,y-w)} Z" fill="${colors.major}" opacity="${theme==='night'?.52:.39}"/>`);
 }
 const meta=`Magazine Morning Star Engraving Field v1 / source Morning Star v5.3, 240 light filaments, 8 tip axes / theme ${theme}`;
 return `<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 ${W} ${H}" preserveAspectRatio="xMidYMid slice" data-asset="magazine-morning-star-engraving-v1" data-origin="morning-star-v5.3" data-theme="${theme}">
<title>${meta}</title>
<desc>Transparent standalone SVG editorial underlay, projected from the approved 3D morning star's 240 rays and eight tip axes. The left reading area softly fades. No embedded bitmap and no animation.</desc>
<defs>
 <linearGradient id="text-safe-fade" gradientUnits="userSpaceOnUse" x1="0" x2="${W}" y1="0" y2="0">
 <stop offset="0" stop-color="white" stop-opacity=".015"/>
 <stop offset=".34" stop-color="white" stop-opacity=".035"/>
 <stop offset=".47" stop-color="white" stop-opacity=".095"/>
 <stop offset=".58" stop-color="white" stop-opacity=".31"/>
 <stop offset=".72" stop-color="white" stop-opacity=".84"/>
 <stop offset="1" stop-color="white" stop-opacity=".96"/>
 </linearGradient>
 <mask id="reading-safe" maskUnits="userSpaceOnUse" x="0" y="0" width="${W}" height="${H}"><rect width="${W}" height="${H}" fill="url(#text-safe-fade)"/></mask>
 <clipPath id="stage-clip"><rect width="${W}" height="${H}"/></clipPath>
</defs>
<g clip-path="url(#stage-clip)" mask="url(#reading-safe)" stroke-linecap="round" fill="none">
 <g id="240-source-filaments">${rays.join('')}</g>
 <g id="eight-axis-intaglio">${major.join('')}</g>
 <g id="directional-burin-cuts">${engrave.join('')}</g>
 <g id="micro-stipple">${dust.join('')}</g>
 <g id="small-light-glints">${spark.join('')}</g>
</g>
</svg>`;
}
