'use strict';
/**
 * P2 04→05 R87. 04 holds → complete original iframe folio retreats →
 * measured Olivet engraving register → opposed MERSI Jerusalem reveal.
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
    const response=await page.goto('http://127.0.0.1:4173/experiments/p2-0105-dawn-preview.html?d=26.2&merci-0405=R87',
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
       bridgeColor:css(bridge).backgroundColor,
       terrainMask:css(terrain).webkitMaskImage||css(terrain).maskImage,
       botanicalMask:css(botany).webkitMaskImage||css(botany).maskImage,
       realmVisibility:css(realm).visibility,
       realmOpacity:css(realm).opacity,
       leftClip:left.style.clipPath,rightClip:right.style.clipPath,
       leftImgReady:$('#dawn-image-left').naturalWidth>0,
       rightImgReady:$('#dawn-image-right').naturalWidth>0,
       scrollOverflow:Math.max(document.documentElement.scrollWidth-innerWidth,0)
      };
     });
     if(filename)await page.screenshot({path:path.join(out,device+'-'+filename+'.png'),animations:'disabled'});
     return s;
    }
    // Protect the whole released speaker art in the first beat.
    const hold=await sample(26.38,'01-olive-complete-hold');
    const retreat=await sample(26.85,'02-whole-olive-folio-retreat');
    const engrave=await sample(27.19,'03-olive-engraving-bridge');
    const entering=await sample(27.52,'04-merci-jerusalem-right-enters');
    const meeting=await sample(27.98,'05-merci-jerusalem-left-enters');
    const arrived=await sample(28.40,'06-jerusalem-whole');
    assert(hold.exit===0&&hold.m===0&&hold.priorOpacity===1&&
      hold.priorVisibility==='visible',device+': original twelve-speaker art was altered prematurely '+JSON.stringify(hold));
    assert(retreat.exit>.35&&retreat.exit<.75&&retreat.m===0&&
      retreat.priorVisibility==='visible'&&retreat.priorOpacity>.95&&
      retreat.priorTransform!=='none',
      device+': source folio is not leaving as one coherent print BEFORE Jerusalem '+JSON.stringify(retreat));
    assert(engrave.retired&&engrave.priorVisibility==='hidden'&&
      engrave.bridgeVisible&&engrave.realmVisibility==='hidden'&&engrave.m===0,
      device+': shared engraved register not isolated after complete 04 exit '+JSON.stringify(engrave));
    assert(/04-olive-mount-terrain-contours-v1\.svg/.test(engrave.terrainMask)&&
      /04-olive-field-v79-1\.svg/.test(engrave.botanicalMask),
      device+': shared engraving uses invented rather than ORIGINAL 04 assets '+JSON.stringify(engrave));
    assert(entering.retired&&entering.priorOpacity===0&&entering.left===0&&
      entering.right>.2&&entering.right<.65&&entering.m>0,
      device+': 05 MERSI enters before 04 has retired or reveals both halves at once '+JSON.stringify(entering));
    assert(meeting.right>.999&&meeting.left>.3&&meeting.left<.9&&
      meeting.leftClip.includes('inset(0')&&meeting.rightClip==='none',
      device+': independent MERSI opposition or left descending edge lost '+JSON.stringify(meeting));
    assert(arrived.left>.999&&arrived.right>.999&&arrived.priorVisibility==='hidden',
      device+': Jerusalem did not assume the entire stage '+JSON.stringify(arrived));
    assert([hold,retreat,engrave,entering,meeting,arrived].every(s=>
      s.method==='source-retreat-register-then-opposed-reveal'&&
      s.priorConnected&&s.scrollOverflow<18),
      device+': broken source control, motion identity or horizontal layout');
    // Scroll backwards: restore precisely the same single unbroken Olive print.
    const reverse=await sample(26.38,'07-olive-whole-recovered');
    assert(reverse.exit===0&&reverse.m===0&&reverse.priorOpacity===1&&
      reverse.priorVisibility==='visible'&&reverse.realmVisibility==='hidden',
      device+': reverse scroll cannot recover the original 04 composition '+JSON.stringify(reverse));
    assert(errors.length===0,device+': JS errors '+errors.join('; '));
    reports.push({device,wholeFolioRetreat:true,originalEngraving:true,merciAfterRetirement:true,
      opposingHalves:true,reverseComplete:true,images:{left:arrived.leftImgReady,right:arrived.rightImgReady}});
   }finally{await page.close()}
  }
 }finally{await browser.close()}
 fs.writeFileSync(path.join(out,'report.json'),JSON.stringify(reports,null,2));
 console.log('P2_OLIVE_DAWN_MERSI_EDITORIAL_RELAY_PASS',JSON.stringify(reports));
})().catch(e=>{console.error(e);process.exitCode=1});
