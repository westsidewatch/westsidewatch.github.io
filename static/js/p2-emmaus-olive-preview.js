/* P2 candidate 03/04: one vertical scroll owner, two coupled editorial scenes.
 * The approved Church/Vol.00 iframe is read-only and unchanged.
 * This script only runs on /experiments/p2-emmaus-olive-handoff-lab.html.
 */
(()=>{'use strict';
 const $=s=>document.querySelector(s),clamp=(v,a=0,b=1)=>Math.min(b,Math.max(a,v)),smooth=t=>{t=clamp(t);return t*t*(3-2*t)};
 const track=$('#proof-track'),base=$('#proof-original'),emmaus=$('#emmaus'),olive=$('#olive-proof');
 const seek=$('#proof-seek'),percent=$('#proof-percentage'),phase=$('#proof-phase');
 if(!track||!base||!emmaus||!olive)return;
 const reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;
 const books=window.ONE_DATA?.books;
 if(!Array.isArray(books)||books.length!==66)throw Error('Canonical ONE 66-book data was not loaded');
 const rail=$('#emmaus-rail'),bookEn=$('#em-book-en'),bookZh=$('#em-book-zh'),bookNum=$('#em-book-number'),bookPart=$('#em-book-part'),bookChapters=$('#em-book-chapters');
 let selectedBook=40;
 function centerRailBook(button,behavior='smooth'){
  if(!button)return;
  // Only the horizontal ONE strip moves. scrollIntoView() can also scroll
  // the sticky P2 page vertically, which would disturb the seven-venue handoff.
  const railRect=rail.getBoundingClientRect(),bookRect=button.getBoundingClientRect();
  const left=rail.scrollLeft+(bookRect.left-railRect.left)-(rail.clientWidth-bookRect.width)/2;
  rail.scrollTo({left:Math.max(0,left),behavior});
 }
 function selectBook(number,center=true){
  const book=books.find(b=>b[0]===number);if(!book)return;
  selectedBook=number;bookEn.textContent=book[2];bookZh.textContent=book[1];
  bookNum.textContent='BOOK '+String(number).padStart(2,'0');
  bookPart.textContent=number<=39?'OLD TESTAMENT':'NEW TESTAMENT';
  bookChapters.textContent=book[3]+' CHAPTERS';
  $('#emmaus-enter').href='/one/?book='+number+'&chapter=1';
  $('#em-plate-selection').textContent='BOOK '+String(number).padStart(2,'0')+' / '+book[2].toUpperCase();
  rail.querySelectorAll('button').forEach(b=>b.setAttribute('aria-pressed',String(Number(b.dataset.book)===number)));
  const active=rail.querySelector(`[data-book="${number}"]`);
  if(center)centerRailBook(active,reduced?'instant':'smooth');
  emmaus.dataset.selectedBook=String(number);
 }
 for(const item of books){
  const b=document.createElement('button');b.type='button';b.className='emmaus__number';b.dataset.book=String(item[0]);
  b.innerHTML=String(item[0]).padStart(2,'0')+'<span>BOOK</span>';
  b.setAttribute('aria-label',String(item[0]).padStart(2,'0')+' '+item[1]+' / '+item[2]);
  b.addEventListener('click',()=>selectBook(item[0]));rail.append(b);
 }
 rail.addEventListener('keydown',e=>{
  if(e.key==='ArrowRight'||e.key==='ArrowLeft'){
   e.preventDefault();selectBook(clamp(selectedBook+(e.key==='ArrowRight'?1:-1),1,66));
   rail.querySelector(`[data-book="${selectedBook}"]`)?.focus({preventScroll:true});
  }
 });
 // Browsers can consume vertical wheel events on an overflow-x:auto strip,
 // even when overflow-y is hidden. Bridge that delta to the single P2 page
 // scroller; never turn the 66-book navigator into a nested vertical scene.
 rail.addEventListener('wheel',event=>{
  if(!event.deltaY||event.ctrlKey)return;
  event.preventDefault();
  const delta=event.deltaY*(event.deltaMode===1?16:event.deltaMode===2?innerHeight:1);
  scrollBy({top:delta,behavior:'instant'});
 },{passive:false});
 // Horizontal pointer-drag only; P2's vertical wheel/touch remains the sole
 // realm-to-realm navigation. No nested vertical scroll container is created.
 let pointer=null;
 rail.addEventListener('pointerdown',e=>{if(e.pointerType==='mouse'&&e.button!==0)return;pointer={id:e.pointerId,x:e.clientX,origin:rail.scrollLeft,moved:false};});
 rail.addEventListener('pointermove',e=>{if(!pointer||pointer.id!==e.pointerId)return;const dx=e.clientX-pointer.x;if(Math.abs(dx)>5){pointer.moved=true;rail.scrollLeft=pointer.origin-dx;}});
 rail.addEventListener('pointerup',()=>{pointer=null});rail.addEventListener('pointercancel',()=>{pointer=null});
 selectBook(40,false);
 requestAnimationFrame(()=>centerRailBook(rail.querySelector('[data-book="40"]'),'instant'));
 // Once the Magazine's city/wall plate has arrived on the right, switch
 // to the canonical 241-plate library in original catalogue order. The right
 // field never invents book-specific images or reuses the city-only shortlist.
 const registry=window.ONE_DORE_COVER_REGISTRY;
 const ids=Array.from({length:241},(_,i)=>i+1);
 const plates=ids.map(id=>({id,file:registry?.files?.[id],title:registry?.titles?.[id]||String(registry?.files?.[id]||'').replace(/^\d+[A-Z]?\./,'').replace(/\.[^.]+$/,'')}));
 if(plates.length!==241||plates.some(p=>!p.file))throw Error('Shared Doré 241-plate inventory is incomplete');
 const plateEls=[$('#em-plate-a'),$('#em-plate-b')];let galleryIndex=0,activeSlot=0,galleryTimer=0,galleryLive=false,plateVersion=0,galleryPrefetch=false;
 const imgUrl=plate=>'https://commons.wikimedia.org/wiki/Special:Redirect/file/'+encodeURIComponent(plate.file)+'?width=1200';
 async function showPlate(index){
  const ticket=++plateVersion,plate=plates[index%plates.length],slot=1-activeSlot,img=plateEls[slot];
  const ok=await new Promise(resolve=>{
   img.onload=()=>resolve(true);img.onerror=()=>resolve(false);img.src=imgUrl(plate);
   if(img.complete&&img.naturalWidth>0)resolve(true);
  });
  if(ticket!==plateVersion)return;
  if(!ok){galleryIndex=index%plates.length;return;}// A missing Commons file never permanently blocks the rest of the collection.
  plateEls[activeSlot].classList.remove('is-active');img.classList.remove('is-active');void img.offsetHeight;img.classList.add('is-active');
  activeSlot=slot;galleryIndex=index%plates.length;
  $('#em-plate-title').textContent='DORÉ / '+plate.title.toUpperCase();
  $('#em-plate-index').textContent=String(galleryIndex+1).padStart(2,'0')+' / '+String(plates.length).padStart(2,'0');
  emmaus.dataset.dorePlate=String(plate.id);
 }
 function syncGallery(live){
  if(live===galleryLive)return;galleryLive=live;clearInterval(galleryTimer);galleryTimer=0;
  if(live){if(!plateEls.some(img=>img.classList.contains('is-active')))showPlate(galleryIndex);if(!reduced)galleryTimer=setInterval(()=>showPlate(galleryIndex+1),15000);}
 }
 const roster=[
  ['watchman-nee','倪柝聲','WATCHMAN NEE'],['derek-prince','葉光明','DEREK PRINCE'],
  ['david-pawson','大衛鮑森','DAVID PAWSON'],['stephen-tong','唐崇榮','STEPHEN TONG'],
  ['huang-shuhua','黃淑華','HUANG SHUHUA'],['kang-lai-chang','康來昌','KANG LAI-CHANG'],
  ['jerry-lai','賴若瀚','JERRY LAI'],['tong-liu','劉彤','TONG LIU'],
  ['jiang-xiuqin','江秀琴','GRACE CHIANG'],['rick-warren','華理克','RICK WARREN'],
  ['yu-hong-jie','于宏潔','YU HONGJIE'],['kou-shao-en','寇紹恩','KOU SHAO-EN']
 ];
 const names=$('#olive-speaker-names'),mainImg=$('#olive-main-image'),main=$('#olive-main'),nextImg=$('#olive-next-image');let currentSpeaker=0;
 const emLeft=$('.emmaus__left'),emRight=$('.emmaus__right'),emPlates=$('.emmaus__plates');
 const oliveHero=$('#olive-morph-hero'),oliveEditorial=$('.olive-proof__editorial'),oliveRegister=$('.olive-proof__register'),oliveWindow=$('.olive-proof__window');
 const heroFolio=$('.olive-proof__hero-folio');
 let galleryBorrowed=false,archiveForOlive=null,sourceStyleDoc=null;
 function chooseSpeaker(index){
  currentSpeaker=index;const [slug,zh,en]=roster[index];
  mainImg.src='/images/olive/'+slug+'-editorial.png';mainImg.alt=zh;
  main.querySelector('olive-speaker-baseline')?.remove();
  const protectedName=document.createElement('olive-speaker-baseline');protectedName.dataset.speaker=slug;protectedName.setAttribute('aria-hidden','true');main.append(protectedName);
  const next=roster[(index+1)%roster.length];nextImg.src='/images/olive/'+next[0]+'-editorial.png';nextImg.alt=next[1];
  $('#olive-next-name').textContent=next[2]+' · '+next[1];
  names.querySelectorAll('button').forEach((b,i)=>b.setAttribute('aria-pressed',String(i===index)));
  olive.dataset.speaker=slug;
 }
 roster.forEach(([slug,zh,en],i)=>{
  const b=document.createElement('button');b.type='button';b.innerHTML=en+'<small>'+zh+'</small>';
  b.dataset.speaker=slug;b.setAttribute('aria-label','選擇講員 '+zh);b.addEventListener('click',()=>chooseSpeaker(i));names.append(b);
 });
 chooseSpeaker(0);
 let transferFigure=null,transferHome=null,transferNext=null,transferStyle=null;
 let sourceOriginalTileOpacity=null,sourceOriginalCoverOpacity=null;
 let frameLoaded=false,lastPaint=NaN,queued=false;
 function paint(){
  queued=false;const vh=Math.max(1,innerHeight),top=track.getBoundingClientRect().top;
  const distance=clamp(-top/vh,0,12),legacyDistance=Math.min(distance,6.5),churchEnd=3.0775,magazineEnd=6.5;
  let legacy;
  if(top>0)legacy=clamp((vh-top)/vh,0,1)*.1/2.9;
  else if(legacyDistance<=churchEnd){const scene=legacyDistance<=1.8?.1+legacyDistance*(.4/1.8):.5+(legacyDistance-1.8);legacy=scene/2.9;}
  else{const scene=2.37+(legacyDistance-churchEnd)/(magazineEnd-churchEnd)*(4-2.37);legacy=scene<=2.9?.75*scene/2.9:.75+.25*(scene-2.9)/1.1;}
  if(frameLoaded)base.contentWindow?.postMessage({type:'westside-p2-scroll',progress:clamp(legacy),active:distance<6.6},location.origin);
  // Same MERSI image object: Magazine LEFT engraving actually travels to
  // the existing RIGHT cover rectangle. No replica image is created.
  // Only once it arrives does the full Doré archive take over silently;
  // ONE reveals TOP to BOTTOM, then BOTH panels expand to fill the screen.
  const move=smooth((distance-6.50)/.90);
  const archive=smooth((distance-7.40)/.28);
  const oneDrop=smooth((distance-7.66)/.78);
  const expand=smooth((distance-8.44)/.48);
  const oliveIn=smooth((distance-9.44)/1.38);
  const emShowing=move>.001&&oliveIn<.999,oliveShowing=oliveIn>.001;
  emmaus.style.visibility=emShowing?'visible':'hidden';emmaus.style.opacity='1';emmaus.style.transform='none';
  const emInteractive=oneDrop>.999&&expand>.999&&oliveIn<.01;
  emmaus.style.pointerEvents=emInteractive?'auto':'none';emmaus.inert=!emInteractive;
  emmaus.setAttribute('aria-hidden',emInteractive?'false':'true');

  const sourceFrame=base.contentDocument?.querySelector('.p2-magazine iframe:not(.p2-magazine__home-film)');
  const sourceDoc=sourceFrame?.contentDocument;
  const sourceTile=sourceDoc?.getElementById('dual-contents');
  const sourceCover=sourceDoc?.getElementById('dual-cover');
  const sourceFigure=transferFigure||sourceDoc?.getElementById('dual-dore-plate');
  const frameRect=sourceFrame?.getBoundingClientRect(),baseRect=base.getBoundingClientRect(),stageRect=$('#proof-stage').getBoundingClientRect();
  const bounds=node=>{
   if(!node||!frameRect)return null;
   const r=node.getBoundingClientRect();
   return {x:baseRect.left-stageRect.left+frameRect.left+r.left,
           y:baseRect.top-stageRect.top+frameRect.top+r.top,w:r.width,h:r.height};
  };
  const original=bounds(sourceTile),coverBounds=bounds(sourceCover);
  // As the SAME engraving leaves the Magazine, its abandoned Contents
  // typography withdraws and the previous cover clears at the receiving end.
  // These are preview-iframe-only inline changes, restored on reverse scroll.
  if(sourceDoc&&sourceStyleDoc!==sourceDoc){
   sourceStyleDoc=sourceDoc;sourceOriginalTileOpacity=sourceTile?.style.opacity??'';
   sourceOriginalCoverOpacity=sourceCover?.style.opacity??'';
  }
  if(sourceTile&&sourceCover){
   if(move>.001){
    sourceTile.style.opacity=String(1-smooth(move/.60));
    sourceCover.style.opacity=String(1-smooth((move-.48)/.52));
   }else{
    sourceTile.style.opacity=sourceOriginalTileOpacity??'';
    sourceCover.style.opacity=sourceOriginalCoverOpacity??'';
   }
  }
  emmaus.style.backgroundColor=move>=.999?'#e7decbd9':'transparent';
  const lerp=(a,b,p)=>a+(b-a)*p;
  const poseRect=(el,a,b,p)=>{
   if(!a||!b)return;
   el.style.left=lerp(a.x,b.x,p).toFixed(2)+'px';
   el.style.top=lerp(a.y,b.y,p).toFixed(2)+'px';
   el.style.width=lerp(a.w,b.w,p).toFixed(2)+'px';
   el.style.height=lerp(a.h,b.h,p).toFixed(2)+'px';
  };
  if(move>.98&&!galleryPrefetch){
   galleryPrefetch=true;void showPlate(galleryIndex);
  }
  const archiveReady=plateEls.some(img=>img.classList.contains('is-active'));
  if(oliveIn<=.001)archiveForOlive=null;
  else if(archiveForOlive===null)archiveForOlive=archiveReady;
  // Lock the visible plate identity for a reversible 03→04 trip, even when
  // the public-domain image host loads during the midpoint of that journey.
  const useArchive=archiveForOlive===null?archiveReady:archiveForOlive;
  const fieldExit=1-smooth((oliveIn-.65)/.34);
  const fullLeft={x:0,y:0,w:stageRect.width*2/3,h:stageRect.height};
  const fullRight={x:stageRect.width*2/3,y:0,w:stageRect.width/3,h:stageRect.height};
  if(move>.001&&sourceFigure&&sourceTile&&coverBounds){
   if(!transferFigure){
    transferFigure=sourceFigure;transferHome=sourceTile;
    transferNext=sourceFigure.nextSibling;transferStyle=sourceFigure.getAttribute('style');
    $('#proof-stage').appendChild(sourceFigure);
   }
   poseRect(transferFigure,original,coverBounds,move);
   if(move>.999)poseRect(transferFigure,coverBounds,fullRight,expand);
   transferFigure.style.setProperty('--p2-transfer-visible',
    String(Math.max(0,1-(useArchive?archive:0))*fieldExit));
   transferFigure.dataset.p2Transferred='true';
  }else if(move<=.001&&transferFigure&&transferHome){
   transferHome.insertBefore(transferFigure,transferNext?.parentNode===transferHome?transferNext:null);
   if(transferStyle===null)transferFigure.removeAttribute('style');
   else transferFigure.setAttribute('style',transferStyle);
   transferFigure.removeAttribute('data-p2-transferred');
   transferFigure=null;transferHome=null;transferNext=null;transferStyle=null;
  }
  // The ONE field opens over the vacated Contents footprint, not from outside.
  poseRect(emLeft,original||fullLeft,fullLeft,expand);
  emLeft.style.clipPath='inset(0 0 '+((1-oneDrop)*100).toFixed(3)+'% 0)';
  poseRect(emRight,coverBounds||fullRight,fullRight,expand);
  emRight.style.clipPath='none';
  syncGallery(move>.98&&oliveIn<.001&&document.visibilityState==='visible');
  emRight.style.opacity=String(useArchive?archive:0);
  // Keep the moving plate visible all the way to the destination.
  // Only its editorial annotation recedes; the image itself must NOT vanish
  // at 32% progress and leave a blank travelling rectangle.
  emPlates.style.opacity='1';
  const annotations=1-smooth(oliveIn/.40);
  $('.emmaus__plate-top').style.opacity=String(annotations);
  $('.emmaus__plate-caption').style.opacity=String(annotations);
  $('.emmaus__gold-line').style.opacity=String(annotations);

  olive.style.visibility=oliveShowing?'visible':'hidden';
  olive.style.opacity='1';olive.style.clipPath='none';
  olive.style.backgroundColor=oliveIn>=.999?'#f0eee7':'transparent';
  olive.style.pointerEvents=oliveIn>.999?'auto':'none';olive.inert=oliveIn<=.999;
  olive.setAttribute('aria-hidden',oliveIn>.999?'false':'true');

  // Move the EXISTING 241-image right panel, not an extra handoff image:
  // it is reparented inside the stage just as the earlier Vol.00 original
  // moved. When scrolling backward it resumes its exact Emmaus position.
  // At the end the original protected speaker poster appears IN PLACE,
  // with no translated/scaled second portrait crossing the screen.
  const panelTravelling=oliveIn>.001&&oliveIn<.999;
  if(panelTravelling&&!galleryBorrowed){
   $('#proof-stage').appendChild(emRight);galleryBorrowed=true;
   emRight.dataset.p2GalleryTransferred='true';
  }else if(!panelTravelling&&galleryBorrowed){
   emmaus.appendChild(emRight);galleryBorrowed=false;
   emRight.removeAttribute('data-p2-gallery-transferred');
  }
  const heroRect=oliveHero.getBoundingClientRect();
  const destination={x:heroRect.left-stageRect.left,y:heroRect.top-stageRect.top,
                     w:heroRect.width,h:heroRect.height};
  if(galleryBorrowed){
   poseRect(emRight,fullRight,destination,oliveIn);
  }else{
   poseRect(emRight,coverBounds||fullRight,fullRight,expand);
  }
  // The old ONE field recedes through an inward horizontal crop as the
  // speaker identity unfolds; its content is never moved off the viewport.
  if(oliveIn>.001)emLeft.style.clipPath='inset(0 0 0 '+(100*smooth(oliveIn/.78)).toFixed(3)+'%)';
  oliveHero.style.transform='none';
  oliveHero.style.opacity=String(smooth((oliveIn-.66)/.33));
  emRight.style.opacity=String((useArchive?archive:0)*fieldExit);
  // If the 241-plate host is unavailable, transfer the exact original
  // magazine plate itself into the Olive portrait slot. No blank panel,
  // placeholder, fabricated engraving, or duplicate image may appear.
  if(transferFigure&&!useArchive&&oliveIn>.001){
   poseRect(transferFigure,fullRight,destination,oliveIn);
  }
  heroFolio.style.opacity=String(smooth((oliveIn-.76)/.23));

  const editorial=smooth(oliveIn/.90),register=smooth((oliveIn-.12)/.76),windowReveal=smooth((oliveIn-.34)/.66);
  oliveEditorial.style.clipPath='inset(0 '+((1-editorial)*100).toFixed(3)+'% 0 0)';
  oliveRegister.style.clipPath='inset('+((1-register)*100).toFixed(3)+'% 0 0 0)';
  oliveWindow.style.clipPath='inset(0 0 '+((1-windowReveal)*100).toFixed(3)+'% 0)';
  $('.olive-proof__folio').style.opacity=String(smooth((oliveIn-.8)/.2));
  const section=distance<3.0775?'01 / 07 — CHURCH':distance<6.5?'02 / 07 — MAGAZINE':distance<9.44?'03 / 07 — EMMAUS':'04 / 07 — OLIVE MOUNTAIN';
  phase.textContent=section;document.body.dataset.proofScene=section.split(' / ')[0];
  seek.value=String(distance/12*100);percent.textContent=(distance/12*100).toFixed(0)+'%';lastPaint=distance;
 }
 function requestPaint(){if(!queued){queued=true;requestAnimationFrame(paint)}}
 function seekTo(distance,updateUrl=false){
  const target=track.getBoundingClientRect().top+scrollY+distance*innerHeight;
  scrollTo({top:target,behavior:'instant'});requestPaint();
  if(updateUrl){const url=new URL(location.href);url.searchParams.set('d',distance.toFixed(2));history.replaceState(null,'',url);}
 }
 document.querySelectorAll('[data-jump]').forEach(b=>b.addEventListener('click',()=>seekTo(Number(b.dataset.jump),true)));
 seek.addEventListener('input',()=>seekTo(Number(seek.value)/100*12,true));
 addEventListener('scroll',requestPaint,{passive:true});addEventListener('resize',requestPaint,{passive:true});
 document.addEventListener('visibilitychange',requestPaint);
 base.addEventListener('load',()=>{
  frameLoaded=true;requestPaint();
  const nested=base.contentDocument?.querySelector('.p2-magazine iframe:not(.p2-magazine__home-film)');
  nested?.addEventListener('load',requestPaint,{once:true});
 });
 const initial=new URLSearchParams(location.search).get('d');
 requestAnimationFrame(()=>seekTo(initial===null?7.85:clamp(Number(initial)||0,0,12)));
 requestPaint();
})();
