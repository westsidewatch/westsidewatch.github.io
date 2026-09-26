const threshold=document.querySelector('#threshold');
const enter=document.querySelector('#enterFond');
const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
function openFond(){if(!threshold||threshold.classList.contains('opening'))return;threshold.classList.add('opening');const delay=reduce?30:1480;setTimeout(()=>{threshold.classList.add('gone');document.body.classList.remove('threshold-locked')},delay)}
enter?.addEventListener('click',openFond);

function bindFondNumerals(){
 const book=document.querySelector('#fondNumerals'); if(!book||book.dataset.bound==='1')return;
 book.dataset.bound='1';
 const ns='http://www.w3.org/2000/svg';
 const pairs=[...book.querySelectorAll('.pair')];
 pairs.forEach(pair=>{
   const key=pair.dataset.book;
   pair.style.pointerEvents='none';
   const box=pair.getBBox();
   const hit=document.createElementNS(ns,'rect');
   hit.setAttribute('x',String(box.x));hit.setAttribute('y',String(box.y));hit.setAttribute('width',String(box.width));hit.setAttribute('height',String(box.height));
   hit.setAttribute('fill','transparent');hit.setAttribute('pointer-events','all');hit.setAttribute('tabindex','0');hit.setAttribute('role','link');hit.dataset.book=key;hit.classList.add('pair-hit');
   pair.parentNode.insertBefore(hit,pair.nextSibling);
   const on=()=>pair.classList.add('is-open');
   const off=()=>pair.classList.remove('is-open');
   hit.addEventListener('pointerenter',on);hit.addEventListener('pointerleave',off);hit.addEventListener('pointercancel',off);
   hit.addEventListener('focus',on);hit.addEventListener('blur',off);
   hit.addEventListener('click',()=>{const href=window.FOND_BOOKS?.[key];if(href)location.href=href});
   hit.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();hit.click()}});
 });
}
window.addEventListener('fond:numerals-ready',bindFondNumerals);
bindFondNumerals();