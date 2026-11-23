#!/usr/bin/env node
/**
 * Playback acceptance for the audience-facing cinema.
 * Only an authorized, real browser-tested film may enter screenings.json.
 * A smoke-test candidate is NEVER copied to the published catalog on failure.
 */
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { createServer } from 'node:http';
import { createRequire } from 'node:module';
import { once } from 'node:events';

const require = createRequire(import.meta.url);
const { chromium } = require(process.env.SHUPIAN_PLAYWRIGHT_MODULE || 'playwright');
const ROOT = process.cwd();
const PAGE = readFileSync(ROOT + '/static/shupian/index.html');
const CANDIDATES = JSON.parse(readFileSync(ROOT + '/scripts/shupian_recovery/authorized_candidates.json', 'utf8'));
const OUT = ROOT + '/static/shupian/screenings.json';
const REPORT = ROOT + '/reports/shupian-browser-acceptance.json';
const SCREENSHOT = ROOT + '/reports/shupian-browser-acceptance.png';
mkdirSync(ROOT + '/reports', { recursive: true });

if (!Array.isArray(CANDIDATES) || !CANDIDATES.length) throw Error('No authorized movie candidates');
if (CANDIDATES.some(x => x.licence?.spdx !== 'CC-BY-3.0' || !x.licence?.source || !x.licence?.attribution)) {
  throw Error('Missing explicit rights provenance; nothing may be published');
}
if (CANDIDATES.some(x => (x.episodes || []).some(ep => (ep.sources || []).some(s => !s.url?.startsWith('https://'))))) {
  throw Error('Invalid media address');
}

// This is used exclusively on the temporary CI server. It is not a public
// admission and is replaced by a real timestamp only after browser playback.
const STAGING = CANDIDATES.map(work => ({
  ...work,
  episodes:work.episodes.map(ep => ({
    ...ep,
    sources:ep.sources.map(s => ({
      ...s,
      playbackVerification:{
        status:'passed',videoStarted:true,seekSucceeded:true,
        observedAt:new Date().toISOString()
      }
    }))
  }))
}));
const server = createServer((req,res) => {
  const path = new URL(req.url, 'http://localhost').pathname;
  if (path === '/shupian/index.html' || path === '/shupian/') {
    res.writeHead(200,{'content-type':'text/html; charset=utf-8','cache-control':'no-store'});
    res.end(PAGE);return;
  }
  if (path === '/shupian/screenings.json') {
    res.writeHead(200,{'content-type':'application/json; charset=utf-8','cache-control':'no-store'});
    res.end(JSON.stringify(STAGING));return;
  }
  res.writeHead(404);res.end('Not Found');
});
server.listen(0,'127.0.0.1');
await once(server,'listening');
const origin = 'http://127.0.0.1:' + server.address().port;
const result = {status:'FAILED',checkedAt:new Date().toISOString(),browser:'chromium',films:[],reason:null};
let browser;
try{
  const config={headless:true,args:['--autoplay-policy=no-user-gesture-required']};
  if(process.env.SHUPIAN_CHROME_BIN)config.executablePath=process.env.SHUPIAN_CHROME_BIN;
  browser=await chromium.launch(config);
  const page=await browser.newPage({viewport:{width:1280,height:900}});
  const errors=[];
  page.on('pageerror',e => errors.push(String(e.message||e)));
  await page.goto(origin+'/shupian/index.html',{waitUntil:'domcontentloaded',timeout:30000});
  await page.locator('.card').first().waitFor({timeout:20000});
  if(await page.locator('.card').count()!==1)throw Error('Unexpected number of staged films');
  if(!(await page.locator('.card').first().innerText()).includes(CANDIDATES[0].title)){
    throw Error('Candidate absent from audience-facing film poster');
  }
  await page.locator('.card .poster').first().click();
  await page.locator('#player[open]').waitFor({timeout:10000});
  const player=page.locator('#video');
  await player.evaluate(async v => {
    v.muted=true;
    await v.play();
  });
  await page.waitForFunction(() => {
    const v=document.getElementById('video');
    return v && !v.paused && v.currentTime>=2 && v.videoWidth>0 && v.videoHeight>0;
  },null,{timeout:45000});
  const beforeSeek=await player.evaluate(v => ({
    time:v.currentTime,duration:v.duration,width:v.videoWidth,height:v.videoHeight
  }));
  if(!Number.isFinite(beforeSeek.duration)||beforeSeek.duration<30){
    throw Error('Invalid or incomplete video duration');
  }
  const seekTo=Math.min(120,Math.floor(beforeSeek.duration/2));
  await player.evaluate(async (target) => {
    const v=document.getElementById('video');
    await new Promise((resolve,reject) => {
      const timer=setTimeout(() => reject(Error('Seek timed out')),30000);
      v.addEventListener('seeked',()=>{clearTimeout(timer);resolve()}, {once:true});
      v.currentTime=target;
    });
    await v.play();
  },seekTo);
  await page.waitForFunction(target => {
    const v=document.getElementById('video');
    return v && !v.paused && v.currentTime>=target+2 && v.videoWidth>0;
  },seekTo,{timeout:45000});
  if(errors.length)throw Error('Browser script error: '+errors.join('; ').slice(0,300));
  await page.screenshot({path:SCREENSHOT,fullPage:true});
  const verifiedAt=new Date().toISOString();
  const approved=CANDIDATES.map(work => ({
    ...work,
    episodes:work.episodes.map(ep => ({
      ...ep,
      sources:ep.sources.map(src => ({
        ...src,
        playbackVerification:{
          status:'passed',videoStarted:true,seekSucceeded:true,
          observedAt:verifiedAt,tool:'chromium-playwright'
        }
      }))
    }))
  }));
  // Exact film/episode that played is eligible; do not silently certify
  // additional candidates without testing each one.
  if(approved.length!==1 || approved[0].episodes.length!==1 ||
     approved[0].episodes[0].sources.length!==1){
    throw Error('More than one candidate needs independent playback verification');
  }
  writeFileSync(OUT,JSON.stringify(approved,null,2)+'\n');
  result.status='PASSED';
  result.checkedAt=verifiedAt;
  result.films=[{id:approved[0].id,videoStarted:true,seekSucceeded:true,
    durationSec:beforeSeek.duration,dimensions:[beforeSeek.width,beforeSeek.height],
    verifiedAt,license:approved[0].licence.spdx}];
  console.log('Audience playback passed; approved 1 film after real-time + seek tests.');
}catch(e){
  result.reason=String(e?.message||e);
  console.error('Playback acceptance failed; public catalog unchanged:',result.reason);
  process.exitCode=1;
}finally{
  writeFileSync(REPORT,JSON.stringify(result,null,2)+'\n');
  if(browser)await browser.close();
  server.close();
}
