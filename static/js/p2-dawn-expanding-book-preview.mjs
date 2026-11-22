/**
 * P2 Dawn · Codrops Thumbnail Grid Expanding Preview interaction grammar.
 * One preview panel follows the selected row; adjacent selection morphs inside
 * the same panel. No dependency, no invented bibliography, no source navigation
 * on initial thumbnail click. Editorial reading remains the original openBook.
 *
 * Reference: https://tympanus.net/Tutorials/ThumbnailGridExpandingPreview/
 */
const matchesMotion=()=>!globalThis.matchMedia?.('(prefers-reduced-motion: reduce)')?.matches;
const safeUrl=url=>{
 // Undefined is not a URL: new URL(undefined, origin) would fabricate /undefined.
 if(typeof url!=='string'||!url.trim())return null;
 try{const x=new URL(url,location.origin);return /^https?:$/.test(x.protocol)?x.href:null}
 catch{return null}
};
const make=(tag,className,content)=>{
 const el=document.createElement(tag);el.className=className;
 if(content!==undefined)el.textContent=String(content);
 return el;
};
const asAuthor=book=>book.creator||book.author||
 (Array.isArray(book.authors)?book.authors.join(' · '):'')||'作者未詳';
const coverFor=book=>{
 // Explicitly same-work illustration; never use a title-based image match.
 const source=book.illustration?.url||book.cover?.url||book.cover?.src;
 return safeUrl(source);
};
function directChildren(grid){
 return [...grid.children].filter(el=>el!==panel&&el.matches?.('li,button'));
}
let panel=null,selected=null,selectedBook=null,selectedContainer=null,openReading=null,revision=0;
let switchTimer=0;
function closePanel(){
 revision++;clearTimeout(switchTimer);
 selected?.classList.remove('dawn-book-selected');
 selected?.setAttribute('aria-expanded','false');
 selected=null;selectedBook=null;selectedContainer=null;openReading=null;
 panel?.remove();panel=null;
}
export function dismissBookPreview(){closePanel()}
function positionAfterRow(grid,tile){
 const siblings=directChildren(grid);
 let index=siblings.indexOf(tile);
 if(index<0)return;
 const rowY=tile.getBoundingClientRect().top;
 while(index+1<siblings.length&&Math.abs(siblings[index+1].getBoundingClientRect().top-rowY)<5)index++;
 siblings[index].after(panel);
}
function previewContents(book,onRead){
 const content=make('div','dawn-expander__content');
 const eyebrow=make('div','dawn-expander__eyebrow',book.discoveryOnly?'書籍介紹':'選書預覽');
 const figure=make('button','dawn-expander__book');
 figure.type='button';figure.setAttribute('aria-label','打開書籍：'+(book.title||'未標題作品'));
 const image=coverFor(book);
 // A blank white "pending book cover" is never an acceptable preview.
 // Keep the exact title in paper while a publisher image is still loading.
 figure.classList.add('dawn-expander__book--paper');
 if(book.discoveryOnly)figure.classList.add('dawn-expander__book--discovery');
 if(image){
  const img=make('img','dawn-expander__book-image');
  img.alt='此作品圖像：'+(book.title||'');
  img.loading='eager';img.decoding='async';
  img.addEventListener('load',()=>{
   if(img.naturalWidth>100){
    figure.classList.add('dawn-expander__book--ready');
    figure.classList.remove('dawn-expander__book--paper');
   }else img.remove();
  });
  img.addEventListener('error',()=>img.remove());
  img.src=image;
  figure.append(img);
 }
 const paper=make('span','dawn-expander__book-paper');
 paper.append(make('small','','DAWN LIBRARY'),
  make('strong','',book.title||'書籍介紹'));
 figure.append(paper);
 // Explicit reader entry is the second action, after choosing a cover.
 // The original canonical reading-pointer resolver can be asynchronous.
 let reading=false,enter;
 async function confirmReader(){
  if(reading)return;
  reading=true;
  if(enter){enter.disabled=true;enter.textContent=book.discoveryOnly?'正在開啟出版方…':'正在開啟書籍…'}
  try{
   await onRead(book,'catalogue');
   // External publisher visits open a new tab, while Dawn stays mounted.
   // Never leave the preview permanently disabled as "opening publisher".
   if(book.discoveryOnly){
    reading=false;
    if(enter&&enter.isConnected){
     enter.disabled=false;
     enter.textContent='前往出版方了解本書';
    }
   }
  }catch(error){
   console.error('[Dawn book reading]',error);
   reading=false;
   if(enter){enter.disabled=false;enter.textContent=book.discoveryOnly?'前往出版方了解本書':'打開此書 · 查看閱讀資訊'}
  }
 }
 figure.addEventListener('click',()=>void confirmReader());
 const meta=make('div','dawn-expander__metadata');
 const title=make('h3','dawn-expander__title',book.title||'書籍介紹');
 if(/[\u3400-\u9fff]/.test(book.title||''))title.classList.add('dawn-expander__title--zh');
 const author=make('p','dawn-expander__author',asAuthor(book));
 meta.append(eyebrow,title,author);
 if(book.date||book.edition?.publishDate){
  meta.append(make('p','dawn-expander__edition',String(book.date||book.edition.publishDate)));
 }
 // Internal Work identity remains in source metadata; never printed to readers.
 if(book.editorialParagraphs?.length){
  meta.append(make('p','dawn-expander__description',String(book.editorialParagraphs[0])));
 }else if(typeof book.descriptionZh==='string'&&book.descriptionZh.trim()){
  meta.append(make('p','dawn-expander__description',book.descriptionZh));
 }else meta.append(make('p','dawn-expander__description',
  '認識這本作品與作者，探索更多相關閱讀。'));
 const actions=make('div','dawn-expander__actions');
 enter=make('button','dawn-expander__read',book.discoveryOnly?'前往出版方了解本書':'打開此書 · 查看閱讀資訊');
 enter.type='button';enter.addEventListener('click',()=>void confirmReader());
 actions.append(enter);
 // External reading is an explicit SECOND act only, and only if a sourced URL exists.
 const url=safeUrl(book.sourceUrl||book.source?.url);
 if(url){
  const link=make('a','dawn-expander__source',book.discoveryOnly?'出版方介紹 ↗':'查看原書 ↗');
  link.href=url;link.target='_blank';link.rel='noopener noreferrer';actions.append(link);
 }
 meta.append(actions);
 content.append(figure,meta);
 return content;
}
export function expandBookPreview({grid,tile,book,onRead}){
 if(!grid||!tile||!book||typeof onRead!=='function')return;
 if(selected===tile&&panel?.isConnected){closePanel();return}
 const samePanel=Boolean(panel&&selectedContainer===grid&&panel.isConnected);
 const token=++revision;
 clearTimeout(switchTimer);
 selected?.classList.remove('dawn-book-selected');
 selected?.setAttribute('aria-expanded','false');
 selected=tile;selectedBook=book;selectedContainer=grid;openReading=onRead;
 tile.classList.add('dawn-book-selected');
 tile.setAttribute('aria-expanded','true');
 tile.setAttribute('aria-controls','dawn-book-expanding-preview');
 if(!samePanel){
  panel?.remove();
  panel=make(grid.tagName==='OL'?'li':'div','dawn-expander');
  panel.setAttribute('role','region');
  panel.setAttribute('aria-label','館藏選書預覽');
  panel.id='dawn-book-expanding-preview';
  const close=make('button','dawn-expander__close','關閉預覽 ×');
  close.type='button';close.addEventListener('click',closePanel);
  panel.append(close);
 }else{
  panel.classList.remove('dawn-expander--switching');
 }
 // The expander occupies the *whole* CSS grid row immediately after the
 // selected thumbnail row. Rows shift downward instead of overlaying covers.
 positionAfterRow(grid,tile);
 const gridBox=grid.getBoundingClientRect(),tileBox=tile.getBoundingClientRect();
 if(gridBox.width)panel.style.setProperty('--dawn-preview-pointer',
  (((tileBox.left+tileBox.right)/2-gridBox.left)/gridBox.width*100).toFixed(2)+'%');
 const old=panel.querySelector('.dawn-expander__content');
 const fresh=previewContents(book,onRead);
 if(old&&matchesMotion()){
  panel.classList.add('dawn-expander--switching');
  old.animate([{opacity:1,transform:'translateY(0)'},{opacity:0,transform:'translateY(-12px)'}],
   {duration:140,fill:'forwards',easing:'ease-in'});
  switchTimer=setTimeout(()=>{
   if(revision!==token||!panel?.isConnected)return;
   old.remove();panel.append(fresh);
   fresh.animate([{opacity:0,transform:'translateY(16px)'},{opacity:1,transform:'translateY(0)'}],
    {duration:320,fill:'both',easing:'cubic-bezier(.2,.75,.2,1)'});
   panel.classList.remove('dawn-expander--switching');
  },145);
 }else{
  old?.remove();panel.append(fresh);
  if(matchesMotion())panel.animate([{opacity:.6,clipPath:'inset(0 0 100% 0)'},{opacity:1,clipPath:'inset(0 0 0 0)'}],
   {duration:460,easing:'cubic-bezier(.2,.75,.2,1)'});
 }
 // Never force document/page navigation. In P2, scroll the inner reading
 // surface to the preview so the catalog remains visible on either side.
 const view=grid.closest('.dawn-second')||grid.closest('[id="dawn-second"]');
 if(view)requestAnimationFrame(()=>{
  if(revision!==token)return;
  const panelTop=panel.getBoundingClientRect().top;
  const surfaceTop=view.getBoundingClientRect().top;
  const target=view.scrollTop+panelTop-surfaceTop-80;
  view.scrollTo({top:Math.max(0,target),behavior:matchesMotion()?'smooth':'instant'});
 });
}
export const previewSelection=()=>({workId:selectedBook?.workId||null,
 title:selectedBook?.title||null,expanded:Boolean(panel?.isConnected)});
