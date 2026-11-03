/* Vol.00 A/B poster studies + seven genuine homepage-style folds.
   Same Design OS palette as first-look-host.js, no new animation clock.
   SVG lettering uses OS CJK display face (geometric, not brushwork).
   This is a revisable TYPE STUDY; the final custom outlined glyph master
   requires visual review. Right cover and Homepage remain untouched. */
(()=>{'use strict';
 const stage=document.getElementById('dual-stage'),tile=document.getElementById('dual-contents');
 if(!stage||!tile)return;
 const query=new URLSearchParams(location.search);
 const mode=query.get('poster')?.toLowerCase()==='b'?'b':'a';
 stage.dataset.p2Poster=mode;
 document.documentElement.dataset.p2Poster=mode;
 const colors=['--ws-water','--ws-first-light','--ws-pale-gold','--ws-olive','--ws-harvest','--ws-crimson','--ws-daylight-mauve'];
 const svg=document.createElementNS('http://www.w3.org/2000/svg','svg');
 svg.classList.add('xw-poster__art');
 svg.setAttribute('viewBox','0 0 1000 1000');
 svg.setAttribute('preserveAspectRatio','xMidYMid meet');
 svg.setAttribute('aria-hidden','true');
 const glyphs='<g class="xw-poster__big-type" text-anchor="middle" lang="zh-Hant">'+
   '<text x="500" y="470" textLength="950" lengthAdjust="spacingAndGlyphs">西</text>'+
   '<text x="500" y="955" textLength="950" lengthAdjust="spacingAndGlyphs">望</text></g>';
 const meta='<g class="xw-poster__metadata"><text x="25" y="24">WESTSIDE WATCH / VOL.00</text>'+
  '<text x="975" y="24" text-anchor="end">2026 · POSTER SERIES</text>'+
  '<text x="25" y="992">WATCH FOR THE DAWN</text>'+
  '<text x="975" y="992" text-anchor="end">ROMANS 13:12</text></g>';
 if(mode==='a'){
  svg.innerHTML='<defs><mask id="xw-geom-mask" maskUnits="userSpaceOnUse" x="0" y="0" width="1000" height="1000">'+
   '<rect width="1000" height="1000" fill="black"/><g fill="white">'+glyphs+'</g>'+
   '<g fill="black"><path d="M140 176 420 69 370 130 149 225Z"/>'+
   '<path d="M562 332 898 253 868 309 576 387Z"/>'+
   '<path d="M90 706 385 580 344 645 120 758Z"/>'+
   '<path d="M550 848 930 770 901 821 585 903Z"/></g></mask></defs>'+
   '<rect width="1000" height="1000" fill="#eee5d4"/>'+
   '<path d="M0 500 H1000" stroke="var(--ws-first-light,#a2872a)" stroke-width="2"/>'+
   '<rect width="1000" height="1000" fill="var(--ws-night,#102a43)" mask="url(#xw-geom-mask)"/>'+meta;
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
