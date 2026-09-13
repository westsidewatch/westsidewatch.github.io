document.documentElement.dataset.surface='holy-light-cinema';
document.documentElement.dataset.core='dore';

const library=document.querySelector('#cinema-library');
const dialog=document.querySelector('#cinema-player');
const stage=document.querySelector('#player-stage');
const closeButton=document.querySelector('.player-close');
const momentQuery=document.querySelector('#cinema-moment-query');
const momentSearch=document.querySelector('#cinema-moment-search');
const momentResults=document.querySelector('#cinema-moment-results');

let resources=[];
let moments=[];
let resourceById=new Map();

function sourceFor(item){return (item.providerSources||[])[0]||{};}
function seconds(ms){return Math.max(0,Math.floor((ms||0)/1000));}
function timecode(ms){const total=seconds(ms);const h=Math.floor(total/3600);const m=Math.floor((total%3600)/60);const s=total%60;return h?`${h}:${String(m).padStart(2,'0')}:${String(s).padStart(2,'0')}`:`${m}:${String(s).padStart(2,'0')}`;}

function playbackTarget(item,startMs=0){
  const source=sourceFor(item);
  const start=seconds(startMs);
  if(source.embed&&source.embedUrl){
    const url=new URL(source.embedUrl,window.location.href);
    if(start>0) url.searchParams.set('start',String(start));
    url.searchParams.set('autoplay','1');
    return {kind:'embed',url:url.toString()};
  }
  if(source.url){
    const url=new URL(source.url,window.location.href);
    if(start>0&&source.provider==='youtube') url.searchParams.set('t',`${start}s`);
    return {kind:'handoff',url:url.toString()};
  }
  return null;
}

function openAt(item,startMs=0){
  const target=playbackTarget(item,startMs);
  if(!target) return;
  if(target.kind==='embed'){
    stage.innerHTML='';
    const frame=document.createElement('iframe');
    frame.src=target.url;
    frame.title=item.title;
    frame.allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';
    frame.allowFullscreen=true;
    stage.appendChild(frame);
    dialog.showModal();
  }else{
    window.open(target.url,'_blank','noopener,noreferrer');
  }
}

function renderMomentButton(moment,item){
  const button=document.createElement('button');
  button.className='moment-card';
  button.type='button';
  button.dataset.momentId=moment.momentId;
  const meta=document.createElement('span');
  meta.className='moment-time';
  meta.textContent=timecode(moment.startMs);
  const label=document.createElement('strong');
  label.textContent=moment.label;
  const source=document.createElement('span');
  source.className='moment-source';
  source.textContent=item?`${item.creator} · ${item.title}`:moment.canonicalId;
  button.append(meta,label,source);
  button.addEventListener('click',()=>item&&openAt(item,moment.startMs));
  return button;
}

function renderCard(item){
  const source=sourceFor(item);
  const card=document.createElement('article');
  card.className='resource-card';
  card.dataset.canonicalId=item.canonicalId;
  const meta=document.createElement('div');
  meta.className='resource-meta';
  meta.textContent=`${item.kind||'video'} · ${item.creator||''}`;
  const title=document.createElement('h4');
  title.textContent=item.title;
  const series=document.createElement('p');
  series.textContent=item.series||'';
  const topics=document.createElement('div');
  topics.className='resource-topics';
  topics.textContent=(item.topics||[]).join(' · ');
  const action=document.createElement('button');
  action.className='resource-action';
  action.type='button';
  action.textContent=source.embed&&source.embedUrl?'在影院播放':'前往官方來源';
  action.addEventListener('click',()=>openAt(item,0));
  card.append(meta,title,series,topics,action);
  const itemMoments=moments.filter(moment=>moment.canonicalId===item.canonicalId);
  if(itemMoments.length){
    const timeline=document.createElement('div');
    timeline.className='resource-timeline';
    const caption=document.createElement('div');
    caption.className='timeline-caption';
    caption.textContent='時間點';
    timeline.append(caption,...itemMoments.map(moment=>renderMomentButton(moment,item)));
    card.appendChild(timeline);
  }
  return card;
}

function searchMoments(){
  const query=(momentQuery.value||'').trim().toLocaleLowerCase();
  if(!query){momentResults.replaceChildren();return;}
  const hits=moments.filter(moment=>{
    const item=resourceById.get(moment.canonicalId);
    const haystack=[moment.label,...(moment.keywords||[]),item?.title,item?.creator,...(item?.topics||[])].filter(Boolean).join(' ').toLocaleLowerCase();
    return haystack.includes(query);
  });
  if(!hits.length){
    const empty=document.createElement('p');
    empty.className='moment-empty';
    empty.textContent='暫未找到已建立的時間點。';
    momentResults.replaceChildren(empty);
    return;
  }
  momentResults.replaceChildren(...hits.map(moment=>renderMomentButton(moment,resourceById.get(moment.canonicalId))));
}

async function loadCinema(){
  try{
    const [resourceResponse,momentResponse]=await Promise.all([
      fetch('data/video-resource.v0.json',{cache:'no-store'}),
      fetch('data/video-moment.v0.json',{cache:'no-store'})
    ]);
    if(!resourceResponse.ok||!momentResponse.ok) throw new Error('Cinema data unavailable');
    const resourcePayload=await resourceResponse.json();
    const momentPayload=await momentResponse.json();
    if(resourcePayload.schema!=='holy-light.video-resource.v0'||!Array.isArray(resourcePayload.items)) throw new Error('Invalid Cinema resource schema');
    if(momentPayload.schema!=='holy-light.video-moment.v0'||!Array.isArray(momentPayload.items)) throw new Error('Invalid Cinema moment schema');
    resources=resourcePayload.items;
    moments=momentPayload.items;
    resourceById=new Map(resources.map(item=>[item.canonicalId,item]));
    library.replaceChildren(...resources.map(renderCard));
    document.documentElement.dataset.cinemaResources=String(resources.length);
    document.documentElement.dataset.cinemaMoments=String(moments.length);
  }catch(error){
    library.innerHTML='<p class="resource-card">館藏資料暫時無法載入。</p>';
    document.documentElement.dataset.cinemaError='resource-load';
  }
}

closeButton.addEventListener('click',()=>dialog.close());
dialog.addEventListener('close',()=>stage.replaceChildren());
dialog.addEventListener('click',event=>{if(event.target===dialog)dialog.close();});
momentSearch.addEventListener('click',searchMoments);
momentQuery.addEventListener('keydown',event=>{if(event.key==='Enter')searchMoments();});
loadCinema();