/* P2 church growth runs as a real, looping 3D animation inside the iframe.
   Do not override it with the fixed churchPreview scroll position.
   Keep the surrounding P2 water/magazine choreography untouched. */
(() => {
  'use strict';
  const stage=document.querySelector('.showcase');
  const frame=document.querySelector('.church-editorial__maquette');
  if(!stage||!frame)return;
  let loaded=Boolean(frame.getAttribute('src'));
  let active=false;
  function prime(){
    if(loaded||!frame.dataset.src)return;
    loaded=true;
    frame.src=frame.dataset.src;
    delete frame.dataset.src;
  }
  function replay(){
    if(!loaded||!frame.contentWindow)return;
    frame.contentWindow.postMessage({type:'P2_CHURCH_BUILD_REPLAY'},location.origin);
  }
  frame.addEventListener('load',()=>{if(active)replay()});
  window.addEventListener('message',e=>{
    if(e.origin!==location.origin||e.source!==frame.contentWindow)return;
    if(e.data?.type==='P2_CHURCH_GEOMETRY_READY'){
      frame.parentElement?.classList.add('maquette-geometry-ready');
      if(active)replay();
    }
  });
  function sync(){
    const pose=Number(stage.dataset.p2Progress||0);
    if(pose>=1.64&&pose<3.15)prime();
    const next=pose>=1.72&&pose<2.85;
    stage.classList.toggle('p2-church-model-visible',next);
    frame.style.visibility=next?'visible':'hidden';
    if(next&&!active){prime();replay()}
    active=next;
  }
  new MutationObserver(sync).observe(stage,{
    attributes:true,attributeFilter:['data-p2-progress']
  });
  sync();
})();
