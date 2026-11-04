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
assert.doesNotMatch(css,/@keyframes/,'no autonomous flashing and no neon timer');
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
     assert(finished.foil>.70,'foil is scroll-driven and visible at final print');
     assert.equal(finished.contentsDisplay,'block','the original Contents really appears');
     assert(finished.contentsOpacity>.99,'the final Contents is visibly composited');
     assert.equal(finished.contentsInert,false,'the final Contents is keyboard-accessible');
     assert.equal(finished.contentsCount,12,'the original twelve editorial desks are preserved');
     assert(Math.abs(finished.markScale-.23)<.02,'original Xi Wang SVG glyph becomes a small masthead');
     assert(finished.posterContents>.99,'poster-to-Contents handoff completed');
     const stamps=[];
     for(const p of [.26,.35,.44,.53,.61,.70,.77])stamps.push(await snap(p));
     assert.equal(new Set(stamps.map(x=>x.bg)).size,7,'background changes for each of seven scroll colors');
     assert.equal(new Set(stamps.map(x=>x.ink)).size,7,'西望 ink color changes for each scroll stop');
     assert.deepEqual(stamps.map(x=>x.colorStep),['1','2','3','4','5','6','7'],
      'seven section colors appear in the specified order');
     const goldHold=await snap(.84);
     assert.equal(goldHold.palette,'midnight-gold');
     assert(Math.abs(goldHold.markScale-1)<.002,'A poster stays monumental until Contents arrives');
     assert(Math.abs(goldHold.scale-1)<.002,'finished gold poster remains full-size');
     assert(goldHold.mastWidthRatio>=1.055,'official WESTSIDE WATCH masthead must span the cover edge-to-edge');
     assert(Math.abs(goldHold.mastLeftOffset)<2,'full-bleed masthead starts at the actual cover edge');
     assert.equal(goldHold.mastLocalTransform,'none','the official masthead must not shrink independently');
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
     const rewind=await snap(.54);
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
 console.log('P2 scroll-registered ink+paper, foil, B alternative, resize/reverse tests PASS');
}finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
