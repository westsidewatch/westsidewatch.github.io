(() => {
 if(!('IntersectionObserver' in window)||matchMedia('(prefers-reduced-motion: reduce)').matches)return;
 const observer=new IntersectionObserver(entries=>entries.forEach(entry=>{if(entry.isIntersecting){entry.target.classList.remove('publication-entering');observer.unobserve(entry.target)}}),{threshold:.08});
 document.querySelectorAll('.section-head,.editorial-lead,.dawn-head,.library-index,.focus-hero').forEach(el=>{el.dataset.publicationReveal='';el.classList.add('publication-entering');observer.observe(el)});
})();
