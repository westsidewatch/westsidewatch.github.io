/* P2 Dawn real Chromium E2E: Codrops-style in-grid book exploration.
 * Run after Hugo build with local server at http://127.0.0.1:4173:
 * node tests/p2-dawn-expanding-preview.cjs
 */
'use strict';
const {chromium}=require('playwright'),assert=require('node:assert/strict');
const fs=require('node:fs'),path=require('node:path');
const out='artifacts/p2-dawn-expander';fs.mkdirSync(out,{recursive:true});
const url='http://127.0.0.1:4173/experiments/p2-0105-dawn-preview.html';
(async()=>{
 const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
 try{
  for(const [device,width,height] of [['desktop',1440,900],['phone',390,844]]){
   const page=await browser.newPage({viewport:{width,height}});
   const errors=[];page.on('pageerror',err=>errors.push(err.message));
   await page.goto(url+'?layer=catalogue&d=28.4&v=expander-qa',{waitUntil:'domcontentloaded',timeout:45000});
   await page.waitForFunction(()=>document.querySelector('#dawn-classification-tree button.dawn-classification__sleeve'),null,{timeout:35000});
   await page.locator('#dawn-primary-records').click();
   await page.waitForFunction(()=>document.querySelectorAll('#dawn-works button.dawn-catalogue__cover-card').length>=3,null,{timeout:35000});
   const cards=page.locator('#dawn-works button.dawn-catalogue__cover-card');
   const route=page.url();
   await cards.nth(0).click();
   const exp=page.locator('#dawn-book-expanding-preview');
   await exp.waitFor({timeout:12000});
   assert.equal(await page.locator('#dawn-book-expanding-preview').count(),1,device+': must have one preview');
   assert.equal(await exp.evaluate(el=>el.tagName),'LI',device+': ordered list preview must be LI');
   assert(!(await page.locator('#dawn-book-detail').isVisible()),device+': first click must not navigate to reader');
   assert.equal(page.url(),route,device+': thumbnail click navigated');
   const first=await exp.locator('.dawn-expander__title').innerText();
   assert(first.trim().length>0,device+': title unavailable');
   await cards.nth(1).click();
   await page.waitForFunction(old=>document.querySelector('#dawn-book-expanding-preview .dawn-expander__title')?.textContent!==old,first,{timeout:15000});
   await page.waitForTimeout(460); // screenshot the final folio, not the transition midpoint
   const second=await exp.locator('.dawn-expander__title').innerText();
   assert.notEqual(second,first,device+': selection did not change');
   assert.equal(await page.locator('#dawn-book-expanding-preview').count(),1,device+': selecting second book created two preview panels');
   assert.equal(page.url(),route,device+': switching to second book navigated');
   assert(!(await page.locator('#dawn-book-detail').isVisible()),device+': second thumbnail navigated without explicit interest');
   await page.screenshot({path:path.join(out,device+'-inline-book-switch.png'),fullPage:false});
   await exp.locator('.dawn-expander__close').click();
   assert.equal(await page.locator('#dawn-book-expanding-preview').count(),0,device+': close did not restore grid');
   await cards.nth(0).click();
   await exp.waitFor({timeout:10000});
   await exp.locator('.dawn-expander__read').click();
   await page.locator('#dawn-book-detail').waitFor({state:'visible',timeout:20000});
   assert(await page.locator('#dawn-book-detail').isVisible(),device+': explicit preview reading action did not open original reader');
   assert.equal(await page.locator('#dawn-book-expanding-preview').count(),0,device+': dangling preview in detail reader');
   await page.screenshot({path:path.join(out,device+'-explicit-read.png'),fullPage:false});
   await page.locator('#dawn-book-back').click();
   assert(await page.locator('#dawn-works').isVisible(),device+': original list not restored');
   assert.equal(errors.length,0,device+': page errors: '+errors.join('; '));
   console.log('DAWN_EXPANDING_PREVIEW',device,'SELECT_SWITCH_CLOSE_EXPLICIT_READ_BACK_PASS');
   await page.close();
  }
  // Also verify semantic Living subject wall uses exactly the same expander.
  const page=await browser.newPage({viewport:{width:1440,height:900}});
  await page.goto(url+'?layer=catalogue&d=28.4&v=expander-category',{waitUntil:'domcontentloaded',timeout:45000});
  await page.waitForFunction(()=>document.querySelectorAll('#dawn-classification-tree button.dawn-classification__sleeve').length===10,null,{timeout:35000});
  await page.locator('#dawn-classification-tree button.dawn-classification__sleeve').first().click();
  await page.locator('#dawn-classification-tree button.dawn-classification__sleeve').first().click();
  await page.waitForFunction(()=>document.querySelectorAll('#dawn-classification-results .dawn-classification__book').length>=2,null,{timeout:45000});
  await page.locator('#dawn-classification-results .dawn-classification__book').first().click();
  assert(await page.locator('#dawn-classification-results .dawn-expander').isVisible(),'Living classified books missing in-row preview');
  assert(!(await page.locator('#dawn-book-detail').isVisible()),'Living thumbnail must not navigate');
  await page.locator('#dawn-classification-results .dawn-expander__read').click();
  await page.locator('#dawn-book-detail').waitFor({state:'visible',timeout:20000});
  assert(await page.locator('#dawn-book-detail').isVisible(),'Living book did not open after explicit confirmation');
  console.log('DAWN_EXPANDING_PREVIEW','LIVING_CLASSIFIED_BOOK_TWO_STEP_PASS');
  await page.close();
 }finally{await browser.close()}
})().catch(err=>{console.error(err);process.exitCode=1});
