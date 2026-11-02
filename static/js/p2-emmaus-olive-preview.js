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
 // A/B editorial experiment: Church alone has the Red Sea split.
 // Magazine remains the fixed geometric master for all following chapters.
 // Only the NON-CONTENT field changes by realm (film, manuscript, terraces).
 let fixedGround=new URLSearchParams(location.search).get('ground')==='1';
 // The 03–07 draft must show the five native engraving backgrounds by default.
 // ?ground=0 (or ?five=0 without an explicit ground setting) keeps the original A/B proof.
 const params=new URLSearchParams(location.search);
 if(!params.has('ground')&&params.get('five')!=='0')fixedGround=true;
 const timelineMax=params.get('five')==='0'?12:16.74;
 const groundToggle=$('#proof-ground-toggle'),realmGround=$('#p2-realm-background'),oliveGround=$('#p2-olive-ground-crossfade');
 function syncGroundMode(){
  document.body.dataset.fixedGround=fixedGround?'on':'off';
  emmaus.dataset.fixedGround=fixedGround?'on':'off';
  olive.dataset.fixedGround=fixedGround?'on':'off';
  if(groundToggle){
   groundToggle.setAttribute('aria-pressed',fixedGround?'true':'false');
   groundToggle.textContent=fixedGround?'底紋 · ON':'底紋 · OFF';
  }
 }
 syncGroundMode();
 groundToggle?.addEventListener('click',()=>{
  fixedGround=!fixedGround;
  const url=new URL(location.href);
  if(fixedGround)url.searchParams.set('ground','1');
  else url.searchParams.set('ground','0');
  url.searchParams.delete('film');
  history.replaceState(null,'',url);
  syncGroundMode();requestPaint();
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
  const b=document.createElement('button');
  b.type='button';b.className='emmaus__number';b.dataset.book=String(item[0]);
  const zh=document.createElement('span');
  zh.className='emmaus__number-zh';zh.lang='zh-Hant';zh.textContent=item[1];
  const en=document.createElement('span');
  en.className='emmaus__number-en';en.lang='en';en.textContent=item[2];
  const numeral=document.createElement('strong');
  numeral.className='emmaus__number-index';numeral.textContent=String(item[0]).padStart(2,'0');
  b.append(zh,en,numeral);
  b.setAttribute('aria-label','第 '+item[0]+' 卷：'+item[1]+' / '+item[2]);
  b.title=item[1]+' · '+item[2]+' · 第 '+item[0]+' 卷';
  b.addEventListener('click',()=>selectBook(item[0]));rail.append(b);
 }
 rail.addEventListener('keydown',e=>{
  if(e.key==='ArrowRight'||e.key==='ArrowLeft'){
   e.preventDefault();selectBook(clamp(selectedBook+(e.key==='ArrowRight'?1:-1),1,66));
   rail.querySelector(`[data-book="${selectedBook}"]`)?.focus({preventScroll:true});
  }
 });
 // A user scrolling over the ONE book strip intends to browse books,
 // NOT leave Emmaus for the following P2 realm. Treat mouse-wheel vertical
 // deltas as horizontal movement on this one-row canonical book rail.
 rail.addEventListener('wheel',event=>{
  if(event.ctrlKey)return;
  const unit=event.deltaMode===1?16:event.deltaMode===2?rail.clientWidth:1;
  if(Math.abs(event.deltaY)>Math.abs(event.deltaX)&&rail.scrollWidth>rail.clientWidth){
   event.preventDefault();
   rail.scrollLeft+=event.deltaY*unit;
  }
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
 let gallerySelectionTimer=0;
 let galleryOrder=ids.slice(),galleryPosition=211,gallerySelectionBook=42;
 const imgUrl=plate=>'https://commons.wikimedia.org/wiki/Special:Redirect/file/'+encodeURIComponent(plate.file)+'?width=960';
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
   // The archive may continue past book-specific plates. Never imply that an
   // unrelated engraving illustrates the selected chapter or Bible book.
   const matched=(bookPlates[gallerySelectionBook]||[]).includes(plate.id);
   $('#em-plate-selection').textContent=(matched?'本卷插圖 / BOOK PLATE':'圖庫其他插圖 / ARCHIVE PLATE')+
    ' · '+String(gallerySelectionBook).padStart(2,'0')+' / '+
    books[gallerySelectionBook-1][2].toUpperCase();
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
  // Allow rapid book browsing without starting dozens of large Wikimedia
  // downloads. Only the most recently selected volume fetches new artwork.
  plateVersion++;galleryPrefetch=false;
  clearTimeout(gallerySelectionTimer);
  gallerySelectionTimer=setTimeout(()=>{
   if(gallerySelectionBook!==number)return;
   galleryPrefetch=true;void showPlate(galleryIndex);
  },180);
  emmaus.dataset.illustrationMode=associated.length?'book-first':'random-fallback';
  $('#em-plate-selection').textContent=(associated.length?'本卷插圖 / BOOK PLATES':'圖庫隨機插圖 / ARCHIVE RANDOM')+
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
 // Actual canonical location is a second, large editorial masthead.
 // It must follow every book and chapter selection, never stay in the footer.
 function chapterZh(n){
  const digit=['','一','二','三','四','五','六','七','八','九'];
  if(n<10)return digit[n];
  if(n<20)return '十'+(n===10?'':digit[n%10]);
  if(n<100)return digit[Math.floor(n/10)]+'十'+(n%10?digit[n%10]:'');
  const h=Math.floor(n/100),tail=n%100;
  return digit[h]+'百'+(tail?(tail<10?'零'+chapterZh(tail):tail<20?'一'+chapterZh(tail):chapterZh(tail)):'');
 }
 function renderBookStudy(number,chapter){
  const item=books[number-1],D=window.ONE_DATA;
  // Only show original ONE studies available in the loaded canonical record.
  const source=number===42?D.luke:number===40?D.matthew:D.studyBooks?.[number]||null;
  selectedChapter=Math.min(item[3],Math.max(1,Number(chapter)||(number===42?24:1)));
  const currentChapter=$('#em-current-chapter-number'),currentChapterZh=$('#em-current-chapter-zh');
  if(currentChapter)currentChapter.textContent=String(selectedChapter).padStart(2,'0');
  if(currentChapterZh)currentChapterZh.textContent='第'+chapterZh(selectedChapter)+'章';
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
   for(const [ref,desc] of detailed.route.slice(0,5)){
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
  emmaus.dataset.selectedChapter=String(selectedChapter);
  showStudy(currentStudyView);
  emmaus.dispatchEvent(new CustomEvent('p2:one-selection',{detail:{book:number,chapter:selectedChapter}}));
 }
 function showStudy(view){
  currentStudyView=view;
  const f=currentBookStudy,item=books[selectedBook-1],D=window.ONE_DATA;
  const source=selectedBook===42?D.luke:selectedBook===40?D.matthew:D.studyBooks?.[selectedBook];
  studyDetail.replaceChildren();
  const article=(heading,copy)=>{
   const el=document.createElement('article'),h=document.createElement('strong');
   h.textContent=heading;el.append(h);
   for(const line of copy.filter(Boolean)){
    const p=document.createElement('p');p.textContent=String(line);el.append(p);
   }
   studyDetail.append(el);
  };
  const ordered=(heading,items)=>{
   const el=document.createElement('article'),h=document.createElement('strong'),ol=document.createElement('ol');
   h.textContent=heading;el.append(h);
   for(const line of items){const li=document.createElement('li');li.textContent=String(line);ol.append(li);}
   el.append(ol);studyDetail.append(el);
  };
  if(view==='story'&&f){
   article('本章故事 / STORY',[f.story,f.position]);
   (f.route||[]).forEach(item=>article(item[0],[item[1]]));
  }else if(view==='background'&&f?.background?.length){
   f.background.forEach(item=>article(item[0],[item[1],item[2]]));
  }else if(view==='connections'&&f?.connections?.length){
   f.connections.forEach(item=>article(item[0]+' / '+(item[1]||''),[item[2]]));
  }else if(view==='questions'&&f?.questions?.length){
   ordered('觀察與討論 / QUESTIONS',f.questions);
  }else if(view==='prepare'&&f?.prepare?.length){
   ordered('預備研讀 / PREPARE',f.prepare);
  }else if(view==='map'&&f?.map){
   article(f.map.title||'本章地理',[f.map.guide,...(f.map.places||[])]);
   if(f.map.source){
    const a=document.createElement('a');a.href=f.map.source;a.target='_blank';a.rel='noopener';
    a.textContent='查閱 ONE 地理原始資料 ↗';studyDetail.append(a);
   }
  }else{
   article(view==='connections'?'串珠 / CROSS REFERENCES':view==='questions'?'問題 / QUESTIONS':
    view==='map'?'地圖 / GEOGRAPHY':view==='prepare'?'預備 / PREPARE':
    view==='story'?'本章 / CHAPTER':'書卷 / BOOK',[
    source?.chapters?.[selectedChapter-1]||source?.summary||item[1]+' · 第 '+selectedChapter+' 章',
    '按「在這頁使用完整 ONE 工作台」，即可直接在此頁使用原版 ONE 的逐章研讀、地圖、串珠、問題與查經日曆。']);
  }
  studyDetail.scrollTop=0;
  for(const tab of studyTabs){
   const active=tab.dataset.studyView===view;tab.setAttribute('aria-selected',String(active));tab.tabIndex=active?0:-1;
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
 window.P2EmmausSelect=(number,chapter)=>{
  const n=Number(number),ch=Number(chapter);if(!Number.isInteger(n)||n<1||n>66)return;
  if(selectedBook!==n)selectBook(n);
  renderBookStudy(n,ch);
 };
 for(const link of [$('#em-study-enter'),$('#emmaus-enter')]){
  link.addEventListener('click',event=>{
   if(!window.P2EmmausONE)return;
   event.preventDefault();window.P2EmmausONE.open();
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
 // The source magazine node stays in its original iframe throughout the handoff.
 let transferFigure=null,transferHome=null,transferOriginalVisibility=null;
 let sourceOriginalTileOpacity=null,sourceOriginalCoverOpacity=null,sourceOriginalEditorialOpacity=null;
 let frameLoaded=false,lastPaint=NaN,queued=false,lastMeasuredSpread=null;
 // Cache the settled Magazine geometry across Emmaus scroll frames.
 let settledGeometry=null,settledGeometryDoc=null,settledGeometryW=0,settledGeometryH=0;
 function paint(){
  queued=false;const vh=Math.max(1,innerHeight),top=track.getBoundingClientRect().top;
  const fullDistance=clamp(-top/vh,0,timelineMax),distance=clamp(fullDistance,0,12),legacyDistance=Math.min(distance,6.5),churchEnd=3.0775,magazineEnd=6.5;
  let legacy;
  if(top>0)legacy=clamp((vh-top)/vh,0,1)*.1/2.9;
  else if(legacyDistance<=churchEnd){const scene=legacyDistance<=1.8?.1+legacyDistance*(.4/1.8):.5+(legacyDistance-1.8);legacy=scene/2.9;}
  else{const scene=2.37+(legacyDistance-churchEnd)/(magazineEnd-churchEnd)*(4-2.37);legacy=scene<=2.9?.75*scene/2.9:.75+.25*(scene-2.9)/1.1;}
  // Magazine keeps its own original film; later chapters use engraving.
  // Never restart or clone the film, and do not alter the Church's unique split.
  if(frameLoaded)base.contentWindow?.postMessage({
   type:'westside-p2-scroll',progress:clamp(legacy),active:distance<6.6
  },location.origin);
  // The 05–07 adapter owns later chapter backgrounds and SVGs. Do not repaint
  // Emmaus/Olive, force the background back to 'sermon', or remeasure the
  // heavyweight nested Magazine DOM on every later scroll frame.
  if(fullDistance>=12){
   if(oliveGround)oliveGround.style.opacity='0';
   if(transferFigure){
    transferFigure.remove();
    if(transferHome)transferHome.style.visibility=transferOriginalVisibility??'';
    transferFigure=null;transferHome=null;transferOriginalVisibility=null;
   }
   emmaus.style.visibility='hidden';emmaus.style.pointerEvents='none';
   emmaus.inert=true;emmaus.setAttribute('aria-hidden','true');
   olive.style.visibility='hidden';olive.style.pointerEvents='none';
   olive.inert=true;olive.setAttribute('aria-hidden','true');
   const section=fullDistance>=15.14?'07 / 07 — DAYLIGHT CAFÉ':fullDistance>=13.57?'06 / 07 — PARADISE CINEMA':'05 / 07 — DAWN BOOKSHOP';
   phase.textContent=section;document.body.dataset.proofScene=section.split(' / ')[0];
   seek.value=String(fullDistance/timelineMax*100);
   percent.textContent=(fullDistance/timelineMax*100).toFixed(0)+'%';
   lastPaint=distance;
   return;
  }
  // Same MERSI image object: Magazine LEFT engraving actually travels to
  // the existing RIGHT cover rectangle. No replica image is created.
  // Only once it arrives does the full Doré archive take over silently;
  // ONE reveals top-to-bottom inside the fixed Magazine perimeter; never zoom back to full-screen.
  const move=smooth((distance-6.50)/.90);
  const archive=smooth((distance-7.40)/.28);
  const oneDrop=smooth((distance-7.66)/.78);
  const oliveIn=smooth((distance-9.44)/1.38);
  // The chapter handoff is a single in-place folio reveal, not three reflowing panels.
  // The incoming ONE paper + original Doré gallery must cover BOTH former
  // Magazine folios from the first pixel of the travelling artwork.
  const emShowing=move>.001&&oliveIn<.999,oliveShowing=oliveIn>.001;
  emmaus.style.visibility=emShowing?'visible':'hidden';emmaus.style.opacity='1';emmaus.style.transform='none';
  // Do not leave a visibly displayed Emmaus page inert merely because the
  // scroll frame sits a few pixels before/after the exact 03 dwell point.
  const emInteractive=oneDrop>.82&&oliveIn<.55;
  emmaus.style.pointerEvents=emInteractive?'auto':'none';emmaus.inert=!emInteractive;
  emmaus.setAttribute('aria-hidden',emInteractive?'false':'true');

  const sourceFrame=base.contentDocument?.querySelector('.p2-magazine iframe:not(.p2-magazine__home-film)');
  const sourceDoc=sourceFrame?.contentDocument;
  const sourceTile=sourceDoc?.getElementById('dual-contents');
  const sourceCover=sourceDoc?.getElementById('dual-cover');
  const sourceSpine=sourceDoc?.getElementById('dual-continuum');
  const sourceFigure=sourceDoc?.getElementById('dual-dore-plate');
  const stageRect=$('#proof-stage').getBoundingClientRect();
  const canReuse=distance>=7.0&&settledGeometryDoc===sourceDoc&&
    settledGeometryW===stageRect.width&&settledGeometryH===stageRect.height&&!!settledGeometry;
  let original,coverBounds,spineBounds;
  if(canReuse){
   ({original,coverBounds,spineBounds}=settledGeometry);
  }else{
   const frameRect=sourceFrame?.getBoundingClientRect(),baseRect=base.getBoundingClientRect();
   const bounds=node=>{
    if(!node||!frameRect)return null;
    const r=node.getBoundingClientRect();
    return {x:baseRect.left-stageRect.left+frameRect.left+r.left,
            y:baseRect.top-stageRect.top+frameRect.top+r.top,w:r.width,h:r.height};
   };
   original=bounds(sourceTile);coverBounds=bounds(sourceCover);spineBounds=bounds(sourceSpine);
   if(distance>=7.0&&original&&coverBounds){
    settledGeometry={original,coverBounds,spineBounds};
    settledGeometryDoc=sourceDoc;
    settledGeometryW=stageRect.width;settledGeometryH=stageRect.height;
   }
  }
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
  // The accepted Magazine iframe, including its book spine and original
  // video proportions, remains unchanged and restores during reverse scroll.
  if(sourceFrame)sourceFrame.style.opacity=sourceOriginalEditorialOpacity??'';
  // A realm-specific engraved backdrop replaces the film ONLY in the
  // background field, on the existing 02→03 timeline (no new reveal effect).
  if(realmGround)realmGround.dataset.realm='bible';
  emmaus.style.backgroundColor=fixedGround?'transparent'
   :(oneDrop>=.999?'var(--em-paper)':'transparent');
  const lerp=(a,b,p)=>a+(b-a)*p;
  const setRect=(el,r)=>{
   if(!r)return;
   // A projected iframe node can inherit inset/right/bottom from its source.
   el.style.inset='auto';el.style.right='auto';el.style.bottom='auto';
   el.style.left=r.x.toFixed(2)+'px';
   el.style.top=r.y.toFixed(2)+'px';
   el.style.width=r.w.toFixed(2)+'px';
   el.style.height=r.h.toFixed(2)+'px';
  };
  const blendRects=(a,b,p)=>({
   x:lerp(a.x,b.x,p),y:lerp(a.y,b.y,p),
   w:lerp(a.w,b.w,p),h:lerp(a.h,b.h,p)
  });
  const fitInside=(original,destination)=>{
   // Never enlarge, crop or distort the square Contents engraving to fill a 5:8 cover.
   const scale=Math.min(1,destination.w/original.w,destination.h/original.h);
   const w=original.w*scale,h=original.h*scale;
   return {x:destination.x+(destination.w-w)/2,
           y:destination.y+(destination.h-h)/2,w,h};
  };
  const poseRect=(el,a,b,p)=>{if(a&&b)setRect(el,blendRects(a,b,p))};
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
  // Fade the temporary Magazine projection away before the new folio crosses it.
  const fieldExit=1-smooth(oliveIn/.12);
  // The actual MAGAZINE 5:8 cover + square Contents + original spine
  // define the protected outer rectangle. Read live DOM geometry; never
  // invent a new 8.5%/9% frame or expand the chapter back to full screen.
  // Include the REAL seven-color spine in the frozen Magazine perimeter.
  // It sits just outside Contents on desktop; excluding it would allow the
  // new engraving to paint OVER the accepted book spine during handoff.
  // The real magazine is one square Contents page adjacent to a 5:8 cover.
  // A transient iframe measurement MUST NOT erase either following chapter.
  // Reconstruct the EXACT approved folio geometry from the source's own layout
  // formula when DOM coordinates are not ready; never fall back to full screen.
  const expectedFolio=()=>{
   const W=stageRect.width,H=stageRect.height,mobile=W<=820;
   if(mobile){
    const mx=Math.max(7,W*.025),my=6;
    const side=Math.max(1,Math.min((W-2*mx)/1.05,(H-2*my)/2.6));
    const edge=Math.max(13,Math.min(20,side*.05));
    const stackY=(H-2.6*side)/2;
    const coverX=(W-side)/2,contentsX=(W-side-edge)/2+edge;
    const x=Math.min(coverX,contentsX);
    return {x,y:stackY,w:Math.max(coverX+side,contentsX+side)-x,h:2.6*side};
   }
   const mx=Math.max(16,W*.06),my=Math.max(18,H*.053);
   const side=Math.max(1,Math.min((W-2*mx)/(1.625+.035),H-2*my));
   const edge=Math.max(18,Math.min(28,side*.035));
   const width=side*1.625+edge;
   return {x:(W-width)/2,y:(H-side)/2,w:width,h:side};
  };
  const validMagazine=original&&coverBounds&&
   original.w>0&&original.h>0&&coverBounds.w>0&&coverBounds.h>0&&
   Math.abs(original.w/original.h-1)<.09&&
   Math.abs(coverBounds.w/coverBounds.h-.625)<.09&&
   (stageRect.width<=820?
    Math.abs(original.x-coverBounds.x)<original.w*.10:
    Math.abs(original.h-coverBounds.h)<original.h*.04&&
    coverBounds.x>=original.x+original.w-original.w*.04)&&
   original.x>=-2&&original.y>=-2&&
   Math.max(original.x+original.w,coverBounds.x+coverBounds.w)<=stageRect.width+2&&
   Math.max(original.y+original.h,coverBounds.y+coverBounds.h)<=stageRect.height+2;
  // The approved source is always the geometry authority when its page bounds
  // are sane; otherwise compute from the SAME dimensions used by its renderer.
  const magSpread=validMagazine?(()=>{
   const folios=[original,coverBounds];
   const x=Math.min(...folios.map(r=>r.x)),y=Math.min(...folios.map(r=>r.y));
   return {x,y,w:Math.max(...folios.map(r=>r.x+r.w))-x,
               h:Math.max(...folios.map(r=>r.y+r.h))-y};
  })():expectedFolio();
  lastMeasuredSpread=magSpread;
  // Never conceal Emmaus or Olive Mountain because a nested iframe was late.
  // A bad measurement is handled by the proportionally reconstructed folio.
  const master=magSpread;
  // Cut the REAL Magazine folio shape OUT of the background engraving.
  // This paints engraving only in the original VIDEO field, never over the
  // published Contents/cover or an arriving ONE page. Even the transition
  // needs no separate full-screen curtain or reflow.
  if(realmGround){
   if(fixedGround&&magSpread){
    const n=v=>Math.round(v*100)/100;
    const x=n(master.x),y=n(master.y),right=n(master.x+master.w),bottom=n(master.y+master.h);
    const w=n(stageRect.width),h=n(stageRect.height);
    const clip='path("M 0 0 H '+w+' V '+h+
      ' H 0 Z M '+x+' '+y+' V '+bottom+' H '+right+' V '+y+' Z")';
    if(realmGround.style.clipPath!==clip)realmGround.style.clipPath=clip;
    realmGround.style.opacity=String(move);
    if(oliveGround){
     if(oliveGround.style.clipPath!==clip)oliveGround.style.clipPath=clip;
     oliveGround.style.opacity=String(oliveIn*move);
    }
   }else{
    realmGround.style.opacity='0';realmGround.style.clipPath='none';
    if(oliveGround){oliveGround.style.opacity='0';oliveGround.style.clipPath='none';}
   }
  }
  // Keep the Doré gallery EXACTLY the size and position of the approved
  // Magazine 5:8 cover. The incoming ONE folio occupies the remaining Contents
  // space: never squeeze the cover again into an arbitrary 1/3-width panel.
  // Mobile's original stacked Magazine folios keep their compact split.
  const coverFolio=validMagazine?coverBounds:{
   x:master.x+master.w-master.h*.625,y:master.y,w:master.h*.625,h:master.h
  };
  const fullRight=stageRect.width>820?coverFolio:{
   x:master.x+master.w*2/3,y:master.y,w:master.w/3,h:master.h
  };
  const fullLeft={x:master.x,y:master.y,w:fullRight.x-master.x,h:master.h};
  // 03–07 remain within the SAME live Magazine perimeter in every proof mode.
  // The engraving toggle changes the surrounding field, never the folio geometry.
  olive.style.inset='auto';
  olive.style.left=master.x.toFixed(2)+'px';
  olive.style.top=master.y.toFixed(2)+'px';
  olive.style.width=master.w.toFixed(2)+'px';
  olive.style.height=master.h.toFixed(2)+'px';
  if(move>.001&&sourceFigure&&sourceTile&&coverBounds){
   // Keep the magazine artwork in its OWN iframe. Never adopt its DOM into P2.
   // Project the same source image URLs only for the scroll-owned transition.
   if(!transferFigure||transferHome!==sourceFigure){
    if(transferFigure)transferFigure.remove();
    if(transferHome)transferHome.style.visibility=transferOriginalVisibility??'';
    transferHome=sourceFigure;transferOriginalVisibility=sourceFigure.style.visibility;
    transferFigure=sourceFigure.cloneNode(true);
    transferFigure.setAttribute('aria-hidden','true');
    transferFigure.dataset.p2Transferred='projection';
    $('#proof-stage').appendChild(transferFigure);
   }
   const originals=sourceFigure.querySelectorAll('img'),projections=transferFigure.querySelectorAll('img');
   originals.forEach((img,i)=>{
    const projection=projections[i];if(!projection)return;
    const url=img.currentSrc||img.src;
    // Freeze the original image transform while the plate travels; the
    // source gallery has its own 15s scan/zoom, which must not resize
    // the projected image during this horizontal slide.
    if(url&&projection.src!==url){
     projection.src=url;
     projection.style.cssText=img.style.cssText;
    }
    projection.className=img.className;
   });
   const credit=sourceFigure.querySelector('figcaption'),projectedCredit=transferFigure.querySelector('figcaption');
   if(credit&&projectedCredit)projectedCredit.textContent=credit.textContent;
   sourceFigure.style.visibility='hidden';
   // 02→03: translate the SAME SIZE engraving horizontally, never scale it.
   // A square engraving crosses to the narrower 5:8 cover without changing
   // its width or height. The destination folio clips the overflowing edges.
   const sourceArt=validMagazine?original:{x:master.x,y:master.y,w:master.h,h:master.h};
   const targetCover=validMagazine?coverBounds:{
    x:master.x+master.w-master.h*.625,y:master.y,w:master.h*.625,h:master.h};
   const targetX=targetCover.x+(targetCover.w-sourceArt.w)/2;
   const movingArt={x:lerp(sourceArt.x,targetX,move),y:sourceArt.y,
                    w:sourceArt.w,h:sourceArt.h};
   setRect(transferFigure,movingArt);
   // Crop only the PAGE WINDOW as it moves: the art itself stays 1:1 size.
   const windowX=lerp(sourceArt.x,targetCover.x,move);
   const windowY=lerp(sourceArt.y,targetCover.y,move);
   const windowW=lerp(sourceArt.w,targetCover.w,move);
   const windowH=lerp(sourceArt.h,targetCover.h,move);
   const crop=[Math.max(0,windowY-movingArt.y),
               Math.max(0,movingArt.x+movingArt.w-windowX-windowW),
               Math.max(0,movingArt.y+movingArt.h-windowY-windowH),
               Math.max(0,windowX-movingArt.x)];
   transferFigure.style.clipPath='inset('+crop.map(x=>x.toFixed(2)+'px').join(' ')+')';
   transferFigure.style.setProperty('--p2-transfer-visible',
    String(Math.max(0,1-(useArchive?archive:0))*fieldExit));
  }else if(transferFigure){
   transferFigure.remove();
   if(transferHome)transferHome.style.visibility=transferOriginalVisibility??'';
   transferFigure=null;transferHome=null;transferOriginalVisibility=null;
  }
  // The ONE field opens over the vacated Contents footprint, not from outside.
  // Chapter text and artwork keep their positions within the Magazine spread.
  poseRect(emLeft,fullLeft,fullLeft,1);
  // Full-size destination remains opaque: no old Contents behind the transfer.
  emLeft.style.clipPath='none';
  poseRect(emRight,fullRight,fullRight,1);
  emRight.style.clipPath='none';
  syncGallery(move>.98&&oliveIn<.001&&document.visibilityState==='visible');
  // Hold an opaque original-gallery matte over the old magazine cover.
  // The archive image can fade inside that stable panel when loaded.
  emRight.style.opacity='1';
  // Keep the moving plate visible all the way to the destination.
  // Only its editorial annotation recedes; the image itself must NOT vanish
  // at 32% progress and leave a blank travelling rectangle.
  emPlates.style.opacity='1';
  const annotations=1-smooth(oliveIn/.40);
  $('.emmaus__plate-top').style.opacity=String(annotations);
  $('.emmaus__plate-caption').style.opacity=String(annotations);
  $('.emmaus__gold-line').style.opacity=String(annotations);

  // 03→04: both complete folios stay at the EXACT same Magazine rectangle.
  // The incoming REAL Olive page is revealed from right to left INSIDE its
  // own bounds; no color-only wipe, animated width, image transfer, layout
  // reflow or separate half-finished layers. Reverse scroll simply reverses
  // this in-place reveal. All source pages and ONE interaction remain intact.
  if(galleryBorrowed){
   emmaus.appendChild(emRight);
   galleryBorrowed=false;
   emRight.removeAttribute('data-p2-gallery-transferred');
  }
  poseRect(emLeft,fullLeft,fullLeft,1);
  emLeft.style.width=fullLeft.w.toFixed(2)+'px';
  // Full-size destination remains opaque: no old Contents behind the transfer.
  emLeft.style.clipPath='none';
  poseRect(emRight,fullRight,fullRight,1);
  emRight.style.clipPath='none';
  // Hold an opaque original-gallery matte over the old magazine cover.
  // The archive image can fade inside that stable panel when loaded.
  emRight.style.opacity='1';
  olive.style.visibility=oliveShowing?'visible':'hidden';
  olive.style.opacity='1';
  olive.style.backgroundColor='#f0eee7';
  olive.style.clipPath='inset(0 0 0 '+((1-oliveIn)*100).toFixed(3)+'%)';
  olive.style.pointerEvents=oliveIn>.999?'auto':'none';
  olive.inert=oliveIn<=.999;
  olive.setAttribute('aria-hidden',oliveIn>.999?'false':'true');
  // All Olive content arrives as a composed page, not a staggered set of
  // banners, white rectangles and floating speaker/gallery panels.
  oliveHero.style.transform='none';
  oliveHero.style.opacity='1';
  heroFolio.style.opacity='1';
  oliveEditorial.style.opacity='1';
  oliveEditorial.style.clipPath='none';
  $('.olive-proof__editorial > div').style.opacity='1';
  $('.olive-proof__editorial > a').style.opacity='1';
  $('.olive-proof__kicker').style.opacity='1';
  oliveBottom.style.opacity='1';
  oliveRegister.style.clipPath='none';
  oliveWindow.style.clipPath='none';
  $('.olive-proof__folio').style.opacity='1';
  // The Magazine->Emmaus projection is already faded when the Olive reveal
  // starts; NEVER leave its z-index:7 plate painting over the incoming page.
  if(transferFigure&&oliveIn>.001){
   transferFigure.style.setProperty('--p2-transfer-visible',String(fieldExit));
  }
  const section=fullDistance>=15.14?'07 / 07 — DAYLIGHT CAFÉ':fullDistance>=13.57?'06 / 07 — PARADISE CINEMA':fullDistance>=12?'05 / 07 — DAWN BOOKSHOP':distance<3.0775?'01 / 07 — CHURCH':distance<6.5?'02 / 07 — MAGAZINE':distance<9.44?'03 / 07 — EMMAUS':'04 / 07 — OLIVE MOUNTAIN';
  phase.textContent=section;document.body.dataset.proofScene=section.split(' / ')[0];
  seek.value=String(fullDistance/timelineMax*100);percent.textContent=(fullDistance/timelineMax*100).toFixed(0)+'%';lastPaint=distance;
 }
 function requestPaint(){if(!queued){queued=true;requestAnimationFrame(paint)}}
 function seekTo(distance,updateUrl=false){
  const target=track.getBoundingClientRect().top+scrollY+distance*innerHeight;
  scrollTo({top:target,behavior:'instant'});requestPaint();
  if(updateUrl){const url=new URL(location.href);url.searchParams.set('d',distance.toFixed(2));history.replaceState(null,'',url);}
 }
 document.querySelectorAll('[data-jump]').forEach(b=>b.addEventListener('click',()=>seekTo(Number(b.dataset.jump),true)));
 seek.addEventListener('input',()=>seekTo(Number(seek.value)/100*timelineMax,true));
 addEventListener('scroll',requestPaint,{passive:true});addEventListener('resize',()=>{settledGeometry=null;settledGeometryDoc=null;requestPaint()},{passive:true});
 document.addEventListener('visibilitychange',requestPaint);
 base.addEventListener('load',()=>{
  frameLoaded=true;requestPaint();
  const nested=base.contentDocument?.querySelector('.p2-magazine iframe:not(.p2-magazine__home-film)');
  nested?.addEventListener('load',requestPaint,{once:true});
 });
 const initial=new URLSearchParams(location.search).get('d');
 requestAnimationFrame(()=>seekTo(initial===null?7.85:clamp(Number(initial)||0,0,timelineMax)));
 requestPaint();
})();
