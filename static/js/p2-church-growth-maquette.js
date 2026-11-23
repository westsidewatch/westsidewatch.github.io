/* P2 01 — true scroll-controlled architectural construction.
 * Red Sea first: water opens 1.72–2.37. After a short, legible pause,
 * the ORIGINAL 3D building begins construction at 2.41 and reaches full
 * height by 3.22. The approved magazine handoff still starts at 3.36.
 * No timer, replay, static model substitute or second animation clock.
 * Scrolling backward reverses the same real geometric growth. */
(() => {
 'use strict';
 const stage=document.querySelector('.showcase');
 const frame=document.querySelector('.church-editorial__maquette');
 if(!stage||!frame)return;
 let loaded=Boolean(frame.getAttribute('src')),lastSent=NaN,ready=false;
 const clamp=v=>Math.min(1,Math.max(0,v));
 function progress(){
  return clamp(Number(stage.dataset.p2ChurchGrowth)||0);
 }
 function prime(){
  if(loaded||!frame.dataset.src)return;
  loaded=true;
  frame.src=frame.dataset.src;
  delete frame.dataset.src;
 }
 function send(force=false){
  if(!loaded||!frame.contentWindow)return;
  const value=progress();
  if(!force&&Number.isFinite(lastSent)&&Math.abs(value-lastSent)<.002)return;
  lastSent=value;
  frame.contentWindow.postMessage({
   type:'P2_CHURCH_BUILD_PROGRESS',progress:value
  },location.origin);
 }
 frame.addEventListener('load',()=>{
  lastSent=NaN;
  send(true);
 });
 window.addEventListener('message',e=>{
  if(e.origin!==location.origin||e.source!==frame.contentWindow)return;
  if(e.data?.type==='P2_CHURCH_GEOMETRY_READY'){
   ready=true;
   frame.parentElement?.classList.add('maquette-geometry-ready');
   send(true);
  }else if(e.data?.type==='P2_CHURCH_BUILD_READY'){
   ready=true;
   send(true);
  }
 });
 function sync(){
  const pose=Number(stage.dataset.p2Progress||0);
  if(pose>=1.42&&pose<5.19)prime();
  // Until 2.41 the church pane and Red Sea may be visible, but no
  // building is allowed to appear before the opening has completed.
  const active=pose>=2.41&&pose<5.19;
  stage.classList.toggle('p2-church-model-visible',active);
  frame.style.visibility=active?'visible':'hidden';
  send();
 }
 new MutationObserver(sync).observe(stage,{
  attributes:true,attributeFilter:['data-p2-progress']
 });
 sync();
})();
