/* P2 / Vol.00 — Two actual original native SVG poster masters, build-time assets.
   A: user-selected midnight-blue geometric 西望, traced to editable paths and fitted to the left square.
   B2: seven actual individually engraved 西望 groups, seven OS colors.
   No Doré, brush glyphs or permanent navigation strip on Magazine left.
   Same reversible sevenfold entry. Approved right-hand cover unchanged.
   A master: static/images/xiwang-poster-a-night-blue-approved-p2.svg; B remains a separate experimental variant. */
(()=>{'use strict';
 const stage=document.getElementById('dual-stage');
 const tile=document.getElementById('dual-contents');
 if(!stage||!tile)return;
 const params=new URLSearchParams(location.search);
 if(params.get('poster')==='legacy')return;
 const mode=params.get('poster')==='b'?'b':'a';
 stage.dataset.p2Poster=mode;
 document.documentElement.dataset.p2Poster=mode;
 const colors=['--ws-water','--ws-first-light','--ws-pale-gold','--ws-olive','--ws-harvest','--ws-crimson','--ws-daylight-mauve'];
 const panel=document.createElement('section');
 panel.id='xw-poster';
 panel.className='xw-poster';
 panel.setAttribute('role','img');
 panel.setAttribute('aria-label','西望 · '+(mode==='a'?'巨型幾何雙字海報':'七組七色刻線雙字海報'));
 const art=document.createElement('img');
 art.className='xw-poster__art';
 art.alt='';
 art.decoding='async';
 art.src=mode==='a'
  ?'/images/xiwang-poster-a-night-blue-approved-p2.svg?v=20261104-approved-a'
  :'/images/xiwang-poster-b-v2.svg?v=20261103-master2';
 art.dataset.vectorMaster=mode==='a'?'approved-night-blue-geometry-a':'engraving-b2-7up';
 art.addEventListener('load',()=>{
  panel.dataset.assetReady=art.naturalWidth>0?'true':'false';
 });
 art.addEventListener('error',()=>{
  panel.dataset.assetReady='false';
  console.error('P2 Xiwang vector artwork did not load',art.src);
 });
 panel.append(art);
 const folds=document.createElement('div');
 folds.className='xw-poster__folds';
 folds.setAttribute('aria-hidden','true');
 colors.forEach((token,i)=>{
  const layer=document.createElement('span');
  layer.className='xw-poster__fold';
  layer.dataset.fold=String(i+1);
  layer.style.setProperty('--fold-ink','var('+token+')');
  folds.append(layer);
 });
 panel.append(folds);tile.append(panel);
 const legacy=document.getElementById('dual-continuum');
 if(legacy){legacy.inert=true;legacy.setAttribute('aria-hidden','true');}
 const ease=x=>{x=Math.max(0,Math.min(1,x));return x*x*(3-2*x);};
 const reduced=matchMedia('(prefers-reduced-motion:reduce)');
 function paint(progress){
  const p=Math.max(0,Math.min(1,Number(progress)||0));
  panel.style.opacity=String(ease((p-.225)/.16));
  [...folds.children].forEach((layer,i)=>{
   const fraction=reduced.matches?(p>=.38?1:0):ease((p-(.29+i*.045))/.145);
   layer.style.transform='scaleY('+fraction.toFixed(4)+')';
  });
  const reveal=reduced.matches?1:ease((p-.73)/.135);
  art.style.clipPath='inset(0 0 '+((1-reveal)*100).toFixed(3)+'% 0)';
  folds.style.opacity=reduced.matches?'0':String(1-ease((p-.855)/.03));
  stage.dataset.posterFoldCount='7';
  stage.dataset.posterRevealed=reveal.toFixed(4);
 }
 window.P2Vol00Poster={paint,mode};
 paint(0);
})();
