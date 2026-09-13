document.documentElement.dataset.surface='holy-light-cinema';
document.documentElement.dataset.core='dore';

const library=document.querySelector('#cinema-library');
const dialog=document.querySelector('#cinema-player');
const stage=document.querySelector('#player-stage');
const closeButton=document.querySelector('.player-close');

function renderCard(item){
  const source=(item.providerSources||[])[0]||{};
  const card=document.createElement('article');
  card.className='resource-card';
  card.dataset.canonicalId=item.canonicalId;
  card.innerHTML=`<div class="resource-meta">${item.kind||'video'} · ${item.creator||''}</div><h4>${item.title}</h4><p>${item.series||''}</p><div class="resource-topics">${(item.topics||[]).join(' · ')}</div>`;
  const action=document.createElement('button');
  action.className='resource-action';
  action.type='button';
  action.textContent=source.embed&&source.embedUrl?'在影院播放':'前往官方來源';
  action.addEventListener('click',()=>{
    if(source.embed&&source.embedUrl){
      stage.innerHTML=`<iframe src="${source.embedUrl}" title="${item.title}" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>`;
      dialog.showModal();
    }else if(source.url){
      window.open(source.url,'_blank','noopener,noreferrer');
    }
  });
  card.appendChild(action);
  return card;
}

async function loadLibrary(){
  try{
    const response=await fetch('data/video-resource.v0.json',{cache:'no-store'});
    if(!response.ok) throw new Error(`HTTP ${response.status}`);
    const payload=await response.json();
    if(payload.schema!=='holy-light.video-resource.v0'||!Array.isArray(payload.items)) throw new Error('Invalid Cinema resource schema');
    library.replaceChildren(...payload.items.map(renderCard));
    document.documentElement.dataset.cinemaResources=String(payload.items.length);
  }catch(error){
    library.innerHTML='<p class="resource-card">館藏資料暫時無法載入。</p>';
    document.documentElement.dataset.cinemaError='resource-load';
  }
}

closeButton.addEventListener('click',()=>dialog.close());
dialog.addEventListener('close',()=>stage.replaceChildren());
dialog.addEventListener('click',event=>{if(event.target===dialog)dialog.close();});
loadLibrary();