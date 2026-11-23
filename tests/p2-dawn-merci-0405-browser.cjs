'use strict';
/**
 * P2 04→05 MERSI / Merci transition acceptance.
 * Test the actual original scroll path, NOT layer=second (which bypasses it).
 * The authentic 04 image remains behind 05; right/bottom appears first,
 * left/top arrives second. The effect must reverse with scrolling. No fade.
 */
const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs'),path=require('node:path');
const out=path.join('artifacts','p2-dawn-merci-0405');
fs.mkdirSync(out,{recursive:true});
const ease=x=>{const n=Math.max(0,Math.min(1,x));return n*n*(3-2*n)};
(async()=>{
 const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
 const results=[];
 try{
  for(const [device,width,height] of [['desktop',1440,900],['phone',390,844]]){
   const page=await browser.newPage({viewport:{width,height},reducedMotion:'reduce'});
   const errors=[];page.on('pageerror',e=>errors.push(e.message));
   try{
    const resp=await page.goto('http://127.0.0.1:4173/experiments/p2-0105-dawn-preview.html?d=26.2&merci-0405=1',
     {waitUntil:'domcontentloaded',timeout:45000});
    assert.equal(resp?.status(),200,device+': P2 05 entrance not mounted');
    await page.waitForFunction(()=>document.querySelector('#p205-stage')?.dataset.p205Scene&&
     document.querySelector('#p205-prior')?.contentWindow,
     null,{timeout:25000});
    const snapshots=[];
    async function sample(d){
     await page.evaluate(d=>{
      const track=document.querySelector('#p205-track');
      scrollTo({top:track.offsetTop+d*innerHeight,behavior:'instant'});
     },d);
     await page.waitForTimeout(220);
     const state=await page.evaluate(()=>{
      const $=s=>document.querySelector(s);
      const stage=$('#p205-stage'),realm=$('#dawn-realm'),world=$('#dawn-world');
      const left=$('#dawn-page-left'),right=$('#dawn-page-right');
      const prior=$('#p205-prior');
      const css=getComputedStyle;
      return {
       d:Number(stage.dataset.p205MerciEntry),
       left:Number(stage.dataset.p205MerciLeft),
       right:Number(stage.dataset.p205MerciRight),
       method:stage.dataset.p205MerciMethod,
       leftClip:left.style.clipPath,rightClip:right.style.clipPath,
       leftTravel:$('#dawn-image-left').style.transform,
       rightTravel:$('#dawn-image-right').style.transform,
       wrapperBg:css(realm).backgroundColor,worldBg:css(world).backgroundColor,
       worldOpacity:css(world).opacity,
       priorPresent:!!prior.contentWindow,
       priorVisibility:css(prior).visibility,
       scene:stage.dataset.p205Scene
      };
     });
     snapshots.push({scroll:d,...state});
     return state;
    }
    const start=await sample(26.18);
    assert.equal(start.d,0,device+': 04 was already obscured before the reveal');
    const first=await sample(26.65),middle=await sample(27.16),complete=await sample(27.56);
    const expectedPhase=(27.16-26.23)/1.30;
    assert(first.right>.5&&first.left===0,
     device+': RIGHT/bottom must lead, LEFT/top must hold 04 '+JSON.stringify(first));
    assert(middle.right>.999&&middle.left>.05&&middle.left<.8,
     device+': LEFT/top must enter after right; never wipe both from same edge '+JSON.stringify(middle));
    assert(Math.abs(middle.left-ease((expectedPhase-.52)/.48))<.035,
     device+': original 03→04 MERSI scroll masks not reused '+JSON.stringify(middle));
    assert(complete.right>.999&&complete.left>.999,
     device+': 05 never becomes full-height in both halves '+JSON.stringify(complete));
    assert(first.leftClip.includes('100%')&&first.rightClip.startsWith('inset(')&&
     middle.leftClip.startsWith('inset(0 ')&&middle.rightClip==='none',
     device+': independent opposing clip geometry missing '+JSON.stringify({first,middle}));
    for(const point of [first,middle,complete]){
     assert(point.worldOpacity==='1'&&point.wrapperBg==='rgba(0, 0, 0, 0)'&&
      point.worldBg==='rgba(0, 0, 0, 0)'&&point.priorPresent,
      device+': giant paper/opacity overlay hides protected 04 '+JSON.stringify(point));
     assert.equal(point.method,'opposed-top-down-bottom-up');
    }
    // Native browser viewport samples at both opposed beats and full arrival.
    await sample(26.65);
    await page.screenshot({path:path.join(out,device+'-merci-right-rising-over-olive.png'),animations:'disabled'});
    await sample(27.16);
    await page.screenshot({path:path.join(out,device+'-merci-left-descending-over-olive.png'),animations:'disabled'});
    await sample(27.73);
    await page.screenshot({path:path.join(out,device+'-dawn-arrived.png'),animations:'disabled'});
    const reverse=await sample(26.65);
    assert(reverse.left===0&&Math.abs(reverse.right-first.right)<.002,
     device+': opposite MERSI masks do not reverse with scroll '+JSON.stringify({first,reverse}));
    assert(!errors.length,device+': JS errors '+errors.join('; '));
    results.push({device,opposed:true,reverse:true,protectedOlive:true,fullArrival:true});
   }finally{await page.close()}
  }
 }finally{await browser.close()}
 fs.writeFileSync(path.join(out,'report.json'),JSON.stringify(results,null,2));
 console.log('P2_OLIVE_DAWN_MERSI_0405_PASS',JSON.stringify(results));
})().catch(e=>{console.error(e);process.exitCode=1});
