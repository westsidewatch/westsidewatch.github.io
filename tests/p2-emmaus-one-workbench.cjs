'use strict';
/* P2 03: actual ONE workstation + 66 volumes, without inner engraving. */
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..');
const read=p=>fs.readFileSync(path.join(root,'static',p),'utf8');
const html=read('experiments/p2-emmaus-olive-handoff-lab.html');
const css=read('css/p2-emmaus-one-workbench.css');
const js=read('js/p2-emmaus-one-workbench.js');
const host=read('js/p2-emmaus-olive-preview.js');
assert.match(html,/id="em-one-chapter-grid"/,'ONE 66-book chapter picker is in P2');
assert.match(html,/id="em-one-workbench"/,'full ONE app lives inside the P2 Emmaus spread');
assert.match(html,/id="em-one-frame"/,'the in-page ONE original application frame exists');
assert.match(html,/src="\/one\/one-data\.js"/,'P2 uses the original 66-book index');
assert.match(css,/#emmaus > \.emmaus__left::before,[\s\S]*content:none!important/,'no decorative engraving in the ONE page');
assert.match(css,/#emmaus > \.emmaus__left\{[\s\S]*background-image:none!important/,'all engraving lives outside the folio');
assert.match(js,/frame\.src=route/,'ONE original app loads inside P2 when activated');
assert.match(js,/book\.?\[3\]/,'canonical chapter counts drive every volume');
assert.match(host,/P2EmmausSelect/,'the native chapter selector and Doré panel share state');
assert.match(host,/p2:one-selection/,'chapter switches update the original ONE workbench');
assert.match(host,/f\.connections\.forEach/,'real ONE cross references appear in the P2 tabs');
assert.match(host,/f\.background\.forEach/,'real ONE chapter background appears in the P2 tabs');
console.log('P2 Emmaus native ONE workbench source: pass');
if(!process.env.P2_BROWSER_PROOF)process.exit(0);
const {chromium}=require('playwright');
(async()=>{
 const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
 try{
  for(const viewport of [{width:1648,height:928},{width:390,height:844}]){
   const page=await browser.newPage({viewport});
   const errors=[];page.on('pageerror',error=>errors.push(error.message));
   await page.goto('http://127.0.0.1:4173/experiments/p2-emmaus-olive-handoff-lab.html?five=1&ground=1&d=9.10',
    {waitUntil:'domcontentloaded',timeout:45000});
   await page.waitForFunction(()=>document.querySelectorAll('#emmaus-rail [data-book]').length===66 &&
    document.querySelectorAll('#em-one-chapter-grid button').length===24,{timeout:25000});
   assert.equal(await page.locator('#em-one-chapter-grid button').count(),24);
   const imgRule=await page.locator('#emmaus > .emmaus__left').evaluate(el=>({
    background:getComputedStyle(el).backgroundImage,
    before:getComputedStyle(el,'::before').display,
    after:getComputedStyle(el,'::after').display
   }));
   assert.equal(imgRule.background,'none','NO engraved decorative illustration inside the ONE reading folio');
   assert.equal(imgRule.before,'none');assert.equal(imgRule.after,'none');
   await page.locator('#emmaus-rail [data-book="45"]').click();
   await page.waitForTimeout(90);
   assert.equal(await page.locator('#em-one-chapter-grid button').count(),16,'Romans shows the real 16 chapters');
   await page.locator('#em-one-chapter-grid [data-one-chapter="8"]').click();
   assert.match(await page.locator('#em-one-location').textContent(),/羅馬書 · 第 8 章/);
   assert.equal(await page.locator('#emmaus').getAttribute('data-selected-book'),'45');
   assert.equal(await page.locator('#emmaus').getAttribute('data-selected-chapter'),'8');
   const dir=path.join(root,'artifacts/p2-emmaus-olive');fs.mkdirSync(dir,{recursive:true});
   await page.screenshot({path:path.join(dir,viewport.width+'-one-66-book-workbench.png')});
   await page.locator('#em-one-open').click();
   assert.equal(await page.locator('#em-one-workbench').isVisible(),true);
   assert.match(await page.locator('#em-one-frame').getAttribute('src'),/\/one\/\?book=45&chapter=8/);
   await page.frameLocator('#em-one-frame').locator('#one-cover').waitFor({timeout:30000});
   await page.screenshot({path:path.join(dir,viewport.width+'-one-original-app-in-p2.png')});
   await page.locator('#em-one-close').click();
   assert.equal(await page.locator('#em-one-workbench').isVisible(),false);
   assert.equal(errors.length,0,'workbench has no JavaScript page errors: '+errors.join(' / '));
   await page.close();
  }
  console.log('P2 Emmaus integrated ONE browser proof: pass');
 }finally{await browser.close()}
})().catch(err=>{console.error(err);process.exitCode=1});
