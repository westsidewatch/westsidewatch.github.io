/* P2 RELEASE GATE — 01 Church → 02 Magazine → 03 Emmaus.
 * Publishing MUST NOT import 04 Olive Mountain or 05–07.
 * Real Chromium verifies the book choreography, not only regexes.
 */
const fs=require('node:fs');
const assert=require('node:assert/strict');
const {chromium}=require('playwright');
const html=fs.readFileSync('static/experiments/p2-0103-release.html','utf8');
const js=fs.readFileSync('static/js/p2-0103-release.js','utf8');
const css=fs.readFileSync('static/css/p2-0103-release.css','utf8');
const vol=fs.readFileSync('static/experiments/p2-double-square-video-lab.html','utf8');
const bridge=fs.readFileSync('static/js/p2-magazine-live-bridge.js','utf8');
const poster=fs.readFileSync('static/js/p2-vol00-poster.js','utf8');
assert(!/id="olive-proof"|p2-five-v15|olive-speaker-baseline|data-jump="1[01]\./.test(html),'04–07 are excluded from the release HTML');
assert(!/\bconst olive\b|\boliveIn\b|\boliveShowing\b|galleryBorrowed|archiveForOlive/.test(js),'04–07 animation is excluded from release runtime');
assert(!/\.olive-proof|data-realm="sermon"|data-realm="cinema"|data-realm="book"/.test(css),'release CSS excludes future realm content');
assert.match(js,/const timelineMax=9\.34/,'release ends before Olive starts at 9.44');
assert.match(html,/p2-0103-release\.css/);
assert.match(html,/p2-0103-release\.js/);
assert.match(vol,/coverIn=stableLargeA\?ease\(\(progress-\.04\)\/\.20\)/,'whole cover enters first');
assert.match(vol,/posterIn=stableLargeA\?ease\(\(progress-\.28\)\/\.07\)/,'whole large poster follows');
assert.match(poster,/const u=clamp\(\(p-\.36\)\/\.41\)\*6/,'seven inks only begin after folios are visible');
assert.match(bridge,/magazine\.style\.background='transparent'/,'no early blank paper curtain');
assert.match(bridge,/filmReveal=easing\(\(progress-\.97\)\/\.03\)/,'home video only revealed at final spread retreat');
assert.match(html,/p2-emmaus-theme-verse\.css/,'ONE green cover scripture has separate scoped OS rule');
assert(!/\.olive-proof/.test(css),'no Olive Mountain CSS');
const out='artifacts/p2-0103-release';fs.mkdirSync(out,{recursive:true});
const u='http://127.0.0.1:4173/experiments/p2-0103-release.html';
const browserPromise=chromium.launch({headless:true});
(async()=>{
 const browser=await browserPromise;
 try{
  for(const [width,height] of [[1648,928],[390,844]]){
   const page=await browser.newPage({viewport:{width,height},reducedMotion:'no-preference'});
   const errors=[];
   page.on('pageerror',error=>errors.push(String(error)));
   try{
    await page.goto(u+'?d=0.12',{waitUntil:'domcontentloaded',timeout:45000});
    await page.waitForFunction(()=>document.querySelector('#proof-original')?.contentDocument
      ?.querySelector('.p2-magazine iframe:not(.p2-magazine__home-film)')?.contentDocument
      ?.getElementById('dual-stage'),{timeout:25000});
    const pose=async d=>{
      await page.evaluate(distance=>{
       const track=document.querySelector('#proof-track');
       scrollTo({top:track.getBoundingClientRect().top+scrollY+distance*innerHeight,behavior:'instant'});
      },d);
      await page.waitForTimeout(190);
      return page.evaluate(()=>{
       const root=document.getElementById('proof-original')?.contentDocument;
       const mag=root?.querySelector('.p2-magazine');
       const f=mag?.querySelector('iframe:not(.p2-magazine__home-film)');
       const doc=f?.contentDocument,stage=doc?.getElementById('dual-stage');
       const cover=doc?.getElementById('dual-cover'),poster=doc?.getElementById('dual-contents');
       const clip=mag?.querySelector('.p2-magazine__home-film');
       const inScene=document.getElementById('emmaus');
       const b=e=>e?.getBoundingClientRect();
       return {scene:document.body.dataset.proofScene,phase:stage?.dataset.phase,
        coverVisible:!!cover&&getComputedStyle(cover).visibility==='visible',
        posterVisible:!!poster&&getComputedStyle(poster).visibility==='visible',
        coverX:b(cover)?.x,coverW:b(cover)?.width,coverH:b(cover)?.height,
        posterX:b(poster)?.x,posterW:b(poster)?.width,posterH:b(poster)?.height,
        coverIn:+stage?.dataset.releaseCoverIn||0,
        posterIn:+stage?.dataset.releasePosterIn||0,
        spreadScale:+stage?.dataset.posterSpreadScale||1,
        filmOpacity:clip?+getComputedStyle(clip).opacity:-1,
        sheetContents:doc?.getElementById('dual-stone-contents')?.inert,
        oneVisible:!!inScene&&getComputedStyle(inScene).visibility==='visible',
        trackHeight:document.querySelector('#proof-track')?.getBoundingClientRect().height,
        olivePresent:!!document.getElementById('olive-proof'),
        banner:document.getElementById('proof-phase')?.textContent};
      });
    };
    const church=await pose(1.6);
    assert.equal(church.olivePresent,false);
    assert(!church.coverVisible&&!church.posterVisible,'nothing from Magazine may cover church in phase 01');
    const cover=await pose(3.63);
    console.log('RELEASE COVER-FIRST',width,JSON.stringify(cover));
    assert(cover.coverIn>.001&&cover.posterIn===0,'full cover must enter BEFORE entire 西望 poster');
    assert(!cover.posterVisible,'blank left folio must NOT be visible during cover entrance');
    assert.equal(cover.filmOpacity,0,'film must remain behind cover');
    const print=await pose(4.65);
    console.log('RELEASE GIANT PRINT',width,JSON.stringify(print));
    assert(print.posterVisible&&print.coverVisible,'full pair must be present for seven-color print');
    assert(Math.abs(print.posterW-print.posterH)<3,'giant 西望 stays 1:1');
    assert.equal(print.filmOpacity,0,'no film while ink colors still run');
    const gold=await pose(5.99);
    console.log('RELEASE BLUE-GOLD',width,JSON.stringify(gold));
    assert(gold.coverVisible&&gold.posterVisible,'gold print has intact complete folios');
    assert(Math.abs(gold.spreadScale-1)<.002,'do not shrink before the Contents entry');
    const contents=await pose(6.34); // p≈.953: fully settled Contents BEFORE spread retreat
    console.log('RELEASE CONTENTS',width,JSON.stringify(contents));
    assert(Math.abs(contents.spreadScale-1)<.002,'Contents must settle before combined spread retreat');
    assert.equal(contents.filmOpacity,0,'film must not be visible until spread shrink');
    const retreat=await pose(6.48); // p≈.994: entire spread already retreats
    assert(retreat.spreadScale<.999,'final filmed background reveals only as the complete spread retreats');
    assert(retreat.filmOpacity>.05,'the existing homepage film appears AFTER Contents has entered');
    const reading=await pose(9.30);
    assert.equal(reading.scene,'03','terminal release page must remain 03 Emmaus');
    assert(reading.oneVisible,'real ONE Bible reader remains visible at release end');
    assert(!reading.olivePresent,'Olive Mountain must never mount');
    assert.equal(await page.evaluate(()=>window.ONE_DATA?.books?.length),66,'all 66 canonical ONE books are available');
    const over=await pose(9.90);
    assert.equal(over.scene,'03','scrolling past 03 must clamp at the release ceiling');
    assert(!over.olivePresent);
    await page.screenshot({path:out+'/end-03-'+width+'.png'});
    await pose(4.65);
    await page.screenshot({path:out+'/giant-seven-color-'+width+'.png'});
    await pose(3.63);
    await page.screenshot({path:out+'/cover-first-'+width+'.png'});
    // Parent frame should never insert a blank opaque paper over the church.
    const rewind=await pose(1.6);
    assert(!rewind.coverVisible&&!rewind.posterVisible,'reverse scroll must restore Church only');
    assert(!errors.some(x=>/ReferenceError|TypeError|SyntaxError/.test(x)),
      'JavaScript errors during release choreography: '+errors.join('; '));
    console.log('P2 RELEASE VERIFIED',width,{church,cover,print,gold,contents,reading,over,rewind});
   }finally{await page.close()}
  }
  console.log('01–03-only P2 release gate PASS. 04–07 excluded.');
 }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
