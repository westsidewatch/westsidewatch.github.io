const threshold=document.querySelector('#threshold');
const enter=document.querySelector('#enterFond');
const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
function openFond(){if(!threshold||threshold.classList.contains('opening'))return;threshold.classList.add('opening');const delay=reduce?30:1480;setTimeout(()=>{threshold.classList.add('gone');document.body.classList.remove('threshold-locked')},delay)}
enter?.addEventListener('click',openFond);

function bindFondNumerals(){
 const book=document.querySelector('#fondNumerals'); if(!book)return;
 book.querySelectorAll('.pair').forEach(pair=>{
   const key=pair.dataset.book;
   pair.setAttribute('tabindex','0');
   pair.setAttribute('role','link');
   const on=()=>pair.classList.add('is-open');
   const off=()=>pair.classList.remove('is-open');
   pair.addEventListener('pointerenter',on); pair.addEventListener('pointerleave',off); pair.addEventListener('pointercancel',off);
   pair.addEventListener('focus',on); pair.addEventListener('blur',off);
   pair.addEventListener('click',()=>{const href=window.FOND_BOOKS?.[key];if(href)location.href=href});
   pair.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();pair.dispatchEvent(new MouseEvent('click'))}});
 });
}
window.addEventListener('fond:numerals-ready',bindFondNumerals);
bindFondNumerals();