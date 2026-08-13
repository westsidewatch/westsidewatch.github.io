const D=window.ONE_DATA,$=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)];
document.documentElement.classList.add('one-bound');
function hydrateFrames(root=document){root.querySelectorAll('iframe[data-src]').forEach(frame=>{if(frame.offsetWidth>0&&!frame.hasAttribute('src'))frame.setAttribute('src',frame.dataset.src)})}
const STORAGE_KEY='one-progress-v1';
const clone=value=>JSON.parse(JSON.stringify(value));
const defaults=()=>({profiles:clone(D.progress.profiles),activeProfile:D.progress.defaultProfile,archives:[]});
function loadState(){try{const saved=JSON.parse(localStorage.getItem(STORAGE_KEY));if(saved?.profiles?.length)return saved}catch(error){}return defaults()}
let state=loadState();
const MODE_KEY='one-reading-mode-v1';
const requestedChapterValue=Number(new URLSearchParams(location.search).get('chapter'));
const requestedChapter=Number.isInteger(requestedChapterValue)&&requestedChapterValue>=1&&requestedChapterValue<=28?requestedChapterValue:null;
let currentChapter=requestedChapter||1;
function loadReadingMode(){
  const queryMode=new URLSearchParams(location.search).get('mode');
  if(queryMode==='reading'||queryMode==='study')return queryMode;
  try{const saved=localStorage.getItem(MODE_KEY);if(saved==='reading'||saved==='study')return saved}catch(error){}
  return 'study';
}
let readingMode=loadReadingMode();
function saveState(){localStorage.setItem(STORAGE_KEY,JSON.stringify(state))}
function profile(){return state.profiles.find(item=>item.id===state.activeProfile)||state.profiles[0]}
function bookState(number){return profile().books[String(number)]||{status:'dormant',completedChapter:0}}
function nextChapterFor(number,total){const done=bookState(number).completedChapter||0;return Math.min(done+1,total)}

function renderCover(){const list=$('#cover-books');list.innerHTML='';D.books.forEach(book=>{const progress=bookState(book[0]),lit=progress.status!=='dormant';const item=document.createElement(lit?'button':'div');item.className=`cover-book ${progress.status}`;item.innerHTML=`<span>${String(book[0]).padStart(2,'0')}</span>${lit?`<strong>${book[1]}<i>${book[2]}</i></strong>`:''}`;if(lit){item.type='button';item.onclick=()=>openBook(book)}list.append(item)})}
function openBook(book){const selected=[...$$('.cover-book')].find(item=>item.textContent.includes(String(book[0]).padStart(2,'0')));selected?.classList.add('entering');$('#one-cover').classList.add('opening-book');setTimeout(()=>{$('#one-cover').hidden=true;$('#one-cover').classList.remove('opening-book');selected?.classList.remove('entering');$$('.app-layer').forEach(el=>el.hidden=false);document.body.classList.add('book-open');if(book[0]===40){$('[data-view="view-chapter"]').click();showChapter(nextChapterFor(40,28),D.matthew.chapters[nextChapterFor(40,28)-1])}else{$('[data-view="view-books"]').click();showBook(book)}window.scrollTo({top:0,behavior:'auto'})},motionDelay())}
function motionDelay(){return matchMedia('(prefers-reduced-motion: reduce)').matches?0:520}
$('#return-cover').onclick=()=>{document.body.classList.add('closing-book');setTimeout(()=>{$$('.app-layer').forEach(el=>el.hidden=true);$('#one-cover').hidden=false;document.body.classList.remove('book-open','closing-book');const url=new URL(location.href);['book','chapter','mode'].forEach(key=>url.searchParams.delete(key));history.replaceState(null,'',url);document.title='ONE · 一卷入夜，合卷天明';renderCover();window.scrollTo({top:0,behavior:'auto'})},motionDelay())};
const reading=$('#light-reading'),openLight=$('#open-scripture'),closeLight=$('#close-scripture');
function showLight(){reading.hidden=false;requestAnimationFrame(()=>reading.classList.add('visible'));document.body.classList.add('reading-light');closeLight.focus()}
function hideLight(){reading.classList.remove('visible');document.body.classList.remove('reading-light');setTimeout(()=>{reading.hidden=true;openLight.focus()},motionDelay())}
openLight.onclick=showLight;closeLight.onclick=hideLight;reading.onclick=event=>{if(event.target===reading)hideLight()};document.addEventListener('keydown',event=>{if(event.key==='Escape'&&!reading.hidden)hideLight()});

const bookGrid=$('#book-grid'),chapterGrid=$('#chapter-grid'),detail=$('#book-detail');
function renderBooks(){bookGrid.innerHTML='';D.books.forEach(book=>{const progress=bookState(book[0]),visible=progress.status!=='dormant';const el=document.createElement(visible?'button':'div');el.className=`book ${progress.status}`;el.setAttribute('aria-label',visible?book[1]:`第 ${book[0]} 卷`);el.innerHTML=`<span>${String(book[0]).padStart(2,'0')}</span><strong>${visible?book[1]:''}</strong><small>${visible?book[2]:''}</small>`;if(visible){el.type='button';el.onclick=()=>showBook(book)}bookGrid.append(el)})}
function showBook(book){const progress=bookState(book[0]);detail.className='book-detail open';detail.innerHTML=`<p class="kicker">Book ${String(book[0]).padStart(2,'0')}</p><h3>${book[1]}<small>${book[2]}</small></h3><p>${progress.status==='completed'?`全 ${book[3]} 章 · 已完成`:`進行中 · 已完成 ${progress.completedChapter} / ${book[3]} 章 · 下一章 ${nextChapterFor(book[0],book[3])}`}</p>`;detail.scrollIntoView({behavior:'smooth',block:'nearest'})}

D.matthew.movements.forEach(m=>$('#movement-grid').insertAdjacentHTML('beforeend',`<div class="movement"><span>${m[0]} · ${m[1]}章</span><strong>${m[2]}</strong></div>`));
function renderChapters(){chapterGrid.innerHTML='';const matthew=bookState(40),next=nextChapterFor(40,28);D.matthew.chapters.forEach((name,index)=>{const n=index+1,status=n<=matthew.completedChapter?'completed':n===next&&matthew.status==='active'?'current':'upcoming',ready=Boolean(D.matthew.chapterStudies[String(n)]);const el=document.createElement(ready?'button':'div');el.className=`chapter ${status}${ready?' available':''}`;el.dataset.chapter=n;el.innerHTML=`<span>${String(n).padStart(2,'0')}</span><strong>${ready?name:''}</strong>`;if(ready){el.type='button';el.onclick=()=>{showChapter(n,name);$('#chapter-detail').scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth',block:'start'})}}chapterGrid.append(el)});markCurrentChapter(currentChapter)}

const resourceCard=r=>`<a class="resource-card-one${r.core?' resource-card-one--core':''}" href="${r.url}" target="_blank" rel="noopener noreferrer" aria-label="開啟 ${r.name} 官方網站"><p class="resource-card-one__folio"><span>${r.id}</span><small>DAWN LIBRARY</small></p><div class="resource-card-one__identity"><span>${r.category}</span><h3>${r.name}</h3><em>${r.nameEn}</em></div><div class="resource-card-one__details"><p>${r.description}</p><dl><div><dt>Spectrum</dt><dd>${r.spectrum}</dd></div><div><dt>Access</dt><dd>${r.access}</dd></div></dl><strong>Open resource <i aria-hidden="true">↗</i></strong></div></a>`;
const resourceGroups=[
  {label:'核心查經平台',en:'Core Bible Study Platforms',items:D.resources.filter(r=>r.core)},
  {label:'逐章伴讀資源',en:'Chapter Companions',items:D.resources.filter(r=>!r.core)}
];
$('#resource-grid').innerHTML=resourceGroups.map(group=>`<section class="resource-group"><header class="resource-group-title"><p>${group.en}</p><h3>${group.label}</h3></header><div class="resource-grid">${group.items.map(resourceCard).join('')}</div></section>`).join('');
$$('.view-tabs button').forEach(button=>button.onclick=()=>{$$('.view-tabs button').forEach(x=>x.setAttribute('aria-selected','false'));button.setAttribute('aria-selected','true');$$('.view').forEach(x=>x.classList.remove('active'));const view=$('#'+button.dataset.view);view.classList.add('active');requestAnimationFrame(()=>hydrateFrames(view))});

function renderProfiles(){const select=$('#profile-select');select.innerHTML='';state.profiles.forEach(item=>{const option=document.createElement('option');option.value=item.id;option.textContent=item.name;option.selected=item.id===state.activeProfile;select.append(option)});const p=profile(),active=p.activeBook?D.books.find(book=>book[0]===p.activeBook):null,completed=Object.values(p.books).filter(item=>item.status==='completed').length;if(active){const progress=p.books[String(active[0])]||{};$('#profile-progress').textContent=`${active[1]} ${progress.completedChapter||0} / ${active[3]}`;$('#profile-next').textContent=`下一次：第 ${nextChapterFor(active[0],active[3])} 章`}else{$('#profile-progress').textContent='尚未開卷';$('#profile-next').textContent='第一卷'}$('#profile-history-count').textContent=`${completed} 卷`;renderCover();renderBooks();renderChapters()}
$('#profile-select').onchange=event=>{state.activeProfile=event.target.value;saveState();renderProfiles()};
$('#new-profile').onclick=()=>{$('#profile-form').hidden=false;$('#restart-confirm').hidden=true;$('#profile-name').focus()};
$('#cancel-profile').onclick=()=>{$('#profile-form').hidden=true};
$('#profile-form').onsubmit=event=>{event.preventDefault();const name=$('#profile-name').value.trim();if(!name)return;const id=`group-${Date.now()}`;state.profiles.push({id,name,created:new Date().toISOString(),activeBook:null,books:{},history:[]});state.activeProfile=id;saveState();event.target.reset();event.target.hidden=true;renderProfiles()};
$('#restart-profile').onclick=()=>{$('#restart-confirm').hidden=false;$('#profile-form').hidden=true};
$('#cancel-restart').onclick=()=>{$('#restart-confirm').hidden=true};
$('#confirm-restart').onclick=()=>{const old=clone(profile()),stamp=new Date().toISOString();state.archives=state.archives||[];state.archives.push({...old,archived:stamp});const id=`round-${Date.now()}`;state.profiles.push({id,name:`${old.name} · 新一輪`,created:stamp,activeBook:null,books:{},history:[]});state.activeProfile=id;saveState();$('#restart-confirm').hidden=true;renderProfiles()};

const notice=`西區的夜晚｜查經\n\n《馬太福音》第 1 章\n家譜與耶穌降生\n日期：${D.meeting.date}\n時間：${D.meeting.time}\nZoom：${D.meeting.zoom}\nCode：${D.meeting.code}\n\n預備：\n${D.matthew.chapterStudies["1"].prepare.map(x=>'・'+x).join('\n')}\n\n${location.href}`;$('#notice-text').textContent=notice;
async function copy(text,button){try{await navigator.clipboard.writeText(text);const old=button.textContent;button.textContent='已複製';setTimeout(()=>button.textContent=old,1600)}catch(error){button.textContent='請手動複製'}}
$('#copy-notice').onclick=event=>copy(notice,event.currentTarget);$('#share-one').onclick=event=>copy(location.href,event.currentTarget);$$('[data-open-chapter]').forEach(button=>button.onclick=()=>{const tab=$('[data-view="view-chapter"]');tab.click();$('#chapter-detail').scrollIntoView({behavior:'smooth',block:'start'})});
function syncChapterLocation(){
  const url=new URL(location.href);
  url.searchParams.set('book','40');
  url.searchParams.set('chapter',currentChapter);
  url.searchParams.set('mode',readingMode);
  history.replaceState(null,'',url);
}
function applyReadingMode(mode,{sync=true}={}){
  readingMode=mode==='reading'?'reading':'study';
  document.body.classList.toggle('mode-reading',readingMode==='reading');
  document.body.classList.toggle('mode-study',readingMode==='study');
  $('#reading-mode-label').textContent=readingMode==='reading'?'閱讀模式':'查經模式';
  $$('[data-reading-mode]').forEach(button=>button.setAttribute('aria-pressed',String(button.dataset.readingMode===readingMode)));
  try{localStorage.setItem(MODE_KEY,readingMode)}catch(error){}
  if(sync)syncChapterLocation();
  requestAnimationFrame(()=>hydrateFrames($('#view-chapter')));
}
function chapterTurnMarkup(n){
  const previous=n>1?`<button type="button" data-turn-chapter="${n-1}" data-turn-direction="previous"><span>Previous · 上一章</span><strong>${String(n-1).padStart(2,'0')} · ${D.matthew.chapters[n-2]}</strong></button>`:`<span class="chapter-turn__boundary"><i>Previous · 上一章</i><strong>卷首</strong></span>`;
  const next=n<28?`<button type="button" data-turn-chapter="${n+1}" data-turn-direction="next"><span>Next · 下一章</span><strong>${String(n+1).padStart(2,'0')} · ${D.matthew.chapters[n]}</strong></button>`:`<span class="chapter-turn__boundary"><i>Next · 下一章</i><strong>卷終</strong></span>`;
  return `<nav class="chapter-turn" aria-label="馬太福音章節翻頁">${previous}<p><span>Matthew</span><b>${String(n).padStart(2,'0')}</b></p>${next}</nav>`;
}
function decorateLeaves(n){
  const chapterDetail=$('#chapter-detail');
  [...chapterDetail.children].filter(leaf=>leaf.matches('.study-intro,.chapter-section,.scripture-reading')).forEach(leaf=>{
    const head=document.createElement('p');
    head.className='running-head';
    head.setAttribute('aria-hidden','true');
    head.innerHTML=`<span>WESTSIDE WATCH · ONE</span><b>MATTHEW · ${String(n).padStart(2,'0')}</b>`;
    leaf.prepend(head);
  });
}
function markCurrentChapter(n){
  $$('#chapter-grid [data-chapter]').forEach(button=>{
    const active=Number(button.dataset.chapter)===n;
    button.classList.toggle('reading',active);
    if(active)button.setAttribute('aria-current','page');else button.removeAttribute('aria-current');
  });
}
function turnChapter(target,direction){
  const chapterDetail=$('#chapter-detail');
  if(chapterDetail.classList.contains('page-turning'))return;
  const delay=matchMedia('(prefers-reduced-motion: reduce)').matches?0:220;
  chapterDetail.classList.add('page-turning',`page-turning--${direction}`);
  setTimeout(()=>{
    showChapter(target,D.matthew.chapters[target-1]);
    chapterDetail.classList.remove('page-turning',`page-turning--${direction}`);
    chapterDetail.classList.add('page-arriving',`page-arriving--${direction}`);
    chapterDetail.scrollIntoView({behavior:'auto',block:'start'});
    setTimeout(()=>chapterDetail.classList.remove('page-arriving',`page-arriving--${direction}`),delay+80);
  },delay);
}
function showChapter(n,name,{sync=true}={}){
  const f=D.matthew.chapterStudies[String(n)];
  if(!f){$('#chapter-detail').innerHTML=`<section class="chapter-section"><h3>第 ${n} 章</h3><div><p>${name}</p></div></section>`;return}
  currentChapter=n;
  if(sync)syncChapterLocation();
  markCurrentChapter(n);
  const now=$('.now');
  document.documentElement.style.setProperty('--one-chapter-number',`"${String(n).padStart(2,'0')}"`);
  const chapterTab=$('[data-view="view-chapter"]');
  const chapterStatus=now.querySelector('.status');
  chapterTab.textContent=`馬太福音 ${n}`;
  document.title=`馬太福音 ${n} · ${f.title} · ONE`;
  chapterStatus.querySelector('span').textContent=n===1?'起點':'本章';
  chapterStatus.querySelector('strong').textContent=`第 ${n} 章`;
  chapterStatus.querySelector('p').textContent=f.title;
  $('.book-frontispiece .head>p:last-child').textContent=`第 ${n} 章 · ${f.title}`;
  if(f.illustration){
    const chapterEngraving=`url("${f.illustration.src}")`;
    now.style.setProperty('--chapter-engraving',chapterEngraving);
    document.documentElement.style.setProperty('--one-chapter-engraving',chapterEngraving);
    const credit=$('#chapter-art-credit');
    credit.href=f.illustration.source;
    credit.textContent=`Gustave Doré · ${f.illustration.title}`;
  }
  const zh=`https://rcuv.hkbs.org.hk/CUNP1/MAT/${n}/`;
  const en=`https://www.bible.com/bible/111/MAT.${n}.NIV`;
  const osm=`https://www.openstreetmap.org/export/embed.html?bbox=${encodeURIComponent(f.map?.bbox||'')}&layer=mapnik&marker=${encodeURIComponent(f.map?.marker||'')}`;
  const timelineByChapter={
    1:{title:'應許進入歷史',range:'馬太福音 1:1–25',note:'從亞伯拉罕、大衛和被擄的世代，抵達以馬內利的降生。',url:'https://bibleeveryone.com/jesus-childhood.php#jrow9',events:[['約 2000 BC','亞伯拉罕蒙召','太 1:1–2'],['約 1000 BC','大衛王朝','太 1:6'],['586 BC','猶大被擄','太 1:11–12'],['5–4 BC','耶穌降生','太 1:18–25']]},
    2:{title:'君王與流亡',range:'馬太福音 2:1–23',note:'從伯利恆的星光，經埃及的逃難，返回拿撒勒。',url:'https://bibleeveryone.com/jesus-trip1.php',events:[['5–4 BC','博士抵達耶路撒冷','太 2:1–8'],['5–4 BC','在伯利恆敬拜','太 2:9–12'],['約 4 BC','逃往埃及','太 2:13–15'],['約 4–1 BC','回到拿撒勒','太 2:19–23']]},
    3:{title:'曠野中的起點',range:'馬太福音 3:1–17',note:'約翰在曠野預備道路；耶穌在約旦河受洗，公開事奉開始。',url:'https://bibleeveryone.com/jesus-trip2.php',events:[['約 AD 26','約翰在曠野傳道','太 3:1–6'],['約 AD 26','悔改的呼召','太 3:7–12'],['約 AD 26/27','耶穌來到約旦河','太 3:13–15'],['約 AD 26/27','天開了','太 3:16–17']]}
  };
  const timelineView=f.timeline||timelineByChapter[n]||{title:'四福音事奉時序',range:f.passage,note:'在四福音共同的耶穌生平中定位本章事件。',url:'https://bibleeveryone.com/jesus-trip2.php',events:[[f.passage,f.title,'本章'],['四福音時期','耶穌的事奉','約 5 BC–AD 30']]};
  const map=f.map?`<section class="chapter-section map-reading">
    <div class="map-reading__head"><h3>01 · 地圖</h3><p class="map-reading__reference">${f.map.reference}</p><h4>${f.map.title}</h4><p>${f.map.guide}</p><ul>${f.map.places.map(x=>`<li>${x}</li>`).join('')}</ul></div>
    <figure class="map-reading__plate"><a href="${f.map.source}" target="_blank" rel="noopener"><img src="${f.map.image}" alt="${f.map.imageTitle}" loading="lazy"></a><figcaption><strong>${f.map.imageTitle}</strong><span>地圖來源：聖光聖經地理 · 《簡明聖經史地圖解》</span></figcaption></figure>
    ${f.map.routes?`<div class="map-reading__route"><header><p class="kicker">Route Notes · 路線圖說</p>${f.map.preface?`<p class="map-reading__preface"><span>圖前事件</span>${f.map.preface}</p>`:''}</header><ol>${f.map.routes.map(x=>`<li><span class="map-reading__number">${x[0]}</span><div><span class="map-reading__verse">${x[1]}</span><p>${x[2]}</p></div></li>`).join('')}</ol></div>`:''}
    <div class="map-reading__foot"><div class="map-reading__links"><a class="map-reading__primary" href="${f.map.source}" target="_blank" rel="noopener">聖光・本章地名 ↗</a><a href="${osm}" target="_blank" rel="noopener">現代地形參照 ↗</a><a href="https://biblemapper.com/web/" target="_blank" rel="noopener">Bible Mapper ↗</a><a href="https://www.stepbible.org/html/places.html" target="_blank" rel="noopener">STEP 地點 ↗</a></div><small>本圖由聖光聖經地理提供，地名與路線固定在原圖中，縮放時不會失位。請尊重原著及網站版權；點擊地圖可前往聖光查閱本章地名資料。</small></div>
  </section>`:'';
  const timeline=`<section class="chapter-section timeline-reading"><header><p class="kicker">02 · ONE Biblical Chronology</p><h3>${timelineView.title}</h3><p class="timeline-reading__range">${timelineView.range}</p><p>${timelineView.note}</p></header><div class="one-scroll" tabindex="0" aria-label="${timelineView.title}時間軸"><div class="one-scroll__rail">${timelineView.events.map((event,index)=>`<article${index===timelineView.events.length-1?' class="current"':''}><span>${event[0]}</span><i aria-hidden="true">✦</i><strong>${event[1]}</strong><small>${event[2]}</small></article>`).join('')}</div></div><footer><span>ONE 章節時間軸 · 依經文與參考資料編排</span><nav aria-label="時間軸延伸資源"><a href="${timelineView.url}" target="_blank" rel="noopener">查閱聖經共享專題 ↗</a><a href="https://bibleeveryone.com/bible-timeline.php" target="_blank" rel="noopener">全本聖經書卷時間軸 ↗</a></nav></footer></section>`;
  const scripture=`<section class="scripture-reading"><header><span>03 · 經文</span><h3>馬太福音第 ${n} 章</h3><p>Scripture · Matthew ${n}</p></header><div class="scripture-reading__pages"><article><div><strong>中文</strong><span>新標點和合本（神版）</span><a href="${zh}" target="_blank" rel="noopener">在香港聖經公會開啟 ↗</a></div><iframe data-src="${zh}" title="馬太福音第 ${n} 章，新標點和合本" loading="lazy"></iframe></article><article lang="en"><div><strong>English</strong><span>New International Version</span><a href="${en}" target="_blank" rel="noopener">Open at YouVersion ↗</a></div><iframe data-src="${en}" title="Matthew ${n}, New International Version" loading="lazy"></iframe></article></div><small>經文內容由香港聖經公會及 YouVersion 官方頁面提供；若瀏覽器阻止內嵌內容，請使用各頁上方的官方連結。</small></section>`;
  $('#chapter-detail').innerHTML=`<header class="study-intro"><p class="kicker">Chapter ${String(n).padStart(2,'0')} · ${f.passage}</p><h2>${f.title}</h2><p>${f.movement}</p></header>${map}${timeline}${scripture}<section class="chapter-section"><h3>04 · 本章故事</h3><div><p>${f.story}</p><p>${f.position}</p></div></section><section class="chapter-section"><h3>故事路徑</h3><div class="route-grid">${f.route.map(x=>`<div><span>${x[0]}</span><strong>${x[1]}</strong></div>`).join('')}</div></section><section class="chapter-section"><h3>背景</h3><div class="background-grid">${f.background.map(x=>`<article><h4>${x[0]}</h4><p>${x[1]}</p>${x[2]?`<p class="background-map"><span>地圖</span>${x[2]}</p>`:''}</article>`).join('')}</div></section><section class="chapter-section"><h3>觀察</h3><ul class="scout-list">${f.scout.map(x=>`<li>${x}</li>`).join('')}</ul></section><section class="chapter-section connection-section"><h3>串珠<small>Cross References</small></h3><div class="connection-grid">${f.connections.map((x,index)=>`<article><header><span>${String(index+1).padStart(2,'0')}</span><div><strong>${x[0]}</strong><small>${x[1]}</small></div></header><blockquote>${x[2]}</blockquote></article>`).join('')}</div></section><section class="chapter-section"><h3>四福音合參</h3><div><table class="harmony"><thead><tr><th>事件</th><th>馬太</th><th>馬可</th><th>路加</th><th>約翰</th></tr></thead><tbody>${f.harmony.map(x=>`<tr>${x.map(y=>`<td>${y}</td>`).join('')}</tr>`).join('')}</tbody></table></div></section><section class="chapter-section"><h3>問題</h3><ol class="question-list">${f.questions.map(x=>`<li>${x}</li>`).join('')}</ol></section><section class="chapter-section"><h3>預備</h3><ul class="prepare-list">${f.prepare.map(x=>`<li>${x}</li>`).join('')}</ul></section>`;
  $('#chapter-detail').insertAdjacentHTML('beforeend',chapterTurnMarkup(n));
  $('#chapter-detail').dataset.chapter=n;
  decorateLeaves(n);
  $$('#chapter-detail [data-turn-chapter]').forEach(button=>button.onclick=()=>turnChapter(Number(button.dataset.turnChapter),button.dataset.turnDirection));
  requestAnimationFrame(()=>hydrateFrames($('#chapter-detail')));
}

$$('[data-reading-mode]').forEach(button=>button.onclick=()=>applyReadingMode(button.dataset.readingMode));
$('#print-chapter').onclick=()=>{document.body.classList.add('printing-chapter');window.print()};
window.addEventListener('afterprint',()=>document.body.classList.remove('printing-chapter'));
renderProfiles();
applyReadingMode(readingMode,{sync:false});
showChapter(currentChapter,D.matthew.chapters[currentChapter-1],{sync:Boolean(requestedChapter)});
if(requestedChapter){
  $('#one-cover').hidden=true;
  $$('.app-layer').forEach(el=>el.hidden=false);
  document.body.classList.add('book-open');
  $('[data-view="view-chapter"]').click();
}
