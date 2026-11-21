'use strict';
/** PARADISO — self-contained, static GitHub-hosted cinema. No external player pages. */
const CATEGORIES = ['全部作品','基督福音劇集','美英劇集','韓日劇集','經典電影','我的收藏'];
const STORAGE_KEYS = { favorites:'paradiso:v1:favorites', custom:'paradiso:v1:custom', progress:'paradiso:v1:progress' };
const $ = (id) => document.getElementById(id);
const getStored = (key, fallback) => {try { const raw=localStorage.getItem(key);return raw ? JSON.parse(raw) : fallback;}catch{return fallback;}};
const saveStored = (key, value) => {try {localStorage.setItem(key,JSON.stringify(value));}catch{/* private mode */}};
const state = {titles:[],activeCategory:'全部作品',query:'',favorites:new Set(getStored(STORAGE_KEYS.favorites, [])),custom:getStored(STORAGE_KEYS.custom, []),progress:getStored(STORAGE_KEYS.progress, {}),current:null,episode:0,source:0,lastFocus:null,hls:null,recovered:false,token:0};
const make = (tag, cls, text) => {const n=document.createElement(tag);if(cls)n.className=cls;if(text!==undefined)n.textContent=text;return n;};
const isSafeMedia = (value) => {try{const url=new URL(value);return url.protocol==='https:' && /\.(m3u8|mp4|webm|ogv|ogg)(?:$|[?#])/i.test(url.pathname+url.search+url.hash);}catch{return false;}};
const isSafeWeb = (value) => {try{return new URL(value).protocol==='https:';}catch{return false;}};
const cleanTitle = (v) => typeof v==='string' ? v.trim().slice(0,100) : '';
const visibleSources = (ep) => Array.isArray(ep.sources)?ep.sources.filter(x=>x&&isSafeMedia(x.url)):[];
function normalizeItem(item){
  if(!item||typeof item!=='object')return null;
  const title=cleanTitle(item.title);
  if(!title||!Array.isArray(item.episodes))return null;
  const episodes=item.episodes.filter(e=>e&&visibleSources(e).length).slice(0,200);
  if(!episodes.length)return null;
  const cat=CATEGORIES.includes(item.category)?item.category:'經典電影';
  return {...item,title,episodes,category:cat};
}
function counts(){
  const hasPlayable=state.titles.filter(x=>x.episodes.length);
  $('total-label').textContent=`${hasPlayable.length} 部作品 · ${hasPlayable.reduce((n,x)=>n+x.episodes.length,0)} 個播放單元`;
  $('favorite-count').textContent=String([...state.favorites].filter(id=>state.titles.some(x=>x.id===id)).length);
}
function setCategory(category){state.activeCategory=category;drawTabs();drawCards();}
function drawTabs(){
  const host=$('category-tabs');host.replaceChildren();
  for(const category of CATEGORIES){const b=make('button','tab',category);b.type='button';b.dataset.active=String(category===state.activeCategory);b.setAttribute('aria-pressed',String(category===state.activeCategory));b.addEventListener('click',()=>setCategory(category));host.append(b);}
}
function filterTitles(){
  const term=state.query.trim().toLocaleLowerCase();
  return state.titles.filter(item=>{
    if(state.activeCategory==='我的收藏'&&!state.favorites.has(item.id))return false;
    if(state.activeCategory!=='全部作品'&&state.activeCategory!=='我的收藏'&&item.category!==state.activeCategory)return false;
    if(!term)return true;
    return [item.title,item.originalTitle,item.year,item.country,(item.genre||[]).join(' ')].join(' ').toLocaleLowerCase().includes(term);
  });
}
function drawCards(){
  const filtered=filterTitles();const grid=$('film-grid');grid.replaceChildren();
  $('results-count').textContent=`${filtered.length} 部作品`;
  $('empty-results').hidden=filtered.length!==0;
  filtered.forEach((item,index)=>{
    const card=make('article','film-card');const poster=make('button',`poster ${['nativity','passion','general'].includes(item.posterStyle)?item.posterStyle:'custom'}`);poster.type='button';poster.setAttribute('aria-label',`播放《${item.title}》`);
    poster.append(make('span','poster-circle'),make('span','poster-top',item.type==='series'?'SERIES / PARADISO':'FULL FEATURE / PARADISO'),make('span','poster-title',item.posterHeadline||item.originalTitle||item.title),make('span','poster-numeral',`Nº ${String(index+1).padStart(3,'0')} · ${item.year||'—'}`),make('span','play-circle','▶'));
    poster.addEventListener('click',()=>openPlayer(item));
    const info=make('div','film-info');info.append(make('div','film-meta',`${item.category}  /  ${item.year||'年份未註明'}  /  ${item.type==='series'?item.episodes.length+'集':item.runtime+' MIN'}`));
    const titleRow=make('div','film-name-row');titleRow.append(make('h3','film-name',item.title));
    const fav=make('button','fav-button',state.favorites.has(item.id)?'♥':'♡');fav.type='button';fav.setAttribute('aria-label',state.favorites.has(item.id)?`取消收藏${item.title}`:`收藏${item.title}`);fav.setAttribute('aria-pressed',String(state.favorites.has(item.id)));
    fav.addEventListener('click',()=>{state.favorites.has(item.id)?state.favorites.delete(item.id):state.favorites.add(item.id);saveStored(STORAGE_KEYS.favorites,[...state.favorites]);counts();drawCards();});titleRow.append(fav);info.append(titleRow);
    info.append(make('p','film-english',item.originalTitle||item.title),make('p','film-synopsis',item.summary||'完整影片播放。'));
    const bottom=make('div','film-bottom');bottom.append(make('span','source-status',item.type==='series'?`${item.episodes.length} 集已收錄`:'完整作品 · 原始來源'));
    const start=make('button','film-cta','站內播放 ↗');start.type='button';start.addEventListener('click',()=>openPlayer(item));bottom.append(start);info.append(bottom);card.append(poster,info);grid.append(card);
  });
}
function status(message,isError=false){$('player-status').textContent=message;$('player-status').dataset.error=String(isError);}
function destroyPlayer(){
  state.token++;
  const video=$('cinema-video');video.pause();video.removeAttribute('src');
  if(state.hls){try{state.hls.destroy();}catch{}state.hls=null;}
  video.load();
}
let scriptPromise;
function ensureHls(){
  if(window.Hls)return Promise.resolve(window.Hls);
  if(scriptPromise)return scriptPromise;
  scriptPromise=new Promise((resolve,reject)=>{const s=document.createElement('script');s.src='https://cdn.jsdelivr.net/npm/hls.js@1.6.13/dist/hls.min.js';s.async=true;s.onload=()=>window.Hls?resolve(window.Hls):reject(new Error('HLS 播放器未能載入'));s.onerror=()=>reject(new Error('網路連接失敗，無法載入 HLS 播放器'));document.head.append(s);}).catch(err=>{scriptPromise=null;throw err;});
  return scriptPromise;
}
function currentEpisode(){return state.current?.episodes[state.episode]||null;}
function episodeData(){const ep=currentEpisode();return ep?visibleSources(ep):[];}
async function connectSource(){
  const item=state.current;const ep=currentEpisode();const sources=episodeData();if(!item||!ep||!sources.length){status('此集沒有可用的影片地址。',true);return;}
  const selected=sources[state.source];if(!selected){status('所有可用來源均已嘗試。請開啟原始典藏來源。',true);return;}
  destroyPlayer();state.recovered=false;const token=state.token;
  const video=$('cinema-video');video.poster='';
  $('source-name').textContent=selected.name||'原始影片來源';
  status(`正在連接 ${selected.name||'影片來源'}…`);
  const url=selected.url;
  try{
    if(/\.m3u8(?:$|[?#])/i.test(url)){
      if(video.canPlayType('application/vnd.apple.mpegurl')){video.src=url;video.load();return;}
      const Hls=await ensureHls();if(token!==state.token)return;
      if(!Hls.isSupported())throw new Error('此瀏覽器不支援 HLS 播放。');
      const hls=new Hls({enableWorker:true,maxBufferLength:30,backBufferLength:30});state.hls=hls;
      hls.on(Hls.Events.ERROR,(_evt,details)=>{if(token!==state.token||!details.fatal)return;
        if(details.type===Hls.ErrorTypes.MEDIA_ERROR&&!state.recovered){state.recovered=true;status('正在恢復影片播放…');hls.recoverMediaError();return;}
        moveToNextSource(details.details||'播放連接中斷');
      });
      hls.attachMedia(video);
      hls.on(Hls.Events.MEDIA_ATTACHED,()=>{if(token===state.token)hls.loadSource(url);});
    }else{video.src=url;video.load();}
  }catch(err){if(token===state.token)moveToNextSource(err.message);}
}
function moveToNextSource(reason){const more=state.source+1<episodeData().length;
  if(more){state.source++;status(`來源無法播放（${reason}），正在切換備選…`);connectSource();}
  else{status(`無法播放：${reason}。請點選「查看典藏來源」。`,true);destroyPlayer();}
}
function selectEpisode(index){
  if(!state.current||index<0||index>=state.current.episodes.length)return;
  state.episode=index;state.source=0;
  const ep=currentEpisode();$('player-subtitle').textContent=`${state.current.originalTitle||''}  ·  ${ep.label||'第'+(index+1)+'集'}`;
  $('previous-episode').disabled=index===0;$('next-episode').disabled=index===state.current.episodes.length-1;
  const list=$('episode-list');list.replaceChildren();state.current.episodes.forEach((entry,i)=>{const b=make('button','episode-button',entry.label||`第 ${String(i+1).padStart(2,'0')} 集`);b.type='button';b.dataset.active=String(i===index);b.addEventListener('click',()=>selectEpisode(i));list.append(b);});
  $('episode-count').textContent=`${state.current.episodes.length} 集`;
  const anchor=$('original-link');if(isSafeWeb(state.current.sourcePage)){anchor.href=state.current.sourcePage;anchor.hidden=false;}else{anchor.hidden=true;}
  connectSource();
}
function openPlayer(item){state.lastFocus=document.activeElement;state.current=item;state.episode=0;state.source=0;
  $('player-title').textContent=item.title;
  $('player-modal').hidden=false;document.body.style.overflow='hidden';
  selectEpisode(0);$('player-close').focus();
}
function closePlayer(){destroyPlayer();state.current=null;$('player-modal').hidden=true;document.body.style.overflow='';state.lastFocus?.focus?.();}
function resumeKey(){return state.current?.id+'#'+state.episode;}
const player=$('cinema-video');
player.addEventListener('loadedmetadata',()=>{status(`已連接影片 · ${Number.isFinite(player.duration)?Math.round(player.duration/60)+' 分鐘':'正在讀取時長'}`);
  const saved=state.progress[resumeKey()];if(Number.isFinite(saved)&&saved>15&&Number.isFinite(player.duration)&&saved<player.duration-20){try{player.currentTime=saved;}catch{}}
});
player.addEventListener('playing',()=>status('正在播放 · PARADISO 站內播放器'));
player.addEventListener('waiting',()=>status('正在緩衝影片…'));
player.addEventListener('error',()=>{if(state.current&&player.getAttribute('src'))moveToNextSource('媒體連接或格式失敗');});
player.addEventListener('ended',()=>{status('放映結束。');if(state.current&&state.episode+1<state.current.episodes.length)status('本集播放完畢 · 可以播放下一集。');});
let lastProgress=0;player.addEventListener('timeupdate',()=>{if(!state.current||!Number.isFinite(player.currentTime)||Date.now()-lastProgress<4000)return;lastProgress=Date.now();state.progress[resumeKey()]=Math.floor(player.currentTime);saveStored(STORAGE_KEYS.progress,state.progress);});
$('player-close').addEventListener('click',closePlayer);
document.querySelector('[data-close-player]').addEventListener('click',closePlayer);
$('previous-episode').addEventListener('click',()=>selectEpisode(state.episode-1));
$('next-episode').addEventListener('click',()=>selectEpisode(state.episode+1));
$('retry-source').addEventListener('click',()=>{state.source=0;connectSource();});
function closeManage(){ $('manage-modal').hidden=true;document.body.style.overflow='';state.lastFocus?.focus?.(); }
$('manage-open').addEventListener('click',()=>{state.lastFocus=document.activeElement;$('manage-modal').hidden=false;document.body.style.overflow='hidden';$('manage-close').focus();});
$('manage-close').addEventListener('click',closeManage);
document.querySelector('[data-close-manage]').addEventListener('click',closeManage);
document.addEventListener('keydown',e=>{if(e.key==='Escape'){if(!$('player-modal').hidden)closePlayer();else if(!$('manage-modal').hidden)closeManage();}});
$('import-form').addEventListener('submit',e=>{
  e.preventDefault();const f=new FormData(e.currentTarget),title=cleanTitle(f.get('title'));const raw=String(f.get('episodes')||'').split(/\r?\n/).map(x=>x.trim()).filter(Boolean);const error=$('import-error');error.textContent='';
  if(raw.length>200){error.textContent='單次最多收錄 200 集。';return;}
  const episodes=[];
  for(let i=0;i<raw.length;i++){const bar=raw[i].indexOf('|');if(bar<1){error.textContent=`第 ${i+1} 行需要用「|」分隔集數與地址。`;return;}
    const label=raw[i].slice(0,bar).trim().slice(0,60),url=raw[i].slice(bar+1).trim();
    if(!isSafeMedia(url)){error.textContent=`第 ${i+1} 行不是 HTTPS m3u8／mp4／webm／ogv 地址。`;return;}
    episodes.push({number:i+1,label,sources:[{name:'我的個人來源',format:url.split('.').pop().split('?')[0],url}]});
  }
  if(!title||!episodes.length){error.textContent='請填寫影片名稱及至少一集。';return;}
  const year=Number(f.get('year'))||null;
  const entry={id:'local-'+Date.now().toString(36)+'-'+Math.random().toString(36).slice(2,7),title,originalTitle:title,category:String(f.get('category')),year,type:episodes.length>1?'series':'film',runtime:0,posterStyle:'custom',summary:'個人保存的播放來源，只存在此瀏覽器。',episodes};
  state.custom.unshift(entry);saveStored(STORAGE_KEYS.custom,state.custom);state.titles.unshift(entry);counts();state.query='';$('search').value='';setCategory('全部作品');e.currentTarget.reset();closeManage();document.querySelector('#collection').scrollIntoView({behavior:'smooth'});
});
$('search').addEventListener('input',e=>{state.query=e.target.value;drawCards();});
$('favorites-nav').addEventListener('click',()=>{setCategory('我的收藏');$('collection').scrollIntoView({behavior:'smooth'});});
$('clear-filter').addEventListener('click',()=>{$('search').value='';state.query='';setCategory('全部作品');});
$('hero-watch').addEventListener('click',()=>{const first=state.titles.find(x=>x.category==='基督福音劇集')||state.titles[0];if(first)openPlayer(first);});
async function init(){drawTabs();try{const response=await fetch('./catalog.json',{cache:'no-store'});if(!response.ok)throw new Error(`HTTP ${response.status}`);
  const catalog=await response.json();const publicItems=(catalog.titles||[]).map(normalizeItem).filter(Boolean);
  const customItems=(Array.isArray(state.custom)?state.custom:[]).map(normalizeItem).filter(Boolean);
  state.titles=[...customItems,...publicItems];counts();drawCards();
  if(!state.titles.length){$('empty-results').hidden=false;$('total-label').textContent='片庫為空';}
}catch(err){$('total-label').textContent='片庫連接失敗';$('results-count').textContent='資料無法載入';$('empty-results').hidden=false;$('empty-results').querySelector('p').textContent='請重新整理頁面。'+err.message;}}
init();
