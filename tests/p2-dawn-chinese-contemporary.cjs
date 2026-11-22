/* P2 Chinese source discovery acceptance.
 * Neither editorial research candidates nor publisher covers become canonical.
 * First click previews in Dawn; only the second explicit action can leave.
 */
'use strict';
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),
 {chromium}=require('playwright');
const manifest=JSON.parse(fs.readFileSync('static/dawn-library/chinese-contemporary-discovery.json','utf8'));
const ancient=JSON.parse(fs.readFileSync('static/dawn-library/chinese-collection.json','utf8'));
assert.equal(manifest.schema,'dawn.library.chinese-contemporary-discovery.v1');
assert.equal(manifest.status,'editorial-source-discovery-not-canonical-admission');
assert.equal(manifest.candidates.length,11);
assert.equal(manifest.candidates.filter(c=>c.translation==='Chinese translation').length,8);
const eligible=manifest.candidates.filter(c=>['verified-free-download','verified-free-subscription','verified-free-reading'].includes(c.freeReading?.status));
assert.equal(eligible.length,9,'reader-facing discovery may show only confirmed free books');
assert.equal(eligible.filter(c=>c.translation==='Chinese translation').length,6);
assert.equal(manifest.candidates.filter(c=>c.freeReading?.status==='not-verified').length,2,
 'unconfirmed free-access editions stay in research, not the reader-facing library');
assert.equal(ancient.works.length,47,'do not mutate 47 original Chinese Works');
assert.equal(manifest.audit.candidateCount,manifest.candidates.length);
const ids=new Set();
for(const c of manifest.candidates){
 assert(!ids.has(c.candidateId),'duplicate candidate: '+c.candidateId);
 ids.add(c.candidateId);
 assert(c.candidateId.startsWith('dawn:discovery:zh:'),'research IDs never impersonate canonical Works');
 assert(/^https:\/\//.test(c.sourceUrl),'publisher link must be HTTPS: '+c.title);
 assert(c.sourceKind==='publisher-book-detail','source detail must have specific work identity');
 assert(c.coverUrl===null||[
    'https://my-elibrary.net/wp-content/uploads/',
    'https://9marks-static.oss-cn-hongkong.aliyuncs.com/wp/'
   ].some(prefix=>c.coverUrl.startsWith(prefix)),
   'publisher cover must be hosted on that title’s actual official publisher image CDN');
 assert(c.admission==='candidate-only','not a canonical admitted Work');
 assert(c.access.includes('publisher')||c.access.includes('license'),
   'do not claim unauthorized public-domain full text');
}
const dir='artifacts/p2-dawn-modern-chinese';
fs.mkdirSync(dir,{recursive:true});
(async()=>{
 const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
 try{
 for(const [device,width,height] of [['desktop',1440,900],['phone',390,844]]){
  const page=await browser.newPage({viewport:{width,height}});
  const errors=[];
  page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:4173/experiments/p2-0105-dawn-preview.html?layer=catalogue&category=zh&v=r69-modern-chinese',
   {waitUntil:'domcontentloaded',timeout:45000});
  // Chinese library must open on contemporary literature, not the older
  // 47 archival works. No extra click should be needed to reach new books.
  const cards=page.locator('#dawn-classification-results .dawn-contemporary__book');
  await page.waitForFunction(()=>document.querySelectorAll('.dawn-contemporary__book').length===9,null,{timeout:25000});
  assert.equal(await cards.count(),9,device+': catalog source discovery cards missing');
  const titles=await cards.evaluateAll(items=>items.map(x=>x.querySelector('.dawn-contemporary__metadata strong')?.textContent));
  assert(!titles.includes('認識協同書的神學')&&!titles.some(t=>t?.startsWith('協同書：')),
   device+': free-reading-unverified publication incorrectly offered as available book');
  assert(eligible.every(c=>titles.includes(c.title)),device+': a verified free book is missing');
  assert.equal(await page.locator('#dawn-classification-results .dawn-contemporary__archive-entry').count(),1,
   device+': early Chinese archival section has no secondary access');
  await page.locator('#dawn-classification-results .dawn-contemporary__archive-entry').click();
  const archiveTiles=page.locator('#dawn-classification-tree button.dawn-classification__sleeve--historical-zh');
  await page.waitForFunction(()=>document.querySelectorAll('#dawn-classification-tree button.dawn-classification__sleeve--historical-zh').length>1,
   null,{timeout:15000});
  assert((await archiveTiles.count())>1,device+': early Chinese works were removed rather than moved below contemporary');
  const tileOrder=await page.locator('#dawn-classification-tree button.dawn-classification__sleeve')
    .evaluateAll(tiles=>tiles.map(t=>({label:t.querySelector('strong')?.textContent,
      modern:t.classList.contains('dawn-classification__sleeve--contemporary')})));
  assert(tileOrder[0]?.modern,device+': contemporary Chinese shelf must precede all early Chinese classes');
  await page.screenshot({path:path.join(dir,device+'-modern-first-archive-second.png')});
  await page.locator('#dawn-primary-chinese').click();
  await page.waitForFunction(()=>document.querySelectorAll('#dawn-classification-results .dawn-contemporary__book').length===11,
   null,{timeout:20000});
  await page.waitForFunction(()=>{
    const cards=[...document.querySelectorAll('#dawn-classification-results .dawn-contemporary__book')];
    return cards.length===9&&cards.every(card=>{
     const img=card.querySelector('img.dawn-contemporary__tile-cover');
     return card.classList.contains('dawn-contemporary__book--pictured')&&img?.complete&&img.naturalWidth>120;
    });
   },null,{timeout:30000});
  const visualProof=await cards.evaluateAll(items=>items.map(card=>{
   const art=card.querySelector('.dawn-contemporary__art');
   const paper=art?.querySelector('.dawn-contemporary__folio');
   const img=art?.querySelector('img');
   const artRect=art?.getBoundingClientRect();
   const paperRect=paper?.getBoundingClientRect();
   const image=art?.querySelector('img:not(.dawn-contemporary__cover-backdrop)');
   const frame=image?.getBoundingClientRect();
   return {title:paper?.querySelector('strong')?.textContent,
    pictured:card.classList.contains('dawn-contemporary__book--pictured'),
    paperColor:paper?getComputedStyle(paper).color:'',
    artBackground:art?getComputedStyle(art).backgroundColor:'',
    imageOpacity:image?parseFloat(getComputedStyle(image).opacity):null,
    artSize:artRect?{w:artRect.width,h:artRect.height}:null,
    paperSize:paperRect?{w:paperRect.width,h:paperRect.height}:null,
    author:paper?.querySelector('.dawn-contemporary__folio-foot span')?.textContent,
    backdrop:!!art?.querySelector('.dawn-contemporary__cover-backdrop'),
    coverSize:frame?{w:frame.width,h:frame.height}:null,
    imageSrc:image?.getAttribute('src')||null,
    imageNaturalWidth:image?.naturalWidth||0,imageNaturalHeight:image?.naturalHeight||0,
    imageFit:image?getComputedStyle(image).objectFit:null};
  }));
  const published=manifest.candidates.filter(c=>['verified-free-download','verified-free-subscription','verified-free-reading'].includes(c.freeReading?.status));
  const configured=published.filter(c=>c.coverUrl);
  const rendered=visualProof.filter(p=>p.pictured);
  console.log('CHINESE_PUBLISHER_TILE_IMAGES',device,JSON.stringify({
   withCoverURLs:configured.length,rendered:rendered.length,
   cards:visualProof.map(p=>({title:p.title,pictured:p.pictured,src:p.imageSrc,width:p.imageNaturalWidth}))}));
  for(const proof of visualProof){
   assert(proof.title?.length>1,device+': missing exact-book title');
   assert(proof.artSize?.w>120&&proof.artSize?.h>150,device+': invalid book square');
   assert(Math.abs(proof.artSize.w-proof.artSize.h)<3,
    device+': card must remain a square before expansion: '+proof.title);
   assert(proof.author?.trim(),device+': book metadata lacks its real author');
   if(proof.pictured){
    assert(proof.imageNaturalWidth>120&&proof.imageNaturalHeight>120,
     device+': purported cover is not actually loaded: '+proof.title);
    assert(proof.coverSize?.w>=proof.artSize.w-4&&proof.coverSize?.h>=proof.artSize.h-4,
     device+': publisher cover does not fill entire square: '+proof.title);
    assert(proof.imageFit==='cover',device+': image not set to fill square');
   }else{
    assert(!proof.imageNaturalWidth,
     device+': image was loaded but obscured by typography: '+proof.title);
   }
  }
  // The first page must display real publisher jackets rather than a complete
  // wall of colored labels. Strict full-coverage remains a release requirement
  // once each official source image is verified.
  assert.equal(configured.length,9,device+': each displayed free title must have its exact publisher jacket');
  assert.equal(rendered.length,9,device+': all nine actual source images must fill their tiles');
  const headingText=await page.locator('#dawn-classification-results .dawn-classification__result-heading').innerText();
  assert(headingText.includes('認識作者與作品')&&headingText.includes('出版方'),
   device+': book introduction must explain the reader journey');
  const forbidden=/已核對|未獲本站|全文轉載|沒有複製|受版權保護|候選書|SOURCE EDITION|WORK ID|內部驗收|測試版|QA|Draft|PR #|commit/i;
  const publicIntroduction=await page.locator('#dawn-classification-results').innerText();
  assert(!forbidden.test(publicIntroduction),
   device+': internal provenance or rights-management text leaked into library: '+publicIntroduction.slice(0,550));
  await page.screenshot({path:path.join(dir,device+'-modern-chinese-source-wall.png')});
  const originalUrl=page.url();
  await cards.first().click();
  const preview=page.locator('#dawn-book-expanding-preview');
  await preview.waitFor({state:'visible',timeout:15000});
  const coverAfterSelection=preview.locator('.dawn-expander__book-image');
  if(manifest.candidates[0].coverUrl){
   await coverAfterSelection.waitFor({state:'attached',timeout:10000});
   assert.equal(await coverAfterSelection.getAttribute('src'),manifest.candidates[0].coverUrl,
    device+': expansion failed to reveal the actual selected book jacket');
  }
  assert.equal(page.url(),originalUrl,device+': first click must not navigate');
  const visiblePreview=await preview.innerText();
  assert(!forbidden.test(visiblePreview),
   device+': preview contains prohibited technical or licensing narration: '+visiblePreview.slice(0,400));
  assert(visiblePreview.includes('出版方')&&visiblePreview.includes('介紹'),
   device+': book preview lacks publisher-facing introduction');
  assert(!(await page.locator('#dawn-book-detail').isVisible()),device+': candidate must not open internal canonical reader');
  assert.equal(await preview.locator('.dawn-expander__read').innerText(),'前往出版方了解本書');
  const titleOS=await preview.locator('.dawn-expander__title').evaluate(el=>({
   font:getComputedStyle(el).fontFamily,weight:getComputedStyle(el).fontWeight
  }));
  assert(/Chiron/i.test(titleOS.font)&&titleOS.weight==='200',
   device+': Chinese book preview must use light OS Chiron title, got '+JSON.stringify(titleOS));
  const previewVisual=await preview.evaluate(el=>{
   const cover=el.querySelector('.dawn-expander__book');
   const image=cover?.querySelector('img');
   const paper=cover?.querySelector('.dawn-expander__book-paper');
   return {ready:cover?.classList.contains('dawn-expander__book--ready'),
    paper:getComputedStyle(paper).display,
    imageOpacity:image?parseFloat(getComputedStyle(image).opacity):null};
  });
  assert(previewVisual.ready||previewVisual.paper!=='none',
   device+': newly expanded preview has a blank white image while loading');
  const folioColor=await preview.locator('.dawn-expander__book').evaluate(el=>({
   pictured:el.classList.contains('dawn-expander__book--ready'),
   background:getComputedStyle(el).backgroundColor,
   paper:getComputedStyle(el.querySelector('.dawn-expander__book-paper')).backgroundColor
  }));
  if(!folioColor.pictured){
   assert(folioColor.background!=='rgb(255, 255, 255)'&&folioColor.paper!=='rgb(255, 255, 255)',
    device+': translated-work fallback was a huge white empty sheet');
  }
  const firstTitle=await preview.locator('.dawn-expander__title').innerText();
  await cards.nth(1).click();
  await page.waitForFunction(old=>document.querySelector('#dawn-book-expanding-preview .dawn-expander__title')?.textContent!==old,
   firstTitle,{timeout:15000});
  assert.equal(await page.locator('#dawn-book-expanding-preview').count(),1,device+': changed candidate duplicated preview');
  assert.equal(page.url(),originalUrl,device+': changing candidates unexpectedly navigated');
  const source=await preview.locator('.dawn-expander__source').getAttribute('href');
  assert.equal(source,manifest.candidates[1].sourceUrl);
  await page.evaluate(()=>{
   window.__lastPublisher=null;
   window.open=(url)=>{window.__lastPublisher=url;return null};
  });
  await preview.locator('.dawn-expander__read').click();
  await page.waitForFunction(()=>Boolean(window.__lastPublisher),null,{timeout:5000});
  const destination=await page.evaluate(()=>window.__lastPublisher);
  assert.equal(destination,manifest.candidates[1].sourceUrl,
   device+': explicit second action not directed to publisher page');
  await page.waitForFunction(()=>!document.querySelector('#dawn-book-expanding-preview .dawn-expander__read')?.disabled,null,{timeout:5000});
  assert.equal(await preview.locator('.dawn-expander__read').innerText(),'前往出版方了解本書',device+': publisher link should reset after opening a tab');
  assert.equal(page.url(),originalUrl,device+': current Dawn collection should remain open');
  await page.screenshot({path:path.join(dir,device+'-translation-expanded-preview.png')});
  assert.equal(errors.length,0,device+': JS exceptions: '+errors.join('; '));
  console.log('MODERN_CHINESE_SOURCE_QA',device,'9_FREE_BOOKS_6_TRANSLATIONS_TWO_STEP_NAV_PASS');
  await page.close();
 }
 }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
