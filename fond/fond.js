const threshold=document.querySelector('#threshold');
const enter=document.querySelector('#enterFond');
const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
function openFond(){if(!threshold||threshold.classList.contains('opening'))return;threshold.classList.add('opening');const delay=reduce?30:1480;setTimeout(()=>{threshold.classList.add('gone');document.body.classList.remove('threshold-locked')},delay)}
enter?.addEventListener('click',openFond);

const numberBook=document.querySelector('.number-book');
const pages=[...document.querySelectorAll('.number-page')];
if(numberBook&&pages.length){
  const setActive=page=>{
    pages.forEach(p=>p.classList.toggle('is-near',p===page));
    numberBook.classList.toggle('has-near',!!page);
  };
  pages.forEach(page=>{
    page.addEventListener('pointerenter',()=>setActive(page));
    page.addEventListener('pointerleave',()=>setActive(null));
    page.addEventListener('focus',()=>setActive(page));
    page.addEventListener('blur',()=>setActive(null));
    page.addEventListener('click',event=>{
      if(reduce)return;
      event.preventDefault();
      if(numberBook.classList.contains('is-opening'))return;
      numberBook.classList.add('is-opening');
      page.classList.add('is-opening');
      const href=page.href;
      setTimeout(()=>{window.location.href=href},720);
    });
  });
}
