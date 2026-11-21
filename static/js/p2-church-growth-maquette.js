/* P2 01 — true scroll-controlled architectural construction.
 * The SAME P2 viewport progress used for the Red Sea doors controls the
 * original 3D model. No countdown, replay loop, static substitute or timer.
 * The model starts before the central paper fully opens and stays complete
 * until the magazine is allowed to enter. Reverse scrolling reverses growth. */
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
  const active=pose>=1.72&&pose<5.19;
  stage.classList.toggle('p2-church-model-visible',active);
  frame.style.visibility=active?'visible':'hidden';
  send();
 }
 new MutationObserver(sync).observe(stage,{
  attributes:true,attributeFilter:['data-p2-progress']
 });
 sync();
})();
