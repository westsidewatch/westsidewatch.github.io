'use strict';
/* Isolated P2 03/04 proof — no runtime writes to the production homepage. */
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..');
const html=fs.readFileSync(path.join(root,'static/experiments/p2-emmaus-olive-handoff-lab.html'),'utf8');
const js=fs.readFileSync(path.join(root,'static/js/p2-emmaus-olive-preview.js'),'utf8');
const css=fs.readFileSync(path.join(root,'static/css/p2-emmaus-olive-preview.css'),'utf8');
assert.match(html,/p2\/living-water\.html\?embed=1/,'reuses approved P2 Church/Magazine source');
assert.match(html,/one\/one-data\.js/,'reads the canonical 66-book inventory');
assert.match(html,/olive\/components\/speaker-baseline-v1\/baseline\.js/,'reuses protected speaker name component');
assert.match(html,/one\/one-dore-assets-241\.js/,'reuses original engraved archive');
assert.match(js,/books\.length!==66/,'guards the full canonical book count');
assert.match(js,/Math\.min\(distance,6\.5\)/,'does not stretch the approved Church/Magazine timing');
assert.match(js,/const emIn=.*6\.50.*oliveIn=.*8\.64/,'both stages share a reversible scroll timeline');
assert.match(js,/const roster=\[/,'uses fixed factual speaker assets');
assert.match(css,/grid-template-columns:minmax\(0,2fr\) minmax\(0,1fr\)/,'Emmaus is left 2/3 and original engravings right 1/3');
assert.match(js,/rail\.addEventListener\('wheel',/,'horizontal ONE strip bridges vertical wheel to the P2 scroll owner');
assert.match(js,/scrollBy\(\{top:delta,behavior:'instant'\}\)/,'the rail forwards vertical wheel to the full-page handoff');
assert.doesNotMatch(js,/stopPropagation\(\)/,'P2 should not trap wheel propagation inside a second viewport');
console.log('P2 03/04 isolated preview source contract: pass');

if(!process.env.P2_BROWSER_PROOF)process.exit(0);
const {chromium}=require('playwright');
(async()=>{
 const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
 const errors=[];
 try{
  for(const viewport of [{width:1648,height:928},{width:390,height:844}]){
   const page=await browser.newPage({viewport});
   page.on('pageerror',error=>errors.push(error.message));
   await page.goto('http://127.0.0.1:4173/experiments/p2-emmaus-olive-handoff-lab.html?d=7.85',{waitUntil:'domcontentloaded',timeout:45000});
   await page.waitForTimeout(550);
   assert.equal(await page.locator('.emmaus__number').count(),66,'all 66 ONE books have selectable numbers');
   assert.equal(await page.locator('#emmaus').getAttribute('aria-hidden'),'false','Emmaus visible in its reading dwell');
   assert.equal(await page.locator('#em-book-en').textContent(),'Matthew');
   await page.locator('[data-book="41"]').evaluate(element=>element.click());
   assert.equal(await page.locator('#em-book-en').textContent(),'Mark','book selection changes live spread');
   assert.match(await page.locator('#emmaus-enter').getAttribute('href'),/book=41&chapter=1/,'selected volume opens the actual ONE chapter, not the default homepage');
   assert.match(await page.locator('#em-plate-selection').textContent(),/BOOK 41 \/ MARK/,'the selected book is carried into the right Doré editorial margin');
   const before=await page.evaluate(()=>scrollY);
   await page.locator('#emmaus-rail').hover();await page.mouse.wheel(0,500);await page.waitForTimeout(300);
   const after=await page.evaluate(()=>scrollY);
   assert(after>before,'vertical wheel on the book rail advances P2 instead of trapping inside ONE');
   await page.locator('[data-jump="10.65"]').click();await page.waitForTimeout(220);
   assert.equal(await page.locator('#olive-proof').getAttribute('aria-hidden'),'false','Olive Mountain follows Emmaus');
   assert.equal(await page.locator('#olive-speaker-names button').count(),12,'twelve verified speakers retained');
   await page.locator('#olive-speaker-names button[data-speaker="derek-prince"]').evaluate(element=>element.click());
   assert.equal(await page.locator('#olive-main-image').getAttribute('alt'),'葉光明');
   await page.locator('[data-jump="6.50"]').click();await page.waitForTimeout(220);
   assert.equal(await page.locator('#olive-proof').getAttribute('aria-hidden'),'true','reverse scroll returns to approved magazine');
   assert.equal(await page.locator('#emmaus').getAttribute('aria-hidden'),'true');
   const screenshot=path.join(root,'artifacts/p2-emmaus-olive',viewport.width+'-olive.png');
   fs.mkdirSync(path.dirname(screenshot),{recursive:true});
   await page.locator('[data-jump="10.65"]').click();await page.screenshot({path:screenshot});
   await page.close();
  }
  assert.deepEqual(errors,[],'no JavaScript errors in either browser size');
  console.log('P2 03/04 Chromium: desktop + phone; stage, books, wheel, posters, reverse scroll: pass');
 }finally{await browser.close()}
})().catch(error=>{console.error(error);process.exitCode=1});
