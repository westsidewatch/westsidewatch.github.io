/* P2 04 isolated visual gate — DO NOT TOUCH THE PUBLISHED 01–03.
 * Manually scroll the real embedded 03 compositor and verify 04 enters
 * two-part upper/lower entrance + poster corridor in the SAME frame. Phone + desktop.
 */
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const {chromium}=require('playwright');
const root=path.resolve(__dirname,'..');
const html=fs.readFileSync(path.join(root,'static/experiments/p2-0104-olive-continuation.html'),'utf8');
const script=fs.readFileSync(path.join(root,'static/js/p2-0104-olive-continuation.js'),'utf8');
const css=fs.readFileSync(path.join(root,'static/css/p2-0104-olive-continuation.css'),'utf8');
assert.match(html,/p2-0103-release\.html\?embed=1/,'01–03 must be the unmodified published compositor');
assert.match(html,/olive-main-image/,'04 must reuse a real published Olive portrait');
assert.match(html,/olive-speaker-baseline/,'04 speaker cover uses the protected original label component');
assert.match(script,/const progress=clamp\(\(d-9\.44\)\/1\.38\)/,'04 enters after the frozen 03 at 9.44');
assert.match(script,/const upperOpen=smooth\(progress\/\.68\)/,
 '04 upper portrait must open downward, not with a generic single folio wipe');
assert.match(script,/const corridorOpen=smooth\(\(progress-\.35\)\/\.65\)/,
 '04 lower corridor must open horizontally after the portrait');
assert.match(script,/names\.scrollLeft=/,
 '04 horizontal twelve-speaker corridor must actually scroll through original posters');
assert.match(script,/upper\.style\.clipPath=/,'04 upper portrait has an independent vertical reveal');
assert.match(script,/lower\.style\.clipPath=/,'04 lower speaker corridor has an independent horizontal reveal');
assert.doesNotMatch(script,/olive\.style\.clipPath=progress\s*>/,
 'the rejected single right-to-left full-04-page wipe must be gone');
assert.match(css,/\.olive-proof__names\{[\s\S]*?display:flex!important/,
 '04 lower region must contain a real horizontal poster gallery');
assert.match(script,/measureFolio\(/,'04 dimensions must come from actual published Emmaus folios');
assert.doesNotMatch(script,/appendChild\(emRight\)|sourceCover\.style\.transform|sourceTile\.style\.width/,'04 must not reshape the approved 03');
assert.match(css,/grid-template-rows:65% 35%/,'Olive keeps original upper/lower editorial layout');
assert.match(css,/04-olive-engraving-v1-5\.svg/,'Olive keeps the original vector master');
assert(fs.existsSync(path.join(root,'static/images/p2-realms/v15/04-olive-engraving-v1-5.svg')),
 'Original 04 V1.5 vector cannot be lost or re-created as gradients');
const out=path.join(root,'artifacts/p2-0104-olive');fs.mkdirSync(out,{recursive:true});
(async()=>{
 const browser=await chromium.launch({headless:true});
 try{
  for(const [width,height] of [[1648,928],[390,844]]){
   const page=await browser.newPage({viewport:{width,height},reducedMotion:'no-preference'});
   const errors=[];page.on('pageerror',e=>{const detail=e.stack||String(e);errors.push(detail);console.error('P2 04 BROWSER PAGEERROR',detail)});
   await page.goto('http://127.0.0.1:4173/experiments/p2-0104-olive-continuation.html?d=9.30',
    {waitUntil:'domcontentloaded',timeout:45000});
   await page.waitForFunction(()=>{
    const stage=document.getElementById('p2-olive-stage');
    const doc=document.getElementById('p2-0103-original')?.contentDocument;
    return stage?.dataset.p2FolioReady==='true'&&
     doc?.getElementById('emmaus')&&doc?.getElementById('proof-original')?.contentDocument
      ?.querySelector('.p2-magazine iframe:not(.p2-magazine__home-film)')?.contentDocument
      ?.getElementById('dual-cover');
   },null,{timeout:35000});
   const go=async d=>{
    await page.evaluate(distance=>{
     const track=document.getElementById('p2-olive-track');
     window.scrollTo({top:track.getBoundingClientRect().top+scrollY+distance*innerHeight,behavior:'instant'});
    },d);
    await page.waitForFunction(distance=>{
     const s=document.getElementById('p2-olive-stage');
     return Math.abs(Number(s?.dataset.p2Distance)-distance)<.035;
    },d,{timeout:15000});
    await page.waitForTimeout(180);
    return page.evaluate(()=>{
     const p=document.getElementById('p2-0103-original');
     const d=p.contentDocument;
     const o=document.getElementById('olive-proof');
     const a=d.querySelector('#emmaus .emmaus__left').getBoundingClientRect();
     const b=d.querySelector('#emmaus .emmaus__right').getBoundingClientRect();
     const c=o.getBoundingClientRect();
     return {scene:d.body.dataset.proofScene,clip:o.style.clipPath,
       reveal:Number(o.dataset.reveal||0),
       upper:Number(o.dataset.upperOpen||0),
       corridor:Number(o.dataset.corridorOpen||0),
       upperClip:o.querySelector('.olive-proof__top')?.style.clipPath,
       lowerClip:o.querySelector('.olive-proof__bottom')?.style.clipPath,
       galleryScroll:o.querySelector('#olive-speaker-names')?.scrollLeft||0,
       posterImages:[...o.querySelectorAll('#olive-speaker-names button img')].map(img=>img.getAttribute('src')),
       visibility:getComputedStyle(o).visibility,
       aria:o.getAttribute('aria-hidden'),portrait:o.querySelector('#olive-main-image')?.getAttribute('src'),
       speakerCount:o.querySelectorAll('#olive-speaker-names button').length,
       folio:{x:c.x,y:c.y,w:c.width,h:c.height},
       source:{x:Math.min(a.x,b.x),y:Math.min(a.y,b.y),
        w:Math.max(a.right,b.right)-Math.min(a.x,b.x),
        h:Math.max(a.bottom,b.bottom)-Math.min(a.y,b.y)},
       exterior:Number(getComputedStyle(document.getElementById('p2-olive-surround')).opacity),
       registered:document.getElementById('p2-olive-stage').dataset.p2FolioReady};
    });
   };
   const original=await go(9.30);
   assert.equal(original.scene,'03','entry must begin with already-published real Emmaus');
   assert.equal(original.visibility,'hidden','04 must not cover approved Emmaus at 9.30');
   await page.screenshot({path:path.join(out,width+'-03-emmaus-held.png')});
   const start=await go(9.44);
   assert(start.reveal<.001&&start.visibility==='hidden','04 must not flash before reveal starts');
   const middle=await go(10.13);
   assert(middle.reveal>.49&&middle.reveal<.51,'04 entrance must track hand 1:1');
   assert(middle.upper>.80&&middle.upper<.84,
    'at halfway the upper portrait/editorial must already be entering DOWNWARD');
   assert(middle.corridor>.12&&middle.corridor<.15,
    'lower horizontal speaker gallery must reveal AFTER the upper page starts');
   // CSSOM removes redundant zero insets: for instance the correct
   // top-down path serializes as inset(0px 0px 17.263%).
   const upperPart=middle.upperClip.match(/^inset\(0(?:px)? 0(?:px)? ([0-9.]+)%(?: 0(?:px)?)?\)$/);
   const lowerPart=middle.lowerClip.match(/^inset\(0(?:px)? 0(?:px)? 0(?:px)? ([0-9.]+)%\)$/);
   assert(upperPart&&+upperPart[1]>15&&+upperPart[1]<20,
    'upper must be a TOP-DOWN reveal, not sideways: '+middle.upperClip);
   assert(lowerPart&&+lowerPart[1]>84&&+lowerPart[1]<88,
    'lower must be a RIGHT→LEFT corridor: '+middle.lowerClip);
   assert.equal(middle.clip,'none','the rejected whole-page right-to-left wipe must not return');
   assert(middle.galleryScroll>(width>800?50:8),
    'horizontal speaker gallery must MOVE substantially (no scroll-snap regression): '+middle.galleryScroll);
   assert.equal(middle.visibility,'visible');
   assert.equal(middle.scene,'03','underlying 03 remains stable until fully covered');
   for(const k of ['x','y','w','h']){
    assert(Math.abs(middle.folio[k]-middle.source[k])<3,
     '04 must reuse exact 03 folio '+k+' without moving/rerendering it '+JSON.stringify(middle));
   }
   assert(middle.exterior>.49&&middle.exterior<.51,'olive engraving exterior follows exactly the same mask progress');
   await page.screenshot({path:path.join(out,width+'-04-half-right-to-left.png')});
   const complete=await go(10.86);
   assert(complete.reveal>.999&&complete.aria==='false','Olive is fully revealed and interactive');
   assert.equal(complete.speakerCount,12,'original 12 published speakers must appear');
   assert.equal(complete.posterImages.length,12,'the actual 12 original speaker POSTERS must form the corridor');
   for(const src of complete.posterImages)assert(/^\/images\/olive\/[a-z-]+-editorial\.png$/.test(src),
    'all corridor artwork must reuse original approved speaker posters: '+src);
   assert(complete.upper>.999&&complete.corridor>.999,
    'both independent upper and lower editorial bands must fully settle');
   assert.equal(complete.upperClip,'none','upper part must stop clipping once complete');
   assert.equal(complete.lowerClip,'none','speaker gallery must remain fully visible after entry');
   assert(Math.abs(complete.folio.w-original.source.w)<3,'folio size must not jump at arrival');
   assert(complete.exterior>.999,'Olive engraved exterior replaces green while preserving inner folio');
   await page.screenshot({path:path.join(out,width+'-04-upper-lower-complete.png')});
   await page.locator('#olive-speaker-names button[data-speaker="derek-prince"]').click();
   assert.equal(await page.locator('#olive-main-image').getAttribute('alt'),'葉光明');
   await page.screenshot({path:path.join(out,width+'-04-speaker-selected.png')});
   // The completed horizontal corridor remains native, user-scrollable,
   // without the P2 scroll controller snapping its x-position back.
   const manuallyScrolled=await page.evaluate(()=>{
    const strip=document.getElementById('olive-speaker-names');
    strip.scrollLeft=Math.min(strip.scrollWidth-strip.clientWidth,strip.scrollLeft+100);
    return strip.scrollLeft;
   });
   await page.waitForTimeout(250);
   const still=await page.evaluate(()=>document.getElementById('olive-speaker-names').scrollLeft);
   assert(Math.abs(still-manuallyScrolled)<2,'user-controlled horizontal corridor must not reset on idle');
   const reverse=await go(10.13);
   assert(Math.abs(reverse.reveal-middle.reveal)<.002,'reverse must restore progress');
   assert(Math.abs(reverse.upper-middle.upper)<.002&&Math.abs(reverse.corridor-middle.corridor)<.002,
    'reverse must restore both TOP-DOWN portrait and horizontal speaker corridor');
   await page.screenshot({path:path.join(out,width+'-04-half-reversed.png')});
   const restored=await go(9.30);
   assert.equal(restored.visibility,'hidden','reverse must restore the existing Emmaus reader without a replacement screen');
   assert.equal(restored.scene,'03','real 01–03 compositor remains loaded and functional');
   assert.equal(errors.length,0,'no JavaScript runtime error: '+errors.join(' | '));
   console.log('P2 04 FOLIO OK',width,JSON.stringify({middle,complete,restored:restored.scene}));
   await page.close();
  }
 }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
