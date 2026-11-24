/* Real-browser proof that DESIGN GRAMMAR == rendered website.
   Tests 7 distinct compositions and one freshly generated publication route. */
const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const base=process.env.EDITORIAL_TEST_ORIGIN||'http://127.0.0.1:4186';
const manifest=JSON.parse(fs.readFileSync('data/editorial/sevenfold.json','utf8'));
const realms=manifest.sequence;
const viewports=[{name:'desktop',width:1440,height:900},{name:'tablet',width:768,height:950},{name:'phone',width:390,height:844},{name:'small',width:320,height:720}];
(async()=>{
 fs.mkdirSync('artifacts/sevenfold-editorial',{recursive:true});
 const browser=await chromium.launch({headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 let checks=0;
 try{
  for(const realm of realms){
   const data=JSON.parse(fs.readFileSync('data/editorial/grammar/'+realm+'.json','utf8'));
   for(const viewport of viewports){
    const page=await browser.newPage({viewport:{width:viewport.width,height:viewport.height},deviceScaleFactor:1});
    const errors=[];page.on('pageerror',e=>errors.push(e.message));
    const response=await page.goto(base+'/'+realm+'/folio/',{waitUntil:'domcontentloaded',timeout:50000});
    assert.equal(response.status(),200,realm+' page must really exist on Hugo');
    await page.evaluate(()=>document.fonts.ready);
    const computed=await page.evaluate(()=>{
      const cover=document.querySelector('.ws-gram-cover');
      const title=document.querySelector('#ws-grammar-title');
      const article=document.querySelector('.ws-grammar');
      const rect=x=>x.getBoundingClientRect();
      const t=rect(title);
      const cv=rect(cover);
      const blocks=[...document.querySelectorAll('.ws-grammar__body [data-type]')];
      const img=[...cover.querySelectorAll('img')];
      return {
       realm:article?.dataset.wsEditorialRealm,
       cover:cover?.dataset.mode,
       blockTypes:blocks.map(x=>x.dataset.type),
       width:document.documentElement.scrollWidth,
       titleWithin:t.left>=-2&&t.right<=innerWidth+2,
       titleClipped:t.height>0&&t.bottom<=cv.bottom+3,
       fontZh:getComputedStyle(document.querySelector('.ws-gram-cover__title-zh')||document.querySelector('.ws-gram-cover__title-en')).fontFamily,
       fontEn:getComputedStyle(document.querySelector('.ws-gram-cover__title-en')).fontFamily,
       assetCount:img.length,
       masthead:!!document.querySelector('.ws-grammar__masthead img'),
       navAvailable:!!document.querySelector('.ws-grammar__directory summary')
      };
    });
    assert.equal(computed.realm,realm);
    assert.equal(computed.cover,data.cover.mode);
    assert.deepEqual(computed.blockTypes,data.blocks.map(x=>x.type),realm+' markup must follow editable JSON composition order');
    assert(computed.width<=viewport.width+3,realm+' page horizontally overflows at '+viewport.width+': '+JSON.stringify(computed));
    assert(computed.titleWithin&&computed.titleClipped,realm+' cover title clips at '+viewport.width+': '+JSON.stringify(computed));
    assert(computed.fontEn.includes('Bodoni'),realm+' English OS font not present');
    assert(computed.masthead&&computed.navAvailable);
    if(realm!=='church')assert(computed.assetCount>=1,realm+' actual cover image absent');
    await page.locator('.ws-grammar__directory summary').click();
    assert.equal(await page.locator('.ws-grammar__directory nav a').count(),7,'Full sevenfold navigation required');
    assert.equal(await page.locator('.ws-grammar__directory nav a[aria-current=page]').count(),1);
    await page.locator('.ws-grammar__directory summary').click();
    for(const block of data.blocks){
      const node=page.locator('#'+block.id);
      assert.equal(await node.getAttribute('data-type'),block.type,'Block not compiled from JSON');
      assert.equal(await node.getAttribute('data-mode'),block.mode,'Composition mode ignored');
      if(block.type==='scripture'){
        await node.locator('iframe').scrollIntoViewIfNeeded();
        await page.waitForFunction(id=>{
          const iframe=document.querySelector('#'+id+' iframe');
          const inner=iframe?.contentDocument;
          return inner?.body?.classList.contains('p2SevenfoldVertical')&&
            inner.querySelectorAll('#formeZh .piece.zh').length>0;
        },block.id,{timeout:70000});
        const m=await node.evaluate(el=>{
          const s=el.querySelector('.ws-gram-scripture__square').getBoundingClientRect();
          const d=el.querySelector('iframe').contentDocument;
          const f=d.querySelector('#formeZh');
          return {
            square:Math.abs(s.width-s.height)<2,
            cjkVertical:getComputedStyle(d.querySelector('#formeZh .piece.zh')).writingMode==='vertical-rl',
            unchanged:!f.style.transform.includes('rotate('),
            originalFont:getComputedStyle(d.querySelector('#formeZh .piece.zh')).fontFamily.includes('Chiron')
          };
        });
        assert(Object.values(m).every(Boolean),'Original scripture V60 mother-form not actually reused: '+JSON.stringify(m));
      }
      if(block.type==='plate'){
        const img=node.locator('img');
        await img.scrollIntoViewIfNeeded();
        await img.evaluate(async x=>{x.loading='eager';if(x.decode)await x.decode()});
        const m=await img.evaluate(x=>({loaded:x.naturalWidth>0,w:x.getBoundingClientRect().width,h:x.getBoundingClientRect().height}));
        assert(m.loaded&&m.w>75&&m.h>75,'Editorial asset invisible even though URL exists '+JSON.stringify(m));
      }
    }
    if(viewport.name==='desktop'||viewport.name==='phone'){
      const images=page.locator('.ws-gram-cover__visual img');
      if(await images.count())await images.first().evaluate(async img=>{img.loading='eager';if(img.decode)await img.decode()});
      await page.evaluate(()=>window.scrollTo(0,0));
      await page.screenshot({path:'artifacts/sevenfold-editorial/'+realm+'-'+viewport.name+'.png',fullPage:true,animations:'disabled',timeout:90000});
      await page.locator('.ws-gram-cover').screenshot({path:'artifacts/sevenfold-editorial/'+realm+'-'+viewport.name+'-cover.png',animations:'disabled',timeout:90000});
    }
    assert.equal(errors.length,0,realm+' JS errors: '+errors.join('\n'));
    if(viewport.name==='desktop')console.log('EDITORIAL_GRAMMAR_METRICS',realm,JSON.stringify(computed));
    checks++;await page.close();
   }
  }
  const generated=await browser.newPage({viewport:{width:1280,height:850}});
  const r=await generated.goto(base+'/journal/grammar-proof/',{waitUntil:'domcontentloaded',timeout:40000});
  assert.equal(r.status(),200,'One-command generator must produce a *new actual website*');
  assert.equal(await generated.locator('.ws-grammar').getAttribute('data-ws-grammar'),'journal-grammar-proof');
  assert.match(await generated.locator('h1').textContent(),/編輯語法實作驗證/);
  assert.equal(await generated.locator('.ws-grammar__body [data-type]').count(),2);
  await generated.screenshot({path:'artifacts/sevenfold-editorial/generated-new-page.png',fullPage:true,animations:'disabled',timeout:90000});
  await generated.close();
  console.log('EDITORIAL_GRAMMAR_BROWSER_PASS',JSON.stringify({realms:7,responsiveWidths:viewports.map(x=>x.width),verifiedPages:checks+1,newRoute:'/journal/grammar-proof/'}));
 }finally{await browser.close()}
})().catch(e=>{console.error(e.stack||e);process.exit(1)});
