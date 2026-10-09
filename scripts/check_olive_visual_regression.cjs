const {chromium}=require('playwright');
const fs=require('node:fs');
(async()=>{
 const browser=await chromium.launch({headless:true});
 const sizes=[{name:'mobile-narrow',width:320,height:640},{name:'mobile',width:390,height:844},{name:'mobile-landscape',width:844,height:390},{name:'tablet',width:768,height:1024},{name:'tablet-landscape',width:1024,height:768},{name:'desktop',width:1440,height:900},{name:'desktop-wide',width:1920,height:1080}];
 fs.mkdirSync('/tmp/olive-visual',{recursive:true});
 try{
  for(const size of sizes){
   const page=await browser.newPage({viewport:{width:size.width,height:size.height},deviceScaleFactor:1});
   const errors=[];
   page.on('pageerror',e=>errors.push('JavaScript: '+e.message));
   const response=await page.goto('http://127.0.0.1:8765/olive/',{waitUntil:'domcontentloaded'});
   if(!response?.ok())errors.push('Olive route HTTP '+response?.status());
   await page.locator('[data-pawson-play]').waitFor({timeout:12000});
   await page.screenshot({path:'/tmp/olive-visual/'+size.name+'.png',fullPage:true});
   const issues=await page.evaluate(()=>{
    const errors=[];
    if(document.documentElement.scrollWidth>innerWidth+2)errors.push('horizontal page overflow');
    const feature=document.querySelector('.olive-feature');
    const cards=[...document.querySelectorAll('.olive-speaker-card:not(.olive-speaker-card--clone)')];
    if(!feature)errors.push('canonical hero missing');
    if(cards.length!==11)errors.push('expected 11 rail cards plus David Pawson hero; got '+cards.length);
    if(!document.querySelector('[data-feature-next]')||!document.querySelector('[data-feature-prev]'))errors.push('rotation controls missing');
    if(!document.querySelector('[data-feature-source]'))errors.push('video source link missing');
    if(!document.querySelector('#olive-sermon-experience')||!document.querySelector('#olive-archive-experience'))errors.push('journey sections missing');
    for(const card of cards){const rect=card.getBoundingClientRect();if(rect.width<1||rect.height<1)errors.push('invisible speaker '+card.dataset.person);}
    return errors;
   });
   errors.push(...issues);
   const initial=await page.locator('.olive-feature__caption h2').innerText();
   await page.locator('[data-feature-next]').click();
   const after=await page.locator('.olive-feature__caption h2').innerText();
   if(initial===after)errors.push('next feature did not rotate speaker');
   const source=await page.locator('[data-feature-source]').getAttribute('href');
   if(!/^https:\/\/www\.youtube\.com\/watch\?v=[A-Za-z0-9_-]{11}$/.test(source||''))errors.push('feature source link invalid');
   await page.locator('[data-feature-prev]').click();
   if((await page.locator('.olive-feature__caption h2').innerText())!==initial)errors.push('previous feature did not restore speaker');
   // Exercise all eight feature selections without requiring YouTube network access.
   const visited=new Set();
   for(let i=0;i<8;i++){
    const sourceUrl=await page.locator('[data-feature-source]').getAttribute('href');
    const id=(sourceUrl||'').match(/[?&]v=([A-Za-z0-9_-]{11})/)?.[1];
    if(!id){errors.push('invalid video source at position '+i);break;}
    visited.add(id);
    await page.locator('[data-pawson-play]').click();
    const iframe=page.locator('[data-pawson-preview]');
    const embed=await iframe.getAttribute('src');
    if(!embed?.includes('/embed/'+id+'?'))errors.push('embed/source mismatch at position '+i);
    if(await iframe.isHidden())errors.push('iframe hidden after play at position '+i);
    await page.locator('[data-feature-next]').click();
    if(await iframe.getAttribute('src'))errors.push('old video continues after feature change '+i);
    if(!(await iframe.isHidden()))errors.push('iframe not hidden after feature change '+i);
   }
   if(visited.size!==8)errors.push('expected eight distinct video selections; got '+visited.size);
   console.log(size.name+': '+(errors.length?errors.join('; '):'PASS'));
   if(errors.length)process.exitCode=1;
   await page.close();
  }
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1});
