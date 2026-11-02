/* P2 / 03 — editorial atlas, chronology and quiet ONE book selector.
 * Data is read only from ONE's own chapter records. Never invent routes,
 * timelines, captions or new engravings to fill missing sources.
 */
(()=>{'use strict';
 const root=document.getElementById('emmaus'),D=window.ONE_DATA;if(!root||!D?.books)return;
 const $=id=>document.getElementById(id),books=D.books;
 const drawer=$('em-book-drawer'),toggle=$('em-book-toggle'),close=$('em-book-drawer-close'),
  search=$('em-book-search'),rail=$('emmaus-rail');
 const figure=$('em-context-map-figure'),image=$('em-context-map-image'),
  credit=$('em-context-map-credit'),guide=$('em-context-map-guide'),
  places=$('em-context-map-places'),mapTitle=$('em-context-map-title'),
  mapSource=$('em-context-map-source'),timelineTitle=$('em-context-time-title'),
  timelineNote=$('em-context-time-note'),timelineEvents=$('em-context-time-events');
 if(!drawer||!toggle||!close||!search||!rail||!figure||!timelineEvents)return;
 // Existing ONE book buttons preserve their canonical data-book identities.
 // Add the actual ONE book names so the chooser works without memorizing 66 numbers.
 for(const b of rail.querySelectorAll('[data-book]')){
  const n=Number(b.dataset.book),entry=books[n-1];if(!entry)continue;
  b.replaceChildren();
  const numeral=document.createElement('span');numeral.className='em-book-num';numeral.textContent=String(n).padStart(2,'0');
  const label=document.createElement('span');label.className='em-book-label';label.textContent=entry[1];
  const en=document.createElement('small');en.textContent=entry[2];
  b.append(numeral,label,en);
 }
 function showDrawer(open){
  drawer.hidden=!open;toggle.setAttribute('aria-expanded',String(open));
  if(open){search.focus({preventScroll:true});search.value='';filterBooks('');}
  else toggle.focus({preventScroll:true});
 }
 function filterBooks(term){
  const q=String(term||'').trim().toLocaleLowerCase();
  for(const button of rail.querySelectorAll('[data-book]')){
   const entry=books[Number(button.dataset.book)-1];if(!entry)continue;
   button.hidden=!!q&&!([String(entry[0]),String(entry[0]).padStart(2,'0'),entry[1].toLocaleLowerCase(),entry[2].toLocaleLowerCase()]
    .some(x=>x.includes(q)));
  }
 }
 toggle.addEventListener('click',()=>showDrawer(drawer.hidden));
 close.addEventListener('click',()=>showDrawer(false));
 search.addEventListener('input',()=>filterBooks(search.value));
 search.addEventListener('keydown',e=>{if(e.key==='Escape'){e.preventDefault();showDrawer(false)}});
 drawer.addEventListener('keydown',e=>{if(e.key==='Escape'){e.preventDefault();showDrawer(false)}});
 rail.addEventListener('click',e=>{
  if(e.target.closest('[data-book]'))showDrawer(false);
 });
 // A change of book does not change the P2 chapter title, only its ONE contents.
 let selectedKey='',lastMap='';
 const sourceFor=n=>n===42?D.luke:n===40?D.matthew:D.studyBooks?.[n];
 const put=(node,text)=>{node.textContent=String(text||'')};
 const label=(parent,text,tag='span')=>{const node=document.createElement(tag);node.textContent=String(text);parent.append(node);return node};
 function paintMap(map,chapter){
  const valid=map&&typeof map==='object';
  const url=valid&&typeof map.image==='string'&&/^https:\/\//.test(map.image)?map.image:null;
  put(mapTitle,valid?(map.title||map.imageTitle||'本章地理'):'本章閱讀路徑');
  const detail=valid?[map.guide||map.preface||'',...(map.places||[]).slice(0,6).map(x=>'· '+x)].filter(Boolean):
   [chapter?.movement||chapter?.position||chapter?.story||'從 ONE 的本章結構與經文脈絡開始查考。'];
  guide.replaceChildren();
  for(const text of detail.slice(0,4))label(guide,text,'p');
  places.replaceChildren();
  if(!valid&&chapter?.route?.length){
   for(const item of chapter.route.slice(0,5)){label(places,item[0]+' / '+item[1]);}
  }
  mapSource.hidden=!valid||!map.source;
  if(valid&&map.source){mapSource.href=map.source;mapSource.textContent='查看 ONE 原始史地圖 ↗';}
  figure.hidden=!url;
  if(url){
   if(image.dataset.mapSrc!==url){image.dataset.mapSrc=url;image.src=url;}
   image.alt=map.imageTitle||map.title||'ONE 聖經史地圖';
   credit.textContent='ONE · '+(map.imageTitle||map.title||'BIBLE GEOGRAPHY');
  }else{image.removeAttribute('src');image.dataset.mapSrc='';}
 }
 function paintTimeline(study,source){
  timelineEvents.replaceChildren();
  const data=study?.timeline;
  const events=Array.isArray(data?.events)&&data.events.length?data.events:
   Array.isArray(source?.movements)?source.movements.map(([id,range,title])=>[range,title,'書卷結構']):
   Array.isArray(study?.route)?study.route.map(([range,title])=>[range,title,'經文路徑']):[];
  put(timelineTitle,data?.title||(source?.movements?.length?'書卷結構':'本章經文路徑'));
  put(timelineNote,data?.note||source?.summary||study?.position||'');
  for(const item of events.slice(0,5)){
   const li=document.createElement('li');label(li,item[0]||'','small');label(li,item[1]||'','strong');
   if(item[2])label(li,item[2],'span');timelineEvents.append(li);
  }
  if(!events.length){
   const li=document.createElement('li');label(li,study?.movement||source?.summary||'閱讀本章','strong');timelineEvents.append(li);
  }
 }
 function render(book,chapter){
  const n=Number(book),ch=Number(chapter);
  if(n<1||n>66||!Number.isInteger(n))return;
  const key=n+':'+ch,source=sourceFor(n);
  const study=source?.chapterStudies?.[String(ch)]||null;
  // A fresh ONE async module may have arrived for the same book/chapter.
  if(key===selectedKey&&lastMap===study)return;
  selectedKey=key;lastMap=study;
  paintMap(study?.map,study);
  paintTimeline(study,source);
 }
 root.addEventListener('p2:one-selection',e=>render(e.detail?.book,e.detail?.chapter));
 render(Number(root.dataset.selectedBook)||42,Number(root.dataset.selectedChapter)||24);
})();
