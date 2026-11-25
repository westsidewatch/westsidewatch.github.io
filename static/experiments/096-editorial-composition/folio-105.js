(()=>{if(!document.documentElement.classList.contains('art105'))return;
const mail=document.querySelector('.folio-contact-primary a');if(mail)mail.lang='en';
const rail=document.querySelector('#church-gathering-list');const update=()=>{const days=[...rail.querySelectorAll('.folio-week-day')];if(days.length!==7||rail.dataset.r105==='1')return;rail.dataset.r105='1';const names=['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];days.forEach((e,i)=>{e.textContent=names[i]});};
new MutationObserver(update).observe(rail,{childList:true,subtree:true});update();
})();