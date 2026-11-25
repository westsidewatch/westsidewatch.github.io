import {chromium} from '@playwright/test';
import {mkdirSync,writeFileSync,readFileSync} from 'node:fs';
import assert from 'node:assert/strict';
const out='artifacts/foundation-096-r07';mkdirSync(out,{recursive:true});
const browser=await chromium.launch({headless:true});
const results=[];
for(const realm of ['home','church','journal','one','olive','dawn'])for(const width of [1440,768,390,320]){
 const page=await browser.newPage({viewport:{width,height:900},reducedMotion:'reduce'});
 const report={realm,width,errors:[]};
 try{
  const url=(process.env.REVIEW_URL||'http://127.0.0.1:4173/experiments/foundation-096-r07/')+'?realm='+realm;
  const response=await page.goto(url,{waitUntil:'domcontentloaded',timeout:30000});assert(response?.ok());
  await page.evaluate(()=>document.fonts.ready);
  const current=page.locator('.realm:not([hidden])');assert.equal(await current.count(),1);assert.equal(await current.locator('h1').count(),1);
  const master=await page.evaluate(async()=>{const r=await fetch('/images/watch-rhythm-original.svg');return r.text()});assert.equal(master.trim(),readFileSync('static/images/watch-rhythm-original.svg','utf8').trim());
  assert.equal(await page.locator('.rail-bay').count(),7);assert.equal(await page.locator('.rail-mark').count(),4);
  for(const img of await current.locator('img').all())await img.evaluate(i=>{i.loading='eager';return i.decode()}).catch(()=>report.errors.push('image unavailable'));
  const geometry=()=>current.evaluate(root=>[...root.querySelectorAll('h1,.home-encounter,.home-opening,.church-field,.scripture,.architecture,.worship,.movement,.movement li,.scripture-spread,.one-art,.olive-intro,.speaker,.dawn-field,.art,.leaf')].map(e=>{const r=e.getBoundingClientRect();return [r.x,r.y,r.width,r.height].map(n=>Math.round(n*10)/10)}));
  const original=await geometry();report.geometry=original;
  assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'horizontal overflow');
  assert.equal(await page.locator('a:visible').filter({hasText:/[↗↘→←↓↑]/u}).count(),0,'decorative arrow');
  await page.screenshot({path:out+'/'+realm+'-'+width+'.png',fullPage:true,timeout:30000});
  await page.locator('[data-marks]').click();
  assert.equal(await page.locator('.realm:not([hidden]) .mark,.realm:not([hidden]) .printmark,.rail-mark').evaluateAll(es=>es.filter(e=>getComputedStyle(e).visibility==='visible').length),0);
  assert.deepEqual(await geometry(),original,'markless geometry changed');
  await page.locator('[data-marks]').click();
  await page.locator('[data-flat]').click();const flat=await geometry();
  assert.notDeepEqual(flat,original,'flat control unchanged');
  await page.screenshot({path:out+'/'+realm+'-'+width+'-flat.png',fullPage:true,timeout:30000});
  await page.locator('[data-flat]').click();
  if(realm==='home'){assert.equal(await current.locator('.home-encounter').count(),5);assert.equal(await current.locator('.home-secondary a').count(),2);assert.equal(await current.locator('.home-pair blockquote').count(),2);}
  if(realm==='church'){assert.equal(await current.locator('.program li').count(),7);assert.equal(await current.locator('.architecture iframe').count(),1);}
  if(realm==='journal'){assert.equal(await current.locator('.movement').count(),4);assert.equal(await current.locator('.movement li').count(),12);}
  if(realm==='one'){assert.equal(await current.locator('.paired-verse blockquote').count(),2);assert.equal(await current.locator('a[href="/one/?book=42&chapter=24"]').count(),1);}
  if(realm==='olive'){assert.equal(await current.locator('.speaker').count(),12);assert.equal(await current.locator('.olive-intro blockquote').count(),2);}
  if(realm==='dawn'){const artWidth=()=>current.locator('.art').evaluate(e=>e.getBoundingClientRect().width);const landscape=await artWidth();await current.locator('[data-plate="1"]').click();await current.locator('#plate-image').evaluate(i=>i.decode());const portrait=await artWidth();report.aperture={landscape,portrait};assert(portrait<landscape*.85,'portrait width not adapted');await page.screenshot({path:out+'/dawn-'+width+'-portrait.png',fullPage:true,timeout:30000});}
 }catch(e){report.errors.push(String(e))}
 finally{console.log(JSON.stringify(report));results.push(report);await page.close()}
}
await browser.close();writeFileSync(out+'/report.json',JSON.stringify(results,null,2));if(results.some(r=>r.errors.length))process.exitCode=1;
