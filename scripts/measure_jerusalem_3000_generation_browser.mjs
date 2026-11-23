import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import {chromium} from 'playwright';
import {openToolsForReview} from './lib/jerusalem-browser-tools.mjs';
const url=process.env.J3K_URL||'http://127.0.0.1:8765/preview/jerusalem-3000/',out=process.env.J3K_OUTPUT||'work/generation-profile';await fs.mkdir(out,{recursive:true});
const browser=await chromium.launch({headless:true}),rows=[],errors=[];
try{
 const page=await browser.newPage({viewport:{width:1200,height:900},reducedMotion:'reduce'});page.on('pageerror',e=>errors.push(String(e)));await openToolsForReview(page);const start=performance.now();await page.goto(url,{waitUntil:'domcontentloaded'});await page.waitForFunction(()=>window.__JERUSALEM3000__?.status==='ready');const initialReadyWallMilliseconds=performance.now()-start;
 async function visit(index,pass){
  const started=performance.now(),position=index===17?17:index+.9;
  await page.locator('.j3k-scrubber').evaluate((e,v)=>{e.value=String(v);e.dispatchEvent(new Event('input',{bubbles:true}));},position);
  await page.waitForFunction(v=>{const s=window.__JERUSALEM3000__,d=s.renderDiagnostics;return s.historicalTime.position===v&&d.housingBatches?.phase===s.historicalTime.phase&&(![4,5,6,7].includes(Math.floor(v))||d.sharedEra.status==='ready');},position);
  await page.evaluate(()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r))));
  const d=await page.evaluate(()=>{const s=window.__JERUSALEM3000__,d=s.renderDiagnostics;return{phase:s.historicalTime.phase,world:d.cityWorld,shared:d.sharedEra,renderCost:d.renderCost,batches:d.housingBatches,accounted:s.inspectCityFoundation().registrationAccounting.visibleScopeAccounted};});assert.ok(d.accounted);rows.push({index,pass,automationToSettledWallMilliseconds:performance.now()-started,...d});await fs.writeFile(`${out}/progress.json`,JSON.stringify({initialReadyWallMilliseconds,rows,errors},null,2));
 }
 for(let i=0;i<18;i++)await visit(i,'first-visit');const cold=rows.at(-1).world;assert.equal(cold.builds,8);assert.equal(Object.keys(cold.generationTimings).length,8);
 const identities=await page.evaluate(()=>Object.fromEntries(window.__JERUSALEM3000__.renderDiagnostics.cityWorld.cachedPhases.map(p=>[p,window.__JERUSALEM3000__.inspectPersistentCityPhase(p)])));
 for(let i=17;i>=0;i--)await visit(i,'return-visit');const warm=rows.at(-1).world;assert.equal(warm.builds,cold.builds,'return visits must not regenerate later phases');assert.ok(warm.cacheHits>cold.cacheHits);
 assert.deepEqual(await page.evaluate(phases=>Object.fromEntries(phases.map(p=>[p,window.__JERUSALEM3000__.inspectPersistentCityPhase(p)])),Object.keys(identities)),identities,'cached mesh and buffer identities persist');assert.deepEqual(errors,[]);
 await fs.writeFile(`${out}/generation-profile.json`,JSON.stringify({initialReadyWallMilliseconds,rows,errors,scope:'single fresh page; first visits and reverse returns in same page; automation-to-settled includes rendering and harness overhead; not network bytes or cross-device guarantee',historicalAcceptance:false},null,2));console.log('PASS:18 first visits and18 returns,8 persistent builds, stable cached identities, stage timings, source accounting and no page errors');
}finally{await browser.close();}
