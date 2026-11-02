'use strict';
/* P2 03: actual ONE workstation + 66 volumes, without inner engraving. */
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..');
const read=p=>fs.readFileSync(path.join(root,'static',p),'utf8');
const html=read('experiments/p2-emmaus-olive-handoff-lab.html');
const css=read('css/p2-emmaus-one-workbench.css');
const js=read('js/p2-emmaus-one-workbench.js');
const host=read('js/p2-emmaus-olive-preview.js');
const editorial=read('js/p2-emmaus-editorial-context.js');
assert.match(html,/id="em-one-context"/,'the chapter displays a central ONE atlas and chronology');
assert.match(html,/id="emmaus-rail"/,'the 66-book index is restored and always visible');
assert.doesNotMatch(html,/id="em-book-drawer"/,'the distracting duplicate selection drawer is removed');
assert.match(html,/class="emmaus__scripture-frame"/,'a separate golden scripture frame encloses the entire folio');
assert.match(html,/LUKE 24:27/,'the gold folio frame is composed with its scripture');
assert.match(css,/#emmaus \.emmaus__scripture-frame\{/,'gold scripture frame is rendered as one structural element');
assert.match(css,/#emmaus \.emmaus__study\{[\s\S]*?box-shadow:none!important/,'ONE layout removes competing nested panel borders');
assert.match(css,/grid-template-columns:repeat\(22,minmax\(0,1fr\)\)!important/,'all 66 canonical books occupy 22 columns and 3 visible rows');
assert.match(css,/grid-template-rows:repeat\(3,minmax\(0,1fr\)\)!important/,'the index has exactly three rows');
assert.match(css,/grid-template-columns:minmax\(0,1\.12fr\) minmax\(0,\.88fr\)/,'the ONE atlas and chapter text use an actual two-column editorial grid');
assert.doesNotMatch(host,/rail\.scrollTo\(/,'book selection never hides the other 65 volumes');
assert.match(html,/id="em-one-open"/,'one primary action opens the original ONE workstation');
assert.doesNotMatch(html,/id="em-book-toggle"/,'no competing book-button action');
assert.match(html,/id="em-study-enter"[^>]*hidden/,'duplicate workbench link is hidden');
assert.match(editorial,/study\?\.map/,'the atlas reuses actual ONE chapter maps');
assert.match(editorial,/data\?\.events/,'chronology comes directly from canonical ONE data');
const canonicalLazy=read('js/p2-emmaus-one-data-lazy.js');
assert.match(canonicalLazy,/remaining-nt-epistles-complete\.js/,'Romans uses the original ONE epistle study module');
assert.match(canonicalLazy,/root\.addEventListener\('p2:one-selection'/,'ONE native study content reloads on selection');
assert.match(html,/p2-emmaus-one-data-lazy\.js/,'P2 loads canonical chapter material when a book is requested');
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
   assert.equal(await page.locator('#emmaus-rail').isVisible(),true,
    'the approved horizontal 66-book navigation must remain permanently visible');
   assert.equal(await page.locator('#emmaus-rail [data-book]').count(),66);
   const catalog=await page.locator('#emmaus-rail').evaluate(el=>{
    const rect=el.getBoundingClientRect(),style=getComputedStyle(el);
    const buttons=[...el.querySelectorAll('[data-book]')];
    const covered=buttons.map(b=>b.getBoundingClientRect()).filter(r=>
      r.width<12||r.height<9||r.left<rect.left-1||r.right>rect.right+1||
      r.top<rect.top-1||r.bottom>rect.bottom+1);
    return {visible:buttons.length,offscreen:covered.length,columns:style.gridTemplateColumns.split(' ').length,
      rows:style.gridTemplateRows.split(' ').length,
      scrollWidth:el.scrollWidth,clientWidth:el.clientWidth,
      scrollHeight:el.scrollHeight,clientHeight:el.clientHeight,
      lastVisible:buttons.at(-1)?.getBoundingClientRect().right<=rect.right+1,
      display:style.display
    };
   });
   assert.equal(catalog.display,'grid','all books must use the editorial grid, not a scrolling strip');
   assert.equal(catalog.visible,66);
   assert.equal(catalog.offscreen,0,'NO Bible book may extend outside the visible P2 magazine folio');
   assert(catalog.lastVisible,'Revelation book 66 must be fully on-screen');
   assert.equal(catalog.columns,viewport.width>900?22:6,'expected canonical grid column count');
   assert.equal(catalog.rows,viewport.width>900?3:11,'expected canonical grid row count');
   assert(catalog.scrollWidth<=catalog.clientWidth+2,'no horizontal scroll hides any book');
   assert(catalog.scrollHeight<=catalog.clientHeight+2,'no vertical scroll hides any book');
   const editorialGrid=await page.locator('#emmaus .emmaus__study-interface').evaluate(el=>({
     display:getComputedStyle(el).display,
     cols:getComputedStyle(el).gridTemplateColumns,
     title:document.querySelector('#emmaus .emmaus__identity')?.getBoundingClientRect().height
   }));
   assert.equal(editorialGrid.display,'grid','main reading folio must use designed grid');
   assert(editorialGrid.title>50,'EMMAUS retains a dominant editorial title');
   const frameDesign=await page.locator('#emmaus .emmaus__scripture-frame').evaluate(el=>({
    border:getComputedStyle(el).borderTopStyle,
    color:getComputedStyle(el).borderTopColor,
    bounds:el.getBoundingClientRect().toJSON()
   }));
   assert.equal(frameDesign.border,'solid','the whole left folio has one golden scripture outline');
   const oneControls=await page.locator('#emmaus .emmaus__one-toolbar button:visible').count();
   assert.equal(oneControls,1,'one primary ONE call-to-action, not repeated neon controls');
   // 66-volume selection is the original live rail; do not introduce a second UI.
   await page.locator('#emmaus-rail [data-book="45"]').evaluate(el=>el.click());
   await page.waitForTimeout(90);
   assert.equal(await page.locator('#em-one-chapter-grid button').count(),16,'Romans shows the real 16 chapters');
   await page.locator('#em-one-chapter-grid [data-one-chapter="8"]').click();
   await page.waitForFunction(()=>{
    const study=window.ONE_DATA?.studyBooks?.[45]?.chapterStudies?.['8'];
    return study?.title&&document.getElementById('emmaus-study-heading')?.textContent===study.title;
   },null,{timeout:18000});
   assert.equal(await page.locator('#em-context-map-title').count(),1,'ONE map pane is part of the actual left folio');
   const atlas=await page.locator('#em-context-time-title').textContent();
   assert(atlas?.length>0,'canonical timeline or actual book structure fills the centre');
   const eventCount=await page.locator('#em-context-time-events li').count();
   assert(eventCount>0,'ONE chronology or canonical book outline appears in the central space');
   const headline=await page.locator('#emmaus .emmaus__identity h1').textContent();
   assert.match(headline,/EMMAUS/,'Emmaus identity never gets replaced by selected book');

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
