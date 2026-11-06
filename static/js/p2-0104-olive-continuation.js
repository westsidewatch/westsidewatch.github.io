/* P2 04 | ORIGINAL SPREAD -> TWELVE VOICES
 * ONE scroll authority. The RELEASED 01–03 iframe is NEVER reparented,
 * restyled or resized. 04 reads its actual Doré plate/ONE folio bounds.
 *
 * 9.44–10.08   Doré plate -> 04 gilt invitation card; mounted original print follows
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
 const firstInvitation=$('#olive-first-invitation');
 const invitationLeft=$('#olive-invitation-left');
 const invitationRight=$('#olive-invitation-right');
 const pair=$('#olive-pair');
 const left=$('#olive-pair-left'),right=$('#olive-pair-right');
 const nextLeft=$('#olive-pair-next-left'),nextRight=$('#olive-pair-next-right');
 const overview=$('#olive-overview'),enter=$('#olive-enter');
 const growthSvg=$('#olive-growth-field'),growthRoot=$('#olive-growth-paths');
 const growthMaskLeft=$('#olive-growth-mask-left'),growthMaskRight=$('#olive-growth-mask-right');
 const growthLines=[],growthTips=[],growthCurves=[],livingBurins=[],reduceGrowth=matchMedia('(prefers-reduced-motion: reduce)');
 let livingClock=0,livingLast=0;
 const neutral=$('#p2-olive-bridge'),ground=$('#p2-olive-surround'),rubric=$('#olive-rubric');
 const slider=$('#p2-olive-seek'),output=$('#p2-olive-progress');
 const status=$('#p2-olive-folio-status');
 if(!stage||!track||!base||!folio||!first||!ground||!neutral||
     !firstInvitation||!invitationLeft||!invitationRight)return;
 // The independent SVG project can be inspected without foreground posters.
 // This is a PREVIEW-ONLY optical proof; original gallery default is untouched.
 if(new URLSearchParams(location.search).get('artOnly')==='1')
  stage.classList.add('olive-art-only');
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
 // The SVG-002 tool animates the actual curve geometry behind a growing tip.
 // Apply that grammar to the eight historical OLIVE spines. All leaf engraving
 // keeps its authorized two-tone stroke-dash growth and twelve-voice timing.
 // Geometry is sampled ONCE from the intact SVG source, never invented afresh.
 function curvePoint(points,u){
  const n=points.length-1,at=clamp(u)*n,j=Math.min(n-1,Math.floor(at));
  const f=at-j,a=points[j],b=points[j+1];
  return {x:a.x+(b.x-a.x)*f,y:a.y+(b.y-a.y)*f};
 }
 function drawGrowingCurve(curve,local){
  const path=curve.el,tip=curve.tip,points=curve.points;
  if(local<=.00001){
   const p=points[0];
   path.setAttribute('d','M'+p.x.toFixed(2)+' '+p.y.toFixed(2));
   tip.style.visibility='hidden';return;
  }
  if(reduceGrowth.matches){
   path.setAttribute('d',curve.originalD);
   tip.style.visibility='hidden';return;
  }
  // The underlying structure physically develops with scroll, then its
  // existing wood fibres continue breathing on an independent time clock.
  // Grounded at the root, the terminal shoots can bend by up to ~3px.
  const count=Math.max(4,Math.ceil(local*(points.length-1)));
  const xy=[];
  for(let j=0;j<=count;j++){
   const u=local*j/count,p=curvePoint(points,u);
   const flex=Math.pow(u,1.65)*(curve.seed>=14?.6:2.65);
   const wave=Math.sin(livingClock*(.64+.039*(curve.seed%7))+
       u*6.8+curve.seed*1.21);
   const cross=Math.cos(livingClock*.41+u*4.3+curve.seed*.77);
   xy.push({x:p.x+flex*wave,y:p.y+flex*.42*cross});
  }
  const d=xy.map((p,i)=>(i?'L':'M')+p.x.toFixed(2)+' '+p.y.toFixed(2)).join(' ');
  if(path.getAttribute('d')!==d)path.setAttribute('d',d);
  // A writing front continues traversing COMPLETED branches, rather than
  // disappearing once local reaches 1. The source centreline remains grown.
  const active=local>=.9999?
   .12+.88*((livingClock*.087+curve.seed*.137)%1):local;
  const end=Math.max(1,Math.floor((xy.length-1)*Math.min(1,active/Math.max(local,.0001))));
  const begin=Math.max(0,end-5);
  tip.setAttribute('d',xy.slice(begin,end+1).map((p,i)=>
   (i?'L':'M')+p.x.toFixed(2)+' '+p.y.toFixed(2)).join(' '));
  tip.style.visibility=local>.025?'visible':'hidden';
 }
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
 // Separate geometries: a full printed invitation card takes over the
 // old Doré frame; the approved 3:4 speaker PRINT mounts within it.
 // None of these calculations can resize a settled speaker poster.
 function printInsideCard(c){
  const side=c.w*.073,top=c.h*.12,bottom=c.h*.10;
  const w=Math.max(1,Math.min(c.w-2*side,(c.h-top-bottom)*.75));
  const h=w/.75;
  return {x:c.x+(c.w-w)/2,
    y:c.y+top+Math.max(0,(c.h-top-bottom-h)/2),w,h};
 }
 function cardAroundPoster(r,other,mobile,sideIndex){
  const gap=mobile?
    Math.max(0,other.y-(r.y+r.h)):
    Math.abs(other.x-(r.x+r.w));
  // A gallery invitation has ONE deliberately wide OUTER rail for a
  // localized Olives relief, and a narrow INNER gutter between works.
  // The original 3:4 poster rectangle is NEVER recomputed or touched.
  const outer=mobile?Math.max(18,Math.min(28,r.w*.08)):
    Math.max(36,Math.min(56,r.w*.095));
  const inner=mobile?Math.max(18,Math.min(28,r.w*.08)):
    Math.max(6,Math.min(12,gap*.28));
  const left=sideIndex===0?outer:inner;
  const right=sideIndex===0?inner:outer;
  const top=mobile?Math.min(24,Math.max(6,gap*.44)):
    Math.max(68,Math.min(76,r.h*.112));
  const bottom=mobile?Math.min(20,Math.max(4,gap*.40)):
    Math.max(27,Math.min(34,r.h*.047));
  return {x:r.x-left,y:r.y-top,w:r.w+left+right,h:r.h+top+bottom};
 }
 // Align the REGISTERED print engraving in the REAL exposed green paper
 // above the frozen 3:4 poster, rather than pinning its gold ink to top:0.
 // The source slot is taller than the settled pair; both are handled
 // geometrically without ever moving/resizing the approved poster.
 function positionInvitedEngraving(el,card,poster,mobile){
  const exposed=Math.max(0,poster.y-card.y);
  const safety=mobile?2:5;
  const h=Math.min(mobile?22:70,Math.max(4,exposed-2*safety));
  const y=Math.max(2,(exposed-h)/2);
  el.style.setProperty('--olive-foil-top',y.toFixed(2)+'px');
  el.style.setProperty('--olive-foil-height',h.toFixed(2)+'px');
 }
 function setCardCaption(card,i){
  const en=card.querySelector('.olive-card__name-en');
  const zh=card.querySelector('.olive-card__name-zh');
  if(!en||!zh)throw new Error('Missing editorial invitation caption');
  if(en.textContent!==roster[i][2])en.textContent=roster[i][2];
  if(zh.textContent!==roster[i][1])zh.textContent=roster[i][1];
 }
 function changePair(index,transition=0,withNext=false,vertical=false){
  setCardCaption(invitationLeft,index*2+(withNext&&transition>.5?2:0));
  setCardCaption(invitationRight,index*2+1+(withNext&&transition>.5?2:0));
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
  const top=g.w>=900?Math.max(122,Math.min(150,g.h*.145)):Math.max(108,Math.min(132,g.h*.15));
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
  const reveal=clamp(u);
  const isInvitation=node===ground;
  // 03's approved green Bible cloth remains on the LEFT while the RIGHT
  // half turns into the gold-foil Sermon invitation. Only then does the
  // new print spread across LEFT. This is an editorial handoff, not a
  // simultaneous two-panel wipe, a yellow intermediary or opacity fade.
  const leftReveal=isInvitation?ease((reveal-.52)/.48):reveal;
  const rightReveal=isInvitation?ease(reveal/.55):reveal;
  node.style.visibility=reveal>0?'visible':'hidden';
  const leftHalf=node.querySelector('[data-side="left"]');
  const rightHalf=node.querySelector('[data-side="right"]');
  if(leftHalf)leftHalf.style.clipPath='inset(0 0 '+
   ((1-leftReveal)*100).toFixed(3)+'% 0)';
  if(rightHalf)rightHalf.style.clipPath=isInvitation?
   'inset('+((1-rightReveal)*100).toFixed(3)+'% 0 0 0)':
   'inset(0 0 '+((1-rightReveal)*100).toFixed(3)+'% 0)';
  node.dataset.reveal=reveal.toFixed(5);
  node.dataset.leftReveal=leftReveal.toFixed(5);
  node.dataset.rightReveal=rightReveal.toFixed(5);
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
  // MERSI source-stage handoff is a SINGLE short spatial takeover:
  // complete the 03 printed-cloth curtain while the invitation is still
  // registered over Doré, BEFORE its movement can expose old scripture.
  // At d=10.26 the outgoing 03 page must be fully hidden, not in shards.
  const readingField=ease((d-T.first)/.065);
  const bg=ease((d-T.groundStart)/(T.groundEnd-T.groundStart));
  revealSplitField(neutral,readingField);
  revealSplitField(ground,bg);
  // ONE is an outgoing transition source only. Once 04 has fully claimed
  // the canvas there must be NO 03 cloth or gilding, even under gutters.
  if(bg>=.99999)neutral.style.visibility='hidden';
  const fan=ease((d-T.indexStart)/(T.indexEnd-T.indexStart));
  const vertical=g.w<600;
  // TWO witnesses are mounted before the background hand-off. Every
  // further PAIR of real speaker transitions grows TWO distinct historic
  // botanical groups, one per speaker, in the SAME continuous MERSI
  // scroll timeline. No waiting until the final twelve-poster overview.
  let speakerGrowth=0;
  if(d>=T.groundStart){
   // The first TWO are drawn as the new 04 material arrives. The right
   // aperture opens first, then the left: no sudden completed vegetation.
   speakerGrowth=(2/12)*bg;
   if(d>=T.pairStart){
    const pairIndex=Math.min(4,Math.floor((d-T.pairStart)/T.pairStep));
    const pairClock=T.pairStart+pairIndex*T.pairStep;
    const pairReveal=ease((d-pairClock)/T.pairDuration);
    speakerGrowth=(2+2*(pairIndex+pairReveal))/12;
   }
   if(d>=T.indexStart)speakerGrowth=1;
  }
  const growth=reduceGrowth.matches?(d>=T.groundEnd?1:0):speakerGrowth;
  if(growthSvg)growthSvg.style.visibility=d>=T.groundStart?'visible':'hidden';
  // Register the line engraving to the EXACT same MERSI material split:
  // right from BOTTOM first, left from TOP afterwards. Never draw olives
  // above the outgoing Bible cover or fake their entrance with opacity.
  // An independent ORIGINAL crop on narrow devices; never distort trees.
  // The same reversible MERSI top/bottom split now covers the exact
  // visible crop instead of the off-screen half of a stretched 1600px SVG.
  const narrow=g.w<600;
  if(growthSvg){
   const crop=narrow?'-45 -54 570 1008':'-96 -54 1792 1008';
   if(growthSvg.getAttribute('viewBox')!==crop)growthSvg.setAttribute('viewBox',crop);
   const aspect=narrow?'xMinYMid slice':'xMidYMid meet';
   if(growthSvg.getAttribute('preserveAspectRatio')!==aspect)
    growthSvg.setAttribute('preserveAspectRatio',aspect);
  }
  if(growthMaskLeft){
   growthMaskLeft.setAttribute('x',narrow?'-45':'-96');
   growthMaskLeft.setAttribute('width',narrow?'285':'896');
  }
  if(growthMaskRight){
   growthMaskRight.setAttribute('x',narrow?'240':'800');
   growthMaskRight.setAttribute('width',narrow?'285':'896');
  }
  const growLeft=ease((bg-.52)/.48),growRight=ease(bg/.55);
  if(growthMaskLeft)growthMaskLeft.setAttribute('height',(1008*growLeft).toFixed(3));
  if(growthMaskRight){
   growthMaskRight.setAttribute('y',(954-1008*growRight).toFixed(3));
   growthMaskRight.setAttribute('height',(1008*growRight).toFixed(3));
  }
  for(const line of growthLines){
   const local=ease((growth-line.start)/(line.end-line.start));
   const offset=(1000*(1-local)).toFixed(3);
   if(line.el.style.strokeDashoffset!==offset)
    line.el.style.strokeDashoffset=offset;
   // SVG-002's moving growth frontier redraws real CURVE GEOMETRY.
   // The botanical leaf hatching remains the approved static source art,
   // with its dash offset advanced along the same scroll timeline.
   if(line.curve)drawGrowingCurve(line.curve,local);
  }
  stage.dataset.p2OliveLiveCurves=String(growthCurves.length);
  stage.dataset.p2OliveGrowth=growth.toFixed(5);
  stage.dataset.p2OliveGrowthVoices=String(Math.floor(growth*12+.0001));
  stage.dataset.p2OliveGrowthPair=String(Math.min(5,Math.floor(growth*6)));
  if(growthSvg)stage.dataset.p2OliveGrowthPaths=String(growthLines.length);
  // Source-bound moving gold burins continue when scrolling stops.
  const ambient=reduceGrowth.matches?0:livingClock;
  for(const mark of livingBurins){
   const visible=ease((growth-mark.start)/(mark.end-mark.start));
   mark.el.style.strokeOpacity=(visible*(.42+.42*(.5+.5*Math.sin(ambient*.67+mark.seed*9)))).toFixed(3);
   mark.el.style.strokeDashoffset=(-1000*((ambient*mark.speed+mark.seed)%1)).toFixed(2);
  }
  const rects=galleryRects(g);
  // Desktop uses true folio halves; on narrow phones two original posters
  // occupy TOP/BOTTOM halves to avoid extremely thin and mostly empty strips.
  // The actual Doré image never moves: overlay #1 inherits ITS bounds.
  // It travels into the left HALF only once the first poster is established.
  const settledLeft=rects[0],settledRight=rects[1];
  const sourceCard=g.plate;
  const mountedSourcePrint=printInsideCard(sourceCard);
  const targetLeftCard=cardAroundPoster(settledLeft,settledRight,vertical,0);
  const targetRightCard=cardAroundPoster(settledRight,settledLeft,vertical,1);
  // 04's physical invitation first assumes the true Doré frame's bounds;
  // it then TRAVELS alongside the original print into the left position.
  const cardGeometry={
   x:mix(sourceCard.x,targetLeftCard.x,firstTravel),
   y:mix(sourceCard.y,targetLeftCard.y,firstTravel),
   w:mix(sourceCard.w,targetLeftCard.w,firstTravel),
   h:mix(sourceCard.h,targetLeftCard.h,firstTravel)
  };
  position(firstInvitation,cardGeometry.x,cardGeometry.y,
   cardGeometry.w,cardGeometry.h);
  firstInvitation.style.visibility=stageActive&&d<T.spread?'visible':'hidden';
  firstInvitation.style.clipPath=d<T.first?
    'inset(0 0 0 '+((1-bridge)*100).toFixed(3)+'%)':'none';
  const bx=mix(mountedSourcePrint.x,settledLeft.x,firstTravel);
  const by=mix(mountedSourcePrint.y,settledLeft.y,firstTravel);
  const bw=mix(mountedSourcePrint.w,settledLeft.w,firstTravel);
  const bh=mix(mountedSourcePrint.h,settledLeft.h,firstTravel);
  position(first,bx,by,bw,bh);
  positionInvitedEngraving(firstInvitation,cardGeometry,
   {x:bx,y:by,w:bw,h:bh},vertical);
  const posterReveal=ease((bridge-.33)/.67);
  first.style.visibility=d>T.start&&d<T.spread?'visible':'hidden';
  first.style.clipPath=d<T.first?
    'inset(0 0 0 '+((1-posterReveal)*100).toFixed(3)+'%)':'none';
  stage.dataset.p2InvitationShell='source-plate-to-minimal-gallery-print';
  stage.dataset.p2CardRelief='independent-olive-topography';
  stage.dataset.p2MountedFirstAspect=(bw/bh).toFixed(5);
  // 03 is still authoritative before the source card. Once the card
  // begins its spatial journey the existing independent field handoff
  // handles the retiring page; no extra paper or ONE motif is introduced.
  position(invitationLeft,targetLeftCard.x,targetLeftCard.y,
   targetLeftCard.w,targetLeftCard.h);
  position(invitationRight,targetRightCard.x,targetRightCard.y,
   targetRightCard.w,targetRightCard.h);
  positionInvitedEngraving(invitationLeft,targetLeftCard,settledLeft,vertical);
  positionInvitedEngraving(invitationRight,targetRightCard,settledRight,vertical);
  const rightCardReveal=ease((form-.44)/.26);
  invitationLeft.style.visibility=d>=T.spread&&d<T.indexStart?'visible':'hidden';
  invitationRight.style.visibility=rightCardReveal>0&&d<T.indexStart?'visible':'hidden';
  invitationLeft.style.clipPath='none';
  invitationRight.style.clipPath=d<T.spread?
   'inset('+((1-rightCardReveal)*100).toFixed(3)+'% 0 0 0)':'none';
  // Pair B enters while A travels; both images stay 3:4 and object-fit.
  position(pair,0,0,g.w,g.h);
  for(const [element,side] of [[left,0],[right,1],[nextLeft,0],[nextRight,1]]){
   const r=rects[side];position(element,r.x,r.y,r.w,r.h);
  }
  pair.style.visibility=d>=T.first&&d<T.indexStart?'visible':'hidden';
  // Strong final-index isolation. Visibility alone allowed huge previously
  // mounted pair composites to bleed beneath 12 prints in some browsers.
  pair.style.display=d>=T.indexStart?'none':'block';
  first.style.display=d>=T.indexStart?'none':'block';
  const forming=d>=T.first&&d<T.spread;
  const paired=d>=T.spread;
  left.style.visibility=paired?'visible':'hidden';
  right.style.visibility=paired?'visible':'hidden';
  if(forming){
   setCardCaption(invitationLeft,0);
   setCardCaption(invitationRight,1);
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
  const printTitle=ease((bg-.78)/.22);
  rubric.style.visibility=printTitle>0?'visible':'hidden';
  // The chapter masthead takes up its own editorial line ABOVE the full
  // twelve-speaker composition; no movement over incoming 3:4 portraits.
  // Pair phase stays within its protected headpiece; the index acquires
  // the larger, optically lowered editorial masthead AFTER recomposition.
  // Never carry a new title down across the mounted speaker originals.
  rubric.style.setProperty('--olive-title-fan',fan.toFixed(4));
  rubric.style.setProperty('--olive-title-growth',
    (fan*(vertical?12:18)).toFixed(2)+'px');
  rubric.style.transform='translate3d(0,'+
    ((vertical?22:(g.w<900?36:78))*fan).toFixed(1)+'px,0)';
  rubric.style.clipPath=printTitle>=1?'none':
   'inset(0 '+((1-printTitle)*49).toFixed(3)+'% 0 '+((1-printTitle)*49).toFixed(3)+'%)';
  overview.style.visibility=d>=T.indexStart?'visible':'hidden';
  if(d>=T.indexStart)layoutIndex(g,fan);
  const finished=d>=T.indexEnd-.00001;
  stage.dataset.p2IndexIsolated=String(d>=T.indexStart);
  stage.dataset.p2RealmSurface=bg>=.99999?'olive-exclusive':
    readingField>0?'emmaus-olive-handoff':'emmaus';
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
 // Load the editable historical botanical SVG as REAL DOM paths.
 // Uses the already tested p2-stroke-growth-prototype dash/front mechanism,
 // not CSS background movement, so every line grows and reverses in place.
 if(growthSvg&&growthRoot){
  stage.dataset.p2OliveGrowthReady='false';
  fetch('/images/p2-realms/v15/04-olive-hillside-copperplate-v3.svg?v=unified-20261106-31').then(response=>{
   if(!response.ok)throw new Error('Olive SVG HTTP '+response.status);
   return response.text();
  }).then(xml=>{
   const doc=new DOMParser().parseFromString(xml,'image/svg+xml');
   if(doc.querySelector('parsererror'))throw new Error('Invalid olive growth SVG');
   for(const child of [...doc.documentElement.children]){
    if(child.localName==='g')growthRoot.appendChild(document.importNode(child,true));
   }
   // V3: one authored botanical topography, represented by four spatial
   // depth bands: left olive, right olive, distant foothill and terrain.
   // Unlike V2, no unrelated plate is pasted onto the scene.
   const ns='http://www.w3.org/2000/svg';
   const sourceRegions=[...growthRoot.querySelectorAll(
     '.olive-growth-cluster,.olive-growth-terrain')];
   if(sourceRegions.length!==4)
    throw new Error('V3 must mount four zones of one authored original landscape');
   stage.dataset.p2OliveGrowthEchoes='0';
   const register=(source,region,i,voice)=>{
    const shine=document.createElementNS(ns,'path');
    shine.setAttribute('class','olive-growth-burin');
    shine.setAttribute('d',source.getAttribute('d'));
    shine.setAttribute('fill','none');
    shine.setAttribute('pathLength','1000');
    shine.setAttribute('stroke-dasharray','105 895');
    shine.setAttribute('stroke-dashoffset','1000');
    shine.setAttribute('stroke-width',i%4===0?'2.0':'1.35');
    shine.setAttribute('stroke-linecap','round');
    shine.style.pointerEvents='none';
    source.parentNode.appendChild(shine);
    livingBurins.push({el:shine,voice,
     start:Number(source.closest('[data-growth-start]')?.dataset.growthStart??region.dataset.growthStart),
     end:Number(source.closest('[data-growth-end]')?.dataset.growthEnd??region.dataset.growthEnd),
     seed:i*.6180339+voice*.317,speed:.11+(i%7)*.016});
   };
   sourceRegions.forEach((region,voice)=>{
    const paths=[...region.querySelectorAll('path.olive-growth-path')];
    const stride=Math.max(1,Math.floor(paths.length/12));
    let count=0;
    for(let i=voice%stride;i<paths.length&&count<12;i+=stride){
     const original=paths[i],length=original.getTotalLength();
     if(!Number.isFinite(length)||length<5)continue;
     register(original,region,i,voice);count++;
    }
   });
   stage.dataset.p2OliveLivingBurins=String(livingBurins.length);
   // Advance a real engraved writing-front without a second RAF or extra
   // network asset; all historic contours remain reversible DOM paths.
   const spines=[...growthRoot.querySelectorAll('[data-live-spine="true"]')];
   for(const original of spines){
    const interval=original.closest('[data-growth-start]');
    if(!interval)continue;
    const tip=original.cloneNode(true);
    tip.setAttribute('class','olive-growth-tip');
    tip.style.strokeDasharray='none';
    tip.style.strokeDashoffset='0';
    tip.style.visibility='hidden';
    original.parentNode.appendChild(tip);
    growthTips.push({el:tip,start:Number(interval.dataset.growthStart),
      end:Number(interval.dataset.growthEnd)});
   }
   stage.dataset.p2OliveGrowthTips=String(growthTips.length);
   for(const el of growthRoot.querySelectorAll('path.olive-growth-path')){
    const parent=el.closest('[data-growth-start]');
    if(!parent)continue;
    const start=Number(parent.getAttribute('data-growth-start'));
    const end=Number(parent.getAttribute('data-growth-end'));
    if(!Number.isFinite(start)||!Number.isFinite(end)||end<=start)
      throw new Error('Invalid staged olive engraving interval');
    const line={el,start,end};
    // Respect the variation of the original engraved burin widths.
    if(!el.hasAttribute('data-live-spine')){
     const authored=Number(el.getAttribute('stroke-width'));
     if(Number.isFinite(authored)&&authored>0)
      el.style.strokeWidth=Math.min(2.8,Math.max(.38,authored)).toFixed(3);
    }
    const isHistoricSpine=!!el.closest('.olive-growth-spines');
    if(isHistoricSpine){
     const length=el.getTotalLength();
     if(!Number.isFinite(length)||length<=0)throw new Error('Invalid olive spine length');
     const points=[];
     const slices=84;
     for(let i=0;i<=slices;i++){
      const p=el.getPointAtLength(length*i/slices);
      points.push({x:p.x,y:p.y});
     }
     const nib=growthTips[growthCurves.length]?.el;
     if(!nib)throw new Error('Historic spine has no source-led pen front');
     const curve={el,tip:nib,points,originalD:el.getAttribute('d'),
      seed:growthCurves.length};
     growthCurves.push(curve);
     line.curve=curve;
     // Original tip-led geometry itself determines which portion exists.
     // Keep offset state for reversible monitoring but disable dash masking.
     el.style.strokeDasharray='none';
    }else{
     el.style.strokeDasharray='1000';
    }
    el.style.strokeDashoffset='1000';
    growthLines.push(line);
   }
   if(growthCurves.length!==18)throw new Error('V3 requires eighteen connected authored olive-tree structure paths');
   stage.dataset.p2OliveLiveCurves=String(growthCurves.length);
   if(growthLines.length<700)throw new Error('V3 original whole-plate botanical etching is incomplete');
   stage.dataset.p2OliveSourceFamilies='4';
   stage.dataset.p2OliveArtVersion='v3';
   stage.dataset.p2OliveOriginalCopperplate='true';
   stage.dataset.p2OliveSourcePathCount=String(growthLines.length);
   stage.dataset.p2OliveGrowthReady='true';
   schedule();
  }).catch(error=>{
   stage.dataset.p2OliveGrowthReady='error';
   stage.dataset.p2OliveGrowthError=String(error.message||error);
  });
 }
 function livingFrame(now){
  if(!livingLast)livingLast=now;
  const dt=Math.min(.06,(now-livingLast)/1000);livingLast=now;
  if(!reduceGrowth.matches&&stage.dataset.p2OliveGrowthReady==='true'&&
     Number(stage.dataset.p2Distance||0)>=T.groundStart){
   livingClock+=dt;
   if(now-(livingFrame.lastPaint||0)>40){livingFrame.lastPaint=now;schedule();}
  }
  requestAnimationFrame(livingFrame);
 }
 requestAnimationFrame(livingFrame);
 document.querySelectorAll('[data-seek]').forEach(b=>b.addEventListener('click',()=>go(+b.dataset.seek)));
 slider.addEventListener('input',()=>go(+slider.value));
 base.addEventListener('load',schedule);
 addEventListener('scroll',schedule,{passive:true});
 addEventListener('resize',()=>{lastGeometry=null;schedule()},{passive:true});
 const initial=Number(new URLSearchParams(location.search).get('d')??9.30);
 requestAnimationFrame(()=>requestAnimationFrame(()=>go(Number.isFinite(initial)?initial:9.30)));
})();