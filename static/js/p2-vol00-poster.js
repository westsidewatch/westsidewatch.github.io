/* Vol.00 A/B poster studies + seven genuine homepage-style folds.
   Same Design OS palette as first-look-host.js, no new animation clock.
   SVG lettering uses OS CJK display face (geometric, not brushwork).
   This is a revisable TYPE STUDY; the final custom outlined glyph master
   requires visual review. Right cover and Homepage remain untouched. */
(()=>{'use strict';
 const stage=document.getElementById('dual-stage'),tile=document.getElementById('dual-contents');
 if(!stage||!tile)return;
 const query=new URLSearchParams(location.search);
 // Explicit archived visual baseline for original Vol.00 regression only.
 if(query.get('poster')==='legacy')return;
 const mode=query.get('poster')?.toLowerCase()==='b'?'b':'a';
 stage.dataset.p2Poster=mode;
 document.documentElement.dataset.p2Poster=mode;
 const colors=['--ws-water','--ws-first-light','--ws-pale-gold','--ws-olive','--ws-harvest','--ws-crimson','--ws-daylight-mauve'];
 const svg=document.createElementNS('http://www.w3.org/2000/svg','svg');
 svg.classList.add('xw-poster__art');
 svg.setAttribute('viewBox','0 0 1000 1000');
 svg.setAttribute('preserveAspectRatio','xMidYMid meet');
 svg.setAttribute('aria-hidden','true');
 // True vector outlines of Traditional Chinese 西 / 望, constructed from
 // SIL OFL 1.1 Noto Sans CJK TC Bold glyphs and optically fitted to 1:1 folio.
 // Do not use SVG <text> inside clipPath/mask: browser rendering was blank.
 const glyphs='<g class="xw-poster__big-type">'+
  '<path data-glyph="xi" d="M26 70V125H328.6V176.3H79.8V488H202.1V461H808.4V487.1H937.1V176.3H673.5V125H974V70ZM202.1 408.3V337.6C219 346.1 235.8 356.1 244.3 362.3C394 331.4 434.1 278.8 440.4 228.9H553.3V279.2C553.3 333.8 576.5 349.5 687.2 349.5C709.3 349.5 778.9 349.5 802.1 349.5H808.4V408.3ZM202.1 314.8V228.9H327.6C322.3 260.7 298.1 291.6 202.1 314.8ZM441.5 176.3V125H553.3V176.3ZM673.5 228.9H808.4V295.8C804.2 296.3 799 296.8 789.5 296.8C774.7 296.8 717.8 296.8 706.2 296.8C676.6 296.8 673.5 294.9 673.5 279.2Z"/>'+
  '<path data-glyph="wang" d="M610.8 524.7C585.5 551 543 579.6 482.3 604.5V566.9H343.7C331.5 552.8 315.4 535.6 299.2 522L190.9 535.6C201 545.1 211.1 556 220.3 566.9H26V612.7H102.9V675.8C102.9 723.4 131.2 740.6 243.5 740.6C262.7 740.6 350.8 740.6 375.1 740.6C408.4 740.6 444.9 740.2 464.1 737C459 725.2 456 705.2 454 692.5C433.7 694.4 396.3 695.3 372 695.3C349.8 695.3 263.8 695.3 243.5 695.3C218.2 695.3 213.2 690.7 213.2 676.7V612.7H462.1C444.9 619.1 427.7 625 408.4 630.4C435.8 637.2 473.2 653.1 491.4 664.4L521.8 654C552.1 668 583.5 683.5 605.7 696.2C565.3 704.3 520.7 710.2 472.2 714.3C492.4 724.3 516.7 742.4 528.8 755.1C755.5 730.2 912.3 679.4 974 564.2L900.1 552.8L878.9 554.7H701.8L726.1 533.3ZM844.5 740.6C656.3 755.6 357.9 764.2 99.9 766C110 777.8 123.1 796.4 124.1 809.6C222.3 809.6 327.5 808.2 431.7 805.9V830H98.8V873.1H431.7V897.6H43.2V942H946.7V897.6H555.1V873.1H898.1V830H555.1V802.8C678.6 798.7 796.9 792.8 895.1 784.6ZM606.7 616.8C651.3 631.3 697.8 647.6 730.2 661.2C717 666.7 701.8 672.1 685.7 676.7C657.3 662.2 617.9 644 582.5 629ZM785.8 633.6C752.4 621.3 710.9 607.7 672.5 595.9H832.4C819.2 609.5 804 622.2 785.8 633.6Z"/></g>';
 const meta='<g class="xw-poster__metadata"><text x="25" y="24">WESTSIDE WATCH / VOL.00</text>'+
  '<text x="975" y="24" text-anchor="end">2026 · POSTER SERIES</text>'+
  '<text x="25" y="992">WATCH FOR THE DAWN</text>'+
  '<text x="975" y="992" text-anchor="end">ROMANS 13:12</text></g>';
 if(mode==='a'){
  // Robust graphic shape: draw actual vectors; cut only *inside* glyphs.
  // clipPath worked in raster/browser checks; the previous SVG mask did not.
  svg.innerHTML='<defs><clipPath id="xw-geom-clip">'+glyphs+'</clipPath></defs>'+
   '<rect width="1000" height="1000" fill="#eee5d4"/>'+
   '<g fill="var(--ws-night,#102a43)">'+glyphs+'</g>'+
   '<g clip-path="url(#xw-geom-clip)" fill="#eee5d4">'+
   '<path d="M145 178 426 68 373 127 153 232Z M562 325 915 254 869 304 585 385Z M89 697 394 567 346 628 119 758Z M575 856 926 770 901 820 595 915Z"/></g>'+meta;
 }else{
  const lines=[],rays=[];
  for(let i=0;i<112;i++){
   const y=285+i*5.85,amp=8+18*Math.sin(i*.044);
   lines.push('<path d="M-30 '+y.toFixed(1)+' C 240 '+(y-amp).toFixed(1)+' 290 '+(y+amp).toFixed(1)+
     ' 500 '+y.toFixed(1)+' S 790 '+(y-amp).toFixed(1)+' 1030 '+y.toFixed(1)+'"/>');
  }
  for(let i=0;i<116;i++){
   const a=-Math.PI*.9+i/115*Math.PI*1.8,r1=25+i%7*3,r2=640+i%9*10;
   rays.push('<path d="M'+(510+Math.cos(a)*r1).toFixed(1)+' '+(825+Math.sin(a)*r1).toFixed(1)+
    ' L'+(510+Math.cos(a)*r2).toFixed(1)+' '+(825+Math.sin(a)*r2).toFixed(1)+'"/>');
  }
  svg.innerHTML='<defs><clipPath id="xw-type-clip">'+glyphs+'</clipPath>'+
   '<pattern id="xw-dot" width="19" height="19" patternUnits="userSpaceOnUse">'+
   '<circle cx="9.5" cy="9.5" r="4.3" fill="#f4ecdd"/></pattern></defs>'+
   '<rect width="1000" height="1000" fill="#343842"/>'+
   '<g clip-path="url(#xw-type-clip)"><rect width="1000" height="290" fill="url(#xw-dot)"/>'+
   '<g fill="none" stroke="#f4ecdd" stroke-width="3.5" stroke-linecap="round">'+lines.join('')+'</g>'+
   '<g fill="none" stroke="#f4ecdd" stroke-width="2.4" opacity=".9">'+rays.join('')+'</g></g>'+meta;
 }
 const poster=document.createElement('section');
 poster.id='xw-poster';poster.className='xw-poster';
 poster.setAttribute('role','img');poster.setAttribute('aria-label','西望 · '+
  (mode==='a'?'幾何字形':'刻線紋路')+'雜誌宣傳海報');
 poster.append(svg);
 const folds=document.createElement('div');
 folds.className='xw-poster__folds';folds.setAttribute('aria-hidden','true');
 colors.forEach((color,i)=>{
  const layer=document.createElement('span');
  layer.className='xw-poster__fold';layer.dataset.fold=String(i+1);
  layer.style.setProperty('--fold-ink','var('+color+')');
  folds.append(layer);
 });
 poster.append(folds);tile.append(poster);
 const old=document.getElementById('dual-continuum');
 if(old){old.inert=true;old.setAttribute('aria-hidden','true');}
 const ease=x=>{x=Math.max(0,Math.min(1,x));return x*x*(3-2*x)};
 const reduced=matchMedia('(prefers-reduced-motion:reduce)');
 function paint(progress){
  const p=Math.max(0,Math.min(1,Number(progress)||0));
  poster.style.opacity=String(ease((p-.225)/.16));
  [...folds.children].forEach((layer,i)=>{
   const amount=reduced.matches?(p>=.38?1:0):ease((p-(.29+i*.045))/.145);
   layer.style.transform='scaleY('+amount.toFixed(4)+')';
  });
  const revealed=reduced.matches?1:ease((p-.73)/.135);
  svg.style.clipPath='inset(0 0 '+((1-revealed)*100).toFixed(3)+'% 0)';
  folds.style.opacity=reduced.matches?'0':String(1-ease((p-.855)/.03));
  stage.dataset.posterFoldCount='7';
  stage.dataset.posterRevealed=revealed.toFixed(4);
 }
 window.P2Vol00Poster={paint,mode};
 paint(0);
})();
