'use strict';
/* P2 04 CLEAN FIELD regression.
 * Approved 03 Emmaus and its 5:8 cloth must remain untouched.
 * Only the 04 full-stage engraving was retired; the V13 card headpiece
 * and original twelve composites stay protected. */
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const {chromium}=require('playwright');
const root=path.resolve(__dirname,'..');
const read=p=>fs.readFileSync(path.join(root,p),'utf8');
const html=read('static/experiments/p2-0104-olive-continuation.html');
const css=read('static/css/p2-0104-olive-continuation.css');
const js=read('static/js/p2-0104-olive-continuation.js');
assert.match(html,/p2-0103-release\.html\?embed=1/);
assert.match(html,/olive-speaker-baseline|baseline\.js/);
assert.doesNotMatch(html,/id="olive-growth-field"/);
assert.doesNotMatch(js,/fetch\(['"]\/images\/p2-realms\/v15\/04-olive-hillside/);
assert.doesNotMatch(js,/requestAnimationFrame\(livingFrame\)/);
assert.doesNotMatch(css,/04-olive-woodward-cousen-(desktop|mobile)-intaglio-v44/);
assert.match(css,/\.olive-surround__half\{[^}]*background-color:var\(--ws-olive\);[^}]*background-image:none;/s);
assert.match(css,/\.olive-card__relief::after\{/,'invitation local relief retained');
assert.match(js,/frozen\.mount\(art,target\)/,'frozen poster typography retained');
assert.match(js,/const readingField=ease\(\(d-T\.first\)\/\.065\);/,
  'original Emmaus handoff timing unchanged');
assert.match(read('static/experiments/p2-0103-release.html'),/p2-emmaus-bookbinding-v7\.css/,
  'genuine Emmaus iframe still retains the original binding stylesheet');
const widths=[1648,390];
(async()=>{
 const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
 try{
  for(const width of widths){
   const page=await browser.newPage({viewport:{width,height:width===1648?928:844},deviceScaleFactor:1});
   const errors=[],oliveRequests=[];
   page.on('pageerror',e=>errors.push(e.message));
   page.on('request',r=>{if(/04-olive-(?:hillside-copperplate|living-grove|woodward-cousen|growth-field)/.test(r.url()))oliveRequests.push(r.url())});
   await page.goto('http://127.0.0.1:4173/experiments/p2-0104-olive-continuation.html?d=9.30',
    {waitUntil:'domcontentloaded'});
   await page.waitForFunction(()=>document.querySelector('#p2-olive-stage')?.dataset.p2FolioReady==='true',{timeout:20000});
   async function go(d,name){
    await page.evaluate(d=>{const t=document.querySelector('#p2-olive-track');scrollTo(0,t.getBoundingClientRect().top+scrollY+d*innerHeight)},d);
    await page.waitForFunction(d=>Math.abs(Number(document.querySelector('#p2-olive-stage').dataset.p2Distance)-d)<.025,d,{timeout:12000});
    const state=await page.evaluate(()=>{
     const stage=document.querySelector('#p2-olive-stage');
     const bg=document.querySelector('#p2-olive-surround');
     const head=document.querySelector('#p2-0103-original');
     return {scene:stage.dataset.p2Scene,
       source:getComputedStyle(head).visibility,
       ground:getComputedStyle(bg).visibility,
       noGrowth:document.querySelector('#olive-growth-field')===null,
       posterNodes:document.querySelectorAll('.olive-stage__index-card').length,
       bgImages:[...bg.querySelectorAll('.olive-surround__half')].map(el=>getComputedStyle(el).backgroundImage),
       bgPseudo:[...bg.querySelectorAll('.olive-surround__half')].map(el=>getComputedStyle(el,'::after').content)};
    });
    await page.screenshot({path:`artifacts/p2-0104-olive/${width}-${name}.png`,animations:'disabled'});
    return state;
   }
   await page.evaluate(()=>document.fonts.ready);
   const src=await go(9.30,'00-original-emmaus');
   assert.equal(src.source,'visible','03 original iframe visible before entry');
   const pair=await go(10.98,'03-two-poster-locked-original-background');
   const mid=await go(13.15,'04-clean-olive-field');
   assert.equal(mid.noGrowth,true,'04 growth SVG must not be in the DOM');
   assert.equal(mid.posterNodes,12,'all twelve source composites still exist');
   assert(mid.bgImages.every(x=>x==='none'),'04 background must have no image');
   assert(mid.bgPseudo.every(x=>x==='none'),'04 background must have no pseudo-image');
   const end=await go(16.70,'09-twelve-voices-final-overview');
   assert.equal(end.posterNodes,12);
   const back=await go(9.30,'10-reversed-original-emmaus');
   assert.equal(back.source,'visible','reverse scrolling restores 03 original');
   assert.deepEqual(oliveRequests,[],'retired 04 background SVGs must never be fetched');
   assert.deepEqual(errors,[],'browser must be free of page errors');
   console.log('P2 04 CLEAN FIELD PASS',width,JSON.stringify({pair:pair.scene,clean:mid.scene,index:end.scene,reverse:back.scene}));
   await page.close();
  }
 }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
