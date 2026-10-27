import assert from 'node:assert/strict';
import {mkdir,writeFile} from 'node:fs/promises';
import {chromium} from 'playwright';
const output=process.env.J3K_OUTPUT||'work/j3k-validation';await mkdir(output,{recursive:true});const browser=await chromium.launch({headless:true});
const url=process.env.J3K_URL||'http://127.0.0.1:8765/preview/jerusalem-3000/';
const scrub=(p,v)=>p.locator('.j3k-scrubber').evaluate((el,v)=>{el.value=String(v);el.dispatchEvent(new Event('input',{bubbles:true}));},v);
const ready=p=>p.waitForFunction(()=>window.__JERUSALEM3000__?.status==='ready');
try{
 const page=await browser.newPage({viewport:{width:1000,height:800},reducedMotion:'reduce'}),errors=[];
 page.on('pageerror',e=>errors.push(String(e)));
 await page.route('**/herodian-typology-grammar.js',async route=>{const response=await route.fetch(),source=await response.text(),needle='yieldControl = () => new Promise(resolve => setTimeout(resolve, 0))';assert.ok(source.includes(needle));await route.fulfill({response,body:source.replace(needle,'yieldControl = () => window.__TEST_GENERATION_GATE__ || new Promise(resolve => setTimeout(resolve, 0))')});});
 await page.goto(url,{waitUntil:'networkidle'});await ready(page);
 await page.evaluate(()=>{window.__TEST_GENERATION_GATE__=new Promise(resolve=>window.__releaseGeneration=resolve);});
 await scrub(page,3.99);await page.locator('.j3k-play').click();await page.waitForFunction(()=>window.__JERUSALEM3000__.playback?.status==='waiting'&&window.__JERUSALEM3000__.historicalTime.phase==='late-first-temple');
 assert.equal(await page.getByRole('button',{name:'統一尺度比較',exact:true}).getAttribute('aria-pressed'),'true','playback must use one landscape frame');
 const landscapeFrame=await page.evaluate(()=>window.__JERUSALEM3000__.renderDiagnostics.terrainPresentation.camera);
 const held=await page.evaluate(()=>({time:window.__JERUSALEM3000__.historicalTime.position,playback:window.__JERUSALEM3000__.playback}));assert.equal(held.time,4,'must enter slow phase exactly at its start');
 await page.waitForTimeout(900);assert.equal(await page.evaluate(()=>window.__JERUSALEM3000__.historicalTime.position),4,'no timeline movement while generation is held');
 await page.locator('.j3k-play').click();assert.equal(await page.locator('.j3k-play').getAttribute('aria-pressed'),'false');await page.evaluate(()=>window.__releaseGeneration());
 await page.waitForFunction(()=>window.__JERUSALEM3000__.renderDiagnostics.sharedEra?.status==='ready');await page.waitForTimeout(150);assert.equal(await page.evaluate(()=>window.__JERUSALEM3000__.historicalTime.position),4,'pausing while waiting must cancel automatic resume');
 await page.locator('.j3k-play').click();await page.waitForFunction(()=>window.__JERUSALEM3000__.historicalTime.position>4.03);await page.locator('.j3k-play').click();
 await page.evaluate(()=>{window.__TEST_GENERATION_GATE__=new Promise(resolve=>window.__releaseGeneration=resolve);});await scrub(page,7);await page.locator('.j3k-play').click();await page.waitForFunction(()=>window.__JERUSALEM3000__.playback?.status==='waiting');assert.equal(await page.evaluate(()=>window.__JERUSALEM3000__.historicalTime.position),7);await page.evaluate(()=>window.__releaseGeneration());await page.waitForFunction(()=>window.__JERUSALEM3000__.historicalTime.position>7.03);assert.equal(await page.locator('.j3k-play').getAttribute('aria-pressed'),'true','readiness must automatically resume an uncancelled play request');await page.locator('.j3k-play').click();
 assert.deepEqual(await page.evaluate(()=>window.__JERUSALEM3000__.renderDiagnostics.terrainPresentation.camera),landscapeFrame,'era changes must not jump the playback camera');
 await scrub(page,4);assert.equal(await page.getByRole('combobox',{name:'每期播放時間'}).inputValue(),'12');await page.locator('.j3k-play').click();
 const progression=[],presentationStarted=Date.now();
 for(const offset of [.1,.4,.82]){await page.waitForFunction(v=>{const s=window.__JERUSALEM3000__;return s.historicalTime.position>=v&&s.renderDiagnostics.phase==='late-first-temple';},4+offset);progression.push(await page.evaluate(()=>({position:window.__JERUSALEM3000__.historicalTime.position,buildings:window.__JERUSALEM3000__.renderDiagnostics.constructionPresentation.visibleByRole.housing})));await page.screenshot({path:`${output}/construction-${offset}.png`});}
 assert.ok(Date.now()-presentationStarted>=9000,'a full visible construction stage must take real viewing time');
 await page.locator('.j3k-play').click();assert.ok(progression[0].buildings>0&&progression[0].buildings<progression[1].buildings);assert.ok(progression[1].buildings<progression[2].buildings);assert.equal(progression[2].buildings,await page.evaluate(()=>window.__JERUSALEM3000__.renderDiagnostics.sharedEra.total));assert.ok(progression[2].position<5,'full city must be visible before leaving the era');
 await page.screenshot({path:`${output}/playback-ready.png`});assert.deepEqual(errors,[]);await page.close();
 const direct=await browser.newPage({viewport:{width:390,height:844},reducedMotion:'reduce'});await direct.goto(url,{waitUntil:'networkidle'});await ready(direct);await scrub(direct,6.1);await direct.waitForFunction(()=>window.__JERUSALEM3000__.renderDiagnostics.sharedEra?.status==='ready');
 const lazy=await direct.evaluate(()=>window.__JERUSALEM3000__.renderDiagnostics.sharedEra);assert.equal(lazy.projection,null,'hidden first-temple ruins must not be generated on direct Persian entry');assert.equal(lazy.successor.status,'ready');
 await direct.getByRole('button',{name:'前代遺存 · 推定',exact:true}).click();await direct.waitForFunction(()=>{const s=window.__JERUSALEM3000__.renderDiagnostics.sharedEra;return s.status==='ready'&&s.projection?.visibleBuildings>0;});
 const retained=await direct.evaluate(()=>window.__JERUSALEM3000__.renderDiagnostics.sharedEra);assert.equal(retained.projection.layerState,'retained-ruin');await direct.close();
 const failed=await browser.newPage();await failed.route('**/herodian-typology-grammar.js',async route=>{const response=await route.fetch();await route.fulfill({response,body:(await response.text()).replace('yieldControl = () => new Promise(resolve => setTimeout(resolve, 0))','yieldControl = async () => {throw new Error("controlled-generation-failure")}')});});await failed.goto(url,{waitUntil:'networkidle'});await ready(failed);await scrub(failed,4);await failed.locator('.j3k-play').click();await failed.waitForFunction(()=>window.__JERUSALEM3000__.playback?.status==='error');assert.equal(await failed.locator('.j3k-play').getAttribute('aria-pressed'),'false');assert.equal(await failed.evaluate(()=>window.__JERUSALEM3000__.historicalTime.position),4);await failed.close();
 await writeFile(`${output}/playback-proof.json`,JSON.stringify({held,progression,lazy:{status:lazy.status,earlierProjection:lazy.projection,successor:lazy.successor.status},retained:{status:retained.status,visibleBuildings:retained.projection.visibleBuildings},errors},null,2));
 console.log('PASS: actual delayed generation holds phase boundary, pause cancels resume, ready playback advances, direct Persian defers hidden ruins, opt-in ruins load and failure stops playback');
}finally{await browser.close();}
