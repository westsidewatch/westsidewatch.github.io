/* P2 04 | ORIGINAL SPREAD -> TWELVE VOICES
 * ONE scroll authority. The RELEASED 01–03 iframe is NEVER reparented,
 * restyled or resized. 04 reads its actual Doré plate/ONE folio bounds.
 *
 * 9.44–10.08   Doré plate -> first original speaker poster, same frame
 * 10.08–10.95  first poster to left half, second to right half
 * 10.95–11.15  both posters HOLD; background does NOT enter yet
 * 11.15–11.73  ONLY the exterior olive SVG changes, directional bottom-up
 * 11.95–15.89  five opposite-mask switches, two speakers per spread (6 pairs)
 * 16.25–17.25  the SAME twelve image works geometrically recompose as index
 * 17.25–17.65  chapter title and entry invitation hold
 *
 * Source: MASTER_SITE_ARCHITECTURE §§11–12; FIRST-LOOK-MOTION-CONTRACT;
 * user's accepted P2 04 art direction. No autoplay, opacity crossfade,
 * film player, poster distortion or second Sevenfold entry.
 */
(()=>{'use strict';
 const $=s=>document.querySelector(s);
 const stage=$('#p2-olive-stage'),track=$('#p2-olive-track');
 const base=$('#p2-0103-original'),folio=$('#olive-proof');
 const first=$('#olive-first'),firstImg=$('#olive-first-image');
 const pair=$('#olive-pair');
 const left=$('#olive-pair-left'),right=$('#olive-pair-right');
 const nextLeft=$('#olive-pair-next-left'),nextRight=$('#olive-pair-next-right');
 const overview=$('#olive-overview'),enter=$('#olive-enter');
 const ground=$('#p2-olive-surround'),rubric=$('#olive-rubric');
 const slider=$('#p2-olive-seek'),output=$('#p2-olive-progress');
 const status=$('#p2-olive-folio-status');
 if(!stage||!track||!base||!folio||!first||!ground)return;
 const clamp=(v,a=0,b=1)=>Math.min(b,Math.max(a,v));
 const ease=v=>{const u=clamp(v);return u*u*(3-2*u)};
 const mix=(a,b,t)=>a+(b-a)*t;
 const T={start:9.44,first:10.08,spread:10.95,
          groundStart:11.15,groundEnd:11.73,
          pairStart:11.95,pairStep:.83,pairDuration:.62,
          indexStart:16.25,indexEnd:17.25,end:17.65};
 const roster=[
  ['watchman-nee','倪柝聲','WATCHMAN NEE'],
  ['derek-prince','葉光明','DEREK PRINCE'],
  ['david-pawson','大衛鮑森','DAVID PAWSON'],
  ['stephen-tong','唐崇榮','STEPHEN TONG'],
  ['huang-shuhua','黃淑華','HUANG SHUHUA'],
  ['kang-lai-chang','康來昌','KANG LAI-CHANG'],
  ['jerry-lai','賴若瀚','JERRY LAI'],
  ['tong-liu','劉彤','TONG LIU'],
  ['jiang-xiuqin','江秀琴','GRACE CHIANG'],
  ['rick-warren','華理克','RICK WARREN'],
  ['yu-hong-jie','于宏潔','YU HONGJIE'],
  ['kou-shao-en','寇紹恩','KOU SHAO-EN']
 ];
 const pathFor=i=>'/images/olive/'+roster[i][0]+'-editorial.png';
 const figures=[left,right,nextLeft,nextRight];
 for(const figure of figures){
  const caption=document.createElement('figcaption');
  caption.setAttribute('aria-hidden','true');figure.append(caption);
 }
 const cards=roster.map(([slug,zh,en],i)=>{
  const a=document.createElement('a');
  a.className='olive-stage__index-card';
  a.href='/olive/';a.tabIndex=-1;
  a.dataset.speaker=slug;a.setAttribute('aria-label',en+' · '+zh+'，進入橄欖山');
  const img=document.createElement('img');
  img.src=pathFor(i);img.alt=en+' · '+zh;
  img.decoding='async';img.loading='eager';
  const cap=document.createElement('span');
  cap.textContent=String(i+1).padStart(2,'0')+' / '+en+' · '+zh;
  a.append(img,cap);
  a.style.zIndex=String(i+1);
  overview.append(a);
  return a;
 });
 function setFigure(element,i){
  if(element.dataset.speakerIndex===String(i))return;
  element.dataset.speakerIndex=String(i);
  const [slug,zh,en]=roster[i];
  const img=element.querySelector('img');
  img.src=pathFor(i);img.alt=en+' · '+zh;
  element.querySelector('figcaption').textContent=
   String(i+1).padStart(2,'0')+' / '+en+' · '+zh;
 }
 function originalProgress(d){
  const boundary=3.0775,limit=6.5,v=Math.min(d,limit);
  if(v<=boundary){
   const scene=v<=1.8?.1+v*(.4/1.8):.5+(v-1.8);
   return clamp(scene/2.9);
  }
  const vh=2.37+(v-boundary)/(limit-boundary)*(4-2.37);
  return clamp(vh<=2.9?.75*vh/2.9:.75+.25*(vh-2.9)/1.1);
 }
 let lastGeometry=null,queued=false;
 function measure(){
  const doc=base.contentDocument;
  const one=doc?.querySelector('#emmaus .emmaus__left');
  const plate=doc?.querySelector('#emmaus .emmaus__right');
  if(!one||!plate)return lastGeometry;
  const a=one.getBoundingClientRect(),b=plate.getBoundingClientRect();
  const src=base.getBoundingClientRect(),dest=stage.getBoundingClientRect();
  if(a.width<30||b.width<30||a.height<30||b.height<30)return lastGeometry;
  const x=Math.min(a.left,b.left)+src.left-dest.left;
  const y=Math.min(a.top,b.top)+src.top-dest.top;
  const w=Math.max(a.right,b.right)-Math.min(a.left,b.left);
  const h=Math.max(a.bottom,b.bottom)-Math.min(a.top,b.top);
  if(x<0||y<0||x+w>dest.width+3||y+h>dest.height+3)return lastGeometry;
  // Both coordinates are in the exact published ONE+Doré scene, in px.
  lastGeometry={x,y,w,h,
   plate:{x:b.left+src.left-dest.left-x,
          y:b.top+src.top-dest.top-y,w:b.width,h:b.height}};
  return lastGeometry;
 }
 function position(el,x,y,w,h){
  el.style.left=x.toFixed(2)+'px';
  el.style.top=y.toFixed(2)+'px';
  el.style.width=w.toFixed(2)+'px';
  el.style.height=h.toFixed(2)+'px';
 }
 function adjustGround(g){
  const W=stage.clientWidth,H=stage.clientHeight,{x,y,w,h}=g;
  const areas={top:[0,0,W,y],left:[0,y,x,h],
    right:[x+w,y,Math.max(0,W-x-w),h],
    bottom:[0,y+h,W,Math.max(0,H-y-h)]};
  for(const el of ground.querySelectorAll('[data-side]')){
   const [px,py,pw,ph]=areas[el.dataset.side];
   position(el,px,py,pw,ph);
   el.style.backgroundSize=W+'px '+H+'px';
   el.style.backgroundPosition=-px+'px '+-py+'px';
  }
 }
 function changePair(index,transition=0,withNext=false){
  setFigure(left,index*2);setFigure(right,index*2+1);
  if(withNext){
   setFigure(nextLeft,(index+1)*2);setFigure(nextRight,(index+1)*2+1);
   const rightCrop=((1-transition)*100).toFixed(3);
   nextLeft.style.clipPath='inset(0 '+rightCrop+'% 0 0)';
   nextRight.style.clipPath='inset(0 0 0 '+rightCrop+'%)';
  }
  nextLeft.style.visibility=withNext&&transition>0?'visible':'hidden';
  nextRight.style.visibility=withNext&&transition>0?'visible':'hidden';
 }
 function layoutIndex(g,t){
  const cols=g.w>=900?6:g.w>=600?4:3;
  const rows=Math.ceil(12/cols);
  const horizontal=g.w>=900?22:9,top=g.w>=900?32:18;
  const bottom=g.w>=900?83:78,gap=g.w>=900?12:5;
  const cellW=(g.w-horizontal*2-gap*(cols-1))/cols;
  const cellH=(g.h-top-bottom-gap*(rows-1))/rows;
  const half=g.w/2;
  cards.forEach((card,i)=>{
   const startX=i%2===0?0:half;
   const targetX=horizontal+(i%cols)*(cellW+gap);
   const targetY=top+Math.floor(i/cols)*(cellH+gap);
   position(card,mix(startX,targetX,t),mix(0,targetY,t),
    mix(half,cellW,t),mix(g.h,cellH,t));
  });
  overview.dataset.columns=String(cols);
 }
 function paint(){
  queued=false;
  const height=Math.max(innerHeight,1);
  const d=clamp(-track.getBoundingClientRect().top/height,0,T.end);
  if(base.contentWindow)base.contentWindow.postMessage({
   type:'westside-p2-home-pose',
   distance:Math.min(d,9.34),
   legacyProgress:originalProgress(d),active:true
  },location.origin);
  const g=measure();
  output.textContent=d.toFixed(2);slider.value=String(d);
  stage.dataset.p2Distance=d.toFixed(4);
  stage.dataset.p2FolioReady=g?'true':'false';
  if(!g)return;
  position(folio,g.x,g.y,g.w,g.h);
  adjustGround(g);
  const stageActive=d>T.start+.00001;
  folio.style.visibility=stageActive?'visible':'hidden';
  const bridge=ease((d-T.start)/(T.first-T.start));
  const form=ease((d-T.first)/(T.spread-T.first));
  const bg=ease((d-T.groundStart)/(T.groundEnd-T.groundStart));
  const fan=ease((d-T.indexStart)/(T.indexEnd-T.indexStart));
  const half=g.w/2;
  // The actual Doré image never moves: overlay #1 inherits ITS bounds.
  // It travels into the left HALF only once the first poster is established.
  const bx=mix(g.plate.x,0,form);
  const by=mix(g.plate.y,0,form);
  const bw=mix(g.plate.w,half,form);
  const bh=mix(g.plate.h,g.h,form);
  position(first,bx,by,bw,bh);
  first.style.visibility=d>T.start&&d<T.spread?'visible':'hidden';
  first.style.clipPath=d<T.first?
   'inset(0 0 0 '+((1-bridge)*100).toFixed(3)+'%)':'none';
  // Pair B enters while A travels; both images stay 3:4 and object-fit.
  position(pair,0,0,g.w,g.h);
  for(const [element,x] of [[left,0],[right,half],[nextLeft,0],[nextRight,half]]){
   position(element,x,0,half,g.h);
  }
  pair.style.visibility=d>=T.first?'visible':'hidden';
  const forming=d>=T.first&&d<T.spread;
  const paired=d>=T.spread;
  left.style.visibility=paired?'visible':'hidden';
  right.style.visibility=paired?'visible':'hidden';
  if(forming){
   setFigure(nextRight,1);
   nextRight.style.visibility=form>0?'visible':'hidden';
   nextRight.style.clipPath='inset(0 0 0 '+((1-form)*100).toFixed(3)+'%)';
   nextLeft.style.visibility='hidden';
  }else if(d<T.pairStart){
   changePair(0); // Both full posters HOLD before the background moves.
  }else{
   const i=Math.min(5,Math.floor((d-T.pairStart)/T.pairStep));
   const tick=T.pairStart+i*T.pairStep;
   const switching=i<5;
   const u=switching?ease((d-tick)/T.pairDuration):1;
   changePair(i,u,switching);
   stage.dataset.p2PairIndex=String(i);
   stage.dataset.p2PairBlend=u.toFixed(5);
  }
  // The engraved exterior is separate from (and later than) the pair.
  // Four pre-cut panels map one SVG without ever painting over the folio.
  // We change the spatial mask; NOT opacity or color crossfade.
  ground.style.visibility=bg>0?'visible':'hidden';
  ground.style.clipPath=bg>.99999?'none':
   'inset('+((1-bg)*100).toFixed(3)+'% 0 0 0)';
  ground.style.opacity='1';
  rubric.style.visibility=d>=T.groundEnd?'visible':'hidden';
  rubric.style.clipPath=d>=T.groundEnd+.19?'none':
   'inset(0 '+((1-ease((d-T.groundEnd)/.19))*100).toFixed(3)+'% 0 0)';
  overview.style.visibility=d>T.indexStart?'visible':'hidden';
  if(d>=T.indexStart)layoutIndex(g,fan);
  const finished=d>=T.indexEnd-.00001;
  enter.style.visibility=finished?'visible':'hidden';
  enter.style.pointerEvents=d>T.indexEnd+.19?'auto':'none';
  enter.style.clipPath=d>=T.indexEnd+.20?'none':
   'inset('+((1-ease((d-T.indexEnd)/.20))*100).toFixed(3)+'% 0 0)';
  const interactive=finished;
  folio.inert=!interactive;
  folio.setAttribute('aria-hidden',interactive?'false':'true');
  enter.tabIndex=interactive?0:-1;
  cards.forEach(card=>card.tabIndex=interactive?0:-1);
  stage.dataset.p2Bridge=bridge.toFixed(5);
  stage.dataset.p2Spread=form.toFixed(5);
  stage.dataset.p2Ground=bg.toFixed(5);
  stage.dataset.p2Index=fan.toFixed(5);
  stage.dataset.p2Composition='dore-to-two-posters-to-six-pairs-to-twelve';
  stage.dataset.p2Scene=d<T.start?'03-held':
    d<T.first?'04-dore-handoff':
    d<T.spread?'04-two-poster-formation':
    d<T.groundStart?'04-pair-hold':
    d<T.groundEnd?'04-ground-reveal':
    d<T.pairStart?'04-editorial-hold':
    d<T.indexStart?'04-six-pair-gallery':
    d<T.indexEnd?'04-twelve-recomposition':'04-twelve-index';
  status.textContent=d<T.start?'03 / 07 · EMMAUS':
   d<T.groundEnd?'04 / 07 · THE FIRST TWO':
   d<T.indexStart?'04 / 07 · TWELVE VOICES':
   '04 / 07 · THE TWELVE';
 }
 function schedule(){if(!queued){queued=true;requestAnimationFrame(paint)}}
 function go(d){
  const top=track.getBoundingClientRect().top+scrollY+clamp(d,0,T.end)*Math.max(1,innerHeight);
  scrollTo({top,behavior:'instant'});schedule();
 }
 document.querySelectorAll('[data-seek]').forEach(b=>b.addEventListener('click',()=>go(+b.dataset.seek)));
 slider.addEventListener('input',()=>go(+slider.value));
 base.addEventListener('load',schedule);
 addEventListener('scroll',schedule,{passive:true});
 addEventListener('resize',()=>{lastGeometry=null;schedule()},{passive:true});
 const initial=Number(new URLSearchParams(location.search).get('d')??9.30);
 requestAnimationFrame(()=>requestAnimationFrame(()=>go(Number.isFinite(initial)?initial:9.30)));
})();