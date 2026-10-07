#!/usr/bin/env node
const { chromium } = require('playwright');

const url = process.argv[2];
if (!url) throw new Error('usage: node tools/dore-visual/geometry-probe.js <url>');

const viewports = [
  { name:'desktop-16x9', width:1920, height:1080 },
  { name:'desktop-16x10', width:1680, height:1050 },
  { name:'laptop', width:1440, height:900 },
  { name:'tablet', width:1024, height:768 }
];

(async()=>{
 const browser=await chromium.launch({headless:true});
 let failed=false;
 for(const viewport of viewports){
   const page=await browser.newPage({viewport:{width:viewport.width,height:viewport.height},reducedMotion:'no-preference'});
   await page.goto(url,{waitUntil:'networkidle'});
   const card=page.locator('.products__grid .product').first();
   // Animated targets never become "stable"; move the real pointer to the
   // current rendered centre instead of using Playwright's stability-gated hover().
   const box=await card.boundingBox();
   if(!box) throw new Error('Candidate 01 hover target missing');
   await page.mouse.move(box.x+box.width/2,box.y+box.height/2);
   await page.waitForTimeout(750);
   const report=await page.evaluate(()=>{
     const rect=e=>{const r=e.getBoundingClientRect();return {top:r.top,bottom:r.bottom,left:r.left,right:r.right,width:r.width,height:r.height,ratio:r.width/r.height}};
     const cards=[...document.querySelectorAll('.products__grid .product')].slice(0,4);
     const preview=[...document.querySelectorAll('.product-preview')].find(e=>getComputedStyle(e).opacity!=='0')||document.querySelector('.product-preview');
     if(cards.length<4||!preview) return {error:'Candidate 01 targets missing'};
     const cr=cards.map(rect), pr=rect(preview);
     const group={top:Math.min(...cr.map(r=>r.top)),bottom:Math.max(...cr.map(r=>r.bottom))};
     const animations=cards.map(e=>getComputedStyle(e).animationName);
     return {preview:pr,cards:cr,deltaTop:pr.top-group.top,deltaBottom:pr.bottom-group.bottom,animations};
   });
   const ok=!report.error && Math.abs(report.deltaTop)<=2 && Math.abs(report.deltaBottom)<=2 &&
     Math.abs(report.preview.ratio-1.6)<=0.01 && report.cards.every(r=>Math.abs(r.ratio-1.6)<=0.01) &&
     report.animations.some(x=>x&&x!=='none');
   console.log(JSON.stringify({viewport,...report,pass:ok},null,2));
   if(!ok) failed=true;
   await page.close();
 }
 await browser.close();
 process.exit(failed?1:0);
})().catch(e=>{console.error(e);process.exit(2)});
