// P2 / Vol.00: visual acceptance guard, not an art-direction substitution.
// Each state is rendered in a real browser and captured for human review.
const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');

const source=fs.readFileSync('static/experiments/p2-double-square-video-lab.html','utf8');
const css=fs.readFileSync('static/css/p2-vol00-editorial.css','utf8');
const nav=JSON.parse(fs.readFileSync('data/westside-core/navigation-shell.v1.json','utf8')).firstLevel;
const out='artifacts/p2-vol00';
fs.mkdirSync(out,{recursive:true});
assert.match(source,/\/css\/westside-design-os\.css/);
assert.match(source,/\/css\/p2-vol00-editorial\.css/);
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
assert.match(source,/star\.style\.left=lerp\(15,50,stone\)/,'Morning Star rises to editorial upper-left');
assert.match(css,/dual-dore-plate__image/,'same double-buffer image folio as Doré Search');
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
 const index=document.querySelector('.dual-contents__index');
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
 const zone=document.querySelector('.dual-contents__star-zone');
 const city=document.querySelector('#dual-cover-city');
 const lightSvg=document.querySelector('#dual-cover-folded-light');
 const cityBox=city.getBoundingClientRect();
 const scale=Math.max(cityBox.width/1448,cityBox.height/1086);
 const rightInk=new DOMPoint(839,759).matrixTransform(lightSvg.getScreenCTM());
 const alignedRight={x:cityBox.left+(cityBox.width-1448*scale)/2+839*scale,y:cityBox.top+759*scale};
 const registerError=Math.hypot(rightInk.x-alignedRight.x,rightInk.y-alignedRight.y);
 const wallRightPost=cityBox.left+(cityBox.width-1448*scale)/2+844*scale;
 const columns=[...document.querySelectorAll('.dual-movement')];
 const secondary=[...document.querySelectorAll(
  '.dual-contents__head span,.dual-movement h3,.dual-movement h3 em,.dual-movement li,.dual-movement li b,.dual-entry__column,.dual-entry__column small,.dual-work,.dual-movement__interlude,.dual-contents__foot'
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
  witnessLast:box(document.querySelector('.dual-movement:nth-child(3) .dual-entry:last-child')),
  witnessInterlude:box(document.querySelector('.dual-movement:nth-child(3) .dual-movement__interlude')),
  worshipHeading:box(document.querySelector('.dual-movement:nth-child(4) h3')),
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
  last:box(document.querySelector('.dual-movement:last-child li:last-child')),
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
  canKeyboardScroll:index.tabIndex===0,
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
     // Capture the FIRST gallery state before advancing. Otherwise the
     // normal p79 screenshot is taken after the swap and cannot prove
     // that two distinct compositions were ever shown.
     const firstFrame=await page.locator('#dual-dore-plate').screenshot({
      path:path.join(out,'desktop-city-first-plate.png'),animations:'disabled'
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
       path:path.join(out,'desktop-city-second-plate.png'),animations:'disabled'
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
     if(width>1100){
      const [watch,walk,witness,worship]=m.movements;
      if(!(watch.left<walk.left&&walk.left<witness.left&&Math.abs(witness.left-worship.left)<2&&worship.top-witness.bottom>=6&&worship.top-witness.bottom<=20))
       faults.push('desktop Contents needs two long columns and a visibly separated stacked third column');
      if(m.worshipHeading.top-m.witnessInterlude.bottom<6)
       faults.push('WITNESS interlude must not collide with WORSHIP heading');
     }
     if(m.witnessInterlude.top-m.witnessLast.bottom<3)
      faults.push('WITNESS interlude overlaps its final editorial entry');
     if(m.starRenderer==='approved-morning-star-svg'&&!m.approvedStarVisible)faults.push('approved vector Morning Star fallback missing without WebGL');
     if(!approx(m.cover.width/m.cover.height,5/8,.01)||!approx(m.page.width/m.page.height,1,.01))faults.push('5:8 cover and 1:1 Contents');
     if(m.entries!==12||m.ariaHead!=='Contents.')faults.push('Contents canon');
     if(m.majorWeight!=='400'||m.secondaryWeights.some(x=>+x>200))faults.push('Contents secondary must be 200');
     if(m.volumeFontSize<10||m.volumeInk!=='rgb(255, 248, 233)'||m.volumeOpacity<.99)
      faults.push('Vol.00 metadata must be readable over the now-dark stone cast shadow');
     if(!m.insideContents||m.stoneOpacity<.999||m.typeOpacity>.02)faults.push('old type must yield to stone Contents');
     if(m.star.top<m.zone.top-4||m.star.bottom>m.zone.bottom+4)faults.push('star intrudes into reading zone');
     if(m.last.bottom>m.index.bottom+1&&!m.canKeyboardScroll)faults.push('last article not keyboard-reachable');
     if(m.railOpacity<.98)faults.push('seven-colour ribbon missing');
    }
    if(pageErrors.length)faults.push('PAGE_ERROR '+pageErrors.join('; '));
    await page.screenshot({path:path.join(out,name+'-'+label+'.png'),animations:'disabled'});
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
    await reduced.screenshot({path:path.join(out,'reduced-'+p+'.png'),animations:'disabled'});
   }
   await reduced.close();
 }finally{await browser.close()}
 fs.writeFileSync(path.join(out,'manifest.json'),JSON.stringify({artApproval:'PENDING_EDITOR_REVIEW',scenes:results},null,2));
 if(results.some(s=>s.errors.length))process.exitCode=1;
})().catch(e=>{console.error(e);process.exitCode=1});
