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
 // A/B art-direction experiment. One original homepage film, still owned by
 // the Magazine iframe; never reparent or clone its media playback node.
 let filmContinuity=new URLSearchParams(location.search).get('film')==='1';
 const filmToggle=$('#proof-film-toggle');
 function syncFilmMode(){
  document.body.dataset.filmContinuity=filmContinuity?'on':'off';
  emmaus.dataset.filmContinuity=filmContinuity?'on':'off';
  olive.dataset.filmContinuity=filmContinuity?'on':'off';
  if(filmToggle){
   filmToggle.setAttribute('aria-pressed',filmContinuity?'true':'false');
   filmToggle.textContent=filmContinuity?'共用影片 · ON':'共用影片 · OFF';
  }
 }
 syncFilmMode();
 filmToggle?.addEventListener('click',()=>{
  filmContinuity=!filmContinuity;
  const url=new URL(location.href);
  if(filmContinuity)url.searchParams.set('film','1');
  else url.searchParams.delete('film');
  history.replaceState(null,'',url);
  syncFilmMode();requestPaint();
 });
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
  renderBookStudy(number);
  selectGalleryForBook(number);
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

 // Doré's original 241 numbered engravings are the only image sources.
 // Book assignments below are conservative, based on the actual titles in
 // ONE's canonical file registry. Works with uncertain attribution are not
 // forced onto a book. A no-match volume gets a random catalogue start.
 const seq=(a,b)=>Array.from({length:b-a+1},(_,i)=>a+i);
 const bookPlates={
  1:seq(1,29),2:seq(30,41),4:seq(42,45),6:seq(46,53),7:seq(54,69),8:[70,71],
  9:seq(72,81),10:seq(82,87),11:[...seq(88,95),107],12:seq(96,104),
  13:[105,106],14:[108,109,110],15:[111,112,113,114],16:[115,116],
  17:[117,118,119,144],18:[120,121,124],23:[122,123],
  24:[125,126],25:[127],26:[128,129],27:[130,131,132,133,134],
  30:[135],32:[136,137],33:[138],38:[139],
  40:seq(161,182),41:seq(183,192),42:seq(193,212),43:seq(213,223),
  44:seq(224,234),52:[235],66:[236,237,238,239,240,241]
 };
 const registry=window.ONE_DORE_COVER_REGISTRY;
 const ids=Array.from({length:241},(_,i)=>i+1);
 const plates=ids.map(id=>({id,file:registry?.files?.[id],title:registry?.titles?.[id]||String(registry?.files?.[id]||'').replace(/^\d+[A-Z]?\./,'').replace(/\.[^.]+$/,'')}));
 if(plates.length!==241||plates.some(p=>!p.file))throw Error('Shared Doré 241-plate inventory is incomplete');
 const plateEls=[$('#em-plate-a'),$('#em-plate-b')];
 let galleryIndex=211,activeSlot=0,galleryTimer=0,galleryLive=false,plateVersion=0,galleryPrefetch=false;
 let galleryOrder=ids.slice(),galleryPosition=211,gallerySelectionBook=42;
 const imgUrl=plate=>'https://commons.wikimedia.org/wiki/Special:Redirect/file/'+encodeURIComponent(plate.file)+'?width=1200';
 async function showPlate(index){
  // A failed Commons image must not leave a prior book's plate visible.
  const ticket=++plateVersion;
  let position=galleryOrder.indexOf((index%plates.length)+1);
  if(position<0)position=0;
  for(let attempt=0;attempt<Math.min(galleryOrder.length,8);attempt++){
   const at=(position+attempt)%galleryOrder.length;
   const plate=plates[galleryOrder[at]-1],url=imgUrl(plate);
   const loaded=await new Promise(resolve=>{
    const probe=new Image();
    probe.onload=()=>resolve(true);probe.onerror=()=>resolve(false);
    probe.src=url;
    if(probe.complete)resolve(probe.naturalWidth>0);
   });
   if(ticket!==plateVersion)return;
   if(!loaded)continue;
   const slot=1-activeSlot,img=plateEls[slot];
   img.src=url;
   plateEls[activeSlot].classList.remove('is-active');
   img.classList.remove('is-active');
   void img.offsetHeight;img.classList.add('is-active');
   activeSlot=slot;galleryIndex=plate.id-1;galleryPosition=at;
   $('#em-plate-title').textContent='DORÉ / '+plate.title.toUpperCase();
   $('#em-plate-index').textContent=String(plate.id).padStart(3,'0')+' / '+String(plates.length);
   emmaus.dataset.dorePlate=String(plate.id);
   emmaus.dataset.galleryLoad='ready';
   return;
  }
  if(ticket===plateVersion){
   emmaus.dataset.galleryLoad='unavailable';
   $('#em-plate-title').textContent='DORÉ / ORIGINAL ARCHIVE UNAVAILABLE';
   $('#em-plate-index').textContent='— / '+plates.length;
  }
 }
 function selectGalleryForBook(number){
  const associated=bookPlates[number]||[];
  const start=associated.length?associated[0]:1+Math.floor(Math.random()*plates.length);
  galleryOrder=[...associated,...ids.filter(id=>!associated.includes(id))];
  if(!associated.length)galleryOrder=[...ids.slice(start-1),...ids.slice(0,start-1)];
  galleryPosition=0;galleryIndex=start-1;gallerySelectionBook=number;
  emmaus.dataset.galleryStart=String(start);
  // Cancel stale asynchronous responses from a preceding book selection.
  plateEls.forEach(img=>img.classList.remove('is-active'));
  emmaus.dataset.galleryLoad='loading';
  $('#em-plate-title').textContent='DORÉ / LOADING BOOK PLATES';
  $('#em-plate-index').textContent=String(start).padStart(3,'0')+' / '+plates.length;
  plateVersion++;galleryPrefetch=true;void showPlate(galleryIndex);
  emmaus.dataset.illustrationMode=associated.length?'book-first':'random-fallback';
  $('#em-plate-selection').textContent=(associated.length?'BOOK PLATES':'ARCHIVE / RANDOM START')+
   ' · '+String(number).padStart(2,'0')+' / '+books[number-1][2].toUpperCase();
 }
 function syncGallery(live){
  if(live===galleryLive)return;galleryLive=live;clearInterval(galleryTimer);galleryTimer=0;
  if(live){
   if(!plateEls.some(img=>img.classList.contains('is-active')))void showPlate(galleryIndex);
   if(!reduced)galleryTimer=setInterval(()=>showPlate(galleryOrder[(galleryPosition+1)%galleryOrder.length]-1),15000);
  }
 }
 const featured=window.ONE_DATA?.luke?.chapterStudies?.['24'];
 if(!featured?.route?.length||!featured?.background?.length||!featured?.connections?.length)
  throw Error('ONE Luke 24 study content missing: feature must use canonical ONE data');
 const studyRoutes=$('#em-study-route'),studyDetail=$('#em-study-detail');
 const studyTabs=[...document.querySelectorAll('[data-study-view]')];
 let currentBookStudy=null,currentStudyView='background';
 let selectedChapter=24;
 function renderBookStudy(number,chapter){
  const item=books[number-1],D=window.ONE_DATA;
  // Only show original ONE studies available in the loaded canonical record.
  const source=number===42?D.luke:number===40?D.matthew:null;
  selectedChapter=Math.min(item[3],Math.max(1,Number(chapter)||(number===42?24:1)));
  const detailed=source?.chapterStudies?.[String(selectedChapter)]||null;
  currentBookStudy=detailed;
  $('#em-study-feature').textContent=(detailed?'ONE / FEATURED CHAPTER':'ONE / BOOK INDEX')+
   ' · '+item[2].toUpperCase();
  $('#em-study-ref').textContent=detailed?.passage||item[1]+' · 第 '+selectedChapter+' / '+item[3]+' 章';
  $('#emmaus-study-heading').textContent=detailed?.title||item[1];
  $('#em-study-movement').textContent=detailed?.movement||
   source?.summary||'選擇章節進入 ONE，從這一卷展開經文閱讀與查經。';
  $('#em-study-source').textContent=item[1]+
   (detailed?' · ONE 原始研讀資料':' · ONE 正式書卷與章節索引');
  const href='/one/?book='+number+'&chapter='+selectedChapter;
  $('#em-study-enter').href=href;$('#emmaus-enter').href=href;
  studyRoutes.replaceChildren();
  if(detailed?.route?.length){
   for(const [ref,desc] of detailed.route.slice(0,2)){
    const li=document.createElement('li'),reference=document.createElement('span'),copy=document.createElement('p');
    reference.textContent=ref;copy.textContent=desc;li.append(reference,copy);studyRoutes.append(li);
   }
  }else{
   const choices=[...new Set([1,Math.ceil(item[3]/2),item[3],selectedChapter])].sort((x,y)=>x-y);
   for(const chapterNo of choices){
    const li=document.createElement('li'),button=document.createElement('button');
    button.type='button';button.className='emmaus__chapter-choice';
    button.dataset.chapter=String(chapterNo);
    button.setAttribute('aria-pressed',String(chapterNo===selectedChapter));
    button.textContent='第 '+chapterNo+' 章 / '+item[2]+' '+chapterNo;
    button.addEventListener('click',()=>renderBookStudy(number,chapterNo));
    li.append(button);studyRoutes.append(li);
   }
  }
  showStudy(currentStudyView);
 }
 function showStudy(view){
  currentStudyView=view;
  const f=currentBookStudy;
  let label='',body='';
  if(view==='connections'&&f?.connections?.length){
   label=f.connections[0][0]+' / '+f.connections[0][1];body=f.connections[0][2];
  }else if(view==='questions'&&f?.questions?.length){
   label='思考與討論 / QUESTIONS';body=f.questions[1]||f.questions[0];
  }else if(view==='background'&&f?.background?.length){
   label=f.background[1]?.[0]||f.background[0][0];body=f.background[1]?.[1]||f.background[0][1];
  }else{
   label=view==='connections'?'相關經文 / CROSS REFERENCES':view==='questions'?'研讀問題 / QUESTIONS':'卷書總覽 / BOOK INDEX';
   body='ONE 已提供本卷 '+books[selectedBook-1][3]+' 章導覽；請開啟正式 ONE 選擇章節，查看實際可用的研讀資料。';
  }
  studyDetail.replaceChildren();
  const strong=document.createElement('strong'),paragraph=document.createElement('p');
  strong.textContent=label;paragraph.textContent=body;studyDetail.append(strong,paragraph);
  for(const tab of studyTabs){
   const active=tab.dataset.studyView===view;tab.setAttribute('aria-selected',String(active));
   tab.tabIndex=active?0:-1;
   if(active)studyDetail.setAttribute('aria-labelledby',tab.id);
  }
  emmaus.dataset.studyView=view;
 }
 for(const tab of studyTabs){
  tab.addEventListener('click',()=>showStudy(tab.dataset.studyView));
  tab.addEventListener('keydown',event=>{
   if(event.key!=='ArrowLeft'&&event.key!=='ArrowRight')return;
   event.preventDefault();
   const offset=event.key==='ArrowRight'?1:-1;
   const next=studyTabs[(studyTabs.indexOf(tab)+offset+studyTabs.length)%studyTabs.length];
   showStudy(next.dataset.studyView);next.focus({preventScroll:true});
  });
 }
 selectBook(42,false);
 requestAnimationFrame(()=>centerRailBook(rail.querySelector('[data-book="42"]'),'instant'));
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
 const oliveHero=$('#olive-morph-hero'),oliveEditorial=$('.olive-proof__editorial'),oliveRegister=$('.olive-proof__register'),oliveWindow=$('.olive-proof__window'),oliveBottom=$('.olive-proof__bottom');
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
 let sourceOriginalTileOpacity=null,sourceOriginalCoverOpacity=null,sourceOriginalEditorialOpacity=null;
 let frameLoaded=false,lastPaint=NaN,queued=false;
 function paint(){
  queued=false;const vh=Math.max(1,innerHeight),top=track.getBoundingClientRect().top;
  const distance=clamp(-top/vh,0,12),legacyDistance=Math.min(distance,6.5),churchEnd=3.0775,magazineEnd=6.5;
  let legacy;
  if(top>0)legacy=clamp((vh-top)/vh,0,1)*.1/2.9;
  else if(legacyDistance<=churchEnd){const scene=legacyDistance<=1.8?.1+legacyDistance*(.4/1.8):.5+(legacyDistance-1.8);legacy=scene/2.9;}
  else{const scene=2.37+(legacyDistance-churchEnd)/(magazineEnd-churchEnd)*(4-2.37);legacy=scene<=2.9?.75*scene/2.9:.75+.25*(scene-2.9)/1.1;}
  // Continue the SAME Magazine/home player through P2 03/04 only in film mode.
  // The default experiment and published Church->Magazine behavior are untouched.
  if(frameLoaded)base.contentWindow?.postMessage({
   type:'westside-p2-scroll',progress:clamp(legacy),
   active:filmContinuity?distance<12:distance<6.6
  },location.origin);
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
  // Never dissolve the approved Magazine just to expose the homepage film.
  // Contents and the cover remain the connected backdrop while the REAL
  // engraving crosses from the left to the right. Only the incoming ONE
  // panel takes over once the right-hand plate reaches its destination.
  if(sourceDoc&&sourceStyleDoc!==sourceDoc){
   sourceStyleDoc=sourceDoc;
   sourceOriginalTileOpacity=sourceTile?.style.opacity??'';
   sourceOriginalCoverOpacity=sourceCover?.style.opacity??'';
   sourceOriginalEditorialOpacity=sourceFrame?.style.opacity??'';
  }
  if(sourceTile)sourceTile.style.opacity=sourceOriginalTileOpacity??'';
  if(sourceCover)sourceCover.style.opacity=sourceOriginalCoverOpacity??'';
  // Only after the actual Magazine plate is borrowed, the approved Contents
  // iframe quietly recedes on the EXISTING ONE paper-reveal timeline, exposing
  // its still-playing film sibling. Reverse scroll restores it completely.
  if(sourceFrame)sourceFrame.style.opacity=filmContinuity
   ?String(1-oneDrop):(sourceOriginalEditorialOpacity??'');
  // Actual video is shown in the open space AROUND the physical spread.
  // The manuscript and its study typography remain opaque, never overlaid
  // by moving images. Both image panels share one measurable inset stage.
  emmaus.style.backgroundColor=filmContinuity?'transparent'
   :(oneDrop>=.999?'var(--em-paper)':'transparent');
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
  // MERSI cadence: move an EXISTING field first; expose the NEW identity in the vacancy second.
  const morphMove=smooth((oliveIn-.32)/.58);
  const fieldExit=1-smooth((oliveIn-.79)/.2);
  // Film-continuity experiment: replace the nearly invisible masked slit
  // with a real panoramic film surround. Contents+engraving retain their
  // original physical handoff; only the FINISHED 03 spread becomes inset.
  // The same insets apply to Olive via scoped CSS, so the gallery can travel
  // to its protected portrait without a second wipe or extra video node.
  const mobileFilm=filmContinuity&&innerWidth<=820;
  const surroundX=filmContinuity&&!mobileFilm?stageRect.width*.085:0;
  const surroundTop=filmContinuity?stageRect.height*(mobileFilm?.115:.09):0;
  const surroundBottom=filmContinuity?stageRect.height*(mobileFilm?.01:.09):0;
  const spreadWidth=stageRect.width-2*surroundX;
  const spreadHeight=stageRect.height-surroundTop-surroundBottom;
  const fullLeft={x:surroundX,y:surroundTop,w:spreadWidth*2/3,h:spreadHeight};
  const fullRight={x:surroundX+spreadWidth*2/3,y:surroundTop,
                   w:spreadWidth/3,h:spreadHeight};
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
  olive.style.backgroundColor=filmContinuity?'transparent'
   :(oliveIn>=.999?'#f0eee7':'transparent');
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
   poseRect(emRight,fullRight,destination,morphMove);
  }else{
   poseRect(emRight,coverBounds||fullRight,fullRight,expand);
  }
  // MERSI shared-boundary reflow: the real ONE panel ends exactly where
  // the existing engraving panel now begins. Its width responds to the
  // moving plate and its text REFLOWS instead of being arbitrarily clipped.
  // Only after the speaker identity has taken over does ONE withdraw.
  const galleryEdge=emRight.getBoundingClientRect().left-stageRect.left;
  if(oliveIn>.001){
   const nextWidth=Math.min(fullLeft.w,Math.max(0,galleryEdge-fullLeft.x));
   emLeft.style.width=nextWidth.toFixed(2)+'px';
   emLeft.style.clipPath=oliveIn>.74
    ?'inset(0 '+(100*smooth((oliveIn-.74)/.25)).toFixed(3)+'% 0 0)'
    :'none';
  }else{
   emLeft.style.width=fullLeft.w.toFixed(2)+'px';
  }
  oliveHero.style.transform='none';
  oliveHero.style.opacity=String(1-fieldExit);
  emRight.style.opacity=String((useArchive?archive:0)*fieldExit);
  // If the 241-plate host is unavailable, transfer the exact original
  // magazine plate itself into the Olive portrait slot. No blank panel,
  // placeholder, fabricated engraving, or duplicate image may appear.
  if(transferFigure&&!useArchive&&oliveIn>.001){
   poseRect(transferFigure,fullRight,destination,morphMove);
  }
  heroFolio.style.opacity=String(smooth((oliveIn-.76)/.23));

  const editorial=smooth((oliveIn-.55)/.36),register=smooth((oliveIn-.70)/.29),windowReveal=smooth((oliveIn-.74)/.25);
  const kicker=$('.olive-proof__kicker');
  kicker.style.opacity=String(smooth((oliveIn-.38)/.3));
  oliveBottom.style.opacity=String(smooth((oliveIn-.69)/.30));
  // Olive editorial is revealed in the exact area vacated by the moving
  // engraved panel, from RIGHT to LEFT, not as a new page wipe.
  // The left edge of this crop tracks the same MERSI morph progress.
  // Withhold the WHOLE Olive editorial surface, not only its letters.
  // Otherwise an empty white rectangle replaces ONE during the early morph.
  oliveEditorial.style.opacity=String(editorial);
  oliveEditorial.style.clipPath='none';
  $('.olive-proof__editorial > div').style.opacity=String(editorial);
  $('.olive-proof__editorial > a').style.opacity=String(smooth((oliveIn-.70)/.25));
  oliveRegister.style.clipPath='inset('+((1-register)*100).toFixed(3)+'% 0 0 0)';
  oliveWindow.style.clipPath='inset(0 0 '+((1-windowReveal)*100).toFixed(3)+'% 0)';
  $('.olive-proof__folio').style.opacity=String(smooth((oliveIn-.83)/.16));
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
