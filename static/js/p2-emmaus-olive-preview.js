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
 // Use exactly the original 241-plate Doré asset registry and the approved
 // P2 city/castle selection. Do not pretend an image depicts an unrelated book.
 const registry=window.ONE_DORE_COVER_REGISTRY,ids=[10,13,48,64,115,123,127,241];
 const plates=ids.map(id=>({id,file:registry?.files?.[id],title:registry?.titles?.[id]||String(registry?.files?.[id]||'').replace(/^\d+[A-Z]?\./,'').replace(/\.[^.]+$/,'')}));
 if(plates.some(p=>!p.file))throw Error('Shared Doré source inventory is incomplete');
 const plateEls=[$('#em-plate-a'),$('#em-plate-b')];let galleryIndex=0,activeSlot=0,galleryTimer=0,galleryLive=false,plateVersion=0;
 const imgUrl=plate=>'https://commons.wikimedia.org/wiki/Special:Redirect/file/'+encodeURIComponent(plate.file)+'?width=1200';
 async function showPlate(index){
  const ticket=++plateVersion,plate=plates[index%plates.length],slot=1-activeSlot,img=plateEls[slot];
  const ok=await new Promise(resolve=>{
   img.onload=()=>resolve(true);img.onerror=()=>resolve(false);img.src=imgUrl(plate);
   if(img.complete&&img.naturalWidth>0)resolve(true);
  });
  if(!ok||ticket!==plateVersion)return;
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
 let frameLoaded=false,lastPaint=NaN,queued=false;
 function paint(){
  queued=false;const vh=Math.max(1,innerHeight),top=track.getBoundingClientRect().top;
  const distance=clamp(-top/vh,0,12),legacyDistance=Math.min(distance,6.5),churchEnd=3.0775,magazineEnd=6.5;
  let legacy;
  if(top>0)legacy=clamp((vh-top)/vh,0,1)*.1/2.9;
  else if(legacyDistance<=churchEnd){const scene=legacyDistance<=1.8?.1+legacyDistance*(.4/1.8):.5+(legacyDistance-1.8);legacy=scene/2.9;}
  else{const scene=2.37+(legacyDistance-churchEnd)/(magazineEnd-churchEnd)*(4-2.37);legacy=scene<=2.9?.75*scene/2.9:.75+.25*(scene-2.9)/1.1;}
  if(frameLoaded)base.contentWindow?.postMessage({type:'westside-p2-scroll',progress:clamp(legacy),active:distance<6.6},location.origin);
  const emIn=smooth((distance-6.50)/.72),oliveIn=smooth((distance-8.64)/.82);
  const emOpacity=emIn*(1-oliveIn),oliveOpacity=oliveIn;
  emmaus.style.visibility=emOpacity>.001?'visible':'hidden';emmaus.style.opacity=String(emOpacity);
  emmaus.style.pointerEvents=emOpacity>.98?'auto':'none';emmaus.inert=emOpacity<=.98;emmaus.setAttribute('aria-hidden',emOpacity>.98?'false':'true');
  olive.style.visibility=oliveOpacity>.001?'visible':'hidden';olive.style.opacity=String(oliveOpacity);
  olive.style.pointerEvents=oliveOpacity>.98?'auto':'none';olive.inert=oliveOpacity<=.98;olive.setAttribute('aria-hidden',oliveOpacity>.98?'false':'true');
  emmaus.style.transform='translate3d('+((1-emIn)*-12).toFixed(3)+'%,0,0)';
  olive.style.clipPath='inset('+((1-oliveIn)*100).toFixed(2)+'% 0 0 0)';
  const emActive=emOpacity>.02&&document.visibilityState==='visible';syncGallery(emActive);
  const section=distance<3.0775?'01 / 07 — CHURCH':distance<6.5?'02 / 07 — MAGAZINE':distance<9.05?'03 / 07 — EMMAUS':'04 / 07 — OLIVE MOUNTAIN';
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
 base.addEventListener('load',()=>{frameLoaded=true;requestPaint()});
 const initial=new URLSearchParams(location.search).get('d');
 requestAnimationFrame(()=>seekTo(initial===null?7.85:clamp(Number(initial)||0,0,12)));
 requestPaint();
})();
