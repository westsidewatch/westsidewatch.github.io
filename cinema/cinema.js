document.documentElement.dataset.surface='holy-light-cinema';
document.documentElement.dataset.core='dore';

const library=document.querySelector('#cinema-library');
const feature=document.querySelector('#cinema-feature');
const dialog=document.querySelector('#cinema-player');
const stage=document.querySelector('#player-stage');
const closeButton=document.querySelector('.player-close');
const momentQuery=document.querySelector('#cinema-moment-query');
const momentSearch=document.querySelector('#cinema-moment-search');
const momentResults=document.querySelector('#cinema-moment-results');

let resources=[];
let moments=[];
let resourceById=new Map();

const JESUS_ID='cinema:video:jesus-film:jesus';
const JESUS_CHAPTERS=['The Beginning','Birth of Jesus','Childhood of Jesus','Baptism of Jesus by John','The Devil Tempts Jesus','Jesus Proclaims Fulfillment of the Scriptures'];

function sourceFor(item){return (item.providerSources||[])[0]||{};}
function seconds(ms){return Math.max(0,Math.floor((ms||0)/1000));}
function timecode(ms){const total=seconds(ms);const h=Math.floor(total/3600);const m=Math.floor((total%3600)/60);const s=total%60;return h?`${h}:${String(m).padStart(2,'0')}:${String(s).padStart(2,'0')}`:`${m}:${String(s).padStart(2,'0')}`;}

function playbackTarget(item,startMs=0){
  return window.HolyLightProviders?.resolve(item,seconds(startMs))||null;
}

function openAt(item,startMs=0){
  if(item.canonicalId===JESUS_ID){
    const inline=document.querySelector('.living-poster__media');
    const shell=document.querySelector('.living-poster');
    if(inline&&shell){mountInlinePlayer(shell,inline,item,startMs);return;}
  }
  const target=playbackTarget(item,startMs);if(!target)return;
  if(target.kind==='embed'){
    stage.replaceChildren();
    window.HolyLightProviders.mount(stage,item,seconds(startMs));
    dialog.showModal();
  }else window.open(target.url,'_blank','noopener,noreferrer');
}

function mountInlinePlayer(shell,target,item,startMs=0){
  const mounted=window.HolyLightProviders?.mount(target,item,seconds(startMs));
  if(!mounted){
    const fallback=playbackTarget(item,startMs);
    if(fallback?.kind==='handoff')window.open(fallback.url,'_blank','noopener,noreferrer');
    return;
  }
  shell.dataset.state='playing';
  shell.classList.add('is-playing');
  const close=shell.querySelector('[data-action="close-player"]');
  close.hidden=false;
  document.documentElement.dataset.cinemaPlayback='inline';
}

function closeInlinePlayer(shell){
  const target=shell.querySelector('.living-poster__media');
  target?.replaceChildren();
  shell.classList.remove('is-playing');
  shell.dataset.state='focus';
  const close=shell.querySelector('[data-action="close-player"]');
  if(close)close.hidden=true;
  delete document.documentElement.dataset.cinemaPlayback;
}

function renderLivingPoster(item){
  if(!feature||!item)return;
  const shell=document.createElement('article');shell.className='living-poster';shell.dataset.state='settle';shell.dataset.canonicalId=item.canonicalId;
  shell.innerHTML=`<div class="living-poster__visual"><div class="living-poster__poster" aria-hidden="true"><span class="living-poster__halo"></span><span class="living-poster__cross"></span><span class="living-poster__grain"></span><span class="living-poster__play-mark">PLAY</span></div><div class="living-poster__media" aria-label="JESUS official embedded player"></div><button class="living-poster__close" type="button" data-action="close-player" hidden aria-label="收起影片">收起影片</button></div><div class="living-poster__copy"><p class="living-poster__kicker">FEATURE FILM · CANONICAL RESOURCE</p><h4>JESUS</h4><p class="living-poster__creator">Jesus Film Project</p><p class="living-poster__line">從降生到復活，按《路加福音》進入耶穌的一生。</p><div class="living-poster__facts"><span>128 MIN</span><span>61 CHAPTERS</span><span>FHD</span><span>OFFICIAL EMBED</span></div><div class="living-poster__actions"><button type="button" data-action="watch">在此播放</button><button type="button" data-action="expand">展開時間</button></div></div><div class="living-poster__timeline" hidden><p>TIME AS CONTENT · 章節預覽</p><ol></ol><small>影片由 Jesus Film Project 官方來源內嵌；本站不複製、不重新託管媒體。</small></div>`;
  const list=shell.querySelector('ol');
  JESUS_CHAPTERS.forEach((label,index)=>{const li=document.createElement('li');li.innerHTML=`<span>${String(index+1).padStart(2,'0')}</span><strong>${label}</strong>`;list.appendChild(li);});
  let focusTimer;
  const focus=()=>{clearTimeout(focusTimer);focusTimer=setTimeout(()=>{if(!shell.classList.contains('is-playing')&&shell.dataset.state!=='expand')shell.dataset.state='focus';},320);};
  const settle=()=>{clearTimeout(focusTimer);if(!shell.classList.contains('is-playing')&&shell.dataset.state!=='expand')shell.dataset.state='settle';};
  shell.addEventListener('pointerenter',focus);shell.addEventListener('pointerleave',settle);shell.addEventListener('focusin',focus);shell.addEventListener('focusout',event=>{if(!shell.contains(event.relatedTarget))settle();});
  shell.querySelector('[data-action="watch"]').addEventListener('click',()=>mountInlinePlayer(shell,shell.querySelector('.living-poster__media'),item,0));
  shell.querySelector('[data-action="close-player"]').addEventListener('click',()=>closeInlinePlayer(shell));
  shell.querySelector('[data-action="expand"]').addEventListener('click',event=>{const timeline=shell.querySelector('.living-poster__timeline');const expanded=!timeline.hidden;timeline.hidden=expanded;if(!shell.classList.contains('is-playing'))shell.dataset.state=expanded?'focus':'expand';event.currentTarget.textContent=expanded?'展開時間':'收起時間';});
  feature.replaceChildren(shell);
}

function renderMomentButton(moment,item){
  const button=document.createElement('button');button.className='moment-card';button.type='button';button.dataset.momentId=moment.momentId;
  const meta=document.createElement('span');meta.className='moment-time';meta.textContent=timecode(moment.startMs);
  const label=document.createElement('strong');label.textContent=moment.label;
  const src=document.createElement('span');src.className='moment-source';src.textContent=item?`${item.creator} · ${item.title}`:moment.canonicalId;
  button.append(meta,label,src);button.addEventListener('click',()=>item&&openAt(item,moment.startMs));return button;
}

function renderCard(item){
  const source=sourceFor(item);const card=document.createElement('article');card.className='resource-card';card.dataset.canonicalId=item.canonicalId;
  const meta=document.createElement('div');meta.className='resource-meta';meta.textContent=`${item.kind||'video'} · ${item.creator||''}`;
  const title=document.createElement('h4');title.textContent=item.title;
  const series=document.createElement('p');series.textContent=item.series||'';
  const topics=document.createElement('div');topics.className='resource-topics';topics.textContent=(item.topics||[]).join(' · ');
  const action=document.createElement('button');action.className='resource-action';action.type='button';action.textContent=source.embed&&source.embedUrl?'在影院播放':'前往官方來源';action.addEventListener('click',()=>openAt(item,0));
  card.append(meta,title,series,topics,action);
  const itemMoments=moments.filter(moment=>moment.canonicalId===item.canonicalId);
  if(itemMoments.length){const timeline=document.createElement('div');timeline.className='resource-timeline';const caption=document.createElement('div');caption.className='timeline-caption';caption.textContent='時間點';timeline.append(caption,...itemMoments.map(moment=>renderMomentButton(moment,item)));card.appendChild(timeline);}
  return card;
}

function searchMoments(){
  const query=(momentQuery.value||'').trim().toLocaleLowerCase();if(!query){momentResults.replaceChildren();return;}
  const hits=moments.filter(moment=>{const item=resourceById.get(moment.canonicalId);const haystack=[moment.label,...(moment.keywords||[]),item?.title,item?.creator,...(item?.topics||[])].filter(Boolean).join(' ').toLocaleLowerCase();return haystack.includes(query);});
  if(!hits.length){const empty=document.createElement('p');empty.className='moment-empty';empty.textContent='暫未找到已建立的時間點。';momentResults.replaceChildren(empty);return;}
  momentResults.replaceChildren(...hits.map(moment=>renderMomentButton(moment,resourceById.get(moment.canonicalId))));
}

async function loadCinema(){
  try{
    const [resourceResponse,momentResponse]=await Promise.all([fetch('data/video-resource.v0.json',{cache:'no-store'}),fetch('data/video-moment.v0.json',{cache:'no-store'})]);
    if(!resourceResponse.ok||!momentResponse.ok)throw new Error('Cinema data unavailable');
    const resourcePayload=await resourceResponse.json();const momentPayload=await momentResponse.json();
    if(resourcePayload.schema!=='holy-light.video-resource.v0'||!Array.isArray(resourcePayload.items))throw new Error('Invalid Cinema resource schema');
    if(momentPayload.schema!=='holy-light.video-moment.v0'||!Array.isArray(momentPayload.items))throw new Error('Invalid Cinema moment schema');
    resources=resourcePayload.items;moments=momentPayload.items;resourceById=new Map(resources.map(item=>[item.canonicalId,item]));
    renderLivingPoster(resourceById.get(JESUS_ID));library.replaceChildren(...resources.map(renderCard));
    document.documentElement.dataset.cinemaResources=String(resources.length);document.documentElement.dataset.cinemaMoments=String(moments.length);document.documentElement.dataset.cinemaUiExperiment='inline-living-cinema-v1';
  }catch(error){library.innerHTML='<p class="resource-card">館藏資料暫時無法載入。</p>';if(feature)feature.innerHTML='<p class="resource-card">實驗資源暫時無法載入。</p>';document.documentElement.dataset.cinemaError='resource-load';}
}

closeButton.addEventListener('click',()=>dialog.close());dialog.addEventListener('close',()=>stage.replaceChildren());dialog.addEventListener('click',event=>{if(event.target===dialog)dialog.close();});momentSearch.addEventListener('click',searchMoments);momentQuery.addEventListener('keydown',event=>{if(event.key==='Enter')searchMoments();});loadCinema();