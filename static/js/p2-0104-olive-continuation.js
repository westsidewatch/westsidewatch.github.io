/* P2 / 04 Olive Mountain — isolated continuation of the LIVE 01–03.
 * Source of truth: docs/MASTER_SITE_ARCHITECTURE.md §§11–12;
 * 03→04 preserves the original book-frame geometry, but unlike the rejected
 * generic full-page right-to-left wipe it follows the TWO design contracts:
 * FIRST-LOOK-MOTION-CONTRACT: immersive horizontal 12-speaker corridor.
 * MASTER_SITE_ARCHITECTURE §12: upper/lower editorial portrait+viewer split.
 * One scroll value drives the upper manuscript curtain and the lower
 * horizontal gallery; source 01–03 never moves or changes size.
 */
(()=>{'use strict';
 const $=s=>document.querySelector(s),stage=$('#p2-olive-stage'),track=$('#p2-olive-track');
 const base=$('#p2-0103-original'),olive=$('#olive-proof'),surround=$('#p2-olive-surround');
 const slider=$('#p2-olive-seek'),output=$('#p2-olive-progress'),folio=$('#p2-olive-folio-status');
 if(!stage||!track||!base||!olive||!surround)return;
 const clamp=(v,a=0,b=1)=>Math.min(b,Math.max(a,v));
 const smooth=v=>{const x=clamp(v);return x*x*(3-2*x)};
 const roster=[
  ['watchman-nee','倪柝聲','WATCHMAN NEE'],['derek-prince','葉光明','DEREK PRINCE'],
  ['david-pawson','大衛鮑森','DAVID PAWSON'],['stephen-tong','唐崇榮','STEPHEN TONG'],
  ['huang-shuhua','黃淑華','HUANG SHUHUA'],['kang-lai-chang','康來昌','KANG LAI-CHANG'],
  ['jerry-lai','賴若瀚','JERRY LAI'],['tong-liu','劉彤','TONG LIU'],
  ['jiang-xiuqin','江秀琴','GRACE CHIANG'],['rick-warren','華理克','RICK WARREN'],
  ['yu-hong-jie','于宏潔','YU HONGJIE'],['kou-shao-en','寇紹恩','KOU SHAO-EN']
 ];
 const names=$('#olive-speaker-names'),mainImg=$('#olive-main-image'),nextImg=$('#olive-next-image');
 const main=$('#olive-main'),upper=$('.olive-proof__top'),lower=$('.olive-proof__bottom');
 function chooseSpeaker(i){
  const [slug,zh,en]=roster[i],next=roster[(i+1)%roster.length];
  mainImg.src='/images/olive/'+slug+'-editorial.png';
  mainImg.alt=zh;
  const old=main.querySelector('olive-speaker-baseline');old?.remove();
  const component=document.createElement('olive-speaker-baseline');
  component.dataset.speaker=slug;component.setAttribute('aria-hidden','true');
  main.append(component);
  nextImg.src='/images/olive/'+next[0]+'-editorial.png';nextImg.alt=next[1];
  $('#olive-next-name').textContent=next[2]+' · '+next[1];
  names.querySelectorAll('button').forEach((b,j)=>b.setAttribute('aria-pressed',String(i===j)));
  olive.dataset.speaker=slug;
 }
 roster.forEach(([slug,zh,en],i)=>{
  const b=document.createElement('button');b.type='button';b.dataset.speaker=slug;
  b.setAttribute('aria-label','選擇講員 '+zh);
  const img=document.createElement('img');
  img.src='/images/olive/'+slug+'-editorial.png';img.alt='';
  img.loading=i<6?'eager':'lazy';img.decoding='async';
  const label=document.createElement('span');label.textContent=en;
  const sm=document.createElement('small');sm.textContent=zh;
  b.append(img,label,sm);
  b.addEventListener('click',()=>chooseSpeaker(i));names.append(b);
 });
 chooseSpeaker(0);
 let lastFolio=null,queued=false,frameReady=false;
 function legacyProgress(d){
  const churchEnd=3.0775,magazineEnd=6.5,dist=Math.min(d,magazineEnd);
  if(dist<=churchEnd){
   const scene=dist<=1.8?.1+dist*(.4/1.8):.5+(dist-1.8);
   return clamp(scene/2.9);
  }
  const vh=2.37+(dist-churchEnd)/(magazineEnd-churchEnd)*(4-2.37);
  return clamp(vh<=2.9?.75*vh/2.9:.75+.25*(vh-2.9)/1.1);
 }
 function measureFolio(){
  const doc=base.contentDocument;
  const left=doc?.querySelector('#emmaus .emmaus__left');
  const right=doc?.querySelector('#emmaus .emmaus__right');
  if(!left||!right)return lastFolio;
  const a=left.getBoundingClientRect(),b=right.getBoundingClientRect();
  const stageRect=stage.getBoundingClientRect(),baseRect=base.getBoundingClientRect();
  if(a.width<25||a.height<25||b.width<25||b.height<25)return lastFolio;
  // Read the actually-composited approved ONE+gallery, not the old Draft's
  // hardcoded 5:8 cover. The parent and child use the same viewport axes.
  const x=Math.min(a.left,b.left)+baseRect.left-stageRect.left;
  const y=Math.min(a.top,b.top)+baseRect.top-stageRect.top;
  const w=Math.max(a.right,b.right)-Math.min(a.left,b.left);
  const h=Math.max(a.bottom,b.bottom)-Math.min(a.top,b.top);
  if(x<0||y<0||x+w>stageRect.width+3||y+h>stageRect.height+3)return lastFolio;
  const box={x,y,w,h};
  lastFolio=box;return box;
 }
 function paint(){
  queued=false;
  const h=Math.max(1,innerHeight),d=clamp(-track.getBoundingClientRect().top/h,0,11.34);
  const progress=clamp((d-9.44)/1.38);
  // Unlike a generic page wipe: the upper portrait/editorial *opens down*
  // into the existing folio; then the lower 12-speaker corridor advances
  // sideways beneath it. Both curves come from one reversible scroll clock.
  const upperOpen=smooth(progress/.68);
  const corridorOpen=smooth((progress-.35)/.65);
  const childD=Math.min(d,9.34);
  if(base.contentWindow)base.contentWindow.postMessage({
   type:'westside-p2-home-pose',distance:childD,
   legacyProgress:legacyProgress(childD),active:true
  },location.origin);
  const frame=measureFolio();
  if(frame){
   const n=v=>v.toFixed(2)+'px';
   Object.assign(olive.style,{left:n(frame.x),top:n(frame.y),width:n(frame.w),height:n(frame.h)});
   const w=stage.clientWidth,h2=stage.clientHeight;
   const a=frame.x,b=frame.y,c=frame.x+frame.w,e=frame.y+frame.h;
   const path='path("M 0 0 H '+w+' V '+h2+' H 0 Z M '+
    a.toFixed(2)+' '+b.toFixed(2)+' V '+e.toFixed(2)+
    ' H '+c.toFixed(2)+' V '+b.toFixed(2)+' Z")';
   surround.style.clipPath=path;
  }
  olive.style.visibility=progress>.0001?'visible':'hidden';
  olive.style.opacity='1';
  // Absolutely no single clip on the complete 04 page: the distinctive
  // upper/lower composition IS the entry animation.
  olive.style.clipPath='none';
  upper.style.clipPath=upperOpen>.99999?'none':
   'inset(0 0 '+((1-upperOpen)*100).toFixed(3)+'% 0)';
  lower.style.clipPath=corridorOpen>.99999?'none':
   'inset(0 0 0 '+((1-corridorOpen)*100).toFixed(3)+'%)';
  olive.dataset.reveal=progress.toFixed(5);
  olive.dataset.upperOpen=upperOpen.toFixed(5);
  olive.dataset.corridorOpen=corridorOpen.toFixed(5);
  olive.style.pointerEvents=progress>.999?'auto':'none';
  olive.inert=progress<.999;
  olive.setAttribute('aria-hidden',progress>.999?'false':'true');
  // On entering, the lower folio acts as an actual horizontal speaker
  // corridor. Once settled, leave native horizontal swipe / keyboard
  // and click navigation alone (do not reset scrollLeft each paint).
  if(corridorOpen<.99999){
   const distance=Math.min(names.scrollWidth-names.clientWidth,names.clientWidth*.70);
   names.scrollLeft=Math.max(0,distance*corridorOpen);
  }
  surround.style.opacity=progress.toFixed(5);
  stage.dataset.p2Distance=d.toFixed(4);
  stage.dataset.p2OliveIn=progress.toFixed(5);
  stage.dataset.p2OliveUpper=upperOpen.toFixed(5);
  stage.dataset.p2OliveCorridor=corridorOpen.toFixed(5);
  stage.dataset.p2FolioReady=frame?'true':'false';
  stage.dataset.p2Composition='portrait-down-corridor-horizontal';
  output.textContent=d.toFixed(2);
  slider.value=String(d);
  folio.textContent=d<9.44?'03 / 07 · EMMAUS':progress>.999?
   '04 / 07 · OLIVE MOUNTAIN':'03 → 04 · SPEAKER CORRIDOR';
 }
 function schedule(){if(!queued){queued=true;requestAnimationFrame(paint)}}
 function go(d){
  const at=track.getBoundingClientRect().top+scrollY+clamp(d,0,11.34)*Math.max(1,innerHeight);
  scrollTo({top:at,behavior:'instant'});schedule();
 }
 document.querySelectorAll('[data-seek]').forEach(button=>
  button.addEventListener('click',()=>go(Number(button.dataset.seek))));
 slider.addEventListener('input',()=>go(Number(slider.value)));
 base.addEventListener('load',()=>{frameReady=true;schedule();});
 addEventListener('message',event=>{
  if(event.origin===location.origin&&event.source===base.contentWindow)requestAnimationFrame(schedule);
 });
 addEventListener('scroll',schedule,{passive:true});
 addEventListener('resize',()=>{lastFolio=null;schedule()},{passive:true});
 // Deep links are acceptance probes only; the default opens at the end
 // of the approved 03 reading, ready to scroll forward into 04.
 const q=new URLSearchParams(location.search),initial=Number(q.get('d')??9.30);
 requestAnimationFrame(()=>requestAnimationFrame(()=>go(Number.isFinite(initial)?initial:9.30)));
})();
