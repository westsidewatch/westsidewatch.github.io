// P2 / Vol.00: visual acceptance guard, not an art-direction substitution.
// Each state is rendered in a real browser and captured for human review.
const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');

const source=fs.readFileSync('static/experiments/p2-double-square-video-lab.html','utf8');
const css=fs.readFileSync('static/css/p2-vol00-editorial.css','utf8');
const studies=fs.readFileSync('static/experiments/p2-contents-twelve.js','utf8');
const studyCss=fs.readFileSync('static/css/p2-contents-twelve.css','utf8');
const nav=JSON.parse(fs.readFileSync('data/westside-core/navigation-shell.v1.json','utf8')).firstLevel;
const out='artifacts/p2-vol00';
fs.mkdirSync(out,{recursive:true});
assert.match(source,/\/css\/westside-design-os\.css/);
assert.match(source,/\/css\/p2-vol00-editorial\.css/);
assert.match(source,/\/css\/p2-contents-twelve\.css/);
assert.match(source,/\/experiments\/p2-contents-twelve\.js/);
assert.match(studies,/const DESIGNS=\[/);
assert.match(studyCss,/\.p2x--12/);
assert.match(source,/p2-vol00-editorial\.css\?v=vol00-editorial-\d{8}[a-z]/,'the standalone folio CSS must cache-bust on visual revision');
assert.equal((source.match(/class="dual-entry"/g)||[]).length,12,'all original desks remain');
assert.equal((source.match(/class="dual-movement"/g)||[]).length,4);
assert.equal((source.match(/class="dual-work/g)||[]).length,11,'do not invent article titles');
assert.match(source,/id="ws-gate-aperture"/);
assert.match(source,/id="ws-light-floor"/);
assert.match(source,/viewBox="0 0 1448 1086" preserveAspectRatio="xMidYMin slice"/,'light must share the original wall-image coordinate system across all cover ratios');
assert.match(source,/<g clip-path="url\(#ws-gate-aperture\)">\s*<rect data-role="gate-inner-light"/,'door illumination must be clipped to the stone opening');
assert.doesNotMatch(source,/data-role="gate-arch-relief"/,'a second invented arch must never extend over the real masonry');
assert.match(source,/data-role="gate-inner-light"/);
assert.match(source,/data-role="gate-jamb-shadow"/);
assert.doesNotMatch(source,/data-role="stone-cast-shadow"|data-role="right-fold-shadow"/);
assert.match(source,/data-role="projected-light"/);
assert.match(source,/data-role="stone-cast-print"/,'light needs a masonry shadow for print contrast');
assert.match(source,/data-role="printed-light-texture"/,'the print impression must preserve graphic surface rather than imitate fog');
assert.match(source,/data-role="threshold-lit-edge"/,'door light and ground projection must share the gate threshold');
assert.doesNotMatch(source,/ws-gate-threshold-fade|ws-gate-ink-fade/,'retired mask erased the light exactly at the gate threshold');
assert.doesNotMatch(source,/data-role="inner-paper-fold"|data-role="central-light-plane"|data-role="fold-seam"/,'do not revive several faint fan wedges');
assert.doesNotMatch(source,/dual-film|dual-radiance|installV53CanvasFallback|data-cover-choice|data-position|dual-transition-water/);
assert.match(source,/\/one\/one-dore-cover-registry\.js/,'reuse the exact Doré Search canonical title catalogue');
assert.match(source,/\/one\/one-dore-assets-241\.js/,'reuse the existing exact 241-image filename registry');
assert.match(source,/CITY_PLATE_IDS=\[10,13,48,64,115,123,127,241\]/,'eight real city, city-gate, wall and New Jerusalem originals only');
assert.match(source,/PLATE_SCAN_MS=15000/,'use the original Doré Search gallery scan rhythm');
assert.match(source,/galleryAdvance|galleryLoad/,'multiple works must actually crossfade and scan, not pan one image');
assert.match(source,/dual-dore-image-a/,'first real original image buffer exists');
assert.match(source,/dual-dore-image-b/,'second crossfade image buffer exists');
assert.match(source,/GUSTAVE DORÉ/,'retained public-domain attribution is required');
assert.match(source,/id:'ws-xiwang-vertical'/,'title is the exact two original Chinese glyphs');
assert.match(source,/viewBox:'0 0 216 218'/,'Westside original 西 must have a true clipped SVG viewport');
assert.match(source,/viewBox:'216 0 216 218'/,'Westside original 望 must have a true clipped SVG viewport');
assert.match(source,/href:'#ws-xiwang-original'/,'both glyphs come only from the protected SVG');
assert.match(source,/const starRise=reduce\?/,'original Morning Star rise remains');
assert.match(source,/star\.style\.left=lerp\(15,16,stone\)/,'Morning Star holds the new upper-left station of the open Contents folio');
assert.match(css,/dual-dore-plate__image/,'same double-buffer image folio as Doré Search');
assert.match(css,/dual-contents__folio-caption/,'Contents and Doré must occupy one editorial folio');
assert.match(css,/VOL\.00 \/ CONTENTS \/ EDITORIAL COMPOSITION/,'Contents must use its newly art-directed editorial composition');
assert.match(css,/grid-template-columns:minmax\(0,39%\) minmax\(0,61%\)/,'open folio must hold monument-scale art alongside the four-movement editorial index');
assert.doesNotMatch(css,/box-shadow:inset 0 0 0 3px/,'retired inset frame must never return');
assert.doesNotMatch(css,/\.dual-contents__head,\.dual-contents__index,\.dual-contents__foot\{[^}]*background:rgba/,'Contents must not be opaque editorial cards');
assert.match(source,/galleryUpdate\(progress>=\.30\)/,'gallery must continue while Contents is open');
assert.doesNotMatch(source,/dual-dore-image"\s+src=|const artImage=document/,'retired single-image-only implementation must be absent');
assert.doesNotMatch(source,/ws-engraved-side-mask|ws-engraved-mask-step|sideSlices|heroSides|residualBands|stoneTones/,'retired sidewall overlays must not interfere with engraving');
assert.doesNotMatch(source,/starClearance|radial-gradient\(ellipse 24% 22%/,'a radial hole is not a physical Morning Star clearance');
assert.doesNotMatch(css,/ocean-rise|water-doors|p2-approved-ocean|repeating-linear-gradient\(118deg/);
assert.doesNotMatch(css,/dual-letterfield\{[^}]*drop-shadow/,'printed SVGs must stay razor-edged');
assert.match(css,/mask-size:cover,100% 100%/);
assert.match(css,/background:url\('\/p2\/magazine-cover\/p2-magazine-sandstone-wall\.png'\) center top\/cover/);
const folio=[...source.matchAll(/<button type="button" data-realm="([^"]+)" data-surface-id="([^"]+)" data-href="([^"]+)" aria-expanded="false" aria-label="展開 ([^"]+)"><span>([^<]+)<\/span><\/button>/g)];
assert.equal(folio.length,nav.length);
folio.forEach((m,i)=>{
 assert.equal(m[2],nav[i].id);
 assert.equal(m[3],nav[i].canonicalPath);
 assert.equal(m[4],nav[i].navLabel);
 assert.equal(m[5],nav[i].navLabel);
});

const scenes=[['cover',14],['type-start',33],['type-complete',44],['star-entry',54],
 ['star-rise',68],['spread-hold',79],['cover-hold',82],['contents-handoff',93],['contents',100]];
const screens=[['desktop',1648,928],['tablet',768,1024],['phone',390,844],['small',320,720]];
const results=[];
const approx=(a,b,t=.01)=>Math.abs(a-b)<=t;
const data=()=> {
 const box=el=>{const r=el.getBoundingClientRect();return {x:r.x,y:r.y,width:r.width,height:r.height,right:r.right,bottom:r.bottom,top:r.top,left:r.left}};
 const stage=document.querySelector('#dual-stage');
 const hero=document.querySelector('.ws-print-hero');
 const face=hero.querySelector('.ws-print-hero__face');
 const galleryImages=[...document.querySelectorAll('.dual-dore-plate__image')];
 const activeArt=galleryImages.find(img=>img.classList.contains('is-active'));
 const artPlate=document.querySelector('#dual-dore-plate');
 const cover=document.querySelector('#dual-cover');
 const page=document.querySelector('#dual-contents');
 const index=document.querySelector('#p2-contents-design');
 const star=document.querySelector('#dual-star');
 // An SVG <use> contains an invisible uncropped 432px source. Only
 // the transformed 216×454 official two-glyph viewport is visible.
 const mx=hero.getScreenCTM();
 const corners=[[0,0],[216,0],[216,454],[0,454]]
  .map(([x,y])=>new DOMPoint(x,y).matrixTransform(mx));
 const xs=corners.map(p=>p.x),ys=corners.map(p=>p.y);
 const left=Math.min(...xs),right=Math.max(...xs),top=Math.min(...ys),bottom=Math.max(...ys);
 const heroRect={x:left,y:top,left,top,right,bottom,width:right-left,height:bottom-top};
 const starRect=box(star),pageRect=box(page);
 const zone=document.querySelector('#p2-contents-design');
 const city=document.querySelector('#dual-cover-city');
 const lightSvg=document.querySelector('#dual-cover-folded-light');
 const cityBox=city.getBoundingClientRect();
 const scale=Math.max(cityBox.width/1448,cityBox.height/1086);
 const rightInk=new DOMPoint(839,759).matrixTransform(lightSvg.getScreenCTM());
 const alignedRight={x:cityBox.left+(cityBox.width-1448*scale)/2+839*scale,y:cityBox.top+759*scale};
 const registerError=Math.hypot(rightInk.x-alignedRight.x,rightInk.y-alignedRight.y);
 const wallRightPost=cityBox.left+(cityBox.width-1448*scale)/2+844*scale;
 const columns=[...document.querySelectorAll('#p2-contents-design .p2x-movement')];
 const secondary=[...document.querySelectorAll(
  '#p2-contents-design .p2x-movement h3,#p2-contents-design .p2x-zh,#p2-contents-design .p2x-en,#p2-contents-design .p2x-works'
 )];
 return {
  phase:stage.dataset.phase,impression:+stage.dataset.xiwangImpression,inkPlate:stage.dataset.xiwangPlate,
  titleOrientation:stage.dataset.xiwangTitleOrientation,
  dorePlateId:artPlate.dataset.plateId,
  dorePlateChanges:+artPlate.dataset.plateChanges,
  galleryIds:window.P2DoreGallery?.items,
  galleryCycle:window.P2DoreGallery?.state?.cycleMs,
  doreVisible:+getComputedStyle(artPlate).opacity,
  doreReady:!!activeArt&&activeArt.complete&&activeArt.naturalWidth>=700,
  doreSource:activeArt?.currentSrc||'',
  doreLayerCount:galleryImages.length,
  doreCurrentId:activeArt?.dataset.doreId||'',
  doreCredit:document.querySelector('#dual-dore-plate-credit')?.textContent||'',
  blue:+stage.dataset.blueReveal,gold:+stage.dataset.dawnReveal,
  cover:box(cover),page:box(page),
  typeOpacity:+getComputedStyle(document.querySelector('#dual-letterfield')).opacity,
  hero:heroRect,heroOpacity:+getComputedStyle(hero).opacity,
  officialGlyphs:document.querySelectorAll('#ws-xiwang-vertical use').length,
  titleAspect:heroRect.height/Math.max(heroRect.width,1),
  starLeftRatio:(starRect.left-pageRect.left)/pageRect.width,
  starTopRatio:(starRect.top-pageRect.top)/pageRect.height,
  starTitleRightGap:heroRect.left-starRect.right,
  heroFaceUsesOfficial:hero.querySelector('.ws-print-hero__face')?.getAttribute('href')==='#ws-xiwang-vertical',
  titleTopRatio:(heroRect.top-pageRect.top)/pageRect.height,
  titleBottomClear:pageRect.bottom-heroRect.bottom,
  starTitleGap:heroRect.top-starRect.bottom,
  starTitleXDelta:Math.abs((heroRect.left+heroRect.right)/2-(starRect.left+starRect.right)/2)/pageRect.width,
  lightOpacity:+getComputedStyle(document.querySelector('#dual-cover-folded-light')).opacity,
  cityOpacity:+getComputedStyle(document.querySelector('#dual-cover-city')).opacity,
  stoneOpacity:+getComputedStyle(document.querySelector('#dual-stone-contents')).opacity,
  starOpacity:+getComputedStyle(star).opacity,
  starRenderer:star.dataset.renderer,
  approvedStarVisible:!!star.querySelector('img.dual-cover__approved-star')&&getComputedStyle(star).opacity==='1',
  star:box(star),zone:box(zone),movements:columns.map(box),
  witnessLast:box(document.querySelector('#p2-contents-design .p2x-movement:nth-child(3) .p2x-entry:last-child')||index),
  witnessInterlude:box(document.querySelector('#p2-contents-design .p2x-movement:nth-child(3) .p2x-interlude')||index),
  worshipHeading:box(document.querySelector('#p2-contents-design .p2x-movement:nth-child(4) h3')||index),
  headings:[...document.querySelectorAll('.dual-cover__en span')].map(el=>el.textContent.trim()),
  title:box(document.querySelector('.dual-cover__editorial')),
  mast:box(document.querySelector('.dual-cover__mast')),
  mastOpacity:+getComputedStyle(document.querySelector('.dual-cover__mast')).opacity,
  volumeOpacity:+getComputedStyle(document.querySelector('.dual-cover__vol')).opacity,
  volumeFontSize:parseFloat(getComputedStyle(document.querySelector('.dual-cover__vol')).fontSize),
  volumeInk:getComputedStyle(document.querySelector('.dual-cover__vol')).color,
  secondaryWeights:[...new Set(secondary.map(el=>getComputedStyle(el).fontWeight))],
  majorWeight:getComputedStyle(document.querySelector('.dual-contents__head h2')).fontWeight,
  entries:document.querySelectorAll('.dual-movement li').length,
  last:box(document.querySelector('#p2-contents-design .p2x-movement:last-child .p2x-entry:last-child')||index),
  index:box(index),scrollHeight:index.scrollHeight,clientHeight:index.clientHeight,
  insideContents:!document.querySelector('#dual-stone-contents').inert,
  rail:box(document.querySelector('#dual-continuum')),
  railOpacity:+getComputedStyle(document.querySelector('#dual-continuum')).opacity,
  wallBg:getComputedStyle(document.querySelector('#dual-cover-wall')).backgroundSize,
  lightRegisterError:registerError,
  rightJambGap:Math.abs(rightInk.x-wallRightPost),
  rightJambTolerance:6*scale,
  lightViewBox:lightSvg.getAttribute('viewBox'),
  lightAspect:lightSvg.getAttribute('preserveAspectRatio'),
  maskSize:getComputedStyle(document.querySelector('#dual-cover-wall')).maskSize,
  mastFit:getComputedStyle(document.querySelector('.dual-cover__mast')).objectFit,
  scrollWidth:document.documentElement.scrollWidth,
  naturalWall:true,
  ariaHead:document.querySelector('#dual-contents-title').textContent.trim(),
  canKeyboardScroll:!!document.querySelector('#p2-contents-design [tabindex="0"]'),
  designId:document.querySelector('#dual-contents').dataset.p2Design,
  liveEntries:document.querySelectorAll('#p2-contents-design .p2x-entry').length,
  liveMovements:columns.length,
  availableDesigns:window.P2ContentsTwelve?.designs.length||0,
  layoutVisible:getComputedStyle(index).display!=='none',
  reliefOpacity:+getComputedStyle(document.querySelector('#dual-contents-relief')).opacity,
  foldSurface:getComputedStyle(page,'::after').backgroundImage
 };
};

(async()=>{
 const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
 try{
  for(const [name,width,height] of screens){
   const page=await browser.newPage({viewport:{width,height},reducedMotion:'no-preference'});
   const pageErrors=[];
   page.on('pageerror',e=>pageErrors.push(e.message));
   await page.goto('http://127.0.0.1:4173/experiments/p2-double-square-video-lab.html?p=0&side=cover-right',{waitUntil:'domcontentloaded',timeout:45000});
   await page.evaluate(()=>document.fonts.ready);
   // The first original is loaded only when the multi-plate folio becomes visible.
   let heroAtTypeHold=0;
   for(const [label,p] of scenes){
    await page.locator('#dual-progress').evaluate((slider,value)=>{
     slider.value=String(value);slider.dispatchEvent(new Event('input',{bubbles:true}));
    },p);
    if(p===33){
     await page.waitForFunction(()=>window.P2DoreGallery?.state.ready,null,{timeout:16000});
    }
    await page.waitForTimeout(90);
    const m=await page.evaluate(data);
    const faults=[];
    if(m.scrollWidth>width+2)faults.push('horizontal overflow');
    if(m.lightRegisterError>1.5||m.rightJambGap>m.rightJambTolerance||m.lightAspect!=='xMidYMin slice')
     faults.push('door right jamb and projected-light origin drift from native stone opening during page morph');
    if(!m.wallBg.includes('cover')||!m.maskSize.includes('cover')||m.mastFit!=='contain')faults.push('stone/masthead must crop proportionally');
    if(p===14&&!(m.blue>.1&&m.blue<.95&&m.gold===0&&m.cityOpacity>.6))faults.push('stone cover must enter with midnight-blue ink');
    if(p===33&&!(m.gold>.1&&m.gold<.95&&m.typeOpacity>.20&&m.heroOpacity>.25&&m.doreVisible>.1))
     faults.push('original Doré folio and official Xi Wang should enter with dawn reveal');
    if(p===33&&m.cityOpacity<.98)faults.push('do not leave empty right-cover midnight-blue block');
    if([44,54,68,79,82].includes(p)&&(!m.doreReady||m.doreLayerCount!==2||!m.doreCredit.includes(String(m.doreCurrentId).padStart(3,'0'))))
     faults.push('actual unmodified public-domain Doré plate failed to load');
    if(p===44){
     heroAtTypeHold=m.hero.top;
     if(!(m.starOpacity<.05&&m.typeOpacity>.98&&m.heroOpacity>.98&&m.officialGlyphs===2&&m.heroFaceUsesOfficial&&m.inkPlate==='official-svg-vertical-dore-city-gallery'&&m.titleOrientation==='vertical'&&m.titleAspect>1.7))
      faults.push('large vertical original 西望 must hold over full bleed Doré plate before Morning Star enters');
    }
    if(p===54&&!(m.starOpacity>.1&&m.typeOpacity>.8))
     faults.push('protected Morning Star must begin rising over Doré plate');
    if(p===68&&!(m.starOpacity>.95&&m.typeOpacity>.98&&m.starTopRatio<.25))
     faults.push('Morning Star must finish rising toward upper-left, with vertical title readable');
    if(p===79&&name==='desktop'){
     // Prove the folio actually changes between TWO DIFFERENT DORÉ WORKS.
     const first=await page.evaluate(()=>window.P2DoreGallery.state);
     // The plate *itself* must move while held, not merely flash a next source.
     const scanFrom=await page.evaluate(()=>{
      const img=document.querySelector('.dual-dore-plate__image.is-active');
      return {matrix:getComputedStyle(img).transform,transition:getComputedStyle(img).transitionDuration};
     });
     await page.waitForTimeout(1100);
     const scanTo=await page.evaluate(()=>{
      const img=document.querySelector('.dual-dore-plate__image.is-active');
      return {matrix:getComputedStyle(img).transform,transition:getComputedStyle(img).transitionDuration};
     });
     if(scanFrom.matrix===scanTo.matrix||!scanTo.transition.includes('15s'))
      faults.push('Doré Search plate must visibly scroll within its own image for 15 seconds');
     // Capture the FIRST gallery state before advancing. Otherwise the
     // normal p79 screenshot is taken after the swap and cannot prove
     // that two distinct compositions were ever shown.
     const firstFrame=await page.locator('#dual-dore-plate').screenshot({
      path:path.join(out,'desktop-city-first-plate.png'),animations:'allow'
     });
     const switched=await page.evaluate(()=>window.P2DoreGallery.next());
     if(!switched)faults.push('second authentic city/wall engraving did not load');
     else {
      // Prove a visibly completed crossfade, not only a network response.
      await page.waitForTimeout(1150);
      const second=await page.evaluate(data);
      if(first.id===+second.doreCurrentId||second.dorePlateChanges<1||!second.doreReady)
       faults.push('gallery must change the actual source image and maintain a real loaded image');
      if(second.galleryCycle!==15000||second.galleryIds.join('|')!=='10|13|48|64|115|123|127|241')
       faults.push('Doré image cycle must use eight curated canonical city IDs and original scan timing');
      const secondFrame=await page.locator('#dual-dore-plate').screenshot({
       path:path.join(out,'desktop-city-second-plate.png'),animations:'allow'
      });
      if(firstFrame.equals(secondFrame))
       faults.push('visual proof FAIL: two different registry IDs produced the same image pixels');
     }
    }
    if(p===79||p===82){
     if(!(m.starOpacity>.98&&m.typeOpacity>.98&&m.heroOpacity>.99&&m.doreVisible>.90))
      faults.push('held spread must retain the star, original large title and complete Doré image');
     if(!(m.starLeftRatio>=-.01&&m.starLeftRatio<.19&&m.starTopRatio>=-.01&&m.starTopRatio<.20))
      faults.push('rising Morning Star must land in the upper-left editorial space');
     if(!(m.starTitleRightGap>m.page.width*.025&&m.titleBottomClear>m.page.height*.035&&m.titleAspect>1.7))
      faults.push('upper-left Morning Star must not collide with vertical original ink title');
    }
    if(p===82&&!(m.lightOpacity>.94&&m.mastOpacity>.98&&m.volumeOpacity>.98&&m.headings.join('|')==='CITY|OF|LIGHT'))
      faults.push('cover hold must carry a fully legible masthead and issue number with the gate light');
    if(p===93&&!(m.stoneOpacity>.1&&m.stoneOpacity<.99))faults.push('Contents must hand off through a measured state');
    if(p===100){
     if(!m.designId||m.designId!=='10'||!m.layoutVisible)
      faults.push('the chosen Cereal engraved-light Contents must be the default editorial design');
     if(m.liveEntries!==12||m.liveMovements!==4||m.availableDesigns!==12)
      faults.push('all twelve desk entries and all twelve independent layouts must be accessible');
     if(m.starRenderer==='approved-morning-star-svg'&&!m.approvedStarVisible)
      faults.push('approved vector Morning Star fallback missing without WebGL');
     if(!approx(m.cover.width/m.cover.height,5/8,.01)||!approx(m.page.width/m.page.height,1,.01))
      faults.push('5:8 cover and 1:1 Contents');
     if(m.entries!==12||m.ariaHead!=='Contents.')
      faults.push('Contents canon');
     if(m.majorWeight!=='400'||m.secondaryWeights.some(x=>+x>200))
      faults.push('Contents secondary must be 200');
     if(m.volumeFontSize<10||m.volumeInk!=='rgb(255, 248, 233)'||m.volumeOpacity<.99)
      faults.push('Vol.00 metadata must be readable over the protected stone cover');
     if(!m.insideContents||m.stoneOpacity<.999||m.typeOpacity<.98||m.doreVisible<.98)
      faults.push('Contents must preserve the original Doré and vertical Xi Wang visual');
     if(m.railOpacity<.98)faults.push('seven-colour ribbon missing');
     if(!m.canKeyboardScroll)faults.push('editorial index needs keyboard-scrolling access');
    }
    if(p===100){
     const editorial=await page.evaluate(()=>{
      const host=document.querySelector(".p2x--10");
      if(!host)return {missing:true};
      const box=e=>e.getBoundingClientRect();
      const header=host.querySelector(".p2x-cereal-header");
      const nav=host.querySelector(".p2x-cereal-nav");
      const rail=host.querySelector(".p2x-cereal-paper");
      const stack=host.querySelector(".p2x-cereal-stack");
      const chapters=[...host.querySelectorAll(".p2x-cereal-movement")];
      const items=[...host.querySelectorAll(".p2x-entry")];
      const title=host.querySelector(".p2x-cereal-header h2");
      const star=document.querySelector("#dual-star");
      const hero=document.querySelector(".ws-print-hero");
      const glyphFace=hero.querySelector(".ws-print-hero__face");
      const glyphCTM=glyphFace.getScreenCTM();
      const pts=[[0,0],[216,0],[216,454],[0,454]]
       .map(([x,y])=>new DOMPoint(x,y).matrixTransform(glyphCTM));
      const glyphRight=Math.max(...pts.map(p=>p.x));
      const glyphTop=Math.min(...pts.map(p=>p.y));
      const glyphBottom=Math.max(...pts.map(p=>p.y));
      const railLeft=box(rail).left;
      const positions=chapters.map(el=>({top:box(el).top,bottom:box(el).bottom,height:box(el).height}));
      const interludeOverlaps=chapters.some(section=>{
       const p=section.querySelector(".p2x-interlude");
       const last=section.querySelector(".p2x-entry:last-child");
       return !!(p&&last&&box(p).top<box(last).bottom-1);
      });
      const itemOverlap=chapters.some(section=>{
       const es=[...section.querySelectorAll(".p2x-entry")];
       return es.slice(1).some((e,i)=>box(e).top<box(es[i]).bottom-1);
      });
      const chaptersOverlap=positions.slice(1).some((p,i)=>p.top<positions[i].bottom+1);
      // Reachability is a real scroll test, not a claim based on DOM count.
      stack.scrollTo({top:stack.scrollHeight,behavior:'instant'});
      const lastItem=items.at(-1);
      const endReachable=box(lastItem).bottom<=box(stack).bottom+2;
      stack.scrollTo({top:0,behavior:'instant'});
      const trace=[...host.querySelectorAll(".p2x-etch-line")];
      const reduced=matchMedia("(prefers-reduced-motion: reduce)").matches;
      return {
       missing:false,chapters:chapters.length,items:items.length,
       navigators:host.querySelectorAll("[data-p2-cereal-jump]").length,
       traceCount:trace.length,traceAnimation:getComputedStyle(trace[0]).animationName,
       scrollerKeyboard:stack.tabIndex>=0,scrollable:stack.scrollHeight>stack.clientHeight+5,
       endReachable,titleReadable:box(title).width<=box(rail).width+1,
       noHeaderNavOverlap:box(nav).top>=box(header).bottom-1,
       noNavIndexOverlap:box(stack).top>=box(nav).bottom-1,
       noGlyphTextCollision:glyphRight<railLeft-6 || glyphBottom<box(rail).top || glyphTop>box(rail).bottom,
       noStarTextCollision:box(star).right<railLeft-5 || box(star).bottom<box(rail).top,
       interludeOverlaps,itemOverlap,chaptersOverlap,reduced
      };
     });
     if(editorial.missing||editorial.chapters!==4||editorial.items!==12||editorial.navigators!==4)
      faults.push('Cereal must contain a real 12-desk reading index with four jump controls');
     if(editorial.traceCount!==3||editorial.traceAnimation==='none'&&!editorial.reduced)
      faults.push('09 gold orbit must be distilled into three living 10 etched engraving paths');
     if(!editorial.scrollerKeyboard||!editorial.scrollable||!editorial.endReachable)
      faults.push('all twelve titles must remain reachable inside the index, with keyboard support');
     if(!editorial.titleReadable||!editorial.noHeaderNavOverlap||!editorial.noNavIndexOverlap)
      faults.push('Contents heading, chapter navigation or first article text collide');
     if(editorial.itemOverlap||editorial.chaptersOverlap||editorial.interludeOverlaps)
      faults.push('article rows, movement sections or interludes physically overlap');
     if(!editorial.noGlyphTextCollision||!editorial.noStarTextCollision)
      faults.push('protected Xi Wang SVG or Morning Star collides with the Contents reading region');
    }
    if(p===100){
     // The original square is physically constrained on phones. Readers
     // must still have a full-size, keyboard-usable 12-desk dialogue.
     const full=page.locator(".p2x-cereal-expand");
     if(await full.count()){
      await full.click({timeout:4000});
      const reader=await page.locator(".p2-cereal-reader").evaluate(el=>({
       open:el.getAttribute("aria-modal")==="true",
       items:el.querySelectorAll(".p2x-entry").length,
       chapters:el.querySelectorAll(".p2x-cereal-movement").length,
       scrollHeight:el.scrollHeight,clientHeight:el.clientHeight,
       width:el.getBoundingClientRect().width
      }));
      if(!reader.open||reader.items!==12||reader.chapters!==4||reader.width<width*.9)
       faults.push('full-size responsive reader must display all twelve canonical desks');
      await page.keyboard.press("Escape");
      if(await page.locator(".p2-cereal-reader").count())
       faults.push('full-size responsive reader must close with Escape');
     }else faults.push('missing full-size accessible index action');
    }
    if(pageErrors.length)faults.push('PAGE_ERROR '+pageErrors.join('; '));
    await page.screenshot({path:path.join(out,name+'-'+label+'.png'),animations:'allow'});
    results.push({id:name+'-'+label,metrics:m,errors:faults});
    console.log(name,label,faults.length?faults:'CAPTURE_OK');
   }
   // No duplicate clock: reversing the ONE slider restores same visual state.
   await page.locator('#dual-progress').evaluate(slider=>{slider.value='33';slider.dispatchEvent(new Event('input',{bubbles:true}))});
   const reverse=await page.evaluate(data);
   if(reverse.phase!=='xiwang-letterpress'||reverse.inkPlate!=='official-svg-vertical-dore-city-gallery'||reverse.doreVisible<.2||reverse.stoneOpacity>.01)
    results.push({id:name+'-reverse',errors:['backwards scroll did not restore the original impression']});
   await page.close();
  }
   const reduced=await browser.newPage({viewport:{width:390,height:844},reducedMotion:'reduce'});
   await reduced.goto('http://127.0.0.1:4173/experiments/p2-double-square-video-lab.html?p=14',{waitUntil:'domcontentloaded'});
   // Reduced motion stays on the first real artwork, without any timers.
   for(const p of [14,44,79,100]){
    await reduced.locator('#dual-progress').evaluate((slider,value)=>{
     slider.value=String(value);slider.dispatchEvent(new Event('input',{bubbles:true}));
    },p);
    if(p===44)await reduced.waitForFunction(()=>window.P2DoreGallery?.state.ready,null,{timeout:16000});
    const r=await reduced.evaluate(data),faults=[];
    if((p===44||p===79)&&!r.doreReady)faults.push('reduced motion must still show the real Doré original');
    if(r.starRenderer!=='approved-morning-star-svg-reduced')
     faults.push('reduced motion must use the official static star');
    if(p===14&&!(r.blue>.99&&r.starOpacity<.01))
     faults.push('reduced motion must show the intact cover');
    if(p===44&&!(r.typeOpacity>.99&&r.starOpacity<.01&&r.heroOpacity>.99))
     faults.push('reduced motion must show the official title');
    if(p===79&&!(r.starOpacity>.99&&r.typeOpacity>.9&&r.starLeftRatio<.19&&r.starTitleRightGap>r.page.width*.02))
     faults.push('reduced Morning Star must stay upper-left without covering vertical title');
    if(p===100&&!(r.entries===12&&r.stoneOpacity>.99&&r.insideContents))
     faults.push('reduced motion must keep all 12 Contents entries');
    results.push({id:'reduced-'+p,metrics:r,errors:faults});
    await reduced.screenshot({path:path.join(out,'reduced-'+p+'.png'),animations:'allow'});
   }
   await reduced.close();
   // Twelve independently constructed Contents: real Chromium proof at
   // each variant, not a color swatch or thumbnail mockup.
   const twelve=await browser.newPage({viewport:{width:1648,height:928},reducedMotion:'no-preference'});
   const twelveErrors=[];
   twelve.on('pageerror',e=>twelveErrors.push(e.message));
   await twelve.goto('http://127.0.0.1:4173/experiments/p2-double-square-video-lab.html?p=100&side=cover-right&variant=10',
    {waitUntil:'domcontentloaded',timeout:45000});
   await twelve.evaluate(()=>document.fonts.ready);
   await twelve.waitForFunction(()=>window.P2ContentsTwelve?.count===12,null,{timeout:16000});
   const frames=[];
   for(const design of windowDesignIds()){
    await twelve.evaluate(id=>window.P2ContentsTwelve.select(id,false),design);
    await twelve.waitForTimeout(120);
    const m=await twelve.evaluate(()=>{
     const host=document.querySelector('#p2-contents-design');
     const page=document.querySelector('#dual-contents');
     const bounds=host.getBoundingClientRect(),p=page.getBoundingClientRect();
     return {id:window.P2ContentsTwelve.active,count:window.P2ContentsTwelve.count,
      groups:host.querySelectorAll('.p2x-movement').length,
      source:window.P2ContentsTwelve.designs.find(x=>x.id===window.P2ContentsTwelve.active).source,
      width:bounds.width,height:bounds.height,localX:bounds.left-p.left,overflow:document.documentElement.scrollWidth>innerWidth+2};
    });
    const errors=[];
    if(m.id!==design||m.count!==12||m.groups!==4||m.width<300||m.height<300||m.overflow)
     errors.push('variant does not deliver a complete independent 12-entry composition');
    if(twelveErrors.length)errors.push('PAGE_ERROR '+twelveErrors.join('; '));
    const snap=await twelve.screenshot({path:path.join(out,'twelve-'+design+'-desktop.png'),animations:'allow'});
    if(frames.some(f=>f.equals(snap)))errors.push('variant screenshot is pixel-identical to an earlier composition');
    frames.push(snap);results.push({id:'twelve-'+design,metrics:m,errors});
    console.log('twelve',design,m.source,errors.length?errors:'CAPTURE_OK');
   }
   await twelve.close();
   function* windowDesignIds(){for(let i=1;i<=12;i++)yield String(i).padStart(2,'0')}
 }finally{await browser.close()}
 fs.writeFileSync(path.join(out,'manifest.json'),JSON.stringify({artApproval:'PENDING_EDITOR_REVIEW',scenes:results},null,2));
 if(results.some(s=>s.errors.length))process.exitCode=1;
})().catch(e=>{console.error(e);process.exitCode=1});
