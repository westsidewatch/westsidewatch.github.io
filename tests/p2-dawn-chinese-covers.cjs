/* Chinese source-cover acceptance: real 46 Yale scanned covers + reading wall.
 * Use local static server: python3 -m http.server 4173 --directory static
 */
'use strict';
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),
 crypto=require('node:crypto'),{chromium}=require('playwright');
const base='http://127.0.0.1:4173';
const data=JSON.parse(fs.readFileSync('static/dawn-library/chinese-collection.json','utf8'));
const originals=data.works.filter(w=>w.cover?.mode==='source-facsimile-title-page');
assert.equal(data.works.length,47,'original 47 Chinese Works preserved');
assert.equal(originals.length,46,'all 46 Yale CLSC Work covers must be sourced');
assert.equal(data.works.filter(w=>!w.cover?.url).length,0,'no Chinese Work may lack a cover URL');
const distinct=new Set();
for(const work of originals){
 const cover=work.cover;
 assert(cover.url.startsWith('/dawn-library/chinese-facsimile-covers/'),
  'no remote guessed jacket for '+work.workId);
 const file=path.join('static',cover.url.replace(/^\//,''));
 assert(fs.existsSync(file),'asset missing for '+work.workId);
 const bytes=fs.readFileSync(file);
 assert.equal(bytes.toString('ascii',0,4),'RIFF','not WEBP: '+file);
 assert.equal(bytes.toString('ascii',8,12),'WEBP','not WEBP: '+file);
 assert.equal(crypto.createHash('sha256').update(bytes).digest('hex'),
  cover.provenance?.imageSha256,'source-image checksum differs: '+work.workId);
 assert(cover.provenance.sourcePdf.startsWith('https://divinity-adhoc.library.yale.edu/HKBU/CLSC/'),
  'source identity not Yale original PDF: '+work.workId);
 assert(!distinct.has(cover.url),'same image wrongly assigned to different Work');
 distinct.add(cover.url);
}
const out='artifacts/p2-dawn-chinese-covers';
fs.mkdirSync(out,{recursive:true});
(async()=>{
 for(const w of originals){
  const r=await fetch(base+w.cover.url);
  assert.equal(r.status,200,w.workId+' image missing from running static server');
  assert(r.headers.get('content-type')?.includes('image/webp'),w.workId+' not served as WEBP');
 }
 const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
 try{
  for(const [name,width,height] of [['desktop',1440,900],['phone',390,844]]){
   const page=await browser.newPage({viewport:{width,height},deviceScaleFactor:1});
   const errors=[];page.on('pageerror',e=>errors.push(e.message));
   // Regression from user screenshot: the *primary seven-subject* wall
   // appeared almost entirely blank although the underlying books had covers.
   await page.goto(base+'/experiments/p2-0105-dawn-preview.html?layer=catalogue&d=28.4&v=r68-category-preload',
    {waitUntil:'domcontentloaded',timeout:45000});
   await page.waitForFunction(()=>document.querySelectorAll('#dawn-classification-tree button.dawn-classification__sleeve').length>=9,
    null,{timeout:35000});
   await page.waitForFunction(()=>{
    const cards=[...document.querySelectorAll('#dawn-classification-tree button.dawn-classification__sleeve')];
    return cards.filter(c=>c.querySelector('img')?.naturalWidth>120).length>=7;
   },null,{timeout:25000});
   const roots=await page.locator('#dawn-classification-tree button.dawn-classification__sleeve')
    .evaluateAll(cards=>cards.map(c=>({label:c.querySelector('strong')?.textContent,
      group:c.dataset.coverGroup,loaded:!!c.querySelector('img')?.naturalWidth,
      source:c.querySelector('img')?.getAttribute('src')})));
   assert(roots.filter(c=>c.loaded).length>=7,
    name+': primary category wall still looks empty: '+JSON.stringify(roots));
   console.log('PRIMARY_CATEGORY_COVER_QA',name,JSON.stringify(roots));
   await page.screenshot({path:path.join(out,name+'-primary-category-cover-wall.png')});
   await page.goto(base+'/experiments/p2-0105-dawn-preview.html?layer=catalogue&category=zh-archive&d=28.4&v=r68-category-preload',
    {waitUntil:'domcontentloaded',timeout:45000});
   await page.waitForFunction(()=>document.querySelectorAll('#dawn-classification-tree button.dawn-classification__sleeve').length>=2,
    null,{timeout:35000});
   // Some early categories contain only the source Gutenberg book; never
   // demand a Yale image on a book that is not in the Yale CLSC collection.
   // The first priority is contemporary; historical shelves remain available.
   await page.waitForFunction(()=>{
    const images=[...document.querySelectorAll('#dawn-classification-tree button.dawn-classification__sleeve img')];
    return images.some(img=>img.complete&&img.naturalWidth>100&&
      img.currentSrc.includes('/chinese-facsimile-covers/'));
   },null,{timeout:15000});
   const categories=page.locator('#dawn-classification-tree button.dawn-classification__sleeve');
   await page.screenshot({path:path.join(out,name+'-chinese-category-cover-wall.png')});
   await categories.nth(1).click();
   await page.waitForTimeout(250);
   const state=await page.evaluate(()=>({
    breadcrumb:document.querySelector('#dawn-classification-path')?.innerText,
    treeCount:document.querySelectorAll('#dawn-classification-tree button.dawn-classification__sleeve').length,
    treeHidden:document.querySelector('#dawn-classification-tree')?.hidden,
    resultHidden:document.querySelector('#dawn-classification-results')?.hidden
   }));
   console.log('CHINESE_GROUP_STATE',name,JSON.stringify(state),JSON.stringify(errors));
   await page.screenshot({path:path.join(out,name+'-after-group-selection.png')});
   await page.locator('#dawn-classification-tree button.dawn-classification__sleeve').first().click({timeout:8000});
   await page.waitForFunction(()=>!document.querySelector('#dawn-classification-results').hidden,
    null,{timeout:20000});
   const covers=page.locator('#dawn-classification-results .dawn-classification__book-art img');
   assert((await covers.count())>0,name+': original cover images are missing in Chinese book wall');
   await covers.first().waitFor({state:'visible',timeout:15000});
   await page.waitForFunction(()=>{
    const imgs=[...document.querySelectorAll('#dawn-classification-results .dawn-classification__book-art img')];
    return imgs.some(img=>img.complete&&img.naturalWidth>150);
   },null,{timeout:15000});
   const actual=await covers.evaluateAll(imgs=>imgs.map(i=>({
    url:i.getAttribute('src'),width:i.naturalWidth,loaded:i.complete})));
   assert(actual.some(a=>a.width>150&&a.url.includes('/chinese-facsimile-covers/')),
    name+': Yale scanned cover not visible in browser');
   await page.screenshot({path:path.join(out,name+'-chinese-real-book-covers.png')});
   console.log('CHINESE_47_COVER_QA',name,'TOTAL',data.works.length,'YALE',originals.length,
    'VISIBLE',actual.filter(x=>x.width>150).length,'PASSED');
   assert.equal(errors.length,0,name+': runtime JS errors: '+errors.join('; '));
   await page.close();
  }
 }finally{await browser.close()}
})().catch(error=>{console.error(error);process.exitCode=1});
