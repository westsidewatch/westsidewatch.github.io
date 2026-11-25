const { chromium }=require('playwright');
const fs=require('node:fs'),assert=require('node:assert/strict');
const OUT='artifacts/watch-window-r15',BASE='http://127.0.0.1:4173',OLD='https://f1227647.westsidewatch-github-io.pages.dev';
fs.mkdirSync(OUT,{recursive:true});
(async()=>{const browser=await chromium.launch({headless:true,args:['--no-sandbox']});const results=[];
const pages=[
 ['church-static','/church/visit/','.church-visit__hero-links.ww-paired',async p=>{await p.waitForFunction(()=>document.querySelectorAll('#church-sunday-live .ws-church-sunday-row').length===7);assert.equal(await p.locator('.church-visit__hero-links a').count(),2)}],
 ['church-tour','/p2/church-tour.html?entry=p2','.ws-ministry-story__rail',async p=>{assert.equal(await p.locator('#church-canvas').count(),1);await p.waitForSelector('.ws-ministry-story__chapter',{state:'attached'});assert.equal(await p.locator('.ws-ministry-story__chapter').count(),7)}],
 ['church-decision','/church/forms/?type=decision','.church-form__scripture-pair',async p=>{await p.waitForSelector('.church-form__scripture-hint--nahum',{state:'visible'})}],
 ['emmaus','/one/?book=42&chapter=24','#view-chapter .ww-chapter-head',async p=>{await p.locator('[data-view="view-chapter"]').click({timeout:20000});await p.waitForSelector('#frontispiece-title',{state:'visible'})}],
 ['olive-second','/experiments/p2-0104-olive-continuation.html?d=24.7','#olive-second-layer',async p=>{await p.locator('#olive-twin-entry').click({timeout:20000});await p.waitForFunction(()=>document.querySelector('#olive-second-layer').getAttribute('aria-hidden')==='false',null,{timeout:25000});assert.equal(await p.locator('.olive-second-layer__person').count(),12);await p.locator('.olive-second-layer__person').first().click();await p.waitForSelector('#olive-second-detail',{state:'visible'});}],
 ['dawn-second','/experiments/p2-0105-dawn-preview.html?layer=second','#dawn-wall',async p=>{await p.waitForSelector('#dawn-second .dawn-feature',{state:'visible',timeout:30000});assert.equal(await p.locator('#dawn-second .dawn-feature').count(),3)}],
 ['dawn-third','/experiments/p2-0105-dawn-preview.html?layer=catalogue&d=28.4','#dawn-book-detail',async p=>{await p.waitForSelector('#dawn-classification-tree button.dawn-classification__sleeve',{timeout:35000});await p.locator('#dawn-primary-records').click();await p.waitForSelector('#dawn-works button.dawn-catalogue__cover-card',{timeout:35000});await p.locator('#dawn-works button.dawn-catalogue__cover-card').first().click();await p.locator('#dawn-book-expanding-preview .dawn-expander__read').click();await p.waitForSelector('#dawn-book-detail',{state:'visible',timeout:20000})}],
 ['cinema-entry','/first-look-editorial/cinema.html','.ww-film-stage',async p=>{assert.equal(await p.locator('.ww-film-stage .ww-window').count(),2);await p.waitForFunction(()=>{const i=document.querySelector('.ww-film-stage img');return i?.complete&&i.naturalWidth>0},null,{timeout:25000})}],
 ['cinema-second','/cinema/','.ww-cinema-program',async p=>{assert.equal(await p.locator('.ww-cinema-program .ww-window').count(),2);await p.waitForFunction(()=>{const i=document.querySelector('.ww-cinema-program img');return i?.complete&&i.naturalWidth>0},null,{timeout:25000})}],
 ['daylight-entry','/first-look-editorial/life.html','.ww-life-stage',async p=>assert.equal(await p.locator('.ww-life-stage .ww-window').count(),2)],
 ['daylight-second','/daylight-cafe/','.ww-daylight-daily',async p=>{const i=p.locator('[data-fl-date-input]');await i.waitFor();const v=await i.inputValue();await p.locator('[data-fl-date-step="1"]').click();await p.waitForFunction(v=>document.querySelector('[data-fl-date-input]').value!==v,v,{timeout:10000});}]
];
for(const [device,width,height] of [['desktop',1440,900],['mobile',390,844]]){
 for(const [name,url,selector,check] of pages){
  const p=await browser.newPage({viewport:{width,height},reducedMotion:'reduce'});const errors=[];p.on('pageerror',e=>errors.push(e.message));
  const r={device,name,url,errors};try{
   const res=await p.goto(BASE+url,{waitUntil:'domcontentloaded',timeout:45000});assert.equal(res.status(),200);
   assert.equal(await p.locator('link[href="/css/watch-window-r15.css"]').count(),1);
   await check(p);
   const region=p.locator(selector).first();await region.waitFor({state:'visible',timeout:20000});
   await region.scrollIntoViewIfNeeded({timeout:8000});await p.screenshot({path:OUT+'/'+device+'-'+name+'.png',animations:'disabled'});
   r.geometry=await p.evaluate(()=>({width:innerWidth,scrollWidth:document.documentElement.scrollWidth,windows:[...document.querySelectorAll('.ww-paired>.ww-window')].map(e=>{const b=e.getBoundingClientRect();return {w:b.width,h:b.height,scrollHeight:e.scrollHeight,clientHeight:e.clientHeight}})}));
   assert.ok(r.geometry.scrollWidth<=width+2,'horizontal document overflow');
   for(const w of r.geometry.windows)if(w.w>0){assert.ok(Math.abs(w.w-w.h)<3,'window is not square');assert.ok(w.scrollHeight<=w.clientHeight+3,'window text overflows')}
   r.pass=true;
  }catch(e){r.pass=false;r.error=String(e);await p.screenshot({path:OUT+'/'+device+'-'+name+'-failure.png'}).catch(()=>{})}
  results.push(r);await p.close();
 }
}
fs.writeFileSync(OUT+'/report.json',JSON.stringify(results,null,2));console.log(JSON.stringify(results));await browser.close();if(results.some(r=>!r.pass))process.exitCode=1;
})().catch(e=>{console.error(e);process.exitCode=1});
