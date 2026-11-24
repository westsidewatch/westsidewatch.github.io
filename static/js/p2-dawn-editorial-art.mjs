/**
 * P2 05 canonical editorial-art bridge.
 * The three entry views own no book identity or independent catalogue.
 * Each plate comes from that entry's already-governed source. No unrelated
 * cover or fictitious historical illustration can be substituted.
 */
import { dawnLibrary } from '/dawn-library/product/library-system.mjs';
const $=selector=>document.querySelector(selector);
const portal={stars:$('[data-dawn-portal="三晨星"]'),
 exhibition:$('[data-dawn-portal="策展集"]'),
 spectrum:$('[data-dawn-portal="光譜"]')};
const safeImage=url=>{
 try{const u=new URL(url,location.origin);return ['https:','http:'].includes(u.protocol)?u.href:null}catch{return null}
};
function insert(tile,items){
 if(!tile||!Array.isArray(items)||!items.length)return;
 const art=tile.querySelector('.dawn-feature__art');
 if(!art)return;
 art.replaceChildren();
 for(const [i,item] of items.slice(0,3).entries()){
  const block=document.createElement('span');block.className='dawn-feature__plate dawn-feature__cover--'+(i+1);
  const title=document.createElement('span');title.className='dawn-feature__plate-title';
  title.textContent=String(item.title||item.workId||'作品');
  block.append(title);
  const url=safeImage(item.cover);
  if(url){
   const img=document.createElement('img');img.className='dawn-feature__cover';
   img.loading='lazy';img.decoding='async';img.alt='';
   img.onload=()=>{block.classList.add('dawn-feature__plate--loaded')};
   img.onerror=()=>{img.remove();block.classList.remove('dawn-feature__plate--loaded')};
   img.src=url;block.prepend(img);
  }
  if(item.workId)block.dataset.dawnWorkId=item.workId;
  if(item.source)block.dataset.dawnSource=item.source;
  art.append(block);
 }
}
async function loadStars(){
 const selection=await dawnLibrary.morningStars();
 if(!Array.isArray(selection.items)||selection.items.length!==3)throw Error('Morning Stars selection contract changed');
 const ids=selection.items.map(item=>item.workId);
 const works=await dawnLibrary.works(ids);
 const items=ids.map(id=>{
  const work=works.get(id);
  // Never pretend a different author's book cover belongs to this Work.
  return {workId:id,title:work?.title||'原書待核對',
   cover:work?dawnLibrary.coverUrl(work):null};
 });
 insert(portal.stars,items);
}
async function loadExhibition(){
 const registry=await(await fetch('/dawn-library/p2-exhibitions/jerusalem-3000.json')).json();
 const images=(registry.items||[]).filter(item=>
  item.media?.src&&item.media?.source&&item.sourceWork&&item.title);
 insert(portal.exhibition,images.slice(0,3).map(item=>({
  title:item.title,cover:item.media.src,source:item.media.source,
  workId:item.workId||''
 })));
}
async function loadSpectrum(){
 const [channel,storefront]=await Promise.all([
  fetch('/dawn-library/p2-editorial-channels.json').then(r=>r.json()),
  fetch('/dawn-library/storefront.json').then(r=>r.json())
 ]);
 const route=channel.channels?.['光譜'];
 if(!route||!Array.isArray(route.topics))throw Error('Spectrum editorial channel missing');
 const allowed=new Set(route.topics.flatMap(topic=>topic.shelves||[]));
 const candidate=(storefront.shelves||[])
  .filter(shelf=>allowed.has(shelf.id))
  .flatMap(shelf=>shelf.items||[])
  .filter(work=>work.title&&work.source?.url&&safeImage(work.cover?.url));
 // Prefer Bible text research, Jewish background and historical scholarship,
 // not unrelated general fiction despite a legacy "精品書架" source shelf.
 const chosen=candidate.filter(work=>/Pentateuch|Hebrew Bible|Post-Biblical history|Bible atlas|Biblical Literature/i.test(work.title)).slice(0,3);
 insert(portal.spectrum,chosen.map(work=>({
  workId:work.workId||'',title:work.title,cover:work.cover.url,
  source:work.source.url
 })));
}
await Promise.allSettled([loadStars(),loadExhibition(),loadSpectrum()]);
