import { resourceManifest, resourceWorks, resourceSearch } from '../../js/resource-fabric-client.mjs';

const root = document.querySelector('[data-dawn-product]');
const shelvesHost = root.querySelector('[data-shelves]');
const search = root.querySelector('[data-search]');
const count = root.querySelector('[data-count]');

const [storefront, surface, manifest] = await Promise.all([
  fetch('../storefront.json').then(r => r.json()),
  fetch('../surfaces/dawn-storefront.json').then(r => r.json()),
  resourceManifest()
]);
const storeShelves = new Map((storefront?.shelves || []).map(shelf => [shelf.id, shelf]));

function pointerSource(pointer) {
  if (typeof pointer === 'string' && /^https?:\/\//.test(pointer)) return { url: pointer };
  if (pointer && typeof pointer === 'object' && typeof pointer.url === 'string') return { url: pointer.url };
  return null;
}
function coverUrl(item) {
  const pointer = item?.resourceCoverPointer || item?.coverPointer;
  return typeof pointer === 'string' && pointer.startsWith('/dawn-library/covers/') ? pointer : '';
}
function makeBook(item) {
  const card = document.createElement('article');card.className='book';card.dataset.workId=item.workId||'';
  const coverWrap=document.createElement('div');coverWrap.className='cover-wrap';
  const fallback=document.createElement('div');fallback.className='fallback';fallback.innerHTML=`<small>Dawn Library</small><strong></strong><small>${item.author||item.authors?.[0]||'Canonical Work'}</small>`;fallback.querySelector('strong').textContent=item.title||'Untitled';coverWrap.append(fallback);
  const url=coverUrl(item);if(url){const img=document.createElement('img');img.alt=`${item.title} 封面`;img.loading='lazy';img.src=url;img.addEventListener('load',()=>fallback.remove(),{once:true});img.addEventListener('error',()=>img.remove(),{once:true});coverWrap.append(img)}
  const badge=document.createElement('span');badge.className='badge';badge.textContent='DAWN';coverWrap.append(badge);
  const title=document.createElement('h3');title.textContent=item.title||'Untitled';const author=document.createElement('p');author.textContent=item.author||item.authors?.[0]||'—';card.append(coverWrap,title,author);
  const source=item.source||pointerSource(item.readingPointer);if(source?.url){card.tabIndex=0;card.setAttribute('role','link');const open=()=>window.open(source.url,'_blank','noopener,noreferrer');card.addEventListener('click',open);card.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();open()}})}
  return card;
}
function appendShelf(title,items){if(!items.length)return 0;const section=document.createElement('section');section.className='shelf';const heading=document.createElement('h2');heading.textContent=title;const rail=document.createElement('div');rail.className='rail';items.forEach(item=>rail.append(makeBook(item)));section.append(heading,rail);shelvesHost.append(section);return items.length}
async function resolveSurfaceShelf(surfaceShelf){
  const refs=surfaceShelf?.items||[];const ids=refs.map(r=>r.workId).filter(Boolean);const works=await resourceWorks(ids);const legacy=storeShelves.get(surfaceShelf.id);const legacyById=new Map((legacy?.items||[]).filter(x=>x.workId).map(x=>[x.workId,x]));
  const items=ids.map(id=>{const work=works.get(id);if(!work)return null;const old=legacyById.get(id)||{};return {...work,author:work.authors?.[0]||old.author||'',source:old.source||pointerSource(work.readingPointer)}}).filter(Boolean);
  return {title:surfaceShelf.title||legacy?.title||surfaceShelf.id,items};
}
let resolvedShelves=null;
async function renderCurated(){
  if(!resolvedShelves)resolvedShelves=await Promise.all((surface?.shelves||[]).map(resolveSurfaceShelf));
  shelvesHost.replaceChildren();let visible=0;for(const shelf of resolvedShelves)visible+=appendShelf(shelf.title,shelf.items);count.textContent=`${manifest?.workCount||visible} resources`;
}
let searchGeneration=0;
async function renderSearch(query){
  const generation=++searchGeneration;const results=await resourceSearch(query);if(generation!==searchGeneration)return;shelvesHost.replaceChildren();const visible=appendShelf('All canonical resources',results.map(work=>({...work,author:work.authors?.[0]||''})));count.textContent=`${visible} / ${manifest?.workCount||0}`;if(!visible){const empty=document.createElement('p');empty.className='empty';empty.textContent='沒有符合目前搜尋的館藏。';shelvesHost.append(empty)}
}
search.addEventListener('input',event=>{const q=event.target.value.trim();if(!q){searchGeneration+=1;renderCurated().catch(console.error);return}renderSearch(q).catch(error=>console.error('Resource Fabric search failed',error))});
renderCurated().catch(error=>console.error('Resource Fabric render failed',error));
