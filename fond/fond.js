const threshold=document.querySelector('#threshold');
const enter=document.querySelector('#enterFond');
const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
function openFond(){if(!threshold||threshold.classList.contains('opening'))return;threshold.classList.add('opening');const delay=reduce?30:1480;setTimeout(()=>{threshold.classList.add('gone');document.body.classList.remove('threshold-locked')},delay)}
enter?.addEventListener('click',openFond);

function placeTitlesBelowNumerals(){
 const stack=document.querySelector('.index-stack');
 const titles=document.querySelector('.book-titles');
 const pairs=[...document.querySelectorAll('#fondNumerals .pair')];
 if(!stack||!titles||!pairs.length)return;
 const stackRect=stack.getBoundingClientRect();
 const bottom=Math.max(...pairs.map(pair=>pair.getBoundingClientRect().bottom));
 titles.style.position='absolute';
 titles.style.top=`${Math.ceil(bottom-stackRect.top+14)}px`;
 titles.style.left='50%';
 titles.style.transform='translateX(-50%)';
 titles.style.marginTop='0';
}

function bindFondNumerals(){
 const book=document.querySelector('#fondNumerals'); if(!book||book.dataset.bound==='1')return;
 book.dataset.bound='1';
 const ns='http://www.w3.org/2000/svg';
 const canHover=matchMedia('(hover: hover) and (pointer: fine)').matches;
 const pairs=[...book.querySelectorAll('.pair')];
 pairs.forEach(pair=>{
   const key=pair.dataset.book;
   const title=document.querySelector(`.book-titles [data-book="${key}"]`);
   pair.style.pointerEvents='none';
   const box=pair.getBBox();
   const hit=document.createElementNS(ns,'rect');
   hit.setAttribute('x',String(box.x));hit.setAttribute('y',String(box.y));hit.setAttribute('width',String(box.width));hit.setAttribute('height',String(box.height));
   hit.setAttribute('fill','transparent');hit.setAttribute('pointer-events','all');hit.setAttribute('tabindex','0');hit.setAttribute('role','link');hit.dataset.book=key;hit.classList.add('pair-hit');
   pair.parentNode.insertBefore(hit,pair.nextSibling);
   let closingTimer=0;
   const open=()=>{clearTimeout(closingTimer);pair.classList.add('is-open');title?.classList.add('is-open')};
   const close=()=>{clearTimeout(closingTimer);closingTimer=setTimeout(()=>{pair.classList.remove('is-open');title?.classList.remove('is-open')},70)};
   if(canHover){
     hit.addEventListener('pointerenter',open);hit.addEventListener('pointerleave',close);
     title?.addEventListener('pointerenter',open);title?.addEventListener('pointerleave',close);
   }else{
     hit.addEventListener('pointerdown',e=>{e.preventDefault();open()},{passive:false});
     hit.addEventListener('pointerup',e=>{e.preventDefault();const href=window.FOND_BOOKS?.[key];setTimeout(()=>{pair.classList.remove('is-open');title?.classList.remove('is-open');if(href)location.href=href},820)},{passive:false});
     title?.addEventListener('pointerdown',e=>{e.preventDefault();open()},{passive:false});
     title?.addEventListener('pointerup',e=>{e.preventDefault();const href=window.FOND_BOOKS?.[key];setTimeout(()=>{pair.classList.remove('is-open');title?.classList.remove('is-open');if(href)location.href=href},820)},{passive:false});
   }
   hit.addEventListener('pointercancel',close);title?.addEventListener('pointercancel',close);
   hit.addEventListener('focus',open);hit.addEventListener('blur',close);title?.addEventListener('focus',open);title?.addEventListener('blur',close);
   if(canHover)hit.addEventListener('click',()=>{const href=window.FOND_BOOKS?.[key];if(href)location.href=href});
   hit.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();open();const href=window.FOND_BOOKS?.[key];setTimeout(()=>{pair.classList.remove('is-open');title?.classList.remove('is-open');if(href)location.href=href},reduce?30:820)}});
 });
 requestAnimationFrame(placeTitlesBelowNumerals);
}
window.addEventListener('fond:numerals-ready',bindFondNumerals);
window.addEventListener('resize',()=>requestAnimationFrame(placeTitlesBelowNumerals));
bindFondNumerals();