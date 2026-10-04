/* Dawn Interaction Layer — scroll, pointer and reading progress participate in Sites surfaces. */
(()=>{"use strict";
const root=document.documentElement;
if(!document.body||!document.body.matches(".sites-home-isolated,.sites-surface"))return;
const reduced=matchMedia("(prefers-reduced-motion: reduce)").matches;
let ticking=false;
const updateScroll=()=>{
  const max=Math.max(1,document.documentElement.scrollHeight-innerHeight);
  const p=Math.min(1,Math.max(0,scrollY/max));
  root.style.setProperty("--dawn-read-progress",p.toFixed(4));
  root.style.setProperty("--dawn-scroll-y",String(scrollY)+"px");
  ticking=false;
};
const requestScroll=()=>{if(!ticking){ticking=true;requestAnimationFrame(updateScroll)}};
updateScroll();addEventListener("scroll",requestScroll,{passive:true});addEventListener("resize",requestScroll,{passive:true});
if(!reduced&&matchMedia("(pointer:fine)").matches){
  let px=.5,py=.5,raf=0;
  const paint=()=>{root.style.setProperty("--dawn-pointer-x",px.toFixed(4));root.style.setProperty("--dawn-pointer-y",py.toFixed(4));raf=0};
  addEventListener("pointermove",e=>{px=e.clientX/innerWidth;py=e.clientY/innerHeight;if(!raf)raf=requestAnimationFrame(paint)},{passive:true});
}
const sections=[...document.querySelectorAll("main > section, main > article, .sites-home-water,.sites-home-gather,.sites-home-city,.sites-home-closing")];
if("IntersectionObserver"in window){
  const io=new IntersectionObserver(entries=>entries.forEach(e=>{if(e.isIntersecting){sections.forEach(s=>s.removeAttribute("data-dawn-active"));e.target.setAttribute("data-dawn-active","")}}),{rootMargin:"-38% 0px -38% 0px",threshold:0});
  sections.forEach(s=>io.observe(s));
}
})();