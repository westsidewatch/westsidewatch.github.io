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
 const token=['--ws-water','--ws-first-light','--ws-pale-gold','--ws-olive','--ws-harvest','--ws-crimson','--ws-daylight-mauve'];
 const osStyle=getComputedStyle(document.documentElement);
 const sampler=document.createElement('canvas');sampler.width=sampler.height=1;
 const ctx=sampler.getContext('2d',{willReadFrequently:true});
 function osColor(name,fallback){const raw=osStyle.getPropertyValue(name).trim();if(/^#[\da-f]{6}$/i.test(raw))return raw.toLowerCase();
  if(raw&&ctx&&window.CSS?.supports('color',raw)){ctx.clearRect(0,0,1,1);ctx.fillStyle=raw;ctx.fillRect(0,0,1,1);const data=ctx.getImageData(0,0,1,1).data;if(data[3]===255)return '#'+[...data].slice(0,3).map(v=>v.toString(16).padStart(2,'0')).join('');}return fallback;}
 const palette=token.map((t,i)=>osColor(t,['#5b8fa8','#a2872a','#cebd74','#738a5a','#b8944a','#a14d57','#b085ab'][i]));
 const harvest=palette[4],gold=osColor('--ws-morning-gold','#d2bc69'),paper=osColor('--ws-paper','#faf9f5'),papyrus=osColor('--ws-papyrus','#eee4c9');
 function hexMix(a,b,t){return '#'+[1,3,5].map(i=>Math.round(mix(parseInt(a.slice(i,i+2),16),parseInt(b.slice(i,i+2),16),clamp(t))).toString(16).padStart(2,'0')).join('')}
 function sevenInk(p){const t=clamp((p-.22)/.62)*6,i=Math.min(5,Math.floor(t));return hexMix(palette[i],palette[i+1],t-i)}
 const ns='http://www.w3.org/2000/svg';
 function svg(name,attrs={}){const e=document.createElementNS(ns,name);for(const [k,v] of Object.entries(attrs))e.setAttribute(k,v);return e}
 function textNode(group,str,x,y,size,color){const n=svg('text',{x,y,'font-size':size,fill:color,'font-family':'Bodoni Moda SC,Georgia,serif'});n.textContent=str;group.append(n);return n}
 const kinetic=svg('svg',{'aria-hidden':'true'}),defs=svg('defs');kinetic.append(defs);
 const clip=svg('clipPath',{id:'p205-v9-clip'}),aperture=svg('rect',{x:800,y:0,width:0,height:108});clip.append(aperture);defs.append(clip);
 const sheetGroup=svg('g');kinetic.append(sheetGroup);
 const sheets=palette.map(color=>{const rect=svg('rect',{x:0,y:0,width:1,height:0,fill:color});sheetGroup.append(rect);return rect});
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
  // Seven full-bleed sheets: each occupies the COMPLETE stage, not the banner.
  // Staggered vertical sweeps overlap with no exposed margin at any screen ratio.
  sheets.forEach((sheet,i)=>{
   const arrive=ease((p-.34-i*.033)/.19);
   const depart=ease((p-.72-i*.018)/.17);
   sheet.setAttribute('x',0);
   sheet.setAttribute('y',(-h*(1-arrive)+h*depart).toFixed(2));
   sheet.setAttribute('width',w);
   sheet.setAttribute('height',h);
  });
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
  if(!duration||matchMedia('(prefers-reduced-motion: reduce)').matches){entryClock=entryProgress=target;schedule();if(target)loadCatalogue();return;}
  const tick=now=>{entryProgress=mix(from,target,clamp((now-start)/duration));entryClock=entryProgress;schedule();
   if(Math.abs(entryProgress-target)>.0001)rafId=requestAnimationFrame(tick);else{rafId=0;if(target)loadCatalogue();}};
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
   img.addEventListener('error',()=>{img.style.opacity='0';});
   img.addEventListener('load',()=>{img.style.removeProperty('opacity');});
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
   // True counterflow: LEFT slides UP, RIGHT slides DOWN; no 3D page flip.
   const left=side.key==='left';
   const currentPct=(fraction*100).toFixed(2);
   const incomingPct=((1-fraction)*100).toFixed(2);
   side.current.style.clipPath=left
    ?`inset(0 0 ${currentPct}% 0)`
    :`inset(${currentPct}% 0 0 0)`;
   side.next.style.clipPath=left
    ?`inset(${incomingPct}% 0 0 0)`
    :`inset(0 0 ${incomingPct}% 0)`;
   // Keep both image surfaces flush to the stage. Motion comes from complementary
   // clipping masks; translating clipped images previously exposed a 12%-high
   // papyrus/ochre strip between consecutive plates.
   side.current.style.transform='none';
   side.next.style.transform='none';
   const shown=fraction>.5?scenes[ni]:scenes[i];
   if(side.node.href!==shown.href){
    side.node.href=shown.href;
    side.node.setAttribute('aria-label','查看 '+shown.title+' · 原始書籍或館藏');
   }
   side.title.textContent=shown.title;
   side.caption.textContent=shown.caption;
   side.node.querySelector('.dawn-world__rubric').textContent=shown.kind;
  }
 }

 // Actual Dawn Library catalogue: 21,047 records / 85 paged JSON files.
 // Fetch one page on demand. Never download the whole corpus on first paint.
 let index=null,currentPage=0,loading=false,loaded=[],cache=new Map();
 function openCollection(origin='館藏總索引',title=''){
  wall.hidden=true;catalogue.hidden=false;
  catalogueFocus.textContent=origin==='館藏總索引'?'館藏 · 歷史書籍與信仰資源':`從「${origin}」探索館藏`;
  if(title&&currentPage){search.value=title;renderWorks()}else if(currentPage){search.value='';renderWorks()}
  second.scrollTo({top:catalogue.offsetTop,behavior:'instant'});
  loadCatalogue();
 }
 function closeCollection(){catalogue.hidden=true;wall.hidden=false;search.value='';second.scrollTo({top:wall.offsetTop,behavior:'instant'})}
 openCatalogue.addEventListener('click',()=>openCollection());
 closeCatalogue.addEventListener('click',closeCollection);
 wallGrid.addEventListener('click',e=>{
  const tile=e.target.closest('button');if(!tile)return;
  if(tile.dataset.dawnPortal)openCollection(tile.dataset.dawnPortal);
  else if(tile.dataset.workTitle)openCollection('書籍',tile.dataset.workTitle);
 });
 function renderWall(records){
  if(wallGrid.dataset.loaded==='true')return;
  const fragment=document.createDocumentFragment();
  records.slice(0,18).forEach((work,i)=>{
   const tile=document.createElement('button'),num=document.createElement('small'),title=document.createElement('strong'),creator=document.createElement('em');
   tile.type='button';tile.className='dawn-wall__tile dawn-wall__tile--record';tile.style.setProperty('--tile-index',i);
   tile.dataset.workTitle=work.title||'';tile.setAttribute('aria-label',`${work.title||'Untitled'}；展開館藏索引`);
   num.textContent=String(i+1).padStart(3,'0');title.textContent=work.title||'Untitled';creator.textContent=work.creator||'作者未詳';
   tile.append(num,title,creator);fragment.append(tile);
  });
  wallGrid.append(fragment);wallGrid.dataset.loaded='true';
 }
 async function loadCatalogue(){if(!index){try{const r=await fetch('/dawn-library/catalogue/index.json');if(!r.ok)throw Error('Catalogue index unavailable');index=await r.json();total.textContent=Number(index.count).toLocaleString('en-CA');}catch(e){pageStatus.textContent='館藏暫時未能載入';console.error(e);return;}}if(!currentPage)await showPage(1);}
 async function showPage(page){if(loading||!index||page<1||page>index.pageCount)return;loading=true;more.disabled=true;prevButton.disabled=true;
  try{if(!cache.has(page)){const file=index.pages[page-1],r=await fetch('/dawn-library/catalogue/'+file);if(!r.ok)throw Error('Missing catalogue page '+page);
   const data=await r.json();cache.set(page,data.works||[]);}
   currentPage=page;loaded=cache.get(page);search.value='';renderWorks();if(page===1)renderWall(loaded);}
  catch(e){pageStatus.textContent='館藏載入中斷，請重試';console.error(e)}
  finally{loading=false;more.disabled=currentPage>=index.pageCount;prevButton.disabled=currentPage<=1;}}
 function renderWorks(){const needle=search.value.trim().toLocaleLowerCase(),matches=loaded.filter(w=>!needle||[w.title,w.creator,String(w.date||'')].some(v=>String(v||'').toLocaleLowerCase().includes(needle)));
  const fragment=document.createDocumentFragment();matches.forEach((work,i)=>{
   const li=document.createElement('li'),num=document.createElement('span'),title=document.createElement('h3'),creator=document.createElement('p'),date=document.createElement('span');
   num.className='work-number';num.textContent=String((currentPage-1)*index.pageSize+loaded.indexOf(work)+1).padStart(4,'0');
   title.textContent=work.title||'Untitled';creator.className='work-creator';creator.textContent=work.creator||'作者未詳';
   date.className='work-date';date.textContent=work.date?String(work.date):'HISTORICAL EDITION';li.append(num,title,creator,date);fragment.append(li);
  });works.replaceChildren(fragment);pageStatus.textContent=`第 ${currentPage} / ${index.pageCount} 頁 · ${matches.length} 筆 · 全部 ${Number(index.count).toLocaleString('en-CA')} 筆`;
 }
 more.addEventListener('click',()=>showPage(currentPage+1));prevButton.addEventListener('click',()=>showPage(currentPage-1));search.addEventListener('input',renderWorks);
 const initial=Number(new URLSearchParams(location.search).get('d')??26.1);
 requestAnimationFrame(()=>requestAnimationFrame(()=>jump(Number.isFinite(initial)?initial:26.1)));
})();
