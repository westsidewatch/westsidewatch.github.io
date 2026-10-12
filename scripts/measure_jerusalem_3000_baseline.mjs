import {chromium} from 'playwright';
import {mkdir,writeFile} from 'node:fs/promises';
const url=process.env.J3K_URL||'https://westsidewatch.github.io/preview/jerusalem-3000/';
const output=process.env.J3K_OUTPUT||'work/j3k-baseline';
await mkdir(output,{recursive:true});
const browser=await chromium.launch({headless:true});
const samples=[];
try {
 for(const [profile,viewport] of [['desktop',{width:1440,height:1000}],['mobile-viewport',{width:390,height:844}]]) {
  const context=await browser.newContext({viewport,reducedMotion:'reduce'}),page=await context.newPage();
  const cdp=await context.newCDPSession(page);await cdp.send('Network.enable');
  let bytes=0,requests=0;const errors=[];
  cdp.on('Network.loadingFinished',e=>bytes+=e.encodedDataLength);
  cdp.on('Network.requestWillBeSent',()=>requests++);
  page.on('pageerror',e=>errors.push(String(e)));
  for(const mode of ['cold','warm']) {
   bytes=0;requests=0;
   const start=performance.now();
   await page.goto(url,{waitUntil:'networkidle',timeout:60000});
   await page.waitForFunction(()=>window.__JERUSALEM3000__?.status==='ready',{},{timeout:60000});
   samples.push({profile,mode,readyMs:Math.round(performance.now()-start),cdpEncodedBytes:bytes,requests,errors:[...errors],state:await page.evaluate(()=>({fullTimelineReady:window.__JERUSALEM3000__.fullTimelineReady??null,diagnostics:window.__JERUSALEM3000__.renderDiagnostics,resources:performance.getEntriesByType('resource').map(r=>({url:r.name,transferSize:r.transferSize,encodedBodySize:r.encodedBodySize,duration:r.duration}))}))});
  }
  const beforeBytes=bytes,beforeRequests=requests,transitions=[];
  for(const [value,phase] of [[3.9,'david-solomon'],[8.9,'herodian-jesus'],[3.9,'david-solomon'],[.9,'chalcolithic-early-bronze']]) {
   const start=performance.now();
   await page.locator('.j3k-scrubber').evaluate((el,v)=>{el.value=String(v);el.dispatchEvent(new Event('input',{bubbles:true}));},value);
   await page.waitForFunction(id=>document.querySelector('.j3k-stage')?.dataset.phase===id,phase);
   await page.evaluate(()=>new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve))));
   transitions.push({phase,stateAppliedMs:Math.round(performance.now()-start),diagnostics:await page.evaluate(()=>window.__JERUSALEM3000__.renderDiagnostics)});
  }
  samples.push({profile,mode:'cached-basic-era-roundtrip',additionalCdpEncodedBytes:bytes-beforeBytes,additionalRequests:requests-beforeRequests,transitions});
  await context.close();
 }
 const result={schema:'j3k.engineering-baseline.v1',url,measuredAt:new Date().toISOString(),environment:'local headless Chromium; real network, no throttling; mobile viewport is not a real phone',caveats:['CDP encoded bytes include protocol overhead and may include cache-related bytes.','readyMs includes networkidle wait; not first-interactive timing.','State application timing is not geometry-ready timing, FPS or p95.','No token/API cost measurement is available from this probe.'],samples};
 await writeFile(`${output}/baseline.json`,JSON.stringify(result,null,2));
 console.log(JSON.stringify(samples.map(({profile,mode,readyMs,cdpEncodedBytes,requests,additionalCdpEncodedBytes,additionalRequests,errors})=>({profile,mode,readyMs,cdpEncodedBytes,requests,additionalCdpEncodedBytes,additionalRequests,errors}))));
} finally {await browser.close();}
