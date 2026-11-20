/* Verify the actual P2 Sunday programme contains a visible architectural
   animation, both on desktop and on the one-column mobile Church page. */
const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const base=process.env.P2_TEST_ORIGIN||'http://127.0.0.1:4173';
(async()=>{
 const browser=await chromium.launch({headless:true,args:['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
 try{
  fs.mkdirSync('artifacts/p2-sunday-growth',{recursive:true});
  for(const screen of [{name:'desktop',width:1440,height:900},{name:'phone',width:390,height:844}]){
   const page=await browser.newPage({viewport:{width:screen.width,height:screen.height},deviceScaleFactor:1});
   const pageErrors=[];
   page.on('pageerror',e=>pageErrors.push(String(e)));
   page.on('console',msg=>{if(msg.type()==='error')pageErrors.push(msg.text())});
   await page.goto(base+'/p2/living-water.html?churchPreview=1',{waitUntil:'domcontentloaded',timeout:45000});
   await page.waitForTimeout(900);
   console.log('PAGE_DEBUG',screen.name,JSON.stringify(await page.evaluate(()=>({
     url:location.href,ready:document.readyState,stage:document.querySelector('.showcase')?.dataset.p2Phase,
     scripts:[...document.scripts].map(s=>s.src).filter(Boolean).slice(-9),
     frame:document.querySelector('.church-editorial__maquette')?.outerHTML.slice(0,240)
   }))),JSON.stringify(pageErrors));
   await page.screenshot({path:'artifacts/p2-sunday-growth/'+screen.name+'-before.png'});
   await page.waitForFunction(()=>document.querySelector('.showcase')?.dataset.p2Phase==='church',null,{timeout:12000});
   await page.waitForFunction(()=>!!document.querySelector('.church-editorial__maquette')?.getAttribute('src'),null,{timeout:12000});
   const result=await page.evaluate(()=>{
    const stage=document.querySelector('.showcase');
    const programme=document.querySelector('.church-schedule-source');
    const visual=document.querySelector('.church-editorial__visual');
    const frame=document.querySelector('.church-editorial__maquette');
    const rect=e=>{const r=e.getBoundingClientRect();return {x:r.x,y:r.y,width:r.width,height:r.height}};
    return {phase:stage.dataset.p2Phase,programme:!!programme,
      visualDisplay:getComputedStyle(visual).display,
      visual:rect(visual),frame:rect(frame),frameSrc:frame.src,
      scheduleDisplay:getComputedStyle(programme).display};
   });
   assert.equal(result.phase,'church',screen.name+' not showing the Church');
   assert.equal(result.programme,true,screen.name+' missing Sunday programme');
   assert.notEqual(result.visualDisplay,'none',screen.name+' hides the architectural model');
   assert.ok(result.visual.width>180&&result.visual.height>170,screen.name+' architectural model collapsed');
   assert.ok(result.frame.width>180&&result.frame.height>170,screen.name+' iframe collapsed');
   await page.screenshot({path:'artifacts/p2-sunday-growth/'+screen.name+'.png'});
   console.log(screen.name,'SUNDAY_MODEL_VISIBLE',JSON.stringify(result));
   await page.close();
  }
  // Verify the real homepage P2, which nests 04 → 01–03 → Church, not just
  // the standalone /p2/ HTML route.
  const home=await browser.newPage({viewport:{width:1440,height:900},deviceScaleFactor:1});
  await home.goto(base+'/',{waitUntil:'domcontentloaded',timeout:45000});
  await home.evaluate(()=>{
    const host=document.querySelector('.ws-p2-sevenfold-host');
    if(!host) throw new Error('P2 homepage section missing');
    window.scrollTo({top:window.scrollY+host.getBoundingClientRect().top+innerHeight*3.8,behavior:'instant'});
  });
  await home.waitForFunction(()=>{
    const o=document.querySelector('.ws-p2-sevenfold-host>iframe')?.contentDocument;
    const m=o?.getElementById('p2-0103-original')?.contentDocument||o;
    const inner=m?.getElementById('proof-original')?.contentDocument;
    const stage=inner?.querySelector('.showcase');
    const visual=inner?.querySelector('.church-editorial__visual');
    const model=inner?.querySelector('.church-editorial__maquette');
    return stage?.dataset.p2Phase==='church'&&
      visual&&getComputedStyle(visual).display!=='none'&&
      visual.getBoundingClientRect().width>200&&
      model?.getAttribute('src')?.includes('/p2-maquette/index.html');
  },{timeout:45000});
  await home.screenshot({path:'artifacts/p2-sunday-growth/homepage-real-p2.png'});
  console.log('HOMEPAGE_REAL_P2_SUNDAY_MODEL_VISIBLE');
  await home.close();
 } finally {await browser.close();}
})().catch(e=>{console.error(e);process.exit(1)});
