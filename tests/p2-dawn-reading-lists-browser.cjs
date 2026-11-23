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
    const section=page.locator('#dawn-wall-grid');
    await section.waitFor({state:'visible',timeout:30000});
    assert.equal(await section.locator('button[data-dawn-reading-list]').count(),3,device+': all three original-grid reading lists needed');
    assert.equal(await section.locator('.dawn-feature').count(),3,device+': original editorial portal missing');
    assert.equal(await page.locator('.dawn-second__motherform').count(),1,device+': original Scripture Studio removed');
    assert.equal(await page.locator('#dawn-issue-contents').count(),0,device+': intrusive old giant booklist headline remains');
    assert(!await page.locator('.dawn-reading-room__departments').isVisible(),device+': seven subjects competing on opening wall');
    await section.scrollIntoViewIfNeeded();
    const style=await section.evaluate(el=>{
      const portal=[...el.querySelectorAll('.dawn-feature')];
      const tiles=[...el.querySelectorAll('button[data-dawn-reading-list]')];
      const chapter=el.querySelector('.dawn-reading-list__series');
      const heading=chapter?.querySelector('#dawn-reading-list-heading');
      const marker=chapter?.querySelector('.dawn-reading-list__marker');
      const first=tiles[0],s=getComputedStyle(first.querySelector('.dawn-reading-list__caption strong'));
      const books=[...el.querySelectorAll('.dawn-cover')];
      const square=marker?.getBoundingClientRect(),end=chapter?.getBoundingClientRect().bottom;
      return {font:s.fontFamily,weight:s.fontWeight,unit:first.getBoundingClientRect().width,
        height:first.getBoundingClientRect().height,
        portalBottom:Math.max(...portal.map(n=>n.getBoundingClientRect().bottom)),
        firstListTop:Math.min(...tiles.map(n=>n.getBoundingClientRect().top)),
        parent:first.parentElement?.className,
        chapterParent:chapter?.parentElement?.id,
        chapterLabel:heading?.textContent?.trim(),
        labelFont:heading?getComputedStyle(heading).fontFamily:'',
        labelHeight:heading?.getBoundingClientRect().height,
        markerWidth:square?.width,markerHeight:square?.height,
        bookStartsAfterSeries:books.every(n=>n.getBoundingClientRect().top>=end-4),
        dividerAfterSeries:(el.querySelector('.dawn-wall__collection-divider')?.getBoundingClientRect().top||0)>=end-4,
        markerCount:marker?.querySelector('.dawn-reading-list__marker-count')?.innerText,
        cardCounts:tiles.map(n=>n.querySelector('.dawn-reading-list__quantity')?.textContent?.trim()||''),
        tileLabels:tiles.map(n=>n.querySelector('.dawn-reading-list__serial')?.textContent?.trim()||''),
        pageOverflow:document.querySelector('#dawn-second').scrollWidth-document.querySelector('#dawn-second').clientWidth};
    });
    assert(/Chiron/i.test(style.font),device+': original Design OS Chinese type removed '+style.font);
    assert(style.parent==='dawn-reading-list__series-grid'&&style.chapterParent==='dawn-wall-grid',
       device+': reading series no longer belongs to the original vinyl wall '+JSON.stringify(style));
    assert(style.chapterLabel==='書單'&&/Chiron/i.test(style.labelFont)&&style.labelHeight>25,
       device+': readable Chinese 書單 heading is missing '+JSON.stringify(style));
    assert(Math.abs(style.markerWidth-style.markerHeight)<12,device+': booklist section identity is not a square '+JSON.stringify(style));
    assert(style.markerWidth>style.unit*1.85,device+': booklist directory is not a true 2x2 lead square '+JSON.stringify(style));
    assert(style.markerCount?.includes('22')&&style.markerCount?.includes('03'),device+': curated series is not identified as a collection '+JSON.stringify(style));
    assert(JSON.stringify(style.cardCounts)===JSON.stringify(['06','09','07']),device+': multi-book quantities 6/9/7 not visually identifiable '+JSON.stringify(style));
    assert(style.dividerAfterSeries,device+': real book-cover wall lacks its own editorial heading '+JSON.stringify(style));
    assert(style.tileLabels.every(s=>s.includes('書單')),device+': list square appears to be an ordinary book '+JSON.stringify(style));
    assert(Math.abs(style.unit-style.height)<12,device+': reading-list sleeve not a square '+JSON.stringify(style));
    assert(style.firstListTop>=style.portalBottom-8,device+': reading lists displayed before the original three editorial portals '+JSON.stringify(style));
    assert(style.bookStartsAfterSeries,device+': actual book jackets intrude into the guided-list group '+JSON.stringify(style));
    assert(style.pageOverflow<18,device+': second layer horizontal overflow '+style.pageOverflow);
    await page.screenshot({path:path.join(out,device+'-native-reading-contents.png'),animations:'disabled',timeout:30000});
    const labelRects=await section.locator('button[data-dawn-reading-list]').evaluateAll(cards=>cards.map(el=>{
      const caption=el.querySelector('.dawn-reading-list__caption'),face=el.querySelector('.dawn-reading-list__face');
      return {id:el.dataset.dawnReadingList,clippedCaption:caption.scrollHeight-caption.clientHeight,
        clippedFace:face.scrollHeight-face.clientHeight,cardWidth:el.getBoundingClientRect().width};
    }));
    for(const label of labelRects){
      assert(label.cardWidth>120&&label.clippedCaption<4&&label.clippedFace<4,
        device+': native vinyl square lost its Chinese label '+JSON.stringify(label));
    }
    await section.locator('#dawn-reading-list-heading').scrollIntoViewIfNeeded();
    await page.screenshot({path:path.join(out,device+'-native-vinyl-list-squares.png'),animations:'disabled',timeout:30000});
    await section.locator('.dawn-reading-list__series').screenshot({path:path.join(out,device+'-complete-booklist-series.png'),animations:'disabled',timeout:30000});
    for(const [slug,count,bookIndex] of cases){
      await page.locator('button[data-dawn-reading-list="'+slug+'"]').click();
      await page.waitForFunction(n=>document.querySelectorAll('#dawn-works button.dawn-catalogue__cover-card').length===n,count,{timeout:30000});
      assert(await page.locator('#dawn-catalogue').isVisible(),device+': native catalogue did not open for '+slug);
      assert(await page.locator('#dawn-catalogue__reading-index').count()===0,'No parallel selector ID allowed');
      assert.equal(await page.locator('.dawn-catalogue__reading-index button').count(),3,device+': same folio list switching missing');
      const guide=page.locator('#dawn-works > .dawn-reading-list__guide');
      assert.equal(await guide.count(),1,device+': 2x2 editorial question is not inside the original six-column work grid');
      const guideText=await guide.innerText();
      assert(guideText.includes('閱讀次序：')&&guideText.length>110,device+': original question, essay and sequence missing');
      const guideBox=await guide.boundingBox(),bookBox=await page.locator('#dawn-works .dawn-reading-list__sleeve').first().boundingBox();
      assert(guideBox&&bookBox&&guideBox.width>bookBox.width*1.85,device+': hierarchy lacks true 2x2 / 1x1 size contrast '+slug);
      assert(Math.abs(guideBox.width-guideBox.height)<22,device+': question tile not square '+slug+' '+JSON.stringify(guideBox));
      assert(!await page.locator('#dawn-catalogue-introduction').isVisible(),device+': duplicate separate reading essay still occupies top of collection');
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
