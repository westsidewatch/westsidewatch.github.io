const D=window.ONE_DATA,$=selector=>document.querySelector(selector),$$=selector=>[...document.querySelectorAll(selector)];
document.documentElement.classList.add('one-bound');

const STORAGE_KEY='one-progress-v2';
const LEGACY_STORAGE_KEY='one-progress-v1';
const MODE_KEY='one-reading-mode-v1';
const clone=value=>JSON.parse(JSON.stringify(value));
const params=new URLSearchParams(location.search);
const requestedBookValue=Number(params.get('book'));
const requestedBook=D.studyBooks?.[requestedBookValue]?requestedBookValue:null;
const requestedChapterValue=Number(params.get('chapter'));
const defaults=()=>({version:2,profiles:[],activeProfile:null,archives:[]});

function normalizeState(value){
  const raw=value&&typeof value==='object'?value:{},seen=new Set();
  const profiles=(Array.isArray(raw.profiles)?raw.profiles:[]).filter(item=>item&&typeof item==='object').map((item,index)=>{
    let id=String(item.id||`group-${index+1}`);
    while(seen.has(id))id+=`-${index+1}`;
    seen.add(id);
    const books=item.books&&typeof item.books==='object'?clone(item.books):{};
    const activeBook=Number(item.activeBook);
    return {id,name:String(item.name||'未命名查經組').trim().slice(0,40)||'未命名查經組',created:item.created||new Date().toISOString(),activeBook:D.studyBooks?.[activeBook]?activeBook:null,books,history:Array.isArray(item.history)?clone(item.history):[]};
  });
  const activeProfile=profiles.some(item=>item.id===raw.activeProfile)?raw.activeProfile:(profiles[0]?.id||null);
  return {version:2,profiles,activeProfile,archives:Array.isArray(raw.archives)?clone(raw.archives):[]};
}
function loadState(){
  try{
    const current=localStorage.getItem(STORAGE_KEY);
    if(current!==null)return normalizeState(JSON.parse(current));
    const legacy=localStorage.getItem(LEGACY_STORAGE_KEY);
    if(legacy!==null){const migrated=normalizeState(JSON.parse(legacy));localStorage.setItem(STORAGE_KEY,JSON.stringify(migrated));return migrated}
  }catch(error){}
  return defaults();
}
function loadReadingMode(){const query=params.get('mode');if(query==='reading'||query==='study')return query;try{const saved=localStorage.getItem(MODE_KEY);if(saved==='reading'||saved==='study')return saved}catch(error){}return 'study'}
function hydrateFrames(root=document){root.querySelectorAll('iframe[data-src]').forEach(frame=>{if(frame.offsetWidth>0&&!frame.hasAttribute('src'))frame.setAttribute('src',frame.dataset.src)})}
function motionDelay(){return matchMedia('(prefers-reduced-motion: reduce)').matches?0:520}
function saveState(){try{localStorage.setItem(STORAGE_KEY,JSON.stringify(state))}catch(error){}}

let state=loadState();
function profile(){return state.profiles.find(item=>item.id===state.activeProfile)||state.profiles[0]||null}
function bookInfo(number){return D.books.find(book=>book[0]===number)}
function studyBook(number=currentBookNumber){return D.studyBooks?.[number]}
function bookState(number,owner=profile()){return owner?.books?.[String(number)]||{status:'dormant',completedChapter:0}}
function nextChapterFor(number,total,owner=profile()){return Math.min((bookState(number,owner).completedChapter||0)+1,total)}
function validatedChapter(number,chapter){const total=studyBook(number)?.chapters.length||1;return Number.isInteger(chapter)&&chapter>=1&&chapter<=total?chapter:null}

const savedStart=profile()?.activeBook;
let currentBookNumber=requestedBook||(D.studyBooks?.[savedStart]?savedStart:40);
let currentChapter=1;
let readingMode=loadReadingMode();
let selectedBookNumber=null;
let pendingBookNumber=null;
let newGroupSelection=false;
let coverRail=null;

const initialChapter=validatedChapter(currentBookNumber,requestedChapterValue);
currentChapter=initialChapter||1;

function renderCover(){
  const list=$('#cover-books'),active=profile(),activeBook=active?.activeBook?bookInfo(active.activeBook):null;
  coverRail?.destroy();coverRail=null;
  list.innerHTML='';
  list.tabIndex=0;
  list.setAttribute('role','listbox');
  list.dataset.profile=active?.id||'';
  $('#cover-groups').setAttribute('aria-label',active?`我的查經組，目前為${active.name}`:'建立查經組');
  D.books.forEach(book=>{
    const progress=bookState(book[0],active),available=Boolean(D.studyBooks?.[book[0]]),item=document.createElement('button');
    item.className=`cover-book ${progress.status}${available?' has-study':' forthcoming'}${selectedBookNumber===book[0]?' selected':''}`;
    item.dataset.book=book[0];
    item.type='button';
    item.tabIndex=-1;
    item.id=`cover-book-${book[0]}`;
    item.setAttribute('role','option');
    item.setAttribute('aria-label',`第 ${book[0]} 卷，${book[1]}，${available?'可開始查考':'研讀內容製作中'}`);
    item.innerHTML=`<span aria-hidden="true">${String(book[0]).padStart(2,'0')}</span><strong aria-hidden="true"><b>${book[1]}</b><i>${book[2]}</i></strong>`;
    item.addEventListener('click',event=>{
      if(coverRail?.shouldSuppressClick(event)){event.preventDefault();return}
      if(!item.classList.contains('rail-current')){coverRail?.settleTo(item,{reveal:true});return}
      selectCoverBook(book);
    });
    list.append(item);
  });
  coverRail=createCoverRail(list,activeBook?.[0]||1);
  renderGroupList();
}

function createCoverRail(list,startBook){
  const items=[...list.querySelectorAll('.cover-book')],step=38,reducedMotion=matchMedia('(prefers-reduced-motion: reduce)').matches;
  let position=Math.max(0,Math.min(items.length-1,startBook-1)),target=position,dragging=false,startY=0,startPosition=position,lastY=0,lastTime=0,velocity=0,frame=0,paintFrame=0,wheelTimer=0,didDrag=false,suppressClickUntil=0,revealTimer=0,destroyed=false;
  const clamp=value=>Math.max(0,Math.min(items.length-1,value));
  const paint=()=>{
    items.forEach((item,index)=>{
      const distance=index-position,absolute=Math.abs(distance),scale=1+Math.max(0,1-absolute)*1.48,opacity=Math.max(.1,1-absolute*.18);
      item.style.setProperty('--rail-y',`${distance*step}px`);
      item.style.setProperty('--rail-scale',scale.toFixed(3));
      item.style.setProperty('--rail-opacity',opacity.toFixed(3));
      item.classList.toggle('rail-near',absolute<.56);
    });
  };
  const reveal=()=>{
    clearTimeout(revealTimer);
    const index=Math.round(position);
    list.classList.add('is-settled');
    items.forEach((item,itemIndex)=>{const current=itemIndex===index;item.classList.toggle('rail-current',current);item.setAttribute('aria-selected',String(current))});
    list.setAttribute('aria-activedescendant',items[index]?.id||'');
  };
  const schedulePaint=()=>{if(!paintFrame)paintFrame=requestAnimationFrame(()=>{paintFrame=0;paint()})};
  const animate=()=>{
    if(destroyed)return;
    const delta=target-position;
    position+=delta*(reducedMotion?1:.2);
    if(Math.abs(delta)<.001){position=target;paint();if(!wheelTimer)reveal();frame=0;return}
    paint();frame=requestAnimationFrame(animate);
  };
  const settle=(next,{reveal:showName=true}={})=>{
    clearTimeout(wheelTimer);wheelTimer=0;target=clamp(next);list.classList.remove('is-settled');items.forEach(item=>item.classList.remove('rail-current'));
    if(frame)cancelAnimationFrame(frame);
    frame=requestAnimationFrame(animate);
    if(!showName)clearTimeout(revealTimer);
  };
  const settleTo=(item,options)=>settle(items.indexOf(item),options);
  const onDown=event=>{
    if(frame)cancelAnimationFrame(frame);frame=0;clearTimeout(wheelTimer);wheelTimer=0;
    dragging=true;didDrag=false;startY=lastY=event.clientY;startPosition=position;lastTime=performance.now();velocity=0;
  };
  const onMove=event=>{
    if(!dragging)return;
    const now=performance.now(),dy=event.clientY-lastY,elapsed=Math.max(8,now-lastTime);
    if(!didDrag&&Math.abs(event.clientY-startY)>5){didDrag=true;list.setPointerCapture?.(event.pointerId);list.classList.add('is-dragging');list.classList.remove('is-settled');items.forEach(item=>item.classList.remove('rail-current'))}
    if(!didDrag)return;
    velocity=dy/elapsed;position=clamp(startPosition-(event.clientY-startY)/step);target=position;
    lastY=event.clientY;lastTime=now;schedulePaint();
  };
  const onUp=event=>{
    if(!dragging)return;
    dragging=false;list.classList.remove('is-dragging');
    if(list.hasPointerCapture?.(event.pointerId))list.releasePointerCapture(event.pointerId);
    if(!didDrag)return;
    const projected=clamp(position-velocity*6.4);suppressClickUntil=performance.now()+360;settle(Math.round(projected));
  };
  const onWheel=event=>{
    if(Math.abs(event.deltaY)<Math.abs(event.deltaX))return;
    event.preventDefault();list.classList.remove('is-settled');items.forEach(item=>item.classList.remove('rail-current'));
    target=clamp(position+event.deltaY/step);
    if(!frame)frame=requestAnimationFrame(animate);
    clearTimeout(wheelTimer);wheelTimer=setTimeout(()=>{wheelTimer=0;settle(Math.round(target))},110);
  };
  const onKey=event=>{
    if(!['ArrowUp','ArrowDown','Home','End','Enter',' '].includes(event.key))return;
    if(event.key==='Enter'||event.key===' '){const current=items[Math.round(position)];if(current.classList.contains('rail-current'))current.click();else settleTo(current);event.preventDefault();return}
    event.preventDefault();settle(event.key==='Home'?0:event.key==='End'?items.length-1:Math.round(position)+(event.key==='ArrowDown'?1:-1));
  };
  list.addEventListener('pointerdown',onDown);list.addEventListener('pointermove',onMove);list.addEventListener('pointerup',onUp);list.addEventListener('pointercancel',onUp);list.addEventListener('wheel',onWheel,{passive:false});list.addEventListener('keydown',onKey);
  paint();revealTimer=setTimeout(reveal,850);
  const shouldSuppressClick=event=>event.detail!==0&&performance.now()<suppressClickUntil;
  return {shouldSuppressClick,settleTo,destroy(){destroyed=true;cancelAnimationFrame(frame);cancelAnimationFrame(paintFrame);clearTimeout(wheelTimer);clearTimeout(revealTimer);list.removeEventListener('pointerdown',onDown);list.removeEventListener('pointermove',onMove);list.removeEventListener('pointerup',onUp);list.removeEventListener('pointercancel',onUp);list.removeEventListener('wheel',onWheel);list.removeEventListener('keydown',onKey)}};
}

function selectCoverBook(book){
  selectedBookNumber=book[0];
  $$('.cover-book').forEach(item=>item.classList.toggle('selected',Number(item.dataset.book)===book[0]));
  openBookDialog(book,{forceNewGroup:newGroupSelection||!profile()});
}

function showDialog(dialog){dialog.hidden=false;document.body.classList.add('one-dialog-open');requestAnimationFrame(()=>dialog.classList.add('visible'))}
function hideDialog(dialog){dialog.classList.remove('visible');dialog.hidden=true;if($('#book-dialog').hidden&&$('#groups-dialog').hidden)document.body.classList.remove('one-dialog-open')}
function openBookDialog(book,{forceNewGroup=false}={}){
  const available=Boolean(D.studyBooks?.[book[0]]),active=profile();
  pendingBookNumber=book[0];
  newGroupSelection=forceNewGroup;
  $('#book-dialog-kicker').textContent=`BOOK ${String(book[0]).padStart(2,'0')} · SELECTED`;
  $('#book-dialog-number').textContent=String(book[0]).padStart(2,'0');
  $('#book-dialog-title').textContent=book[1];
  $('#book-dialog-en').textContent=book[2];
  $('#book-dialog-question').textContent=available?'是否確定查考這一卷？':'本卷研讀內容仍在製作中';
  $('#book-dialog-context').textContent=available?(forceNewGroup?'確定經卷後，下一步為查經組命名。':`目前查經組：${active.name}`):'目前已備妥：馬太福音、帖撒羅尼迦前書、帖撒羅尼迦後書。';
  $('#confirm-book').textContent=forceNewGroup?'確定此卷，下一步':`以「${active?.name||''}」查考此卷`;
  $('#confirm-book').disabled=!available;
  $('#confirm-new-group').hidden=forceNewGroup||!active;
  $('#confirm-new-group').disabled=!available;
  $('#book-confirm-step').hidden=false;
  $('#group-start-step').hidden=true;
  showDialog($('#book-dialog'));
  requestAnimationFrame(()=>$('#book-dialog-title').setAttribute('tabindex','-1'));
}
function cancelBookDialog(){
  hideDialog($('#book-dialog'));
  pendingBookNumber=null;selectedBookNumber=null;
  $$('.cover-book').forEach(item=>item.classList.remove('selected'));
}
function showGroupStartStep(){
  const book=bookInfo(pendingBookNumber);
  if(!book||!studyBook(book[0]))return;
  newGroupSelection=true;
  $('#book-confirm-step').hidden=true;
  $('#group-start-step').hidden=false;
  $('#group-start-book').textContent=`已確定：第 ${String(book[0]).padStart(2,'0')} 卷 · ${book[1]} · ${book[2]}`;
  const input=$('#group-start-name');input.value='';input.setCustomValidity('');input.focus();
}

function activateBook(number,{chapter=null}={}){
  const volume=studyBook(number),book=bookInfo(number);
  if(!volume||!book)return false;
  currentBookNumber=number;
  const progress=bookState(number),resume=progress.status==='completed'?Math.max(1,Math.min(progress.completedChapter||book[3],book[3])):nextChapterFor(number,book[3]);
  currentChapter=validatedChapter(number,chapter)||resume||1;
  renderBookShell();
  renderChapters();
  showChapter(currentChapter,volume.chapters[currentChapter-1]);
  return true;
}

function startBookForProfile(owner,number,{open=true,chapter=null}={}){
  const volume=studyBook(number),book=bookInfo(number);
  if(!owner||!volume||!book)return false;
  owner.books=owner.books||{};
  owner.books[String(number)]=owner.books[String(number)]||{status:'active',completedChapter:0};
  owner.activeBook=number;state.activeProfile=owner.id;
  currentBookNumber=number;
  const progress=bookState(number,owner),resume=progress.status==='completed'?Math.max(1,Math.min(progress.completedChapter||book[3],book[3])):nextChapterFor(number,book[3],owner);
  currentChapter=validatedChapter(number,chapter)||resume||1;
  saveState();renderBookShell();renderProfiles();
  if(open)openBook(book,{chapter:currentChapter});
  else{activateBook(number,{chapter:currentChapter});$('[data-view="view-chapter"]').click();window.scrollTo({top:0,behavior:'smooth'})}
  return true;
}

function openBook(book,{chapter=null}={}){
  const selected=$(`.cover-book[data-book="${book[0]}"]`);
  selected?.classList.add('entering');
  $('#one-cover').classList.add('opening-book');
  setTimeout(()=>{
    $('#one-cover').hidden=true;
    $('#one-cover').classList.remove('opening-book');
    selected?.classList.remove('entering');
    $$('.app-layer').forEach(element=>element.hidden=false);
    document.body.classList.add('book-open');
    activateBook(book[0],{chapter});
    $('[data-view="view-chapter"]').click();
    window.scrollTo({top:0,behavior:'auto'});
  },motionDelay());
}

function returnToCover({createGroup=false}={}){
  document.body.classList.add('closing-book');
  setTimeout(()=>{
    $$('.app-layer').forEach(element=>element.hidden=true);
    $('#one-cover').hidden=false;
    document.body.classList.remove('book-open','closing-book');
    const url=new URL(location.href);
    ['book','chapter','mode'].forEach(key=>url.searchParams.delete(key));
    history.replaceState(null,'',url);
    document.title='ONE · 一卷入夜，合卷天明';
    newGroupSelection=createGroup;selectedBookNumber=null;renderCover();
    window.scrollTo({top:0,behavior:'auto'});
    if(createGroup)requestAnimationFrame(()=>$('#cover-books').scrollIntoView({behavior:'smooth',block:'start'}));
  },motionDelay());
}
$('#return-cover').onclick=()=>returnToCover();

function beginNewGroupSelection(){
  newGroupSelection=true;selectedBookNumber=null;renderCover();
  $('#cover-books').scrollIntoView({behavior:'smooth',block:'start'});
  $('#cover-books').focus({preventScroll:true});
}

function renderGroupList(){
  const list=$('#local-group-list');list.innerHTML='';
  state.profiles.forEach((item,index)=>{
    const activeBook=item.activeBook?bookInfo(item.activeBook):null,progress=activeBook?bookState(activeBook[0],item):null;
    const button=document.createElement('button');
    button.type='button';button.className='local-group';button.dataset.profile=item.id;
    if(item.id===state.activeProfile)button.classList.add('current');
    const folio=document.createElement('span'),name=document.createElement('strong'),meta=document.createElement('small'),action=document.createElement('i');
    folio.textContent=`GROUP ${String(index+1).padStart(2,'0')}`;name.textContent=item.name;
    meta.textContent=activeBook?`${activeBook[1]} · ${progress.completedChapter||0} / ${activeBook[3]} 章`:'尚未開卷';
    action.textContent=item.id===state.activeProfile?'目前查經組 · 繼續':'切換並繼續';
    button.append(folio,name,meta,action);button.onclick=()=>switchProfile(item.id,{open:true});list.append(button);
  });
}
function openGroupsDialog(){if(!state.profiles.length){beginNewGroupSelection();return}renderGroupList();showDialog($('#groups-dialog'));requestAnimationFrame(()=>$('#local-group-list button')?.focus())}
function closeGroupsDialog(){hideDialog($('#groups-dialog'))}
function switchProfile(id,{open=false}={}){
  const owner=state.profiles.find(item=>item.id===id);if(!owner)return;
  state.activeProfile=id;
  const number=D.studyBooks?.[owner.activeBook]?owner.activeBook:Number(Object.keys(owner.books||{}).find(key=>D.studyBooks?.[Number(key)]));
  if(number){owner.activeBook=number;closeGroupsDialog();startBookForProfile(owner,number,{open})}
  else{saveState();closeGroupsDialog();renderProfiles();renderCover()}
}

$('#cover-groups').onclick=openGroupsDialog;
$('#groups-new').onclick=()=>{closeGroupsDialog();beginNewGroupSelection()};
$('#close-groups-dialog').onclick=closeGroupsDialog;
$('#groups-dialog').onclick=event=>{if(event.target===$('#groups-dialog'))closeGroupsDialog()};
$('#close-book-dialog').onclick=cancelBookDialog;
$('#cancel-book').onclick=cancelBookDialog;
$('#book-dialog').onclick=event=>{if(event.target===$('#book-dialog'))cancelBookDialog()};
$('#confirm-book').onclick=()=>{const active=profile();if(!studyBook(pendingBookNumber))return;if(newGroupSelection||!active)showGroupStartStep();else{const number=pendingBookNumber;hideDialog($('#book-dialog'));pendingBookNumber=null;selectedBookNumber=null;startBookForProfile(active,number,{open:true})}};
$('#confirm-new-group').onclick=showGroupStartStep;
$('#back-book-confirm').onclick=()=>{$('#group-start-step').hidden=true;$('#book-confirm-step').hidden=false;$('#confirm-book').focus()};
$('#group-start-name').oninput=event=>event.currentTarget.setCustomValidity('');
$('#group-start-step').onsubmit=event=>{
  event.preventDefault();
  const input=$('#group-start-name'),name=input.value.trim(),start=pendingBookNumber,book=bookInfo(start);
  if(!name||!book||!studyBook(start))return;
  if(state.profiles.some(item=>item.name.toLocaleLowerCase()===name.toLocaleLowerCase())){input.setCustomValidity('這個瀏覽器已有同名查經組，請使用不同名稱。');input.reportValidity();return}
  const id=`group-${Date.now()}-${Math.random().toString(36).slice(2,7)}`;
  const owner={id,name,created:new Date().toISOString(),activeBook:start,books:{[String(start)]:{status:'active',completedChapter:0}},history:[]};
  state.profiles.push(owner);state.activeProfile=id;saveState();hideDialog($('#book-dialog'));pendingBookNumber=null;selectedBookNumber=null;newGroupSelection=false;startBookForProfile(owner,start,{open:true,chapter:1});
};

document.addEventListener('keydown',event=>{
  if(event.key!=='Escape')return;
  if(!$('#book-dialog').hidden)cancelBookDialog();
  else if(!$('#groups-dialog').hidden)closeGroupsDialog();
});

const reading=$('#light-reading'),openLight=$('#open-scripture'),closeLight=$('#close-scripture');
function showLight(){reading.hidden=false;requestAnimationFrame(()=>reading.classList.add('visible'));document.body.classList.add('reading-light');closeLight.focus()}
function hideLight(){reading.classList.remove('visible');document.body.classList.remove('reading-light');setTimeout(()=>{reading.hidden=true;openLight.focus()},motionDelay())}
openLight.onclick=showLight;
closeLight.onclick=hideLight;
reading.onclick=event=>{if(event.target===reading)hideLight()};
document.addEventListener('keydown',event=>{if(event.key==='Escape'&&!reading.hidden)hideLight()});

const bookGrid=$('#book-grid'),chapterGrid=$('#chapter-grid'),detail=$('#book-detail');
function renderBooks(){
  bookGrid.innerHTML='';
  D.books.forEach(book=>{
    const progress=bookState(book[0]),visible=progress.status!=='dormant',available=Boolean(D.studyBooks?.[book[0]]);
    const element=document.createElement(visible?'button':'div');
    element.className=`book ${progress.status}${available?' available':''}`;
    element.setAttribute('aria-label',visible?book[1]:`第 ${book[0]} 卷`);
    element.innerHTML=`<span>${String(book[0]).padStart(2,'0')}</span><strong>${visible?book[1]:''}</strong><small>${visible?book[2]:''}</small>`;
    if(visible){element.type='button';element.onclick=()=>available?openStudyFromGrid(book):showBook(book)}
    bookGrid.append(element);
  });
}
function openStudyFromGrid(book){startBookForProfile(profile(),book[0],{open:false})}
function showBook(book){const progress=bookState(book[0]);detail.className='book-detail open';detail.innerHTML=`<p class="kicker">Book ${String(book[0]).padStart(2,'0')}</p><h3>${book[1]}<small>${book[2]}</small></h3><p>${progress.status==='completed'?`全 ${book[3]} 章 · 已完成`:`進行中 · 已完成 ${progress.completedChapter} / ${book[3]} 章 · 下一章 ${nextChapterFor(book[0],book[3])}`}</p>`;detail.scrollIntoView({behavior:'smooth',block:'nearest'})}

function renderBookShell(){
  const volume=studyBook(),book=bookInfo(currentBookNumber),study=volume.chapterStudies[String(currentChapter)]||volume.chapterStudies['1'];
  $('#current-book-title').textContent=volume.name;
  $('#current-book-en').textContent=volume.nameEn;
  $('#current-book-meta').textContent=`第 ${String(currentBookNumber).padStart(2,'0')} 卷 · 共 ${book[3]} 章`;
  $('#frontispiece-kicker').textContent=`Book ${String(currentBookNumber).padStart(2,'0')} · ${volume.nameEn}`;
  $('#frontispiece-title').textContent=volume.name;
  $('#frontispiece-chapter').textContent=`第 ${currentChapter} 章 · ${study.title}`;
  $('#movement-grid').innerHTML=volume.movements.map(m=>`<div class="movement"><span>${m[0]} · ${m[1]}章</span><strong>${m[2]}</strong></div>`).join('');
  const first=volume.nowCards?.[0]||['本卷',volume.summary],second=volume.nowCards?.[1]||['線索',volume.meta.at(-1)?.[1]||'逐章研讀'];
  $('#now-card-one-title').textContent=first[0];$('#now-card-one-copy').textContent=first[1];
  $('#now-card-two-title').textContent=second[0];$('#now-card-two-copy').textContent=second[1];
  $('[data-open-chapter]').textContent=`進入${volume.name}第 ${currentChapter} 章`;
  document.body.dataset.book=currentBookNumber;
}

function renderChapters(){
  const volume=studyBook(),progress=bookState(currentBookNumber),next=nextChapterFor(currentBookNumber,volume.chapters.length);
  chapterGrid.innerHTML='';
  volume.chapters.forEach((name,index)=>{
    const number=index+1,status=number<=progress.completedChapter?'completed':number===next&&progress.status==='active'?'current':'upcoming',ready=Boolean(volume.chapterStudies[String(number)]);
    const element=document.createElement(ready?'button':'div');
    element.className=`chapter ${status}${ready?' available':''}`;
    element.dataset.chapter=number;
    element.innerHTML=`<span>${String(number).padStart(2,'0')}</span><strong>${ready?name:''}</strong>`;
    if(ready){element.type='button';element.onclick=()=>{showChapter(number,name);$('#chapter-detail').scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth',block:'start'})}}
    chapterGrid.append(element);
  });
  markCurrentChapter(currentChapter);
}

const resourceCard=resource=>`<a class="resource-card-one${resource.core?' resource-card-one--core':''}" href="${resource.url}" target="_blank" rel="noopener noreferrer" aria-label="開啟 ${resource.name} 官方網站"><p class="resource-card-one__folio"><span>${resource.id}</span><small>DAWN LIBRARY</small></p><div class="resource-card-one__identity"><span>${resource.category}</span><h3>${resource.name}</h3><em>${resource.nameEn}</em></div><div class="resource-card-one__details"><p>${resource.description}</p><dl><div><dt>Spectrum</dt><dd>${resource.spectrum}</dd></div><div><dt>Access</dt><dd>${resource.access}</dd></div></dl><strong>Open resource <i aria-hidden="true">↗</i></strong></div></a>`;
const resourceGroups=[{label:'核心查經平台',en:'Core Bible Study Platforms',items:D.resources.filter(resource=>resource.core)},{label:'逐章伴讀資源',en:'Chapter Companions',items:D.resources.filter(resource=>!resource.core)}];
$('#resource-grid').innerHTML=resourceGroups.map(group=>`<section class="resource-group"><header class="resource-group-title"><p>${group.en}</p><h3>${group.label}</h3></header><div class="resource-grid">${group.items.map(resourceCard).join('')}</div></section>`).join('');

$$('.view-tabs button').forEach(button=>button.onclick=()=>{
  $$('.view-tabs button').forEach(item=>item.setAttribute('aria-selected','false'));
  button.setAttribute('aria-selected','true');
  $$('.view').forEach(view=>view.classList.remove('active'));
  const view=$('#'+button.dataset.view);view.classList.add('active');requestAnimationFrame(()=>hydrateFrames(view));
});

function renderProfiles(){
  const select=$('#profile-select'),owner=profile();select.innerHTML='';
  state.profiles.forEach(item=>{const option=document.createElement('option');option.value=item.id;option.textContent=item.name;option.selected=item.id===state.activeProfile;select.append(option)});
  select.disabled=!owner;
  $('#restart-profile').disabled=!owner;
  const active=owner?.activeBook?bookInfo(owner.activeBook):null,completed=owner?Object.values(owner.books||{}).filter(item=>item.status==='completed').length:0;
  $('#calendar-group-kicker').textContent=owner?.name||'本機查經組';
  $('#calendar-group-name').textContent=`時間待定 · ${owner?.name||'尚未建立查經組'}`;
  if(active){const progress=bookState(active[0],owner);$('#profile-progress').textContent=`${active[1]} ${progress.completedChapter||0} / ${active[3]}`;$('#profile-next').textContent=progress.status==='completed'?'本卷已完成':`下一次：第 ${nextChapterFor(active[0],active[3],owner)} 章`}else{$('#profile-progress').textContent='尚未開卷';$('#profile-next').textContent='返回一卷，選卷並建立查經組'}
  $('#profile-history-count').textContent=`${completed} 卷`;
  const trackedBooks=Object.entries(owner?.books||{}).filter(([number])=>Boolean(studyBook(Number(number))));
  const chaptersRead=trackedBooks.reduce((total,[number,item])=>total+Math.min(item.completedChapter||0,studyBook(Number(number)).chapters.length),0);
  const chaptersTracked=trackedBooks.reduce((total,[number])=>total+studyBook(Number(number)).chapters.length,0);
  document.documentElement.style.setProperty('--one-light-progress',String(chaptersRead));
  document.documentElement.style.setProperty('--one-light-level',String(chaptersTracked?chaptersRead/chaptersTracked:0));
  renderCover();renderBooks();
  if(studyBook()){renderChapters();updateCompleteButton()}
}

$('#profile-select').onchange=event=>switchProfile(event.target.value,{open:false});
$('#new-profile').onclick=()=>returnToCover({createGroup:true});
$('#restart-profile').onclick=()=>{if(profile())$('#restart-confirm').hidden=false};
$('#cancel-restart').onclick=()=>{$('#restart-confirm').hidden=true};
$('#confirm-restart').onclick=()=>{
  const current=profile();if(!current)return;
  const old=clone(current),stamp=new Date().toISOString(),start=old.activeBook&&D.studyBooks?.[old.activeBook]?old.activeBook:40;
  state.archives=state.archives||[];state.archives.push({...old,archived:stamp});
  const id=`round-${Date.now()}`;
  state.profiles.push({id,name:`${old.name} · 新一輪`,created:stamp,activeBook:start,books:{[start]:{status:'active',completedChapter:0}},history:[]});
  state.activeProfile=id;currentBookNumber=start;currentChapter=1;saveState();$('#restart-confirm').hidden=true;renderBookShell();renderProfiles();
};

async function copy(text,button){try{await navigator.clipboard.writeText(text);const old=button.textContent;button.textContent='已複製';setTimeout(()=>button.textContent=old,1600)}catch(error){button.textContent='請手動複製'}}
$('#copy-notice').onclick=event=>copy($('#notice-text').textContent,event.currentTarget);
$('#share-one').onclick=event=>copy(location.href,event.currentTarget);
$$('[data-open-chapter]').forEach(button=>button.onclick=()=>{const tab=$('[data-view="view-chapter"]');tab.click();$('#chapter-detail').scrollIntoView({behavior:'smooth',block:'start'})});

function syncChapterLocation(){const url=new URL(location.href);url.searchParams.set('book',currentBookNumber);url.searchParams.set('chapter',currentChapter);url.searchParams.set('mode',readingMode);history.replaceState(null,'',url)}
function applyReadingMode(mode,{sync=true}={}){readingMode=mode==='reading'?'reading':'study';document.body.classList.toggle('mode-reading',readingMode==='reading');document.body.classList.toggle('mode-study',readingMode==='study');$('#reading-mode-label').textContent=readingMode==='reading'?'閱讀模式':'查經模式';$$('[data-reading-mode]').forEach(button=>button.setAttribute('aria-pressed',String(button.dataset.readingMode===readingMode)));try{localStorage.setItem(MODE_KEY,readingMode)}catch(error){}if(sync)syncChapterLocation();requestAnimationFrame(()=>hydrateFrames($('#view-chapter')))}

function chapterTurnMarkup(number){
  const volume=studyBook(),last=volume.chapters.length;
  const previous=number>1?`<button type="button" data-turn-chapter="${number-1}" data-turn-direction="previous"><span>Previous · 上一章</span><strong>${String(number-1).padStart(2,'0')} · ${volume.chapters[number-2]}</strong></button>`:`<span class="chapter-turn__boundary"><i>Previous · 上一章</i><strong>卷首</strong></span>`;
  const next=number<last?`<button type="button" data-turn-chapter="${number+1}" data-turn-direction="next"><span>Next · 下一章</span><strong>${String(number+1).padStart(2,'0')} · ${volume.chapters[number]}</strong></button>`:`<span class="chapter-turn__boundary"><i>Next · 下一章</i><strong>卷終</strong></span>`;
  return `<nav class="chapter-turn" aria-label="${volume.name}章節翻頁">${previous}<p><span>${volume.nameEn}</span><b>${String(number).padStart(2,'0')}</b></p>${next}</nav>`;
}
function decorateLeaves(number){const volume=studyBook();[...$('#chapter-detail').children].filter(leaf=>leaf.matches('.study-intro,.chapter-section,.scripture-reading')).forEach(leaf=>{const head=document.createElement('p');head.className='running-head';head.setAttribute('aria-hidden','true');head.innerHTML=`<span>WESTSIDE WATCH · ONE</span><b>${volume.nameEn.toUpperCase()} · ${String(number).padStart(2,'0')}</b>`;leaf.prepend(head)})}
function markCurrentChapter(number){$$('#chapter-grid [data-chapter]').forEach(button=>{const active=Number(button.dataset.chapter)===number;button.classList.toggle('reading',active);if(active)button.setAttribute('aria-current','page');else button.removeAttribute('aria-current')})}
function turnChapter(target,direction){const chapterDetail=$('#chapter-detail');if(chapterDetail.classList.contains('page-turning'))return;const delay=matchMedia('(prefers-reduced-motion: reduce)').matches?0:220;chapterDetail.classList.add('page-turning',`page-turning--${direction}`);setTimeout(()=>{showChapter(target,studyBook().chapters[target-1]);chapterDetail.classList.remove('page-turning',`page-turning--${direction}`);chapterDetail.classList.add('page-arriving',`page-arriving--${direction}`);chapterDetail.scrollIntoView({behavior:'auto',block:'start'});setTimeout(()=>chapterDetail.classList.remove('page-arriving',`page-arriving--${direction}`),delay+80)},delay)}

function comparisonMarkup(study,volume){
  const model=study.comparison||{title:volume.comparisonTitle||'書卷互照',headers:volume.comparisonHeaders||['主題','本章','相關經文'],rows:study.harmony||[]};
  return `<section class="chapter-section"><h3>${model.title}</h3><div><table class="harmony"><thead><tr>${model.headers.map(header=>`<th>${header}</th>`).join('')}</tr></thead><tbody>${model.rows.map(row=>`<tr>${row.map(cell=>`<td>${cell}</td>`).join('')}</tr>`).join('')}</tbody></table></div></section>`;
}

function showChapter(number,name,{sync=true}={}){
  const volume=studyBook(),study=volume.chapterStudies[String(number)];
  if(!study){$('#chapter-detail').innerHTML=`<section class="chapter-section"><h3>第 ${number} 章</h3><div><p>${name}</p></div></section>`;return}
  currentChapter=number;
  if(sync)syncChapterLocation();
  markCurrentChapter(number);
  renderBookShell();
  const now=$('.now'),chapterStatus=now.querySelector('.status');
  document.documentElement.style.setProperty('--one-chapter-number',`"${String(number).padStart(2,'0')}"`);
  document.documentElement.style.setProperty('--one-book-running',`"${volume.nameEn.toUpperCase()}"`);
  $('[data-view="view-chapter"]').textContent=`${volume.name} ${number}`;
  $('#now-kicker').textContent=`${volume.nameEn} ${number}`;
  $('#now-chapter-title').textContent=`第 ${number} 章`;
  $('#now-card-three-copy').textContent=study.title;
  document.title=`${volume.name} ${number} · ${study.title} · ONE`;
  chapterStatus.querySelector('span').textContent=number===1?'起點':'本章';chapterStatus.querySelector('strong').textContent=`第 ${number} 章`;chapterStatus.querySelector('p').textContent=study.title;
  $('#frontispiece-chapter').textContent=`第 ${number} 章 · ${study.title}`;
  $('[data-open-chapter]').textContent=`進入${volume.name}第 ${number} 章`;
  {const coverArt=$('#chapter-cover-art'),credit=$('#chapter-art-credit');if(study.illustration){const engraving=`url("${study.illustration.src}")`;now.style.setProperty('--chapter-engraving',engraving);document.documentElement.style.setProperty('--one-chapter-engraving',engraving);coverArt.src=study.illustration.src;coverArt.alt=study.illustration.alt;coverArt.hidden=false;credit.href=study.illustration.source;credit.textContent=`Gustave Doré · ${study.illustration.title}`;credit.hidden=false}else{now.style.removeProperty('--chapter-engraving');document.documentElement.style.removeProperty('--one-chapter-engraving');coverArt.removeAttribute('src');coverArt.alt='';coverArt.hidden=true;credit.removeAttribute('href');credit.textContent='';credit.hidden=true}}
  const displayArt=study.illustration?`<figure class="chapter-illustration"><a href="${study.illustration.source}" target="_blank" rel="noopener"><img src="${study.illustration.src}" alt="${study.illustration.alt}" loading="eager"></a><figcaption>Gustave Doré · ${study.illustration.title}</figcaption></figure>`:'';
  const zh=`https://rcuv.hkbs.org.hk/CUNP1/${volume.zhCode}/${number}/`,en=`https://www.bible.com/bible/111/${volume.enCode}.${number}.NIV`,osm=`https://www.openstreetmap.org/export/embed.html?bbox=${encodeURIComponent(study.map?.bbox||'')}&layer=mapnik&marker=${encodeURIComponent(study.map?.marker||'')}`;
  const timeline=study.timeline||{title:'書卷時序',range:study.passage,note:'把本章放回整卷書的時間與處境。',url:'https://bibleeveryone.com/bible-timeline.php',events:[[study.passage,study.title,'本章']]};
  const map=study.map?`<section class="chapter-section map-reading"><div class="map-reading__head"><h3>01 · 地圖</h3><p class="map-reading__reference">${study.map.reference}</p><h4>${study.map.title}</h4><p>${study.map.guide}</p><ul>${study.map.places.map(place=>`<li>${place}</li>`).join('')}</ul></div><figure class="map-reading__plate"><a href="${study.map.source}" target="_blank" rel="noopener"><img src="${study.map.image}" alt="${study.map.imageTitle}" loading="lazy"></a><figcaption><strong>${study.map.imageTitle}</strong><span>地圖來源：聖光聖經地理 · 《簡明聖經史地圖解》</span></figcaption></figure>${study.map.routes?`<div class="map-reading__route"><header><p class="kicker">Route Notes · 路線圖說</p>${study.map.preface?`<p class="map-reading__preface"><span>圖前事件</span>${study.map.preface}</p>`:''}</header><ol>${study.map.routes.map(route=>`<li><span class="map-reading__number">${route[0]}</span><div><span class="map-reading__verse">${route[1]}</span><p>${route[2]}</p></div></li>`).join('')}</ol></div>`:''}<div class="map-reading__foot"><div class="map-reading__links"><a class="map-reading__primary" href="${study.map.source}" target="_blank" rel="noopener">聖光・本章地名 ↗</a><a href="${osm}" target="_blank" rel="noopener">現代地形參照 ↗</a><a href="https://biblemapper.com/web/" target="_blank" rel="noopener">Bible Mapper ↗</a><a href="https://www.stepbible.org/html/places.html" target="_blank" rel="noopener">STEP 地點 ↗</a></div><small>本圖由聖光聖經地理提供，地名與路線固定在原圖中，縮放時不會失位；點擊地圖可查閱詳細中文圖說。</small></div></section>`:'';
  const chronology=`<section class="chapter-section timeline-reading"><header><p class="kicker">02 · ONE Biblical Chronology</p><h3>${timeline.title}</h3><p class="timeline-reading__range">${timeline.range}</p><p>${timeline.note}</p></header><div class="one-scroll" tabindex="0" aria-label="${timeline.title}時間軸"><div class="one-scroll__rail">${timeline.events.map((event,index)=>`<article${index===timeline.events.length-1?' class="current"':''}><span>${event[0]}</span><i aria-hidden="true">✦</i><strong>${event[1]}</strong><small>${event[2]}</small></article>`).join('')}</div></div><footer><span>ONE 章節時間軸 · 依經文與參考資料編排</span><nav aria-label="時間軸延伸資源"><a href="${timeline.url}" target="_blank" rel="noopener">查閱聖經共享專題 ↗</a><a href="https://bibleeveryone.com/bible-timeline.php" target="_blank" rel="noopener">全本聖經書卷時間軸 ↗</a></nav></footer></section>`;
  const scripture=`<section class="scripture-reading"><header><span>03 · 經文</span><h3>${volume.name}第 ${number} 章</h3><p>Scripture · ${volume.nameEn} ${number}</p></header><div class="scripture-reading__pages"><article><div><strong>中文</strong><span>新標點和合本（神版）</span><a href="${zh}" target="_blank" rel="noopener">在香港聖經公會開啟 ↗</a></div><iframe data-src="${zh}" title="${volume.name}第 ${number} 章，新標點和合本" loading="lazy"></iframe></article><article lang="en"><div><strong>English</strong><span>New International Version</span><a href="${en}" target="_blank" rel="noopener">Open at YouVersion ↗</a></div><iframe data-src="${en}" title="${volume.nameEn} ${number}, New International Version" loading="lazy"></iframe></article></div><small>經文內容由香港聖經公會及 YouVersion 官方頁面提供；若瀏覽器阻止內嵌內容，請使用各頁上方的官方連結。</small></section>`;
  $('#chapter-detail').innerHTML=`<header class="study-intro"><p class="kicker">Chapter ${String(number).padStart(2,'0')} · ${study.passage}</p><h2>${study.title}</h2><p>${study.movement}</p>${displayArt}</header>${map}${chronology}${scripture}<section class="chapter-section"><h3>04 · 本章故事</h3><div><p>${study.story}</p><p>${study.position}</p></div></section><section class="chapter-section"><h3>故事路徑</h3><div class="route-grid">${study.route.map(route=>`<div><span>${route[0]}</span><strong>${route[1]}</strong></div>`).join('')}</div></section><section class="chapter-section"><h3>背景</h3><div class="background-grid">${study.background.map(item=>`<article><h4>${item[0]}</h4><p>${item[1]}</p>${item[2]?`<p class="background-map"><span>地圖</span>${item[2]}</p>`:''}</article>`).join('')}</div></section><section class="chapter-section"><h3>觀察</h3><ul class="scout-list">${study.scout.map(item=>`<li>${item}</li>`).join('')}</ul></section><section class="chapter-section connection-section"><h3>串珠<small>Cross References</small></h3><div class="connection-grid">${study.connections.map((item,index)=>`<article><header><span>${String(index+1).padStart(2,'0')}</span><div><strong>${item[0]}</strong><small>${item[1]}</small></div></header><blockquote>${item[2]}</blockquote></article>`).join('')}</div></section>${comparisonMarkup(study,volume)}<section class="chapter-section"><h3>問題</h3><ol class="question-list">${study.questions.map(item=>`<li>${item}</li>`).join('')}</ol></section><section class="chapter-section"><h3>預備</h3><ul class="prepare-list">${study.prepare.map(item=>`<li>${item}</li>`).join('')}</ul></section>`;
  $('#chapter-detail').insertAdjacentHTML('beforeend',chapterTurnMarkup(number));
  $('#chapter-detail').dataset.chapter=number;$('#chapter-detail').dataset.book=currentBookNumber;
  decorateLeaves(number);
  $$('#chapter-detail [data-turn-chapter]').forEach(button=>button.onclick=()=>turnChapter(Number(button.dataset.turnChapter),button.dataset.turnDirection));
  updateNotice();updateCompleteButton();requestAnimationFrame(()=>hydrateFrames($('#chapter-detail')));
}

function updateNotice(){const volume=studyBook(),study=volume?.chapterStudies?.[String(currentChapter)],owner=profile();if(!volume||!study)return;const lines=study.prepare.map(item=>'・'+item).join('\n');$('#notice-text').textContent=`${owner?.name||'本機查經組'}｜查經\n\n《${volume.name}》第 ${currentChapter} 章\n${study.title}\n日期：${D.meeting.date}\n時間：${D.meeting.time}\nZoom：${D.meeting.zoom}\nCode：${D.meeting.code}\n\n預備：\n${lines}\n\n${location.href}`}
function updateCompleteButton(){const button=$('#complete-chapter'),owner=profile(),progress=bookState(currentBookNumber,owner);if(!owner){button.textContent='請先建立查經組';button.disabled=true}else if(progress.status==='completed'||progress.completedChapter>=currentChapter){button.textContent='本章已完成';button.disabled=true}else{button.textContent='完成本章';button.disabled=false}}
function completeCurrentChapter(){
  const volume=studyBook(),p=profile();
  if(!volume||!p)return;
  const key=String(currentBookNumber),record=p.books[key]||{status:'active',completedChapter:0};
  record.completedChapter=Math.max(record.completedChapter||0,currentChapter);
  if(record.completedChapter>=volume.chapters.length){record.status='completed';p.history=p.history||[];if(!p.history.some(item=>item.book===currentBookNumber))p.history.push({book:currentBookNumber,completedChapter:volume.chapters.length,status:'completed',completed:new Date().toISOString()})}else{record.status='active';p.activeBook=currentBookNumber}
  p.books[key]=record;saveState();renderProfiles();
}

$$('[data-reading-mode]').forEach(button=>button.onclick=()=>applyReadingMode(button.dataset.readingMode));
$('#complete-chapter').onclick=completeCurrentChapter;
$('#print-chapter').onclick=()=>{document.body.classList.add('printing-chapter');window.print()};
window.addEventListener('afterprint',()=>document.body.classList.remove('printing-chapter'));

renderBookShell();
renderProfiles();
applyReadingMode(readingMode,{sync:false});
if(profile()){
  showChapter(currentChapter,studyBook().chapters[currentChapter-1],{sync:Boolean(initialChapter)});
  if(requestedBook||initialChapter){
    const owner=profile();owner.books[String(currentBookNumber)]=owner.books[String(currentBookNumber)]||{status:'active',completedChapter:0};owner.activeBook=currentBookNumber;saveState();
    $('#one-cover').hidden=true;$$('.app-layer').forEach(element=>element.hidden=false);document.body.classList.add('book-open');$('[data-view="view-chapter"]').click();
  }
}else if(requestedBook){
  requestAnimationFrame(()=>selectCoverBook(bookInfo(requestedBook)));
}
