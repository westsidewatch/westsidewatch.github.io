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
   await page.waitForFunction(() => [...document.querySelectorAll('.olive-speaker-card:not(.olive-speaker-card--clone)')].every(card => !!card.querySelector('.olive-speaker-card__editorial')),null,{timeout:15000});
   // Horizontal editorial rails intentionally lazy-load off-screen posters.
   // Request their decoding for the screenshot audit without changing production behavior.
   const imageReport=await page.evaluate(async () => {
    const cards=[...document.querySelectorAll('.olive-speaker-card:not(.olive-speaker-card--clone)')];
    return await Promise.all(cards.map(async card => {
     const img=card.querySelector('.olive-speaker-card__editorial');
     img.loading='eager';
     try { await img.decode(); } catch (_) {}
     return {speaker:card.dataset.person,src:img.currentSrc||img.src,loaded:img.complete&&img.naturalWidth>0};
    }));
   });
   for(const item of imageReport)if(!item.loaded)errors.push('editorial image failed to load '+item.speaker+': '+item.src);
    try {
     await page.waitForFunction(() => document.querySelectorAll('.olive-poster-gallery .olive-gallery-card').length===12,null,{timeout:15000});
    } catch (error) {
     const diagnostic=await page.evaluate(() => ({
      railCards:document.querySelectorAll('.olive-speaker-card:not(.olive-speaker-card--clone)').length,
      galleryCards:document.querySelectorAll('.olive-poster-gallery .olive-gallery-card').length,
      galleryPresent:!!document.querySelector('.olive-poster-gallery'),
      rootPresent:!!document.querySelector('.olive-archive'),
      scripts:[...document.querySelectorAll('script[src*="olive-"]')].map(el=>el.src),
      speakerNames:[...document.querySelectorAll('.olive-speaker-card:not(.olive-speaker-card--clone)')].map(el=>el.dataset.person)
     }));
     await page.screenshot({path:'/tmp/olive-visual/'+size.name+'-gallery-failure.png',fullPage:true});
     throw new Error('Olive poster gallery initialization failed: '+JSON.stringify({diagnostic,errors,cause:error.message}));
    }
   // Image decoding alone does not prove the editorial poster is visually visible.
   // Verify stacking, dimensions and actual hit-tested paint at the card center.
   const visibility=await page.evaluate(() => [...document.querySelectorAll('.olive-speaker-card:not(.olive-speaker-card--clone)')].map(card => {
    const img=card.querySelector('.olive-speaker-card__editorial');
    if(!img)return {speaker:card.dataset.person,error:'missing editorial image'};
    const cardBox=card.getBoundingClientRect(),box=img.getBoundingClientRect(),style=getComputedStyle(img);
    const railBoxForHit=card.closest('.olive-speaker-rail')?.getBoundingClientRect();
    const left=Math.max(0,cardBox.left,railBoxForHit?.left??0),right=Math.min(innerWidth,cardBox.right,railBoxForHit?.right??innerWidth);
    const topEdge=Math.max(0,cardBox.top,railBoxForHit?.top??0),bottomEdge=Math.min(innerHeight,cardBox.bottom,railBoxForHit?.bottom??innerHeight);
    const x=(left+right)/2,y=(topEdge+bottomEdge)/2;
    const railBox=card.closest('.olive-speaker-rail')?.getBoundingClientRect();
    const visibleInViewport=!!railBox&&cardBox.right>railBox.left&&cardBox.left<railBox.right&&cardBox.bottom>railBox.top&&cardBox.top<railBox.bottom&&cardBox.right>0&&cardBox.left<innerWidth&&cardBox.bottom>0&&cardBox.top<innerHeight;
    const top=visibleInViewport?document.elementFromPoint(x,y):null;
    const hit=right>left&&bottomEdge>topEdge&&(top===img||img.contains(top)||card.contains(top));
    return {speaker:card.dataset.person,visibleInViewport,hit,opacity:style.opacity,visibility:style.visibility,display:style.display,width:box.width,height:box.height,loaded:img.complete&&img.naturalWidth>0};
   }));
   for(const item of visibility){
    if(item.visibleInViewport&&(!item.loaded||item.display==='none'||item.visibility==='hidden'||Number(item.opacity)===0||item.width<1||item.height<1||!item.hit))
     errors.push('poster visually obscured '+JSON.stringify(item));
   }
   await page.screenshot({path:'/tmp/olive-visual/'+size.name+'.png',fullPage:true});
   const issues=await page.evaluate(()=>{
    const errors=[];
    if(document.documentElement.scrollWidth>innerWidth+2)errors.push('horizontal page overflow');
    const feature=document.querySelector('.olive-feature');
    const cards=[...document.querySelectorAll('.olive-speaker-card:not(.olive-speaker-card--clone)')];
    if(!feature)errors.push('canonical hero missing');
    if(cards.length!==12)errors.push('expected 12 unique speaker cards including David Pawson; got '+cards.length);
    if(new Set(cards.map(card=>card.dataset.person)).size!==12)errors.push('speaker rail contains duplicate or unnamed cards');
    if(document.querySelectorAll('.olive-poster-gallery .olive-gallery-card').length!==12)errors.push('twelve-speaker poster gallery missing');
    for(const poster of document.querySelectorAll('.olive-poster-gallery .olive-gallery-card')){
      const en=poster.querySelector('.olive-gallery-card__identity-en');
      const zh=poster.querySelector('.olive-gallery-card__identity-zh');
      if(!en?.textContent?.trim()||!zh?.textContent?.trim())errors.push('missing bilingual poster identity');
      else if(getComputedStyle(en).display==='none'||getComputedStyle(zh).display==='none'||en.getBoundingClientRect().height<1||zh.getBoundingClientRect().height<1)errors.push('hidden bilingual poster identity');
    }
    if(document.querySelector('#olive-archive-experience')||document.querySelector('.olive-journey-nav')||document.querySelector('.olive-journey-heading'))errors.push('internal journey taxonomy leaked into visible page');
    for(const card of cards){
      const rect=card.getBoundingClientRect();
      if(rect.width<1||rect.height<1)errors.push('invisible speaker '+card.dataset.person);
      const img=card.querySelector('.olive-speaker-card__editorial');
      if(img){
        const style=getComputedStyle(img);
        if(style.objectFit!=='contain')errors.push('poster cropped '+card.dataset.person);
        if(Math.abs(rect.width/rect.height-.75)>.04)errors.push('poster aspect ratio '+card.dataset.person+': '+(rect.width/rect.height).toFixed(2));
      }
    }
    // The approved poster rail intentionally overlays the hero media.
    // Verify it stays within the stage rather than rejecting the editorial overlap.
    const rail=document.querySelector('.olive-speaker-rail')?.getBoundingClientRect();
    const stage=document.querySelector('.olive-home-stage')?.getBoundingClientRect();
    if(rail&&stage&&(rail.top<stage.top-3||rail.bottom>stage.bottom+3))errors.push('poster rail escapes hero stage');
    const gallery=[...document.querySelectorAll('.olive-poster-gallery .olive-gallery-card')];
    if(gallery.length!==12)errors.push('expected twelve gallery posters; got '+gallery.length);
    if(document.querySelector('.olive-journey-screen'))errors.push('placeholder green theater screen remains');
    return errors;
   });
   errors.push(...issues);
   // Selecting a speaker must switch the home channel without leaving /olive/.
   // The speaker rail moves continuously by design: Playwright's default
   // stable-element click cannot target a moving card. Pause only for the
   // test's pointer selection, without disabling the production animation.
   const selectSpeaker=async name=>{
    const selector='.olive-speaker-card:not(.olive-speaker-card--clone)[data-person="'+name+'"]';
    await page.locator(selector).evaluate(el=>{
     const rail=el.closest('.olive-speaker-rail');
     if(rail)rail.style.setProperty('animation-play-state','paused','important');
     for(const node of rail?.querySelectorAll('*')||[])node.style.setProperty('animation-play-state','paused','important');
    });
    await page.locator(selector).click({force:true,timeout:5000});
   };
   await selectSpeaker('江秀琴');
   if((await page.locator('.olive-feature__caption h2').innerText())!=='江秀琴')errors.push('speaker card did not select its home channel');
   if(!page.url().endsWith('/olive/'))errors.push('speaker card navigated away from home');
   if(await page.locator('.olive-feature__channel .olive-feature__episode').count()<1)errors.push('selected channel episodes missing');
   await selectSpeaker('倪柝聲');
   if((await page.locator('.olive-feature__caption h2').innerText())!=='倪柝聲')errors.push('speaker without featured video did not switch channel');
   if(!(await page.locator('[data-pawson-play]').isHidden()))errors.push('speaker without verified video exposes play button');
   // Verify the player configuration and that switching clears the previous embed.
   await selectSpeaker('大衛鮑森');
   await page.locator('[data-pawson-play]').click();
   const firstEmbed=await page.locator('[data-pawson-preview]').getAttribute('src');
   if(!firstEmbed?.includes('/embed/fizg-bxIjuY?'))errors.push('Pawson first curated episode mismatch');
   if(!firstEmbed?.includes('enablejsapi=1')||!firstEmbed?.includes('origin='))errors.push('YouTube iframe API parameters missing');
   // Switching via the canonical rail must tear down the prior embed.
   await selectSpeaker('江秀琴');
   if(await page.locator('[data-pawson-preview]').getAttribute('src'))errors.push('previous player not cleared on speaker change');
   if(!(await page.locator('[data-pawson-preview]').isHidden()))errors.push('old iframe remains visible after speaker change');
   if((await page.locator('.olive-feature__caption h2').innerText())!=='江秀琴')errors.push('speaker rail failed to switch channel');
   console.log(size.name+': '+(errors.length?errors.join('; '):'PASS'));
   if(errors.length)process.exitCode=1;
   await page.close();
  }
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1});
