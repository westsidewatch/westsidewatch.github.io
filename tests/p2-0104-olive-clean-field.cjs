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
assert.match(css,/04-olive-botanical-folio-v54\.svg/);
assert.match(css,/04-olive-botanical-folio-outline-v56\.svg/);
assert.match(read('static/images/p2-realms/v15/04-olive-botanical-folio-outline-v56.svg'),/fill="none" stroke="white"/);
assert.match(read('static/images/p2-realms/v15/04-olive-botanical-folio-v54.svg'),/crane-public-domain-olive/,'use genuine public-domain Crane engraved foliage, not invented needles');
assert.equal((read('static/images/p2-realms/v15/04-olive-botanical-folio-v54.svg').match(/href="#crane-public-domain-olive"/g)||[]).length,6,'six mature folio sprays, not two twigs');
assert.match(css,/04-olive-mount-terrain-contours-v1\.svg/);
assert.match(read('static/images/p2-realms/v15/04-olive-mount-terrain-contours-v1.svg'),/olivet-true-topography/);
assert.match(js,/dataset\.p2EngravingPlant/);
assert.match(js,/dataset\.p2EngravingTerrain/);
assert.match(html,/p2-0104-olive-path-growth-v53\.js/);
const terrainEngine=read('static/js/p2-0104-olive-path-growth-v53.js');
assert.match(terrainEngine,/P2OliveEngraving=\{paint\}/);
assert.match(terrainEngine,/svg\.querySelector\('\.terrain-'\+name\)/);
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
assert(css.includes('--olive-card-motif:url('),'botanical print is the shared default');
for(const family of ['terrain','city','horizon'])
 assert(css.includes('data-olive-print-family="'+family+'"'),family+' print edition available');
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
        mask:getComputedStyle(el.querySelector('.olive-card__imprint'),'::before').webkitMaskImage
       })),
       cardInk:Number(stage.dataset.p2CardInkReveal),
       contourGroups:[...document.querySelectorAll('.olive-editorial-engraving__print--topography svg > g g')].length,
       contourOffsets:['major','mid','fine'].map(k=>document.querySelector('.terrain-'+k)?.getAttribute('stroke-dashoffset')),
       oliveMask:getComputedStyle(document.querySelector('.olive-editorial-engraving__print--botanical'),'::after').webkitMaskImage,
       ground:getComputedStyle(bg).visibility,
       noGrowth:document.querySelector('#olive-growth-field')===null,
       posterNodes:document.querySelectorAll('.olive-stage__index-card').length,
       bgImages:[...bg.querySelectorAll('.olive-surround__half')].map(el=>getComputedStyle(el).backgroundImage),
       bgPseudo:[...bg.querySelectorAll('.olive-surround__half')].map(el=>getComputedStyle(el,'::after').content)};
    });
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
   assert(mid.cardImprints.length===2&&mid.cardImprints.every(c=>c.family&&c.mask!=='none'),
    'both invitation cards must have authentic vector-print decorations');
   assert(mid.cardImprints.every(c=>c.rail>=8 && c.edition?.includes('/ 12')),
    'physical exterior rails visibly receive a coordinated numbered edition');
   assert(mid.cardImprints.every(c=>c.clip.endsWith('%')),
    'card engraving growth driven by same scroll position');
   assert.equal(mid.posterNodes,12,'all twelve source composites still exist');
   assert(mid.bgImages.every(x=>x==='none'),'04 background must have no image');
   assert(mid.bgPseudo.every(x=>x==='none'),'04 background must have no pseudo-image');
   const leftInk=await go(11.90,'05a-left-botanical-only');
   assert(leftInk.plant>.6&&leftInk.terrain<.001,'first engraving moment: left only');
   await page.waitForFunction(()=>['real-dem-dash-v53','static-fallback'].includes(document.querySelector('#p2-olive-stage')?.dataset.p2TerrainStrokeEngine),{timeout:20000});
   const rightInk=await go(12.60,'05b-right-terrain-only');
   assert.equal(rightInk.terrainEngine,'real-dem-dash-v53','real geographic contours load and animate; static fallback is not a passing result');
   assert.equal(rightInk.contourOffsets[0],'0.000','major true-topography paths have drawn by full right-phase');
   assert(rightInk.terrain>.99&&rightInk.plant<.01,'second engraving moment: right only');
   const leftAgain=await go(13.50,'05c-left-botanical-return');
   assert(leftAgain.plant>.99&&leftAgain.terrain<.01,'paired alternation restores left');
   const end=await go(17.30,'09-twelve-voices-final-overview');
   assert(end.plant>.999&&end.terrain>.999,'all twelve posters: both engravings shown');
   assert(end.contourOffsets.every(x=>Number(x)<.001),'major, medium, fine contours completely drawn in the final spread');
   assert(end.oliveMask.includes('04-olive-botanical-folio-outline-v56'),'left folio uses the genuine six-spray print master');
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
