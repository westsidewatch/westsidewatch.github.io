'use strict';
/* P2 04 manuscript gallery — physical-frame 03→04, no 01–03 changes.
 * Browser checks actual geometry/mask states at every designed beat.
 * Never mistake an engineering PASS for final visual art direction.
 */
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const {chromium}=require('playwright');
const root=path.resolve(__dirname,'..');
const read=p=>fs.readFileSync(path.join(root,p),'utf8');
const html=read('static/experiments/p2-0104-olive-continuation.html');
const js=read('static/js/p2-0104-olive-continuation.js');
const css=read('static/css/p2-0104-olive-continuation.css');
assert.match(html,/p2-0103-release\.html\?embed=1/,'use real approved 01–03 stage');
assert.match(html,/id="olive-first"/,'first speaker must originate in the actual Doré frame');
assert.match(html,/id="olive-pair-next-left"/,'opposed double-spread image masks');
assert.match(html,/id="olive-overview"/,'all twelve original posters must converge in one finished layout');
assert.match(js,/first:10\.08,spread:10\.95/,'separate artwork handoff and two-poster formation');
assert.match(js,/groundStart:11\.15,groundEnd:11\.73/,'background MUST wait until after settled two-poster spread');
assert.match(js,/pairStart:11\.95,pairStep:\.83,pairDuration:\.62/,'six coherent original double-spread gallery stages');
assert.match(js,/indexStart:16\.25,indexEnd:17\.25/,'twelve real posters recompose after all six pairs');
assert.match(js,/getBoundingClientRect\(\)/,'original Doré source coordinates measured live');
assert.match(js,/style\.clipPath=/,'physical cutout/masks under one scroll owner');
assert.match(js,/ground\.style\.opacity='1'/,'background is NOT faded over the entering speakers');
assert.doesNotMatch(js,/setInterval|setTimeout|new Promise|animate\(|transitionDelay/,
 'no secondary timeline or time-based lag in P2 scroll choreography');
assert.doesNotMatch(html,/olive-main-image|olive-next-image|olive-speaker-names/,
 'remove prior speaker-player layout and small-thumb corridor');
assert.match(css,/04-olive-engraving-v1-5\.svg/,'reuse approved original Olive line engraving SVG');
assert(fs.existsSync(path.join(root,'static/images/p2-realms/v15/04-olive-engraving-v1-5.svg')),
 'do not reproduce approved SVG line art');
const out=path.join(root,'artifacts/p2-0104-olive');fs.mkdirSync(out,{recursive:true});
(async()=>{
 const browser=await chromium.launch({headless:true});
 try{
  for(const [width,height] of [[1648,928],[390,844]]){
   const page=await browser.newPage({viewport:{width,height},reducedMotion:'no-preference'});
   const errors=[];page.on('pageerror',e=>errors.push(e.stack||String(e)));
   await page.goto('http://127.0.0.1:4173/experiments/p2-0104-olive-continuation.html?d=9.30',
    {waitUntil:'domcontentloaded',timeout:45000});
   await page.waitForFunction(()=>{
    const st=document.getElementById('p2-olive-stage');
    const d=document.getElementById('p2-0103-original')?.contentDocument;
    const source=d?.getElementById('proof-original')?.contentDocument;
    return st?.dataset.p2FolioReady==='true'&&source
      ?.querySelector('.p2-magazine iframe:not(.p2-magazine__home-film)')?.contentDocument
      ?.getElementById('dual-cover');
   },null,{timeout:35000});
   const state=()=>page.evaluate(()=>{
    const st=document.getElementById('p2-olive-stage');
    const shell=document.getElementById('olive-proof');
    const image=document.getElementById('olive-first');
    const source=document.getElementById('p2-0103-original').contentDocument;
    const origRight=source.querySelector('#emmaus .emmaus__right').getBoundingClientRect();
    const left=document.getElementById('olive-pair-left');
    const right=document.getElementById('olive-pair-right');
    const nl=document.getElementById('olive-pair-next-left');
    const nr=document.getElementById('olive-pair-next-right');
    const ground=document.getElementById('p2-olive-surround');
    const overview=document.getElementById('olive-overview');
    const box=el=>{const b=el.getBoundingClientRect();return {x:b.x,y:b.y,w:b.width,h:b.height}};
    const get=el=>({visibility:getComputedStyle(el).visibility,
      src:el.querySelector('img')?.getAttribute('src')||'',
      clip:el.style.clipPath,box:box(el)});
    return {distance:+st.dataset.p2Distance,
      scene:st.dataset.p2Scene,frameReady:st.dataset.p2FolioReady,
      underlying:source.body.dataset.proofScene,
      first:+st.dataset.p2Bridge,spread:+st.dataset.p2Spread,
      ground:+st.dataset.p2Ground,index:+st.dataset.p2Index,
      pairIndex:st.dataset.p2PairIndex||'0',pairBlend:st.dataset.p2PairBlend||'0',
      pairOrientation:st.dataset.p2PairOrientation,
      main:box(shell),source:{...box(source.querySelector('#emmaus .emmaus__right')),folio:box(source.querySelector('#emmaus'))},
      firstFrame:get(image),pairLeft:get(left),pairRight:get(right),
      incomingLeft:get(nl),incomingRight:get(nr),
      groundCSS:{visibility:getComputedStyle(ground).visibility,
       opacity:getComputedStyle(ground).opacity,clip:ground.style.clipPath,
       parts:ground.querySelectorAll('.olive-surround__plane').length},
      cards:[...overview.querySelectorAll('.olive-stage__index-card')].map(el=>
       ({src:el.querySelector('img')?.getAttribute('src'),...box(el)})),
      grid:overview.dataset.columns,
      overviewVisibility:getComputedStyle(overview).visibility,
      ctaVisibility:getComputedStyle(document.getElementById('olive-enter')).visibility
    };
   });
   const go=async(d,label)=>{
    await page.evaluate(v=>{
     const t=document.getElementById('p2-olive-track');
     window.scrollTo({top:t.getBoundingClientRect().top+scrollY+innerHeight*v,behavior:'instant'});
    },d);
    await page.waitForFunction(v=>Math.abs(
     Number(document.getElementById('p2-olive-stage')?.dataset.p2Distance)-v)<.035,
     d,{timeout:18000});
    await page.waitForTimeout(140);
    const result=await state();
    if(label)await page.screenshot({path:path.join(out,width+'-'+label+'.png'),animations:'allow'});
    assert.equal(result.underlying,'03','approved 01–03 must stay on its original 03');
    return result;
   };
   const at03=await go(9.30,'00-original-emmaus');
   assert.equal(at03.scene,'03-held');
   assert.equal(at03.firstFrame.visibility,'hidden','04 must not enter before the 03 hold');
   assert.equal(at03.groundCSS.visibility,'hidden','Olive exterior must wait until the posters settle');
   const bridge=await go(9.76,'01-dore-frame-first-poster-half');
   assert(bridge.first>.45&&bridge.first<.55,'same-frame handoff should be at midpoint');
   assert.equal(bridge.scene,'04-dore-handoff');
   assert(Math.abs(bridge.firstFrame.box.x-bridge.source.x)<2 &&
     Math.abs(bridge.firstFrame.box.w-bridge.source.w)<2,
     'first original speaker poster must physically occupy the original Doré image frame');
   assert(bridge.firstFrame.src.includes('watchman-nee-editorial.png'),'use approved original first speaker');
   assert.equal(bridge.groundCSS.visibility,'hidden','background must NOT enter with first speaker');
   const forming=await go(10.38,'02-first-to-left-second-to-right');
   assert.equal(forming.scene,'04-two-poster-formation');
   assert(forming.spread>.25&&forming.spread<.45,'first speaker must visibly travel toward left folio');
   assert(forming.firstFrame.box.x<bridge.firstFrame.box.x,
    'first speaker moves from right Doré frame to the left half');
   assert.equal(forming.groundCSS.visibility,'hidden','background stays untouched during pair formation');
   const pair=await go(10.98,'03-two-poster-locked-original-background');
   assert.equal(pair.scene,'04-pair-hold');
   assert.equal(pair.pairLeft.visibility,'visible');
   assert.equal(pair.pairRight.visibility,'visible');
   assert.equal(pair.pairLeft.src,'/images/olive/watchman-nee-editorial.png');
   assert.equal(pair.pairRight.src,'/images/olive/derek-prince-editorial.png');
   if(width>800){
    assert.equal(pair.pairOrientation,'side-by-side');
    assert(Math.abs(pair.pairLeft.box.w-pair.main.w/2)<3,
     'desktop must maintain two original art works in equal LEFT/RIGHT folios');
   }else{
    assert.equal(pair.pairOrientation,'stacked');
    assert(Math.abs(pair.pairLeft.box.h-pair.main.h/2)<3,
     'phone must use equal TOP/BOTTOM folios, not tiny thin portrait columns');
    assert(Math.abs(pair.pairLeft.box.w-pair.main.w)<3,
     'phone art must have the full page width');
    assert(Math.abs(pair.pairRight.box.y-(pair.pairLeft.box.y+pair.pairLeft.box.h))<3,
     'phone second speaker poster must start below first without overlap');
   }
   assert.equal(pair.groundCSS.visibility,'hidden',
    'the existing Emmaus background must remain during the settled two-poster hold');
   const material=await go(11.44,'04-only-now-olive-svg-background');
   assert.equal(material.scene,'04-ground-reveal');
   assert(material.ground>.45&&material.ground<.60,'engraved exterior changes on its own later beat');
   assert.equal(material.groundCSS.parts,4,'use four original-geometry surround planes, not one overlaid bitmap');
   assert.equal(material.groundCSS.opacity,'1','background transition must not use opacity fading');
   assert(material.groundCSS.clip.startsWith('inset('),'background material must enter by spatial clipping');
   assert.equal(material.pairLeft.src,pair.pairLeft.src);
   assert.equal(material.pairRight.src,pair.pairRight.src);
   for(const key of ['x','y','w','h'])assert(Math.abs(material.pairLeft.box[key]-pair.pairLeft.box[key])<1,
    'speakers must be FIXED as background changes: '+key);
   const backgroundReady=await go(11.75,'05-olive-material-fixed');
   assert(backgroundReady.ground>.999&&backgroundReady.groundCSS.clip==='none',
    'background replacement completes before any pair cycling');
   const pairTransition=await go(12.25,'06-opposed-double-poster-change');
   assert.equal(pairTransition.scene,'04-six-pair-gallery');
   assert(+pairTransition.pairBlend>.4&&+pairTransition.pairBlend<.7,'new pair is physically half revealed');
   assert(pairTransition.incomingLeft.clip.includes('inset(')&&
     pairTransition.incomingRight.clip.includes('inset('),'both half-spreads have spatial opposing masks');
   if(width<=800){
    assert(/^inset\(0(?:px)? 0(?:px)? [0-9.]+%/.test(pairTransition.incomingLeft.clip),
     'phone upper poster switches from TOP DOWN');
    assert(/^inset\([0-9.]+% 0(?:px)? 0(?:px)?/.test(pairTransition.incomingRight.clip),
     'phone lower poster switches from BOTTOM UP');
   }
   assert(pairTransition.incomingLeft.src.includes('david-pawson-editorial.png'));
   assert(pairTransition.incomingRight.src.includes('stephen-tong-editorial.png'));
   for(const key of ['x','y','w','h'])assert(Math.abs(pairTransition.pairLeft.box[key]-pair.pairLeft.box[key])<1,
    'all six pairs keep exactly the same folio/anchor geometry');
   const last=await go(16.11,'07-final-pair-eleven-twelve');
   assert(last.pairLeft.src.includes('yu-hong-jie-editorial.png'));
   assert(last.pairRight.src.includes('kou-shao-en-editorial.png'));
   const indexHalf=await go(16.70,'08-twelve-works-recomposing');
   assert.equal(indexHalf.scene,'04-twelve-recomposition');
   assert(indexHalf.index>.35&&indexHalf.index<.55,'twelve images must visibly recompose');
   assert.equal(indexHalf.cards.length,12,'must be original TWELVE works, not gallery thumb proxies');
   assert(indexHalf.cards[0].w<indexHalf.main.w*(width>800?.5:.82),
    'twelve cards must interpolate from their approved desktop HALF or mobile FULL-WIDTH stacked source to grid destinations');
   const indexFull=await go(17.33,'09-twelve-voices-final-overview');
   assert.equal(indexFull.scene,'04-twelve-index');
   assert.equal(indexFull.cards.length,12);
   assert.equal(indexFull.grid,width>=800?'6':'3','6x2 desktop or 3x4 phone exhibition index');
   assert.equal(indexFull.ctaVisibility,'visible');
   const seen=new Set(indexFull.cards.map(x=>x.src));
   assert.equal(seen.size,12,'all original 12 unique approved speaker images must be present');
   for(const [i,c] of indexFull.cards.entries()){
    assert(c.src==='/images/olive/'+[
     'watchman-nee','derek-prince','david-pawson','stephen-tong',
     'huang-shuhua','kang-lai-chang','jerry-lai','tong-liu',
     'jiang-xiuqin','rick-warren','yu-hong-jie','kou-shao-en'][i]+'-editorial.png',
     'order must remain original approval order');
    assert(c.w>25&&c.h>25,'twelve original posters still visible, no zero-size index cards');
   }
   const backMid=await go(11.44,'10-reverse-return-to-ground-mid');
   assert(Math.abs(backMid.ground-material.ground)<.005,
    'reversing returns exact exterior mask position, no delayed animation');
   const backBeginning=await go(9.76,'11-reverse-restore-dore-frame');
   assert(Math.abs(backBeginning.first-bridge.first)<.005,
    'reverse restores exact first poster clip and Doré frame geometry');
   const restored=await go(9.30,'12-reverse-restored-emmaus');
   assert.equal(restored.firstFrame.visibility,'hidden');
   assert.equal(restored.groundCSS.visibility,'hidden');
   assert.equal(errors.length,0,'JavaScript browser errors: '+errors.join(' | '));
   console.log('P2 04 TWELVE VOICES PASS',width,
    JSON.stringify({stage:indexFull.scene,groundAfterHold:material.ground,
      finalColumns:indexFull.grid,photos:indexFull.cards.length,
      reversed:restored.scene}));
   await page.close();
  }
 }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
