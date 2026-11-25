import {chromium} from '@playwright/test';
import {mkdirSync,writeFileSync} from 'node:fs';
import assert from 'node:assert/strict';
const out='artifacts/foundation-096-r06';mkdirSync(out,{recursive:true});
const browser=await chromium.launch({headless:true});
const results=[];
for(const realm of ['church','journal','dawn']) for(const width of [1440,768,390,320]){
 const page=await browser.newPage({viewport:{width,height:900},reducedMotion:'reduce'});
 const result={realm,width,errors:[]};
 try{
 const url=(process.env.REVIEW_URL||'http://127.0.0.1:4173/experiments/foundation-096-r06/')+'?realm='+realm;
 const res=await page.goto(url,{waitUntil:'domcontentloaded',timeout:30000});assert(res?.ok());
 await page.evaluate(()=>document.fonts.ready);
 const current=page.locator('.realm:not([hidden])');
 assert.equal(await current.locator('h1').count(),1);
 for(const img of await current.locator('img').all())await img.evaluate(i=>i.decode()).catch(()=>result.errors.push('image unavailable'));
 const geometry=()=>current.evaluate(root=>[...root.querySelectorAll('h1,.church-field,.scripture,.architecture,.worship,.movement,.movement li,.dawn-field,.art,.leaf,.leaf h2')].map(e=>{const r=e.getBoundingClientRect();return [r.x,r.y,r.width,r.height].map(x=>Math.round(x*10)/10)}));
 const natural=await geometry();
 result.geometry=natural;
 assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'horizontal overflow');
 assert.equal(await current.locator('a').filter({hasText:/[↗↘→←↓↑]/u}).count(),0,'arrow link');
 await page.screenshot({path:out+'/'+realm+'-'+width+'.png',fullPage:true,timeout:30000});
 await page.locator('[data-marks]').click();
 assert.equal(await current.locator('.mark,.printmark').evaluateAll(es=>es.filter(e=>getComputedStyle(e).visibility==='visible').length),0);
 assert.deepEqual(await geometry(),natural,'hiding marks alters layout');
 await page.locator('[data-marks]').click();
 await page.locator('[data-flat]').click();const flat=await geometry();assert.notDeepEqual(flat,natural,'flat comparison does not alter geometry');
 await page.screenshot({path:out+'/'+realm+'-'+width+'-flat.png',fullPage:true,timeout:30000});
 await page.locator('[data-flat]').click();
 if(realm==='church'){assert.equal(await current.locator('.program li').count(),7);assert.equal(await current.locator('.architecture iframe').count(),1);assert.notEqual(await current.locator('.terrain').evaluate(e=>getComputedStyle(e).clipPath),'none');}
 if(realm==='journal'){assert.equal(await current.locator('.movement').count(),4);assert.equal(await current.locator('.movement li').count(),12);result.layouts=await current.locator('.movement ol').evaluateAll(es=>es.map(e=>getComputedStyle(e).gridTemplateColumns));assert(new Set(result.layouts).size>=2,'no editorial rhythm differences');}
 if(realm==='dawn'){const artWidth=()=>current.locator('.art').evaluate(e=>e.getBoundingClientRect().width);const landscape=await artWidth();await current.locator('[data-plate="1"]').click();await current.locator('#plate-image').evaluate(i=>i.decode());const portrait=await artWidth();result.aperture={landscape,portrait};assert(portrait<landscape*.85,'art orientation does not change layout');assert.equal(await current.locator('.dawn-field').getAttribute('data-orientation'),'portrait');await page.screenshot({path:out+'/dawn-'+width+'-portrait.png',fullPage:true,timeout:30000});}
 }catch(e){result.errors.push(String(e))}
 finally{console.log(JSON.stringify(result));results.push(result);await page.close()}
}
await browser.close();writeFileSync(out+'/report.json',JSON.stringify(results,null,2));if(results.some(r=>r.errors.length))process.exitCode=1;
