/* Westside Design OS — readable end-of-line (orphans) correction.
 * P2 adoption: text-only, non-destructive to canonical source data.
 * For Chinese paragraphs bind the last 3 ideographs + punctuation; for
 * English paragraphs bind the last 2 words. Native text-wrap:pretty is
 * first-line protection; this tiny semantic tail guard supplements it.
 * Never touches protected Magazine/Church iframe or changes ONE datasets.
 */
(()=>{'use strict';
 const roots=[document.getElementById('emmaus'),document.getElementById('olive-proof')].filter(Boolean);
 if(!roots.length)return;
 const selector='p,blockquote,h1,h2,h3,h4,li,strong,.emmaus__scripture-zh,.emmaus__scripture-en,.olive-proof__statement';
 const cjk=/([\p{Script=Han}]{3}[\p{Punctuation}\s]*)$/u;
 const english=/([A-Za-z][A-Za-z'’\-]*[ \t]+[A-Za-z][A-Za-z'’\-]*[.!?;:)"”’]*)$/u;
 const pending=new Set();
 let queued=false;
 for(const root of roots)root.setAttribute('data-ws-editorial-orphans','');
 function eligible(el){
  if(!el||!el.matches?.(selector)||el.children.length||el.closest('[contenteditable="true"],[data-ws-orphans-off]'))return false;
  if(el.closest('script,style,svg,pre,code,[hidden]'))return false;
  return roots.some(root=>root.contains(el));
 }
 function lockTail(el){
  if(!eligible(el))return;
  const node=el.firstChild;
  if(!node||node.nodeType!==3)return;
  const source=node.nodeValue||'',plain=source.trim();
  if(plain.length<12)return;
  let match=source.match(cjk);
  if(!match&&plain.length>=24)match=source.match(english);
  if(!match)return;
  const tail=match[1],prefix=source.slice(0,source.length-tail.length);
  if(prefix.trim().length<6)return;
  // A span is a visual no-break unit; the rendered + copied paragraph's
  // textContent remains byte-for-byte identical to its original text.
  const span=document.createElement('span');
  span.className='ws-editorial-no-orphan-tail';
  span.textContent=tail;
  node.nodeValue=prefix;
  node.after(span);
 }
 function addTargets(node,deep=false){
  const el=node?.nodeType===1?node:node?.parentElement;
  if(!el||!roots.some(root=>root===el||root.contains(el)))return;
  if(el.matches?.(selector))pending.add(el);
  if(deep&&el.querySelectorAll)for(const desc of el.querySelectorAll(selector))pending.add(desc);
  const closest=el.closest?.(selector);
  if(closest)pending.add(closest);
 }
 function flush(){
  queued=false;
  const batch=[...pending];pending.clear();
  for(const el of batch)if(el.isConnected)lockTail(el);
 }
 function schedule(){
  if(queued)return;
  queued=true;
  requestAnimationFrame(flush);
 }
 for(const root of roots)addTargets(root,true);
 schedule();
 const observer=new MutationObserver(records=>{
  for(const record of records){
   if(record.type==='characterData'){addTargets(record.target);continue;}
   addTargets(record.target);
   for(const node of record.addedNodes)addTargets(node,true);
  }
  if(pending.size)schedule();
 });
 for(const root of roots)observer.observe(root,{subtree:true,childList:true,characterData:true});
 // P2 appenders may request a cheap refresh; this never queries iframe content.
 window.WestsideEditorialOrphans={refresh(node){
  addTargets(node||document.getElementById('emmaus'),true);schedule();
 }};
})();