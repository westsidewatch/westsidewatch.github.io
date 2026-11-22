/* Dawn P2 05 Design OS browser acceptance, not token-stub grep.
 * Run against the built static site on http://127.0.0.1:4173.
 */
'use strict';
const {chromium}=require('playwright'),assert=require('node:assert/strict');
const fs=require('node:fs'),path=require('node:path');
const out='artifacts/p2-dawn-os-repair';fs.mkdirSync(out,{recursive:true});
(async()=>{
 const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
 try{
  for(const [device,width,height] of [['desktop',1440,900],['phone',390,844]]){
   const page=await browser.newPage({viewport:{width,height},deviceScaleFactor:1});
   const errors=[];page.on('pageerror',error=>errors.push(error.message));
   await page.goto('http://127.0.0.1:4173/experiments/p2-0105-dawn-preview.html?layer=second&d=28.4&v=os-r57',
    {waitUntil:'domcontentloaded',timeout:45000});
   await page.locator('#dawn-second .dawn-reading-room__masthead').waitFor({state:'visible',timeout:20000});
   await page.evaluate(()=>document.fonts.ready);
   await page.waitForFunction(()=>document.querySelectorAll('#dawn-wall-grid button.dawn-cover').length>=12,
    null,{timeout:35000});
   const openingTitles=await page.locator('#dawn-wall-grid button.dawn-cover')
    .evaluateAll(tiles=>tiles.slice(0,4).map(tile=>tile.dataset.workTitle));
   assert(!openingTitles.some(title=>/Confessions of Zeno|The Duke of York’s Steps|A Fighting Man of Mars/.test(title)),
    device+': generic fiction unexpectedly dominates gospel library entrance');
   assert(openingTitles.some(title=>/Bible|history|church/i.test(title)),
    device+': no source-backed Biblical or church-history Works in opening selection');
   const result=await page.evaluate(()=>{
    const grab=s=>{const el=document.querySelector(s);if(!el)throw Error('Missing '+s);
      const st=getComputedStyle(el),r=el.getBoundingClientRect();
      return {font:st.fontFamily,size:parseFloat(st.fontSize),weight:parseInt(st.fontWeight,10),
       x:r.x,y:r.y,right:r.right,bottom:r.bottom,width:r.width,height:r.height,
       display:st.display,position:st.position}
    };
    return {
      nav:grab('.dawn-second__global-nav'),
      returnEn:grab('.dawn-second__return .dawn-second__nav-en'),
      returnZh:grab('.dawn-second__return .dawn-second__nav-zh'),
      collectionEn:grab('.dawn-second__all-works .dawn-second__nav-en'),
      collectionZh:grab('.dawn-second__all-works .dawn-second__nav-zh'),
      personalEn:grab('.dawn-second__personal .dawn-second__nav-en'),
      featureEn:grab('#dawn-wall-grid .dawn-feature__titles em'),
      featureZh:grab('#dawn-wall-grid .dawn-feature__titles strong'),
      missingCoverCSS:(()=>{
       const sheet=document.createElement('button');
       sheet.className='dawn-cover dawn-cover--missing';
       sheet.innerHTML='<span class="dawn-cover__meta"><strong>Real source title</strong></span>';
       sheet.style.cssText='position:absolute;width:210px;height:210px;visibility:hidden';
       document.querySelector('#dawn-wall-grid').append(sheet);
       const meta=sheet.querySelector('.dawn-cover__meta');
       const value={tileDisplay:getComputedStyle(sheet).display,opacity:getComputedStyle(meta).opacity,
        copy:getComputedStyle(meta).color};
       sheet.remove();return value;
      })(),
      personalLabelBackground:getComputedStyle(document.querySelector('.dawn-second__personal>.dawn-second__nav-en')).backgroundColor,
      loadedCoverCSS:(()=>{
       const cover=document.createElement('button');
       cover.className='dawn-wall__tile dawn-cover dawn-cover--ready';
       cover.style.cssText='position:absolute;width:210px;height:210px;visibility:hidden';
       const meta=document.createElement('span');meta.className='dawn-cover__meta';
       const title=document.createElement('strong');title.textContent='A genuine title';
       meta.append(title);cover.append(meta);
       document.querySelector('#dawn-wall-grid').append(cover);
       const cs=getComputedStyle(meta),ts=getComputedStyle(title);
       const value={opacity:cs.opacity,color:ts.color,font:ts.fontFamily};
       cover.remove();return value;
      })(),
      mastEn:grab('#dawn-room-heading > span'),
      mastZh:grab('#dawn-room-heading > strong'),
      lead:grab('.dawn-reading-room__lead'),
      gallery:grab('#dawn-wall-grid'),
      source:grab('#dawn-second'),
      departmentZh:grab('.dawn-reading-room__departments-intro h3 > strong'),
      departmentEn:grab('.dawn-reading-room__departments-intro h3 > span'),
      mast:grab('.dawn-reading-room__masthead')
    };
   });
   for(const [id,en,zh] of [['return',result.returnEn,result.returnZh],
      ['collection',result.collectionEn,result.collectionZh]]){
     assert(en.size>zh.size*1.25,device+': '+id+' English is not larger than Chinese');
     assert(/Bodoni/i.test(en.font),device+': '+id+' English family is not OS Bodoni: '+en.font);
     assert(/Chiron/i.test(zh.font),device+': '+id+' Chinese family is not OS Chiron: '+zh.font);
     assert.equal(zh.weight,200,device+': '+id+' Chinese helper is not 200');
   }
   assert(result.featureEn.size>result.featureZh.size*1.18,
    device+': editorial cover portal still uses oversized Chinese and tiny English');
   assert.equal(result.featureZh.weight,200,
    device+': three feature portal Chinese labels must be 200');
   assert(result.personalLabelBackground==='rgba(0, 0, 0, 0)'||
     result.personalLabelBackground==='transparent',
     device+': old personal counter pill behind English navigation text');
   assert(result.missingCoverCSS.tileDisplay!=='none'&&result.missingCoverCSS.opacity==='1',
     device+': missing jackets still disappear or become blank grid swatches');
   assert(result.loadedCoverCSS.opacity==='1'&&
     !['rgb(255, 255, 255)','white'].includes(result.loadedCoverCSS.color),
     device+': loaded source cards hide their title or print it in white on paper');
   assert(result.mastEn.size>result.mastZh.size*1.28,
    device+': English masthead is not dominant');
   assert(result.mastEn.font.includes('Bodoni'),device+': main masthead missing Bodoni');
   assert(result.mastZh.font.includes('Chiron'),device+': Chinese masthead missing Chiron');
   assert.equal(result.mastZh.weight,900,device+': principal Chinese title must preserve anchor weight');
   assert.equal(result.lead.weight,200,device+': prose must be Chinese air weight');
   assert.equal(result.departmentZh.weight,200,device+': secondary Chinese heading must be air');
   assert(result.departmentEn.size>result.departmentZh.size,device+': department heading scale reversed');
   assert(result.nav.height<180,device+': navigation behaves like a giant toolbar');
   assert(result.nav.position!=='fixed',device+': toolbar stuck over composition');
   assert(result.gallery.width>width*.65,device+': gallery contracted off canvas');
   assert(result.gallery.height>120,device+': source image wall collapsed');
   assert(result.mast.height<480,device+': oversized empty header carrier');
   const overWidth=await page.evaluate(()=>document.querySelector('#dawn-second').scrollWidth-document.querySelector('#dawn-second').clientWidth);
   assert(overWidth<18,device+': horizontal overflow '+overWidth);
   await page.screenshot({path:path.join(out,device+'-os-navigation-masthead.png'),fullPage:false});
   await page.locator('#dawn-wall-grid').scrollIntoViewIfNeeded();
   await page.screenshot({path:path.join(out,device+'-os-original-gallery.png'),fullPage:false});
   assert.equal(errors.length,0,device+': runtime errors '+errors.join('; '));
   console.log('DAWN_OS',device,'NAV_EN_GT_ZH_CHIRON_200_BODONI_MASTHEAD_GALLERY_PASS',
    JSON.stringify({navHeight:result.nav.height,mastHeight:result.mast.height,
      en:result.mastEn.size,zh:result.mastZh.size,overflow:overWidth}));
   await page.close();
  }
 }finally{await browser.close()}
})().catch(err=>{console.error(err);process.exitCode=1});
