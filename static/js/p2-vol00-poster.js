/* P2 / Vol.00 scroll-registered poster printing.
 * User decision 2026-11-04:
 *   A: seven Design OS palettes AND the paper color travel with the existing
 *   parent scroll progress. Scroll back = exact rewind. No clock, CSS keyframe,
 *   independent wheel listener, random shuffle, or seven full-plane curtains.
 *   Final: --ws-night background + matte dawn-gold foiled original 西望 paths.
 *   B: unchanged alternate SVG art; no inherited folded entrance.
 * Original approved right cover, parent film and Church/Emmaus untouched.
 */
(()=>{'use strict';
 const stage=document.getElementById('dual-stage');
 const tile=document.getElementById('dual-contents');
 if(!stage||!tile)return;
 const params=new URLSearchParams(location.search);
 if(params.get('poster')==='legacy')return;
 const mode=params.get('poster')==='b'?'b':'a';
 const reduced=matchMedia('(prefers-reduced-motion: reduce)');
 stage.dataset.p2Poster=mode;
 document.documentElement.dataset.p2Poster=mode;
 const colorStops=[
  {name:'water',token:'--ws-water'},
  {name:'magazine',token:'--ws-first-light'},
  {name:'emmaus',token:'--ws-pale-gold'},
  {name:'olive',token:'--ws-olive'},
  {name:'bookshop',token:'--ws-harvest'},
  {name:'cinema',token:'--ws-crimson'},
  {name:'cafe',token:'--ws-daylight-mauve'}
 ];
 const panel=document.createElement('section');
 panel.id='xw-poster';
 panel.className='xw-poster';
 panel.setAttribute('role','img');
 panel.setAttribute('aria-label','西望 · '+(mode==='a'?'七色滾動後定格的黎明金雙字海報':'七組七色刻線字體海報'));
 const art=document.createElement('img');
 art.className='xw-poster__art';
 art.alt='';
 art.decoding='async';
 art.src=mode==='a'
  ?'/images/xiwang-poster-a-night-blue-approved-p2.svg?v=20261104-approved-a'
  :'/images/xiwang-poster-b-v2.svg?v=20261103-master2';
 art.dataset.vectorMaster=mode==='a'?'approved-night-blue-geometry-a':'engraving-b2-7up';
 art.addEventListener('load',()=>{panel.dataset.assetReady=art.naturalWidth>0?'true':'false'});
 art.addEventListener('error',()=>{panel.dataset.assetReady='false';console.error('P2 poster asset failed',art.src)});
 panel.append(art);
 if(mode==='a'){
  // Transparent glyph-only original path mask, not a generated raster font.
  // Keep the approved SVG image as a fallback where browser masks are absent.
  const canMask=typeof CSS!=='undefined'&&(
   CSS.supports('mask-image','url("/images/xiwang-poster-a-glyph-mask.svg")')||
   CSS.supports('-webkit-mask-image','url("/images/xiwang-poster-a-glyph-mask.svg")')
  );
  if(canMask){
   art.style.display='none';
   const glyph=document.createElement('span');
   glyph.className='xw-poster__glyph';
   glyph.setAttribute('aria-hidden','true');
   const foil=document.createElement('span');
   foil.className='xw-poster__glyph xw-poster__glyph--foil';
   foil.setAttribute('aria-hidden','true');
   panel.append(glyph,foil);
  }else panel.dataset.maskFallback='original-approved-svg';
  const caption=document.createElement('span');
  caption.className='xw-poster__caption';
  caption.innerHTML='<span class="xw-poster__slogan">Watch for the Dawn</span><span class="xw-poster__citation">ROMANS 13:12</span>';
  caption.setAttribute('aria-hidden','true');
  panel.append(caption);
 }
 tile.append(panel);
 const legacy=document.getElementById('dual-continuum');
 if(legacy){legacy.inert=true;legacy.setAttribute('aria-hidden','true');}
 const clamp=x=>Math.max(0,Math.min(1,Number(x)||0));
 const ease=x=>{x=clamp(x);return x*x*(3-2*x)};
 const mix=(a,b,t)=>'color-mix(in oklab, '+a+' '+(100*(1-t)).toFixed(2)+'%, '+b+')';
 const paper=token=>'color-mix(in oklab, var('+token+') 24%, #f6eae2)';
 const ink=token=>'color-mix(in oklab, var('+token+') 73%, var(--ws-night))';
 function paint(progress){
  const p=clamp(progress);
  const reveal=ease((p-.23)/.115);
  panel.style.opacity=String(reveal);
  if(mode==='a'){
   // Longer color print travel: the same parent wheel progress (26–77%).
   // Final foil registers by 84.5%; the full-size poster remains until
   // CONTENTS comes forward (86–94.5%); only the finished Contents spread
   // may retreat to reveal the EXISTING homepage film.
   const u=clamp((p-.26)/.51)*6;
   const from=Math.min(6,Math.floor(u));
   const to=Math.min(6,from+1);
   const segment=ease(u-from);
   const inkBase=mix(ink(colorStops[from].token),ink(colorStops[to].token),segment);
   const paperBase=mix(paper(colorStops[from].token),paper(colorStops[to].token),segment);
   const final=ease((p-.77)/.075);
   const contents=ease((p-.86)/.085);
   const gold='var(--ws-morning-gold, #d2bc69)';
   panel.style.setProperty('--xw-ink',mix(inkBase,gold,final));
   panel.style.setProperty('--xw-poster-bg',mix(paperBase,'var(--ws-night,#102a43)',final));
   panel.style.setProperty('--xw-foil-opacity',(.72*final).toFixed(4));
   // Use exactly the SAME approved gold glyph paths, shrinking only when
   // Contents begins. The poster PAGE never shrinks at this moment.
   panel.style.setProperty('--xw-mark-scale',(1-.77*contents).toFixed(5));
   panel.style.setProperty('--xw-page-ink-opacity',((1-contents)*100).toFixed(2)+'%');
   panel.style.setProperty('--xw-caption-opacity',(final*(1-contents)).toFixed(4));
   panel.dataset.palette=colorStops[from].name;
   panel.dataset.paletteFrom=String(from+1);
   panel.dataset.paletteTo=String(to+1);
   panel.dataset.paletteBlend=segment.toFixed(4);
   panel.dataset.finalRegistration=final.toFixed(4);
   stage.dataset.posterPalette=final>=.9999?'midnight-gold':colorStops[from].name;
   stage.dataset.posterRegistration=final.toFixed(4);
   stage.dataset.posterColorStep=String(from+1);
   stage.dataset.posterContents=contents.toFixed(4);
   panel.dataset.posterState=contents>=.999?'contents':final>=.999?'gold-printed':'ink-travel';
  }else{
   panel.style.removeProperty('--xw-ink');
   panel.style.removeProperty('--xw-poster-bg');
   stage.dataset.posterPalette='engraving-b';
   stage.dataset.posterRegistration='0';
   stage.dataset.posterColorStep='0';
  }
  // The previous full-surface sevenfold entrance has been removed.
  stage.dataset.posterFoldCount='0';
  stage.dataset.posterRevealed=reveal.toFixed(4);
  stage.dataset.posterScrollLinked='true';
 }
 window.P2Vol00Poster={paint,mode,colorStops:colorStops.map(x=>x.name)};
 paint(0);
})();
