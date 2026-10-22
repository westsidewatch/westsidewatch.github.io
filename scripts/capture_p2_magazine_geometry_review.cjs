#!/usr/bin/env node
/* Westside §6A / New Westside Editorial Web: rendered visual evidence.
   This is NOT a substitute for the award-level human art-direction review. */
'use strict';
const fs=require('node:fs');
const path=require('node:path');
const {chromium}=require('playwright');
const base='http://127.0.0.1:4173';
const out='artifacts/p2-magazine-visual';
const viewports=[['desktop',1648,928],['tablet',768,1024],['phone',390,844],['zoom-proxy',824,928]];
const shapes=['square','wide','full'];
fs.mkdirSync(out,{recursive:true});
function intersect(a,b){return a&&b?Math.max(0,Math.min(a.right,b.right)-Math.max(a.left,b.left))*Math.max(0,Math.min(a.bottom,b.bottom)-Math.max(a.top,b.top)):0}
(async()=>{
  const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
  const results=[];const failures=[];
  try{
    for(const [name,width,height] of viewports)for(const shape of shapes){
      const page=await browser.newPage({viewport:{width,height},reducedMotion:'reduce'});
      const errs=[];page.on('pageerror',e=>errs.push(e.message));
      const id=name+'-'+shape;
      try{
        const response=await page.goto(base+'/experiments/p2-magazine-art-direction-studio.html?view=geometry&shape='+shape,{waitUntil:'load',timeout:45000});
        await page.locator('#stage.geo').waitFor({state:'visible'});
        await page.evaluate(()=>document.fonts.ready);
        const m=await page.evaluate(()=>{
          const box=s=>{const r=document.querySelector(s)?.getBoundingClientRect();return r?{left:r.left,right:r.right,top:r.top,bottom:r.bottom,width:r.width,height:r.height}:null};
          const photo=document.querySelector('.geo__media img'),logo=document.querySelector('.geo__mast img'),li=document.querySelector('.geo__toc li');
          const font=s=>getComputedStyle(document.querySelector(s)).fontFamily;
          return {
            width:innerWidth,scrollWidth:document.documentElement.scrollWidth,
            photoCount:document.querySelectorAll('.geo__media img').length,
            photoDecoded:!!photo?.complete&&photo.naturalWidth>0,
            logoDecoded:!!logo?.complete&&logo.naturalWidth>0,
            image:box('.geo__media'),title:box('.geo__display'),
            contents:document.querySelectorAll('.geo__toc .issue-list li').length,
            movements:document.querySelectorAll('.geo__toc .movement-head').length,
            tocFontSize:li?parseFloat(getComputedStyle(li).fontSize):0,
            source:!!document.querySelector('.geo__source')?.textContent.includes('非考古實拍'),
            realCopy:!!document.querySelector('.geo__excerpt p')?.textContent.includes('人在曠野走了很久'),
            squareLink:!!document.querySelector('.geo__square-seal[href="#geo-contents"]'),
            englishFont:font('.geo__huge'),chineseFont:font('.geo__display h2')
          };
        });
        const defects=[];
        if(response.status()!==200)defects.push('HTTP_'+response.status());
        if(errs.length)defects.push('JS: '+errs.join(';'));
        if(m.scrollWidth>m.width+2)defects.push('HORIZONTAL_OVERFLOW');
        if(m.photoCount!==1||!m.photoDecoded||!m.logoDecoded)defects.push('ASSET_DECODE');
        if(m.contents!==12||m.movements!==4)defects.push('CANONICAL_CONTENTS');
        if(m.tocFontSize<14)defects.push('TOC_UNDER_14PX');
        if(!m.source||!m.realCopy)defects.push('PROVENANCE_OR_MANUSCRIPT');
        if(shape!=='full'&&intersect(m.image,m.title)>200)defects.push('IMAGE_TYPE_COLLISION');
        if(shape==='square'&&Math.abs(m.image.width/m.image.height-1)>.08)defects.push('SQUARE_RATIO');
        if(shape==='wide'&&Math.abs(m.image.width/m.image.height-1.95)>.1)defects.push('WIDE_RATIO');
        if(shape!=='square'&&!m.squareLink)defects.push('FOLIO_LINK');
        const screenshot=id+'.png';
        await page.screenshot({path:path.join(out,screenshot),fullPage:true,animations:'disabled'});
        results.push({id,shape,viewport:{width,height},metrics:m,screenshot,defects});
        if(defects.length)failures.push({id,defects});
        console.log(id+' '+(defects.length?'FAIL: '+defects.join(', '):'BROWSER-CONTRACT PASS'));
      }catch(e){console.error(id+' ERROR '+e.message);failures.push({id,defects:[e.message]})}
      finally{await page.close()}
    }
  }finally{await browser.close()}
  fs.writeFileSync(path.join(out,'manifest.json'),JSON.stringify({
    schema:'westside.magazine.visual-evidence.v1',commit:process.env.GITHUB_SHA,
    source:'PR-local Hugo preview',cases:results,failures,
    humanVisualReview:'PENDING',awardScore:'NOT SCORED',
    realBrowserZoom200:'NOT VERIFIED (824px case is only an effective viewport proxy)',
    finalPromotion:'BLOCKED UNTIL VISUAL SIGNOFF'
  },null,2)+'\n');
  console.log('Captured '+results.length+' screenshots; objective defects '+failures.length+'; artistic verdict NOT VERIFIED');
  if(failures.length)process.exitCode=1;
})().catch(e=>{console.error(e);process.exitCode=1});
