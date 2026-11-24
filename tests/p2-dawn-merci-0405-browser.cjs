'use strict';
/**
 * P2 04→05 R96. 04 holds until both independent opposed MERSI apertures complete.
 * Test ACTUAL P2 scroll, never layer=second or a mock visual.
 */
const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs'),path=require('node:path');
const out=path.join('artifacts','p2-dawn-merci-0405');
fs.mkdirSync(out,{recursive:true});
const approx=(a,b,tol=.035)=>Math.abs(a-b)<tol;
(async()=>{
 const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
 const reports=[];
 try{
  for(const [device,width,height] of [['desktop',1440,900],['phone',390,844]]){
   const page=await browser.newPage({viewport:{width,height},reducedMotion:'reduce'});
   const errors=[];page.on('pageerror',e=>errors.push(e.message));
   try{
    const response=await page.goto('http://127.0.0.1:4173/experiments/p2-0105-dawn-preview.html?d=26.2&merci-0405=R96',
     {waitUntil:'domcontentloaded',timeout:45000});
    assert.equal(response?.status(),200,device+': native original P2 scene missing');
    await page.waitForFunction(()=>document.querySelector('#p205-stage')?.dataset.p205Scene&&
      document.querySelector('#p205-prior')?.contentWindow,null,{timeout:25000});
    async function sample(d,filename){
     await page.evaluate(d=>{
      const t=document.querySelector('#p205-track');
      scrollTo({top:t.offsetTop+d*innerHeight,behavior:'instant'});
     },d);
     await page.waitForTimeout(250);
     const s=await page.evaluate(()=>{
      const $=s=>document.querySelector(s),stage=$('#p205-stage');
      const prior=$('#p205-prior'),bridge=$('#p205-engraving-bridge'),realm=$('#dawn-realm');
      const css=getComputedStyle;
      const terrain=bridge.querySelector('.p205-engraving-bridge__terrain');
      const botany=bridge.querySelector('.p205-engraving-bridge__botanical');
      const left=$('#dawn-page-left'),right=$('#dawn-page-right');
      return {
       exit:Number(stage.dataset.p205OliveFolio),
       retired:stage.dataset.p205OliveRetired==='true',
       ink:Number(stage.dataset.p205InkTransfer),
       chapter:stage.dataset.p205EngravingRelay,
       stage:stage.dataset.p205Scene,
       m:Number(stage.dataset.p205MerciEntry),
       left:Number(stage.dataset.p205MerciLeft),
       right:Number(stage.dataset.p205MerciRight),
       method:stage.dataset.p205MerciMethod,
       priorVisibility:css(prior).visibility,
       priorOpacity:Number(css(prior).opacity),
       priorTransform:css(prior).transform,
       priorConnected:!!prior.contentWindow,
       bridgeVisible:css(bridge).visibility==='visible',
       historyReady:bridge.dataset.historyReady,
       historyOpacity:Number(css($('#p205-engraving-history')).opacity),
       historySrc:$('#p205-engraving-history').getAttribute('src'),
       historyImageReady:$('#p205-engraving-history').naturalWidth>100,
       rightHistoryReady:$('#p205-engraving-history-right').naturalWidth>100,
       rightHistorySrc:$('#p205-engraving-history-right').getAttribute('src'),
       bridgeColor:css(bridge).backgroundColor,
       terrainMask:css(terrain).webkitMaskImage||css(terrain).maskImage,
       botanicalMask:css(botany).webkitMaskImage||css(botany).maskImage,
       realmVisibility:css(realm).visibility,
       realmOpacity:css(realm).opacity,
       leftClip:left.style.clipPath,rightClip:right.style.clipPath,
       leftInkEdge:css(left).maskImage,rightInkEdge:css(right).maskImage,
       edgeMethod:stage.dataset.p205MerciEdge,
       leftImgReady:$('#dawn-image-left').naturalWidth>0,
       rightImgReady:$('#dawn-image-right').naturalWidth>0,
       scrollOverflow:Math.max(document.documentElement.scrollWidth-innerWidth,0)
      };
     });
     if(filename)await page.screenshot({path:path.join(out,device+'-'+filename+'.png'),animations:'disabled'});
     return s;
    }
    const hold=await sample(26.38,'01-olive-hold');
    const split=await sample(27.32,'02-masthead-register');
    const entering=await sample(27.77,'03-left-down');
    const meeting=await sample(28.11,'04-right-up');
    const arrived=await sample(28.40,'05-both-complete');
    assert(hold.m===0&&split.m===0,device+': Merci starts before masthead');
    for(const s of [hold,split,entering,meeting]){
     assert(s.priorVisibility==='visible'&&s.priorOpacity===1&&!s.bridgeVisible&&!s.retired,device+': whole-field replacement '+JSON.stringify(s));
    }
    assert(entering.left>.2&&entering.left<.9&&entering.right===0,device+': left must enter independently '+JSON.stringify(entering));
    assert(/^inset\(0(?:px)? 0(?:px)? [\d.]+%/.test(entering.leftClip),device+': left must reveal down '+entering.leftClip);
    assert(meeting.left>.999&&meeting.right>.3&&meeting.right<.9,device+': right must follow independently '+JSON.stringify(meeting));
    assert(/^inset\([\d.]+% 0(?:px)? 0(?:px)? 0(?:px)?\)/.test(meeting.rightClip),device+': right must reveal up '+meeting.rightClip);
    assert(arrived.retired&&arrived.left>.999&&arrived.right>.999&&arrived.priorVisibility==='hidden',device+': source retires only after both complete');
    assert([hold,split,entering,meeting,arrived].every(s=>s.priorConnected&&s.scrollOverflow<18&&s.method==='original-olive-to-opposed-merci'),device+': source/layout contract broken');
    // Scroll backwards: restore precisely the same single unbroken Olive print.
    const reverse=await sample(26.38,'07-olive-whole-recovered');
    assert(reverse.exit===0&&reverse.m===0&&reverse.priorOpacity===1&&
      reverse.priorVisibility==='visible'&&reverse.realmVisibility==='hidden',
      device+': reverse scroll cannot recover the original 04 composition '+JSON.stringify(reverse));
    assert(errors.length===0,device+': JS errors '+errors.join('; '));
    reports.push({device,unboxedFolio:true,originalSourcePreserved:true,retirementAfterBothHalves:true,
      opposingHalves:true,reverseComplete:true,images:{left:arrived.leftImgReady,right:arrived.rightImgReady}});
   }finally{await page.close()}
  }
 }finally{await browser.close()}
 fs.writeFileSync(path.join(out,'report.json'),JSON.stringify(reports,null,2));
 console.log('P2_OLIVE_DAWN_MERSI_EDITORIAL_RELAY_PASS',JSON.stringify(reports));
})().catch(e=>{console.error(e);process.exitCode=1});
