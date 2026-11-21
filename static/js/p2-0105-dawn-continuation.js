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
 const plates=[$('#dawn-plate-zh'),$('#dawn-plate-en')];
 const search=$('#dawn-search'),works=$('#dawn-works');
 const more=$('#dawn-more'),prevButton=$('#dawn-prev'),pageStatus=$('#dawn-page-status'),total=$('#dawn-total');
 const wall=$('#dawn-wall'),wallGrid=$('#dawn-wall-grid'),catalogue=$('#dawn-catalogue'),catalogueFocus=$('#dawn-catalogue-focus');
 const openCatalogue=$('#dawn-open-catalogue'),closeCatalogue=$('#dawn-close-catalogue');
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
 const ns='http://www.w3.org/2000/svg';
 function svg(name,attrs={}){const e=document.createElementNS(ns,name);for(const [k,v] of Object.entries(attrs))e.setAttribute(k,v);return e}
 function textNode(group,str,x,y,size,color){const n=svg('text',{x,y,'font-size':size,fill:color,'font-family':'Bodoni Moda SC,Georgia,serif'});n.textContent=str;group.append(n);return n}
 const kinetic=svg('svg',{'aria-hidden':'true'}),defs=svg('defs');kinetic.append(defs);
 const clip=svg('clipPath',{id:'p205-v9-clip'}),aperture=svg('rect',{x:800,y:0,width:0,height:108});clip.append(aperture);defs.append(clip);
 const sheetGroup=svg('g');kinetic.append(sheetGroup);
 // Full-screen sevenfold rects removed by editorial direction.
 const banner=svg('g',{'clip-path':'url(#p205-v9-clip)'}),topRule=svg('path',{d:'M0 1H1600',stroke:gold,'stroke-width':1,fill:'none'}),bottomRule=svg('path',{d:'M0 107H1600',stroke:gold,'stroke-width':1,fill:'none'});
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
  handoff.style.visibility=p>.001&&!complete?'visible':'hidden';
  second.style.visibility=p>.64?'visible':'hidden';
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
  const ink=hexMix(gold,sevenInk(p),ease((p-.07)/.13));letters.setAttribute('fill',ink);topRule.setAttribute('stroke',ink);bottomRule.setAttribute('stroke',ink);banner.setAttribute('opacity',String(1-ease((p-.59)/.13)));
  const source=squares.map(node=>node.getBoundingClientRect());const target=plates.map(node=>node.getBoundingClientRect());
  const lift=ease((p-.015)/.17),cross=ease((p-.18)/.34),land=ease((p-.58)/.15),capHeight=100*scale;
  seals.forEach((seal,i)=>{
   const src=source[i],dst=target[i],s0=src.width,sz=mix(mix(s0,capHeight,lift),dst.width,land);
   const sourceX=src.left-bounds.left+src.width/2,sourceY=src.top-bounds.top+src.height/2;
   const stationX=bx+bw*(i?.68:.43),stationY=by+bh/2;
   const endX=dst.left-bounds.left+dst.width/2,endY=dst.top-bounds.top+dst.height/2;
   const cx=mix(mix(sourceX,stationX,cross),endX,land),cy=mix(mix(sourceY,stationY,lift),endY,land);
   seal.g.setAttribute('transform',`translate(${cx-sz/2} ${cy-sz/2}) scale(${sz/500})`);
   seal.g.setAttribute('opacity',String(1-ease((p-.76)/.14)));
   const currentSealInk=hexMix(i?papyrus:harvest,sevenInk(p),ease((p-.14)/.66));
   seal.shell.setAttribute('fill',currentSealInk);
   seal.shell.setAttribute('stroke',ink);
   seal.initial.querySelectorAll('text').forEach(n=>n.setAttribute('fill',hexMix(i?harvest:paper,paper,ease((p-.14)/.66))));
   seal.initial.setAttribute('opacity',1-ease((p-.13)/.18));seal.copy.setAttribute('opacity',ease((p-.57)/.12)*(1-ease((p-.74)/.14)));
   // The two real second-layer plates are the physical targets: no last-frame jump.
  });
 }
 function resetEntry(){if(rafId)cancelAnimationFrame(rafId);rafId=0;entryClock=entryProgress=entryTarget=0;catalogue.hidden=true;wall.hidden=false;second.scrollTop=0;schedule()}
 function animateEntry(target){if(rafId)cancelAnimationFrame(rafId);entryTarget=target;
  const from=entryProgress,start=performance.now(),duration=target?7600:0;
  if(!duration||matchMedia('(prefers-reduced-motion: reduce)').matches){entryClock=entryProgress=target;schedule();if(target){loadCatalogue();loadWallCovers();}return;}
  const tick=now=>{entryProgress=mix(from,target,clamp((now-start)/duration));entryClock=entryProgress;schedule();
   if(Math.abs(entryProgress-target)>.0001)rafId=requestAnimationFrame(tick);else{rafId=0;if(target){loadCatalogue();loadWallCovers();}}};
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
 function appendReaderText(message){const p=document.createElement('p');p.textContent=message;detailText.append(p)}
 async function openBook(work,from){
  if(!work?.title)return;
  const ticket=++detailTicket;
  returnTo=from||(!catalogue.hidden?'catalogue':'wall');returnScroll=second.scrollTop;activeBook=work;
  wall.hidden=true;catalogue.hidden=true;detail.hidden=false;
  detailTitle.textContent=work.title;detailAuthor.textContent=work.creator||work.author||'';
  detailEdition.textContent=work.date?String(work.date):'';
  detailText.replaceChildren();
  const source=coverLookup?.get(normalizeTitle(work.title));
  const visual=imageFor(work,source);
  setDetailImage(visual);
  const sourceUrl=safeHttp(work.sourceUrl||work.source?.url||source?.source?.url||visual?.workSource||visual?.source);
  if(sourceUrl){detailSource.href=sourceUrl;detailSource.hidden=false}else{detailSource.hidden=true;detailSource.removeAttribute('href')}
  appendReaderText('正在檢查本站可閱讀的內容…');
  second.scrollTo({top:detail.offsetTop,behavior:'instant'});
  try{
   const reader=await import('/js/dawn-reading-resolver.mjs');
   const pack=await reader.localReadingPack(work.workId||work.id);
   if(ticket!==detailTicket)return;
   detailText.replaceChildren();
   if(pack?.segments?.length){
    pack.segments.forEach(segment=>{
     const unit=document.createElement('div');unit.className='dawn-book-detail__paragraph';
     if(segment.source){const p=document.createElement('p');p.lang=pack.sourceLanguage||'en';p.textContent=segment.source;unit.append(p)}
     if(segment.translation){const p=document.createElement('p');p.lang='zh-Hant';p.textContent=segment.translation;unit.append(p)}
     detailText.append(unit);
    });
   }else{
    appendReaderText(sourceUrl?'本站尚未收錄此書的完整正文。可從下方來源查閱原書；書局頁面會保留，方便繼續選書。':'本站目前保留此書的書目資料；可閱讀的正文與原書連結尚待核實。');
   }
  }catch{
   if(ticket!==detailTicket)return;
   detailText.replaceChildren();appendReaderText('本站的閱讀內容暫時無法載入。');
  }
 }
 function closeBook(){
  if(detail.hidden)return;
  ++detailTicket;detail.hidden=true;activeBook=null;
  if(returnTo==='catalogue'){catalogue.hidden=false;wall.hidden=true}
  else{wall.hidden=false;catalogue.hidden=true}
  second.scrollTo({top:returnScroll,behavior:'instant'});
 }
 detailBack.addEventListener('click',closeBook);
 function openCollection(origin='館藏總索引',title=''){
  if(!detail.hidden)closeBook();
  wall.hidden=true;catalogue.hidden=false;
  catalogueFocus.textContent=origin==='館藏總索引'?'':origin;
  if(title&&currentPage){search.value=title;renderWorks()}else if(currentPage){search.value='';renderWorks()}
  second.scrollTo({top:catalogue.offsetTop,behavior:'instant'});
  loadCatalogue();
 }
 function closeCollection(){if(!detail.hidden)closeBook();catalogue.hidden=true;wall.hidden=false;search.value='';second.scrollTo({top:wall.offsetTop,behavior:'instant'})}
 openCatalogue.addEventListener('click',()=>openCollection());
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
 async function showPage(page){if(loading||!index||page<1||page>index.pageCount)return;loading=true;more.disabled=true;prevButton.disabled=true;
  try{if(!cache.has(page)){const file=index.pages[page-1],r=await fetch('/dawn-library/catalogue/'+file);if(!r.ok)throw Error('Missing catalogue page '+page);
   const data=await r.json();cache.set(page,data.works||[])}
   currentPage=page;loaded=cache.get(page);search.value='';await Promise.all([loadCatalogueCoverLookup(),loadVisualLookup()]);renderWorks();if(page===1)loadWallCovers();
  }catch(e){pageStatus.textContent='館藏載入中斷，請重試';console.error(e)}
  finally{loading=false;more.disabled=currentPage>=index.pageCount;prevButton.disabled=currentPage<=1}
 }
 function renderWorks(){
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
 const initial=Number(new URLSearchParams(location.search).get('d')??26.1);
 requestAnimationFrame(()=>requestAnimationFrame(()=>jump(Number.isFinite(initial)?initial:26.1)));
})();
