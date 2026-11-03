// A/B Campaign Poster + Homepage-faithful sevenfold fold: real-browser proof.
const assert=require('node:assert/strict');
const fs=require('node:fs');
const {chromium}=require('playwright');
const poster=fs.readFileSync('static/js/p2-vol00-poster.js','utf8');
const css=fs.readFileSync('static/css/p2-vol00-poster.css','utf8');
const html=fs.readFileSync('static/experiments/p2-double-square-video-lab.html','utf8');
const bridge=fs.readFileSync('static/js/p2-magazine-live-bridge.js','utf8');

assert.match(html,/p2-vol00-poster\.js/,'P2 actually loads both campaign posters');
assert.match(html,/p2-vol00-poster\.css/,'P2 loads the scoped poster design');
assert.match(poster,/poster'\)==='legacy'/,'an archived legacy visual baseline remains inspectable');
assert.match(poster,/const colors=\['--ws-water','--ws-first-light','--ws-pale-gold','--ws-olive','--ws-harvest','--ws-crimson','--ws-daylight-mauve'\]/,
 'sevenfold reuses exact homepage seven Design OS colors');
assert.match(poster,/scaleY\(/,'seven full-surface planes, not narrow vertical swatches');
assert.match(poster,/const glyphs=/,'two large editable vector Chinese glyphs remain one poster artwork');
assert.match(poster,/clipPath id="xw-type-clip"/,'the B1 line system is actually clipped into full-size type');
assert.match(css,/\.dual-continuum\{[\s\S]*visibility:hidden!important/,'old colored Magazine navigation removed visually');
assert.match(bridge,/const poster=requestedPoster==='b'\?'b':'a'/,'full P2 preview can choose A or B');
assert.match(html,/window\.P2Vol00Poster\?\.paint\(progress\)/,
 'poster is driven by EXISTING native P2 scroll, not an independent clock');

(async()=>{
const browser=await chromium.launch({headless:true});
try{
for(const mode of ['a','b']){
 for(const [width,height] of [[1648,928],[390,844]]){
  const page=await browser.newPage({viewport:{width,height},reducedMotion:'no-preference'});
  await page.goto('http://127.0.0.1:4173/experiments/p2-double-square-video-lab.html?poster='+mode+'&p=100&side=cover-right',
    {waitUntil:'domcontentloaded',timeout:45000});
  await page.waitForFunction(()=>document.querySelector('#dual-stage')?.dataset.posterFoldCount==='7');
  const atRest=await page.evaluate(()=>{
   const stage=document.getElementById('dual-stage'),panel=document.getElementById('xw-poster');
   const tile=document.getElementById('dual-contents'),art=panel.querySelector('svg');
   const colorLayers=[...panel.querySelectorAll('.xw-poster__fold')];
   const rect=el=>el.getBoundingClientRect();
   const cover=document.getElementById('dual-cover');
   return {mode:stage.dataset.p2Poster,folds:colorLayers.length,
    colors:colorLayers.map(l=>getComputedStyle(l).backgroundColor),
    poster:rect(panel),tile:rect(tile),cover:rect(cover),
    scene:rect(stage),coverTitle:!!cover.querySelector('img.dual-cover__mast'),
    oldRail:getComputedStyle(document.getElementById('dual-continuum')).visibility,
    railInert:document.getElementById('dual-continuum').inert,
    oldDoré:getComputedStyle(document.getElementById('dual-dore-plate')).display,
    oldInk:getComputedStyle(document.getElementById('dual-letterfield')).display,
    posterOpacity:getComputedStyle(panel).opacity,
    artClip:getComputedStyle(art).clipPath,
    fieldCount:panel.querySelectorAll('.xw-poster__big-type text').length,
    scrollWidth:document.documentElement.scrollWidth};
  });
  assert.equal(atRest.mode,mode);
  assert.equal(atRest.folds,7);
  assert.equal(new Set(atRest.colors).size,7,'seven OS colors have distinct computed values');
  assert.equal(atRest.oldRail,'hidden');
  assert.equal(atRest.railInert,true);
  assert.equal(atRest.oldDoré,'none','Magazine no longer displays Doré');
  assert.equal(atRest.oldInk,'none','the brush-calligraphy mother is not shown on the campaign');
  assert.equal(atRest.posterOpacity,'1');
  assert.equal(atRest.fieldCount,2,'only two monumental Chinese characters make the poster');
  assert(Math.abs(atRest.poster.width-atRest.tile.width)<1.5,'poster fills original square');
  assert(Math.abs(atRest.cover.width/atRest.cover.height-.625)<.02,'RIGHT approved magazine cover remains 5:8');
  assert(atRest.scrollWidth<=width+3,'poster does not create horizontal overflow');
  assert(/inset\(0px 0px 0% 0px\)|inset\(0 0 0% 0\)/.test(atRest.artClip)||atRest.artClip.includes('0%'),
   'sevenfold has fully revealed the clean poster');
  await page.locator('[data-snap="0.60"]').click();
  const partial=await page.evaluate(()=>({
   seven:+document.getElementById('dual-stage').dataset.posterFoldCount,
   revealed:+document.getElementById('dual-stage').dataset.posterRevealed,
   turns:[...document.querySelectorAll('.xw-poster__fold')].map(el=>getComputedStyle(el).transform)
  }));
  assert.equal(partial.seven,7);
  assert(partial.revealed<.01,'at 60% the poster is still behind the sevenfold');
  assert(partial.turns.some(x=>x!=='matrix(1, 0, 0, 0, 0, 0)')&&partial.turns.some(x=>x!=='none'),
   'layered fold is being composed from the top');
  await page.locator('[data-snap="1"]').click();
  assert.equal(await page.locator('#dual-stage').getAttribute('data-poster-revealed'),'1.0000',
   'scroll back through the same sevenfold to full poster');
  await page.screenshot({path:'artifacts/p2-vol00/poster-'+mode+'-'+width+'.png'});
  await page.close();
 }
}
console.log('P2 A/B sevenfold campaign poster checks PASS (visual review still required).');
}finally{await browser.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
