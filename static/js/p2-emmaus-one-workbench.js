/* P2 / 03 Emmaus — an actual ONE study workstation, not an outbound-only teaser.
 * Canonical book/chapter identities come from /one/one-data.js; the full
 * unchanged ONE app is embedded on demand to avoid an expensive second app
 * while the visitor scrolls the Magazine. Never changes /one/ or /p2/ source.
 */
(()=>{'use strict';
 const root=document.getElementById('emmaus'),data=window.ONE_DATA;
 const books=data?.books,chapterGrid=document.getElementById('em-one-chapter-grid'),
  locationLabel=document.getElementById('em-one-location'),
  chapterCount=document.getElementById('em-one-chapter-count'),
  pane=document.getElementById('em-one-workbench'),
  open=document.getElementById('em-one-open'),close=document.getElementById('em-one-close'),
  frame=document.getElementById('em-one-frame'),title=document.getElementById('em-one-workbench-title'),
  standalone=document.getElementById('em-one-standalone');
 if(!root||books?.length!==66||!chapterGrid||!pane||!frame||!open||!close)return;
 let activeBook=42,activeChapter=24,lastRenderedBook=0;
 const studyFor=number=>number===42?data.luke:number===40?data.matthew:
  data.studyBooks?.[number]||null;
 const bookAt=number=>books[number-1];
 const urlFor=(n,ch)=>'/one/?book='+n+'&chapter='+ch;
 function chooseChapter(n,ch){
  if(typeof window.P2EmmausSelect==='function')window.P2EmmausSelect(n,ch);
  else root.dispatchEvent(new CustomEvent('p2:one-request',{detail:{book:n,chapter:ch}}));
 }
 function renderChapterNumbers(){
  const book=bookAt(activeBook);if(!book)return;
  if(lastRenderedBook!==activeBook){
   const frag=document.createDocumentFragment(),source=studyFor(activeBook);
   for(let ch=1;ch<=book[3];ch++){
    const item=document.createElement('button');item.type='button';
    item.dataset.oneChapter=String(ch);item.textContent=String(ch).padStart(2,'0');
    item.setAttribute('aria-label',book[1]+' 第 '+ch+' 章'+(source?.chapters?.[ch-1]?' — '+source.chapters[ch-1]:''));
    item.title=source?.chapters?.[ch-1]||book[1]+' '+ch;
    item.addEventListener('click',()=>chooseChapter(activeBook,ch));
    frag.append(item);
   }
   chapterGrid.replaceChildren(frag);lastRenderedBook=activeBook;
  }
  chapterCount.textContent=String(book[3])+' CHAPTERS';
  const current=book[1]+' · 第 '+activeChapter+' 章';
  locationLabel.textContent=current;
  title.textContent=current;
  standalone.href=urlFor(activeBook,activeChapter);
  for(const button of chapterGrid.children){
   const selected=Number(button.dataset.oneChapter)===activeChapter;
   button.setAttribute('aria-pressed',String(selected));
   if(selected)button.setAttribute('aria-current','step');
   else button.removeAttribute('aria-current');
  }
 }
 function select(n,ch){
  if(!Number.isInteger(n)||n<1||n>66)return;
  activeBook=n;
  activeChapter=Math.max(1,Math.min(bookAt(n)[3],Number(ch)||1));
  renderChapterNumbers();
  // Do not continuously reload a full ONE app while the book rail is scrolled.
  // If already open, changing book/chapter deliberately selects a new ONE session.
  if(!pane.hidden){
   const route=urlFor(activeBook,activeChapter);
   if(frame.getAttribute('src')!==route)frame.src=route;
  }
 }
 function openWorkbench(){
  renderChapterNumbers();
  pane.hidden=false;
  pane.setAttribute('aria-hidden','false');
  root.dataset.oneWorkbench='open';
  const route=urlFor(activeBook,activeChapter);
  if(frame.getAttribute('src')!==route)frame.src=route;
  close.focus({preventScroll:true});
 }
 function closeWorkbench(){
  pane.hidden=true;pane.setAttribute('aria-hidden','true');
  root.dataset.oneWorkbench='closed';
  // Release full ONE app timers, DOM and chapter imagery before scrolling 04.
  frame.removeAttribute('src');
  open.focus({preventScroll:true});
 }
 open.addEventListener('click',openWorkbench);
 close.addEventListener('click',closeWorkbench);
 pane.addEventListener('keydown',e=>{
  if(e.key==='Escape'){e.preventDefault();closeWorkbench()}
 });
 root.addEventListener('p2:one-selection',e=>{
  const n=Number(e.detail?.book),ch=Number(e.detail?.chapter);
  select(n,ch);
 });
 // Workbench is interactive INSIDE P2, never a forced external navigation.
 root.dataset.oneWorkbench='closed';pane.hidden=true;pane.setAttribute('aria-hidden','true');
 select(Number(root.dataset.selectedBook)||42,Number(root.dataset.selectedChapter)||24);
 window.P2EmmausONE={select,open:openWorkbench,close:closeWorkbench,refresh:()=>{lastRenderedBook=0;renderChapterNumbers()}};
})();
