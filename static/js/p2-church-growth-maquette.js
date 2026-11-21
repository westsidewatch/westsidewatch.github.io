/* One P2 scroll clock owns architectural growth.
   The completed church view holds the whole model; reversing the P2 scroll
   reverses construction. Page transitions and Sunday copy are unchanged. */
(() => {
 'use strict';
 const stage=document.querySelector('.showcase');
 const frame=document.querySelector('.church-editorial__maquette');
 if(!stage||!frame)return;
 const reduced=window.matchMedia('(prefers-reduced-motion: reduce)');
 let loaded=Boolean(frame.getAttribute('src')),active=false,lastProgress=null;
 const clamp=v=>Math.min(1,Math.max(0,v));
 function constructionProgress(){
  if(reduced.matches)return 1;
  const pose=Number(stage.dataset.p2Progress||0);
  const x=clamp((pose-1.72)/.60);
  return x*x*(3-2*x);
 }
 function prime(){
  if(loaded||!frame.dataset.src)return;
  loaded=true;
  frame.src=frame.dataset.src;
  delete frame.dataset.src;
 }
 function sendProgress(force=false){
  if(!loaded||!frame.contentWindow)return;
  const progress=constructionProgress();
  if(!force&&lastProgress!==null&&Math.abs(progress-lastProgress)<.006)return;
  lastProgress=progress;
  frame.contentWindow.postMessage({type:'P2_CHURCH_BUILD_PROGRESS',progress},location.origin);
 }
 frame.addEventListener('load',()=>{lastProgress=null;sendProgress(true)});
 window.addEventListener('message',e=>{
  if(e.origin!==location.origin||e.source!==frame.contentWindow)return;
  if(e.data?.type==='P2_CHURCH_GEOMETRY_READY'){
   frame.parentElement?.classList.add('maquette-geometry-ready');
   sendProgress(true);
  }else if(e.data?.type==='P2_CHURCH_BUILD_READY')sendProgress(true);
 });
 function sync(){
  const pose=Number(stage.dataset.p2Progress||0);
  if(pose>=1.64&&pose<3.15)prime();
  const nowActive=pose>=1.72&&pose<2.85;
  stage.classList.toggle('p2-church-model-visible',nowActive);
  frame.style.visibility=nowActive?'visible':'hidden';
  if(nowActive){if(!active)prime();sendProgress(!active)}
  active=nowActive;
 }
 new MutationObserver(sync).observe(stage,{
  attributes:true,attributeFilter:['data-p2-progress']
 });
 reduced.addEventListener?.('change',()=>sendProgress(true));
 sync();
})();
