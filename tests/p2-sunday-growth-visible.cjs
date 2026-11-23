/* Verify the actual P2 Sunday programme contains a visible architectural
   animation, both on desktop and on the one-column mobile Church page. */
const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const base=process.env.P2_TEST_ORIGIN||'http://127.0.0.1:4173';
(async()=>{
 const browser=await chromium.launch({headless:true,args:['--no-sandbox','--enable-webgl','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
 try{
  fs.mkdirSync('artifacts/p2-sunday-growth',{recursive:true});
  for(const screen of [{name:'desktop',width:1440,height:900},{name:'reference-screenshot',width:1158,height:850},{name:'phone',width:390,height:844}]){
   const page=await browser.newPage({viewport:{width:screen.width,height:screen.height},deviceScaleFactor:1});
   const pageErrors=[];
   page.on('pageerror',e=>pageErrors.push(String(e)));
   page.on('response',r=>{if(r.status()===404)console.log('P2_ASSET_404',screen.name,r.url())});
   page.on('console',msg=>{if(msg.type()==='error')pageErrors.push(msg.text())});
   await page.goto(base+'/p2/living-water.html?churchPreview=1',{waitUntil:'domcontentloaded',timeout:45000});
   await page.waitForTimeout(900);
   console.log('PAGE_DEBUG',screen.name,JSON.stringify(await page.evaluate(()=>({
     url:location.href,ready:document.readyState,stage:document.querySelector('.showcase')?.dataset.p2Phase,
     scripts:[...document.scripts].map(s=>s.src).filter(Boolean).slice(-9),
     frame:document.querySelector('.church-editorial__maquette')?.outerHTML.slice(0,240)
   }))),JSON.stringify(pageErrors));
   // Opt-in churchPreview=1 deliberately starts at pose 2.37 (Red Sea open),
   // when the original white GLB MUST still be hidden. Move to mid-build.
   await page.evaluate(()=>{const d=(2.885-2.37)/.58*innerHeight;window.scrollTo({top:d,behavior:'instant'});});
   await page.waitForFunction(()=>document.querySelector('.showcase')?.classList.contains('p2-church-model-visible'),null,{timeout:12000});
   await page.waitForFunction(()=>!!document.querySelector('.church-editorial__maquette')?.getAttribute('src'),null,{timeout:12000});
   const result=await page.evaluate(()=>{
    const stage=document.querySelector('.showcase');
    const programme=document.querySelector('.church-schedule-source');
    const visual=document.querySelector('.church-editorial__visual');
    const copy=document.querySelector('.church-editorial__copy');
    const figure=document.querySelector('.church-schedule-maquette');
    const frame=document.querySelector('.church-editorial__maquette');
    const ocean=document.querySelector('.ocean-rise #upper');
    const lastVerse=document.querySelector('.schedule-theme-scripture p:last-child');
    const themeTitle=document.querySelector('.schedule-theme-scripture h3');
    const rect=e=>{const r=e.getBoundingClientRect();return {x:r.x,y:r.y,width:r.width,height:r.height,bottom:r.bottom,right:r.right}};
    return {phase:stage.dataset.p2Phase,modelActive:stage.classList.contains('p2-church-model-visible'),programme:!!programme,
      leftContainsModel:visual.contains(frame),rightHasNoModel:!copy.contains(frame),
      leftWaterEngravingPreserved:!!ocean, 
      originalSundayRows:document.querySelectorAll('.worship-row').length,
      allThreeScriptures:!!lastVerse&&!!themeTitle&&
        document.querySelector('.schedule-theme-scripture').textContent.includes('以弗所書 5:20')&&
        document.querySelector('.schedule-theme-scripture').textContent.includes('帖撒羅尼迦前書 5:16–18')&&
        document.querySelector('.schedule-theme-scripture').textContent.includes('腓立比書 4:6–7'),
      visual:rect(visual),right:rect(copy),figure:rect(figure),frame:rect(frame),frameSrc:frame.src,
      finalVerse:rect(lastVerse),themeTitle:rect(themeTitle), 
      copyScrollHeight:copy.scrollHeight,copyClientHeight:copy.clientHeight,
      scheduleDisplay:getComputedStyle(programme).display};
   });
   console.log('P2_FULL_LAYOUT_METRICS',screen.name,JSON.stringify(result));
   assert.equal(result.modelActive,true,screen.name+' not displaying the Church visual');
   assert.equal(result.programme,true,screen.name+' missing Sunday programme');
   assert.equal(result.leftContainsModel,true,screen.name+' model absent from LEFT water-engraving pane');
   assert.equal(result.rightHasNoModel,true,screen.name+' model still consumes RIGHT programme space');
   assert.equal(result.leftWaterEngravingPreserved,true,screen.name+' water engraving removed');
   assert.equal(result.originalSundayRows,7,screen.name+' lost Sunday worship rows');
   assert.equal(result.allThreeScriptures,true,screen.name+' lost a scripture quotation');
   if(screen.width>700){
     assert.ok(result.figure.width>180&&result.figure.height>150,screen.name+' model illustration collapsed');
     assert.ok(result.figure.x>=result.visual.x-2&&result.figure.right<=result.visual.right+2,screen.name+' not inside left water field');
     assert.ok(result.figure.y>=result.visual.y+result.visual.height*.55,screen.name+' model is not LOWER-LEFT');
     assert.ok(result.figure.bottom<=result.visual.bottom-10,screen.name+' model clips out of left field');
     assert.ok(result.finalVerse.bottom<=result.right.bottom+2,screen.name+' final scripture clipped at bottom');
     assert.ok(result.copyScrollHeight<=result.copyClientHeight+3,screen.name+' programme still requires internal scrolling at full desktop height');
   }else{
     // On phone, the single reading column scrolls; no model may cover text.
     assert.equal(result.visual.width,0,'phone must prioritize Sunday reading');
   }
   console.log(screen.name,'SUNDAY_MODEL_LOWER_LEFT_ALL_SCRIPTURES',JSON.stringify(result));
   await page.close();
  }
  // Verify the real homepage P2, which nests 04 → 01–03 → Church, not just
  // the standalone /p2/ HTML route.
  const home=await browser.newPage({viewport:{width:1440,height:900},deviceScaleFactor:1});
  await home.goto(base+'/',{waitUntil:'domcontentloaded',timeout:45000});
  await home.evaluate(()=>{
    const host=document.querySelector('.ws-p2-sevenfold-host');
    if(!host) throw new Error('P2 homepage section missing');
    window.scrollTo({top:window.scrollY+host.getBoundingClientRect().top+innerHeight*3.09,behavior:'instant'});
  });
  await home.waitForFunction(()=>{
    const o=document.querySelector('.ws-p2-sevenfold-host>iframe')?.contentDocument;
    const m=o?.getElementById('p2-0103-original')?.contentDocument||o;
    const inner=m?.getElementById('proof-original')?.contentDocument;
    const stage=inner?.querySelector('.showcase');
    const water=inner?.querySelector('.ocean-rise #upper');
    const right=inner?.querySelector('.church-editorial__copy');
    const left=inner?.querySelector('.church-editorial__visual');
    const figure=left?.querySelector('.church-schedule-maquette');
    const model=figure?.querySelector('.church-editorial__maquette');
    const last=right?.querySelector('.schedule-theme-scripture p:last-child');
    return stage?.classList.contains('p2-church-model-visible')&&
      !!water&&!!right&&!!left&&left.contains(model)&&!right.contains(model)&&
      figure?.getBoundingClientRect().y>left.getBoundingClientRect().height*.55&&
      !!last&&last.getBoundingClientRect().bottom<=right.getBoundingClientRect().bottom+3&&
      model?.getAttribute('src')?.includes('/p2-maquette/index.html');
  },{timeout:45000});
  console.log('HOMEPAGE_P2_MODEL_LOWER_LEFT_TEXT_VISIBLE');
  await home.close();
 } finally {await browser.close();}
})().catch(e=>{console.error(e);process.exit(1)});
