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
    if(cards.length!==11)errors.push('expected 11 rail cards plus David Pawson hero; got '+cards.length);
    if(!document.querySelector('[data-feature-next]')||!document.querySelector('[data-feature-prev]'))errors.push('rotation controls missing');
    if(!document.querySelector('[data-feature-source]'))errors.push('video source link missing');
    if(!document.querySelector('#olive-sermon-experience')||!document.querySelector('#olive-archive-experience'))errors.push('journey sections missing');
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
