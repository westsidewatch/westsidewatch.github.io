/* Build-time vector poster generator for Westside Watch P2 Vol.00.
 * Copyright (c) 2026 Westside Watch. SVG output only; no runtime dependencies.
 * B's glyph contour seed is derived from OFL-1.1 Noto Sans CJK; see
 * https://github.com/notofonts/noto-cjk/blob/main/Sans/LICENSE.
 * The shapes for A are independently constructed original vector geometry.
 * B uses deterministic curve/radial/halftone/contour/hatch/cross/concentric
 * SVG geometry algorithms from the open generative-graphics family; no
 * third-party UI framework is loaded at runtime.
 */
import {mkdirSync,writeFileSync} from 'node:fs';
const XI="M26 70V125H328.6V176.3H79.8V488H202.1V461H808.4V487.1H937.1V176.3H673.5V125H974V70ZM202.1 408.3V337.6C219 346.1 235.8 356.1 244.3 362.3C394 331.4 434.1 278.8 440.4 228.9H553.3V279.2C553.3 333.8 576.5 349.5 687.2 349.5C709.3 349.5 778.9 349.5 802.1 349.5H808.4V408.3ZM202.1 314.8V228.9H327.6C322.3 260.7 298.1 291.6 202.1 314.8ZM441.5 176.3V125H553.3V176.3ZM673.5 228.9H808.4V295.8C804.2 296.3 799 296.8 789.5 296.8C774.7 296.8 717.8 296.8 706.2 296.8C676.6 296.8 673.5 294.9 673.5 279.2Z";
const WANG="M610.8 524.7C585.5 551 543 579.6 482.3 604.5V566.9H343.7C331.5 552.8 315.4 535.6 299.2 522L190.9 535.6C201 545.1 211.1 556 220.3 566.9H26V612.7H102.9V675.8C102.9 723.4 131.2 740.6 243.5 740.6C262.7 740.6 350.8 740.6 375.1 740.6C408.4 740.6 444.9 740.2 464.1 737C459 725.2 456 705.2 454 692.5C433.7 694.4 396.3 695.3 372 695.3C349.8 695.3 263.8 695.3 243.5 695.3C218.2 695.3 213.2 690.7 213.2 676.7V612.7H462.1C444.9 619.1 427.7 625 408.4 630.4C435.8 637.2 473.2 653.1 491.4 664.4L521.8 654C552.1 668 583.5 683.5 605.7 696.2C565.3 704.3 520.7 710.2 472.2 714.3C492.4 724.3 516.7 742.4 528.8 755.1C755.5 730.2 912.3 679.4 974 564.2L900.1 552.8L878.9 554.7H701.8L726.1 533.3ZM844.5 740.6C656.3 755.6 357.9 764.2 99.9 766C110 777.8 123.1 796.4 124.1 809.6C222.3 809.6 327.5 808.2 431.7 805.9V830H98.8V873.1H431.7V897.6H43.2V942H946.7V897.6H555.1V873.1H898.1V830H555.1V802.8C678.6 798.7 796.9 792.8 895.1 784.6ZM606.7 616.8C651.3 631.3 697.8 647.6 730.2 661.2C717 666.7 701.8 672.1 685.7 676.7C657.3 662.2 617.9 644 582.5 629ZM785.8 633.6C752.4 621.3 710.9 607.7 672.5 595.9H832.4C819.2 609.5 804 622.2 785.8 633.6Z";
const PALETTE=[{"name":"LIVING WATER","token":"--ws-water","hex":"#5b8fa8","family":"FLOW"},{"name":"VOL.00 / FIRST LIGHT","token":"--ws-first-light","hex":"#a2872a","family":"RADIAL"},{"name":"EMMAUS / SCRIPTURE","token":"--ws-pale-gold","hex":"#cebd74","family":"HALFTONE"},{"name":"OLIVE MOUNTAIN","token":"--ws-olive","hex":"#738a5a","family":"CONTOUR"},{"name":"DAWN LIBRARY","token":"--ws-harvest","hex":"#b8944a","family":"HATCH"},{"name":"CINEMA","token":"--ws-crimson","hex":"#a14d57","family":"CROSSHATCH"},{"name":"DAYLIGHT CAFE","token":"--ws-daylight-mauve","hex":"#b085ab","family":"CONCENTRIC"}];
const xml=s=>s.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
const p2=(n)=>Number(n).toFixed(2);
function makeA(){
  const ink="#102a43",gold="#a2872a",paper="#eee6d8";
  const XiShape=[
   "M50 72H948L917 142H77Z", 
   "M127 190H873V463H127ZM243 265V384H757V265Z",
   "M367 209H490Q470 292 427 334Q389 377 288 391H227Q331 319 367 209Z",
   "M531 209H633V306Q633 351 703 351H786V396H696Q531 396 531 308Z"
  ];
  const WangShape=[
   "M236 502L355 532L311 575L204 545Z",
   "M75 582L484 566L456 626H94Z",
   "M112 617H226L211 703Q271 720 462 682L485 737Q349 797 154 774Q112 763 112 713Z",
   "M511 570H923V779H820V626H617V779H511Z",
   "M637 659H813V689H637Z",
   "M637 720H813V749H637Z",
   "M91 801H931L896 841H117Z",
   "M448 811H555V936H448Z",
   "M159 866H871L851 901H175Z",
   "M52 927H950L935 966H68Z"
  ];
  // Shapes and structural negatives are hand drawn; no old font silhouette
  // or automatic geometric 'slashes' applied to a pre-existing glyph.
  const holes=`<path d="M643 646H818V696H643Z M643 707H818V744H643Z" fill="${paper}"/>`;
  const edges=`<g fill="none" stroke="${gold}" stroke-width="1.6" opacity=".70"><path d="M24 49H190 M807 49H976 M24 980H206 M794 980H976"/></g>`;
  return `<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="1000" viewBox="0 0 1000 1000" role="img" aria-labelledby="aTitle aDesc">
<title id="aTitle">西望 — Geometry / Campaign A2</title>
<desc id="aDesc">Two monumental, individually constructed Traditional Chinese characters. Modern geometric editorial poster. No brush lettering or illustration.</desc>
<rect width="1000" height="1000" fill="${paper}"/>
<g fill="${ink}" data-word="西" data-authority="original-geometry" shape-rendering="geometricPrecision">
${XiShape.map((d,i)=>`<path data-construct="${i}" d="${d}" ${i===1?'fill-rule="evenodd"':''}/>`).join("\n")}
</g>
<g fill="${ink}" data-word="望" data-authority="original-geometry" shape-rendering="geometricPrecision">
${WangShape.map((d,i)=>`<path data-construct="${i}" d="${d}"/>`).join("\n")}
</g>
${holes}
${edges}
<g font-family="Georgia,serif" font-size="12" fill="${gold}" letter-spacing="2" aria-hidden="true">
<text x="23" y="34">WESTSIDE WATCH / VOL.00</text>
<text x="976" y="34" text-anchor="end">TYPE AS CAMPAIGN</text>
<text x="23" y="991">WATCH FOR THE DAWN</text>
<text x="976" y="991" text-anchor="end">ROMANS 13:12</text>
</g>
</svg>`;
}
function texture(index,color){
  let out=[];
  if(index===0){ // FLOW: undulating lines change amplitude with location.
    for(let i=0;i<45;i++){let y=i*6.4;let amp=12+7*Math.sin(i*.35);out.push(`<path d="M-25 ${p2(y)} C 145 ${p2(y-amp)} 320 ${p2(y+amp)} 465 ${p2(y)} S 720 ${p2(y-amp)} 940 ${p2(y)}"/>`);}
  }else if(index===1){ // RADIAL: 104 genuine diverging engraved rays.
    for(let i=0;i<112;i++){let a=i*Math.PI*2/112,r1=18+(i%4)*8,r2=950;let x=450,y=135;out.push(`<path d="M${p2(x+Math.cos(a)*r1)} ${p2(y+Math.sin(a)*r1)} L${p2(x+Math.cos(a)*r2)} ${p2(y+Math.sin(a)*r2)}"/>`);}
  }else if(index===2){ // HALFTONE: hex stagger and variable dot diameter.
    for(let r=0;r<15;r++)for(let c=0;c<43;c++){let x=13+c*21+(r%2)*10.5,y=11+r*19;let radius=2.1+2.6*(.5+.5*Math.sin(c*.32+r*.46));out.push(`<circle cx="${p2(x)}" cy="${p2(y)}" r="${p2(radius)}" fill="${color}" stroke="none"/>`);}
  }else if(index===3){ // CONTOUR: concentric quasi-topographic Bézier field.
    for(let i=0;i<58;i++){let y=3+i*5.3;let shift=30*Math.sin(i*.13);out.push(`<path d="M-20 ${p2(y)} C 130 ${p2(y+shift)} 235 ${p2(y-shift*1.6)} 360 ${p2(y)} S 660 ${p2(y+shift)} 930 ${p2(y-shift*.4)}"/>`);}
  }else if(index===4){ // HATCH: deep diagonal engraving with two density zones.
    for(let i=-440;i<1300;i+=12){out.push(`<path d="M${i} 305 l320 -315"/>`);}
    for(let i=-390;i<1300;i+=19){out.push(`<path d="M${i} 305 l250 -195" opacity=".46"/>`);}
  }else if(index===5){ // CROSSHATCH: two directional fields, editorial interference.
    for(let i=-440;i<1280;i+=17)out.push(`<path d="M${i} 310 l330 -330"/>`);
    for(let i=-350;i<1350;i+=23)out.push(`<path d="M${i} -20 l360 330" opacity=".64"/>`);
  }else if(index===6){ // CONCENTRIC: 73 circular engravings & elliptical cross contours.
    for(let r=11;r<730;r+=13)out.push(`<circle cx="472" cy="148" r="${r}" />`);
    for(let r=18;r<430;r+=27)out.push(`<ellipse cx="630" cy="190" rx="${r}" ry="${p2(r*.36)}" opacity=".47"/>`);
  }
  return `<g fill="none" stroke="${color}" stroke-width="${index===2?0:index===5?5.3:5.7}" stroke-linecap="round">${out.join("")}</g>`;
}
function makeB(){
  const navy="#0f1927",paper="#f2ead9",gold="#a2872a";
  // An independent B lettering base: modular 2-character pairing from
  // licensed Noto CJK outlines, NOT A's custom geometric shapes.
  const glyphs=`<g data-outline="西" transform="translate(12 8) scale(.45 .61) translate(-26 -70)"><path d="${XI}"/></g><g data-outline="望" transform="translate(466 8) scale(.45 .61) translate(-26 -522)"><path d="${WANG}"/></g>`;
  const layout=[
   {x:45,y:105,w:618,h:214},
   {x:693,y:104,w:262,h:103},
   {x:51,y:366,w:532,h:188},
   {x:612,y:356,w:340,h:133},
   {x:43,y:601,w:466,h:170},
   {x:560,y:585,w:388,h:157},
   {x:328,y:810,w:620,h:141}
  ];
  let defs="",groups="";
  for(let i=0;i<7;i++){
   const p=PALETTE[i],l=layout[i],id=`xw-b2-ink-${i+1}`;
   defs+=`<pattern id="${id}" patternUnits="userSpaceOnUse" width="900" height="315"><g>${texture(i,p.hex)}</g></pattern>`;
   const transform=`translate(${l.x} ${l.y}) scale(${p2(l.w/900)} ${p2(l.h/300)})`;
   const positionTextX=l.x,positionTextY=l.y+l.h+15;
   // Faint color underprint guarantees glyph legibility at small mobile sizes,
   // while actual lines/dots produce the main visual mass.
   groups+=`<g data-poster-word="${i+1}" data-engraving-family="${p.family}" data-ws-token="${p.token}" data-color="${p.hex}" transform="${transform}">
    <g fill="${p.hex}" opacity=".14">${glyphs}</g>
    <g fill="url(#${id})">${glyphs}</g>
    <g fill="none" stroke="${p.hex}" stroke-width="1.9" opacity=".47">${glyphs}</g>
   </g>
   <text x="${positionTextX}" y="${positionTextY}" font-family="Georgia,serif" font-size="10" letter-spacing="1.35" fill="${p.hex}">${String(i+1).padStart(2,"0")}  /  ${xml(p.name)}  —  ${p.family}</text>`;
  }
  return `<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="1000" viewBox="0 0 1000 1000" role="img" aria-labelledby="bTitle bDesc">
<title id="bTitle">西望 × 7 — Engraved Campaign B2</title>
<desc id="bDesc">Seven distinct typographic Westside Watch wordgroups, each corresponding to a section's Design OS color and a separate true SVG engraving system.</desc>
<defs>${defs}</defs>
<rect width="1000" height="1000" fill="${navy}"/>
<path d="M24 57H976 M24 979H976" fill="none" stroke="${gold}" stroke-width="1" opacity=".65"/>
<g fill="${paper}" font-family="Georgia,serif" font-size="13" letter-spacing="1.8">
<text x="25" y="37">WESTSIDE WATCH / VOL.00</text>
<text x="975" y="37" text-anchor="end">SEVEN FIELDS / ONE MAGAZINE</text>
</g>
${groups}
<g fill="${gold}" font-family="Georgia,serif" font-size="11" letter-spacing="1.5">
<text x="27" y="950">SEVEN</text>
<text x="27" y="966">FOLDS</text>
<text x="975" y="992" text-anchor="end">WATCH FOR THE DAWN · ROMANS 13:12</text>
</g>
</svg>`;
}
const out='static/images';
mkdirSync(out,{recursive:true});
writeFileSync(out+'/xiwang-poster-a-v2.svg',makeA(),'utf8');
writeFileSync(out+'/xiwang-poster-b-v2.svg',makeB(),'utf8');
console.log('Generated A two-character and B seven-word SVG posters.');