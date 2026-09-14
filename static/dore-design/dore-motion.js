(()=>{
  const REDUCED='(prefers-reduced-motion: reduce)';
  const SEMANTICS=new Set(['stillness','ceremonial-reveal','threshold-opening','architectural-assembly','quiet-dissolve','measured-drift','editorial-cut','weighted-convergence','page-turn-continuity','kinetic-typography']);
  const reduced=()=>window.matchMedia&&window.matchMedia(REDUCED).matches;
  const visible=(el)=>{el.style.opacity='1';el.style.transform='none';el.style.clipPath='none';};
  const keyframes={
    'ceremonial-reveal':[{opacity:0,transform:'translateY(18px)'},{opacity:1,transform:'translateY(0)'}],
    'threshold-opening':[{opacity:.15,clipPath:'inset(0 12% 0 12%)',transform:'scale(.985)'},{opacity:1,clipPath:'inset(0 0 0 0)',transform:'scale(1)'}],
    'architectural-assembly':[{opacity:.3,transform:'translateY(14px) scale(.985)'},{opacity:1,transform:'translateY(0) scale(1)'}],
    'quiet-dissolve':[{opacity:0},{opacity:1}],
    'measured-drift':[{opacity:.72,transform:'translateY(10px)'},{opacity:1,transform:'translateY(0)'}],
    'editorial-cut':[{opacity:0,transform:'translateX(-10px)'},{opacity:1,transform:'translateX(0)'}],
    'weighted-convergence':[{opacity:.35,transform:'scale(.97)'},{opacity:1,transform:'scale(1)'}],
    'page-turn-continuity':[{opacity:.35,transform:'translateX(12px)'},{opacity:1,transform:'translateX(0)'}],
    'kinetic-typography':[{opacity:0,letterSpacing:'.06em',transform:'translateY(.18em)'},{opacity:1,letterSpacing:'inherit',transform:'translateY(0)'}]
  };
  function animate(el,intent){
    if(intent==='stillness'||reduced()||!el.animate){visible(el);return {engine:'stillness',intent};}
    const frames=keyframes[intent];
    if(!frames){visible(el);return {engine:'stillness',intent:'stillness'};}
    const duration=Number(el.dataset.doreMotionDuration||720);
    const delay=Number(el.dataset.doreMotionDelay||0);
    el.animate(frames,{duration,delay,easing:'cubic-bezier(.2,.7,.2,1)',fill:'both'});
    return {engine:'web-animations-api',intent};
  }
  function mount(root=document){
    const nodes=[...root.querySelectorAll('[data-dore-motion]')];
    const observer=('IntersectionObserver' in window)&&!reduced()?new IntersectionObserver(entries=>{
      for(const entry of entries){if(!entry.isIntersecting)continue;const el=entry.target;observer.unobserve(el);el.__doreMotion=animate(el,el.dataset.doreMotion);}
    },{threshold:.12,rootMargin:'0px 0px -5% 0px'}):null;
    for(const el of nodes){
      const intent=SEMANTICS.has(el.dataset.doreMotion)?el.dataset.doreMotion:'stillness';
      el.dataset.doreMotion=intent;
      if(intent==='stillness'||!observer){el.__doreMotion=animate(el,intent);}else observer.observe(el);
    }
    document.documentElement.dataset.doreMotionRouter='native-first-v0';
    document.documentElement.dataset.doreReducedMotion=reduced()?'true':'false';
    return {count:nodes.length,reduced:reduced(),enginePolicy:'native-first'};
  }
  window.DoreMotion={semantics:SEMANTICS,mount,animate,reducedMotion:reduced};
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',()=>mount());else mount();
})();
