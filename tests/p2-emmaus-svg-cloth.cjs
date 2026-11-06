'use strict';
/* Fourth requested item: vectorize P2 03 Emmaus Scripture's fabric cover.
 * Verify one newly authored 5:8 native SVG across the real book, turning
 * underleaf, exterior and 03→04 carrier WITHOUT changing canonical /one/.
 */
const fs=require('node:fs'),assert=require('node:assert/strict'),path=require('node:path');
const {chromium}=require('playwright');
const asset=fs.readFileSync('static/images/p2-emmaus-binding-cloth-v1.svg','utf8');
const book=fs.readFileSync('static/css/p2-emmaus-bookbinding-v7.css','utf8');
const release=fs.readFileSync('static/js/p2-0103-release.js','utf8');
const transition=fs.readFileSync('static/css/p2-0104-olive-continuation.css','utf8');
const html=fs.readFileSync('static/experiments/p2-0103-release.html','utf8');
const link='p2-emmaus-binding-cloth-v1.svg';
assert.match(asset,/<svg[^>]*viewBox="0 0 640 1024"/);
assert.equal((asset.match(/<pattern\b/g)||[]).length,4);
assert(!/<image\b|<linearGradient\b|<filter\b|xlink:href/.test(asset));
assert((book.match(/p2-emmaus-binding-cloth-v1\.svg/g)||[]).length>=5);
assert((release.match(/p2-emmaus-binding-cloth-v1\.svg/g)||[]).length>=2);
assert(transition.includes(link),'MERSI 03→04 bridge must preserve ONE cloth');
assert(html.includes('20261106-vector-cloth-v1'),'actual release must load new CSS');
assert(html.includes('20261106-vector-cloth-turn-v1'),'actual release must load new turn');
assert(!/cover-texture-antique-green\.png\?v=93ae0c7e0609/.test(book+release+transition));
(async()=>{
 const browser=await chromium.launch({headless:true});
 try{
  const dir='artifacts/p2-0104-olive';fs.mkdirSync(dir,{recursive:true});
  for(const [width,height] of [[1648,928],[390,844]]){
   const page=await browser.newPage({viewport:{width,height}});
   const errors=[];page.on('pageerror',e=>errors.push(String(e)));
   await page.goto('http://127.0.0.1:4173/experiments/p2-0103-release.html',
    {waitUntil:'domcontentloaded',timeout:45000});
   await page.waitForFunction(()=>!!document.querySelector('#emmaus .emmaus__entry-cover-leaf'),null,{timeout:20000});
   await page.evaluate(()=>{const track=document.querySelector('#proof-track');
     scrollTo({top:track.getBoundingClientRect().top+scrollY+7.30*innerHeight,behavior:'instant'});
   });
   await page.waitForFunction(()=>document.querySelector('#emmaus')?.dataset.coverState==='green',null,{timeout:20000});
   const result=await page.evaluate(async()=>{
    const d=document,cover=d.querySelector('#emmaus .emmaus__entry-cover-leaf');
    const outer=d.querySelector('#emmaus > .emmaus__right > .emmaus__entry-cover');
    const texture=d.querySelector('#p2-realm-background[data-realm="bible"]');
    const u='/images/p2-emmaus-binding-cloth-v1.svg?v=20261106-gilt-weave';
    const response=await fetch(u);
    const source=await response.text();
    const xml=new DOMParser().parseFromString(source,'image/svg+xml');
    return {
      code:response.status,xml:!xml.querySelector('parsererror'),
      patterns:xml.querySelectorAll('pattern').length,
      front:getComputedStyle(cover).backgroundImage,
      outer:getComputedStyle(outer).backgroundImage,
      exterior:texture?getComputedStyle(texture).backgroundImage:'',
      state:d.querySelector('#emmaus').dataset.coverState,
      rect:{w:cover.getBoundingClientRect().width,h:cover.getBoundingClientRect().height}
    };
   });
   assert.equal(result.code,200,'SVG fetch must succeed in the built P2 preview');
   assert.equal(result.xml,true,'SVG must be parseable');
   assert.equal(result.patterns,4);
   assert(result.front.includes(link),'actual green cover MUST show SVG cloth');
   assert(result.outer.includes(link),'outbound face MUST show SVG cloth');
   assert.equal(result.state,'green','cover is the paused approved first turn');
   assert(!errors.length,'real bookturn JS errors '+errors.join(' / '));
   await page.screenshot({path:path.join(dir,`${width}-emmaus-svg-cloth-green-hold.png`),animations:'disabled'});
   console.log('EMMAUS SVG CLOTH PASS',width,JSON.stringify(result));
   await page.close();
  }
 }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
