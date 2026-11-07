'use strict';
/* P2 04 CLEAN FIELD regression.
 * Approved 03 Emmaus and its 5:8 cloth must remain untouched.
 * Only the 04 full-stage engraving was retired; the V13 card headpiece
 * and original twelve composites stay protected. */
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const {chromium}=require('playwright');
const root=path.resolve(__dirname,'..');
const read=p=>fs.readFileSync(path.join(root,p),'utf8');
const html=read('static/experiments/p2-0104-olive-continuation.html');
const css=read('static/css/p2-0104-olive-continuation.css');
const js=read('static/js/p2-0104-olive-continuation.js');
assert.match(html,/p2-0103-release\.html\?embed=1/);
assert.match(html,/olive-speaker-baseline|baseline\.js/);
assert.match(html,/id="olive-editorial-engraving"/);
assert.match(css,/04-olive-botanical-impression-v60-1\.svg/);
assert.match(css,/04-olive-botanical-impression-v60-6\.svg/);
for(let n=1;n<=6;n++)assert.match(read(`static/images/p2-realms/v15/04-olive-botanical-impression-v60-${n}.svg`),/crane-public-domain-olive/);
assert.doesNotMatch(css,/04-olive-botanical-folio-outline-v56\\.svg/,'full-scale botanical leaf art must not be shrunk into tiny card gutter');
assert.match(read('static/images/p2-realms/v15/04-olive-botanical-folio-outline-v56.svg'),/fill="none" stroke="white"/);
assert.match(read('static/images/p2-realms/v15/04-olive-botanical-folio-v54.svg'),/crane-public-domain-olive/,'use genuine public-domain Crane engraved foliage, not invented needles');
assert.equal((read('static/images/p2-realms/v15/04-olive-botanical-folio-v54.svg').match(/href="#crane-public-domain-olive"/g)||[]).length,6,'six mature folio sprays, not two twigs');
assert.match(css,/04-olive-mount-terrain-contours-v1\.svg/);
assert.match(read('static/images/p2-realms/v15/04-olive-mount-terrain-contours-v1.svg'),/olivet-true-topography/);
assert.match(js,/dataset\.p2EngravingPlant/);
assert.match(js,/dataset\.p2EngravingTerrain/);
assert.match(html,/p2-0104-olive-path-growth-v60\.js/);
assert.equal((html.match(/data-print-impression=/g)||[]).length,6,'six independent print layers');
assert.equal((html.match(/class="olive-card__reverse olive-card__reverse--/g)||[]).length,2,
 'each invitation has an actual second face');
assert.match(css,/backface-visibility:hidden/,'front and reverse need hidden back faces');
assert.match(css,/--folio-paper-alpha,0/,'fold stock appears only during the 3D turn');
assert.match(css,/--folio-edge-alpha,0/,'fold foil disappears when the back merges into the field');
assert.doesNotMatch(html,/<strong>OLIVE <i>MOUNTAIN<\/i><\/strong>/,
 'duplicate chapter masthead must not be printed on every reverse');
assert.match(js,/measured-two-faced-rotating-card-v63/,'MERSI drives measured 3D turns');
const terrainEngine=read('static/js/p2-0104-olive-path-growth-v60.js');
assert.match(terrainEngine,/P2OliveEngraving=\{paint\}/);
assert.match(terrainEngine,/getBBox\(\)/);
assert.doesNotMatch(terrainEngine,/strokeDashoffset='1000'/,'do not redraw or crop entire rings');
assert.match(terrainEngine,/p2ContourImpression/);
assert.match(terrainEngine,/original\*1\.65/,'terrain line hierarchy optically strengthened');
assert.match(terrainEngine,/b\.area-a\.area/,'major topographic ridge lines must print before tiny isolated loops');
assert.match(css,/filter:opacity\(\.64\)/,'oversized botanical area subdued without deleting the SVG layers');
const terrainSvg=read('static/images/p2-realms/v15/04-olive-mount-terrain-growth-v53.svg');
assert.match(terrainSvg,/class="terrain-major"/);
assert.match(terrainSvg,/class="terrain-mid"/);
assert.match(terrainSvg,/class="terrain-fine"/);
assert.match(terrainSvg,/pathLength="1000"/);
assert.doesNotMatch(html,/id="olive-growth-field"/);
assert.doesNotMatch(js,/olive-growth-|growthSvg|growthMask|drawGrowingCurve|livingClock/,
 'retired full-stage botanical/under-poster strokes must not run');
assert.doesNotMatch(css,/\.olive-growth-|#olive-growth-field|04-olive-woodward-cousen/,
 'no dormant CSS can resurrect full-stage background strokes');
assert.doesNotMatch(html,/olive-growth-|04-olive-hillside-copperplate/,
 'no background engraving nodes or assets in the live stage');
assert.doesNotMatch(js,/fetch\(['"]\/images\/p2-realms\/v15\/04-olive-hillside/);
assert.doesNotMatch(js,/requestAnimationFrame\(livingFrame\)/);
assert.doesNotMatch(css,/04-olive-woodward-cousen-(desktop|mobile)-intaglio-v44/);
assert.match(css,/\.olive-surround__half\{[^}]*background-color:var\(--ws-olive\);[^}]*background-image:none;/s);
assert.match(css,/\.olive-card__relief::after\{/,'invitation local relief retained');
assert.equal((html.match(/class="olive-card__imprint"/g)||[]).length,3,
 'first and paired invitations each carry one shared imprint system');
assert.equal((html.match(/class="olive-card__edition"/g)||[]).length,3,'all card shells have a readable edition rail');
assert.match(css,/radial-gradient\(ellipse 92% 89%/,'both editorial print fields feather before a hard edge');
assert.match(css,/inset:-7% -12% -23% -9%/,'botanical print bleeds below actual viewport');
assert.match(css,/inset:-7% -24% -22% -8%/,'terrain print bleeds beyond right and bottom of viewport');
assert.match(css,/transparent 10%,#000 27%/,'editorial masthead has a gradual 10-27% exclusion zone');
assert.match(css,/\.olive-card__imprint::before,\.olive-card__imprint::after\{[^}]*content:none!important;/s,
 'reject unrelated miniature botanical engraving in the narrow card gutter');
assert.match(css,/\.olive-card__relief::after\{/,
 'approved historic card masthead is preserved across all editions');
assert.match(js,/imprintFamilies=/,'four editions assigned from approved twelve');
assert.match(js,/frozen\.mount\(art,target\)/,'frozen poster typography retained');
assert.match(js,/const readingField=ease\(\(d-T\.first\)\/\.065\);/,
  'original Emmaus handoff timing unchanged');
assert.match(read('static/experiments/p2-0103-release.html'),/p2-emmaus-bookbinding-v7\.css/,
  'genuine Emmaus iframe still retains the original binding stylesheet');
fs.mkdirSync(path.join(root,'artifacts/p2-0104-olive'),{recursive:true});
const widths=[1648,390];
(async()=>{
 const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
 try{
  for(const width of widths){
   const page=await browser.newPage({viewport:{width,height:width===1648?928:844},deviceScaleFactor:1});
   const errors=[],oliveRequests=[];
   page.on('pageerror',e=>errors.push(e.message));
   page.on('request',r=>{if(/04-olive-(?:hillside-copperplate|living-grove|woodward-cousen|growth-field)/.test(r.url()))oliveRequests.push(r.url())});
   await page.goto('http://127.0.0.1:4173/experiments/p2-0104-olive-continuation.html?d=9.30',
    {waitUntil:'domcontentloaded'});
   await page.waitForFunction(()=>document.querySelector('#p2-olive-stage')?.dataset.p2FolioReady==='true',{timeout:20000});
   async function go(d,name){
    await page.evaluate(d=>{const t=document.querySelector('#p2-olive-track');scrollTo(0,t.getBoundingClientRect().top+scrollY+d*innerHeight)},d);
    await page.waitForFunction(d=>Math.abs(Number(document.querySelector('#p2-olive-stage').dataset.p2Distance)-d)<.025,d,{timeout:12000});
    const state=await page.evaluate(()=>{
     const stage=document.querySelector('#p2-olive-stage');
     const bg=document.querySelector('#p2-olive-surround');
     const head=document.querySelector('#p2-0103-original');
     return {scene:stage.dataset.p2Scene,
       source:getComputedStyle(head).visibility,
       plant:Number(stage.dataset.p2EngravingPlant),
       terrain:Number(stage.dataset.p2EngravingTerrain),
       artVisibility:getComputedStyle(document.querySelector('#olive-editorial-engraving')).visibility,
       terrainEngine:stage.dataset.p2TerrainStrokeEngine,
       cardImprints:[...document.querySelectorAll('.olive-stage__invitation--pair')].map(el=>({
        family:el.dataset.olivePrintFamily,
        clip:el.style.getPropertyValue('--olive-imprint-clip'),
        rail:Number.parseFloat(el.style.getPropertyValue('--olive-outer-rail-width')),
        edition:el.querySelector('.olive-card__edition')?.textContent,
        stray:getComputedStyle(el.querySelector('.olive-card__imprint'),'::before').content,
        header:getComputedStyle(el.querySelector('.olive-card__relief'),'::after').webkitMaskImage
       })),
       cardInk:Number(stage.dataset.p2CardInkReveal),
       fullContourPaths:Number(stage.dataset.p2TerrainPathTotal),
       visibleContours:Number(stage.dataset.p2TerrainVisiblePaths),
       completedRings:Number(stage.dataset.p2TerrainCompleteRings),
       plantLayers:[...document.querySelectorAll('[data-print-impression]')].map(p=>Number(p.style.opacity)),
       leftClip:document.querySelector('[data-art-side="left"]').style.clipPath,
       rightClip:document.querySelector('[data-art-side="right"]').style.clipPath,
       changingSide:stage.dataset.p2ActiveSide,
       oppositeLocked:stage.dataset.p2OppositeLocked,
       folioFront:stage.dataset.p2FolioFront,
       folioFaces:stage.dataset.p2FolioReverse,
       folioAngles:stage.dataset.p2FolioAngles,
       folioSystem:stage.dataset.p2FolioSystem,
       reverseFaces:[...document.querySelectorAll('.olive-card__reverse')].map(el=>({
        visible:getComputedStyle(el).visibility,
        mask:getComputedStyle(el,'::before').webkitMaskImage,
        transform:getComputedStyle(el).transform
       })),
       leftPoster:document.querySelector('#olive-pair-left')?.dataset.speakerIndex,
       rightPoster:document.querySelector('#olive-pair-right')?.dataset.speakerIndex,
       portraitDecode:stage.dataset.p2PortraitDecode,
       contourOffsets:['major','mid','fine'].map(k=>document.querySelector('.terrain-'+k)?.getAttribute('stroke-dashoffset')),
       oliveMask:getComputedStyle(document.querySelector('.olive-editorial-engraving__print--botanical'),'::after').webkitMaskImage,
       ground:getComputedStyle(bg).visibility,
       noGrowth:document.querySelector('#olive-growth-field')===null,
       posterNodes:document.querySelectorAll('.olive-stage__index-card').length,
       bgImages:[...bg.querySelectorAll('.olive-surround__half')].map(el=>getComputedStyle(el).backgroundImage),
       bgPseudo:[...bg.querySelectorAll('.olive-surround__half')].map(el=>getComputedStyle(el,'::after').content)};
    });
    // Every image used by the active two-card handoff must have rendered
    // pixels before visual proof; image decode regressions previously left
    // huge blank speaker frames even when the print artwork was intact.
    if(d>=10.95&&d<16.25){
     await page.waitForFunction(()=>{
      const stage=document.querySelector('#p2-olive-stage');
      if(stage?.dataset.p2PortraitDecode!=='ready')return false;
      const list=[...document.querySelectorAll('#olive-pair .olive-stage__poster img')]
       .filter(img=>img.getAttribute('src'));
      return list.length>=2&&list.every(img=>img.complete&&img.naturalWidth>0);
     },null,{timeout:30000});
     await page.evaluate(()=>Promise.all(
      [...document.querySelectorAll('#olive-pair .olive-stage__poster img')]
       .filter(img=>img.getAttribute('src')).map(img=>img.decode())));
    }
    // The twelve protected portraits load asynchronously. A screenshot taken
    // immediately after a seek can catch their fonts before decoded pixels.
    // Verify REAL rendered image assets rather than merely counting DOM cards.
    if(d>=17.25){
     await page.waitForFunction(()=>{
      const imgs=[...document.querySelectorAll('#olive-overview .olive-stage__index-card img')];
      return imgs.length===12&&imgs.every(img=>img.complete&&img.naturalWidth>0);
     },null,{timeout:30000});
     await page.evaluate(()=>Promise.all(
      [...document.querySelectorAll('#olive-overview .olive-stage__index-card img')]
       .map(img=>img.decode())));
    }
    await page.screenshot({path:`artifacts/p2-0104-olive/${width}-${name}.png`,animations:'disabled'});
    return state;
   }
   await page.evaluate(()=>document.fonts.ready);
   const src=await go(9.30,'00-original-emmaus');
   assert.equal(src.source,'visible','03 original iframe visible before entry');
   const pair=await go(10.98,'03-two-poster-locked-original-background');
   const mid=await go(13.15,'04-clean-olive-field');
   assert.equal(mid.noGrowth,true,'04 growth SVG must not be in the DOM');
   assert(mid.cardImprints.length===2&&mid.cardImprints.every(c=>
     c.family&&c.stray==='none'&&c.header.includes('04-olive-historic-engraving-v13')),
    'both physical invitation cards share V13 header without alien miniature card flora');
   assert(mid.cardImprints.every(c=>c.rail>=8 && c.edition?.includes('/ 12')),
    'physical exterior rails visibly receive a coordinated numbered edition');
   assert(mid.cardImprints.every(c=>c.clip.endsWith('%')),
    'card engraving growth driven by same scroll position');
   assert.equal(mid.posterNodes,12,'all twelve source composites still exist');
   assert(mid.bgImages.every(x=>x==='none'),'04 background must have no image');
   assert(mid.bgPseudo.every(x=>x==='none'),'04 background must have no pseudo-image');
   const leftInk=await go(11.90,'05a-left-portrait-and-right-back');
   assert(leftInk.plant>.16&&leftInk.terrain>.16,'both printing fields retained');
   assert.equal(leftInk.folioFaces,'front,back','first: left portrait and right engraved reverse');
   assert.equal(leftInk.folioSystem,'measured-two-faced-rotating-card-v63');
   assert.equal(leftInk.reverseFaces.length,2);
   assert(leftInk.reverseFaces.every(x=>x.visible==='visible'&&x.mask==='none'),
    'the original full botanical/terrain field itself must be the back, without duplicate local engravings');
   assert.equal(leftInk.leftClip,'none','no box clipping on botanical field');
   assert.equal(leftInk.rightClip,'none','no box clipping on contour field');
   await page.waitForFunction(()=>['real-dem-whole-contours-v60','static-fallback'].includes(document.querySelector('#p2-olive-stage')?.dataset.p2TerrainStrokeEngine),{timeout:20000});
   const rightLocked=await go(12.33,'05aa-right-front-left-back');
   assert.equal(rightLocked.folioFaces,'back,front','right figure is front; left botanical back');
   assert.equal(rightLocked.rightPoster,'1','right approved Derek Prince portrait');
   assert.equal(rightLocked.portraitDecode,'ready','approved portraits decoded');
   const rightInk=await go(13.10,'05b-right-terrain-second-complete');
   assert.equal(rightInk.leftPoster,'4','left has safely preloaded the next portrait behind its botanical reverse');
   assert.equal(rightInk.portraitDecode,'ready','original portraits predecoded before alternating swaps');
   assert.equal(rightInk.terrainEngine,'real-dem-whole-contours-v60','complete measured contour paths are printed, never SVG wipe');
   assert(rightInk.fullContourPaths>=24&&rightInk.visibleContours>0,'full geographic contours displayed');
   assert(rightInk.completedRings>=2,'two successive right speakers each print a complete new contour batch');
   assert(rightInk.terrain>.3&&rightInk.plant>.3,'left printed editions HOLD while right adds a new whole contour batch');
   const leftAgain=await go(13.50,'05c-left-botanical-return');
   assert(leftAgain.plant>.3&&leftAgain.terrain>.3,'old letterpress impressions persist through next alternating speaker');
   const end=await go(17.30,'09-twelve-voices-final-overview');
   assert(end.plant>.999&&end.terrain>.999,'all twelve posters: both engravings shown');
   assert.equal(end.completedRings,6,'all six right speaker contour editions are printed');
   assert(end.plantLayers.every(v=>v>.999),'all six botanical engraved editions remain visible after twelve speakers');
   assert.match(css,/var\(--ws-deep\)/,'plant includes genuinely dark olive impression from the shared OS');
   assert.equal(end.posterNodes,12);
   const back=await go(9.30,'10-reversed-original-emmaus');
   assert.equal(back.source,'visible','reverse scrolling restores 03 original');
   assert.equal(back.artVisibility,'hidden','reverse to 03 removes both 04 engraving fields');
   assert.deepEqual(oliveRequests,[],'retired 04 background SVGs must never be fetched');
   assert.deepEqual(errors,[],'browser must be free of page errors');
   console.log('P2 04 CLEAN FIELD PASS',width,JSON.stringify({pair:pair.scene,clean:mid.scene,botanical:leftInk.plant,topography:rightInk.terrain,index:end.scene,reverse:back.scene}));
   await page.close();
  }
 }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
