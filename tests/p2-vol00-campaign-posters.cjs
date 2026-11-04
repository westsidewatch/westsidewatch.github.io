// P2 A scroll-linked ink/paper registration + B alternate vector + native film.
// The retired sevenfold curtain is intentionally absent from Magazine;
// the homepage's separate sevenfold motion is unaffected.
const assert=require('node:assert/strict');
const fs=require('node:fs');
const {chromium}=require('playwright');
const {PNG}=require('pngjs');
fs.mkdirSync('artifacts/p2-vol00',{recursive:true});
const poster=fs.readFileSync('static/js/p2-vol00-poster.js','utf8');
const css=fs.readFileSync('static/css/p2-vol00-poster.css','utf8');
const html=fs.readFileSync('static/experiments/p2-double-square-video-lab.html','utf8');
const bridge=fs.readFileSync('static/js/p2-magazine-live-bridge.js','utf8');
const emmausTransition=fs.readFileSync('static/js/p2-emmaus-olive-preview.js','utf8');
const emmausTheme=fs.readFileSync('static/css/p2-emmaus-theme-verse.css','utf8');
const os=fs.readFileSync('static/css/westside-design-os.css','utf8');
const glyph=fs.readFileSync('static/images/xiwang-poster-a-glyph-mask.svg','utf8');
const masterB=fs.readFileSync('static/images/xiwang-poster-b-v2.svg','utf8');

assert.match(html,/p2-vol00-poster\.js/,'P2 loads the campaign poster state controller');
assert.match(html,/p2-vol00-poster\.css/,'P2 loads isolated poster CSS');
assert.match(poster,/poster'\)==='legacy'/,'legacy reference stays available');
const tokens=['--ws-water','--ws-first-light','--ws-pale-gold','--ws-olive','--ws-harvest','--ws-crimson','--ws-daylight-mauve'];
for(const token of tokens) {
 assert(poster.includes("token:'"+token+"'"),'missing P2 poster palette '+token);
 assert(os.includes(token+':'),'missing Design OS palette token '+token);
}
assert.match(poster,/function paint\(progress\)/,'poster has one externally owned scroll progress');
assert.match(html,/window\.P2Vol00Poster\?\.paint\(progress\)/,'P2 calls same progress painter');
assert.match(bridge,/westside-p2-dual-progress/,'full P2 uses existing parent scroll bridge');
assert.doesNotMatch(emmausTransition,/function ensureMagazinePrologue/,'no redundant 經上所指 interleaf');
assert.match(emmausTransition,/const firstAngle=-172\*smooth\(move\)/,'entire cover rotates beyond edge-on rather than disappearing at 86 degrees');
assert.match(emmausTransition,/p2-emmaus-turning::after/,'page has real verso throughout second half of flip');
assert.match(emmausTransition,/magazineUnderlay.style.display=move>/,'ONE scripture leaf hides entirely before page turn');
assert.match(emmausTheme,/font-weight:var\(--ws-weight-zh-air,200\)!important/,'Emmaus CLOTH COVER quotation uses user-selected Chiron ultra-light 200');
assert.match(emmausTransition,/sourceTile\.style\.clipPath=oneDrop>/,'native Magazine Contents exits through physical mask, not opacity');
assert.match(emmausTransition,/emLeft\.style\.clipPath=oneDrop/,'incoming ONE page enters with opposing scroll clip');
assert.match(emmausTransition,/emLeft\.style\.opacity=oneDrop>/,'incoming ONE page is opaque, not translucent ghost');
assert.match(emmausTheme,/font-style:italic!important/,'English Scripture reference is genuine OS Bodoni Italic');
assert.match(html,/stage\.addEventListener\('wheel'/,'standalone preview can scrub with wheel');
assert.match(html,/!document\.documentElement\.classList\.contains\('dual-embed'\)/,
 'standalone wheel event does not steal parent P2 wheel');
assert.doesNotMatch(poster,/xw-poster__folds|xw-poster__fold'/,'previous seven full-sheet curtain removed');
assert.match(poster,/posterFoldCount='0'/,'observability declares curtain removed');
assert.match(poster,/poster-a-night-blue-approved-p2\.svg/,'A retains approved original silhouette fallback');
assert.match(css,/xiwang-poster-a-glyph-mask\.svg/,'colorful ink and foil are masked by the actual two glyph paths');
assert.equal((glyph.match(/<path\b/g)||[]).length,2,'A glyph mask has separate 西 and 望 paths');
assert.doesNotMatch(glyph,/<rect\b/,'mask must not cover the background');
assert.match(css,/xw-poster__glyph--foil/,'final print has stable metallic foil');
assert.match(poster,/var\(--ws-morning-gold/,'final ink uses OS dawn-gold');
assert.match(poster,/var\(--ws-night/,'final background uses OS midnight navy');
assert.match(poster,/Watch for the Dawn/,'minimal editorial slogan remains');
assert.match(html,/ease\(\(progress-\.97\)\/\.03\)/,
 'A spread shrinks only after the actual Contents has completed its entrance');
assert.match(html,/ease\(\(progress-\.88\)\/\.07\)/,
 'original Contents enters AFTER the poster is finalized');
assert.match(css,/display:block!important;z-index:9/,
 'A reinstates the original 12-desk Contents instead of force hiding it');
assert.match(html,/posterSpread\.style\.transform='scale\('/,'no separate shrinking of cover or poster');
assert.match(css,/@keyframes xw-corner-slow-neon/,'the only new timed color loop belongs to the small editorial wordmark');
assert.doesNotMatch(poster,/setInterval|requestAnimationFrame/,'monumental scroll-printed art cannot have its own timer');
assert.match(poster,/xiwang-poster-b-v2\.svg/,'B remains a separately authored native SVG');
assert.equal((masterB.match(/data-poster-word="[1-7]"/g)||[]).length,7,
 'B still contains seven independently authored word groups');
assert.equal(new Set([...masterB.matchAll(/data-engraving-family="([^"]+)"/g)].map(m=>m[1])).size,7,
 'seven B groups still have different actual engraving methods');

(async()=>{
const browser=await chromium.launch({headless:true});
try{
 for(const mode of ['a','b']){
  for(const [width,height] of [[1648,928],[390,844]]){
   const page=await browser.newPage({viewport:{width,height},reducedMotion:'no-preference'});
   try{
    const url='http://127.0.0.1:4173/experiments/p2-double-square-video-lab.html?poster='+mode+'&p=100&side=cover-right';
    await page.goto(url,{waitUntil:'domcontentloaded',timeout:45000});
    await page.waitForFunction(()=>document.getElementById('xw-poster')?.dataset.assetReady==='true',{timeout:20000});
    const sample=()=>page.evaluate(()=>{
     const stage=document.getElementById('dual-stage'),p=document.getElementById('xw-poster');
     const art=p.querySelector('img.xw-poster__art');
     const rect=e=>e.getBoundingClientRect();
     const cover=document.getElementById('dual-cover'),tile=document.getElementById('dual-contents');
     return {
      mode:stage.dataset.p2Poster,scrollLinked:stage.dataset.posterScrollLinked,
      foldCount:stage.dataset.posterFoldCount,palette:stage.dataset.posterPalette,
      colorStep:stage.dataset.posterColorStep,reg:+stage.dataset.posterRegistration,
      bg:getComputedStyle(p).backgroundColor,ink:getComputedStyle(p.querySelector('.xw-poster__glyph')||art).backgroundColor,
      scale:+stage.dataset.posterSpreadScale,revealed:+stage.dataset.posterRevealed,
      poster:rect(p).width,tile:rect(tile).width,coverRatio:rect(cover).width/rect(cover).height,
      cornerPalette:stage.dataset.posterCornerPalette||'',cornerProgress:+stage.dataset.posterCornerProgress||0,
      bigStable:stage.dataset.posterBigStable||'',
      cornerAnimation:getComputedStyle(p.querySelector('.xw-poster__glyph:not(.xw-poster__glyph--foil)')||art).animationName,
      cornerDuration:getComputedStyle(p.querySelector('.xw-poster__glyph:not(.xw-poster__glyph--foil)')||art).animationDuration,
      tileSize:[rect(tile).width,rect(tile).height],tilePos:[rect(tile).left,rect(tile).top],
      clip:getComputedStyle(tile).clipPath,
      masks:p.querySelectorAll('.xw-poster__glyph').length,foil:p.querySelector('.xw-poster__glyph--foil')?
       +getComputedStyle(p.querySelector('.xw-poster__glyph--foil')).opacity:0,
      visible:getComputedStyle(p).opacity,
      artOk:p.dataset.assetReady,artWidth:art.naturalWidth,
      overflow:document.documentElement.scrollWidth,oldRail:getComputedStyle(document.getElementById('dual-continuum')).visibility,
      contentsDisplay:getComputedStyle(document.getElementById('dual-stone-contents')).display,
      contentsOpacity:+getComputedStyle(document.getElementById('dual-stone-contents')).opacity,
      contentsInert:document.getElementById('dual-stone-contents').inert,
      contentsCount:window.P2ContentsTwelve?.count||0,
      markScale:+p.style.getPropertyValue('--xw-mark-scale')||1,
      markInset:parseFloat(p.style.getPropertyValue('--xw-mark-inset'))||0,
      markGlyphLeft:p.querySelector('.xw-poster__glyph')?.getBoundingClientRect().left||0,
      markGlyphTransform:p.querySelector('.xw-poster__glyph')?getComputedStyle(p.querySelector('.xw-poster__glyph')).transform:'none',
      posterContents:+stage.dataset.posterContents||0,
      gutter:innerWidth>820?rect(cover).left-rect(tile).right:rect(cover).top-rect(tile).bottom,
      mastWidthRatio:rect(cover.querySelector('.dual-cover__mast')).width/rect(cover).width,
      mastLeftOffset:rect(cover.querySelector('.dual-cover__mast')).left-rect(cover).left,
      mastLocalTransform:getComputedStyle(cover.querySelector('.dual-cover__mast')).transform,
      oldArt:getComputedStyle(document.getElementById('dual-dore-plate')).display,
      oldLetter:getComputedStyle(document.getElementById('dual-letterfield')).display
     };
    });
    const snap=async value=>{await page.evaluate(v=>{const range=document.getElementById('dual-progress');range.value=String(Math.round(v*100));range.dispatchEvent(new Event('input',{bubbles:true}));},value);return sample()};
    const finished=await sample();
    assert.equal(finished.mode,mode);
    assert.equal(finished.scrollLinked,'true');
    assert.equal(finished.foldCount,'0');
    assert.equal(finished.artOk,'true');
    assert.equal(finished.artWidth,1000);
    assert.equal(finished.oldRail,'hidden');
    assert.equal(finished.oldArt,'none');
    assert.equal(finished.oldLetter,'none');
    assert.equal(finished.visible,'1');
    assert(Math.abs(finished.coverRatio-.625)<.025,'approved RIGHT cover is still 5:8');
    assert(finished.overflow<=width+3,'no horizontal overflow');
    assert(finished.gutter>5,'poster and official cover must be separated by a visible folio gutter');
    assert(Math.abs(finished.scale-.85)<.004,'final paired spread retreats exactly 15%');
    // Test glyph ink from the true full-size printed poster BEFORE the
    // accepted handoff; final p=100 is deliberately an editorial index.
    if(mode==='a')await page.locator('[data-snap="0.845"]').click();
    const screenshot=await page.locator('#xw-poster').screenshot();
    if(mode==='a')await page.locator('[data-snap="1"]').click();
    fs.writeFileSync('artifacts/p2-vol00/poster-'+mode+'-'+width+'-visible-proof.png',screenshot);
    const img=PNG.sync.read(screenshot);
    let viewed=0,different=0;
    const bgPx=[img.data[4*(Math.min(img.width-1,2)+Math.min(img.height-1,2)*img.width)],img.data[4*(Math.min(img.width-1,2)+Math.min(img.height-1,2)*img.width)+1],img.data[4*(Math.min(img.width-1,2)+Math.min(img.height-1,2)*img.width)+2]];
    for(let y=Math.floor(img.height*.1);y<img.height*.9;y+=4)for(let x=Math.floor(img.width*.08);x<img.width*.92;x+=4){
     const i=4*(y*img.width+x);viewed++;
     if(Math.abs(img.data[i]-bgPx[0])+Math.abs(img.data[i+1]-bgPx[1])+Math.abs(img.data[i+2]-bgPx[2])>75)different++;
    }
    assert(different/Math.max(1,viewed)>.055,'poster screenshot must contain visible strokes not just a blank field');
    if(mode==='a'){
     assert.equal(finished.palette,'midnight-gold');
     assert(finished.reg>.999,'last stop fully registered in navy and gold');
     assert.equal(finished.masks,2,'real glyph mask + registered foil glyph');
     assert.equal(finished.cornerPalette,'slow-neon','only the settled small Contents identity gets a slow neon color cycle');
     assert.equal(finished.cornerAnimation,'xw-corner-slow-neon','mini color loop is scoped to the finished index');
     assert.equal(finished.cornerDuration,'32s','seven inks have long, smoothly interpolated holds');
     assert(finished.foil<.01,'small colored masthead does not retain gold foil overprint');
     assert.equal(finished.contentsDisplay,'block','the original Contents really appears');
     assert(finished.contentsOpacity>.99,'the final Contents is visibly composited');
     assert.equal(finished.contentsInert,false,'the final Contents is keyboard-accessible');
     assert.equal(finished.contentsCount,12,'the original twelve editorial desks are preserved');
     assert(Math.abs(finished.markScale-.23)<.02,'original Xi Wang SVG glyph becomes a small masthead');
     assert(Math.abs(finished.markInset-2.2)<.01,'mini Xi Wang gains a reserved 2.2% optical gutter');
     assert(Math.abs(finished.markGlyphLeft-(finished.tilePos[0]+finished.tileSize[0]*.022))<2,
       'compact glyph is positioned at the actual page margin, not the left bleed');
     assert.equal(finished.markGlyphTransform==='none',false,'compact identity is genuinely repositioned in its composed transform');
     assert(finished.posterContents>.99,'poster-to-Contents handoff completed');
     const editorial=await page.evaluate(()=>{
      const root=document.querySelector('#dual-stone-contents .p2x--10');
      const head=root?.querySelector('.p2x-cereal-header h2');
      const grid=root?.querySelector('.p2x-cereal-stack');
      const groups=[...(root?.querySelectorAll('.p2x-cereal-movement')||[])];
      const works=root?.querySelector('.p2x-works');
      return {heading:head?.textContent,headingSize:head?parseFloat(getComputedStyle(head).fontSize):0,
       display:grid?getComputedStyle(grid).display:'',groupCount:groups.length,
       indexCount:root?.querySelectorAll('.p2x-entry').length,
       workFont:works?parseFloat(getComputedStyle(works).fontSize):0,
       readerButton:!!root?.querySelector('.p2x-cereal-expand'),
       gridHeight:grid?.clientHeight,scrollHeight:grid?.scrollHeight,
       gridBottom:grid?.getBoundingClientRect().bottom,
       lastMovementBottom:groups[3]?.getBoundingClientRect().bottom,
       tinyLeft:root?.querySelector('.p2x-cereal-tiny')?.getBoundingClientRect().left,
       markRight:document.querySelector('#xw-poster .xw-poster__glyph')?.getBoundingClientRect().right};
     });
     assert.equal(editorial.heading,'Contents.','Contents headline remains editable HTML');
     assert(editorial.headingSize>=(width>820?39:22),'large English title must establish editorial hierarchy');
     assert.equal(editorial.groupCount,4,'four original movements remain');
     assert.equal(editorial.indexCount,12,'all twelve desks remain DOM text');
     assert(editorial.workFont>=10,'article copy cannot be smaller than legible reading size');
     assert(editorial.readerButton,'full index remains accessible');
     assert.equal(editorial.display,width>820?'grid':'flex','desktop two-column; mobile single-column editorial reading');
     assert(editorial.tinyLeft>=editorial.markRight-8,'gold 西望 cannot overprint the tiny issue label');
     if(width>820)assert(editorial.lastMovementBottom>editorial.gridBottom-35,
      'lower movement register must visibly occupy bottom editorial area, not leave a dead blank half-page');
     await snap(.95);
     await page.screenshot({path:'artifacts/p2-vol00/contents-redesign-'+width+'.png'});
     console.log('Contents editorial QA',width,JSON.stringify(editorial));
     const stamps=[];
     for(const p of [.26,.35,.44,.53,.61,.70,.77])stamps.push(await snap(p));
     assert.equal(new Set(stamps.map(x=>x.bg)).size,7,'background changes for each of seven scroll colors');
     assert.equal(new Set(stamps.map(x=>x.ink)).size,7,'西望 ink color changes for each scroll stop');
     assert.deepEqual(stamps.map(x=>x.colorStep),['1','2','3','4','5','6','7'],
      'seven section colors appear in the specified order');
     // CORE REGRESSION: the old 75.5–86% "sevenfold" fold was still
     // resizing the giant A and sweeping its square across the spread.
     // Colors must travel; the approved glyph/page geometry must NOT.
     for(const state of stamps){
      assert.equal(state.bigStable,'true');
      assert(Math.abs(state.markInset)<.001,'full-size seven-color A cannot inherit the miniature offset');
      assert.equal(state.clip,'none','no second parent wipe above the giant printed ink');
      assert(Math.abs(state.tileSize[0]-state.tileSize[1])<2,'each color keeps full square');
      assert(Math.abs(state.tileSize[0]-stamps[0].tileSize[0])<1,
       'huge letterforms cannot resize while the scroll palette changes');
      assert(Math.abs(state.tilePos[0]-stamps[0].tilePos[0])<1,
       'huge letterforms cannot slide while scroll palette changes');
      assert.equal(state.cornerAnimation,'none','mini neon cannot leak onto large A');
     }
     const goldHold=await snap(.85);
     assert.equal(goldHold.palette,'midnight-gold');
     assert(goldHold.foil>.70,'full size approved gold has static foil impression');
     assert.equal(goldHold.cornerPalette,'gold','before the logo shrinks it stays in approved gold');
     assert(Math.abs(goldHold.markScale-1)<.002,'A poster stays monumental until Contents arrives');
     assert(Math.abs(goldHold.markInset)<.001,'monumental approved A art must keep its original optical placement');
     assert.equal(goldHold.bigStable,'true');
     assert.equal(goldHold.cornerAnimation,'none','no neon or timed animation on giant Westside Watch poster');
     assert.equal(goldHold.clip,'none','historical full-sheet curtain may not amputate the giant glyph');
     assert(Math.abs(goldHold.tileSize[0]-goldHold.tileSize[1])<2,'giant poster stays a real 1:1 square');
     assert(Math.abs(goldHold.scale-1)<.002,'finished gold poster remains full-size');
     assert(goldHold.mastWidthRatio>=1.055,'official WESTSIDE WATCH masthead must span the cover edge-to-edge');
     assert(Math.abs(goldHold.mastLeftOffset)<2,'full-bleed masthead starts at the actual cover edge');
     assert.equal(goldHold.mastLocalTransform,'none','the official masthead must not shrink independently');
     // The mini identity must NEVER race through seven colors in the
     // last 5.6% of wheel progress. It changes slowly after the 02
     // Contents is completely composed; the giant printed A is untouched.
     const compact=await snap(.96);
     assert.equal(compact.cornerPalette,'slow-neon');
     assert.equal(compact.cornerAnimation,'xw-corner-slow-neon');
     const reverseMini=await snap(.90);
     assert.equal(reverseMini.cornerPalette,'gold');
     assert.equal(reverseMini.cornerAnimation,'none',
       'reversing toward the full-size poster disables the mini neon loop');
     const atHold=await snap(.90);
     assert.equal(atHold.palette,'midnight-gold');
     assert(atHold.markScale<1&&atHold.markScale>.23,'original gold glyph begins shrinking INTO Contents');
     assert(atHold.contentsOpacity>0&&atHold.contentsOpacity<1,'the existing index enters gradually');
     assert(Math.abs(atHold.scale-1)<.002,'two-page spread MUST NOT shrink during Contents arrival');
     const contentsHold=await snap(.95);
     assert(contentsHold.contentsOpacity>.99,'Contents is fully present before spread shrink');
     assert(Math.abs(contentsHold.markScale-.23)<.02,'Xi Wang has settled in editorial corner');
     assert(Math.abs(contentsHold.scale-1)<.002,'complete Contents+cover must rest before retreat');
     assert(contentsHold.mastWidthRatio>=1.055,'official masthead must still fill the cover while Contents settles');
     assert.equal(contentsHold.mastLocalTransform,'none','Contents handoff cannot scale the official masthead');
     const shrinking=await snap(.976);
     assert(shrinking.scale<1&&shrinking.scale>.85,'retreat is controlled by scrolling, not a timer');
     const rewind=await snap(.53);
     assert.equal(rewind.bg,stamps[3].bg,'scroll reversal restores exact original background');
     assert.equal(rewind.ink,stamps[3].ink,'scroll reversal restores exact original ink');
     assert.equal(rewind.scale,1,'reversing scroll restores full-size spread');
     assert.equal(rewind.markScale,1,'reverse-scroll restores the monumental lettering');
     assert(rewind.contentsOpacity<.01,'reverse-scroll removes the contents without stale overlay');
     // Mouse wheel is an additional control ONLY for standalone laboratory.
     await page.mouse.move(width/2,height/2);
     const oldValue=await page.locator('#dual-progress').inputValue();
     await page.mouse.wheel(0,220);
     const nextValue=await page.locator('#dual-progress').inputValue();
     assert(Number(nextValue)>Number(oldValue),'standalone mouse-wheel advances poster progress');
     await page.mouse.wheel(0,-220);
     const backValue=await page.locator('#dual-progress').inputValue();
     assert(Number(backValue)<Number(nextValue),'standalone wheel upward reverses poster progress');
    }else{
     assert.equal(finished.palette,'engraving-b');
     assert.equal(finished.masks,0,'B stays an independent native image');
     const early=await snap(.31);
     assert(early.revealed<1,'B also follows P2 reveal but no longer uses sevenfold curtains');
     await snap(1);
    }
    await page.screenshot({path:'artifacts/p2-vol00/poster-'+mode+'-'+width+'.png'});
    console.log('P2 POSTER OK',mode,width,'visible pixel difference', (different/viewed).toFixed(3));
   }finally{await page.close();}
  }
 }
 // Reuse the existing ONE 66-book / Emmaus scene in the same scroll stage
 // after Magazine Contents, rather than a new mock page.
 const connected=await browser.newPage({viewport:{width:1648,height:928}});
 try{
  await connected.goto('http://127.0.0.1:4173/experiments/p2-emmaus-olive-handoff-lab.html?d=6.50&five=1',
   {waitUntil:'domcontentloaded',timeout:45000});
  await connected.waitForFunction(()=>window.ONE_DATA?.books?.length===66,{timeout:20000});
  const continuity=await connected.evaluate(()=>{
   const base=document.querySelector('#proof-original');
   const mag=base?.contentDocument?.querySelector('.p2-magazine iframe:not(.p2-magazine__home-film)');
   return {hasOriginalMagazine:!!mag,magazineSource:mag?.getAttribute('src')||'',
     hasRealEmmaus:!!document.querySelector('#emmaus')};
  });
  assert(continuity.hasRealEmmaus,'03 Emmaus must exist in the same scroll track');
  // MERSI geometry gate: at three separate intermediate scroll positions,
  // OLD Magazine Contents and NEW ONE paper must form a SINGLE straight
  // crop edge, NOT semi-transparent overlapping words.
  for(const d of [7.81,7.99,8.16]){
   await connected.evaluate(distance=>{
    const range=document.querySelector('#proof-seek');
    range.value=String(distance/16.74*100);
    range.dispatchEvent(new Event('input',{bubbles:true}));
   },d);
   await connected.waitForTimeout(90);
   const wipe=await connected.evaluate(()=>{
    const root=document.querySelector('#proof-original');
    const mag=root?.contentDocument?.querySelector('.p2-magazine iframe:not(.p2-magazine__home-film)');
    const old=mag?.contentDocument?.getElementById('dual-contents');
    const incoming=document.querySelector('#emmaus > .emmaus__left');
    const pagePaper=incoming?.querySelector('.emmaus__binding-paper');
    return {oldClip:old?.style.clipPath||'',newClip:incoming?.style.clipPath||'',
      oldOpacity:old?+getComputedStyle(old).opacity:-1,
      newOpacity:incoming?+getComputedStyle(incoming).opacity:-1,
      paperOpacity:pagePaper?+getComputedStyle(pagePaper).opacity:-1};
   });
   const m1=wipe.oldClip.match(/inset\(0 ([\d.]+)% 0 0\)/);
   const m2=wipe.newClip.match(/inset\(0 0 0 ([\d.]+)%\)/);
   assert(m1&&m2,'both existing folios must own opposing clip masks at '+d);
   assert(Math.abs(+m1[1]+ +m2[1]-100)<.11,'mask edges must meet exactly with no duplicated text');
   assert.equal(wipe.newOpacity,1,'ONE page must be completely opaque within revealed bounds');
   assert.equal(wipe.paperOpacity,1,'ONE binding paper may not separately fade');
   assert.equal(wipe.oldOpacity,1,'old Magazine Contents must be completely opaque where still revealed');
   await connected.screenshot({path:'artifacts/p2-vol00/mersi-handoff-'+d.toFixed(2)+'.png'});
  }
  await connected.locator('[data-jump="6.49"]').click();
  await connected.waitForFunction(()=>{
   const f=document.querySelector('#proof-original')?.contentDocument
    ?.querySelector('.p2-magazine iframe:not(.p2-magazine__home-film)');
   const old=f?.contentDocument?.getElementById('dual-contents');
   return old && !old.style.clipPath.startsWith('inset(');
  },{timeout:15000});
  assert(!await connected.locator('.p2-emmaus-prologue').count(),'no extra text-only prologue');
  await connected.locator('[data-jump="6.49"]').click();
  await connected.waitForFunction(()=>document.body.dataset.proofScene==='02',{timeout:15000});
  await connected.locator('[data-jump="7.42"]').click();
  await connected.waitForFunction(()=>{
   const cover=document.querySelector('#proof-original')?.contentDocument
    ?.querySelector('.p2-magazine iframe:not(.p2-magazine__home-film)')
    ?.contentDocument?.querySelector('#p2-emmaus-magazine-underleaf');
   return !!cover&&getComputedStyle(cover).display!=='none';
  },{timeout:15000});
  await connected.locator('[data-jump="6.49"]').click();
  await connected.waitForFunction(()=>{
   const cover=document.querySelector('#proof-original')?.contentDocument
    ?.querySelector('.p2-magazine iframe:not(.p2-magazine__home-film)')
    ?.contentDocument?.querySelector('#p2-emmaus-magazine-underleaf');
   return !cover||getComputedStyle(cover).display==='none';
  },{timeout:15000});
  await connected.locator('[data-jump="9.10"]').click();
  await connected.waitForFunction(()=>document.body.dataset.proofScene==='03' &&
   getComputedStyle(document.querySelector('#emmaus')).visibility==='visible',{timeout:15000});
  assert(await connected.locator('#em-book-en').count(),'real ONE book selector is present');
  await connected.screenshot({path:'artifacts/p2-vol00/p2-emmaus-03.png'});
  await connected.locator('[data-jump="6.49"]').click();
  await connected.waitForFunction(()=>document.body.dataset.proofScene==='02',{timeout:15000});
  console.log('P2 CONTINUOUS 02→03→02 PASS',JSON.stringify(continuity));
 }finally{await connected.close();}
 console.log('P2 ink+paper, readable Contents, live Emmaus 02→03, reverse-scroll and final retreat tests PASS');
}finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
