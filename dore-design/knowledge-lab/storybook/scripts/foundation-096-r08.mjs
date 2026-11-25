import {chromium} from '@playwright/test';
import {mkdirSync,writeFileSync} from 'node:fs';
import assert from 'node:assert/strict';
const out='artifacts/foundation-096-r08';mkdirSync(out,{recursive:true});
const browser=await chromium.launch({headless:true});const results=[];
for(const width of [1440,768,390,320]){
 const page=await browser.newPage({viewport:{width,height:900},reducedMotion:'reduce'});
 const report={width,errors:[]};
 try{
 const r=await page.goto((process.env.REVIEW_URL||'http://127.0.0.1:4173/experiments/foundation-096-r08/'),{waitUntil:'domcontentloaded',timeout:30000});assert(r?.ok());
 await page.evaluate(()=>document.fonts.ready);
 for(const img of await page.locator('img').all())await img.evaluate(i=>i.decode()).catch(()=>report.errors.push('image unavailable'));
 assert.equal(await page.locator('.joint').count(),3);
 assert.equal(await page.locator('.continuous svg').count(),4);
 assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'horizontal overflow');
 const metrics=()=>page.locator('.joint').evaluateAll(es=>es.map(e=>{const a=e.querySelector('.field'),b=e.querySelector('.counter'),x=a.getBoundingClientRect(),y=b.getBoundingClientRect();return {overlap:x.bottom-y.top,depth:parseFloat(getComputedStyle(e).gridTemplateRows.split(' ')[1]),upper:getComputedStyle(a,'::before').clipPath,lower:getComputedStyle(b,'::before').clipPath}}));
 const natural=await metrics();report.joints=natural;
 for(const j of natural){assert(j.upper.startsWith('polygon(')&&j.lower.startsWith('polygon('),'invalid masks');assert(Math.abs(j.overlap-j.depth)<1,'seam mismatch');assert(j.depth>0,'no joint depth')}
 await page.screenshot({path:out+'/'+width+'-natural.png',fullPage:true,timeout:30000});
 for(const id of ['church','journal','dawn'])await page.locator('#'+id).screenshot({path:out+'/'+width+'-'+id+'.png',timeout:30000});
 await page.locator('[data-control=markless]').click();assert.equal(await page.locator('.imprint,.optical-mark').evaluateAll(es=>es.filter(e=>getComputedStyle(e).visibility==='visible').length),0);assert.deepEqual(await metrics(),natural);
 await page.screenshot({path:out+'/'+width+'-markless.png',fullPage:true,timeout:30000});
 await page.locator('[data-control=markless]').click();await page.locator('[data-control=reverse]').click();assert.deepEqual(await metrics(),natural);await page.screenshot({path:out+'/'+width+'-reverse.png',fullPage:true,timeout:30000});
 await page.locator('[data-control=reverse]').click();await page.locator('[data-control=flat]').click();for(const j of await metrics())assert.equal(j.upper,'none');await page.screenshot({path:out+'/'+width+'-flat.png',fullPage:true,timeout:30000});
 await page.locator('[data-control=flat]').click();const landscape=await page.locator('.dawn .art').evaluate(e=>e.getBoundingClientRect().width);await page.locator('[data-plate="1"]').click();await page.locator('#art').evaluate(i=>i.decode());const portrait=await page.locator('.dawn .art').evaluate(e=>e.getBoundingClientRect().width);assert(portrait<landscape*.85,'art aspect ratio did not alter aperture');report.aperture={landscape,portrait};await page.locator('#dawn').screenshot({path:out+'/'+width+'-portrait.png',timeout:30000});
 }catch(e){report.errors.push(String(e))}
 finally{results.push(report);console.log(JSON.stringify(report));await page.close()}
}
await browser.close();writeFileSync(out+'/report.json',JSON.stringify(results,null,2));if(results.some(r=>r.errors.length))process.exitCode=1;
