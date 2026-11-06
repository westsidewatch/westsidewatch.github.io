'use strict';
/* Same-viewport, same-scroll-keyframe BEFORE/AFTER art proof.
 * Immutable Cloudflare deployment URLs are recorded in the editorial
 * comparison page.  This verifies BOTH historical screenshots can render
 * and captures actual browser pairs; not a path-count or CI-as-art claim. */
const fs=require('node:fs');
const path=require('node:path');
const assert=require('node:assert/strict');
const {chromium}=require('playwright');
const root=path.resolve(__dirname,'..');
const html=fs.readFileSync(path.join(root,
 'static/experiments/olive-engraving-v1-v2-compare.html'),'utf8');
assert.match(html,/5aa9c100\.westsidewatch-github-io\.pages\.dev/);
assert.match(html,/15125d1a\.westsidewatch-github-io\.pages\.dev/);
assert.match(html,/OLIVE MOUNTAIN/);
const out=path.join(root,'artifacts/p2-0104-olive');
fs.mkdirSync(out,{recursive:true});
(async()=>{
 const browser=await chromium.launch({headless:true});
 try{
  for(const vp of [{width:1648,height:928},{width:390,height:844}]){
   const page=await browser.newPage({viewport:vp,reducedMotion:'reduce'});
   const failures=[];
   page.on('pageerror',e=>failures.push(String(e)));
   await page.goto('http://127.0.0.1:4173/experiments/olive-engraving-v1-v2-compare.html',
    {waitUntil:'domcontentloaded',timeout:45000});
   await page.selectOption('#width',String(vp.width));
   for(const checkpoint of [
     '05b-two-voices-with-growing-olive-field',
     '09-twelve-voices-final-overview']){
    await page.selectOption('#stage',checkpoint);
    await page.waitForFunction(()=>{
      const imgs=[document.getElementById('before'),document.getElementById('after')];
      return imgs.every(i=>i.complete&&i.naturalWidth>200&&i.naturalHeight>200);
    },null,{timeout:30000});
    const imageInfo=await page.evaluate(()=>[...document.querySelectorAll('article img')]
      .map(i=>({src:i.src,width:i.naturalWidth,height:i.naturalHeight})));
    assert.equal(imageInfo.length,2);
    assert(imageInfo[0].src.includes('5aa9c100.'));
    assert(imageInfo[1].src.includes('15125d1a.'));
    assert.equal(imageInfo[0].width,imageInfo[1].width);
    assert.equal(imageInfo[0].height,imageInfo[1].height);
    const short=checkpoint.startsWith('05b-')?'live-growth':'twelve-index';
    await page.screenshot({
      path:path.join(out,vp.width+'-olive-v1-v2-'+short+'-review.png'),
      fullPage:true,animations:'disabled'});
    console.log('Olive V1 vs V2 comparable browser capture PASS',
      vp.width,checkpoint,JSON.stringify(imageInfo));
   }
   assert.equal(failures.length,0,'comparison-page errors '+failures.join(' | '));
   await page.close();
  }
 }finally{await browser.close()}
})().catch(error=>{console.error(error);process.exitCode=1});
