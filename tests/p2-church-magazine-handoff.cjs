// P2 production-bridge guard: the existing Church scene must finish first.
// All proof frames are actual, nested, same-origin Chromium renderings.
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const {chromium}=require('playwright');

const home=fs.readFileSync('layouts/partials/watch-home-editorial.html','utf8');
const bridge=fs.readFileSync('static/js/p2-magazine-live-bridge.js','utf8');
const church=fs.readFileSync('static/p2/living-water.html','utf8');
assert.match(home,/p2-main-0103-20261105/,'homepage must mount approved 01–03 runtime rather than the old 01–02-only iframe');
assert.match(home,/height:1034svh!important/,'P2 host must reserve the 03 Emmaus passage after Magazine');
assert.match(home,/magazineEnd=6\.5/,'Magazine movement must span separate pinned viewports');
assert.match(church,/p2-magazine-live-bridge\.js/,'church P2 must append the new Magazine bridge');
assert.match(bridge,/handoffVh=2\.37/,'the new magazine cannot replace the prior Church scene');
assert.match(bridge,/embedded\?4:5\.2/,'standalone P2 must also have ample room for Magazine');
assert.match(bridge,/MutationObserver/,'the bridge follows the existing P2 scroll clock');
assert.match(bridge,/magazine\.replaceChildren\(film,frame\)/,'replace only the retired Magazine placeholder with film and folio');
assert.match(bridge,/watch-cover-playback/,'the reused homepage film must pause offstage');
assert.match(bridge,/westside-p2-dual-progress/,'forward one scroll-owned clock to the approved magazine');

const out='artifacts/p2-church-magazine';
fs.mkdirSync(out,{recursive:true});
const screens=[['desktop',1648,928],['tablet',768,1024],['phone',390,844],['small',320,720]];
const stages=[['ocean',38],['church-open',55],['handoff',62],['star-ink',91],['contents',100],['reverse-church',55]];
const results=[];
const data=()=>{
 const frame=document.getElementById('p2-scene');
 const doc=frame.contentDocument;
 const root=doc?.querySelector('.showcase');
 const magazine=root?.querySelector('.p2-magazine');
 const titleFrame=magazine?.querySelector('iframe:not(.p2-magazine__home-film)');
 const final=titleFrame?.contentDocument;
 const fStage=final?.querySelector('#dual-stage');
 const water=root?.querySelector('.ocean-rise');
 const church=root?.querySelector('.church-editorial');
 const doors=root?.querySelector('.water-doors');
 return {
  rootPhase:root?.dataset.p2Phase||'',
  magazinePhase:magazine?.dataset.magazineStage||'',
  magazineProgress:+(root?.dataset.p2MagazineProgress||0),
  magazineVisibility:magazine?getComputedStyle(magazine).visibility:'missing',
  magazinePaper:magazine?.style.background||'',
  magazineChildren:magazine?.children.length||0,
  filmSrc:magazine?.querySelector('.p2-magazine__home-film')?.getAttribute('src')||'',
  filmOpacity:+(magazine?.querySelector('.p2-magazine__home-film')?.style.opacity||0),
  churchInert:church?.inert||false,
  churchVisible:church?getComputedStyle(church).visibility:'missing',
  waterVisible:water?getComputedStyle(water).visibility:'missing',
  waterLevel:+(root?.dataset.p2WaterLevel||0),
  doorsVisible:doors?getComputedStyle(doors).visibility:'missing',
  originalWater:!!root?.querySelector('.ocean-rise #upper')&&
   !!root?.querySelector('.ocean-rise #water-lower'),
  originalChurchSchedule:!!root?.querySelector('.church-schedule-source .sunday-schedule'),
  originalDoorCount:root?.querySelectorAll('.water-door').length||0,
  coverStage:fStage?.dataset.phase||'',
  activeDesign:final?.querySelector('#dual-contents')?.dataset.p2Design||'',
  count:final?.querySelectorAll('#p2-contents-design .p2x-entry').length||0,
  heroOriginal:!!final?.querySelector('.ws-print-hero__face[href="#ws-xiwang-vertical"]'),
  originalCover:!!final?.querySelector('#dual-cover .dual-cover__mast'),
  starInk:fStage?.dataset.starInkCoupling||'',
  scrollWidth:document.documentElement.scrollWidth
 };
};

(async()=>{
 const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
 try{
  for(const [screen,width,height] of screens){
   const page=await browser.newPage({viewport:{width,height}});
   const errors=[];
   page.on('pageerror',e=>errors.push(e.message));
   await page.goto('http://127.0.0.1:4173/experiments/p2-church-vol00-handoff-lab.html?p=38',
    {waitUntil:'domcontentloaded',timeout:45000});
   await page.waitForFunction(()=>{
    const child=document.querySelector('#p2-scene')?.contentDocument;
    return !!child?.querySelector('.showcase[data-p2-magazine-design] .p2-magazine iframe:not(.p2-magazine__home-film)')?.contentDocument?.querySelector('#dual-stage');
   },null,{timeout:30000});
   for(const [label,value] of stages){
    await page.locator('#progress').evaluate((input,p)=>{
     input.value=String(p);input.dispatchEvent(new Event('input',{bubbles:true}));
    },value);
    await page.waitForFunction(expected=>{
     const root=document.querySelector('#p2-scene')?.contentDocument?.querySelector('.showcase');
     if(!root)return false;
     const v=+(root.dataset.p2Progress||0);
     const target=expected<=75?expected/75*2.9:2.9+(expected/100-.75)/.25*1.1;
     // Above the 75% threshold the normalized input is 0..1.
     return Math.abs(v-target)<.014;
    },value,{timeout:5000});
    const m=await page.evaluate(data);
    const faults=[];
    if(!m.originalWater||!m.originalChurchSchedule||m.originalDoorCount!==2)
     faults.push('existing V75 water, Church Sunday schedule or Red Sea doors were replaced');
    if(m.scrollWidth>width+2)faults.push('handoff laboratory horizontal overflow');
    if(value===38&&!(m.rootPhase==='ocean-rise'&&m.waterVisible==='visible'&&
       m.waterLevel>.01&&m.waterLevel<1&&m.magazineVisibility==='hidden'))
     faults.push('the original moving water must own its stage before Magazine');
    if(value===55&&!(m.rootPhase==='red-sea'&&m.churchVisible==='visible'&&
       m.doorsVisible==='visible'&&m.magazineVisibility==='hidden'&&!m.churchInert))
     faults.push('the original Church and opening water doors must remain accessible on reverse');
    if(value===62&&!(m.rootPhase==='church-to-magazine'&&m.magazineProgress>0&&
       m.magazineProgress<.1&&m.magazineVisibility==='visible'&&m.churchInert&&
       m.filmOpacity===0&&m.magazinePaper==='transparent'))
     faults.push('the approved Magazine must begin only after the Church door is open');
    if(value===91&&!(m.magazineProgress>.7&&m.starInk==='single-rising-incision'&&m.heroOriginal))
     faults.push('the Morning Star must bring the original ink title into the spread');
    if(value===100&&!(m.magazineProgress>.999&&m.magazinePhase==='contents-final'&&
      m.coverStage==='contents-final'&&m.activeDesign==='10'&&m.count===12&&m.originalCover&&
      m.magazinePaper==='transparent'&&m.magazineChildren===2&&m.filmOpacity>.999&&
      m.filmSrc.startsWith('/preview/watch-city-vol00/hosanna/?cover=1')))
     faults.push('the live P2 must reach its genuine two-page cover and all twelve Contents desks');
    if(errors.length)faults.push('PAGE_ERROR '+errors.join('; '));
    await page.screenshot({path:path.join(out,screen+'-'+label+'.png'),animations:'allow'});
    results.push({id:screen+'-'+label,metrics:m,errors:faults});
    console.log(screen,label,faults.length?faults:'PASS');
   }
   await page.close();
  }
  // Main-site wheel integration: the native homepage iframe must now
  // contain 01 Church + 02 Magazine + 03 Emmaus, NOT merely link to a
  // working /experiments URL. The historical lab above is still tested.
  const homePage=await browser.newPage({viewport:{width:1440,height:900}});
  await homePage.goto('http://127.0.0.1:4173/',{waitUntil:'domcontentloaded',timeout:45000});
  await homePage.waitForFunction(()=>{
   const release=document.querySelector('.ws-p2-sevenfold-host>iframe')?.contentDocument;
   const root=release?.querySelector('#proof-original')?.contentDocument?.querySelector('.showcase');
   return !!release?.getElementById('emmaus')&&
    !!root?.querySelector('.p2-magazine iframe:not(.p2-magazine__home-film)')?.contentDocument?.querySelector('#dual-stage');
  },null,{timeout:30000});
  const realScroll=[
   ['church',2.65,'01',1.80,.01],
   ['magazine-start',3.10,'02',2.381,.02],
   ['star-rising',5.10,'02',3.333,.59],
   ['contents',6.40,'02',3.952,.97],
   ['emmaus-green-cover',7.30,'03',4.00,1],
   ['emmaus-dore',8.06,'03',4.00,1],
   ['emmaus-reading',9.30,'03',4.00,1],
   ['church-reverse',2.65,'01',1.80,.01]
  ];
  for(const [name,distance,expectedScene,wantVh,wantMagazine] of realScroll){
   await homePage.evaluate(d=>{
    const host=document.querySelector('.ws-p2-sevenfold-host');
    window.scrollTo({top:window.scrollY+host.getBoundingClientRect().top+innerHeight*d,behavior:'instant'});
   },distance);
   await homePage.waitForFunction(expected=>{
    const release=document.querySelector('.ws-p2-sevenfold-host>iframe')?.contentDocument;
    return release?.body.dataset.proofScene===expected;
   },expectedScene,{timeout:11000});
   await homePage.waitForTimeout(230);
   const state=await homePage.evaluate(()=>{
    const release=document.querySelector('.ws-p2-sevenfold-host>iframe')?.contentDocument;
    const root=release?.getElementById('proof-original')?.contentDocument?.querySelector('.showcase');
    const em=release?.getElementById('emmaus');
    return {scene:release?.body.dataset.proofScene,
      vh:+root?.dataset.p2Progress,magazine:+root?.dataset.p2MagazineProgress,
      originalDoors:root?.querySelectorAll('.water-door').length||0,
      schedule:!!root?.querySelector('.church-schedule-source .sunday-schedule'),
      emVisible:em?release.defaultView.getComputedStyle(em).visibility:'missing',
      oneBooks:release?.querySelectorAll('#emmaus-rail .emmaus__number').length||0,
      scriptureChars:release?.querySelector('#em-scripture-verses')?.textContent?.trim().length||0,
      hasOlive:!!release?.querySelector('#olive-proof')};
   });
   assert.equal(state.scene,expectedScene,name+': main homepage P2 scene incorrect');
   assert.equal(state.originalDoors,2,name+': original Red Sea doors disappeared');
   assert(state.schedule,name+': original Church schedule disappeared');
   assert(Math.abs(state.vh-wantVh)<.065,name+': original Church timing changed: '+JSON.stringify(state));
   assert(Math.abs(state.magazine-wantMagazine)<.065,name+': original Magazine timing changed: '+JSON.stringify(state));
   assert(!state.hasOlive,name+': 04 Olive must remain excluded');
   if(distance>=7.3){
    assert.equal(state.emVisible,'visible',name+': Emmaus is NOT on the actual homepage');
    assert.equal(state.oneBooks,66,name+': original 66-book ONE navigation not mounted');
   }
   if(name==='emmaus-reading')assert(state.scriptureChars>30,'ONE Chinese/KJV verses must render');
   if(name==='church-reverse')assert.equal(state.emVisible,'hidden','reverse scroll must hide Emmaus');
   await homePage.screenshot({path:path.join(out,'homepage-'+name+'.png'),animations:'allow'});
   console.log('HOME 01–03',name,'PASS',state);
  }
  await homePage.close();
 }finally{await browser.close()}
 fs.writeFileSync(path.join(out,'manifest.json'),JSON.stringify({scenes:results},null,2));
 if(results.some(s=>s.errors.length))process.exitCode=1;
})().catch(e=>{console.error(e);process.exitCode=1});
