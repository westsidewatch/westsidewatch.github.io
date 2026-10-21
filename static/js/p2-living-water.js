(()=>{'use strict';
const root=document.querySelector('.showcase'),planes=[...root.querySelectorAll('.plane')],wrap=root.querySelector('.planes'),scripture=root.querySelector('.editorial-john'),editions=[...root.querySelectorAll('.edition')],sea=root.querySelector('.ocean-rise'),cover=root.querySelector('.water-cover'),doors=root.querySelector('.water-doors'),leftDoor=root.querySelector('.water-door--left'),rightDoor=root.querySelector('.water-door--right'),church=root.querySelector('.church-editorial'),index=root.querySelector('.index'),tint=root.querySelector('.water-rise-tint'),waterline=root.querySelector('.water-rise-line path');
const clamp=(v,a,b)=>Math.min(b,Math.max(a,v)),smooth=v=>{v=clamp(v,0,1);return v*v*(3-2*v)};
// Same positional curve and stagger as the homepage navigation; no timed playback.
const magazineProof=new URLSearchParams(location.search).get('magazineProof')==='1';
// Proof-only handoff: Church finishes at 2.37 vh, then Magazine starts immediately.
// The production/non-proof mapping remains identical to its existing schedule.
const handoffVh=2.37,finalVh=3.85;
const handoffProgress=.75*handoffVh/2.9;
const embeddedScene=p=>magazineProof
 ? p<=handoffProgress?p/.75*2.9
   : handoffVh+(p-handoffProgress)/(1-handoffProgress)*(finalVh-handoffVh)
 : p<=.75?p/.75*2.9:2.9+(p-.75)/.25*1.1;
const foldEase=v=>v<.5?8*v**4:1-(-2*v+2)**4/2;
const embedded=document.documentElement.dataset.p2Embedded==='true',reduced=typeof matchMedia==='function'?matchMedia('(prefers-reduced-motion: reduce)'): {matches:false};
let raf=0,externalProgress=0,hasExternalProgress=embedded,displayVh=null,sceneVh=null,active=!embedded;
function render(now=performance.now()){
 raf=0;
 const distance=embedded?0:clamp(-root.getBoundingClientRect().top/Math.max(1,innerHeight),0,5.4);
 const target=hasExternalProgress?embeddedScene(externalProgress):distance<=1.8?.1+distance*(.4/1.8):.5+(distance-1.8);
 // Scroll position is the only choreography clock: no catch-up or timed easing.
 displayVh=target;
 const rect=embedded?null:root.getBoundingClientRect();
 const visible=document.visibilityState==='visible'&&(embedded?active:rect.bottom>0&&rect.top<innerHeight);
 if(!visible)displayVh=target;
 // One clock paints the original V75 geometry and every shared SVG view.
 if(visible)window.wsP2Water?.paint(now);
 if(displayVh!==sceneVh||(visible&&displayVh>.65&&displayVh<1.6)){
  drawScene(displayVh,now);sceneVh=displayVh;
 }
 root.dataset.p2Animating=String(visible&&!reduced.matches);
 if(visible&&!reduced.matches)schedule();
}
function drawScene(vh,now){
 const magazineStart=2.85,magazineEnd=3.85,magazineProgress=smooth((vh-magazineStart)/(magazineEnd-magazineStart));
 // Use the remapped progress solely in the isolated magazineProof path.
 const handoffMagazineProgress=magazineProof?clamp((vh-handoffVh)/(finalVh-handoffVh),0,1):magazineProgress;
 const magazine=root.querySelector('.p2-magazine');
 const reveal=clamp(vh/.5,0,1),rise=smooth((vh-.65)/.95),opening=smooth((vh-1.72)/.65),showChurch=vh>=1.72;
 const waterTop=(1-rise)*100,wave=[],coverWave=[],foldWave=[],line=[];
 for(let j=0;j<=64;j++){
  const x=j*100/64,ripple=(rise>0&&rise<1?Math.sin(Math.PI*rise):0)*(1.25*Math.sin(x*.18+now*.0011)+.5*Math.sin(x*.47-now*.0007)),y=clamp(waterTop+ripple,0,100);
  wave.push(x.toFixed(2)+'% '+y.toFixed(2)+'%');foldWave.push(x.toFixed(2)+'% '+Math.min(100,y*2).toFixed(2)+'%');coverWave.push(x.toFixed(2)+'% '+Math.min(50,y).toFixed(2)+'%');line.push((j?'L':'M')+x.toFixed(2)+' '+y.toFixed(2));
 }
 cover.style.clipPath=rise>=1?'inset(0 0 100% 0)':'polygon(0% 0%,100% 0%,'+coverWave.slice().reverse().join(',')+')';
 tint.style.clipPath=showChurch?'inset(0 50% 0 0)':'polygon('+wave.join(',')+',100% 100%,0% 100%)';
 tint.style.opacity=rise>0?'1':'0';
 waterline.setAttribute('d',line.join(' '));
 waterline.style.opacity=rise>0&&rise<1?'1':'0';
 sea.style.visibility='visible';sea.style.clipPath=showChurch?'inset(0 50% 0 0)':'none';sea.style.opacity='1';
 doors.style.visibility=showChurch?'visible':'hidden';leftDoor.style.transform='none';rightDoor.style.transform='translate3d('+(50*opening).toFixed(3)+'vw,0,0)';
 planes.forEach((el,i)=>{
  // Seven independent top-anchored curtains, staggered like the navigation.
  // Easing shapes the fold by position; it never continues after scroll stops.
  const phase=clamp((reveal*1.11-i*.065)/.72,0,1),opened=foldEase(phase);
  el.style.setProperty('transform','scale3d(1,'+opened.toFixed(6)+',1)');el.style.zIndex=String(i+1);el.style.visibility='visible';
 });
 // Keep the completed identity until the rising surface physically covers it.
 wrap.style.visibility=rise<1?'visible':'hidden';wrap.style.opacity='1';
 wrap.style.clipPath='polygon(0% 0%,100% 0%,'+foldWave.slice().reverse().join(',')+')';
 const scriptureOpacity=1-smooth((rise-.12)/.45);
 scripture.classList.toggle('is-current',scriptureOpacity>0);scripture.style.visibility=scriptureOpacity>0?'visible':'hidden';scripture.style.opacity=String(scriptureOpacity);scripture.setAttribute('aria-hidden',scriptureOpacity>0?'false':'true');
 for(const el of editions)if(el!==scripture){el.classList.remove('is-current');el.style.visibility='hidden';el.style.opacity='0'}
 church.style.visibility=showChurch?'visible':'hidden';church.style.opacity='1';root.style.setProperty('--p2-door-open',opening.toFixed(5));church.setAttribute('aria-hidden',showChurch?'false':'true');
 // The original P2 remains unchanged unless the explicit proof query is set.
 // The proof uses the same scroll-owned vh value: no second animation clock.
 if(magazineProof){
  if(window.wsP2MagazineProof)window.wsP2MagazineProof.render(vh);
  else magazine.style.visibility='hidden';
 }else{
 magazine.style.visibility=magazineProgress>0?'visible':'hidden';
 magazine.style.clipPath='inset(0 '+(100-100*magazineProgress).toFixed(3)+'% 0 0)';
 magazine.style.setProperty('--magazine-reveal',magazineProgress.toFixed(5));
 magazine.style.setProperty('--magazine-shift-up',(-13*(1-magazineProgress)).toFixed(3)+'svh');
 magazine.style.setProperty('--magazine-shift-down',(13*(1-magazineProgress)).toFixed(3)+'svh');
 magazine.style.setProperty('--magazine-shift-third',(-9*(1-magazineProgress)).toFixed(3)+'svh');
 magazine.setAttribute('aria-hidden',magazineProgress>=.999?'false':'true');
 }
 church.style.pointerEvents=handoffMagazineProgress>0?'none':'';
 root.dataset.p2Phase=vh<.65?'identity':vh<1.72?'ocean-rise':vh<2.37?'red-sea':handoffMagazineProgress>=.999?'magazine':handoffMagazineProgress>0?'church-to-magazine':'church';root.dataset.p2Progress=vh.toFixed(4);root.dataset.p2WaterLevel=rise.toFixed(4);
 index.querySelector('span').textContent=handoffMagazineProgress>=.5?'02 / 07':'01 / 07';
 const entry=index.querySelector('a');entry.href=handoffMagazineProgress>=.5?'/journal/':'/church/';entry.textContent=handoffMagazineProgress>=.5?'READ THE JOURNAL':'ENTER LIVING WATER';
}

function schedule(){if(!raf)raf=requestAnimationFrame(render)}
function visibilityWater(){
 cancelAnimationFrame(raf);raf=0;schedule();
}
addEventListener('visibilitychange',visibilityWater);
addEventListener('scroll',schedule,{passive:true});addEventListener('resize',schedule,{passive:true});
addEventListener('message',e=>{if(!embedded||e.source!==window.parent||e.origin!==location.origin||!e.data||e.data.type!=='westside-p2-scroll')return;externalProgress=clamp(Number(e.data.progress)||0,0,1);hasExternalProgress=true;active=e.data.active!==false;
 // Apply incoming scroll geometry immediately; RAF is reserved for live water.
 const next=embeddedScene(externalProgress);
 if(next!==sceneVh){displayVh=next;drawScene(next,performance.now());sceneVh=next}
 schedule()});
render();
})();
