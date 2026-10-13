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
const sections=[...document.querySelectorAll("main > section, main > article, .sites-home-realm, .sites-home-closing")];
const focusScreens=[...document.querySelectorAll(".candidate-focus-screen")];
/* Homepage scene coordinator: one normalized timeline for the existing hero and two film screens. */
const homeHero=document.querySelector("body.home .sites-home-hero");
const homeScenes=homeHero?[homeHero,...focusScreens]:[];
let sceneTick=false;
const clamp01=v=>Math.max(0,Math.min(1,v));
const sceneFrames=focusScreens.map(scene=>scene.querySelector("iframe"));
const sendSceneState=(frame,payload)=>{
  if(!frame||!frame.contentWindow)return;
  try{frame.contentWindow.postMessage(payload,location.origin)}catch(_){}
};
sceneFrames.forEach((frame,i)=>{
  if(frame)frame.addEventListener("load",()=>{
    const scene=focusScreens[i];
    const progress=Number(scene.style.getPropertyValue("--home-scene-progress"))||0;
    sendSceneState(frame,{type:"westside-scene",scene:i+2,progress,phase:scene.dataset.scenePhase||"upcoming",reducedMotion:reduced});
  });
});
const updateHomeSequence=()=>{
  sceneTick=false;
  if(!homeScenes.length)return;
  const center=innerHeight*.5;
  const viewportHeight=Math.max(1,innerHeight);
  let nearest=0, distance=Infinity;
  homeScenes.forEach((scene,i)=>{
    const r=scene.getBoundingClientRect();
    const d=Math.abs((r.top+r.bottom)/2-center);
    if(d<distance){distance=d;nearest=i}
    const progress=clamp01((viewportHeight-r.top)/Math.max(1,r.height+viewportHeight));
    scene.style.setProperty("--home-scene-progress",progress.toFixed(4));
    scene.dataset.scenePhase=r.top>center?"upcoming":r.bottom<center?"passed":"active";
    if(i>0&&r.bottom>0&&r.top<innerHeight){
      sendSceneState(sceneFrames[i-1],{type:"westside-scene",scene:i+1,progress,phase:scene.dataset.scenePhase,reducedMotion:reduced});
    }
  });
  document.body.dataset.homeScene=String(nearest+1);
  // Publish the current chapter to the host without trapping native scroll.
  root.style.setProperty("--home-chapter-index",String(nearest+1));
  const heroRect=homeHero.getBoundingClientRect();
  const exit=clamp01(-heroRect.top/Math.max(1,heroRect.height*.75));
  homeHero.style.setProperty("--home-hero-exit",exit.toFixed(4));
  focusScreens.forEach((scene,i)=>{
    const r=scene.getBoundingClientRect();
    const enter=clamp01((viewportHeight-r.top)/Math.max(1,viewportHeight*.65));
    const leave=clamp01(-r.top/Math.max(1,r.height*.8));
    scene.style.setProperty("--home-chapter-enter",enter.toFixed(4));
    scene.style.setProperty("--home-chapter-leave",leave.toFixed(4));
    scene.toggleAttribute("data-chapter-current",nearest===i+1);
  });
};
const requestHomeSequence=()=>{if(!sceneTick){sceneTick=true;requestAnimationFrame(updateHomeSequence)}};
if(homeScenes.length){
  updateHomeSequence();
  addEventListener("scroll",requestHomeSequence,{passive:true});
  addEventListener("resize",requestHomeSequence,{passive:true});
}

const realms=[...document.querySelectorAll(".sites-home-realm")];
if(!reduced&&"IntersectionObserver"in window){
  const motionIO=new IntersectionObserver(entries=>entries.forEach(e=>{
    e.target.toggleAttribute("data-motion-live",e.isIntersecting);
    const frame=e.target.querySelector("iframe");
    if(frame&&frame.contentWindow)sendSceneState(frame,{type:"westside-motion",active:e.isIntersecting});
  }),{rootMargin:"12% 0px 12% 0px",threshold:.08});
  focusScreens.forEach(s=>motionIO.observe(s));
  const realmIO=new IntersectionObserver(entries=>entries.forEach(e=>e.target.toggleAttribute("data-motion-live",e.isIntersecting)),{rootMargin:"8% 0px 8% 0px",threshold:.08});
  realms.forEach(s=>realmIO.observe(s));
}
if("IntersectionObserver"in window){
  const io=new IntersectionObserver(entries=>entries.forEach(e=>{if(e.isIntersecting){sections.forEach(s=>s.removeAttribute("data-dawn-active"));e.target.setAttribute("data-dawn-active","")}}),{rootMargin:"-38% 0px -38% 0px",threshold:0});
  sections.forEach(s=>io.observe(s));
}
})();