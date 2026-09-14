const style=document.createElement('link');style.rel='stylesheet';style.href='coordinate-layer.css';style.dataset.cinemaCoordinateStyle='v0';document.head.appendChild(style);

function allCoordinateLabels(entry){const c=entry?.coordinate?.coordinates||entry?.coordinates||{};return [...(c.text||[]),...(c.world||[])].map(item=>item.label).filter(Boolean);}
function collectionCount(works,id){return works.reduce((count,item)=>count+(item.coordinate?.collection===id?1:0),0);}
async function waitForCards(){for(let attempt=0;attempt<80;attempt++){if(document.querySelector('.resource-card[data-canonical-id]'))return true;await new Promise(resolve=>setTimeout(resolve,50));}return false;}

function ensureNote(library){const note=document.createElement('p');note.id='cinema-collection-note';note.className='collection-note';library.parentElement?.insertBefore(note,library);return note;}
function buildNav(graph){
  const nav=document.querySelector('nav');const library=document.querySelector('#cinema-library');if(!nav||!library)return;
  nav.classList.add('collection-nav');nav.replaceChildren();
  const choices=[{id:'all',label:'全部館藏',description:'天堂電影院 canonical resource graph 中目前已建立座標的全部資源。'},...graph.collections];
  const notes=new Map(choices.map(item=>[item.id,item.description||'']));const byId=new Map(graph.works.map(item=>[item.canonicalId,item]));const buttons=[];
  for(const choice of choices){
    const count=choice.id==='all'?graph.works.length:collectionCount(graph.works,choice.id);if(choice.id!=='all'&&count===0)continue;
    const button=document.createElement('button');button.type='button';button.className='collection-filter';button.dataset.collection=choice.id;button.setAttribute('aria-pressed',choice.id==='all'?'true':'false');button.innerHTML=`<span>${choice.label}</span><small>${String(count).padStart(2,'0')}</small>`;
    button.addEventListener('click',()=>{for(const candidate of buttons)candidate.setAttribute('aria-pressed',candidate===button?'true':'false');const active=choice.id;for(const card of library.querySelectorAll('.resource-card[data-canonical-id]')){const entry=byId.get(card.dataset.canonicalId);card.hidden=active!=='all'&&entry?.coordinate?.collection!==active;}const note=document.querySelector('#cinema-collection-note')||ensureNote(library);note.textContent=notes.get(active)||'';document.documentElement.dataset.cinemaCollection=active;});
    buttons.push(button);nav.appendChild(button);
  }
  const note=document.querySelector('#cinema-collection-note')||ensureNote(library);note.textContent=notes.get('all')||'';document.documentElement.dataset.cinemaCollection='all';
}
function decorateCards(graph){
  const byId=new Map(graph.works.map(item=>[item.canonicalId,item]));
  for(const card of document.querySelectorAll('.resource-card[data-canonical-id]')){const entry=byId.get(card.dataset.canonicalId);if(!entry)continue;card.dataset.collection=entry.coordinate?.collection||'';const labels=allCoordinateLabels(entry);if(!labels.length)continue;const line=document.createElement('div');line.className='resource-coordinates';line.setAttribute('aria-label','聖經世界座標');line.textContent=labels.slice(0,4).join(' · ');const action=card.querySelector('.resource-action');card.insertBefore(line,action||null);}
}
function expose(graph){window.ParadiseCinemaCoordinates=Object.freeze({schema:'dore.bible-media-coordinate.v0',get(canonicalId){return graph.coordinate(canonicalId);},labels(canonicalId){return allCoordinateLabels(graph.get(canonicalId));},collection(canonicalId){return graph.get(canonicalId)?.coordinate?.collection||null;}});}
async function init(){
  try{const graph=await window.ParadiseCinemaGraph?.ready;if(!graph||graph.schema!=='dore.bible-media-graph.v0')throw new Error('canonical graph unavailable');if(!await waitForCards())throw new Error('cinema cards unavailable');decorateCards(graph);buildNav(graph);expose(graph);document.documentElement.dataset.cinemaCoordinates=String(graph.coordinates.length);document.documentElement.dataset.cinemaCoordinateSchema='v0';document.documentElement.dataset.cinemaCoordinateAuthority='dore.bible-media-graph.v0';}
  catch(error){document.documentElement.dataset.cinemaCoordinateError='load';}
}
init();
