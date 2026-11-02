'use strict';
/* Isolated P2 03/04 proof — no runtime writes to the production homepage. */
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..');
const html=fs.readFileSync(path.join(root,'static/experiments/p2-emmaus-olive-handoff-lab.html'),'utf8');
const js=fs.readFileSync(path.join(root,'static/js/p2-emmaus-olive-preview.js'),'utf8');
const css=fs.readFileSync(path.join(root,'static/css/p2-emmaus-olive-preview.css'),'utf8');
const engraving=fs.readFileSync(path.join(root,'static/css/westside-engraving-authority.css'),'utf8');

const fiveCSS=fs.readFileSync(path.join(root,'static/css/p2-five-v15-continuation.css'),'utf8');
const fiveJS=fs.readFileSync(path.join(root,'static/js/p2-five-v15-continuation.js'),'utf8');
const emmausOriginalSVG=fs.readFileSync(path.join(root,'static/images/p2-realms/v15/03-emmaus-engraving-v1-5.svg'),'utf8');
const emmausRuntimeSVG=fs.readFileSync(path.join(root,'static/images/p2-realms/v15/03-emmaus-engraving-p2-local-bow-v2.svg'),'utf8');
assert.match(emmausOriginalSVG,/ws-bow-whole-slow-rotation/,'retain the original SVG master unchanged');
assert.match(fiveCSS,/03-emmaus-engraving-p2-local-bow-v2\.svg/,'P2 uses the optimized locally animated bow SVG');
assert.match(fiveCSS,/background-size:cover/,'the native SVG ratio must be preserved across screens');
assert.doesNotMatch(fiveCSS,/background-size:100% 100%/,'never stretch an engraved background nonuniformly');
assert.match(emmausRuntimeSVG,/#emmaus-bow-core-motion/,'only the central bow is allowed to rotate');
assert.match(emmausRuntimeSVG,/clipPathUnits="userSpaceOnUse"/,'local knot is clipped in fixed SVG coordinates');
assert.doesNotMatch(emmausRuntimeSVG,/#emmaus-motion-rotor\s*\{[\s\S]*?animation:/,'the original full-field motion group must remain motionless');
const rotatingCore=emmausRuntimeSVG.match(/<g id="emmaus-bow-core-motion"[^>]*>([\s\S]*?)<\/g>/);
assert(rotatingCore&&((rotatingCore[1].match(/<path\b/g)||[]).length===40),'exactly 40 local engraved paths move; all outer paths remain fixed');
assert.match(emmausRuntimeSVG,/<svg[^>]+viewBox="0 0 1440 900"/,'native vector geometry and viewBox remain');
assert((emmausRuntimeSVG.match(/<path\b/g)||[]).length<=900,'optimized engraving reduces the SVG DOM path count');
assert(emmausRuntimeSVG.length<emmausOriginalSVG.length*.65,'P2 runtime SVG is substantially lighter than the preserved master');
assert.doesNotMatch(emmausRuntimeSVG,/<(?:image|foreignObject|filter)\b|data:image/,'P2 background remains pure native SVG');
assert.match(fiveJS,/im\.dataset\.src=srcRoot\+sec\.image/,'future SVG chapters are not decoded while entering Emmaus');
assert.match(js,/if\(fullDistance>=12\)/,'the 03/04 animator stops repaints once 05–07 own the page');
assert.match(html,/p2\/living-water\.html\?embed=1/,'reuses approved P2 Church/Magazine source');
assert.match(html,/one\/one-data\.js/,'reads the canonical 66-book inventory');
assert.match(html,/one\/luke-21-24\.js/,'features the original Luke 24 ONE study content');
assert.doesNotMatch(html,/<img class="emmaus__scroll-engraving"/,'Emmaus tool panel contains no decorative engraving');
assert.doesNotMatch(html,/emmaus__realm-nav|emmaus__folio-layer/,'no second spine is inserted in the Emmaus chapter');
assert.doesNotMatch(js,/data-realm-jump|realmNav/,'Magazine spines are not replaced by a second navigation controller');
assert.match(html,/id="proof-ground-toggle"/,'P2 preview provides a fixed-folio A/B control');
assert.match(html,/westside-engraving-authority\.css/,'uses the one existing engraving authority');
for(const realm of ['church','magazine','sermon','book','cinema','life','bible']){
 assert.match(engraving,new RegExp('data-realm='+realm+'\\]'),
  'the already-owned Westside engraving authority registers '+realm);
}
assert.match(html,/id="p2-realm-background"/,'the background texture is its own field');
assert.match(js,/fixedGround=new URLSearchParams\(location\.search\)\.get\('ground'\)==='1'/,
 'engraved-background mode is opt-in and default remains unchanged');
assert.match(js,/const validMagazine=original&&coverBounds/,
 'the later chapters validate the approved magazine source formats before any projected handoff');
assert.match(js,/Math\.abs\(original\.w\/original\.h-1\)/,'Contents must remain square');
assert.match(js,/Math\.abs\(coverBounds\.w\/coverBounds\.h-\.625\)/,'cover must remain 5:8');
assert.match(js,/sourceSpine=sourceDoc\?\.getElementById\('dual-continuum'\)/,
 'the original frozen sevenfold spine belongs INSIDE the protected Magazine aperture');
assert.match(js,/const clip='path\("/,
 'engraving field must cut out the measured Magazine folio hole');
assert.match(js,/const coverFolio=validMagazine\?coverBounds/,
 'the right gallery takes its exact 5:8 size from the approved Magazine cover');
assert.match(js,/const fullLeft=\{x:master\.x,y:master\.y,w:fullRight\.x-master\.x/,
 'ONE takes the remaining Contents width rather than forcing the cover to one-third');
const binding=fs.readFileSync(path.join(root,'static/css/p2-emmaus-bookbinding-v7.css'),'utf8');
assert(binding.includes('V10 / EXTERIOR CLOTH PROOF'),
 'V10 must replace the Bible surround, not modify or duplicate magazine cover');
assert(binding.includes('body[data-p2-surround="cloth"] #p2-realm-background[data-realm="bible"]'),
 'the approved ONE cover cloth must replace engraving only in 03 exterior');
assert(binding.includes('/one/cover-texture-antique-green.png'),
 'the canonical ONE image is reused rather than regenerated');
assert(js.includes("document.body.dataset.p2Surround=surround"),
 'the controlled P2 exterior supports comparative engraving and cloth states');
assert(js.includes("emRight.style.setProperty('--em-binding-reveal',String(oneDrop))"),
 'the matching green cloth rim must appear on the right 5:8 Doré folio');

assert(js.includes('const move=smooth((distance-6.50)/.72)'), 'first turn follows P2 scroll');
assert(js.includes('const archive=smooth((distance-7.66)/.64)'), 'second turn follows P2 scroll');
assert(js.includes('const oneDrop=smooth((distance-8.55)/.55)'), 'reading appears only after second turn');
assert(!js.includes('sourceFigure.cloneNode(true)'),'the original Magazine engraving is never duplicated or moved');
assert(js.includes('emCover.style.clipPath=greenClip'),'ONE cover uses lightweight editorial clipping');
assert(binding.includes('/one/cover-texture-antique-green.png')&&
 binding.includes('/one/cover-golden-shoot-frame-transparent.png'),
 'P2 directly reuses real ONE cloth and gold master');
assert(html.includes('路加福音 24:27')&&html.includes('路加福音 24:32'),
 'the Emmaus cover must show both canonical section scripture references');
assert.match(js,/olive\.style\.inset='auto'/,
 'the Olive stage is also constrained to the Magazine geometry');
assert.match(js,/active:distance<6\.6/,
 'the homepage film is not artificially replayed in the next chapters');
assert.match(js,/oliveGround\.style\.opacity=String\(oliveIn\*move\)/,
 'Olive exterior engraving fades in as a distinct background layer, without a hard swap');
assert.match(html,/id="p2-olive-ground-crossfade"/,
 'the two exterior textures share one measured Magazine aperture');
assert.doesNotMatch(js,/surroundX|surroundTop|filmContinuity|filmToggle|createElement\(['"](?:iframe|video)['"]\)/,
 'the rejected cinema surround and new media instances are gone');
assert.match(css,/#p2-realm-background\[data-realm="bible"\]/,
 'Bible engraving derives from manuscript material');
assert.match(css,/#p2-realm-background\[data-realm="sermon"\]/,
 'Sermon engraving derives from olive terraces');
assert.match(css,/--ws-papyrus/,'Emmaus background inherits ONE papyrus palette, not Magazine white');
assert.match(css,/scroll-micro-engraving\.svg/,'scroll edge engraving is visible in chapter structure');
assert.match(js,/ONE_DATA\?\.luke\?\.chapterStudies\?\.\['24'\]/,'chapter text comes from canonical ONE, never invented copy');
assert.match(css,/var\(--ws-type-reading-zh\)/,'Emmaus tool preview binds OS Chinese reading font');
const oneBookCSS=fs.readFileSync(path.join(root,'static/one/one-book.css'),'utf8');
assert.match(oneBookCSS,/ONE ↔ Westside Design OS \/ scoped typography normalization candidate/,'ONE tool receives scoped typography migration');
assert.match(oneBookCSS,/--one-body-size:var\(--ws-type-scale-reading\)/,'ONE reading size consumes OS role rather than a competing type scale');

assert.match(html,/olive\/components\/speaker-baseline-v1\/baseline\.js/,'reuses protected speaker name component');
assert.match(html,/one\/one-dore-assets-241\.js/,'reuses original engraved archive');
assert.match(js,/books\.length!==66/,'guards the full canonical book count');
assert.match(js,/plates\.length!==241/,'right page rotates the entire canonical Doré library, after the art-directed opening plates');
assert.match(js,/let galleryIndex=211/,'canonical Doré Emmaus plate 212 leads the same complete 241-plate archive');
assert.match(js,/const bookPlates=/,'indexed canonical Doré plates are matched to books');
assert.match(js,/Math\.random\(\)/,'unillustrated volumes receive a random canonical-archive start');
assert.match(js,/selectGalleryForBook\(number\)/,'book selection changes gallery sequence');
assert.match(js,/renderBookStudy\(number\)/,'book selection also changes ONE study view');
assert.match(js,/Math\.min\(distance,6\.5\)/,'does not stretch the approved Church/Magazine timing');
assert.match(js,/const move=.*6\.50[\s\S]*oliveIn=.*9\.44/,'both stages share a reversible scroll timeline');
assert.doesNotMatch(js,/transferFigure=sourceFigure\\.cloneNode\\(true\\)/,
 'handoff must not clone or horizontally move Magazine engraving');
assert.doesNotMatch(js,/appendChild\(sourceFigure\)/,'Magazine source remains inside its original iframe');
assert.doesNotMatch(js,/sourceTile\.style\.opacity=String\(1-smooth/,'Magazine Contents never disappear to expose the unrelated background film');
assert.doesNotMatch(js,/sourceCover\.style\.opacity=String\(1-smooth/,'approved cover remains in the continuous frame during transfer');
assert.match(js,/transferHome\.style\.visibility=transferOriginalVisibility/,'reverse scrolling restores the original artwork visibility');
assert.doesNotMatch(html,/em-handoff-photo/,'no added substitute picture is allowed');
assert.match(js,/const roster=\[/,'uses fixed factual speaker assets');
assert.match(css,/grid-template-columns:minmax\(0,2fr\) minmax\(0,1fr\)/,'Emmaus is left 2/3 and original engravings right 1/3');
assert.match(js,/rail\.addEventListener\('wheel',/,'original horizontal ONE navigation handles vertical wheel as horizontal browse');
assert.match(js,/rail\.scrollLeft\+=event\.deltaY\*unit/,'the book strip scrolls horizontally rather than ejecting readers from Emmaus');
assert.doesNotMatch(js,/stopPropagation\(\)/,'P2 should not trap wheel propagation inside a second viewport');
assert.doesNotMatch(js,/\$\('#proof-stage'\)\.appendChild\(emRight\)/,
 'the 03→04 gallery must never leave its original editorial column');
assert.match(js,/poseRect\(emRight,fullRight,fullRight,1\)/,
 'the gallery stays in its original fixed 1/3 right-page rectangle');
assert.doesNotMatch(html,/olive-handoff-(image|plate)/,'no duplicate Doré handoff image is inserted');
assert.match(js,/oliveHero\.style\.transform='none'/,'the speaker portrait never flies into the page');
assert.match(js,/oliveEditorial\.style\.clipPath=/,'Olive editorial fields reveal independently from the persistent spread');
assert.match(js,/olive\.style\.clipPath='inset\(0 0 0 '/,
 'the incoming complete Olive page reveals only inside its unchanged Magazine footprint');
assert.doesNotMatch(js,/emLeft\.style\.width=nextWidth/,
 'ONE must not reflow, resize or be crushed during 03→04');
assert.doesNotMatch(js,/poseRect\(emRight,fullRight,destination,morphMove\)/,
 'the Doré gallery must not move or scale into Olive');
assert.match(js,/oliveEditorial\.style\.opacity='1'/,
 'the destination folio is already composed before it becomes visible');
// Emmaus rework: the 66-book controller stays live, while the approved magazine
// book-spine treatment is frozen without a separate Emmaus folio controller.
assert.match(html,/aria-live="polite"/,'selected volume identity is announced');
assert.match(js,/renderBookStudy\(number,chapter\)/,'ONE work window accepts per-book chapter state');
assert.match(js,/emmaus__chapter-choice/,'unfeatured volumes have functional chapter selectors');
assert.match(js,/if\(ticket!==plateVersion\)return/,'late image responses cannot overwrite new book selection');
assert.match(js,/plateEls\.forEach\(img=>img\.classList\.remove\('is-active'\)\)/,
 'old-book image is hidden before new plate is resolved');
assert.match(js,/ORIGINAL ARCHIVE UNAVAILABLE/,'failed artwork load states unavailability, not a fake plate');
assert.doesNotMatch(js,/aria-current|realmNav/,'no duplicated sevenfold active-state logic');
assert.match(css,/--em-paper:var\(--ws-one-paper\)/,
 'ONE paper must use the exact accepted ONE hue, registered in Design OS');
assert.doesNotMatch(css,/--em-paper:color-mix\(in oklab/,
 'old near-match gold blend must not return');
assert.match(css,/--em-ink:var\(--ws-night\)/,'ONE ink uses night blue, not olive green');
assert.match(css,/p2-emmaus-scroll-micro-engraving\.svg/,'engraved space uses its own vector');
assert.match(css,/--ws-type-scale-display-lg/,'Emmaus display uses the Design OS type scale');
// V16 visual contract: native scalable paths, ONE colors, and film-field-only scope.
const v16=fs.readFileSync(path.join(root,'static/images/p2-emmaus-chronology-engraving-v16.svg'),'utf8');
assert.match(v16,/<svg[^>]*viewBox="0 0 1600 900"/,'native full-bleed SVG uses the source film field geometry');
assert.match(v16,/id="time-longitudes"/,'temporal wire grid must not degrade to a fluid flow field');
assert.match(v16,/id="scripture-sixty-six"/,'scriptural-register layer survives optimization');
assert.match(v16,/id="interpretive-passage"/,'time passage is a vector geometry layer');
assert.match(v16,/id="micro-engraved-lenses"/,'localized hatching adds non-water tonal variety');
assert((v16.match(/<path\b/g)||[]).length>1200,'V16 uses real vector engraving lines, not a rasterized still');
assert.doesNotMatch(v16,/<(?:image|foreignObject|filter)\b|data:image/,'V16 must not embed raster, foreign DOM or visual filters');
assert.match(css,/body\[data-p2-engraving="v16"\] #p2-realm-background\[data-realm="bible"\]/,'the candidate takes over the existing VIDEO negative space');
assert.match(css,/background-color:var\(--ws-one-paper,#ded096\)/,'the visible paper is the ONE Design OS surface, not dark magazine night');
assert.match(html,/p2Engraving='v16'/,'V16 stays in opt-in proof and never changes the default');
const {execFileSync}=require('node:child_process');
const generatedV16=execFileSync(process.execPath,[path.join(root,'scripts/build-emmaus-engraving-v16.mjs')],{encoding:'utf8',maxBuffer:1024*1024*3});
assert.equal(generatedV16,v16,'V16 SVG must be reproducible from its dependency-free source generator');

// V17 creative source gate — remains in existing P2 contract, not new CI.
const v17=fs.readFileSync(path.join(root,'static/images/p2-emmaus-time-held-open-v17.svg'),'utf8');
assert.match(v17,/<svg[^>]*viewBox="0 0 1600 900"/,'V17 keeps the film-field coordinate frame');
for(const key of ['time-sectioned-aperture','pressed-plate-highlights','engraved-distance-registers',
                  'sixty-six-canonical-cross-references','time-plate-crosshatch','editorial-chapter-indexing']){
 assert(v17.includes('id="'+key+'"'),'V17 preserves the '+key+' art-directed layer');
}
assert((v17.match(/<path\b/g)||[]).length>=2600,'V17 exports true parametric SVG engraving paths');
assert.doesNotMatch(v17,/<(?:image|foreignObject|filter)\b|data:image/,'V17 cannot be a traced PNG or generated photo');
assert.match(css,/body\[data-p2-engraving="v17"\] #p2-realm-background\[data-realm="bible"\]/,
 'V17 belongs to the measured video negative space, not the ONE study paper');
assert.match(css,/background-color:var\(--ws-one-paper,#ded096\)/,
 'V17 retains the approved ONE paper material color');
assert.match(html,/p2Engraving='v17'/,'V17 may only be tested by opt-in branch query');
const regenV17=execFileSync(process.execPath,[path.join(root,'scripts/build-emmaus-engraving-v17.mjs')],
 {encoding:'utf8',maxBuffer:1024*1024*4});
assert.equal(v17,regenV17,'V17 is deterministically rebuilt from its checked-in original source');

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
   await page.goto('http://127.0.0.1:4173/experiments/p2-emmaus-olive-handoff-lab.html?five=0&ground=0&d=9.10',{waitUntil:'domcontentloaded',timeout:45000});
   await page.waitForTimeout(550);
   assert.equal(await page.locator('.emmaus__number').count(),66,'all 66 ONE books have selectable numbers');
   assert.equal(await page.locator('#emmaus').getAttribute('aria-hidden'),'false','Emmaus visible in its reading dwell');
   assert.equal(await page.locator('#em-book-en').textContent(),'Luke');
   assert.equal(await page.locator('.emmaus__folio-layer').count(),0,'no second sevenfold spine is created');
   const surroundProof=await page.locator('#p2-realm-background').evaluate(el=>({
    mode:document.body.dataset.p2Surround,
    texture:getComputedStyle(el).backgroundImage,
    size:getComputedStyle(el).backgroundSize,
    legacyEngraving:getComputedStyle(el,'::after').content
   }));
   assert.equal(surroundProof.mode,'cloth','current P2 draft defaults to the green cloth');
   assert.match(surroundProof.texture,/cover-texture-antique-green/,
    'the exterior must visually use original ONE green-cloth cover texture');
   assert.equal(surroundProof.legacyEngraving,'none',
    'the old radiating engraving cannot remain above the cloth');
   const rim=await page.locator('#emmaus-gallery .emmaus__right-binding').evaluate(el=>({
    opacity:Number(getComputedStyle(el).opacity),
    bg:getComputedStyle(el.querySelector('.emmaus__right-binding-top')).backgroundImage
   }));
   assert(rim.opacity>.95,'both open folios must retain green binding');
   assert.match(rim.bg,/cover-texture-antique-green/,'right frame uses the same ONE textile');
   await page.screenshot({path:path.join(groundDir,viewport.width+'-green-cloth-exterior-v10.png')});
   const paper=await page.locator('#emmaus > .emmaus__left').evaluate(el=>{
    const cloth=getComputedStyle(el),page=getComputedStyle(el.querySelector('.emmaus__binding-paper'));
    return {paper:page.backgroundColor,clothImage:cloth.backgroundImage,
     token:getComputedStyle(document.documentElement).getPropertyValue('--ws-one-paper').trim()};
   });
   assert.equal(paper.paper,'rgb(222, 208, 150)','opened Bible must keep ONE papyrus inside the cloth cover');
   assert.match(paper.clothImage,/cover-texture-antique-green/,'binding cloth must reuse the genuine ONE asset');
   assert.equal(paper.token,'rgb(222 208 150)','ONE paper token stays the shared Design OS source');
   assert.equal(await page.locator('body').getAttribute('data-fixed-ground'),'off',
    'protected original version is the default');
   await page.waitForFunction(()=>{
    const frame=document.querySelector('#proof-original')?.contentDocument;
    const source=frame?.querySelector('.p2-magazine iframe:not(.p2-magazine__home-film)')?.contentDocument;
    const stage=source?.getElementById('dual-stage');
    return stage?.dataset?.spread==='contents-square-cover-5-8' &&
      Number(stage?.dataset?.spineFlip)>0.99;
   },null,{timeout:20000});
   const sourceGeometry=await page.locator('#proof-original').evaluate(frame=>{
    const doc=frame.contentDocument;
    const source=doc?.querySelector('.p2-magazine iframe:not(.p2-magazine__home-film)')?.contentDocument;
    const c=source?.getElementById('dual-cover')?.getBoundingClientRect();
    const t=source?.getElementById('dual-contents')?.getBoundingClientRect();
    const spine=source?.getElementById('dual-continuum')?.getBoundingClientRect();
    if(!c||!t||!spine)return null;
    const all=[c,t,spine],x=Math.min(...all.map(r=>r.x)),y=Math.min(...all.map(r=>r.y));
    return {x,y,
     w:Math.max(...all.map(r=>r.right))-x,
     h:Math.max(...all.map(r=>r.bottom))-y,
     coverWidth:c.width,coverHeight:c.height,
     filmCount:doc.querySelectorAll('.p2-magazine__home-film').length};
   });
   assert(sourceGeometry,'Magazine geometry must be available before acceptance');
   assert.equal(sourceGeometry.filmCount,1,'the ONE existing magazine film player is preserved');
   await page.locator('#proof-ground-toggle').click();await page.waitForTimeout(220);
   assert.equal(await page.locator('body').getAttribute('data-fixed-ground'),'on',
    'opt-in shared proportions and engraved backdrop are active');
   assert.equal(await page.locator('#proof-ground-toggle').getAttribute('aria-pressed'),'true');
   assert.equal(await page.locator('#p2-realm-background').getAttribute('data-realm'),'bible');
   assert.match(await page.locator('#p2-realm-background').evaluate(
    el=>getComputedStyle(el,'::after').backgroundImage),/repeating-linear-gradient/,
    'Bible uses the real shared folio engraving rules');
   assert.match(await page.locator('#p2-realm-background').evaluate(
    el=>getComputedStyle(el).clipPath),/path\(/,
    'real Magazine aperture leaves the editorial pages uncovered');
   const stageGround=await page.locator('#proof-stage').boundingBox();
   const emLeaf=await page.locator('#emmaus > .emmaus__left').boundingBox();
   const emPlate=await page.locator('#emmaus > #emmaus-gallery').boundingBox();
   assert(stageGround&&emLeaf&&emPlate,'the same Bible leaf and original Doré image remain');
   const expectedX=stageGround.x+sourceGeometry.x,expectedY=stageGround.y+sourceGeometry.y;
   const expectedW=sourceGeometry.w,expectedH=sourceGeometry.h;
   assert(Math.abs(emLeaf.x-expectedX)<4,'Bible leaf starts at the real Magazine left boundary');
   assert(Math.abs(emLeaf.y-expectedY)<4,'Bible top uses the Magazine field exactly');
   assert(Math.abs(emLeaf.width+emPlate.width-expectedW)<4,'the complete Bible spread fits inside Magazine bounds');
   assert(Math.abs(emLeaf.height-expectedH)<4,'Bible folio matches Magazine height');
   assert(Math.abs(emLeaf.x+emLeaf.width-emPlate.x)<4,'Bible leaf and engraving have no new gap');
   if(viewport.width>820){
    assert(Math.abs(emPlate.width-sourceGeometry.coverWidth)<4,
     'right Doré gallery is exactly as wide as the original Magazine cover');
    assert(Math.abs(emPlate.height-sourceGeometry.coverHeight)<4,
     'right Doré gallery retains the original cover height and 5:8 aspect ratio');
   }else{
    assert(Math.abs(emLeaf.width-2*emPlate.width)<4,
     'phone keeps its compact horizontal editorial allocation');
   }
   assert.equal(await page.locator('#emmaus > .emmaus__left').evaluate(
    el=>getComputedStyle(el).maskImage),'none',
    'previously rejected narrow mask is fully removed');
   const groundDir=path.join(root,'artifacts/p2-emmaus-olive');
   fs.mkdirSync(groundDir,{recursive:true});
   await page.screenshot({path:path.join(groundDir,viewport.width+'-fixed-ground-bible.png')});
   // New 02 -> 03 stage: original ONE green-and-gilt title cover first,
   // opened papyrus and readable selected-book masthead only afterwards.
   await page.locator('[data-jump="7.42"]').click();
   await page.waitForTimeout(120);
   assert.equal(await page.locator('#emmaus').getAttribute('data-cover-state'),'green');
   const coverState=await page.locator('#em-entry-cover').evaluate(el=>({
    visible:getComputedStyle(el).visibility,
    gilded:getComputedStyle(el.querySelector('.emmaus__entry-cover-gilt')).maskImage,
    ratio:el.querySelector('.emmaus__entry-cover-leaf').getBoundingClientRect()
   }));
   assert.equal(coverState.visible,'visible','ONE Emmaus gilt cover precedes page opening');
   assert.match(coverState.gilded,/cover-golden-shoot-frame-transparent/,'ornament is the original ONE hot-stamped master');
   await page.screenshot({path:path.join(groundDir,viewport.width+'-emmaus-green-one-cover.png')});
   await page.locator('[data-jump="9.10"]').click();
   await page.waitForTimeout(150);
   assert.equal(await page.locator('#emmaus').getAttribute('data-cover-state'),'reading');
   assert.equal(await page.locator('#em-entry-cover').isVisible(),false,'book cover disappears after opening');

   await page.locator('[data-jump="11.10"]').click();await page.waitForTimeout(220);
   assert.equal(await page.locator('#p2-realm-background').getAttribute('data-realm'),'bible',
    'Bible backdrop stays stable during the Olive reveal');
   const oliveField=await page.locator('#p2-olive-ground-crossfade').evaluate(el=>({
    opacity:Number(getComputedStyle(el).opacity),
    clip:getComputedStyle(el).clipPath
   }));
   assert(oliveField.opacity>.99,'the Olive backdrop has fully faded in by chapter 04');
   assert.match(oliveField.clip,/path\(/,'both background layers use the same Magazine aperture');
   const olRect=await page.locator('#olive-proof').boundingBox();
   assert(olRect&&Math.abs(olRect.x-expectedX)<4&&Math.abs(olRect.y-expectedY)<4,
    'Olive retains the Magazine top-left origin');
   assert(Math.abs(olRect.width-expectedW)<4&&Math.abs(olRect.height-expectedH)<4,
    'Olive retains the exact source footprint');
   await page.screenshot({path:path.join(groundDir,viewport.width+'-fixed-ground-sermon.png')});
   await page.locator('[data-jump="9.10"]').click();await page.waitForTimeout(220);
   assert.equal(await page.locator('#p2-realm-background').getAttribute('data-realm'),'bible');
   await page.locator('#proof-ground-toggle').click();await page.waitForTimeout(170);
   assert.equal(await page.locator('body').getAttribute('data-fixed-ground'),'off');
   assert.equal(await page.locator('#p2-realm-background').evaluate(
    el=>getComputedStyle(el).opacity),'0','baseline background restores on OFF');
   assert.match(paper.image,/SITE-TEMPLE-STONE-LIGHT/,'Emmaus keeps the original ONE paper texture, not magazine white');
   assert.match(await page.locator('#emmaus-study-heading').textContent(),/復活/);
   assert.equal(await page.locator('#em-study-route li').count(),2);
   assert.equal(await page.locator('#emmaus').getAttribute('data-study-view'),'background');
   if(viewport.width>820){
    await page.locator('#em-tab-connections').click();
    assert.equal(await page.locator('#emmaus').getAttribute('data-study-view'),'connections');
    assert.match(await page.locator('#em-study-detail').textContent(),/詩篇 16:10/);
    await page.locator('#em-tab-questions').click();
    assert.match(await page.locator('#em-study-detail').textContent(),/以馬忤斯/);
    await page.locator('#em-tab-background').click();
   }else{
    assert.equal(await page.locator('.emmaus__study-tools').evaluate(el=>getComputedStyle(el).display),'none',
     'phone intentionally uses a readable single-column extract instead of forcing desktop tabs into 2/3 of 390px');
    assert.equal(await page.locator('.emmaus__study-reading').evaluate(el=>getComputedStyle(el).display),'flex');
    const studyHeight=await page.locator('#emmaus-study').evaluate(el=>el.getBoundingClientRect().height);
    assert(studyHeight<260,'phone study excerpt does not leave a half-empty fixed-height box');
   }
   await page.locator('[data-book="41"]').evaluate(element=>element.click());
   assert.equal(await page.locator('#em-book-en').textContent(),'Mark','book selection changes live spread');
   assert.match(await page.locator('#emmaus-enter').getAttribute('href'),/book=41&chapter=1/,'selected volume opens the actual ONE chapter, not the default homepage');
   assert.match(await page.locator('#em-plate-selection').textContent(),/41 \/ MARK/,'book name appears in the right Doré margin');
   assert.equal(await page.locator('#emmaus').getAttribute('data-gallery-start'),'183','Mark selects its first indexed Doré plate');
   assert.match(await page.locator('#emmaus-study-heading').textContent(),/馬可福音/,'study section follows Mark rather than staying on Luke');
   await page.locator('[data-book="1"]').evaluate(el=>el.click());
   assert.equal(await page.locator('#emmaus').getAttribute('data-gallery-start'),'1','Genesis begins with Doré Creation of Light');
   assert.match(await page.locator('#em-study-ref').textContent(),/創世記/,'Genesis updates study identity');
   await page.locator('[data-book="59"]').evaluate(el=>el.click());
   assert.equal(await page.locator('#emmaus').getAttribute('data-illustration-mode'),'random-fallback','unillustrated James uses a random valid catalogue start');
   const fallbackIndex=Number(await page.locator('#emmaus').getAttribute('data-gallery-start'));
   assert(fallbackIndex>=1&&fallbackIndex<=241,'random fallback remains inside the canonical complete 241-plate archive');
   await page.locator('[data-book="42"]').evaluate(el=>el.click());
   assert.equal(await page.locator('#emmaus').getAttribute('data-gallery-start'),'193','Luke begins at first assigned Doré plate');
   assert.match(await page.locator('#em-study-ref').textContent(),/路加福音/);
   assert.equal(await page.locator('.emmaus__realm-nav').count(),0,'original magazine spine stays with Magazine');
   await page.locator('[data-jump="11.10"]').click();
   await page.waitForTimeout(120);
   assert.equal(await page.locator('#olive-proof').getAttribute('aria-hidden'),'false',
    'original P2 preview controls still reach Olive Mountain');
   await page.locator('[data-jump="9.10"]').click();
   await page.waitForTimeout(120);
   assert.equal(await page.locator('#emmaus').getAttribute('aria-hidden'),'false',
    'P2 scene controls stay reversible through the same scroll controller');
   const before=await page.evaluate(()=>({pageY:scrollY,railX:document.getElementById('emmaus-rail').scrollLeft}));
   await page.locator('#emmaus-rail').hover();
   await page.mouse.wheel(0,500);await page.waitForTimeout(300);
   const after=await page.evaluate(()=>({pageY:scrollY,railX:document.getElementById('emmaus-rail').scrollLeft}));
   assert(after.railX>before.railX,'wheel should browse books without requiring memorized volume numbers');
   assert(Math.abs(after.pageY-before.pageY)<5,'wheel must not unexpectedly exit Emmaus');
   // V8: verify the original square Doré NEVER moves, no clone is created,
   // first flip reveals ONE's green cover at the right in its 5:8 frame,
   // second flip uncovers the archive, then the left becomes CUV/KJV reading.
   const sourcePlate=async()=>page.locator('#proof-original').evaluate(frame=>{
    const source=frame.contentDocument?.querySelector('.p2-magazine iframe:not(.p2-magazine__home-film)')?.contentDocument;
    const plate=source?.getElementById('dual-dore-plate');
    const box=plate?.getBoundingClientRect();
    return {parent:plate?.parentElement?.id,visible:plate?.style.visibility,
     box:box?{x:box.x,y:box.y,w:box.width,h:box.height}:null};
   });
   const baseline=await sourcePlate();
   assert(baseline?.box&&baseline.parent==='dual-contents','original magazine engraving remains attached to Contents');
   assert.equal(await page.locator('#proof-stage > #dual-dore-plate').count(),0,
     'the old travelling Doré plate projection must not be created');
   await page.locator('[data-jump="7.42"]').click();
   await page.waitForTimeout(160);
   assert.equal(await page.locator('#emmaus').getAttribute('data-cover-state'),'green');
   assert.equal(await page.locator('#em-entry-cover').isVisible(),true);
   const firstState=await page.locator('#em-entry-cover').evaluate(el=>({
     side:el.parentElement?.id,clip:getComputedStyle(el).clipPath,
     image:getComputedStyle(el.querySelector('.emmaus__entry-cover-leaf')).backgroundImage
   }));
   assert.equal(firstState.side,'emmaus-gallery','the ONE green front cover replaces the RIGHT magazine cover');
   assert.match(firstState.image,/cover-texture-antique-green/);
   assert(firstState.clip.startsWith('inset('),'the full ONE cover is revealed by a mask');
   await page.screenshot({path:path.join(groundDir,viewport.width+'-one-green-cover-right.png')});
   await page.locator('[data-jump="8.16"]').click();
   await page.waitForTimeout(140);
   assert.equal(await page.locator('#emmaus').getAttribute('data-cover-state'),'second-turn');
   const mid=await page.locator('#em-entry-cover').evaluate(el=>getComputedStyle(el).clipPath);
   assert(mid.startsWith('inset('),'second turn is a scroll-owned mask');
   await page.screenshot({path:path.join(groundDir,viewport.width+'-one-second-turn.png')});
   await page.locator('[data-jump="9.10"]').click();
   await page.waitForTimeout(150);
   const settled=await sourcePlate();
   assert.equal(await page.locator('#proof-stage > #dual-dore-plate').count(),0);
   assert.equal(settled.parent,'dual-contents');
   assert.equal(settled.visible,baseline.visible,'the original left engraving was not hidden or adopted');
   assert(Math.abs(settled.box.w-baseline.box.w)<3,'the original engraving retains its dimensions');
   assert.equal(await page.locator('#emmaus').getAttribute('data-cover-state'),'reading');
   assert.equal(await page.locator('#em-entry-cover').isVisible(),false);
   await page.locator('[data-jump="6.50"]').click();
   await page.waitForTimeout(180);
   assert.equal(await page.locator('#proof-stage > #dual-dore-plate').count(),0,
     'reverse scrolling restores the original Magazine without transient clones');
   await page.locator('[data-jump="9.10"]').click();
   await page.waitForTimeout(150);
   // Hold the established Emmaus spread before moving into Olive.
   await page.locator('[data-jump="9.10"]').click();
   await page.waitForTimeout(150);
   assert.equal(await page.locator('#emmaus > #emmaus-gallery').count(),1,
    'at rest ONE retains its own right gallery');
   const emmausRect=await page.locator('#emmaus > #emmaus-gallery').boundingBox();
   const stageRect=await page.locator('#proof-stage').boundingBox();
   const lockedCoverWidth=viewport.width>820?sourceGeometry.coverWidth:expectedW/3;
   assert(emmausRect && stageRect && Math.abs(emmausRect.width-lockedCoverWidth)<3,
    'Emmaus gallery never becomes smaller than the approved cover after handoff');
   const studyBounds=await page.locator('#emmaus-study').boundingBox();
   assert(studyBounds&&studyBounds.height>=140&&studyBounds.height<stageRect.height*.55,
    'ONE has a substantial but bounded study area between the Emmaus title and the book index');
   const controlsSize=await page.locator('#em-tab-background').evaluate(el=>getComputedStyle(el).fontSize);
   assert(parseFloat(controlsSize)>=12,'ONE tool controls remain readable when shown on P2');
   const emmausScreenshot=path.join(root,'artifacts/p2-emmaus-olive',viewport.width+'-emmaus-held.png');
   await page.screenshot({path:emmausScreenshot});
   await page.locator('[data-jump="10.05"]').click();await page.waitForTimeout(150);
   const midState=await page.evaluate(()=>{
    const gallery=document.getElementById('emmaus-gallery');
    const olive=document.getElementById('olive-proof'),left=document.querySelector('#emmaus .emmaus__left');
    const rect=e=>{const r=e.getBoundingClientRect();return{x:r.x,y:r.y,w:r.width,h:r.height}};
    return {left:rect(left),gallery:rect(gallery),olive:rect(olive),
      clip:getComputedStyle(olive).clipPath,
      galleryParent:gallery.parentElement.id,
      opacity:getComputedStyle(olive).opacity,
      ground:Number(getComputedStyle(document.getElementById('p2-olive-ground-crossfade')).opacity)};
   });
   assert.equal(midState.galleryParent,'emmaus','the gallery must stay in its original right column');
   assert.equal(midState.opacity,'1','the destination page is fully assembled inside its reveal');
   assert.match(midState.clip,/inset\(/,'the actual destination folio reveals in-place');
   assert(midState.ground>0&&midState.ground<1,'background crossfades rather than flashing');
   assert(Math.abs(midState.gallery.w-lockedCoverWidth)<4,
    'the Doré image retains the Magazine cover width through 03→04');
   assert(Math.abs(midState.left.w-(expectedW-lockedCoverWidth))<4,
    'ONE uses the remainder without a second gallery resize');
   assert.equal(await page.locator('#olive-morph-hero').evaluate(el=>getComputedStyle(el).transform),'none',
    'the Olive portrait remains in its fixed slot; no flying image');
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

   // Real P2 (not a separate SVG mock): verify that the background renders
   // as a static optimized SVG in the surviving Magazine surrounding field.
   await page.goto('http://127.0.0.1:4173/experiments/p2-emmaus-olive-handoff-lab.html?five=1&ground=1&d=9.10',
    {waitUntil:'domcontentloaded',timeout:45000});
   await page.waitForFunction(()=>{
    const bg=document.getElementById('p2-realm-background');
    return document.body.dataset.p2FiveV15==='on'&&
     document.body.dataset.fixedGround==='on'&&
     bg?.dataset.realm==='bible'&&
     getComputedStyle(bg).backgroundImage.includes('03-emmaus-engraving-p2-local-bow-v2.svg')&&
     Number(getComputedStyle(bg).opacity)>.9;
   },null,{timeout:25000});
   const asset=await page.request.get('http://127.0.0.1:4173/images/p2-realms/v15/03-emmaus-engraving-p2-local-bow-v2.svg');
   assert.equal(asset.status(),200,'optimized SVG exists in the actual Hugo preview output');
   const validSVG=await page.evaluate(xml=>!(
    new DOMParser().parseFromString(xml,'image/svg+xml').getElementsByTagName('parsererror').length
   ),await asset.text());
   assert(validSVG,'browser can parse the optimized native SVG without errors');
   assert.equal(await page.locator('#p2-realm-background').evaluate(el=>getComputedStyle(el).backgroundSize),'cover',
    'Emmaus SVG should retain its native aspect ratio instead of skewing in the surrounding field');
   await page.screenshot({path:path.join(root,'artifacts/p2-emmaus-olive',viewport.width+'-emmaus-static-engraving.png')});
   await page.close();
  }
  assert.deepEqual(errors,[],'no JavaScript errors in either browser size');
  console.log('P2 03/04 Chromium: desktop + phone; stage, books, wheel, posters, reverse scroll: pass');
 }finally{await browser.close()}
})().catch(error=>{console.error(error);process.exitCode=1});
