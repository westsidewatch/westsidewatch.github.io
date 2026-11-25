/* Browser proof: real Hugo output for the readable church site, single Sunday and QR/forms. */
const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const base=process.env.CHURCH_TEST_ORIGIN||'http://127.0.0.1:4174';
(async()=>{
 fs.mkdirSync('artifacts/church-visitor',{recursive:true});
 const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
 try{
  for(const screen of [{label:'desktop',width:1440,height:900},{label:'laptop',width:1024,height:768},{label:'tablet',width:768,height:900},{label:'phone',width:390,height:844},{label:'small',width:320,height:720}]){
   const page=await browser.newPage({viewport:{width:screen.width,height:screen.height},deviceScaleFactor:1});
   const errors=[];page.on('pageerror',e=>errors.push(e.message));
   await page.goto(base+'/church/visit/',{waitUntil:'domcontentloaded',timeout:30000});
   await page.evaluate(()=>document.fonts.ready);
   await page.waitForFunction(()=>document.querySelectorAll('#church-ministry-list article').length===7
    &&document.querySelectorAll('#church-gathering-list article').length===4
    &&document.querySelectorAll('#church-sunday-live .ws-church-sunday-row').length===7
    &&document.querySelectorAll('[data-church-qr] canvas').length===4,null,{timeout:20000});
   await page.waitForFunction(()=>{
     const doc=document.querySelector('#church-letterpress')?.contentDocument;
     return doc?.body?.classList.contains('p2ChurchVertical')&&
       doc.querySelectorAll('#formeZh .column>.piece.zh').length>0;
   },null,{timeout:60000});
   const metrics=await page.evaluate(()=>{
    const story=document.querySelector('#church-sunday-live');
    const cards=[...document.querySelectorAll('[data-church-qr] canvas')];
    return {
      width:document.documentElement.scrollWidth,viewport:innerWidth,
      osGlass:(()=>{
        const tile=document.querySelector('.church-visit__scripture-tile');
        const card=document.querySelector('.church-visit__gathering');
        const os=getComputedStyle(document.body);
        const t=getComputedStyle(tile),g=getComputedStyle(card);
        const blur=s=>((s.backdropFilter||s.webkitBackdropFilter||'').includes('blur('));
        const heading=getComputedStyle(document.querySelector('.church-visit__section-head h2'));
        return blur(t)&&blur(g)&&
          getComputedStyle(card.querySelector('span')).fontFamily.includes('Chiron')&&
          heading.fontFamily.includes('Chiron')&&
          os.getPropertyValue('--ws-branch').trim().length>0;
      })(),
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
      geometry:(()=>{
        const box=node=>node.getBoundingClientRect();
        const region=document.querySelector('.church-visit__invitation');
        const heading=region.querySelector('h2');
        const headingText=document.createRange();headingText.selectNodeContents(heading);
        const ht=headingText.getBoundingClientRect();
        const cards=[...region.querySelectorAll('.church-visit__intake-grid article')].map(box);
        const intrudes=cards.some(rect=>ht.right>rect.left+1&&ht.left<rect.right-1
          &&ht.bottom>rect.top+1&&ht.top<rect.bottom-1);
        const headingFitsViewport=ht.left>=-2&&ht.right<=innerWidth+2;
        const tile=document.querySelector('.church-visit__scripture-tile');
        const tileBox=box(tile);
        const content=[...tile.querySelectorAll('.church-visit__tile-index,.church-visit__tile-chapter,blockquote,cite')].map(box);
        const tileContentFits=content.every(x=>x.top>=tileBox.top-2&&x.bottom<=tileBox.bottom+2);
        const tileOrderValid=content.every((x,i)=>i===0||content[i-1].bottom<=x.top+2);
        const translation=box(document.querySelector('.church-visit__scripture-translation'));
        const orphanCards=[...region.querySelectorAll('.church-visit__intake-grid h3')].filter(node=>{
          const text=node.firstChild;
          if(!text||text.nodeType!==Node.TEXT_NODE)return false;
          const lines=new Map();
          for(let i=0;i<text.length;i++){
            const range=document.createRange();
            range.setStart(text,i);range.setEnd(text,i+1);
            const rect=range.getBoundingClientRect();
            const key=Math.round(rect.top/3);
            lines.set(key,(lines.get(key)||0)+1);
          }
          return [...lines.values()].some(v=>v===1)&&text.length>2;
        }).map(x=>x.textContent.trim());
        return {
          tileWidth:tileBox.width,tileHeight:tileBox.height,
          tileContentFits,tileOrderValid,
          translationBelow:translation.top>=tileBox.bottom-2,
          invitationTitleOverlapsCards:intrudes,
          invitationTitleFitsViewport:headingFitsViewport,
          orphanCards,
          maxHeadingRight:Math.round(ht.right)
        };
      })(),
      motherForm:(()=>{
        const doc=document.querySelector('#church-letterpress')?.contentDocument;
        if(!doc)return {ready:false};
        const original=cls=>[...doc.querySelectorAll('#formeZh .piece.'+cls)].map(n=>n.dataset.original||n.textContent).join('');
        const plate=doc.querySelector('#plateZh');
        const box=plate.getBoundingClientRect();
        const glyphs=[...doc.querySelectorAll('#formeZh .column>.piece')].map(n=>n.getBoundingClientRect());
        const form=doc.querySelector('#formeZh');
        const zn=doc.querySelector('#formeZh .piece.zh');
        return {
          ready:true,mode:doc.body.classList.contains('p2ChurchVertical'),
          unrotated:form.style.transform.includes('scale(')&&!form.style.transform.includes('rotate('),
          verticalWriting:getComputedStyle(zn).writingMode==='vertical-rl',
          zh:original('zh').slice(0,70),en:original('en').slice(0,100),
          glyphsFit:glyphs.length>0&&glyphs.every(x=>x.left>=box.left-5&&x.top>=box.top-5&&
            x.right<=box.right+5&&x.bottom<=box.bottom+5),
          secondHidden:getComputedStyle(doc.querySelector('.impression:nth-child(2)')).display==='none',
          firstVisible:getComputedStyle(doc.querySelector('.impression:first-child')).display!=='none'
        };
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
   assert(metrics.osGlass,screen.label+' visitor glass blur + OS typography not active '+JSON.stringify(metrics));
   const gatheringGeometry=await page.locator('#church-gathering-list article').evaluateAll(nodes=>nodes.map(n=>{
     const r=n.getBoundingClientRect();return {x:r.x,y:r.y,w:r.width,h:r.height,bottom:r.bottom};
   }));
   if(screen.width>=1121){
     const [lead,...week]=gatheringGeometry;
     assert(week.every(r=>r.x>=lead.x+lead.w-2),'Weekday rhythm must be right of Sunday');
     assert(Math.abs(lead.y-week[0].y)<3&&Math.abs(lead.bottom-week[2].bottom)<3,'Sunday must span the three weekday rows');
   }else{
     assert(gatheringGeometry.every((r,i)=>i===0||r.y>=gatheringGeometry[i-1].bottom-2),'Narrow calendar must keep natural reading order');
   }

   assert(metrics.motherForm.ready&&metrics.motherForm.mode&&metrics.motherForm.unrotated&&
     metrics.motherForm.verticalWriting&&metrics.motherForm.secondHidden&&metrics.motherForm.firstVisible,
     screen.label+' failed to reuse V60 Chinese VERTICAL mother forme '+JSON.stringify(metrics.motherForm));
   assert(metrics.motherForm.zh.includes('信我的人')&&metrics.motherForm.en.includes('He that believeth'),
     screen.label+' mother forme verse mismatch '+JSON.stringify(metrics.motherForm));
   assert(metrics.motherForm.glyphsFit,screen.label+' letterpress clipping '+JSON.stringify(metrics.motherForm));
   const g=metrics.geometry;
   assert(Math.abs(g.tileWidth-g.tileHeight)<=2,screen.label+' opening Scripture must be 1:1 square '+JSON.stringify(g));
   assert(g.tileContentFits&&g.tileOrderValid&&g.translationBelow,
     screen.label+' square Scripture clips text or KJV translation '+JSON.stringify(g));
   assert(!g.invitationTitleOverlapsCards&&g.invitationTitleFitsViewport,
     screen.label+' invitation heading crushed or exceeds viewport '+JSON.stringify(g));
   assert.deepEqual(g.orphanCards,[],screen.label+' one-character CJK orphan card heading '+JSON.stringify(g));
   assert.equal(metrics.qr.length,4);assert(metrics.qr.every(q=>q.w===164&&q.h===164&&q.painted));
   for(const type of ['join','decision','newcomer','prayer'])
     assert(metrics.allLinks.includes('/church/forms/?type='+type),screen.label+' missing '+type);
   assert.deepEqual(errors,[],screen.label+' JS errors');
   await page.locator('.church-visit__scripture-group').screenshot({path:'artifacts/church-visitor/'+screen.label+'-letterpress.png',animations:'disabled'});
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
  const formGlass=await form.evaluate(()=>{
    const panel=getComputedStyle(document.querySelector('.church-form__gospel-step'));
    const title=getComputedStyle(document.querySelector('.church-form__gospel-head h2'));
    return (panel.backdropFilter||panel.webkitBackdropFilter||'').includes('blur(')
      &&title.fontFamily.includes('Chiron');
  });
  assert(formGlass,'Decision panels must use OS typography and backdrop blur');
  const collision=await form.evaluate(()=>{
    const title=document.querySelector('body[data-intake-type=decision] #form-title');
    const scripture=document.querySelector('.church-form__scripture-hint');
    const a=title.getBoundingClientRect(),b=scripture.getBoundingClientRect();
    return {
      spans:title.querySelectorAll('span').length,
      overlap:a.right>b.left+3&&a.left<b.right&&a.bottom>b.top+3&&a.top<b.bottom,
      titleWidth:a.width,scriptureLeft:b.left
    };
  });
  assert(collision.spans===2&&!collision.overlap,
    'Gospel title must split into two lines without overlapping Scripture '+JSON.stringify(collision));
  assert.equal(await form.locator('.church-form__gospel-step').count(),3,'Love, Cross and Faith steps required');
  for(const width of [1280,390,320]){
    await form.setViewportSize({width,height:850});
    const boxes=await form.locator('.church-form__gospel-step').evaluateAll(nodes=>nodes.map(n=>{
      const r=n.getBoundingClientRect();return {x:r.x,y:r.y,w:r.width,bottom:r.bottom};
    }));
    assert(boxes.every((r,i)=>i===0||r.y>=boxes[i-1].bottom-2),width+' Gospel passages must retain reading order');
    if(width>=1050)assert(boxes[1].w>boxes[0].w&&boxes[1].w>boxes[2].w,'Cross and resurrection must have editorial primacy');
  }

  assert.equal(await form.locator('.church-form__scripture-pair .church-form__scripture-hint').count(),2,'Decision must have two Scripture squares');
  assert.match(await form.locator('.church-form__scripture-hint--nahum').textContent(),/耶和華本為善.*認得那些投靠他的人/s);
  assert.match(await form.locator('.church-form__scripture-hint--nahum').textContent(),/The LORD is good, a strong hold in the day of trouble/);
  for(const width of [1280,390,320]){
    await form.setViewportSize({width,height:850});
    await form.evaluate(()=>document.fonts.ready);
    const squareMetrics=await form.evaluate(()=>[...document.querySelectorAll('.church-form__scripture-pair figure')].map(n=>{
      const b=n.getBoundingClientRect();
      const t=[...n.querySelectorAll('figcaption,blockquote,p,cite')].map(x=>x.getBoundingClientRect());
      return {width:b.width,height:b.height,contentFits:t.every(x=>
        x.left>=b.left-3&&x.right<=b.right+3&&x.top>=b.top-3&&x.bottom<=b.bottom+3)};
    }));
    assert(squareMetrics.length===2&&squareMetrics.every(s=>Math.abs(s.width-s.height)<2&&s.contentFits),
      width+'px decision Scripture squares clip '+JSON.stringify(squareMetrics));
    await form.locator('.church-form__scripture-pair').screenshot({
      path:'artifacts/church-visitor/decision-verses-'+width+'.png',animations:'disabled'
    });
  }
  await form.setViewportSize({width:1280,height:720});
  assert.equal(await form.locator('[name="response"]').getAttribute('required'),'','Decision selection must be explicit');
  await form.screenshot({path:'artifacts/church-visitor/decision-form.png',fullPage:true});
  await form.close();
  console.log('CHURCH_VISITOR_BROWSER_PASS: correct 1:1 verse square, no invitation collision/CJK orphans (1440/1024/768/390/320), original identity, seven ministries, four QRs');
 }finally{await browser.close();}
})().catch(error=>{console.error(error);process.exitCode=1;});
