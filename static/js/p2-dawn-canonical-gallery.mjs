/**
 * Canonical reader projection over ORIGINAL Dawn 203,448-work cover-preview.
 * Pre-existing /product/library-system API; no second catalog/identity.
 * Bounded 60 cards. Historical 21k index remains a separate browse shelf.
 */
import {dawnLibrary} from '/dawn-library/product/library-system.mjs';
import {resourceSearch} from '/js/resource-fabric-client.mjs';
let root=null,offset=0,rows=[],busy=false,readPointers=null;
let searchResults=null,searchRequest=0,searchTerm='';
let pageStarts=[{shard:0,index:0}],pageNumber=0,nextStart=null,hasFollowing=false;
const pageSize=60;
const safe=url=>{
 try{const u=new URL(url,location.origin);return /^https?:$/.test(u.protocol)?u.href:null}catch{return null}
};
const options=({container,total,status,prev,next,search,openBook,expectedWorkCount})=>
 ({container,total,status,prev,next,search,openBook,expectedWorkCount});
export async function show(args,requested=0){
 if(busy)return;
 busy=true;
 try{
  root ||= await dawnLibrary.coverPreviewRoot();
  if(root.workCount!==args.expectedWorkCount||root.shardCount!==root.shards.length)
   throw Error('Dawn canonical versus cover-preview identity mismatch');
  if(requested===0){pageNumber=0;pageStarts=[{shard:0,index:0}]}
  else if(requested==='next'&&nextStart){
   pageNumber++;pageStarts[pageNumber]={...nextStart};pageStarts.length=pageNumber+1;
  }else if(requested==='previous'&&pageNumber>0)pageNumber--;
  const start=pageStarts[pageNumber];
  if(!start)throw Error('Dawn page cursor unavailable');
  let cursor={...start};
  rows=[];
  // Some legacy cover-preview shard counts/offsets precede source-scope
  // exclusions. Only actual member rows may advance this cursor.
  // NEVER index into a shortened shard using the stale manifest offset.
  while(rows.length<pageSize&&cursor.shard<root.shards.length){
   const meta=root.shards[cursor.shard];
   const data=await dawnLibrary.coverPreviewShard(meta.href);
   if(data.schema!=='dawn.library.cover-preview-shard.v1'||!Array.isArray(data.items))
    throw Error('Dawn cover-preview source contract invalid');
   if(cursor.index>=data.items.length){cursor.shard++;cursor.index=0;continue}
   const batch=data.items.slice(cursor.index,cursor.index+(pageSize-rows.length));
   if(!batch.length){cursor.shard++;cursor.index=0;continue}
   rows.push(...batch);
   cursor.index+=batch.length;
   if(cursor.index>=data.items.length){cursor.shard++;cursor.index=0}
  }
  nextStart=cursor.shard<root.shards.length?{...cursor}:null;
  hasFollowing=Boolean(nextStart);
  offset=pageNumber*pageSize;
  args.total.textContent=root.workCount.toLocaleString('en-CA');
  if(!String(args.search.value||'').trim())render(args);
 }catch(e){
  console.error('[Dawn canonical cover projection]',e);
  args.status.textContent='館藏資料暫時無法載入，請稍後重試。';
 }finally{busy=false}
}
export function render({container,status,prev,next,search,openBook}){
 if(!root)return;
 const needle=search.value.trim().toLocaleLowerCase();
 const matchingSearch=needle&&searchTerm===needle&&Array.isArray(searchResults);
 const shown=matchingSearch?searchResults:needle?[]:rows;
 const frag=document.createDocumentFragment();
 for(const [i,record] of shown.entries()){
  const title=String(record.title||'').trim();
  const author=(record.authors||[]).join(' · ');
  // Resource Fabric resolves canonical Work IDs; do not filter again against
  // the current 60-row window or silently drop indexed matches.
  const li=document.createElement('li');li.className='dawn-catalogue__sleeve';
  const imgUrl=safe(record.cover?.src||record.cover?.url);
  const visual=imgUrl&&record.cover?.source!=='dawn-placeholder';
  const book={title:title||record.workId,creator:author,workId:record.workId,
   cover:visual?{url:imgUrl}:null};
  const card=document.createElement('button');card.type='button';
  card.className='dawn-catalogue__cover-card'+(visual?' dawn-catalogue__cover-card--image':' dawn-catalogue__cover-card--unresolved');
  card.setAttribute('aria-label','查看 '+book.title);
  card.addEventListener('click',async()=>{
   try{
    readPointers ||= await fetch('/dawn-library/reading-pointer-map.json').then(r=>r.ok?r.json():null);
    const reading=(readPointers?.items||[]).find(row=>row.workId===record.workId);
    if(reading?.sourceUrl)book.sourceUrl=reading.sourceUrl;
   }catch{}
   openBook(book,'catalogue');
  });
  if(visual){
   const image=document.createElement('img');image.src=imgUrl;
   image.alt='書籍封面：'+book.title;image.loading='lazy';image.decoding='async';
   image.addEventListener('error',()=>{
    image.remove();card.classList.remove('dawn-catalogue__cover-card--image');
    card.classList.add('dawn-catalogue__cover-card--unresolved');
   });card.append(image);
  }
  const text=document.createElement('div');text.className='dawn-catalogue__cover-typography';
  const number=document.createElement('small');number.textContent=String((matchingSearch?0:offset)+i+1).padStart(5,'0');
  const name=document.createElement('strong');name.textContent=book.title;
  const creator=document.createElement('span');creator.textContent=author||'作者未詳';
  text.append(number,name,creator);card.append(text);li.append(card);frag.append(li);
 }
 container.replaceChildren(frag);
 if(needle){
  status.textContent=matchingSearch?
   '全館索引搜尋：找到 '+searchResults.length+' 筆相關作品 · 搜尋索引不等於全館逐字全文檢索':
   '正在搜尋全館作品索引…';
  prev.disabled=true;next.disabled=true;
 }else{
  status.textContent='第 '+(pageNumber+1)+' 頁 · 本頁 '+rows.length+' 部作品 · 主書目 '+root.workCount.toLocaleString('en-CA')+' 筆';
  prev.disabled=pageNumber===0;next.disabled=!hasFollowing;
 }
}
/** Use the existing site-wide Resource Fabric search buckets, not a page-only filter. */
export async function searchCatalogue(args){
 const term=String(args.search.value||'').trim().toLocaleLowerCase();
 const ticket=++searchRequest;
 searchTerm=term;searchResults=null;
 if(!term){render(args);return}
 render(args);
 try{
  const found=await resourceSearch(term);
  if(ticket!==searchRequest||String(args.search.value||'').trim().toLocaleLowerCase()!==term)return;
  searchResults=Array.isArray(found)?found:[];
  render(args);
 }catch(error){
  if(ticket!==searchRequest)return;
  console.error('[Dawn resource-fabric search]',error);
  args.status.textContent='全館搜尋暫時無法使用，請稍後重試。';
  args.prev.disabled=true;args.next.disabled=true;
 }
}

export const nextOffset=()=> 'next';
export const prevOffset=()=> 'previous';
