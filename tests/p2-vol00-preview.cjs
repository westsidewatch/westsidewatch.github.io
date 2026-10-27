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
assert.match(source,/makeSvg\('g','ws-print-hero',letters\)/,'one typographic protagonist must be built from the official SVG');
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
 ['star-rise',68],['cover-hold',82],['contents-handoff',93],['contents',100]];
const screens=[['desktop',1648,928],['tablet',768,1024],['phone',390,844],['small',320,720]];
const results=[];
const approx=(a,b,t=.01)=>Math.abs(a-b)<=t;
const data=()=> {
 const box=el=>{const r=el.getBoundingClientRect();return {x:r.x,y:r.y,width:r.width,height:r.height,right:r.right,bottom:r.bottom,top:r.top,left:r.left}};
 const stage=document.querySelector('#dual-stage');
 const hero=document.querySelector('.ws-print-hero');
 const cover=document.querySelector('#dual-cover');
 const page=document.querySelector('#dual-contents');
 const index=document.querySelector('.dual-contents__index');
 const star=document.querySelector('#dual-star');
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
  phase:stage.dataset.phase,lines:+stage.dataset.xiwangLines,
  blue:+stage.dataset.blueReveal,gold:+stage.dataset.dawnReveal,
  cover:box(cover),page:box(page),
  typeOpacity:+getComputedStyle(document.querySelector('#dual-letterfield')).opacity,
  hero:box(hero),heroOpacity:+getComputedStyle(hero).opacity,
  heroDepths:hero.querySelectorAll('.ws-print-hero__side').length,
  heroFaceUsesOfficial:hero.querySelector('.ws-print-hero__face')?.getAttribute('href')==='#ws-xiwang-original',
  heroExtrusion:+stage.dataset.xiwangExtrusion,
  starClear:+stage.dataset.xiwangStarClear,
  starNearCount:+stage.dataset.xiwangStarNear,
  starNearMaxOpacity:+stage.dataset.xiwangStarNearMax,
  lowerRegisterOpacity:+getComputedStyle(document.querySelector('.ws-print-band[data-register="7"]')).opacity,
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
   let heroAtTypeHold=0;
   for(const [label,p] of scenes){
    await page.locator('#dual-progress').evaluate((slider,value)=>{
     slider.value=String(value);slider.dispatchEvent(new Event('input',{bubbles:true}));
    },p);
    await page.waitForTimeout(90);
    const m=await page.evaluate(data);
    const faults=[];
    if(m.scrollWidth>width+2)faults.push('horizontal overflow');
    if(m.lightRegisterError>1.5||m.rightJambGap>m.rightJambTolerance||m.lightAspect!=='xMidYMin slice')
     faults.push('door right jamb and projected-light origin drift from native stone opening during page morph');
    if(!m.wallBg.includes('cover')||!m.maskSize.includes('cover')||m.mastFit!=='contain')faults.push('stone/masthead must crop proportionally');
    if(p===14&&!(m.blue>.1&&m.blue<.95&&m.gold===0&&m.cityOpacity>.6))faults.push('stone cover must enter with midnight-blue ink');
    if(p===33&&!(m.gold>.1&&m.gold<.95&&m.lines>=1&&m.typeOpacity>.25&&m.lowerRegisterOpacity>.8&&m.heroOpacity>.5))
      faults.push('bottom print register must be visible as gold sheet rises');
    if(p===33&&m.cityOpacity<.98)faults.push('no empty midnight-blue block may persist after cover arrival');
    if(p===44){
     heroAtTypeHold=m.hero.top;
     if(!(m.lines>=6&&m.starOpacity<.05&&m.typeOpacity>.8&&m.heroOpacity>.98&&m.heroDepths===21&&m.heroFaceUsesOfficial&&m.heroExtrusion>.99))
      faults.push('official 西望 must rise as one continuous 21-plane lead-type master before Morning Star');
    }
    if(p===54&&!(m.starOpacity>.1&&m.lines>=6))faults.push('Morning Star entrance missing');
    if(p===68&&!(m.starOpacity>.95&&m.typeOpacity>.45&&m.typeOpacity<.65))faults.push('real star must take focus while official print remains visible');
    if(p===68&&!(m.hero.top>heroAtTypeHold+height*.10&&m.starClear>.99&&m.starNearCount>=1&&m.starNearMaxOpacity<.34))
     faults.push('lead type must physically recede and nearby printed marks must clear the Morning Star');
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
   if(reverse.phase!=='xiwang-letterpress'||reverse.lines<1||reverse.stoneOpacity>.01)
    results.push({id:name+'-reverse',errors:['backwards scroll did not restore the original impression']});
   await page.close();
  }
  const reduced=await browser.newPage({viewport:{width:390,height:844},reducedMotion:'reduce'});
  await reduced.goto('http://127.0.0.1:4173/experiments/p2-double-square-video-lab.html?p=100',{waitUntil:'domcontentloaded'});
  const r=await reduced.evaluate(data);
  results.push({id:'reduced-motion-final',metrics:r,errors:r.entries===12&&r.stoneOpacity>.99?[]:['reduced motion hid the magazine']});
  await reduced.screenshot({path:path.join(out,'reduced-motion-final.png')});
  await reduced.close();
 }finally{await browser.close()}
 fs.writeFileSync(path.join(out,'manifest.json'),JSON.stringify({artApproval:'PENDING_EDITOR_REVIEW',scenes:results},null,2));
 if(results.some(s=>s.errors.length))process.exitCode=1;
})().catch(e=>{console.error(e);process.exitCode=1});
