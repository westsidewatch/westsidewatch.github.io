// P2 05 isolated preview: inspect actual native classification navigation.
const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const base='http://127.0.0.1:4173/experiments/p2-0105-dawn-preview.html';
const out='artifacts/p2-dawn-vinyl';
fs.mkdirSync(out,{recursive:true});
(async()=>{
 const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
 try{
  for(const [name,width,height] of [['desktop',1440,900],['phone',390,844]]){
   const page=await browser.newPage({viewport:{width,height}});
   const errors=[];page.on('pageerror',e=>errors.push(e.message));
   await page.goto(base+'?layer=catalogue&category=zh&d=28.4&v=qa-vinyl', {waitUntil:'domcontentloaded',timeout:45000});
   const classification=page.locator('#dawn-classification');
   await page.waitForFunction(()=>{
    const x=document.querySelector('#dawn-classification-tree');
    return x&&x.querySelectorAll('button.dawn-classification__sleeve').length>0;
   },null,{timeout:35000});
   assert(await classification.isVisible(),name+': category panel hidden');
   assert(await page.locator('#dawn-classification-path').innerText().then(s=>s.includes('中文圖書')),name+': Chinese entrance missing');
   await page.locator('#dawn-classification-tree button.dawn-classification__sleeve').first().click();
   await page.locator('#dawn-classification-tree button.dawn-classification__sleeve').first().click();
   await page.waitForFunction(()=>!document.querySelector('#dawn-classification-results').hidden,null,{timeout:15000});
   const bookCount=await page.locator('#dawn-classification-results button.dawn-classification__book').count();
   assert(bookCount>0,name+': real Chinese category has no books');
   await page.screenshot({path:path.join(out,name+'-chinese-leaf.png'),fullPage:false});
   await page.locator('#dawn-classification-results button.dawn-classification__book').first().click();
   assert(await page.locator('#dawn-book-detail').isVisible(),name+': book reader did not open');
   assert((await page.locator('#dawn-book-title').innerText()).length>0,name+': book title missing');
   await page.locator('#dawn-book-back').click();
   assert(await page.locator('#dawn-classification-results').isVisible(),name+': return path lost book category');
   assert(await page.locator('#dawn-classification-path').innerText().then(s=>s.includes('中文圖書')),name+': return path lost breadcrumb');
   assert(errors.length===0,name+': page errors '+errors.join('; '));
   console.log('DAWN_VINYL',name,'CHINESE_CATEGORY_BOOK_RETURN_PASS',bookCount);
   await page.close();
  }
  // User journey, not a special catalogue URL: the real "全部館藏"
  // action must replace the former flat list with the vinyl wall.
  const journey=await browser.newPage({viewport:{width:1440,height:900}});
  await journey.goto(base+'?layer=second&d=28.4&v=qa-vinyl',{waitUntil:'domcontentloaded',timeout:45000});
  await journey.locator('#dawn-open-catalogue-top').click();
  await journey.waitForFunction(()=>document.querySelectorAll('#dawn-classification-tree button.dawn-classification__sleeve').length===9,null,{timeout:35000});
  assert(await journey.locator('#dawn-classification').isVisible(),'normal nav did not open vinyl classification');
  // Dynamic jackets must use genuine sourced images, never black record art.
  await journey.waitForFunction(()=>document.querySelectorAll('#dawn-classification-tree .dawn-classification__art img').length>=1,null,{timeout:30000});
  const jacket=await journey.locator('#dawn-classification-tree .dawn-classification__sleeve').first().evaluate(el=>({
   background:getComputedStyle(el).backgroundColor,
   image:!!el.querySelector('.dawn-classification__art img'),
   disc:!!el.querySelector('.dawn-classification__vinyl')
  }));
  assert(jacket.image&&!jacket.disc,'category still renders a manufactured vinyl disc');

  assert(!(await journey.locator('#dawn-catalogue .dawn-catalogue__nav').isVisible()),'old search page appears before vinyl wall');
  assert(!(await journey.locator('#dawn-works').isVisible()),'old flat results appear at the landing');
  await journey.screenshot({path:path.join(out,'desktop-normal-entry-vinyl.png'),fullPage:false});
  await journey.locator('#dawn-classification-tree button.dawn-classification__sleeve').last().click();
  await journey.waitForFunction(()=>document.querySelector('#dawn-works')?.children.length>0,null,{timeout:35000});
  assert(await journey.locator('#dawn-works').isVisible(),'bibliographic sub-shelf not accessible');
  assert(await journey.locator('#dawn-classification-path').innerText().then(s=>s.includes('全部書目')),'bibliographic breadcrumb missing');
  await journey.locator('#dawn-classification-path button').first().click();
  assert(!(await journey.locator('#dawn-works').isVisible()),'flat list not hidden after return');
  assert(await journey.locator('#dawn-classification-tree button').count()===9,'vinyl landing not restored');
  console.log('DAWN_VINYL','NORMAL_ALL_COLLECTION_ENTRY_AND_BIBLIOGRAPHY_RETURN_PASS');
  await journey.close();
  const page=await browser.newPage({viewport:{width:1440,height:900}});
  await page.goto(base+'?layer=catalogue&d=28.4&v=qa-vinyl',{waitUntil:'domcontentloaded',timeout:45000});
  await page.waitForFunction(()=>document.querySelectorAll('#dawn-classification-tree button.dawn-classification__sleeve').length===9,null,{timeout:35000});
  await page.locator('#dawn-classification-tree button.dawn-classification__sleeve').first().click();
  const subCount=await page.locator('#dawn-classification-tree button.dawn-classification__sleeve').count();
  assert(subCount>=4,'Bible root did not open subcategories');
  await page.locator('#dawn-classification-tree button.dawn-classification__sleeve').first().click();
  await page.waitForFunction(()=>!document.querySelector('#dawn-classification-results').hidden,null,{timeout:45000});
  assert(await page.locator('#dawn-classification-path').innerText().then(s=>s.includes('原文與文本')),'English child path missing');
  assert(await page.locator('#dawn-classification-results .dawn-classification__actions button').count()===2,'Leaf navigation has no return actions');
  await page.locator('#dawn-classification-results .dawn-classification__actions button').first().click();
  assert(await page.locator('#dawn-classification-tree button').count()>=4,'Return to subcategory wall broken');
  await page.screenshot({path:path.join(out,'desktop-knowledge-map.png'),fullPage:false});
  console.log('DAWN_VINYL','ROOT_CHILD_BACK_PASS');
  await page.close();
 }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
