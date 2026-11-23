/* Browser proof: real Hugo output for the readable church site, single Sunday and QR/forms. */
const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const base=process.env.CHURCH_TEST_ORIGIN||'http://127.0.0.1:4174';
(async()=>{
 fs.mkdirSync('artifacts/church-visitor',{recursive:true});
 const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
 try{
  for(const screen of [{label:'desktop',width:1440,height:900},{label:'phone',width:390,height:844},{label:'small',width:320,height:720}]){
   const page=await browser.newPage({viewport:{width:screen.width,height:screen.height},deviceScaleFactor:1});
   const errors=[];page.on('pageerror',e=>errors.push(e.message));
   await page.goto(base+'/church/visit/',{waitUntil:'domcontentloaded',timeout:30000});
   await page.evaluate(()=>document.fonts.ready);
   await page.waitForFunction(()=>document.querySelectorAll('#church-ministry-list article').length===7
    &&document.querySelectorAll('#church-gathering-list article').length===4
    &&document.querySelectorAll('#church-sunday-live .ws-church-sunday-row').length===7
    &&document.querySelectorAll('[data-church-qr] canvas').length===4,null,{timeout:20000});
   const metrics=await page.evaluate(()=>{
    const story=document.querySelector('#church-sunday-live');
    const cards=[...document.querySelectorAll('[data-church-qr] canvas')];
    return {
      width:document.documentElement.scrollWidth,viewport:innerWidth,
      identity:(()=>{
       const zh=document.querySelector('.church-visit__official-artwork');
       const en=document.querySelector('.church-visit__identity-lockup .church-visit__english');
       if(!zh||!en)return false;
       const zhRect=zh.getBoundingClientRect(),enRect=en.getBoundingClientRect();
       const mask=getComputedStyle(zh).maskImage;
       return mask.includes('/images/living-water-west-church-name.png') &&
         zhRect.width>200 && zhRect.height>10 && enRect.top>=zhRect.bottom-2 &&
         en.textContent.trim()==='P.A.O.C. Living Water Assembly West';
      })(),
      archive:story?.textContent?.includes('歷史主日程序'),
      sunday:story?.querySelectorAll('.ws-church-sunday-row').length,
      ministries:document.querySelectorAll('.church-visit__ministry').length,
      gatherings:document.querySelectorAll('.church-visit__gathering').length,
      qr:cards.map(c=>({w:c.width,h:c.height,painted:(()=>{const data=c.getContext('2d').getImageData(20,20,1,1).data;return data[3]>0})()})),
      allLinks:[...document.querySelectorAll('.church-visit__intake-grid a')].map(x=>x.getAttribute('href'))
    };
   });
   assert(metrics.width<=screen.width+2,screen.label+' horizontal overflow '+JSON.stringify(metrics));
   assert(metrics.identity&&metrics.archive&&metrics.sunday===7&&metrics.ministries===7&&metrics.gatherings===4);
   assert.equal(metrics.qr.length,4);assert(metrics.qr.every(q=>q.w===164&&q.h===164&&q.painted));
   for(const type of ['join','decision','newcomer','prayer'])
     assert(metrics.allLinks.includes('/church/forms/?type='+type),screen.label+' missing '+type);
   assert.deepEqual(errors,[],screen.label+' JS errors');
   await page.screenshot({path:'artifacts/church-visitor/'+screen.label+'.png',fullPage:true,animations:'disabled'});
   await page.close();
  }
  const editor=await browser.newPage();
  await editor.goto(base+'/tools/church-schedule-editor.html',{waitUntil:'domcontentloaded'});
  await editor.waitForFunction(()=>document.querySelectorAll('#sunday-rows .schedule-row').length===7,null,{timeout:12000});
  assert.equal(await editor.locator('[name="status"]').inputValue(),'archive');
  assert.equal(await editor.locator('[name="date"]').inputValue(),'2026-10-11');
  await editor.screenshot({path:'artifacts/church-visitor/sunday-editor.png',fullPage:true});
  await editor.close();
  const form=await browser.newPage();
  await form.goto(base+'/church/forms/?type=decision',{waitUntil:'domcontentloaded'});
  await form.waitForFunction(()=>document.querySelector('#form-status')?.textContent?.includes('未開放'),null,{timeout:12000});
  assert.equal(await form.locator('#church-submit').isDisabled(),true,'No backend: form must fail closed');
  assert.equal(await form.locator('#form-title').textContent(),'信仰回應與決志');
  assert.equal(await form.locator('#church-gospel').isVisible(),true,'Gospel editorial pathway must be visible on decision');
  assert.equal(await form.locator('.church-form__gospel-step').count(),3,'Love, Cross and Faith steps required');
  assert.equal(await form.locator('[name="response"]').getAttribute('required'),'','Decision selection must be explicit');
  await form.screenshot({path:'artifacts/church-visitor/decision-form.png',fullPage:true});
  await form.close();
  console.log('CHURCH_VISITOR_BROWSER_PASS: full readable pages, archive guard, seven ministries, four offline QRs, editor and fail-closed forms');
 }finally{await browser.close();}
})().catch(error=>{console.error(error);process.exitCode=1;});
