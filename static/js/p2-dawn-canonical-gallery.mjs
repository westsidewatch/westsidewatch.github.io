/**
 * Canonical reader projection over ORIGINAL Dawn 203,448-work cover-preview.
 * Pre-existing /product/library-system API; no second catalog/identity.
 * Bounded 60 cards. Historical 21k index remains a separate browse shelf.
 */
import {dawnLibrary} from '/dawn-library/product/library-system.mjs';
let root=null,offset=0,rows=[],busy=false,readPointers=null;
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
  render(args);
 }catch(e){
  console.error('[Dawn canonical cover projection]',e);
  args.status.textContent='館藏資料暫時無法載入，請稍後重試。';
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
 status.textContent='第 '+(pageNumber+1)+' 頁 · 本頁 '+rows.length+' 部作品 · 主書目 '+root.workCount.toLocaleString('en-CA')+' 筆';
 prev.disabled=pageNumber===0;next.disabled=!hasFollowing;
}
export const nextOffset=()=> 'next';
export const prevOffset=()=> 'previous';
