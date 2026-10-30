import assert from 'node:assert/strict';
import {mkdir,writeFile} from 'node:fs/promises';
import {chromium} from 'playwright';
const output=process.env.J3K_OUTPUT||'work/j3k-validation';await mkdir(output,{recursive:true});
const browser=await chromium.launch({headless:true});
try{
 const page=await browser.newPage({viewport:{width:390,height:844},reducedMotion:'reduce'}),errors=[],requests=[],proof=[],first=new Map();
 page.on('pageerror',e=>errors.push(String(e)));page.on('request',r=>requests.push(r.url()));
 await page.goto(process.env.J3K_URL||'http://127.0.0.1:8765/preview/jerusalem-3000/',{waitUntil:'networkidle'});
 await page.waitForFunction(()=>window.__JERUSALEM3000__?.status==='ready');
 await page.getByRole('button',{name:'空間骨架對照',exact:true}).click();
 for(const phase of [13,14,15,16,17,16,15,12,11,10,17,16,13]){
  await page.locator('.j3k-scrubber').evaluate((el,value)=>{el.value=String(value);el.dispatchEvent(new Event('input',{bubbles:true}));},phase===17?17:phase+.9);
  await page.waitForFunction(value=>{const s=window.__JERUSALEM3000__;return s.historicalTime.position===value&&s.renderDiagnostics.phase===s.historicalTime.phase;},phase===17?17:phase+.9);
  const read=()=>page.evaluate(()=>{const s=window.__JERUSALEM3000__;return {foundation:s.inspectCityFoundation(),skeleton:s.inspectSpatialSkeleton(),inheritance:s.inheritanceState,overview:s.renderDiagnostics.cityOverview,camera:s.renderDiagnostics.terrainPresentation.camera};});
  const state=await read();assert.equal(state.foundation.owner,'independent-later-skeleton');assert.equal(state.foundation.renderer.unboundComponents,0);assert.equal(state.foundation.renderer.provisionalInheritedComponents,0);assert.equal(state.inheritance.active,false);assert.equal(state.skeleton.domains.routes.spatialObjects,({10:5,11:8,12:9,13:11,14:10,15:10,16:13,17:14})[phase]||3);assert.equal(state.overview.framePhase,phase>=16?'independent-expansion-shared-window':'independent-later-shared-window');
  if(first.has(phase))assert.deepEqual(state.skeleton.features,first.get(phase),'return must restore exact same map identities and geometry');else first.set(phase,state.skeleton.features);
  await page.getByRole('button',{name:'實證',exact:true}).click();const hidden=await read();assert.equal(hidden.skeleton.features.length,0);assert.equal(hidden.foundation.renderer.boundComponents,0);
  await page.getByRole('button',{name:'全部',exact:true}).click();const restored=await read();assert.deepEqual(restored.skeleton.features,state.skeleton.features);assert.equal(restored.foundation.renderer.visibleComponents,state.foundation.renderer.visibleComponents);
  if(phase>=13){await page.screenshot({path:`${output}/medieval-${phase}-mobile.png`,fullPage:true});proof.push({phase:state.foundation.phaseId,foundation:state.foundation,skeleton:state.skeleton,overview:state.overview,camera:state.camera});}
 }
 const box=await page.locator('.j3k-skeleton-panel canvas').boundingBox();assert.ok(box.x>=0&&box.x+box.width<=390);
 for(const pack of ['roman-byzantine-islamic','medieval-ottoman','expansion-modern'])assert.equal(requests.filter(url=>url.includes(`${pack}.skeleton.v1.json`)).length,1);
 for(const frame of ['independent-later-shared-window','independent-expansion-shared-window']){const group=proof.filter(p=>p.overview.framePhase===frame);assert.ok(group.every(p=>p.overview.distance===group[0].overview.distance),'return must restore the same portrait comparison distance per group');}assert.deepEqual(errors,[]);
 await writeFile(`${output}/medieval-proof.json`,JSON.stringify({proof,errors,scope:'inferred spatial foundation; historical acceptance false'},null,2));
 console.log('PASS: eight independent mobile phases, expansion/medieval reverse and evidence restore, shared portrait camera, zero unbound/inherited components, one request per pack');
}finally{await browser.close();}
