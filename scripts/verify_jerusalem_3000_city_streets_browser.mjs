import assert from 'node:assert/strict';
import {readFile,mkdir,writeFile} from 'node:fs/promises';
import {chromium} from 'playwright';
const out=process.env.J3K_OUTPUT||'work/city-streets',url=process.env.J3K_URL||'http://127.0.0.1:8765/preview/jerusalem-3000/';
await mkdir(out,{recursive:true});
const browser=await chromium.launch({headless:true}),errors=[],results={};
try{
 for(const mode of process.env.J3K_ROADS_BEFORE?['before','after']:['after']){
  const page=await browser.newPage({viewport:{width:1350,height:950},reducedMotion:'reduce'});
  page.on('pageerror',e=>errors.push(String(e)));
  if(!url.startsWith('https:'))await page.route('**/css/typography-sitewide.css',r=>r.fulfill({path:'static/css/typography-sitewide.css',contentType:'text/css'}));
  if(mode==='before')for(const [pattern,path]of[['**/herodian-road-geometry.js',process.env.J3K_ROADS_BEFORE],['**/city-visual-hierarchy.js',process.env.J3K_ROAD_HIERARCHY_BEFORE]]){const body=await readFile(path,'utf8');await page.route(pattern,r=>r.fulfill({body,contentType:'text/javascript'}));}
  await page.goto(url,{waitUntil:'networkidle'});await page.waitForFunction(()=>window.__JERUSALEM3000__?.status==='ready');
  const rows=[];
  for(let i=0;i<18;i++){
   const position=i===17?17:i+.9;
   await page.locator('.j3k-scrubber').evaluate((e,v)=>{e.value=String(v);e.dispatchEvent(new Event('input',{bubbles:true}));},position);
   await page.waitForFunction(v=>{const s=window.__JERUSALEM3000__,d=s.renderDiagnostics;return s.historicalTime.position===v&&d.phase===s.historicalTime.phase&&d.cityGenerationStatus==='ready';},position);
   await page.getByRole('button',{name:'城市總覽',exact:true}).click();
   await page.evaluate(()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r))));
   const row=await page.evaluate(()=>{const s=window.__JERUSALEM3000__,t=s.renderDiagnostics.terrainPresentation,f=s.inspectCityFoundation();return{phase:s.historicalTime.phase,terrain:t,landmarks:f.renderer.visibleLandmarkIds,ownership:f.renderer.outOfPhaseBindingIds,roads:s.inspectRoadSurfaces(),housing:s.inspectOverviewBaseline().registeredHousingObjects};});
   assert.equal(row.terrain.verticalScale,1);assert.deepEqual(row.ownership,[]);
   if(mode==='after'){assert.equal(row.roads.outsideTerrain,0);assert.ok(row.roads.maxOffsetErrorMetres<.002,`${i} road contact error ${row.roads.maxOffsetErrorMetres}`);if(i>=4)assert.ok(row.roads.meshes>0);}
   if(results.before){const b=results.before[i];assert.deepEqual(row.landmarks,b.landmarks);assert.equal(row.housing,b.housing);assert.deepEqual(row.terrain.camera,b.terrain.camera);assert.deepEqual(row.terrain.target,b.terrain.target);assert.equal(row.terrain.gridId,b.terrain.gridId);}
   rows.push(row);
   if([3,8,11,12,15,17].includes(i))await page.locator('.j3k-stage').screenshot({path:`${out}/${mode}-${i}.png`});
  }
  await page.setViewportSize({width:390,height:844});await page.getByRole('button',{name:'城市總覽',exact:true}).click();assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);await page.screenshot({path:`${out}/${mode}-mobile.png`,fullPage:true});
  results[mode]=rows;await page.close();
 }
 assert.deepEqual(errors,[]);await writeFile(`${out}/city-streets-proof.json`,JSON.stringify({results,errors,streetPlansChanged:false,pavingGeometryChanged:true,ancientSurfaceVerified:false,visualAcceptance:'requires-human-review'},null,2));console.log('PASS:18 street states and ground-contact checks, original cameras/housing/landmarks/scale, portrait, zero page errors; baseline when supplied');
}finally{await browser.close();}
