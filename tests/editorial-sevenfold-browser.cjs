/* Sevenfold Westside editorial folios — real Hugo + Chromium layout acceptance.
   Screen captures are the acceptance evidence, not assertions of award quality. */
const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const origin=process.env.EDITORIAL_TEST_ORIGIN||'http://127.0.0.1:4186';
const realms=['church','journal','emmaus','olive','dawn-library','cinema','daylight-cafe'];
const screens=[{name:'desktop',width:1440,height:900},{name:'phone',width:390,height:844},{name:'small',width:320,height:720}];
(async()=>{
 fs.mkdirSync('artifacts/sevenfold-editorial',{recursive:true});
 const browser=await chromium.launch({headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 let checked=0;
 try{
   for(const realm of realms){
     const sizes= screens;
     for(const screen of sizes){
       const page=await browser.newPage({viewport:{width:screen.width,height:screen.height},deviceScaleFactor:1});
       const errors=[];page.on('pageerror',e=>errors.push(e.message));
       const path='/'+realm+'/folio/';
       const response=await page.goto(origin+path,{waitUntil:'domcontentloaded',timeout:50000});
       assert(response&&response.status()===200,realm+' should render at '+path);
       await page.evaluate(()=>document.fonts.ready);
       await page.waitForFunction(()=>{
         const frame=document.querySelector('.ws-interior__verse-composition');
         const d=frame?.contentDocument;
         return !!d?.body?.classList.contains('p2SevenfoldVertical')&&
           d.querySelectorAll('#formeZh .column>.piece.zh').length>0;
       },null,{timeout:70000});
       const m=await page.evaluate(()=>{
         const root=document.querySelector('.ws-interior');
         const hero=document.querySelector('.ws-interior__opening-text');
         const box=document.querySelector('.ws-interior__verse-frame');
         const a=hero.getBoundingClientRect(),b=box.getBoundingClientRect();
         const heading=document.querySelector('#ws-interior-heading');
         const head=heading.getBoundingClientRect();
         const frame=document.querySelector('.ws-interior__verse-composition');
         const doc=frame.contentDocument;
         const form=doc.querySelector('#formeZh');
         const plate=doc.querySelector('#plateZh');
         const p=plate.getBoundingClientRect();
         const glyphs=[...doc.querySelectorAll('#formeZh .column>.piece')].map(x=>x.getBoundingClientRect());
         const nav=[...document.querySelectorAll('.ws-interior__chapters a')];
         const cards=[...document.querySelectorAll('.ws-interior__index-list a')];
         const overlap=a.left<b.right-2&&a.right>b.left+2&&a.top<b.bottom-2&&a.bottom>b.top+2;
         const fonts=getComputedStyle(document.querySelector('.ws-interior__title-en')||document.querySelector('.ws-interior__church-en')).fontFamily;
         const quoteFont=getComputedStyle(doc.querySelector('#formeZh .piece.zh')).fontFamily;
         return{
           scrollWidth:document.documentElement.scrollWidth,
           root:root?.dataset.wsEditorialRealm,
           nav:nav.length,selected:nav.filter(x=>x.getAttribute('aria-current')==='page').length,
           links:cards.length,linksValid:cards.every(x=>x.getAttribute('href')?.startsWith('/')),
           square:Math.abs(b.width-b.height)<2,width:b.width,height:b.height,
           overlap,headingInside:head.left>=-2&&head.right<=innerWidth+2,
           sourceVerse:doc.querySelectorAll('#formeZh .piece.zh').length>0,
           vertical:doc.body.classList.contains('p2SevenfoldVertical')&&
             getComputedStyle(doc.querySelector('#formeZh .piece.zh')).writingMode==='vertical-rl',
           unrotated:!form.style.transform.includes('rotate('),
           glyphFit:glyphs.length>0&&glyphs.every(g=>g.left>=p.left-6&&g.right<=p.right+6&&g.top>=p.top-6&&g.bottom<=p.bottom+6),
           font:fonts,quoteFont,
           scope:getComputedStyle(root).getPropertyValue('--ws-interior-accent').trim(),
           gallery:document.querySelectorAll('.ws-interior__feature-art').length,
           imageReady:(()=>{
             const im=document.querySelector('.ws-interior__feature-art>img');
             return !im||im.complete&&im.naturalWidth>0;
           })()
         };
       });
       if(screen.name==='desktop')console.log('SEVENFOLD_METRICS',realm,JSON.stringify(m));
       assert(m.root===realm&&m.nav===7&&m.selected===1,realm+' must belong to complete 7-node navigation '+JSON.stringify(m));
       assert(m.links>=3&&m.linksValid&&m.gallery===1,realm+' needs real contents and feature');
       assert(m.imageReady,realm+' uses an unrenderable/404 illustration '+JSON.stringify(m));
       assert(m.square&&m.width>240&&m.headingInside,realm+' square/heading invalid '+JSON.stringify(m));
       assert(!m.overlap,realm+' title/verse overlap '+JSON.stringify(m));
       assert(m.vertical&&m.unrotated&&m.glyphFit,realm+' canonical Chinese vertical type clipping '+JSON.stringify(m));
       assert(m.scrollWidth<=screen.width+3,realm+' has horizontal document overflow '+JSON.stringify(m));
       assert(m.font.includes('Bodoni')&&m.quoteFont.includes('Chiron'),
         realm+' failed shared OS font role '+JSON.stringify(m));
       assert.equal(errors.length,0,realm+' browser runtime errors: '+errors.join('\n'));
       if(screen.name!=='small'){
         const img=page.locator('.ws-interior__feature-art img');
         if(await img.count()){
           await img.scrollIntoViewIfNeeded();
           await img.evaluate(async element=>{
             element.loading='eager';
             if(element.decode)await element.decode();
           });
           const art=await img.evaluate(element=>{
             const b=element.getBoundingClientRect(),s=getComputedStyle(element);
             return {width:b.width,height:b.height,opacity:s.opacity,display:s.display,
               visibility:s.visibility,src:element.currentSrc,loaded:element.naturalWidth>0};
           });
           assert(art.loaded&&art.width>70&&art.height>70&&art.display!=='none'&&art.visibility==='visible'&&Number(art.opacity)>.25,
             realm+' editorial artwork must actually be visible '+JSON.stringify(art));
           console.log('SEVENFOLD_ARTWORK',realm,JSON.stringify(art));
         }
         await page.locator('.ws-interior__feature-art').screenshot({
           path:'artifacts/sevenfold-editorial/'+realm+'-'+screen.name+'-feature.png',
           animations:'disabled',timeout:90000
         });
         await page.evaluate(()=>window.scrollTo(0,0));
         await page.screenshot({path:'artifacts/sevenfold-editorial/'+realm+'-'+screen.name+'.png',fullPage:true,animations:'disabled',timeout:90000});
         await page.locator('.ws-interior__opening').screenshot({
           path:'artifacts/sevenfold-editorial/'+realm+'-'+screen.name+'-opening.png',animations:'disabled',timeout:90000});
       }
       checked++;
       await page.close();
     }
   }
   console.log('SEVENFOLD_EDITORIAL_BROWSER_PASS',JSON.stringify({folios:realms.length,viewports:screens.map(x=>x.width),measurements:checked,screenshots:realms.length*4}));
 }finally{await browser.close()}
})().catch(e=>{console.error(e.stack||e);process.exit(1)});
