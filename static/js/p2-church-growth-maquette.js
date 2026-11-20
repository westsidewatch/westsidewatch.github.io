/* Silent architectural growth beside the actual Sunday programme.
   The Magazine bridge overwrites data-p2-phase, so observe the canonical
   scroll-owned data-p2-progress instead. Do not modify the P2 choreography. */
(() => {
 const stage=document.querySelector('.showcase');
 const frame=document.querySelector('.church-editorial__maquette');
 if(!stage||!frame)return;
 let loaded=Boolean(frame.getAttribute('src'));
 let active=false;

 function prime(){
  if(loaded||!frame.dataset.src)return;
  const url=frame.dataset.src;
  loaded=true;
  frame.src=url;
  delete frame.dataset.src;
 }
 function replay(){
  if(loaded&&frame.contentWindow){
   frame.contentWindow.postMessage({type:'P2_CHURCH_BUILD_REPLAY'},location.origin);
  }
 }
 frame.addEventListener('load',()=>{if(active)replay()});
 // Hide the paper maquette placeholder only when the real GLB has arrived.
 window.addEventListener('message',e=>{
  if(e.origin!==location.origin||e.source!==frame.contentWindow)return;
  if(e.data?.type==='P2_CHURCH_GEOMETRY_READY'){
   frame.parentElement?.classList.add('maquette-geometry-ready');
  }
 });

 function sync(){
  const pose=Number(stage.dataset.p2Progress||0);
  // Begin fetching during the original two-door entry; never wait for the
  // phase label, because the Magazine bridge can replace that label.
  if(pose>=1.64&&pose<3.15)prime();
  const nowActive=pose>=1.72&&pose<2.85;
  stage.classList.toggle('p2-church-model-visible',nowActive);
  frame.style.visibility=nowActive?'visible':'hidden';
  if(nowActive&&!active){prime();replay()}
  active=nowActive;
 }
 new MutationObserver(sync).observe(stage,{
  attributes:true,attributeFilter:['data-p2-progress']
 });
 sync();
})();
