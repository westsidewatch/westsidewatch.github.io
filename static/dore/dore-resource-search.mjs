import {resourceSearch,resourceManifest} from '/js/resource-fabric-client.mjs';

const SECTION_ID='dore-resource-fabric-results';
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));

function host(){return document.querySelector('#results')||document.querySelector('.dore-search-results');}
function removeSection(){document.getElementById(SECTION_ID)?.remove();}
function localHref(pointer=''){const p=String(pointer||'');return p.startsWith('/')&&!/^\/\//.test(p)?p:null;}
function render(query,works){
  const root=host();if(!root)return;
  removeSection();
  const section=document.createElement('section');section.id=SECTION_ID;section.dataset.resourceFabricResults='v0';section.style.gridColumn='1/-1';
  const cards=(works||[]).slice(0,24).map(work=>{
    const href=localHref(work.readingPointer);
    const title=esc(work.title||'Untitled');
    const author=esc((work.authors||[]).join(', ')||'Canonical Work');
    return `<article class="result-card" data-resource-work-id="${esc(work.workId)}"><header><strong>${title}</strong><span>${author}</span></header><p>黎明資源底層 · ${work.authorityBacked?'Authority-backed':'Canonical'}${href?` · <a href="${esc(href)}">閱讀</a>`:''}</p><footer><span>${esc(work.workId)}</span><span>RESOURCE FABRIC</span></footer></article>`;
  }).join('');
  section.innerHTML=`<div class="results-head"><h2>全站資源</h2><span>${works.length} resources · Atlas routed</span></div><div style="display:grid;grid-template-columns:repeat(2,minmax(0,1fr));column-gap:clamp(34px,3.4vw,72px)">${cards||`<p class="empty">沒有符合「${esc(query)}」的共享資源。</p>`}</div>`;
  root.prepend(section);
}

async function search(detail={}){
  const query=String(detail.query||'').trim();if(!query)return [];
  const manifest=await resourceManifest();
  if(manifest.canonicalMonolithRequired!==false)throw new Error('Resource Fabric monolith boundary violated');
  const works=await resourceSearch(query);
  render(query,works);
  document.documentElement.dataset.doreResourceSearch=`PASS:${works.length}`;
  return works;
}

window.addEventListener('dore:search-query',event=>{
  search(event.detail||{}).catch(error=>{console.warn('[DORÉ Resource Search]',error);removeSection();});
});

window.DoreResourceSearch=Object.freeze({schema:'dore.resource-search.consumer.v0',search});
