#!/usr/bin/env node
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const baseUrl = process.argv[2];
if (!baseUrl) throw new Error('usage: node tools/dore-visual/geometry-probe.js <base-url>');

const registry = JSON.parse(fs.readFileSync('tools/dore-visual/contracts.json','utf8'));
const required=registry.schema?.contractRequired||['id','path','probe','required'];
const supportedRules=new Set(registry.schema?.supportedRules||[]);
const supportedStates=new Set(registry.schema?.supportedStates||[]);
const ids=new Set();
for(const contract of registry.contracts||[]){
  const missing=required.filter(k=>contract[k]===undefined||contract[k]===null||contract[k]==='');
  if(missing.length) throw new Error(`invalid visual contract ${contract.id||'<unnamed>'}: missing ${missing.join(', ')}`);
  if(ids.has(contract.id)) throw new Error(`duplicate visual contract id: ${contract.id}`);
  ids.add(contract.id);
  for(const key of Object.keys(contract.rules||{})) if(supportedRules.size&&!supportedRules.has(key)) throw new Error(`unsupported rule "${key}" in ${contract.id}`);
  for(const state of contract.states||[]) for(const key of Object.keys(state)) if(key!=='name'&&supportedStates.size&&!supportedStates.has(key)) throw new Error(`unsupported state field "${key}" in ${contract.id}`);
}
const viewports = registry.viewports;

(async()=>{
 const browser=await chromium.launch({headless:true});
 const artifactRoot=process.env.DORE_VISUAL_ARTIFACTS||'artifacts/dore-visual';
 fs.mkdirSync(artifactRoot,{recursive:true});
 let failed=false;
 for(const contract of registry.contracts){
  if(!['candidate01','homepage'].includes(contract.probe)) continue;
  const url=new URL(contract.path,baseUrl).href;
  for(const viewport of viewports){
   for(const state of (contract.states||[{name:'default'}])){
   const page=await browser.newPage({viewport:{width:viewport.width,height:viewport.height},reducedMotion:state.reducedMotion||'no-preference'});
   await page.goto(url,{waitUntil:'networkidle'});
   // Probe a generic Candidate card, not ONE: ONE has its own second-level
   // reading transition and would contaminate the four-card geometry contract.
   if(contract.probe==='homepage'){
     await page.waitForTimeout(1400);
     const report=await page.evaluate(()=>{
       const rect=s=>{const e=document.querySelector(s);if(!e)return null;const r=e.getBoundingClientRect();return {top:r.top,bottom:r.bottom,left:r.left,right:r.right,width:r.width,height:r.height}};
       const hero=rect('.sites-home-hero'), masthead=rect('.sites-home-masthead'), intro=rect('.sites-home-intro'), nav=rect('.sites-home-nav'), entry=rect('.sites-home-entry');
       const animations=[...document.querySelectorAll('.sites-home-masthead,.sites-home-intro,.sites-home-entry')].map(e=>getComputedStyle(e).animationName);
       return {hero,masthead,intro,nav,entry,animations};
     });
     const required=[report.hero,report.masthead,report.intro,report.nav,report.entry];
     const inside=required.every(Boolean)&&report.masthead.left>=report.hero.left&&report.intro.left>=report.hero.left&&report.nav.right<=report.hero.right+2&&report.entry.right<=report.hero.right+2;
     const reduced=state.reducedMotion==='reduce';
     const motionOk=reduced?report.animations.every(x=>!x||x==='none'):report.animations.some(x=>x&&x!=='none');
     const ok=inside&&motionOk;
     const artifactDir=path.join(artifactRoot,contract.id); fs.mkdirSync(artifactDir,{recursive:true});
     const stem=(viewport.name+'--'+state.name).replace(/[^a-z0-9_-]/gi,'-');
     await page.screenshot({path:path.join(artifactDir,stem+'.png'),fullPage:true});
     fs.writeFileSync(path.join(artifactDir,stem+'.json'),JSON.stringify({contract:contract.id,state:state.name,viewport,...report,pass:ok},null,2));
     console.log(JSON.stringify({contract:contract.id,state:state.name,viewport,...report,pass:ok},null,2));
     if(!ok) failed=true;
     await page.close();
     continue;
   }
   const card=page.locator(state.target||'.products__grid .product:not([data-source="ONE"])').first();
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
   const rules=contract.rules||{};
   const tolerancePx=rules.geometry?.tolerancePx??registry.defaults?.tolerancePx??2;
   const ratioTolerance=rules.aspectRatio?.tolerance??registry.defaults?.aspectRatioTolerance??0.01;
   const previewRatio=rules.aspectRatio?.preview??1.6;
   const cardRatio=rules.aspectRatio?.cards??1.6;
   const desktopContract=viewport.width>=(registry.defaults?.desktopMinWidth??901);
   const reduced=state.reducedMotion==='reduce';
   const geometryOk=!report.error &&
     Math.abs(report.deltaTop)<=tolerancePx && Math.abs(report.deltaBottom)<=tolerancePx &&
     Math.abs(report.preview.ratio-previewRatio)<=ratioTolerance &&
     report.cards.every(r=>Math.abs(r.ratio-cardRatio)<=ratioTolerance);
   const motionOk=!report.error && (reduced
     ? (rules.motion?.reduced??'none')==='none' && report.animations.every(x=>!x||x==='none')
     : (rules.motion?.normal??'present')==='present' && report.animations.some(x=>x&&x!=='none'));
   const ok=!desktopContract ? true : geometryOk && motionOk;
   const artifactDir=path.join(artifactRoot,contract.id);
   fs.mkdirSync(artifactDir,{recursive:true});
   const stem=(viewport.name+'--'+state.name).replace(/[^a-z0-9_-]/gi,'-');
   await page.screenshot({path:path.join(artifactDir,stem+'.png'),fullPage:true});
   fs.writeFileSync(path.join(artifactDir,stem+'.json'),JSON.stringify({contract:contract.id,state:state.name,viewport,...report,pass:ok},null,2));
   console.log(JSON.stringify({contract:contract.id,state:state.name,viewport,...report,pass:ok},null,2));
   if(!ok) failed=true;
   await page.close();
   }
  }
 }
 await browser.close();
 process.exit(failed?1:0);
})().catch(e=>{console.error(e);process.exit(2)});
