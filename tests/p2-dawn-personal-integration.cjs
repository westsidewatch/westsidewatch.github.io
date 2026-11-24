// Verify the P2 public reader reuses the already accepted Formal Edition
// personal-state module and Living Library; it must NOT own a second schema.
const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const fs=require('fs');
fs.mkdirSync('artifacts/p2-dawn-personal',{recursive:true});
const base='http://127.0.0.1:4173';
(async()=>{
 const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
 try{
  for(const [kind,width,height] of [['desktop',1440,900],['phone',390,844]]){
   const context=await browser.newContext({viewport:{width,height}});
   const page=await context.newPage();
   const errors=[];page.on('pageerror',e=>errors.push(String(e)));
   await page.goto(base+'/experiments/p2-0105-dawn-preview.html?layer=catalogue&category=zh&d=28.4',{waitUntil:'domcontentloaded',timeout:45000});
   await page.waitForFunction(()=>document.querySelectorAll('#dawn-classification-tree .dawn-classification__sleeve').length>0,null,{timeout:35000});
   assert(await page.locator('#dawn-personal-open').isVisible(),kind+': original personal library entry missing');
   await page.locator('#dawn-personal-open').click();
   assert(await page.locator('#dawn-personal-dialog').isVisible(),kind+': personal library dialog missing');
   await page.locator('#dawn-personal-close').click();
   await page.locator('#dawn-classification-tree .dawn-classification__sleeve').first().click();
   await page.locator('#dawn-classification-tree .dawn-classification__sleeve').first().click();
   await page.waitForFunction(()=>!document.querySelector('#dawn-classification-results').hidden,null,{timeout:15000});
   await page.locator('#dawn-classification-results .dawn-classification__book').first().click();
   await page.locator('#dawn-book-expanding-preview .dawn-expander__read').waitFor();
   await page.locator('#dawn-book-expanding-preview .dawn-expander__read').click();
   await page.locator('#dawn-book-detail').waitFor({state:'visible',timeout:20000});
   const bookmark=page.locator('#dawn-book-bookmark');
   assert(await bookmark.isEnabled(),kind+': canonical Chinese Work rejected by Library Card');
   await bookmark.click();
   const saved=await page.evaluate(()=>JSON.parse(localStorage.getItem('dawn.personal-state.v1')||'{}'));
   assert(saved.schema==='dawn.personal-state.v1',kind+': invented a parallel personal schema');
   assert(saved.bookmarks?.length===1,kind+': saveBookmark did not persist');
   await page.screenshot({path:'artifacts/p2-dawn-personal/'+kind+'-book-library-card.png',fullPage:false});
   await page.locator('#dawn-personal-open').click();
   assert(await page.locator('#dawn-personal-items').getByText('我的藏書 · 1').isVisible(),kind+': saved bookmark not visible');
   await page.locator('#dawn-personal-view').click();
   await page.locator('#dawn-personal-close').click();
   await page.reload({waitUntil:'domcontentloaded'});
   await page.locator('#dawn-personal-open').click();
   const reloaded=await page.evaluate(()=>JSON.parse(localStorage.getItem('dawn.personal-state.v1')||'{}'));
   assert(reloaded.bookmarks?.length===1&&reloaded.views?.length===1,kind+': save state lost on reload');
   assert(await page.locator('#dawn-personal-items').getByText('保存的書架 · 1').isVisible(),kind+': saved view missing');
   await page.screenshot({path:'artifacts/p2-dawn-personal/'+kind+'-reader-shelves.png',fullPage:false});
   // The same origin key is readable from the existing Formal Edition route.
   const formal=await context.newPage();
   await formal.goto(base+'/dawn-library/formal-edition/phase4/',{waitUntil:'domcontentloaded',timeout:45000});
   assert(await formal.evaluate(()=>!!localStorage.getItem('dawn.personal-state.v1')),kind+': not shared with original formal Personal Dawn');
   assert(!errors.length,kind+': '+errors.join('; '));
   console.log('PERSONAL_DAWN',kind,'SAME_SCHEMA_BOOKMARK_VIEW_PERSISTENCE_PASS');
   await context.close();
  }
  const page=await browser.newPage();
  await page.goto(base+'/experiments/p2-0105-dawn-preview.html?layer=catalogue&d=28.4',{waitUntil:'domcontentloaded',timeout:45000});
  await page.waitForFunction(()=>document.querySelectorAll('#dawn-classification-tree .dawn-classification__sleeve').length===10,null,{timeout:35000});
  const tile=await page.locator('#dawn-classification-tree .dawn-classification__sleeve').first().innerText();
  assert(tile.includes('27,692'), 'did not use original Dawn Living Library count for 聖經: '+tile);
  console.log('PERSONAL_DAWN','LIVING_LIBRARY_AUTHORITATIVE_TAXONOMY_PASS');
  await page.close();
 }finally{await browser.close()}
})().catch(error=>{console.error(error);process.exitCode=1});
