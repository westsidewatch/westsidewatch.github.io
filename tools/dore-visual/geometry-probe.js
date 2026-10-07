#!/usr/bin/env node
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const baseUrl = process.argv[2];
if (!baseUrl) throw new Error('usage: node tools/dore-visual/geometry-probe.js <base-url>');

const registry = JSON.parse(fs.readFileSync('tools/dore-visual/contracts.json','utf8'));
const viewports = registry.viewports;

(async()=>{
 const browser=await chromium.launch({headless:true});
 const artifactRoot=process.env.DORE_VISUAL_ARTIFACTS||'artifacts/dore-visual';
 fs.mkdirSync(artifactRoot,{recursive:true});
 let failed=false;
 for(const contract of registry.contracts){
  if(contract.probe!=='candidate01') continue;
  const url=new URL(contract.path,baseUrl).href;
  for(const viewport of viewports){
   const page=await browser.newPage({viewport:{width:viewport.width,height:viewport.height},reducedMotion:'no-preference'});
   await page.goto(url,{waitUntil:'networkidle'});
   // Probe a generic Candidate card, not ONE: ONE has its own second-level
   // reading transition and would contaminate the four-card geometry contract.
   const card=page.locator('.products__grid .product:not([data-source="ONE"])').first();
   // Animated targets never become "stable"; move the real pointer to the
   // current rendered centre instead of using Playwright's stability-gated hover().
   const box=await card.boundingBox();
   if(!box) throw new Error('Candidate 01 hover target missing');
   await page.mouse.move(box.x+box.width/2,box.y+box.height/2);
   await page.waitForTimeout(750);
   const report=await page.evaluate(()=>{
     const rect=e=>{const r=e.getBoundingClientRect();return {top:r.top,bottom:r.bottom,left:r.left,right:r.right,width:r.width,height:r.height,ratio:r.width/r.height}};
     const preview=[...document.querySelectorAll('.product-preview')].find(e=>getComputedStyle(e).opacity!=='0')||document.querySelector('.product-preview');
     const all=[...document.querySelectorAll('.products__grid .product')];
     const pr0=preview?rect(preview):null;
     // Measure the four small cards on the side opposite the active preview.
     // Focus animations can enlarge/move covered cards, so "first four DOM nodes"
     // is not a valid visual group.
     const candidates=pr0 ? all.map(e=>({e,r:rect(e)})).filter(x=>
       pr0.left > innerWidth/2 ? x.r.right <= innerWidth/2+4 : x.r.left >= innerWidth/2-4
     ) : [];
     const cards=candidates.slice(0,4).map(x=>x.e);
     if(cards.length<4||!preview) return {error:'Candidate 01 targets missing'};
     const cr=cards.map(rect), pr=rect(preview);
     const group={top:Math.min(...cr.map(r=>r.top)),bottom:Math.max(...cr.map(r=>r.bottom))};
     const animations=cards.map(e=>getComputedStyle(e).animationName);
     return {preview:pr,cards:cr,deltaTop:pr.top-group.top,deltaBottom:pr.bottom-group.bottom,animations};
   });
   const desktopContract=viewport.width>=901;
   const ok=!report.error && (!desktopContract || (
     Math.abs(report.deltaTop)<=2 && Math.abs(report.deltaBottom)<=2 &&
     Math.abs(report.preview.ratio-1.6)<=0.01 && report.cards.every(r=>Math.abs(r.ratio-1.6)<=0.01) &&
     report.animations.some(x=>x&&x!=='none')
   ));
   const artifactDir=path.join(artifactRoot,contract.id);
   fs.mkdirSync(artifactDir,{recursive:true});
   const stem=viewport.name.replace(/[^a-z0-9_-]/gi,'-');
   await page.screenshot({path:path.join(artifactDir,stem+'.png'),fullPage:true});
   fs.writeFileSync(path.join(artifactDir,stem+'.json'),JSON.stringify({contract:contract.id,viewport,...report,pass:ok},null,2));
   console.log(JSON.stringify({contract:contract.id,viewport,...report,pass:ok},null,2));
   if(!ok) failed=true;
   await page.close();
  }
 }
 await browser.close();
 process.exit(failed?1:0);
})().catch(e=>{console.error(e);process.exit(2)});
