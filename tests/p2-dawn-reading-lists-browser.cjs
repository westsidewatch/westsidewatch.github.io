'use strict';
const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs'),path=require('node:path');
const out=path.join('artifacts','p2-dawn-reading-lists');
fs.mkdirSync(out,{recursive:true});
const cases=[['gospel-essentials',6,1],['inner-life',9,0],['church-history',7,0]];
(async()=>{
 const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
 const results=[];
 try{
  for(const [device,width,height] of [['desktop',1440,900],['phone',390,844]]){
   const page=await browser.newPage({viewport:{width,height},reducedMotion:'reduce'});
   const errors=[];page.on('pageerror',err=>errors.push(err.message));
   try{
    const response=await page.goto('http://127.0.0.1:4173/experiments/p2-0105-dawn-preview.html?layer=second&d=28.4&native-list=1',
      {waitUntil:'domcontentloaded',timeout:45000});
    assert.equal(response?.status(),200,device+': P2 05 preview missing');
    const section=page.locator('.dawn-reading-room__reading-lists');
    await section.waitFor({state:'visible',timeout:30000});
    assert.equal(await section.locator('button[data-dawn-reading-list]').count(),3,device+': all three lists needed');
    assert.equal(await page.locator('#dawn-wall-grid .dawn-feature').count(),3,device+': original editorial portal missing');
    assert.equal(await page.locator('.dawn-second__motherform').count(),1,device+': original Scripture Studio removed');
    await section.scrollIntoViewIfNeeded();
    const style=await section.evaluate(el=>{
      const title=el.querySelector('h2'),s=getComputedStyle(title);
      return {font:s.fontFamily,weight:s.fontWeight,bg:getComputedStyle(el).backgroundColor,
        clip:el.scrollWidth-el.clientWidth, viewport:document.querySelector('#dawn-second').clientWidth,
        pageOverflow:document.querySelector('#dawn-second').scrollWidth-document.querySelector('#dawn-second').clientWidth};
    });
    assert(/Chiron/i.test(style.font),device+': original Design OS Chinese type removed '+style.font);
    assert(style.pageOverflow<18,device+': second layer horizontal overflow '+style.pageOverflow);
    await page.screenshot({path:path.join(out,device+'-native-reading-contents.png'),animations:'disabled',timeout:30000});
    for(const [slug,count,bookIndex] of cases){
      await page.locator('button[data-dawn-reading-list="'+slug+'"]').click();
      await page.waitForFunction(n=>document.querySelectorAll('#dawn-works button.dawn-catalogue__cover-card').length===n,count,{timeout:30000});
      assert(await page.locator('#dawn-catalogue').isVisible(),device+': native catalogue did not open for '+slug);
      assert(await page.locator('#dawn-catalogue__reading-index').count()===0,'No parallel selector ID allowed');
      assert.equal(await page.locator('.dawn-catalogue__reading-index button').count(),3,device+': same folio list switching missing');
      assert(await page.locator('#dawn-catalogue-introduction').isVisible(),device+': reading guide not in original editorial area');
      const guide=await page.locator('#dawn-catalogue-introduction').innerText();
      assert(guide.includes('閱讀次序：'),device+': source-selected reading sequence absent');
      const card=page.locator('#dawn-works button.dawn-catalogue__cover-card').nth(bookIndex);
      await card.scrollIntoViewIfNeeded();
      const visualTitle=await card.locator('.dawn-catalogue__cover-typography>strong').evaluate(el=>{
        const box=el.getBoundingClientRect(),style=getComputedStyle(el);
        return {text:el.textContent?.trim(),height:box.height,font:style.fontFamily,color:style.color,opacity:style.opacity};
      });
      assert(visualTitle.text.length>1&&visualTitle.height>15&&visualTitle.opacity!=='0'&&/Chiron/i.test(visualTitle.font),
        device+': actual Chinese book title is invisible '+slug+' '+JSON.stringify(visualTitle));
      await page.screenshot({path:path.join(out,device+'-'+slug+'-bookwall.png'),animations:'disabled',timeout:30000});
      await card.click();
      await page.locator('#dawn-book-expanding-preview .dawn-expander__read').waitFor({state:'visible',timeout:20000});
      await page.locator('#dawn-book-expanding-preview .dawn-expander__read').click();
      await page.locator('#dawn-book-detail').waitFor({state:'visible',timeout:20000});
      const heading=await page.locator('#dawn-book-title').evaluate(el=>{
        const style=getComputedStyle(el),box=el.getBoundingClientRect();
        return {font:style.fontFamily,opacity:style.opacity,height:box.height,text:el.textContent.trim()};
      });
      assert(/Chiron/i.test(heading.font)&&heading.height>25&&heading.opacity!=='0'&&heading.text.length>1,
        device+': original book detail Chinese title not rendered '+slug+' '+JSON.stringify(heading));
      const text=await page.locator('#dawn-book-text').innerText();
      assert(text.includes('為什麼推薦：')&&text.includes('怎樣閱讀：')&&text.includes('與其他作品並讀：'),
        device+': detailed source-backed editorial review missing '+slug);
      assert(await page.locator('#dawn-book-title').innerText().then(v=>v.trim().length>2),device+': book identity gone');
      const source=page.locator('#dawn-book-source');
      if(await source.isVisible())assert(/中文版本|免費中文版/.test(await source.innerText()),device+': edition link misleading');
      await page.screenshot({path:path.join(out,device+'-'+slug+'-book-detail.png'),animations:'disabled',timeout:30000});
      await page.locator('#dawn-book-back').click();
      assert(await page.locator('#dawn-catalogue').isVisible(),device+': native return from book lost '+slug);
      await page.locator('#dawn-close-catalogue').click();
      assert(await page.locator('#dawn-wall').isVisible(),device+': original second-layer bookwall lost '+slug);
    }
    assert.equal(await page.locator('#dawn-wall-grid .dawn-feature').count(),3);
    assert(errors.length===0,device+': javascript errors '+errors.join('; '));
    results.push({device,lists:3,books:22,nativeReturn:true,originalPortals:3});
   }finally{await page.close()}
  }
 }finally{await browser.close()}
 fs.writeFileSync(path.join(out,'report.json'),JSON.stringify(results,null,2));
 console.log('P2_DAWN_NATIVE_READING_LISTS_PASS',JSON.stringify(results));
})().catch(err=>{console.error(err);process.exitCode=1});
