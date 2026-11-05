/* P2 04 | ORIGINAL SPREAD -> TWELVE VOICES
 * ONE scroll authority. The RELEASED 01–03 iframe is NEVER reparented,
 * restyled or resized. 04 reads its actual Doré plate/ONE folio bounds.
 *
 * 9.44–10.08   Doré plate -> first original speaker poster, same frame
 * 10.08–10.95  03 paper clears through opposed split-field masks as A moves LEFT,
 *              then B reveals from BELOW in the right plate
 * 10.95–11.15  two approved posters HOLD; 04 mountain pigment has not entered
 * 11.15–11.73  dark olive/gold mountain enters top-down LEFT, bottom-up RIGHT,
 *              center label uses the SAME scroll progress (MERSI's actual grammar)
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
 const neutral=$('#p2-olive-bridge'),ground=$('#p2-olive-surround'),rubric=$('#olive-rubric');
 const slider=$('#p2-olive-seek'),output=$('#p2-olive-progress');
 const status=$('#p2-olive-folio-status');
 if(!stage||!track||!base||!folio||!first||!ground||!neutral)return;
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
 // The user's two-day APPROVED original English composition is not in
 // the portrait PNG. It lives in speaker-baseline-v1 (shadow DOM: 12
 // position, width, line, font-size, optical size and occlusion records).
 // Every original poster must therefore be a COMPOSITE, NOT a naked PNG.
 // Never duplicate its type by rebuilding it from roster labels.
 const frozen=window.OliveSpeakerBaseline;
 if(!frozen||typeof frozen.mount!=='function'){
  throw new Error('CRITICAL: protected Olive speaker typographic master is unavailable');
 }
 function protectArtwork(figure,index){
  const img=figure.querySelector('img');
  if(!img)throw new Error('No original portrait in '+figure.id);
  let art=figure.querySelector('.olive-stage__artwork');
  if(!art){
   art=document.createElement('div');
   art.className='olive-stage__artwork';
   img.parentNode.insertBefore(art,img);
   art.append(img);
   img.classList.add('olive-stage__original');
  }
  // Frozen component is keyed by speaker; old shadow roots must be
  // disconnected when the pair changes. Do not write into the master.
  const target=roster[index][0];
  const overlay=art.querySelector('olive-speaker-baseline');
  if(overlay&&overlay.dataset.speaker!==target)overlay.remove();
  if(!art.querySelector('olive-speaker-baseline'))frozen.mount(art,target);
  figure.dataset.oliveProtectedBaseline='v1';
  figure.dataset.speakerIndex=String(index);
  return art;
 }
 const figures=[left,right,nextLeft,nextRight];
 for(const figure of figures){
  const caption=document.createElement('figcaption');
  caption.setAttribute('aria-hidden','true');figure.append(caption);
 }
 protectArtwork(first,0);
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
  protectArtwork(a,i);
  return a;
 });
 function setFigure(element,i){
  if(element.dataset.speakerIndex===String(i) &&
     element.querySelector('olive-speaker-baseline')?.dataset.speaker===roster[i][0])return;
  const [slug,zh,en]=roster[i];
  const img=element.querySelector('img');
  img.src=pathFor(i);img.alt=en+' · '+zh;
  // The approved name and Chinese are INSIDE the artwork, as originally
  // placed; this outer caption is just a discrete folio number.
  element.querySelector('figcaption').textContent=
   String(i+1).padStart(2,'0')+' / 12';
  protectArtwork(element,i);
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
 // ONE continuous landscape plate. The previous four registered panels
 // created rectangular cuts and could never read as one mountain.
 // Each protected composite (PNG + frozen Shadow DOM lettering) MUST
 // remain a true 3:4 print. We calculate the actual outer boxes from that
 // immutable aspect instead of letting an arbitrary responsive cell resize
 // its image and expose synthetic gray strips.
 function galleryRects(g){
  const portraitRatio=3/4;
  const mobile=g.w<600;
  const margin=mobile?Math.max(10,Math.min(20,g.w*.037)):
    Math.max(36,Math.min(118,g.w*.065));
  const top=mobile?Math.max(84,Math.min(100,g.h*.12)):
    Math.max(118,Math.min(149,g.h*.142));
  const bottom=mobile?Math.max(46,Math.min(67,g.h*.075)):
    Math.max(50,Math.min(73,g.h*.078));
  const gap=mobile?12:Math.max(18,Math.min(37,g.w*.03));
  const maxHeight=Math.max(1,g.h-top-bottom);
  if(mobile){
   // True 3:4 upper and lower PRINTS. Mobile cannot physically show two
   // full-width 3:4 portraits in one 9:16 viewport; center them instead
   // of stretching or cutting the frozen lettering.
   const maxPosterH=(maxHeight-gap)/2;
   const posterW=Math.min(g.w-2*margin,maxPosterH*portraitRatio);
   const posterH=posterW/portraitRatio;
   const x=(g.w-posterW)/2;
   const y=top+Math.max(0,(maxHeight-(2*posterH+gap))/2);
   return [{x,y,w:posterW,h:posterH},
           {x,y:y+posterH+gap,w:posterW,h:posterH}];
  }
  const maxPosterW=(g.w-2*margin-gap)/2;
  const posterW=Math.min(maxPosterW,maxHeight*portraitRatio);
  const posterH=posterW/portraitRatio;
  const x=(g.w-(2*posterW+gap))/2;
  const y=top+Math.max(0,(maxHeight-posterH)/2);
  return [{x,y,w:posterW,h:posterH},
          {x:x+posterW+gap,y,w:posterW,h:posterH}];
 }
 function changePair(index,transition=0,withNext=false,vertical=false){
  setFigure(left,index*2);setFigure(right,index*2+1);
  if(withNext){
   setFigure(nextLeft,(index+1)*2);setFigure(nextRight,(index+1)*2+1);
   const crop=((1-transition)*100).toFixed(3);
   // The same true MERSI opposition on desktop and mobile: LEFT or TOP
   // uncovers downward; RIGHT or BOTTOM uncovers upward. No opacity fade.
   nextLeft.style.clipPath='inset(0 0 '+crop+'% 0)';
   nextRight.style.clipPath='inset('+crop+'% 0 0 0)';
  }
  nextLeft.style.visibility=withNext&&transition>0?'visible':'hidden';
  nextRight.style.visibility=withNext&&transition>0?'visible':'hidden';
 }
 function layoutIndex(g,t){
  const cols=g.w>=900?6:g.w>=600?4:3;
  const rows=Math.ceil(12/cols);
  const horizontal=g.w>=900?33:12;
  const top=g.w>=900?Math.max(122,Math.min(150,g.h*.145)):95;
  const bottom=g.w>=900?72:64;
  const gapX=g.w>=900?13:7;
  // A caption is now OUTSIDE its original 3:4 print, on dark-green
  // invitation stock. The portrait box itself NEVER includes the caption.
  const rowGap=g.w>=900?31:21;
  const maxW=(g.w-2*horizontal-(cols-1)*gapX)/cols;
  const maxH=(g.h-top-bottom-(rows-1)*rowGap)/rows;
  const posterW=Math.max(1,Math.min(maxW,maxH*.75));
  const posterH=posterW*4/3;
  const totalW=cols*posterW+(cols-1)*gapX;
  const totalH=rows*posterH+(rows-1)*rowGap;
  const leftX=(g.w-totalW)/2;
  const topY=top+Math.max(0,(g.h-top-bottom-totalH)/2);
  const anchors=galleryRects(g);
  cards.forEach((card,i)=>{
   const from=anchors[i%2];
   const targetX=leftX+(i%cols)*(posterW+gapX);
   const targetY=topY+Math.floor(i/cols)*(posterH+rowGap);
   position(card,mix(from.x,targetX,t),mix(from.y,targetY,t),
    mix(from.w,posterW,t),mix(from.h,posterH,t));
  });
  overview.style.setProperty('--index-caption-alpha',
    String(ease((t-.69)/.31)));
  overview.dataset.columns=String(cols);
 }
 function revealSplitField(node,u){
  const reveal=clamp(u),crop=((1-reveal)*100).toFixed(3);
  node.style.visibility=reveal>0?'visible':'hidden';
  const leftHalf=node.querySelector('[data-side="left"]');
  const rightHalf=node.querySelector('[data-side="right"]');
  // Both panels sample one full image. Opposite insets are authored from
  // one absolute scroll position: pause and reverse restore exact geometry.
  if(leftHalf)leftHalf.style.clipPath='inset(0 0 '+crop+'% 0)';
  if(rightHalf)rightHalf.style.clipPath='inset('+crop+'% 0 0 0)';
  node.dataset.reveal=reveal.toFixed(5);
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
  // Landscape is one uninterrupted plate behind the poster folio.
  const stageActive=d>T.start+.00001;
  folio.style.visibility=stageActive?'visible':'hidden';
  const bridge=ease((d-T.start)/(T.first-T.start));
  const form=ease((d-T.first)/(T.spread-T.first));
  const firstTravel=ease(form/.73);
  const secondArrival=ease((form-.57)/.43);
  const readingField=ease(form/.20);
  const bg=ease((d-T.groundStart)/(T.groundEnd-T.groundStart));
  revealSplitField(neutral,readingField);
  revealSplitField(ground,bg);
  const fan=ease((d-T.indexStart)/(T.indexEnd-T.indexStart));
  const vertical=g.w<600;
  const rects=galleryRects(g);
  // Desktop uses true folio halves; on narrow phones two original posters
  // occupy TOP/BOTTOM halves to avoid extremely thin and mostly empty strips.
  // The actual Doré image never moves: overlay #1 inherits ITS bounds.
  // It travels into the left HALF only once the first poster is established.
  const settledLeft=rects[0];
  const bx=mix(g.plate.x,settledLeft.x,firstTravel);
  const by=mix(g.plate.y,settledLeft.y,firstTravel);
  const bw=mix(g.plate.w,settledLeft.w,firstTravel);
  const bh=mix(g.plate.h,settledLeft.h,firstTravel);
  position(first,bx,by,bw,bh);
  first.style.visibility=d>T.start&&d<T.spread?'visible':'hidden';
  first.style.clipPath=d<T.first?
   'inset(0 0 0 '+((1-bridge)*100).toFixed(3)+'%)':'none';
  // Pair B enters while A travels; both images stay 3:4 and object-fit.
  position(pair,0,0,g.w,g.h);
  for(const [element,side] of [[left,0],[right,1],[nextLeft,0],[nextRight,1]]){
   const r=rects[side];position(element,r.x,r.y,r.w,r.h);
  }
  pair.style.visibility=d>=T.first&&d<T.indexStart?'visible':'hidden';
  const forming=d>=T.first&&d<T.spread;
  const paired=d>=T.spread;
  left.style.visibility=paired?'visible':'hidden';
  right.style.visibility=paired?'visible':'hidden';
  if(forming){
   setFigure(nextRight,1);
   nextRight.style.visibility=secondArrival>0?'visible':'hidden';
   nextRight.style.clipPath='inset('+((1-secondArrival)*100).toFixed(3)+'% 0 0 0)';
   nextLeft.style.visibility='hidden';
  }else if(d<T.pairStart){
   changePair(0); // Both full posters HOLD before the background moves.
  }else{
   const i=Math.min(5,Math.floor((d-T.pairStart)/T.pairStep));
   const tick=T.pairStart+i*T.pairStep;
   const switching=i<5;
   const u=switching?ease((d-tick)/T.pairDuration):1;
   changePair(i,u,switching,vertical);
   stage.dataset.p2PairIndex=String(i);
   stage.dataset.p2PairBlend=u.toFixed(5);
  }
  // Mountain replaces the 03 reading substrate AFTER the double-spread
  // is fixed. Label and split-field move from the same progress; gold
  // is a print material, NOT a gradient opacity overlay.
  ground.style.opacity='1';
  rubric.style.visibility=bg>0?'visible':'hidden';
  rubric.style.clipPath=bg>=1?'none':
   'inset(0 '+((1-bg)*49).toFixed(3)+'% 0 '+((1-bg)*49).toFixed(3)+'%)';
  overview.style.visibility=d>=T.indexStart?'visible':'hidden';
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
  stage.dataset.p2ReadingField=readingField.toFixed(5);
  stage.dataset.p2Ground=bg.toFixed(5);
  stage.dataset.p2FieldMethod='opposed-top-down-bottom-up';
  stage.dataset.p2Index=fan.toFixed(5);
  stage.dataset.p2Composition='green-bible-cover-to-gilt-sermon-invitation-to-twelve';
  stage.dataset.p2PosterAspect='3:4';
  stage.dataset.p2PairOrientation=vertical?'stacked':'side-by-side';
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