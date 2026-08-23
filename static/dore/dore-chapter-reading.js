(()=>{
'use strict';
const $=s=>document.querySelector(s);
const esc=s=>String(s??'').replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));
let applying=false;
function chapterRef(){
  const q=$('#search-input')?.value?.trim();
  if(!q)return null;
  const refs=window.DoreReferenceGrammar?.parseAll?.(q)||[];
  if(refs.length!==1)return null;
  const ref=refs[0];
  return ref.start==null?ref:null;
}
function enforce(){
  if(applying)return;
  const ref=chapterRef(),box=$('#results'),count=$('#result-count');
  if(!ref||!box||!count||box.querySelector('.chapter-reading'))return;
  const cards=[...box.querySelectorAll('.result-card')];
  if(cards.length<2)return;
  const rows=cards.map(card=>{
    const label=card.querySelector('header strong')?.textContent?.trim()||'';
    const m=label.match(/(\d+)\s*$/);
    const verse=m?m[1]:'';
    const zh=card.querySelector('p[lang="zh-Hant"]')?.textContent?.trim()||'';
    const en=card.querySelector('p.english')?.textContent?.trim()||'';
    return{verse,zh,en};
  }).filter(x=>x.zh||x.en);
  if(rows.length<2)return;
  const firstLabel=cards[0].querySelector('header strong')?.textContent?.trim()||'';
  const book=firstLabel.replace(/\s+\d+:\d+\s*$/,'').trim()||ref.book;
  const zh=rows.map(r=>`<sup>${esc(r.verse)}</sup>${esc(r.zh)}`).join('　');
  const en=rows.filter(r=>r.en).map(r=>`<sup>${esc(r.verse)}</sup>${esc(r.en)}`).join(' ');
  applying=true;
  count.textContent=`${book} ${ref.chapter}章 · ${rows.length}節`;
  box.innerHTML=`<article class="chapter-reading"><header><strong>${esc(book)} ${esc(ref.chapter)}章</strong></header><p class="chapter-reading__zh" lang="zh-Hant">${zh}</p>${en?`<p class="chapter-reading__en english" lang="en">${en}</p>`:''}</article>`;
  applying=false;
}
function init(){
  const box=$('#results');if(!box)return;
  new MutationObserver(()=>queueMicrotask(enforce)).observe(box,{childList:true,subtree:true});
  $('#search-form')?.addEventListener('submit',()=>setTimeout(enforce,0));
  enforce();
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
})();
