/* P2 04 isolated visual gate — DO NOT TOUCH THE PUBLISHED 01–03.
 * Manually scroll the real embedded 03 compositor and verify 04 enters
 * right-to-left in the precise same page rectangle. Phone + desktop.
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
assert.match(script,/const progress=smooth\(\(d-9\.44\)\/1\.38\)/,'04 enters after the frozen 03 at 9.44');
assert.match(script,/inset\(0 0 0 /,'04 must reveal from the RIGHT edge');
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
   const errors=[];page.on('pageerror',e=>errors.push(String(e)));
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
   assert(middle.reveal>.49&&middle.reveal<.51,'04 half reveal must track hand 1:1');
   // Chromium normalizes CSS 50.000% into 50%, so test the actual
   // percentage and direction rather than one serialization string.
   const mask=middle.clip.match(/^inset\(\s*0(?:px)?\s+0(?:px)?\s+0(?:px)?\s+([\\d.]+)%\s*\)$/);
   assert(mask&&Math.abs(Number(mask[1])-50)<.15,
    '50% must reveal FROM RIGHT across the same fixed book rectangle: '+middle.clip);
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
   assert(Math.abs(complete.folio.w-original.source.w)<3,'folio size must not jump at arrival');
   assert(complete.exterior>.999,'Olive engraved exterior replaces green while preserving inner folio');
   await page.screenshot({path:path.join(out,width+'-04-upper-lower-complete.png')});
   await page.locator('#olive-speaker-names button[data-speaker="derek-prince"]').click();
   assert.equal(await page.locator('#olive-main-image').getAttribute('alt'),'葉光明');
   await page.screenshot({path:path.join(out,width+'-04-speaker-selected.png')});
   const reverse=await go(10.13);
   assert(Math.abs(reverse.reveal-middle.reveal)<.002,'reverse must restore identical reveal mask');
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
