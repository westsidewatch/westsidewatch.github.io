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
const v5=read('css/p2-emmaus-editorial-v5.css');
const v6=read('css/p2-emmaus-scripture-v6.css');
const os=read('css/westside-design-os.css');
const osTokens=JSON.parse(fs.readFileSync(path.join(root,'design-system/tokens/westside.tokens.json'),'utf8'));
assert(host.includes('b.append(zh,en,numeral)'), 'book tiles must name their Chinese and English book before the number');
assert(!host.includes("b.innerHTML=String(item[0])"),'no number-only BOOK tiles');
assert(v6.includes('.emmaus__number-zh')&&v6.includes('.emmaus__number-en'),'bilingual book labels styled');
assert(v6.includes('--em-v6-gold-ink:color-mix'),'small gold font has contrast adjustment');
assert(html.includes('左右滑動選書'),'visible horizontal navigation hint');
assert.equal(osTokens.font['reading-zh'].$value[0],'Chiron Hei HK WS','canonical Chinese reading font is Chiron');
assert(!os.includes('Noto Serif TC'),'do not import forbidden Chinese font in Design OS runtime');
assert(!v6.includes('Georgia'),'English KJV must not silently use Georgia');
assert(!v6.includes('Noto Serif TC'),'Chinese P2 scripture must not use Noto Serif');
assert(!v6.includes('font:600'),'no extra-heavy Chinese P2 typography');

const verseJS=read('js/p2-emmaus-scripture-v6.js');
const lukeBilingual=JSON.parse(read('data/p2-emmaus-scripture-v6/Luke.json'));
const johnBilingual=JSON.parse(read('data/p2-emmaus-scripture-v6/John.json'));
for(const [index,chapters,data] of [[42,24,lukeBilingual],[43,21,johnBilingual]]){
 assert.equal(data.translations.cuv.bookId,index,'local Chinese CUV book identity is canonical');
 assert.equal(data.translations.kjv.bookId,index,'local English KJV book identity is canonical');
 assert.equal(data.translations.cuv.chapters.length,chapters,'CUV must cover the full Gospel');
 assert.equal(data.translations.kjv.chapters.length,chapters,'KJV must cover the full Gospel');
}
assert(html.includes('id="em-scripture-verses"'),'P2 includes bilingual verses');
assert(html.includes('p2-emmaus-scripture-v6.js'),'P2 loads the real verse reader');
assert(html.indexOf('id="em-one-chapter-grid"')<html.indexOf('class="emmaus__current-chapter"'),
 'chapter picker must sit under the selected Bible book');
assert(v6.includes('var(--ws-one-paper')&&v6.includes('var(--ws-night')&&v6.includes('var(--ws-first-light'),
 'P2 scripture uses canonical Design OS palette');
assert(verseJS.includes('translations.cuv')&&verseJS.includes('translations.kjv'),'real CUV and KJV verse pairs');
assert(verseJS.includes('raw.githubusercontent.com'),'pinned source for other books');

assert.match(html,/class="emmaus__book-switch emmaus__source-hero"/,
 'the selected Bible book has a real masthead below EMMAUS');
assert.match(html,/id="em-current-chapter-number"/,
 'current chapter has its own large, always-visible number');
assert.match(html,/id="em-current-chapter-zh"/,
 'current chapter has its Chinese ordinal');
assert.match(v5,/#emmaus \.emmaus__source-hero #em-book-en/,
 'selected English Bible book has intentional editorial typography');
assert.match(v5,/#emmaus #em-current-chapter-number/,
 'current chapter is a substantial visual anchor');
assert.match(v5,/grid-template-columns:minmax\(0,1\.62fr\) minmax\(0,\.88fr\)/,
 'scripture and research panels have deliberate 65/35 editorial proportions');
assert.match(html,/id="em-one-context"/,'the chapter displays a central ONE atlas and chronology');
assert.match(html,/id="emmaus-rail"/,'the 66-book index is restored and always visible');
assert.doesNotMatch(html,/id="em-book-drawer"/,'the distracting duplicate selection drawer is removed');
assert.match(html,/class="emmaus__scripture-frame"/,'a separate golden scripture frame encloses the entire folio');
assert.match(html,/LUKE 24:27/,'the gold folio frame is composed with its scripture');
assert.match(css,/#emmaus \.emmaus__scripture-frame\{/,'gold scripture frame is rendered as one structural element');
assert.match(css,/#emmaus \.emmaus__study\{[\s\S]*?box-shadow:none!important/,'ONE layout removes competing nested panel borders');
assert.match(css,/#emmaus \.emmaus__rail\{[\s\S]*?overflow-x:auto!important/,'the first P2 one-row 66-book scroll navigation is restored');
assert.match(css,/scroll-snap-type:x proximity!important/,'original horizontal canonical scroll snap is restored');
assert.match(css,/grid-template-columns:minmax\(0,1\.12fr\) minmax\(0,\.88fr\)/,'the ONE atlas and chapter text use an actual two-column editorial grid');
assert.match(host,/rail\.scrollTo\(\{left:Math\.max\(0,left\),behavior\}\)/,'selected volume scrolls to the centre in the original rail');
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
   assert.equal(await page.locator('#em-current-chapter-number').textContent(),'24');
   assert.equal(await page.locator('#em-current-chapter-zh').textContent(),'第二十四章');
   assert.equal(await page.locator('#em-one-chapter-grid').evaluate(el=>!!el.closest('.emmaus__book-current')),true,
    'chapter picker lives immediately beneath the selected book title');
   await page.waitForFunction(()=>document.querySelector('#emmaus')?.dataset.scriptureState==='ready'&&
    document.querySelector('#emmaus')?.dataset.scriptureBook==='42',{timeout:25000});
   const firstVerse=page.locator('#em-scripture-verses .emmaus__scripture-verse').first();
   assert.match(await firstVerse.locator('.emmaus__scripture-zh').textContent(),/七日/);
   assert.match(await firstVerse.locator('.emmaus__scripture-en').textContent(),/first day of the week/i);
   assert.equal(await page.locator('#em-scripture-verses .emmaus__scripture-verse').count(),53,
    'Luke 24 loads the actual canonical full chapter with 53 paired verse rows');

   const hero=await page.evaluate(()=>{
    const box=id=>document.querySelector(id).getBoundingClientRect();
    const a=box('#emmaus .emmaus__identity'),b=box('#emmaus .emmaus__source-hero'),
      c=box('#emmaus .emmaus__study');
    const font=id=>Number.parseFloat(getComputedStyle(document.querySelector(id)).fontSize);
    return {identity:{y:a.y,bottom:a.bottom},source:{y:b.y,bottom:b.bottom},
      study:{y:c.y,bottom:c.bottom},bookFont:font('#em-book-en'),
      chapterFont:font('#em-current-chapter-number'),subjectFont:font('#emmaus-study-heading')};
   });
   assert(hero.identity.bottom<=hero.source.y+3,'the 03 realm masthead precedes the selected book');
   assert(hero.source.bottom<=hero.study.y+3,'book/chapter masthead precedes study body');
   assert(hero.bookFont>hero.subjectFont,'selected book has stronger visual presence than study subject');
   assert(hero.chapterFont>hero.subjectFont,'selected chapter is not another tiny control');
   if(viewport.width>900){
    assert(hero.bookFont>=38,'selected book should read like a magazine feature title');
    assert(hero.chapterFont>=48,'chapter number is an unmistakable second visual anchor');
   }
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
   // Actual pointer hit testing, not element.click() dispatch: a visible page
   // with inert/pointer-events:none is a broken reader even if synthetic tests pass.
   assert.equal(await page.locator('#emmaus').evaluate(el=>el.inert),false,
     'Emmaus must accept real user input at the documented preview location');
   const nextVisible=page.locator('#emmaus-rail [data-book="43"]');
   await nextVisible.scrollIntoViewIfNeeded({timeout:10000});
   const targetInfo=await nextVisible.evaluate(el=>{
    const r=el.getBoundingClientRect(),hit=document.elementFromPoint(r.left+r.width/2,r.top+r.height/2);
    return {target:el.dataset.book,hit:el===hit||el.contains(hit)};
   });
   assert(targetInfo.hit,'book navigator must not be covered by an invisible blocking layer');
   await nextVisible.click({timeout:10000});
   await page.waitForFunction(()=>document.getElementById('em-book-zh')?.textContent==='約翰福音',
    null,{timeout:2500});
   assert.equal(await page.locator('#emmaus').getAttribute('data-selected-book'),'43',
    'a real mouse click must synchronously change the selected book');
   await page.locator('#emmaus-rail [data-book="42"]').click({timeout:10000});
   await page.waitForFunction(()=>document.getElementById('em-book-zh')?.textContent==='路加福音',
    null,{timeout:2500});

   const labeledRail=await page.locator('#emmaus-rail').evaluate(rail=>{
    const item=n=>{
     const el=rail.querySelector('[data-book="'+n+'"]'),zh=el?.querySelector('.emmaus__number-zh'),
      en=el?.querySelector('.emmaus__number-en'),idx=el?.querySelector('.emmaus__number-index');
     return {zh:zh?.textContent,en:en?.textContent,idx:idx?.textContent,
      zhVisible:getComputedStyle(zh).opacity,enVisible:getComputedStyle(en).opacity,
      direction:getComputedStyle(el).flexDirection};
    };
    return {mark:item(41),luke:item(42),john:item(43),acts:item(44),long:item(53)};
   });
   assert.deepEqual([labeledRail.mark.zh,labeledRail.mark.en,labeledRail.mark.idx],
    ['馬可福音','Mark','41'],'the navigation never requires memorizing the 41st book');
   assert.deepEqual([labeledRail.john.zh,labeledRail.john.en,labeledRail.john.idx],
    ['約翰福音','John','43'],'the bilingual book identity appears above its number');
   assert.equal(labeledRail.long.zh,'帖撒羅尼迦後書','long Chinese book labels are retained verbatim');
   for(const item of Object.values(labeledRail)){
    assert.equal(item.zhVisible,'1','every Chinese book name is always visible');
    assert.equal(item.enVisible,'1','every English book name is always visible');
    assert.equal(item.direction,'column','book names are stacked above the canon number');
   }

   const catalog=await page.locator('#emmaus-rail').evaluate(el=>({
     display:getComputedStyle(el).display,
     wrap:getComputedStyle(el).flexWrap,
     scrollWidth:el.scrollWidth,clientWidth:el.clientWidth,
     buttons:el.querySelectorAll('[data-book]').length,
     first:el.querySelector('[data-book="1"]')?.getBoundingClientRect().toJSON(),
     last:el.querySelector('[data-book="66"]')?.getBoundingClientRect().toJSON()
   }));
   assert.equal(catalog.display,'flex','the original 66-book one-row strip is restored');
   assert.equal(catalog.wrap,'nowrap','the book strip must never become a multi-row matrix');
   assert.equal(catalog.buttons,66);
   assert(catalog.scrollWidth>catalog.clientWidth*1.8,'all 66 books remain horizontally accessible in the original strip');
   assert(Math.abs(catalog.last.top-catalog.first.top)<3,'all 66 remain on one physical row');
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
   await page.screenshot({path:path.join(dir,viewport.width+'-emmaus-v5-book-chapter-hierarchy.png')});
   await page.locator('#emmaus-rail [data-book="43"]').evaluate(el=>el.click());
   await page.waitForTimeout(100);
   assert.equal(await page.locator('#em-book-en').textContent(),'John');
   assert.equal(await page.locator('#em-book-zh').textContent(),'約翰福音');
   assert.equal(await page.locator('#em-current-chapter-number').textContent(),'01');
   await page.locator('#em-one-chapter-grid [data-one-chapter="3"]').evaluate(el=>el.click());
   assert.equal(await page.locator('#em-current-chapter-number').textContent(),'03');
   assert.equal(await page.locator('#em-current-chapter-zh').textContent(),'第三章');
   await page.waitForFunction(()=>document.querySelector('#emmaus')?.dataset.scriptureState==='ready'&&
    document.querySelector('#emmaus')?.dataset.scriptureBook==='43'&&
    document.querySelector('#emmaus')?.dataset.scriptureChapter==='3',{timeout:25000});
   const johnFirst=page.locator('#em-scripture-verses .emmaus__scripture-verse').first();
   assert.match(await johnFirst.locator('.emmaus__scripture-zh').textContent(),/尼哥德慕/);
   assert.match(await johnFirst.locator('.emmaus__scripture-en').textContent(),/Nicodemus/i);
   assert.equal(await page.locator('#em-scripture-verses .emmaus__scripture-verse').count(),36,
    'John 3 contains 36 CUV/KJV verse pairs');
   await page.screenshot({path:path.join(dir,viewport.width+'-emmaus-v6-john-03-bilingual.png')});

   assert.match(await page.locator('#emmaus .emmaus__identity').textContent(),/EMMAUS/);
   await page.screenshot({path:path.join(dir,viewport.width+'-emmaus-v5-john-chapter-03.png')});
   await page.locator('#emmaus-rail [data-book="45"]').evaluate(el=>el.click());
   await page.locator('#em-one-chapter-grid [data-one-chapter="8"]').evaluate(el=>el.click());
   assert.equal(await page.locator('#em-current-chapter-number').textContent(),'08');
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
