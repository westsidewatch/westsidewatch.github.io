/**
 * Canonical reader projection over ORIGINAL Dawn 203,448-work cover-preview.
 * Pre-existing /product/library-system API; no second catalog/identity.
 * Bounded 60 cards. Historical 21k index remains a separate browse shelf.
 */
import {dawnLibrary} from '/dawn-library/product/library-system.mjs';
let root=null,offset=0,rows=[],busy=false,readPointers=null;
const pageSize=60;
const safe=url=>{
 try{const u=new URL(url,location.origin);return /^https?:$/.test(u.protocol)?u.href:null}catch{return null}
};
export async function show({container,total,status,prev,next,search,openBook,expectedWorkCount},requested=0){
 if(busy)return;
 busy=true;
 try{
  root ||= await dawnLibrary.coverPreviewRoot();
  if(root.workCount!==expectedWorkCount||root.shardCount!==root.shards.length)
   throw Error('Dawn canonical versus cover-preview identity mismatch');
  offset=Math.max(0,Math.min(requested,root.workCount-1));
  rows=[];
  while(rows.length<pageSize&&offset+rows.length<root.workCount){
   const at=offset+rows.length;
   const shard=root.shards.find(s=>at>=s.offset&&at<s.offset+s.count);
   if(!shard)throw Error('Dawn cover shard is missing for '+at);
   const data=await dawnLibrary.coverPreviewShard(shard.href);
   if(data.schema!=='dawn.library.cover-preview-shard.v1'||!Array.isArray(data.items))
    throw Error('Invalid Dawn cover shard');
   const batch=data.items.slice(at-shard.offset,at-shard.offset+pageSize-rows.length);
   if(!batch.length)throw Error('Dawn cover shard has no rows');
   rows.push(...batch);
  }
  total.textContent=root.workCount.toLocaleString('en-CA');
  render({container,status,prev,next,search,openBook});
 }catch(e){
  console.error('[Dawn canonical cover projection]',e);
  status.textContent='館藏資料暫時無法載入，請稍後重試。';
 }finally{busy=false}
}
export function render({container,status,prev,next,search,openBook}){
 if(!root)return;
 const needle=search.value.trim().toLocaleLowerCase();
 const frag=document.createDocumentFragment();
 for(const [i,record] of rows.entries()){
  const title=String(record.title||'').trim();
  const author=(record.authors||[]).join(' · ');
  if(needle&&!(title+' '+author).toLocaleLowerCase().includes(needle))continue;
  const li=document.createElement('li');li.className='dawn-catalogue__sleeve';
  const imgUrl=safe(record.cover?.src);
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
  const number=document.createElement('small');number.textContent=String(offset+i+1).padStart(5,'0');
  const name=document.createElement('strong');name.textContent=book.title;
  const creator=document.createElement('span');creator.textContent=author||'作者未詳';
  text.append(number,name,creator);card.append(text);li.append(card);frag.append(li);
 }
 container.replaceChildren(frag);
 status.textContent=(offset+1).toLocaleString('en-CA')+'–'+Math.min(offset+rows.length,root.workCount).toLocaleString('en-CA')+' / '+root.workCount.toLocaleString('en-CA')+' 部館藏作品';
 prev.disabled=offset===0;next.disabled=offset+rows.length>=root.workCount;
}
export const nextOffset=()=>offset+pageSize;
export const prevOffset=()=>Math.max(0,offset-pageSize);
