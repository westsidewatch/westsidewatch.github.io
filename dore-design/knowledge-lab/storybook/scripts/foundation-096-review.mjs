import {chromium} from '@playwright/test';
import {readFileSync,writeFileSync,mkdirSync} from 'node:fs';
import assert from 'node:assert/strict';
const url=process.env.REVIEW_URL||'http://127.0.0.1:4173/experiments/foundation-096-r05/';
const out='artifacts/foundation-096-r05';
mkdirSync(out,{recursive:true});
const browser=await chromium.launch({headless:true});
const results=[];
const failures=[];
for(const route of ['church.html','journal.html','dawn.html','wall.html'])for(const width of [1440,768,390,320]){
 const page=await browser.newPage({viewport:{width,height:900},reducedMotion:'reduce'});
 const report={route,width,errors:[]};
 try{
  const response=await page.goto(url+route,{waitUntil:'domcontentloaded',timeout:30000});
  assert(response?.ok(),'HTTP '+response?.status());
  await page.evaluate(()=>document.fonts.ready);
  if(route==='dawn.html'){await page.locator('#plate-image').evaluate(img=>img.decode()).catch(e=>report.errors.push('first Met image unavailable'));}
  const snapshot=()=>page.evaluate(()=>({width:innerWidth,scrollWidth:document.documentElement.scrollWidth,headings:[...document.querySelectorAll('h1')].map(h=>({text:h.innerText,font:getComputedStyle(h).fontFamily,size:getComputedStyle(h).fontSize})),brokenImages:[...document.images].filter(i=>i.complete&&!i.naturalWidth).map(i=>i.src),marks:[...document.querySelectorAll('.printmark,.wall-ink')].filter(i=>getComputedStyle(i).visibility==='visible').length,visibleArrows:[...document.querySelectorAll('a[href]')].filter(a=>a.getClientRects().length&&/[↗↘→←↓↑]/u.test(a.innerText)).map(a=>a.innerText)}));
  report.before=await snapshot();
  if(report.before.scrollWidth>width+2)report.errors.push('horizontal overflow');
  if(report.before.headings.length!==1)report.errors.push('one h1 required');
  if(report.before.visibleArrows.length)report.errors.push('decorative link arrows');
  if(report.before.brokenImages.length)report.errors.push('broken images');
  await page.screenshot({path:out+'/'+route+'-'+width+'.png',fullPage:true,timeout:20000});
  const geometry=()=>page.evaluate(()=>[...document.querySelectorAll('h1,.bookplate,.illustration,.worship-mini,.spread,.opening,.movement,.atlas-field,.leaf,.wallband')].map(e=>{let r=e.getBoundingClientRect();return [Math.round(r.x),Math.round(r.y),Math.round(r.width),Math.round(r.height)]}));
  const beforeGeometry=await geometry();
  await page.locator('[data-ink-toggle]').click();
  report.markless=await snapshot();
  if(report.markless.marks!==0)report.errors.push('visible marks in markless mode');
  assert.deepEqual(await geometry(),beforeGeometry,'markless mode changed layout geometry');
  await page.screenshot({path:out+'/'+route+'-'+width+'-markless.png',fullPage:true,timeout:20000});
  if(route==='church.html'){
   assert.equal(await page.locator('.sunday .program li').count(),7);
   assert.equal(await page.locator('.wall iframe').count(),1);
   assert.equal(await page.locator('a[href="/church/visit/"]').count(),1);
  }
  if(route==='journal.html'){assert.equal(await page.locator('.movement li').count(),12);assert.equal(await page.locator('.movement').count(),4);}
  if(route==='wall.html'){
   assert.equal(await page.locator('.wallband button').count(),7);
   await page.locator('[data-ink-toggle]').click();
   await page.locator('.wallband [data-realm="library"]').click();
   assert.equal(await page.locator('.wallband [aria-pressed=true]').count(),1);
   assert.equal(await page.locator('#selected-zh').textContent(),'黎明書局');
  }
  if(route==='dawn.html'){
   const area=()=>page.locator('#atlas-field .art').evaluate(e=>Math.round(e.getBoundingClientRect().width));
   const landscape=await area();
   await page.locator('[data-plate="1"]').click();
   await page.locator('#plate-image').evaluate(img=>img.decode()).catch(e=>report.errors.push('second Met image unavailable'));
   await page.waitForTimeout(450);
   const portrait=await area();
   report.aperture={landscape,portrait,orientation:await page.locator('#atlas-field').getAttribute('data-orientation')};
   assert.equal(report.aperture.orientation,'portrait');
   if(width>760)assert(portrait<landscape*.85,'portrait did not change reading field');
   await page.locator('[data-ink-toggle]').click();
   await page.screenshot({path:out+'/dawn-portrait-'+width+'.png',fullPage:true,timeout:20000});
  }
 }catch(e){report.errors.push(String(e))}
 finally{results.push(report);if(report.errors.length)failures.push({route,width,errors:report.errors});console.log(JSON.stringify(report));await page.close();}
}
await browser.close();writeFileSync(out+'/report.json',JSON.stringify({results,failures},null,2));
if(failures.length)process.exitCode=1;
