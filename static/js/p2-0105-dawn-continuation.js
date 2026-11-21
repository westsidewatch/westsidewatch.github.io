/* P2 05 — continuous 01–04 -> Dawn Library, V9 flag and scripture-to-catalogue handoff.
   A single scroll distance drives the first layer; one click-driven 7.6s
   timeline drives only the second-layer entry, mirroring approved Olive 04.
   P2 returns never replay the flag. All animation states are deterministic. */
(()=>{'use strict';
 const $=s=>document.querySelector(s),track=$('#p205-track'),stage=$('#p205-stage');
 const prior=$('#p205-prior'),realm=$('#dawn-realm');
 const twins=$('#dawn-twins'),squares=[...twins.querySelectorAll('.dawn-twins__square')];
 const world=$('#dawn-world');
 const handoff=$('#dawn-handoff'),second=$('#dawn-second'),returnButton=$('#dawn-return');
 const scriptureFrame=$('.dawn-second__motherform');
 const search=$('#dawn-search'),works=$('#dawn-works');
 const more=$('#dawn-more'),prevButton=$('#dawn-prev'),pageStatus=$('#dawn-page-status'),total=$('#dawn-total');
 const wall=$('#dawn-wall'),wallGrid=$('#dawn-wall-grid'),catalogue=$('#dawn-catalogue'),catalogueFocus=$('#dawn-catalogue-focus');
 const openCatalogue=$('#dawn-open-catalogue'),openCatalogueTop=$('#dawn-open-catalogue-top'),closeCatalogue=$('#dawn-close-catalogue');
 const clamp=(n,a=0,b=1)=>Math.max(a,Math.min(b,n)),ease=n=>{const x=clamp(n);return x*x*(3-2*x)};
 const mix=(a,b,t)=>a+(b-a)*t;
 let queued=false,at=0,entryProgress=0,entryClock=0,entryTarget=0,rafId=0;
 function progress(){return clamp(-track.getBoundingClientRect().top/Math.max(1,innerHeight),0,32.3)}
 function paint(){queued=false;const d=progress(),p=entryProgress;

  // THE ORIGINAL 01–04 FILES REMAIN UNMODIFIED AND BEHIND THEIR OWN STAGE.
  prior.contentWindow?.postMessage({type:'westside-p2-home-pose',distance:Math.min(d,26.3),legacyProgress:clamp(d/26.3),active:d<27.3},location.origin);
  const appear=ease((d-26.23)/1.22),settled=ease((d-27.35)/.44);
  realm.style.visibility=appear>.001?'visible':'hidden';
  realm.inert=settled<.98||p>.001;
  realm.setAttribute('aria-hidden',settled<.98||p>.001?'true':'false');
  realm.style.pointerEvents=settled>.98&&p<.001?'auto':'none';
  world.style.opacity=String(appear);
  twins.style.visibility=settled>.02?'visible':'hidden';
   // Keep the original paired masthead rendered above the image stage.
   squares.forEach(square=>{square.style.visibility='visible';square.style.opacity='1';});
  twins.style.opacity=String(settled*(1-ease((p-.01)/.16)));
  twins.style.transform='translate(-50%,-50%)';
  paintWorld(d);
  stage.dataset.p205Scene=d<26.23?'04-protected':'05-gospel-image-world';
  paintHandoff();
 }
 function schedule(){if(!queued){queued=true;requestAnimationFrame(paint)}}
 function jump(d){resetEntry();scrollTo({top:track.offsetTop+clamp(d,0,32.3)*innerHeight,behavior:'instant'});schedule()}
 addEventListener('scroll',()=>{if(entryProgress>.001&&progress()<26.23)resetEntry();schedule()},{passive:true});
 addEventListener('resize',schedule,{passive:true});prior.addEventListener('load',schedule);

 // These are the seven exact Design OS color roles already used by Olive 04.
 const token=['--ws-water','--ws-first-light','--ws-pale-gold','--ws-olive','--ws-harvest','--ws-harvest','--ws-daylight-mauve'];
 const osStyle=getComputedStyle(document.documentElement);
 const sampler=document.createElement('canvas');sampler.width=sampler.height=1;
 const ctx=sampler.getContext('2d',{willReadFrequently:true});
 function osColor(name,fallback){const raw=osStyle.getPropertyValue(name).trim();if(/^#[\da-f]{6}$/i.test(raw))return raw.toLowerCase();
  if(raw&&ctx&&window.CSS?.supports('color',raw)){ctx.clearRect(0,0,1,1);ctx.fillStyle=raw;ctx.fillRect(0,0,1,1);const data=ctx.getImageData(0,0,1,1).data;if(data[3]===255)return '#'+[...data].slice(0,3).map(v=>v.toString(16).padStart(2,'0')).join('');}return fallback;}
 const palette=token.map((t,i)=>osColor(t,['#5b8fa8','#a2872a','#cebd74','#738a5a','#b8944a','#b8944a','#b085ab'][i]));
 const harvest=palette[4],gold=osColor('--ws-morning-gold','#d2bc69'),paper=osColor('--ws-paper','#faf9f5'),papyrus=osColor('--ws-papyrus','#eee4c9');
 function hexMix(a,b,t){return '#'+[1,3,5].map(i=>Math.round(mix(parseInt(a.slice(i,i+2),16),parseInt(b.slice(i,i+2),16),clamp(t))).toString(16).padStart(2,'0')).join('')}
 function sevenInk(p){const t=clamp((p-.22)/.62)*6,i=Math.min(5,Math.floor(t));return hexMix(palette[i],palette[i+1],t-i)}
 // Sample the *visible* twin masthead immediately before entry. This is a visual
 // handoff, not a separately designed color scheme.
 function computedHex(raw,fallback){
  const match=String(raw||'').match(/^rgba?\(\s*(\d+)[,\s]+(\d+)[,\s]+(\d+)/i);
  if(match)return '#'+match.slice(1,4).map(n=>Math.min(255,Number(n)).toString(16).padStart(2,'0')).join('');
  if(/^#[\da-f]{6}$/i.test(raw))return raw.toLowerCase();
  return fallback;
 }
 function currentTwinColors(){
  return squares.map((square,i)=>{
   const style=getComputedStyle(square);
   return {background:computedHex(style.backgroundColor,i?papyrus:harvest),
    ink:computedHex(style.color,i?osColor('--ws-ink','#252525'):paper)};
  });
 }
 let startTwinColors=currentTwinColors();
 const ns='http://www.w3.org/2000/svg';
 function svg(name,attrs={}){const e=document.createElementNS(ns,name);for(const [k,v] of Object.entries(attrs))e.setAttribute(k,v);return e}
 function textNode(group,str,x,y,size,color){const n=svg('text',{x,y,'font-size':size,fill:color,'font-family':'Bodoni Moda SC,Georgia,serif'});n.textContent=str;group.append(n);return n}
 const kinetic=svg('svg',{'aria-hidden':'true'}),defs=svg('defs');kinetic.append(defs);
 const clip=svg('clipPath',{id:'p205-v9-clip'}),aperture=svg('rect',{x:800,y:0,width:0,height:108});clip.append(aperture);defs.append(clip);
 const sheetGroup=svg('g');kinetic.append(sheetGroup);
 // Full-screen sevenfold rects removed by editorial direction.
 const banner=svg('g',{'clip-path':'url(#p205-v9-clip)'});
 const topRule=svg('path',{d:'M0 1H1600',stroke:startTwinColors[0].ink,'stroke-width':1,fill:'none'});
 const bottomRule=svg('path',{d:'M0 107H1600',stroke:startTwinColors[1].ink,'stroke-width':1,fill:'none'});
 const letters=svg('g');banner.append(topRule,bottomRule,letters);kinetic.append(banner);
 const seals=[0,1].map(i=>{
  const g=svg('g'),shell=svg('rect',{width:500,height:500,fill:i?papyrus:harvest,stroke:gold,'stroke-width':2});g.append(shell);
  const initial=svg('g');textNode(initial,i?'JOHN 8:32':'DAWN LIBRARY',25,56,22,i?harvest:paper);
  textNode(initial,i?'THE TRUTH':'DAWN LIBRARY',25,192,i?42:45,i?harvest:paper);
  textNode(initial,i?'真理使人自由':'黎明書局',25,280,36,i?harvest:paper);g.append(initial);
  const copy=svg('g',{opacity:0});textNode(copy,i?'THE TRUTH':'DAWN LIBRARY',25,50,23,gold);
  if(i){textNode(copy,'AND YE SHALL KNOW',25,136,29,paper);textNode(copy,'THE TRUTH, AND',25,182,29,paper);textNode(copy,'THE TRUTH SHALL',25,228,29,paper);textNode(copy,'MAKE YOU FREE.',25,274,29,paper);textNode(copy,'JOHN 8:32 · KJV',25,460,18,gold)}
  else{textNode(copy,'你們必曉得真理，',25,155,35,paper);textNode(copy,'真理必叫你們',25,220,35,paper);textNode(copy,'得以自由。',25,285,35,paper);textNode(copy,'約翰福音 8:32',25,460,18,gold)}
  g.append(copy);kinetic.append(g);return {g,shell,initial,copy};
 });
 handoff.replaceChildren(kinetic);
 let glyphReady=false;
 fetch('/images/westside-watch-lettering-v9-clean-kern.svg').then(r=>{if(!r.ok)throw Error('V9 lettering not available');return r.text()}).then(xml=>{
  const doc=new DOMParser().parseFromString(xml,'image/svg+xml');const paths=[...doc.querySelectorAll('path[data-letter]')];
  if(paths.length!==13||paths.map(n=>n.getAttribute('data-letter')).join('')!=='WESTSIDEWATCH')throw Error('Original V9 glyph mismatch');
  paths.forEach(n=>letters.append(document.importNode(n,true)));glyphReady=true;stage.dataset.p205Wordmark='v9-final';
 }).catch(e=>{console.error(e);stage.dataset.p205Wordmark='unavailable'});
 function paintHandoff(){const p=entryProgress,complete=p>=.99999;stage.dataset.p205Handoff=p.toFixed(4);
  twins.setAttribute('aria-expanded',String(complete));
  handoff.style.visibility=p>.001&&p<.63?'visible':'hidden';
  // Reveal the reading page as the retained V9 handoff leaves, not after an
  // otherwise empty intermediate frame.
  second.style.visibility=p>.61?'visible':'hidden';
  second.style.clipPath='none';
  second.inert=!complete;second.setAttribute('aria-hidden',complete?'false':'true');
  second.style.pointerEvents=complete?'auto':'none';
  if(p<=.001)return;
  const bounds=stage.getBoundingClientRect(),w=bounds.width,h=bounds.height;
  kinetic.setAttribute('viewBox',`0 0 ${w} ${h}`);
  // No full-screen sevenfold sheets. Only the original V9 lettering and two
  // 1:1 scripture carriers animate; no color field covers the exhibition.
  const bw=w*.9,scale=bw/1600,bh=108*scale,bx=(w-bw)/2,by=Math.max(25,Math.min(h*.27,twins.getBoundingClientRect().bottom-bounds.top+14));
  banner.setAttribute('transform',`translate(${bx} ${by}) scale(${scale})`);
  const opened=ease((p-.045)/.28),retire=ease((p-.56)/.15);
  aperture.setAttribute('x',800*(1-opened+retire*opened));aperture.setAttribute('width',1600*opened*(1-retire));
  // The V9 letters remain a single original SVG, with no extra color slabs.
  // Ink starts in the visible masthead's existing color and enters sevenfold
  // only after the ribbon has fully opened.
  const shift=ease((p-.35)/.25);
  const ink=hexMix(startTwinColors[0].ink,sevenInk(p),shift);
  letters.setAttribute('fill',ink);
  topRule.setAttribute('stroke',hexMix(startTwinColors[0].ink,sevenInk(p),shift));
  bottomRule.setAttribute('stroke',hexMix(startTwinColors[1].ink,sevenInk(p),shift));
  banner.setAttribute('opacity',String(1-ease((p-.56)/.08)));
  const source=squares.map(node=>node.getBoundingClientRect());
  // Measure the actual embedded scripture field. The old invisible landing
  // divs were display:none and yielded zero-width, zero-height destinations.
  const frame=scriptureFrame.getBoundingClientRect();
  const gap=Math.min(24,Math.max(10,frame.width*.025));
  const targetSide=Math.max(1,Math.min((frame.width-gap)/2,frame.height*.96));
  const insetX=(frame.width-(2*targetSide+gap))/2;
  const target=[0,1].map(i=>({
   left:frame.left+insetX+i*(targetSide+gap),
   top:frame.top+(frame.height-targetSide)/2,
   width:targetSide,height:targetSide
  }));
  const lift=ease((p-.015)/.17),cross=ease((p-.18)/.34),land=ease((p-.58)/.15),capHeight=100*scale;
  seals.forEach((seal,i)=>{
   const src=source[i],dst=target[i],s0=src.width,sz=mix(mix(s0,capHeight,lift),dst.width,land);
   const sourceX=src.left-bounds.left+src.width/2,sourceY=src.top-bounds.top+src.height/2;
   const stationX=bx+bw*(i?.68:.43),stationY=by+bh/2;
   const endX=dst.left-bounds.left+dst.width/2,endY=dst.top-bounds.top+dst.height/2;
   const cx=mix(mix(sourceX,stationX,cross),endX,land),cy=mix(mix(sourceY,stationY,lift),endY,land);
   seal.g.setAttribute('transform',`translate(${cx-sz/2} ${cy-sz/2}) scale(${sz/500})`);
   seal.g.setAttribute('opacity',String(ease((p-.045)/.07)*(1-ease((p-.53)/.1))));
   const original=startTwinColors[i],sealTransition=ease((p-.35)/.18);
   seal.shell.setAttribute('fill',hexMix(original.background,sevenInk(p),sealTransition));
   seal.shell.setAttribute('stroke',hexMix(original.ink,sevenInk(p),sealTransition));
   seal.initial.querySelectorAll('text').forEach(n=>n.setAttribute('fill',hexMix(original.ink,paper,sealTransition)));
   seal.initial.setAttribute('opacity',1-ease((p-.13)/.18));seal.copy.setAttribute('opacity',ease((p-.57)/.12)*(1-ease((p-.74)/.14)));
   // The two real second-layer plates are the physical targets: no last-frame jump.
  });
 }
 function resetEntry(){if(rafId)cancelAnimationFrame(rafId);rafId=0;entryClock=entryProgress=entryTarget=0;catalogue.hidden=true;wall.hidden=false;second.scrollTop=0;schedule()}
 function animateEntry(target){
  if(rafId)cancelAnimationFrame(rafId);
  if(target&&entryProgress<.001){
   // Reading metadata is small and can load while the first-layer motion runs.
   // Full-catalogue search remains deferred until the visitor asks for it.
   void loadFeaturedIntroductions().catch(()=>{});
   // Mount existing jacket artwork before the reader reaches the second layer.
   // It never waits for the 7.6s transition to finish.
   void loadWallCovers();
   startTwinColors=currentTwinColors();
   for(let i=0;i<2;i++){
    seals[i].shell.setAttribute('fill',startTwinColors[i].background);
    seals[i].initial.querySelectorAll('text').forEach(n=>n.setAttribute('fill',startTwinColors[i].ink));
   }
  }
  entryTarget=target;
  const from=entryProgress,start=performance.now(),duration=target?7600:0;
  if(!duration||matchMedia('(prefers-reduced-motion: reduce)').matches){entryClock=entryProgress=target;schedule();if(target){loadWallCovers();}return;}
  const tick=now=>{entryProgress=mix(from,target,clamp((now-start)/duration));entryClock=entryProgress;schedule();
   if(Math.abs(entryProgress-target)>.0001)rafId=requestAnimationFrame(tick);else{rafId=0;if(target){loadWallCovers();}}};
  rafId=requestAnimationFrame(tick);
 }
 twins.addEventListener('click',()=>{if(progress()<27.96||entryProgress>.001)return;if(!glyphReady){console.warn('V9 original lettering still loading');return;}animateEntry(1)});
 returnButton.addEventListener('click',()=>{resetEntry();schedule()});
 document.addEventListener('keydown',e=>{if(e.key==='Escape'&&entryProgress>.001)resetEntry()});

 // Genuine interior illustrations and Holy Land photographs.
 // MERSI grammar: the scroll position directly sets slide and clip geometry.
 // No page rotation, clock-based slideshow, fictional book-cover art, or central seam.
 const commons=name=>'https://commons.wikimedia.org/wiki/Special:FilePath/'+encodeURIComponent(name)+'?width=1200';
 // Registry-driven P2 presentation: any curated collection may publish a
 // verified image manifest. P2 is a shared surface, not a hard-coded exhibit.
 let activeCollection='jerusalem-3000';
 let gospelScenes={left:[],right:[]};
 function validExhibitionItem(item){
  if(!item||!item.title||!item.media?.src||!item.media?.source||!item.destination)return false;
  const media=item.media.src,source=item.media.source;
  const validMedia=media.startsWith('/')||media.startsWith('https://');
  return validMedia&&(source.startsWith('/')||source.startsWith('https://')) &&
   (item.destination.startsWith('/')||item.destination.startsWith('https://'));
 }
 async function loadExhibition(){
  try{
   const registryResponse=await fetch('/dawn-library/p2-exhibitions/index.json');
   if(!registryResponse.ok)throw Error('P2 exhibitions index '+registryResponse.status);
   const registry=await registryResponse.json();
   const requested=new URLSearchParams(location.search).get('collection')||registry.defaultId;
   const selected=(registry.collections||[]).find(e=>e.id===requested);
   if(!selected||!selected.manifest?.startsWith('/dawn-library/p2-exhibitions/'))throw Error('Exhibition not registered');
   const response=await fetch(selected.manifest);
   if(!response.ok)throw Error('Exhibition data '+response.status);
   const exhibition=await response.json();
   if(exhibition.schema!=='dawn.p2.curated-exhibition.v1'||exhibition.id!==selected.id||!Array.isArray(exhibition.items))throw Error('Invalid exhibition manifest');
   const items=exhibition.items.filter(validExhibitionItem).map(item=>({
    image:item.media.src,title:item.title,caption:item.caption||'',kind:item.kind||'',
    href:item.destination,source:item.media.source,workId:item.workId||''
   }));
   if(items.length<2)throw Error('Exhibition has too few verified image items');
   // Counterflow: alternate collection plates across both independently
   // moving visual channels. Pages always lead back to admitted collection.
   gospelScenes={left:items.filter((_,i)=>i%2===0),right:items.filter((_,i)=>i%2===1)};
   activeCollection=exhibition.id;
   world.dataset.exhibition=exhibition.id;
   stage.dataset.p205CuratedCollection=exhibition.id;
   // Reset image indices so on-screen media cannot be mislabeled.
   imageSides.forEach(side=>{side.index=-1;side.nextIndex=-1;});
   schedule();
  }catch(e){console.error('[Dawn P2 exhibition]',e);world.dataset.exhibition='unavailable';}
 }
 const imageSides=['left','right'].map((key)=>{
  const node=$('#dawn-page-'+key),art=$('#dawn-art-'+key),current=$('#dawn-image-'+key);
  const next=document.createElement('img');next.className='dawn-world__incoming';
  next.alt='';next.decoding='async';next.loading='lazy';art.append(next);
  return {key,node,current,next,art,title:$('#dawn-title-'+key),caption:$('#dawn-author-'+key),index:-1,nextIndex:-1};
 });
 for(const side of imageSides){
  // Hide any broken remote asset rather than displaying a missing-image icon.
  for(const img of [side.current,side.next]){
   img.addEventListener('error',()=>{img.style.opacity='0';schedule();});
   img.addEventListener('load',()=>{img.style.removeProperty('opacity');schedule();});
  }
 }
 void loadExhibition();
 function paintWorld(d){
  // Two independently staggered visual strips, with scroll-owned MERSI-like
  // sliding masks. Motion stops on stationary scroll and reverses precisely.
  const base=Math.max(0,d-27.65);
  for(const side of imageSides){
   const scenes=gospelScenes[side.key];if(!scenes.length)continue;
   const s=base*(side.key==='left'?1.18:1.12)+(side.key==='right'?.42:0);
   const step=Math.floor(Math.max(0,s)),fraction=ease(s-Math.floor(s));
   const i=step%scenes.length,ni=(i+1)%scenes.length;
   if(side.index!==i){
    const item=scenes[i];side.current.src=item.image;
    side.current.alt=item.title+' — '+item.caption;
    side.index=i;
   }
   if(side.nextIndex!==ni){
    side.next.src=scenes[ni].image;
    side.next.alt=scenes[ni].title+' — '+scenes[ni].caption;
    side.nextIndex=ni;
   }
   // Never expose the papyrus canvas while a remote image is missing or loading.
   // A one-image fallback must fill the whole half-screen, with correct attribution.
   const left=side.key==='left';
   const currentReady=side.current.complete&&side.current.naturalWidth>0;
   const nextReady=side.next.complete&&side.next.naturalWidth>0;
   let shown;
   if(currentReady&&nextReady){
    const currentPct=(fraction*100).toFixed(2);
    const incomingPct=((1-fraction)*100).toFixed(2);
    side.current.style.clipPath=left
     ?`inset(0 0 ${currentPct}% 0)`
     :`inset(${currentPct}% 0 0 0)`;
    side.next.style.clipPath=left
     ?`inset(${incomingPct}% 0 0 0)`
     :`inset(0 0 ${incomingPct}% 0)`;
    shown=fraction>.5?scenes[ni]:scenes[i];
   }else if(currentReady){
    side.current.style.clipPath='none';side.next.style.clipPath='inset(0 0 100% 0)';
    shown=scenes[i];
   }else if(nextReady){
    side.current.style.clipPath='inset(0 0 100% 0)';side.next.style.clipPath='none';
    shown=scenes[ni];
   }else{
    side.current.style.clipPath='none';side.next.style.clipPath='inset(0 0 100% 0)';
    shown=scenes[i];
   }
   side.current.style.transform='none';
   side.next.style.transform='none';
   if(side.node.href!==shown.href){
    side.node.href=shown.href;
    side.node.target='_blank';side.node.rel='noopener noreferrer';
    side.node.setAttribute('aria-label','查看 '+shown.title+' · 原始書籍或館藏');
   }
   side.title.textContent=shown.title;
   side.caption.textContent=shown.caption;
   side.node.querySelector('.dawn-world__rubric').textContent=shown.kind;
  }
 }

 // Book and reading states belong to Dawn; never navigate away on cover click.
 const detail=$('#dawn-book-detail'),detailBack=$('#dawn-book-back'),detailTitle=$('#dawn-book-title'),detailAuthor=$('#dawn-book-author'),detailEdition=$('#dawn-book-edition'),detailImage=$('#dawn-book-image'),detailCaption=$('#dawn-book-image-caption'),detailVisual=$('#dawn-book-visual'),detailText=$('#dawn-book-text'),detailSource=$('#dawn-book-source');
 let index=null,currentPage=0,loading=false,loaded=[],cache=new Map();
 let coverLookup=null,coverLookupLoading=null,visualLookup=null,visualLookupLoading=null,activeBook=null,returnTo='wall',returnScroll=0,detailTicket=0;
 function normalizeTitle(s){return String(s||'').toLocaleLowerCase().normalize('NFKC').replace(/[^\p{L}\p{N}]+/gu,' ').trim();}
 function shelvesOf(data){return Array.isArray(data)?data:Array.isArray(data?.shelves)?data.shelves:[];}
 function safeHttp(url){try{const a=new URL(url,location.origin);return /^https?:$/.test(a.protocol)?a.href:null}catch{return null}}
 async function loadCatalogueCoverLookup(){
  if(coverLookup)return coverLookup;
  if(coverLookupLoading)return coverLookupLoading;
  coverLookupLoading=(async()=>{
   const map=new Map();
   try{
    const response=await fetch('/dawn-library/storefront.json');
    if(!response.ok)throw Error('Storefront unavailable');
    const data=await response.json();
    for(const shelf of shelvesOf(data))for(const work of (shelf.items||[])){
     if(work.title&&work.cover?.url&&work.source?.url)map.set(normalizeTitle(work.title),work);
    }
   }catch(error){console.warn('[Dawn covers]',error)}
   coverLookup=map;return map;
  })();
  return coverLookupLoading;
 }
 // These images are matched to their actual, documented source works.
 // Do not apply a generic Jerusalem visual to an unrelated catalogue entry.
 async function loadVisualLookup(){
  if(visualLookup)return visualLookup;
  if(visualLookupLoading)return visualLookupLoading;
  visualLookupLoading=(async()=>{
   const map=new Map();
   try{
    const response=await fetch('/dawn-library/p2-exhibitions/jerusalem-3000.json');
    if(!response.ok)throw Error('Curated works unavailable');
    const data=await response.json();
    for(const item of data.items||[]){
     if(item.title&&safeHttp(item.media?.src)){
      map.set(normalizeTitle(item.title),{url:item.media.src,alt:item.media.alt||item.title,source:safeHttp(item.media.source||item.sourceWork||item.destination),credit:item.creator||'',workSource:safeHttp(item.sourceWork||item.destination),verified:!String(item.imageStatus||'').includes('unmatched')});
     }
    }
   }catch(error){console.warn('[Dawn images]',error)}
   visualLookup=map;return map;
  })();
  return visualLookupLoading;
 }
 function imageFor(work,storefront){
  if(work?.illustration?.url&&safeHttp(work.illustration.url))return {...work.illustration,url:safeHttp(work.illustration.url),kind:'illustration'};
  const cover=safeHttp(work?.cover?.url||storefront?.cover?.url);
  if(cover)return {url:cover,alt:'封面：'+(work.title||''),kind:'cover',source:safeHttp(storefront?.source?.url||work.sourceUrl)};
  const visual=visualLookup?.get(normalizeTitle(work?.title));
  if(visual&&visual.verified)return {...visual,kind:'illustration'};
  return null;
 }
 function setDetailImage(visual){
  detailImage.hidden=true;detailImage.removeAttribute('src');detailVisual.classList.remove('dawn-book-detail__visual--image');detailCaption.textContent='';
  if(!visual){detailVisual.classList.add('dawn-book-detail__visual--text');return}
  detailVisual.classList.remove('dawn-book-detail__visual--text');
  const ticket=detailTicket;detailImage.alt=visual.alt||'書籍插圖';detailImage.onload=()=>{if(ticket===detailTicket){detailImage.hidden=false;detailVisual.classList.add('dawn-book-detail__visual--image')}};
  detailImage.onerror=()=>{if(ticket===detailTicket){detailImage.hidden=true;detailVisual.classList.add('dawn-book-detail__visual--text');detailCaption.textContent=''}};
  detailImage.src=visual.url;
  detailCaption.textContent=visual.kind==='illustration'?'書內圖版 · '+(visual.credit||'原作'):'';
 }
 // Visitor-facing book presentation is literary editorial copy, never a status report.
 const CATEGORY_ZH={
  'bible':'聖經與信仰','church':'教會歷史','ancient':'歷史與考古',
  'philosophy':'哲學與思想','biography':'傳記與生命'
 };
 let featuredIntroductions=null;
 async function loadFeaturedIntroductions(){
  if(featuredIntroductions)return featuredIntroductions;
  const response=await fetch('/dawn-library/p2-featured-introductions.json');
  if(!response.ok)throw Error('Dawn reading essays unavailable');
  featuredIntroductions=await response.json();return featuredIntroductions;
 }
 let bookIntroductionIndex=null;
 async function getBookIntroductionIndex(){
  if(bookIntroductionIndex)return bookIntroductionIndex;
  const response=await fetch('/dawn-library/p2-exhibitions/jerusalem-3000-introductions.json');
  if(!response.ok)throw Error('Curated introductions unavailable');
  bookIntroductionIndex=await response.json();return bookIntroductionIndex;
 }
 function introductionParagraphs(work,source){
  if(Array.isArray(work.editorialParagraphs)&&work.editorialParagraphs.length)return work.editorialParagraphs;
  const candidate=[work.introductionZh,work.descriptionZh,work.summaryZh,work.description?.zhHant,work.description?.zh,source?.introductionZh]
   .find(v=>typeof v==='string'&&v.trim().length>=110&&/[一-龥]/u.test(v));
  return candidate?[candidate.trim()]:[];
 }
 function drawBookIntroduction(work,source){
  detailText.replaceChildren();
  const paragraphs=introductionParagraphs(work,source);
  if(!paragraphs.length){
   // No invented contents: the heading area already has actual bibliographic
   // metadata. Do not manufacture simplistic copy and call it a synopsis.
   return;
  }
  const lead=document.createElement('section');lead.className='dawn-book-detail__introduction';lead.lang='zh-Hant';
  const heading=document.createElement('h3');heading.textContent='作品導讀';lead.append(heading);
  for(const copy of paragraphs){const p=document.createElement('p');p.textContent=copy;lead.append(p)}
  detailText.append(lead);
 }
 function appendReadingExtract(pack){
  const excerpt=document.createElement('section');excerpt.className='dawn-book-detail__extract';
  const heading=document.createElement('h3');heading.textContent='原文與繁中試讀';excerpt.append(heading);
  for(const segment of pack.segments){
   const unit=document.createElement('div');unit.className='dawn-book-detail__paragraph';
   if(segment.source){const p=document.createElement('p');p.lang=pack.sourceLanguage||'en';p.textContent=segment.source;unit.append(p)}
   if(segment.translation){const p=document.createElement('p');p.lang='zh-Hant';p.textContent=segment.translation;unit.append(p)}
   excerpt.append(unit);
  }
  detailText.append(excerpt);
 }
 async function openBook(work,from){
  if(!work?.title)return;
  const ticket=++detailTicket;
  returnTo=from||(!catalogue.hidden?'catalogue':'wall');returnScroll=second.scrollTop;activeBook=work;
  wall.hidden=true;catalogue.hidden=true;detail.hidden=false;
  detailTitle.textContent=work.title;detailAuthor.textContent=work.creator||work.author||'';
  detailEdition.textContent=work.date?String(work.date):'';
  const source=coverLookup?.get(normalizeTitle(work.title));
  const visual=imageFor(work,source);
  setDetailImage(visual);
  const sourceUrl=safeHttp(work.sourceUrl||work.source?.url||source?.source?.url||visual?.workSource||visual?.source);
  const sourceHint=$('#dawn-book-source-hint');
  sourceHint.hidden=!sourceUrl;
  detailSource.target='_blank';detailSource.rel='noopener noreferrer';
  if(sourceUrl){detailSource.href=sourceUrl;detailSource.hidden=false}else{detailSource.hidden=true;detailSource.removeAttribute('href')}
  drawBookIntroduction(work,source);
  // Featured editions receive source-grounded editorial introductions; the
  // figure and bibliography remain stable while the essay data is fetched.
  if(!introductionParagraphs(work,source).length){
   loadFeaturedIntroductions().then(index=>{
    if(ticket!==detailTicket)return;
    const paragraphs=index.items?.[work.title]||[];
    if(paragraphs.length)drawBookIntroduction({...work,editorialParagraphs:paragraphs},source);
   }).catch(error=>console.debug('[Dawn edited essays]',error));
  }
  second.scrollTo({top:detail.offsetTop,behavior:'instant'});
  // Optional source-backed trial text appears only when genuinely present.
  try{
   const reader=await import('/js/dawn-reading-resolver.mjs');
   const pack=await reader.localReadingPack(work.workId||work.id);
   if(ticket!==detailTicket)return;
   if(pack?.segments?.length)appendReadingExtract(pack);
  }catch(error){console.debug('[Dawn editorial reading pack]',error)}
 }
 function closeBook(){
  if(detail.hidden)return;
  ++detailTicket;detail.hidden=true;activeBook=null;
  if(returnTo==='catalogue'){catalogue.hidden=false;wall.hidden=true}
  else{wall.hidden=false;catalogue.hidden=true}
  second.scrollTo({top:returnScroll,behavior:'instant'});
 }
 detailBack.addEventListener('click',closeBook);
 // Each named portal has its own published source and distinct selection.
 let portalTicket=0,activePortal='all';
 function openCollection(origin='館藏總索引',title=''){
  if(!detail.hidden)closeBook();
  wall.hidden=true;catalogue.hidden=false;activePortal=origin==='館藏總索引'?'all':origin;
  catalogueFocus.textContent=activePortal==='all'?'':origin;
  const catalogueTitle=$('#dawn-catalogue-title');
  if(catalogueTitle)catalogueTitle.textContent=activePortal==='all'?'全部館藏':origin;
  renderChannelIntroduction(activePortal);
  second.scrollTo({top:catalogue.offsetTop,behavior:'instant'});
  const ticket=++portalTicket;
  if(activePortal==='all'){
   portalTopics?.remove();portalTopics=null;editorialWorks=[];
   search.disabled=false;search.value=title||'';
   loadCatalogue();
   if(currentPage)renderWorks();
  }else{
   search.disabled=true;search.value='';
   prevButton.disabled=true;more.disabled=true;
   works.replaceChildren();
   pageStatus.textContent='';
   showPortalCollection(activePortal,ticket);
  }
 }
 const portalIntro=$('#dawn-catalogue-introduction');
 const channelCopy={
  '三晨星':[
   '三晨星不是按銷量、年代或書架位置排列的暢銷榜，而是從書局作品中挑選值得反覆閱讀的三部著作。每一次推薦都應能回答：這部書提出什麼重要問題，它如何幫助我們理解信仰、歷史與生命？',
   '選書保留原著身份與版本線索，讀者可以由這三部書進入作者的思想，再逐步延伸到相關作品。這裡重視深入閱讀，而非以書量製造豐富的假象。'
  ],
  '策展集':[
   '一座城市可以在地圖、手抄本、版畫、攝影和考古重建中呈現完全不同的面貌。《耶路撒冷三千年》以作品之間的對照展開：同一個地方如何被朝聖者描繪、被史家書寫、被藝術家想像，又如何進入現代測繪與攝影。',
   '每件圖像都應回到自己的年代、媒材與原始來源。歷史見證、藝術寓言和當代重建不能混作同一種證據；它們相互並置，才使策展成為一條有論點的閱讀路徑。'
  ],
  '光譜':[
   '閱讀不能只停在單一學科的書目。聖經詮釋需要歷史背景，教會思想與哲學問題彼此對話；人物的生命經驗也常常照見一個時代的信仰、制度與文化。',
   '光譜以聖經與信仰、教會歷史、歷史與考古、哲學與思想、傳記與生命五條線索組織作品。分類是發現書與書之間關係的入口，而不是把不同知識封存在互不往來的房間。'
  ]
 };
 function renderChannelIntroduction(channel){
  if(!portalIntro)return;
  portalIntro.replaceChildren();
  if(channel==='all'){portalIntro.hidden=true;return}
  for(const text of channelCopy[channel]||[]){const p=document.createElement('p');p.textContent=text;portalIntro.append(p)}
  portalIntro.hidden=!portalIntro.childElementCount;
 }
 let editorialManifest=null,activeTopic='all',editorialWorks=[],portalTopics=null;
 async function loadEditorialChannels(){
  if(editorialManifest)return editorialManifest;
  const response=await fetch('/dawn-library/p2-editorial-channels.json');
  if(!response.ok)throw Error('Collection index unavailable');
  editorialManifest=await response.json();return editorialManifest;
 }
 function editorialTabBar(kind,topics){
  portalTopics?.remove();portalTopics=null;
  if(!Array.isArray(topics)||topics.length<2)return;
  const bar=document.createElement('nav');bar.className='dawn-catalogue__topics';bar.setAttribute('aria-label',kind+'分類');
  topics.forEach((t,i)=>{
   const button=document.createElement('button');button.type='button';button.textContent=t.label;
   button.setAttribute('aria-pressed',String(i===0));button.dataset.topic=t.id;
   button.addEventListener('click',()=>{
    activeTopic=t.id;
    bar.querySelectorAll('button').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));
    renderPortalWorks(editorialWorks.filter(w=>topicMatches(kind,w,t)),kind);
   });
   bar.append(button);
  });
  works.before(bar);portalTopics=bar;activeTopic=topics[0].id;
 }
 function topicMatches(kind,work,topic){
  if(topic.id==='all'||kind==='三晨星')return true;
  if(kind==='光譜')return work.editorialTopic===topic.id;
  if(kind==='策展集')return topic.mediums.some(m=>{
   const medium=String(work.curationMedium||'').toLowerCase();
   return medium===m||medium.includes(m);
  });
  return true;
 }
 async function showPortalCollection(kind,ticket){
  const list=[];
  try{
   const config=(await loadEditorialChannels()).channels[kind];if(!config)throw Error('Editorial channel unavailable');
   if(kind==='三晨星'){
    const response=await fetch(config.source);if(!response.ok)throw Error('Morning selection missing');
    const data=await response.json();
    const ids=(data.items||[]).map(x=>x.workId).filter(Boolean);
    const lib=await import('/dawn-library/product/library-system.mjs');
    const matched=await lib.dawnLibrary.works(ids);
    ids.forEach(id=>{const w=matched.get(id);if(w)list.push({title:w.title,creator:(w.authors||[]).join(' · '),workId:w.workId,cover:w.cover,authorityIds:w.authorityIds,edition:w.edition})});
   }else if(kind==='策展集'){
    const response=await fetch(config.source);if(!response.ok)throw Error('Exhibition missing');
    const data=await response.json();
    const introductionIndex=await getBookIntroductionIndex().catch(()=>({items:{}}));
    for(const item of data.items||[])list.push({id:item.id,title:item.title,creator:item.creator,date:item.year,curationMedium:item.curationMedium,editorialParagraphs:introductionIndex.items?.[item.id]||[],illustration:{url:item.media?.src,alt:item.media?.alt,source:item.media?.source,credit:item.creator},sourceUrl:item.sourceWork||item.destination});
   }else if(kind==='光譜'){
    const response=await fetch(config.source);if(!response.ok)throw Error('Disciplinary shelves missing');
    const data=await response.json(),byId=new Map();
    for(const topic of config.topics)for(const id of topic.shelves||[]){
     const shelf=(data.shelves||[]).find(x=>x.id===id);
     (shelf?.items||[]).slice(0,config.selectionPerShelf||8).forEach(x=>{
      if(x.workId&&!byId.has(x.workId))byId.set(x.workId,topic.id);
     });
    }
    const lib=await import('/dawn-library/product/library-system.mjs');
    const matches=await lib.dawnLibrary.works([...byId.keys()]);
    byId.forEach((topic,id)=>{const w=matches.get(id);if(w)list.push({title:w.title,creator:(w.authors||[]).join(' · '),workId:w.workId,cover:w.cover,authorityIds:w.authorityIds,edition:w.edition,editorialTopic:topic})});
   }
   await Promise.all([loadCatalogueCoverLookup(),loadVisualLookup()]);
   if(ticket!==portalTicket||activePortal!==kind)return;
   editorialWorks=list;
   editorialTabBar(kind,config.topics);
   renderPortalWorks(list.filter(w=>topicMatches(kind,w,config.topics?.[0]||{id:'all'})),kind);
  }catch(err){if(ticket!==portalTicket)return;console.warn('[Dawn editorial channels]',err);pageStatus.textContent='館藏暫時無法載入。'}
 }
 function renderPortalWorks(items,kind){
  const frag=document.createDocumentFragment();
  items.forEach((work,i)=>{
   const li=document.createElement('li');li.className='dawn-catalogue__sleeve';
   const source=coverLookup?.get(normalizeTitle(work.title));
   const art=imageFor(work,source);
   const card=document.createElement('button');card.type='button';
   card.className='dawn-catalogue__cover-card'+(art?' dawn-catalogue__cover-card--image':' dawn-catalogue__cover-card--unresolved');
   card.setAttribute('aria-label','閱讀：'+work.title);
   if(art){
    const img=document.createElement('img');img.loading='lazy';img.decoding='async';img.src=art.url;img.alt=art.alt||work.title;
    img.onerror=()=>{img.remove();card.classList.remove('dawn-catalogue__cover-card--image');card.classList.add('dawn-catalogue__cover-card--unresolved')};
    card.append(img);
   }
   const copy=document.createElement('div');copy.className='dawn-catalogue__cover-typography';
   const num=document.createElement('small');num.textContent=String(i+1).padStart(2,'0');
   const title=document.createElement('strong');title.textContent=work.title;
   const author=document.createElement('span');author.textContent=work.creator||'';
   const year=document.createElement('small');year.textContent=work.date||'';
   copy.append(num,title,author,year);card.append(copy);
   card.addEventListener('click',()=>openBook(work,'catalogue'));
   li.append(card);frag.append(li);
  });
  works.replaceChildren(frag);
  pageStatus.textContent=items.length?String(items.length)+' 部作品':'本分類目前沒有可顯示的作品。';
 }
 function closeCollection(){++portalTicket;activePortal='all';portalTopics?.remove();portalTopics=null;editorialWorks=[];search.disabled=false;if(!detail.hidden)closeBook();catalogue.hidden=true;wall.hidden=false;search.value='';second.scrollTo({top:wall.offsetTop,behavior:'instant'})}
 openCatalogue.addEventListener('click',()=>openCollection());
 openCatalogueTop?.addEventListener('click',()=>openCollection());
 closeCatalogue.addEventListener('click',closeCollection);
 wallGrid.addEventListener('click',e=>{
  const tile=e.target.closest('button');if(!tile)return;
  if(tile.dataset.dawnPortal)openCollection(tile.dataset.dawnPortal);
  else if(tile.dataset.workTitle){
   const source=coverLookup?.get(normalizeTitle(tile.dataset.workTitle));
   openBook({...source,title:source?.title||tile.dataset.workTitle,creator:source?.author||'',sourceUrl:source?.source?.url},'wall');
  }
 });
 async function loadWallCovers(){
  if(wallGrid.dataset.loaded==='true'||wallGrid.dataset.loading==='true')return;
  wallGrid.dataset.loading='true';
  try{
   await Promise.all([loadCatalogueCoverLookup(),loadVisualLookup()]);
   const response=await fetch('/dawn-library/storefront.json');
   if(!response.ok)throw Error('Storefront covers '+response.status);
   const storefront=await response.json();
   const shelves=shelvesOf(storefront);
   const curated=[],primary=(shelves.find(s=>String(s.title||'').includes('Standard Ebooks'))?.items||[]).filter(w=>w.cover?.url&&w.source?.url);
   primary.slice(0,12).forEach(w=>curated.push(w));
   for(const shelf of shelves){
    for(const w of shelf.items||[]){
     if(curated.length>=18)break;
     if(w.cover?.url&&w.source?.url&&!curated.some(v=>v.title===w.title))curated.push(w);
    }
    if(curated.length>=18)break;
   }
   const frag=document.createDocumentFragment();
   curated.forEach(work=>{
    const tile=document.createElement('button');tile.type='button';tile.className='dawn-wall__tile dawn-wall__tile--record dawn-cover';
    tile.dataset.workTitle=work.title;tile.setAttribute('aria-label','閱讀：'+work.title);
    const sleeve=document.createElement('span');sleeve.className='dawn-cover__sleeve';
    const img=document.createElement('img');img.src=work.cover.url;img.alt='原書封面：'+work.title;img.loading='lazy';img.decoding='async';img.referrerPolicy='no-referrer';
    img.addEventListener('error',()=>{tile.classList.add('dawn-cover--missing');sleeve.hidden=true});sleeve.append(img);
    const meta=document.createElement('span');meta.className='dawn-cover__meta';
    const title=document.createElement('strong');title.textContent=work.title;
    const author=document.createElement('em');author.textContent=work.author||'';
    meta.append(title,author);tile.append(sleeve,meta);frag.append(tile);
   });
   wallGrid.append(frag);wallGrid.dataset.loaded='true';
  }catch(err){console.error('[Dawn covers]',err);wallGrid.dataset.loading='error'}
 }
 async function loadCatalogue(){if(!index){try{const r=await fetch('/dawn-library/catalogue/index.json');if(!r.ok)throw Error('Catalogue index unavailable');index=await r.json();total.textContent=Number(index.count).toLocaleString('en-CA')}catch(e){pageStatus.textContent='館藏暫時未能載入';console.error(e);return}}if(!currentPage)await showPage(1)}
 async function showPage(page){if(activePortal!=='all'||loading||!index||page<1||page>index.pageCount)return;loading=true;more.disabled=true;prevButton.disabled=true;
  try{if(!cache.has(page)){const file=index.pages[page-1],r=await fetch('/dawn-library/catalogue/'+file);if(!r.ok)throw Error('Missing catalogue page '+page);
   const data=await r.json();cache.set(page,data.works||[])}
   currentPage=page;loaded=cache.get(page);search.value='';await Promise.all([loadCatalogueCoverLookup(),loadVisualLookup()]);renderWorks();if(page===1)loadWallCovers();
  }catch(e){pageStatus.textContent='館藏載入中斷，請重試';console.error(e)}
  finally{loading=false;more.disabled=currentPage>=index.pageCount;prevButton.disabled=currentPage<=1}
 }
 function renderWorks(){
  if(activePortal!=='all')return;
  const needle=search.value.trim().toLocaleLowerCase();
  const matches=loaded.filter(w=>!needle||[w.title,w.creator,String(w.date||'')].some(v=>String(v||'').toLocaleLowerCase().includes(needle)));
  const frag=document.createDocumentFragment();
  matches.forEach(work=>{
   const li=document.createElement('li');li.className='dawn-catalogue__sleeve';
   const source=coverLookup?.get(normalizeTitle(work.title));
   const visual=imageFor(work,source);
   const card=document.createElement('button');card.type='button';card.className='dawn-catalogue__cover-card'+(visual?' dawn-catalogue__cover-card--image':' dawn-catalogue__cover-card--unresolved');
   card.setAttribute('aria-label','閱讀：'+(work.title||'Untitled'));
   card.addEventListener('click',()=>openBook({...work,sourceUrl:source?.source?.url},'catalogue'));
   if(visual){
    const img=document.createElement('img');img.src=visual.url;img.alt=visual.alt;img.loading='lazy';img.decoding='async';
    img.addEventListener('error',()=>{img.remove();card.classList.remove('dawn-catalogue__cover-card--image');card.classList.add('dawn-catalogue__cover-card--unresolved')});
    card.append(img);
   }
   const text=document.createElement('div');text.className='dawn-catalogue__cover-typography';
   const folio=document.createElement('small');folio.textContent=String((currentPage-1)*index.pageSize+loaded.indexOf(work)+1).padStart(5,'0');
   const title=document.createElement('strong');title.textContent=work.title||'UNTITLED';
   const creator=document.createElement('span');creator.textContent=work.creator||'作者未詳';
   const footer=document.createElement('small');footer.textContent=work.date?String(work.date):'';
   text.append(folio,title,creator,footer);card.append(text);li.append(card);frag.append(li);
  });
  works.replaceChildren(frag);
  pageStatus.textContent='第 '+currentPage+' / '+index.pageCount+' 頁 · '+matches.length+' 筆 · 全部 '+Number(index.count).toLocaleString('en-CA')+' 筆';
 }
 more.addEventListener('click',()=>showPage(currentPage+1));prevButton.addEventListener('click',()=>showPage(currentPage-1));search.addEventListener('input',renderWorks);
 const previewParams=new URLSearchParams(location.search);
 const requestedLayer=previewParams.get('layer');
 const initial=Number(previewParams.get('d')??26.1);
 requestAnimationFrame(()=>requestAnimationFrame(()=>{
  // Direct review URL: enter the actual second/third reading layer without
  // asking the reviewer to discover the long scroll + 7.6s click gesture.
  // Normal P2 interaction and reversible V9 motion remain unchanged.
  const direct=requestedLayer==='second'||requestedLayer==='catalogue';
  jump(direct?Math.max(28.4,Number.isFinite(initial)?initial:28.4):(Number.isFinite(initial)?initial:26.1));
  if(direct){
   entryProgress=entryClock=entryTarget=1;
   void loadWallCovers();
   schedule();
   if(requestedLayer==='catalogue')openCollection();
  }
 }));
})();
