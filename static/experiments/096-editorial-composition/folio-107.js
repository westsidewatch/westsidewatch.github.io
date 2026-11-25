(()=>{if(!document.documentElement.classList.contains('art107'))return;
const list=document.querySelector('#church-gathering-list');
const order=['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
const bind=()=>{const entries=[...list.querySelectorAll('article')];const labels=[...list.querySelectorAll('.folio-week-day')];if(entries.length!==4||labels.length!==7||list.dataset.r107==='1'||entries.some(e=>!e.querySelector('.folio-day-en')))return;
const pairs=entries.map(e=>({e,day:e.querySelector('.folio-day-en').textContent.trim()})).map(x=>({...x,n:order.indexOf(x.day)+1})).sort((a,b)=>a.n-b.n);if(pairs.some(x=>x.n<1)||new Set(pairs.map(x=>x.n)).size!==entries.length)return;
list.dataset.r107='1';pairs.forEach((x,i)=>{const span=Math.min(2,(pairs[i+1]?.n||8)-x.n);x.e.style.setProperty('--day-start',String(x.n));x.e.style.setProperty('--day-span',String(span));x.e.dataset.weekday=x.day;labels[x.n-1].dataset.active='1';});};
new MutationObserver(bind).observe(list,{childList:true,subtree:true});bind();
})();