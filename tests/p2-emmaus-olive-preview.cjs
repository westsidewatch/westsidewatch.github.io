'use strict';
/* Isolated P2 03/04 proof — no runtime writes to the production homepage. */
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..');
const html=fs.readFileSync(path.join(root,'static/experiments/p2-emmaus-olive-handoff-lab.html'),'utf8');
const js=fs.readFileSync(path.join(root,'static/js/p2-emmaus-olive-preview.js'),'utf8');
const css=fs.readFileSync(path.join(root,'static/css/p2-emmaus-olive-preview.css'),'utf8');
assert.match(html,/p2\/living-water\.html\?embed=1/,'reuses approved P2 Church/Magazine source');
assert.match(html,/one\/one-data\.js/,'reads the canonical 66-book inventory');
assert.match(html,/one\/luke-21-24\.js/,'features the original Luke 24 ONE study content');
assert.match(html,/p2-emmaus-scroll-micro-engraving\.svg/,'Emmaus has its own local editable engraved scroll study');
assert.equal((html.match(/class="emmaus__folio-layer"/g)||[]).length,7,'seven inherited OS-colored folio edges');
assert.match(js,/ONE_DATA\?\.luke\?\.chapterStudies\?\.\['24'\]/,'chapter text comes from canonical ONE, never invented copy');
assert.match(js,/oneDrop-i\*\.058/,'sevenfold motion shares the existing P2 scroll owner');
assert.match(css,/var\(--ws-type-reading-zh\)/,'Emmaus tool preview binds OS Chinese reading font');
const oneBookCSS=fs.readFileSync(path.join(root,'static/one/one-book.css'),'utf8');
assert.match(oneBookCSS,/ONE ↔ Westside Design OS \/ scoped typography normalization candidate/,'ONE tool receives scoped typography migration');
assert.match(oneBookCSS,/--one-body-size:var\(--ws-type-scale-reading\)/,'ONE reading size consumes OS role rather than a competing type scale');

assert.match(html,/olive\/components\/speaker-baseline-v1\/baseline\.js/,'reuses protected speaker name component');
assert.match(html,/one\/one-dore-assets-241\.js/,'reuses original engraved archive');
assert.match(js,/books\.length!==66/,'guards the full canonical book count');
assert.match(js,/plates\.length!==241/,'right page rotates the entire canonical Doré library, after the art-directed opening plates');
assert.match(js,/let galleryIndex=211/,'canonical Doré Emmaus plate 212 leads the same complete 241-plate archive');
assert.match(js,/Math\.min\(distance,6\.5\)/,'does not stretch the approved Church/Magazine timing');
assert.match(js,/const move=.*6\.50[\s\S]*oliveIn=.*9\.44/,'both stages share a reversible scroll timeline');
assert.match(js,/appendChild\(sourceFigure\)/,'the original engraving node crosses into the receiving stage');
assert.doesNotMatch(js,/sourceTile\.style\.opacity=String\(1-smooth/,'Magazine Contents never disappear to expose the unrelated background film');
assert.doesNotMatch(js,/sourceCover\.style\.opacity=String\(1-smooth/,'approved cover remains in the continuous frame during transfer');
assert.match(js,/insertBefore\(transferFigure/,'reverse scroll restores the same original node');
assert.doesNotMatch(html,/em-handoff-photo/,'no added substitute picture is allowed');
assert.match(js,/const roster=\[/,'uses fixed factual speaker assets');
assert.match(css,/grid-template-columns:minmax\(0,2fr\) minmax\(0,1fr\)/,'Emmaus is left 2/3 and original engravings right 1/3');
assert.match(js,/rail\.addEventListener\('wheel',/,'horizontal ONE strip bridges vertical wheel to the P2 scroll owner');
assert.match(js,/scrollBy\(\{top:delta,behavior:'instant'\}\)/,'the rail forwards vertical wheel to the full-page handoff');
assert.doesNotMatch(js,/stopPropagation\(\)/,'P2 should not trap wheel propagation inside a second viewport');
assert.match(js,/appendChild\(emRight\)/,'existing ONE gallery itself transfers to the Olive image slot');
assert.match(js,/emmaus\.appendChild\(emRight\)/,'the same gallery returns on reverse scroll');
assert.doesNotMatch(html,/olive-handoff-(image|plate)/,'no duplicate Doré handoff image is inserted');
assert.match(js,/oliveHero\.style\.transform='none'/,'the speaker portrait never flies into the page');
assert.match(js,/oliveEditorial\.style\.clipPath=/,'Olive editorial fields reveal independently from the persistent spread');
assert.doesNotMatch(js,/olive\.style\.clipPath='inset/,'a whole-scene curtain would replace one page with another');
console.log('P2 03/04 isolated preview source contract: pass');

if(!process.env.P2_BROWSER_PROOF)process.exit(0);
const {chromium}=require('playwright');
(async()=>{
 const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
 const errors=[];
 try{
  for(const viewport of [{width:1648,height:928},{width:390,height:844}]){
   const page=await browser.newPage({viewport});
   page.on('pageerror',error=>errors.push(error.message));
   await page.goto('http://127.0.0.1:4173/experiments/p2-emmaus-olive-handoff-lab.html?d=9.10',{waitUntil:'domcontentloaded',timeout:45000});
   await page.waitForTimeout(550);
   assert.equal(await page.locator('.emmaus__number').count(),66,'all 66 ONE books have selectable numbers');
   assert.equal(await page.locator('#emmaus').getAttribute('aria-hidden'),'false','Emmaus visible in its reading dwell');
   assert.equal(await page.locator('#em-book-en').textContent(),'Luke');
   assert.equal(await page.locator('.emmaus__folio-layer').count(),7);
   assert.match(await page.locator('#emmaus-study-heading').textContent(),/復活/);
   assert.equal(await page.locator('#em-study-route li').count(),3);
   assert.equal(await page.locator('#emmaus').getAttribute('data-study-view'),'background');
   await page.locator('#em-tab-connections').click();
   assert.equal(await page.locator('#emmaus').getAttribute('data-study-view'),'connections');
   assert.match(await page.locator('#em-study-detail').textContent(),/詩篇 16:10/);
   await page.locator('#em-tab-questions').click();
   assert.match(await page.locator('#em-study-detail').textContent(),/以馬忤斯/);
   await page.locator('#em-tab-background').click();
   await page.locator('[data-book="41"]').evaluate(element=>element.click());
   assert.equal(await page.locator('#em-book-en').textContent(),'Mark','book selection changes live spread');
   assert.match(await page.locator('#emmaus-enter').getAttribute('href'),/book=41&chapter=1/,'selected volume opens the actual ONE chapter, not the default homepage');
   assert.match(await page.locator('#em-plate-selection').textContent(),/BOOK 41 \/ MARK/,'the selected book is carried into the right Doré editorial margin');
   const before=await page.evaluate(()=>scrollY);
   await page.locator('#emmaus-rail').hover();await page.mouse.wheel(0,500);await page.waitForTimeout(300);
   const after=await page.evaluate(()=>scrollY);
   assert(after>before,'vertical wheel on the book rail advances P2 instead of trapping inside ONE');
   // Verify one physical engraving moves out of and back into the already
   // published Magazine iframe, without an inserted second picture.
   await page.evaluate(()=>{
    const el=document.getElementById('proof-track');
    scrollTo({top:el.getBoundingClientRect().top+scrollY+7.0*innerHeight,behavior:'instant'});
   });
   await page.waitForTimeout(350);
   const magazineVisibility=await page.locator('#proof-original').evaluate(frame=>{
    const doc=frame.contentDocument?.querySelector('.p2-magazine iframe:not(.p2-magazine__home-film)')?.contentDocument;
    const left=doc?.getElementById('dual-contents'),right=doc?.getElementById('dual-cover');
    return [left?Number(getComputedStyle(left).opacity):0,right?Number(getComputedStyle(right).opacity):0];
   });
   assert(magazineVisibility[0]>.9&&magazineVisibility[1]>.9,
    '61%: existing Contents and cover remain visibly connected behind the moving original plate');
   assert.equal(await page.locator('#proof-stage > #dual-dore-plate').count(),1,
    'the actual magazine engraving is adopted into the shared P2 stage');
   const transferShot=path.join(root,'artifacts/p2-emmaus-olive',viewport.width+'-magazine-plate-transfer.png');
   fs.mkdirSync(path.dirname(transferShot),{recursive:true});
   await page.screenshot({path:transferShot});
   await page.locator('[data-jump="6.50"]').click();
   await page.waitForTimeout(200);
   assert.equal(await page.locator('#proof-stage > #dual-dore-plate').count(),0,
    'reverse scrolling restores the engraving to its original magazine document');
   // Hold the established Emmaus spread before moving into Olive.
   await page.locator('[data-jump="9.10"]').click();
   await page.waitForTimeout(150);
   assert.equal(await page.locator('#emmaus > #emmaus-gallery').count(),1,
    'at rest ONE retains its own right gallery');
   const emmausRect=await page.locator('#emmaus > #emmaus-gallery').boundingBox();
   const stageRect=await page.locator('#proof-stage').boundingBox();
   assert(emmausRect && stageRect && Math.abs(emmausRect.width-stageRect.width/3)<3,
    'Emmaus finishes at the agreed two-thirds to one-third ratio');
   const studyBounds=await page.locator('#emmaus-study').boundingBox();
   assert(studyBounds&&studyBounds.height>=140&&studyBounds.height<stageRect.height*.55,
    'ONE has a substantial but bounded study area between the Emmaus title and the book index');
   const controlsSize=await page.locator('#em-tab-background').evaluate(el=>getComputedStyle(el).fontSize);
   assert(parseFloat(controlsSize)>=12,'ONE tool controls remain readable when shown on P2');
   const emmausScreenshot=path.join(root,'artifacts/p2-emmaus-olive',viewport.width+'-emmaus-held.png');
   await page.screenshot({path:emmausScreenshot});
   await page.locator('[data-jump="10.05"]').click();await page.waitForTimeout(150);
   assert.equal(await page.locator('#olive-proof').evaluate(el=>getComputedStyle(el).opacity),'1','Olive separate fields remain opaque while the earlier spread persists');
   assert.equal(await page.locator('#emmaus').evaluate(el=>getComputedStyle(el).visibility),'visible','Emmaus remains on stage while its pieces become Olive');
   assert.equal(await page.locator('#proof-stage > #emmaus-gallery').count(),1,'same ONE gallery is the travelling image object');
   assert.equal(await page.locator('#olive-morph-hero').evaluate(el=>getComputedStyle(el).transform),'none','no overscaled speaker poster flies into frame');
   assert.equal(await page.locator('#olive-morph-hero').evaluate(el=>getComputedStyle(el).opacity),'0',
    'Olive portrait does not appear before the travelling engraving reaches its slot');
   assert(Number(await page.locator('.olive-proof__editorial').evaluate(el=>getComputedStyle(el).opacity))<.01,
    '82%: no premature blank white Olive editorial slab masks the previous ONE page');
   assert(Number(await page.locator('.olive-proof__kicker').evaluate(el=>getComputedStyle(el).opacity))<.15,
    '82%: do not pre-reveal Olive until the ONE/photo reflow begins');
   assert.equal(await page.locator('.olive-proof__bottom').evaluate(el=>getComputedStyle(el).opacity),'0',
    'the speaker register must not reveal before the moving engraved field is established');
   assert((await page.locator('.emmaus__left').evaluate(el=>getComputedStyle(el).clipPath)).includes('inset(0px 0px 0px 0'),
    'ONE stays legible during initial image travel');
   assert.equal(await page.locator('#olive-handoff-image').count(),0,'no second Doré image constructed');
   const oneBefore=await page.locator('.emmaus__left').evaluate(el=>getComputedStyle(el).clipPath);
   assert(oneBefore.includes('inset(0px 0px 0px 0'),'ONE is still fully legible before the picture crosses its title at 82%');
   const movingPanel=await page.locator('#proof-stage > #emmaus-gallery').boundingBox();
   assert(movingPanel && movingPanel.x<stageRect.x+stageRect.width*2/3,
    'ONE image field is physically crossing toward the Olive upper-left portrait slot');
   assert.match(await page.locator('.olive-proof__register').evaluate(el=>getComputedStyle(el).clipPath),/inset/,'speaker grid rises independently from the ONE rail');
   const midScreenshot=path.join(root,'artifacts/p2-emmaus-olive',viewport.width+'-mersi-mid.png');
   fs.mkdirSync(path.dirname(midScreenshot),{recursive:true});await page.screenshot({path:midScreenshot});
   await page.locator('[data-jump="11.10"]').click();await page.waitForTimeout(220);
   assert.equal(await page.locator('#olive-proof').getAttribute('aria-hidden'),'false','Olive Mountain follows Emmaus');
   assert.equal(await page.locator('#proof-stage > #emmaus-gallery').count(),0,'completed Olive restores source gallery to Emmaus');
   assert.equal(await page.locator('#olive-speaker-names button').count(),12,'twelve verified speakers retained');
   await page.locator('#olive-speaker-names button[data-speaker="derek-prince"]').evaluate(element=>element.click());
   assert.equal(await page.locator('#olive-main-image').getAttribute('alt'),'葉光明');
   await page.locator('[data-jump="6.50"]').click();await page.waitForTimeout(220);
   assert.equal(await page.locator('#olive-proof').getAttribute('aria-hidden'),'true','reverse scroll returns to approved magazine');
   assert.equal(await page.locator('#emmaus').getAttribute('aria-hidden'),'true');
   assert.equal(await page.locator('#emmaus > #emmaus-gallery').count(),1,'reverse scroll returns the original ONE image panel');
   const screenshot=path.join(root,'artifacts/p2-emmaus-olive',viewport.width+'-olive.png');
   fs.mkdirSync(path.dirname(screenshot),{recursive:true});
   await page.locator('[data-jump="11.10"]').click();await page.screenshot({path:screenshot});
   await page.close();
  }
  assert.deepEqual(errors,[],'no JavaScript errors in either browser size');
  console.log('P2 03/04 Chromium: desktop + phone; stage, books, wheel, posters, reverse scroll: pass');
 }finally{await browser.close()}
})().catch(error=>{console.error(error);process.exitCode=1});
